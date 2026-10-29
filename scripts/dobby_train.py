#!/usr/bin/env python3
"""
dobby_train.py  🦉  — Pipeline de fine-tuning LoRA pour Dobby

Génère un dataset d'entraînement à partir des transcripts PKA et des patterns
extraits par dobby_retro.py, puis fine-tune un modèle via MLX pour spécialiser
la voix et les connaissances de Dobby.

Usage :
    python3 scripts/dobby_train.py --build-dataset          # Générer le dataset seulement
    python3 scripts/dobby_train.py                          # Build + train
    python3 scripts/dobby_train.py --model Qwen/Qwen2.5-7B-Instruct
    python3 scripts/dobby_train.py --train-only             # Reprendre entraînement
    python3 scripts/dobby_train.py --export-gguf            # Exporter vers GGUF

Prérequis : pip install mlx mlx-lm transformers sentencepiece
"""

import json
import os
import sqlite3
import subprocess
import sys
import time
from collections import Counter
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

# ── CONFIG ──────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent
PKA_DIR = BASE_DIR.parent
DB_PATH = PKA_DIR / "TEAM" / "team.db"
MODEL_DIR = PKA_DIR / "_local" / "dobby-models"
LORA_DIR = PKA_DIR / "_local" / "dobby-lora"
DATASET_DIR = PKA_DIR / "_local" / "dobby-dataset"

# Modèle de base (HF, M5 compatible avec 16GB RAM)
# Qwen2.5-7B-Instruct: 7.6B paramètres, bon rapport qualité/taille
# Gemma-4-9B-IT: plus récent mais plus lourd
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct-1M"

# Configuration LoRA
LORA_CONFIG = {
    "lora_rank": 8,
    "lora_alpha": 16,
    "lora_dropout": 0.05,
    "lora_layers": 24,        # nombre de couches LoRA (toutes les couches attention)
    "num_epochs": 3,
    "batch_size": 4,
    "learning_rate": 1e-4,
    "max_seq_length": 2048,
    "steps_per_report": 10,
    "save_every": 100,
}

INSTRUCTION_TEMPLATE = """### Instruction
{instruction}

### Response
{response}"""

DEFAULT_RETRO_INSTRUCTION = "Analyse les patterns de travail dans les sessions PKA et identifie les décisions, échecs et tendances."

# ── DATASET BUILDER ────────────────────────────────────────────────────

def build_dataset(days: int = 30) -> list[dict]:
    """Construit un dataset d'entraînement depuis team.db et transcripts."""
    print(f"[Dataset] Construction depuis {days} jours de données…")
    samples = []

    # 1. Retro patterns → instruction pairs
    samples.extend(_build_from_retro_patterns(days))
    print(f"[Dataset] {len(samples)} samples depuis retro_patterns")

    # 2. Retro sessions → full retro examples
    samples.extend(_build_from_retro_reports(days))
    print(f"[Dataset] {len(samples)} samples depuis retro_reports")

    # 3. Recent transcripts → contexte JCH
    samples.extend(_build_from_transcripts(days))
    print(f"[Dataset] {len(samples)} samples depuis transcripts")

    return samples


def _build_from_retro_patterns(days: int = 30) -> list[dict]:
    """Transforme les patterns stockés en paires instruction/réponse."""
    samples = []
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()

        # Vérifier si la table existe
        c.execute("SELECT name FROM sqlite_master WHERE name='retro_patterns'")
        if not c.fetchone():
            conn.close()
            return samples

        cutoff = (date.today() - timedelta(days=days)).isoformat()
        c.execute(
            "SELECT pattern_type, content, date, session_count FROM retro_patterns WHERE date >= ? ORDER BY date",
            (cutoff,),
        )
        rows = c.fetchall()
        conn.close()

        # Grouper par type de pattern pour créer des instructions significatives
        by_type: dict[str, list[str]] = {}
        for ptype, content, d, sc in rows:
            if ptype not in by_type:
                by_type[ptype] = []
            by_type[ptype].append(content[:300])

        instructions_map = {
            "decision": "Voici des décisions récentes extraites des sessions PKA. Synthétise-les.",
            "failure": "Voici des échecs et bloqueurs détectés dans les sessions PKA. Analyse les causes racines.",
            "question": "Voici des questions posées pendant les sessions PKA. Sont-elles le signe d'une lacune documentaire ?",
            "recurring_question": "Ces questions reviennent fréquemment dans les sessions. Propose des solutions pour les anticiper.",
        }

        for ptype, items in by_type.items():
            instruction = instructions_map.get(ptype, f"Analyse ces patterns de type '{ptype}'.")
            if items:
                response_lines = []
                for item in items[:15]:
                    response_lines.append(f"- {item}")
                response = "\n".join(response_lines)
                samples.append({
                    "instruction": instruction,
                    "response": response,
                    "source": "retro_patterns",
                    "type": ptype,
                })
    except (OSError, sqlite3.DatabaseError) as e:
        print(f"[Dataset] Erreur DB retro_patterns: {e}")

    return samples


