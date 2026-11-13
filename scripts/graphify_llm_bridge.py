#!/usr/bin/env python3
"""
graphify_llm_bridge — Extraction sémantique pour graphify via Ollama (M1).

Lit les fichiers non-code du workspace, envoie leur contenu à Ollama sur M1
pour extraction de concepts + relations, et produit un fichier JSON compatible
avec le pipeline graphify (build → cluster → report).

Usage:
    python3 scripts/graphify_llm_bridge.py                    # workspace courant
    python3 scripts/graphify_llm_bridge.py --dir docs/system  # dossier spécifique
    python3 scripts/graphify_llm_bridge.py --model qwen3:30b-a3b  # modèle spécifique
    python3 scripts/graphify_llm_bridge.py --dry-run          # affiche sans sauver
    python3 scripts/graphify_llm_bridge.py --max-files 10     # limite le nombre de fichiers
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from typing import Any
from urllib import request, error

# ── Configuration ────────────────────────────────────────────────────────────

OLLAMA_HOST = "http://100.73.212.110:11434"
DEFAULT_MODEL = "qwen2.5-coder:14b"  # Bon compromis vitesse/qualité
MAX_CHARS_PER_FILE = 8000             # Tronque les fichiers longs
MAX_CHARS_PER_BATCH = 12000           # Max contexte par requête Ollama
FILES_PER_BATCH = 3                   # Fichiers par lot

# Extensions considérées comme "non-code" (analyse sémantique)
DOC_EXTENSIONS = {".md", ".txt", ".yaml", ".yml", ".toml", ".json", ".csv", ".html", ".css"}

# Fichiers/dossiers à ignorer
SKIP_PATTERNS = [
    "graphify-out", "node_modules", ".git", "__pycache__",
    ".DS_Store", "package-lock.json", "*.min.js", "*.min.css",
    "session_*.json", "*.bak-*",
]

# ── Prompt d'extraction ──────────────────────────────────────────────────────

EXTRACTION_PROMPT = """You are a knowledge graph extractor. Analyze the document(s) below and extract key concepts and their relationships.

For each concept, provide:
- id: unique snake_case identifier (prefix with file-derived short slug)
- label: human-readable name
- type: one of [project, technology, person, idea, process, tool, config, file, concept]

For each relationship, provide:
- source_id: id of the source concept
- target_id: id of the target concept
- relation: one of [uses, depends_on, part_of, related_to, references, implements, configures, documents]
- confidence: float between 0.5 and 0.95 (how sure you are about this relationship)

Rules:
- Extract only meaningful, specific concepts (not generic words)
- Prefer 5-15 concepts per document
- Every concept mentioned in a relationship MUST be in the concepts list
- Skip relationships that are trivial or obvious from file structure

Return ONLY valid JSON, no explanation, in this exact format:
{
  "concepts": [
    {"id": "ex_react", "label": "React", "type": "technology"},
    {"id": "ex_dobby", "label": "Dobby", "type": "person"}
  ],
  "relationships": [
    {"source_id": "ex_dobby", "target_id": "ex_react", "relation": "uses", "confidence": 0.85}
  ]
}

Documents to analyze:
---
{DOCUMENTS}
---

JSON output:"""


# ── Helpers ──────────────────────────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert text to snake_case slug."""
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def file_slug(filepath: Path) -> str:
    """Generate a short unique prefix from a file path."""
    name = filepath.stem.lower()
    name = re.sub(r"[^a-z0-9]+", "_", name)[:20]
    h = hashlib.md5(str(filepath).encode()).hexdigest()[:4]
    return f"{name}_{h}"


def should_skip(path: Path) -> bool:
    """Check if a file should be skipped."""
    path_str = str(path)
    for pattern in SKIP_PATTERNS:
        if pattern in path_str:
            return True
    return False