def _build_from_retro_reports(days: int = 30) -> list[dict]:
    """Utilise les rapports de rétro existants comme exemples."""
    samples = []
    retro_dir = PKA_DIR / "wiki" / "Daily"

    cutoff = (date.today() - timedelta(days=days)).isoformat()
    try:
        for md_file in sorted(retro_dir.rglob("*-dobby-retro.md"), reverse=True):
            # Extract date from filename
            fname = md_file.stem  # e.g. "2026-06-05-dobby-retro"
            file_date = fname[:10]

            if file_date < cutoff:
                continue

            content = md_file.read_text(encoding="utf-8")

            # Extract the YAML frontmatter and the retro body
            parts = content.split("---\n", 2)
            body = parts[2] if len(parts) >= 3 else content
            body = body.strip()

            if len(body) < 100:
                continue

            samples.append({
                "instruction": "Produis une rétrospective quotidienne des sessions PKA.",
                "response": body[:2500],
                "source": "retro_report",
                "type": "retro",
                "date": file_date,
            })
    except Exception as e:
        print(f"[Dataset] Erreur retro_reports: {e}")

    return samples


def _extract_text(content: str | list) -> str:
    """Extrait le texte d'un message, qu'il soit str ou list."""
    if isinstance(content, str):
        return content.strip()
    elif isinstance(content, list):
        parts = [c.get("text", "") for c in content
                 if isinstance(c, dict) and c.get("type") == "text"]
        return " ".join(parts).strip()
    return ""


def _build_from_transcripts(days: int = 30) -> list[dict]:
    """Extrait des paires Question/Réponse des transcripts récents."""
    samples = []
    sessions_dir = Path.home() / ".deepseek" / "sessions"

    if not sessions_dir.is_dir():
        return samples

    cutoff = datetime.now() - timedelta(days=days)

    for fpath in sorted(sessions_dir.glob("*.json"),
                        key=lambda f: f.stat().st_mtime, reverse=True):
        mtime = datetime.fromtimestamp(fpath.stat().st_mtime)
        if mtime < cutoff:
            break

        try:
            with open(fpath) as f:
                data = json.load(f)
        except (json.JSONDecodeError, OSError):
            continue

        messages = data.get("messages", [])
        model = data.get("metadata", {}).get("model", "unknown")

        # Extraire paires : chaque user suivi de l'assistant
        user_text = None
        for msg in messages:
            role = msg.get("role", "")
            content = _extract_text(msg.get("content", ""))
            if not content:
                continue

            if role == "user":
                user_text = content[:500]
            elif role == "assistant" and user_text:
                # Créer une instruction à partir du message utilisateur
                if any(kw in user_text.lower() for kw in
                       ["analyse", "évalue", "regarde", "vérifie",
                        "check", "review", "explique", "compare",
                        "décris", "résume", "synthétise", "propose",
                        "que penses", "recommande", "optimise"]):
                    samples.append({
                        "instruction": user_text[:400],
                        "response": content[:1500],
                        "source": "deepseek_transcript",
                        "type": "analysis",
                        "model": model,
                    })
                user_text = None

    return samples


def format_dataset(samples: list[dict]) -> list[dict]:
    """Formate les samples au format attendu par mlx-lm."""
    formatted = []
    for s in samples:
        text = INSTRUCTION_TEMPLATE.format(
            instruction=s["instruction"],
            response=s["response"],
        )
        formatted.append({
            "text": text,
            "source": s.get("source", "unknown"),
            "type": s.get("type", "generic"),
        })
    return formatted


def save_dataset(samples: list[dict], split_ratio: float = 0.9):
    """Sauvegarde le dataset en JSONL (train + valid)."""
    DATASET_DIR.mkdir(parents=True, exist_ok=True)

    # Split
    split = int(len(samples) * split_ratio)
    train = samples[:split]
    valid = samples[split:] if len(samples) > 1 else []

    def write_jsonl(data: list[dict], path: Path):
        with open(path, "w") as f:
            for item in data:
                f.write(json.dumps({"text": item["text"]}, ensure_ascii=False) + "\n")

    write_jsonl(train, DATASET_DIR / "train.jsonl")
    if valid:
        write_jsonl(valid, DATASET_DIR / "valid.jsonl")
    else:
        # Si pas assez de données, copier train comme valid
        write_jsonl(train[:1], DATASET_DIR / "valid.jsonl")

    print(f"[Dataset] Train: {len(train)} samples → {DATASET_DIR / 'train.jsonl'}")
    if valid:
        print(f"[Dataset] Valid: {len(valid)} samples → {DATASET_DIR / 'valid.jsonl'}")

    # Stats
    total_chars = sum(len(s["text"]) for s in train)
    types = Counter(s.get("type", "?") for s in samples)
    print(f"[Dataset] Stats: {total_chars} chars, types: {dict(types)}")

    return DATASET_DIR


# ── TRAINING ───────────────────────────────────────────────────────────

def train_lora():
    """Lance le fine-tuning LoRA via mlx-lm."""
    train_file = DATASET_DIR / "train.jsonl"
    valid_file = DATASET_DIR / "valid.jsonl"

    if not train_file.exists():
        print("[Train] Dataset introuvable. Lance --build-dataset d'abord.")
        return False

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    LORA_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[Train] Modèle: {DEFAULT_MODEL}")
    print(f"[Train] LoRA rank: {LORA_CONFIG['lora_rank']}")
    print(f"[Train] Epochs: {LORA_CONFIG['num_epochs']}")
    print(f"[Train] Batch size: {LORA_CONFIG['batch_size']}")
    print(f"[Train] Max seq length: {LORA_CONFIG['max_seq_length']}")
    print()

    # Utiliser mlx-lm.lora.train_or_eval (CLI)
    cmd = [
        sys.executable, "-m", "mlx_lm.lora",
        "--model", DEFAULT_MODEL,
        "--train",
        "--data", str(DATASET_DIR),
        "--adapter-path", str(LORA_DIR),
        "--lora-layers", str(LORA_CONFIG["lora_layers"]),
        "--batch-size", str(LORA_CONFIG["batch_size"]),
        "--iters", str(LORA_CONFIG["num_epochs"] * 100),  # approx
        "--val-batches", "10",
        "--learning-rate", str(LORA_CONFIG["learning_rate"]),
        "--steps-per-report", str(LORA_CONFIG["steps_per_report"]),
        "--steps-per-eval", "50",
        "--save-every", str(LORA_CONFIG["save_every"]),
        "--max-seq-length", str(LORA_CONFIG["max_seq_length"]),
        "--seed", "42",
    ]

    print("[Train] Lancement…")
    print(f"  {' '.join(cmd)}")
    print()

    start = time.time()
    result = subprocess.run(cmd, cwd=str(PKA_DIR))
    elapsed = time.time() - start

    if result.returncode == 0:
        print(f"\n[Train] ✅ Fine-tuning terminé en {elapsed:.0f}s")
        print(f"  Adaptateurs LoRA → {LORA_DIR}")
        return True
    else:
        print(f"\n[Train] ❌ Échec (exit {result.returncode}) après {elapsed:.0f}s")
        return False


# ── EXPORT ─────────────────────────────────────────────────────────────