def collect_doc_files(root: Path) -> list[Path]:
    """Collect non-code files for semantic extraction."""
    files = []
    for ext in DOC_EXTENSIONS:
        for p in root.rglob(f"*{ext}"):
            if should_skip(p):
                continue
            if p.suffix not in DOC_EXTENSIONS:
                continue
            # Skip files that are clearly code (heuristic)
            if p.suffix in {".json"} and p.stat().st_size > 50_000:
                continue  # Probablement un data file, pas un doc
            files.append(p)
    return sorted(files)


def read_file_safe(filepath: Path, max_chars: int = MAX_CHARS_PER_FILE) -> str | None:
    """Read a file, return None if binary or unreadable."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return None
    if len(content) > max_chars:
        # Prendre début + fin pour garder le contexte
        half = max_chars // 2
        content = content[:half] + "\n\n[... truncated ...]\n\n" + content[-half:]
    return content


def call_ollama(prompt: str, model: str = DEFAULT_MODEL) -> dict | None:
    """Send a prompt to Ollama and return parsed JSON response."""
    # Certains modèles (thinking, MoE) ignorent `format: json`
    use_json_format = "thinking" not in model.lower() and "r1" not in model.lower()
    
    # Thinking models need more token budget (thinking + answer)
    is_thinking = "thinking" in model.lower() or "r1" in model.lower()
    num_predict = 8192 if is_thinking else 4096
    
    payload_dict: dict = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": num_predict,
        },
    }
    if use_json_format:
        payload_dict["format"] = "json"
    
    # For thinking models, skip thinking content and parse only the final answer
    if is_thinking:
        payload_dict["enable_thinking"] = False  # Try to disable if supported
    
    payload = json.dumps(payload_dict).encode("utf-8")

    url = f"{OLLAMA_HOST}/api/generate"
    req = request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with request.urlopen(req, timeout=180) as resp:
            body = json.loads(resp.read().decode("utf-8"))
            raw_response = body.get("response", "")
            # For thinking models, the answer may be in `response` (after thinking)
            # or in `thinking` if tokens ran out. Prefer `response`, fallback to `thinking`.
            if not raw_response.strip():
                raw_response = body.get("thinking", "")
    except error.URLError as e:
        print(f"  ⚠️  Ollama unreachable: {e}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"  ⚠️  Ollama error: {e}", file=sys.stderr)
        return None

    # Parse JSON from response (handle markdown code blocks)
    # Try ```json ... ``` blocks first, then bare JSON
    code_block = re.search(r"```(?:json)?\s*(\{[\s\S]*?\})\s*```", raw_response)
    if code_block:
        raw_json = code_block.group(1)
    else:
        json_match = re.search(r"\{[\s\S]*\}", raw_response)
        if not json_match:
            print(f"  ⚠️  No JSON found — raw: {raw_response[:300]}...", file=sys.stderr)
            return None
        raw_json = json_match.group(0)

    try:
        return json.loads(raw_json)
    except json.JSONDecodeError as e:
        print(f"  ⚠️  Invalid JSON: {e} — raw: {raw_json[:300]}...", file=sys.stderr)
        return None


# ── Core extraction ──────────────────────────────────────────────────────────

def extract_batch(
    files: list[tuple[Path, str]],
    model: str,
    batch_num: int,
    total_batches: int,
) -> dict:
    """Extract concepts + relationships from a batch of files."""
    docs_text = []
    for fpath, content in files:
        rel = str(fpath)
        docs_text.append(f"### FILE: {rel}\n```\n{content}\n```\n")

    prompt = EXTRACTION_PROMPT.replace("{DOCUMENTS}", "\n".join(docs_text))
    print(f"  Batch {batch_num}/{total_batches}: {len(files)} fichiers → Ollama/{model}...", end=" ", flush=True)

    result = call_ollama(prompt, model)
    if result is None:
        print("FAILED")
        return {"concepts": [], "relationships": []}

    n_concepts = len(result.get("concepts", []))
    n_rels = len(result.get("relationships", []))
    print(f"→ {n_concepts} concepts, {n_rels} relations")
    return result


def transform_to_graphify(
    batch_result: dict,
    file_lookup: dict[str, Path],
    prefix: str,
) -> tuple[list[dict], list[dict]]:
    """Transform Ollama extraction into graphify-compatible nodes/edges."""
    nodes = []
    edges = []

    concept_map: dict[str, str] = {}  # llm_id → graphify_node_id

    for c in batch_result.get("concepts", []):
        raw_id = c.get("id", "")
        if not raw_id:
            continue
        gid = f"sem_{prefix}_{slugify(raw_id)}"
        concept_map[raw_id] = gid

        # Trouver le fichier source
        source_file = ""
        label_lower = c.get("label", "").lower()
        # Heuristique : associer au fichier dont le nom correspond le mieux
        for fname, fpath in file_lookup.items():
            if slugify(fname) in slugify(raw_id) or slugify(raw_id) in slugify(fname):
                source_file = str(fpath)
                break

        nodes.append({
            "id": gid,
            "label": c.get("label", raw_id),
            "file_type": "document",
            "source_file": source_file,
            "source_location": "",
            "_origin": "semantic",
            "norm_label": slugify(c.get("label", raw_id)),
        })

    for r in batch_result.get("relationships", []):
        src_id = r.get("source_id", "")
        tgt_id = r.get("target_id", "")
        if src_id not in concept_map or tgt_id not in concept_map:
            continue
        confidence = max(0.5, min(0.95, float(r.get("confidence", 0.7))))
        edges.append({
            "source": concept_map[src_id],
            "target": concept_map[tgt_id],
            "relation": r.get("relation", "related_to"),
            "confidence": "INFERRED",
            "confidence_score": confidence,
            "source_file": "",
            "source_location": "",
            "weight": confidence,
        })

    return nodes, edges


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="graphify LLM bridge — Ollama/M1")
    parser.add_argument("--dir", default=".", help="Dossier à analyser")
    parser.add_argument("--model", default=DEFAULT_MODEL, help="Modèle Ollama")
    parser.add_argument("--dry-run", action="store_true", help="Affiche sans sauver")
    parser.add_argument("--max-files", type=int, default=0, help="Limite le nombre de fichiers")
    parser.add_argument("--skip", type=int, default=0, help="Saute les N premiers fichiers")
    parser.add_argument("--output", default="graphify-out/semantic_extraction.json", help="Fichier de sortie")
    parser.add_argument("--merge", action="store_true", help="Fusionner avec le graph existant après extraction")
    parser.add_argument("--merge-graph", default="graphify-out/graph.json", help="Chemin du graph.json à merger")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild clustering + report après merge")
    args = parser.parse_args()

    root = Path(args.dir).resolve()
    print(f"🔍 Scan des fichiers non-code dans {root}...")
    files = collect_doc_files(root)
    print(f"   {len(files)} fichiers trouvés")

    if args.skip:
        files = files[args.skip:]
        print(f"   Skip {args.skip}, reste {len(files)} fichiers")
    if args.max_files and args.max_files < len(files):
        files = files[: args.max_files]
        print(f"   Limité à {args.max_files} fichiers")

    if not files:
        print("   Aucun fichier à traiter.")
        return

    # Lire tous les fichiers
    file_contents: list[tuple[Path, str]] = []
    skipped = 0
    for fp in files:
        content = read_file_safe(fp)
        if content and len(content.strip()) > 50:  # Ignorer fichiers quasi-vides
            file_contents.append((fp, content))
        else:
            skipped += 1

    print(f"   {len(file_contents)} fichiers lisibles ({skipped} ignorés — binaires/vides)")

    # Grouper en batches
    batches = []
    current_batch = []
    current_chars = 0
    for fp, content in file_contents:
        if current_chars + len(content) > MAX_CHARS_PER_BATCH and current_batch:
            batches.append(current_batch)
            current_batch = []
            current_chars = 0
        current_batch.append((fp, content))
        current_chars += len(content)
    if current_batch:
        batches.append(current_batch)

    total_batches = len(batches)
    print(f"\n📦 {total_batches} lots à traiter via Ollama ({args.model})\n")

    all_nodes = []
    all_edges = []
    all_node_ids: set[str] = set()

    for i, batch in enumerate(batches, 1):
        file_lookup = {fp.stem: fp for fp, _ in batch}
        prefix = file_slug(batch[0][0]) if batch else "unknown"

        result = extract_batch(batch, args.model, i, total_batches)
        nodes, edges = transform_to_graphify(result, file_lookup, prefix)

        # Déduplication des nœuds par ID
        for n in nodes:
            if n["id"] not in all_node_ids:
                all_node_ids.add(n["id"])
                all_nodes.append(n)
        all_edges.extend(edges)

    print(f"\n✅ Total: {len(all_nodes)} concepts sémantiques, {len(all_edges)} relations INFERRED")

    output = {
        "nodes": all_nodes,
        "edges": all_edges,
        "metadata": {
            "model": args.model,
            "files_processed": len(file_contents),
            "batches": total_batches,
            "generated_by": "graphify_llm_bridge",
        },
    }

    out_path = Path(args.output)
    if args.dry_run:
        print(f"\n📋 DRY-RUN — premier nœud: {json.dumps(all_nodes[0], indent=2)[:300] if all_nodes else 'N/A'}")
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"📄 Sauvé dans {out_path}")

    if args.merge:
        merge_semantic(Path(args.merge_graph), out_path, rebuild=args.rebuild)

    if not args.merge:
        print("\n💡 Pour merger avec le graph existant :")
        print(f"   python3 scripts/graphify_llm_bridge.py --merge {out_path}")


def merge_semantic(graph_path: Path, semantic_path: Path, rebuild: bool = False):
    """Merge semantic nodes/edges into existing graph.json and optionally rebuild."""
    if not graph_path.exists():
        print(f"⚠️  Graph introuvable: {graph_path}", file=sys.stderr)
        return
    if not semantic_path.exists():
        print(f"⚠️  Extraction sémantique introuvable: {semantic_path}", file=sys.stderr)
        return

    print(f"\n🔗 Fusion de {semantic_path.name} → {graph_path.name}...")

    with open(graph_path) as f:
        graph = json.load(f)
    with open(semantic_path) as f:
        semantic = json.load(f)

    existing_ids = {n["id"] for n in graph.get("nodes", [])}
    new_nodes = 0
    for n in semantic.get("nodes", []):
        if n["id"] not in existing_ids:
            existing_ids.add(n["id"])
            graph.setdefault("nodes", []).append(n)
            new_nodes += 1

    # Déduplication des edges (source+target+relation)
    existing_edge_keys = {
        (e["source"], e["target"], e.get("relation", ""))
        for e in graph.get("links", [])
    }
    new_edges = 0
    for e in semantic.get("edges", []):
        key = (e["source"], e["target"], e.get("relation", ""))
        if key not in existing_edge_keys:
            existing_edge_keys.add(key)
            graph.setdefault("links", []).append(e)
            new_edges += 1

    print(f"   +{new_nodes} nœuds sémantiques, +{new_edges} edges INFERRED")

    # Sauver
    graph_path.write_text(json.dumps(graph, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"   ✅ {graph_path} mis à jour")

    if rebuild:
        print("\n🔄 Reconstruction du graphe (clustering + report)...")
        rebuild_graph(graph_path.parent.parent)


def rebuild_graph(root: Path):
    """Run graphify rebuild (clustering + report) via _rebuild_graph.py."""
    import subprocess

    rebuild_script = Path(__file__).resolve().parent / "_rebuild_graph.py"
    if not rebuild_script.exists():
        print("   ⚠️  _rebuild_graph.py introuvable, rebuild manuel requis", file=sys.stderr)
        return

    result = subprocess.run(
        ["python3", str(rebuild_script)],
        capture_output=True, text=True, timeout=120, cwd=str(root),
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)


if __name__ == "__main__":
    main()