def export_gguf():
    """Exporte le modèle + adaptateurs vers GGUF pour Ollama."""
    gguf_dir = PKA_DIR / "_local" / "dobby-gguf"
    gguf_dir.mkdir(parents=True, exist_ok=True)

    if not (LORA_DIR / "adapters.safetensors").exists():
        print("[Export] Aucun adaptateur LoRA trouvé. Entraîne d'abord.")
        return False

    # Fusionner adaptateurs dans le modèle
    merged_dir = PKA_DIR / "_local" / "dobby-merged"
    merged_dir.mkdir(parents=True, exist_ok=True)

    cmd = [
        sys.executable, "-m", "mlx_lm.fuse",
        "--model", DEFAULT_MODEL,
        "--adapter-path", str(LORA_DIR),
        "--save-path", str(merged_dir),
    ]
    print("[Export] Fusion LoRA → modèle complet…")
    print(f"  {' '.join(cmd)}")

    result = subprocess.run(cmd, cwd=str(PKA_DIR))
    if result.returncode != 0:
        print("[Export] ❌ Fusion échouée")
        return False

    print(f"[Export] ✅ Modèle fusionné → {merged_dir}")

    # Vérifier si llama.cpp est disponible pour la conversion GGUF
    which_llama = subprocess.run("which llama-quantize 2>/dev/null || which llama.cpp-convert 2>/dev/null || echo NOT_FOUND",
                                 shell=True, capture_output=True, text=True)

    if "NOT_FOUND" in which_llama.stdout:
        print("[Export] llama.cpp non trouvé — modèle disponible en HF format. Pour GGUF :")
        print(f"  1. git clone https://github.com/ggerganov/llama.cpp")
        print(f"  2. python llama.cpp/convert.py {merged_dir} --outfile {gguf_dir}/dobby-q4_k_m.gguf")
        print(f"  3. Ollama: ollama create dobby -f /path/to/Modelfile")
    else:
        convert_tool = which_llama.stdout.strip()
        gguf_out = gguf_dir / "dobby-q4_k_m.gguf"
        cmd = [convert_tool, str(merged_dir), "--outfile", str(gguf_out), "--outtype", "q4_k_m"]
        print(f"[Export] Conversion GGUF: {' '.join(cmd)}")
        subprocess.run(cmd, cwd=str(PKA_DIR))

    return True


# ── CLI ───────────────────────────────────────────────────────────────

def main():
    args = {
        "build_only": False,
        "train_only": False,
        "export_only": False,
        "model": DEFAULT_MODEL,
        "days": 30,
        "all": False,
    }

    i = 0
    argv = sys.argv[1:]
    while i < len(argv):
        a = argv[i]
        if a == "--build-dataset":
            args["build_only"] = True
        elif a == "--train-only":
            args["train_only"] = True
        elif a == "--export-gguf":
            args["export_only"] = True
        elif a == "--model" and i + 1 < len(argv):
            args["model"] = argv[i + 1]
            i += 1
        elif a in ("--days", "-d") and i + 1 < len(argv):
            args["days"] = int(argv[i + 1])
            i += 1
        elif a == "--all":
            args["all"] = True
            args["days"] = 365
        i += 1

    if args["export_only"]:
        export_gguf()
        return

    if not args["train_only"]:
        print("=" * 60)
        print("  Dobby 🦉 — Fine-tuning Pipeline")
        print("=" * 60)
        print()

        samples = build_dataset(days=args["days"])
        formatted = format_dataset(samples)
        print(f"\n[Pipeline] {len(formatted)} samples formatés")

        if len(formatted) < 5:
            print("[Pipeline] Dataset trop petit (< 5 samples). Ajoute --days 60 ou vérifie les sources.")
            return

        save_dataset(formatted)

        if args["build_only"]:
            print("[Pipeline] Dataset généré. Pour entraîner : python3 dobby_train.py")
            return

    else:
        if not (DATASET_DIR / "train.jsonl").exists():
            print("[Pipeline] Dataset manquant. Lance --build-dataset d'abord.")
            return

    # Train
    success = train_lora()
    if success and not args["train_only"]:
        print()
        print("[Pipeline] Prochaine étape : python3 dobby_train.py --export-gguf")


if __name__ == "__main__":
    main()
