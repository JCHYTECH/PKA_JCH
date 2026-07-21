#!/usr/bin/env python3
"""
deepseek_chat.py — Agent Dobby avec outils (API OpenAI-compatible).
Chargé par dobby.sh --model deepseek|kimi|openrouter
Support multi-provider via PKA_POINTER / PKA_PROVIDER / DEEPSEEK_BASE_URL

Outils disponibles : read_file, list_dir, grep_files, exec_shell, write_file
"""
import os
import sys
import json
import subprocess
import re
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parent.parent

try:
    from openai import OpenAI
except ImportError:
    print("❌ openai SDK manquant — installer : pip install openai")
    sys.exit(1)

# ── Configuration ──────────────────────────────────────────────

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    print("❌ DEEPSEEK_API_KEY non définie.")
    sys.exit(1)

MODEL    = os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash")
POINTER  = os.environ.get("PKA_POINTER", "DEEPSEEK.md")
PROVIDER = os.environ.get("PKA_PROVIDER", "DeepSeek")
BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

MAX_TOOL_OUTPUT = 8000   # caractères max par résultat d'outil
SHELL_TIMEOUT   = 30     # secondes max pour une commande shell

# ── System prompt ──────────────────────────────────────────────

def load_system_prompt():
    """Charge le system prompt complet selon dobby-memory-bootstrap.md."""
    parts = []
    # Runtime context
    parts.append(f"# Runtime: {PROVIDER}\n# Model: {MODEL}\n# PKA Provider: OpenRouter-compatible API\n\n")
    # Phase 1 — Config (identité, immuable)
    for fname, label in [
        ("ADAPTER-PROMPT.md", "Bootstrap universel PKA"),
        (POINTER, "Pointer spécifique outil"),
        ("SOUL.md", "Personnalité & règles"),
        ("USER.md", "Profil JCH"),
        ("TEAM/dobby.md", "Persona complet Dobby"),
    ]:
        fpath = PKA_DIR / fname
        if fpath.exists():
            if label:
                parts.append(f"\n\n---\n## {fname} ({label})\n---\n")
            parts.append(fpath.read_text())
    # Phase 2 — Log (contexte, historique)
    for fname, label in [
        ("MEMORY.md", "Connaissances accumulées"),
    ]:
        fpath = PKA_DIR / fname
        if fpath.exists():
            if label:
                parts.append(f"\n\n---\n## {fname} ({label})\n---\n")
            parts.append(fpath.read_text())
    # Phase 2+ — Bootstrap instructions (protocole Phase 2→5)
    bootstrap_path = PKA_DIR / "BOOTSTRAP.md"
    if bootstrap_path.exists():
        parts.append(f"\n\n---\n## BOOTSTRAP.md (Protocole démarrage session)\n---\n")
        parts.append(bootstrap_path.read_text())
    return "".join(parts)

system_prompt = load_system_prompt() or "You are Dobby 🦉, PKA orchestrator for Jean-Claude."

# ── Outils ─────────────────────────────────────────────────────

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Lire un fichier du workspace PKA. Retourne le contenu texte.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif au workspace PKA (ex: MEMORY.md, JCH_Inbox/03_PROJECTS/)"
                    },
                    "max_lines": {
                        "type": "integer",
                        "description": "Nombre max de lignes à retourner (défaut: 200, max: 500)"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "Lister le contenu d'un dossier du workspace PKA.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif au workspace PKA (ex: ., JCH_Inbox/00_INBOX)"
                    }
                },
                "required": ["path"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "grep_files",
            "description": "Rechercher un motif (regex) dans les fichiers du workspace PKA.",
            "parameters": {
                "type": "object",
                "properties": {
                    "pattern": {
                        "type": "string",
                        "description": "Expression régulière à chercher"
                    },
                    "path": {
                        "type": "string",
                        "description": "Dossier ou fichier où chercher (relatif au workspace, défaut: '.')"
                    },
                    "include": {
                        "type": "string",
                        "description": "Glob pour filtrer les fichiers (ex: '*.md,*.py')"
                    }
                },
                "required": ["pattern"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "exec_shell",
            "description": "Exécuter une commande shell dans le workspace PKA. Timeout: 30s. ⚠️ Éviter les commandes destructrices (rm -rf, force push, etc.).",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string",
                        "description": "Commande shell à exécuter"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Écrire/créer un fichier dans le workspace PKA. ⚠️ Écrase le contenu existant. À utiliser avec parcimonie, seulement quand JCH le demande.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Chemin relatif au workspace PKA"
                    },
                    "content": {
                        "type": "string",
                        "description": "Contenu du fichier"
                    }
                },
                "required": ["path", "content"]
            }
        }
    }
]

# ── Exécution des outils ───────────────────────────────────────

def safe_path(relpath: str) -> Path:
    """Résout un chemin relatif dans PKA_DIR et vérifie qu'il ne sort pas du workspace."""
    resolved = (PKA_DIR / relpath).resolve()
    if not str(resolved).startswith(str(PKA_DIR)):
        raise ValueError(f"⛔ Chemin hors workspace : {relpath}")
    return resolved

def tool_read_file(path: str, max_lines: int = 200) -> str:
    fp = safe_path(path)
    if not fp.exists():
        return f"❌ Fichier introuvable : {path}"
    if fp.is_dir():
        return f"❌ {path} est un dossier, pas un fichier."
    try:
        text = fp.read_text()
    except Exception as e:
        return f"❌ Erreur lecture : {e}"
    lines = text.split('\n')
    total = len(lines)
    max_lines = min(max_lines, 500)
    if total <= max_lines:
        return f"📄 {path} ({total} lignes) :\n{text}"
    else:
        truncated = '\n'.join(lines[:max_lines])
        return f"📄 {path} ({total} lignes, {max_lines} affichées) :\n{truncated}\n... (tronqué)"

def tool_list_dir(path: str = ".") -> str:
    fp = safe_path(path)
    if not fp.exists():
        return f"❌ Dossier introuvable : {path}"
    if not fp.is_dir():
        return f"❌ {path} n'est pas un dossier."
    try:
        entries = sorted(fp.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
    except PermissionError:
        return f"❌ Permission refusée : {path}"
    lines = []
    for e in entries:
        tag = "📁" if e.is_dir() else "📄"
        lines.append(f"  {tag} {e.name}")
    return f"📁 {path} ({len(entries)} entrées) :\n" + '\n'.join(lines)

def tool_grep_files(pattern: str, path: str = ".", include: str = None) -> str:
    fp = safe_path(path)
    if not fp.exists():
        return f"❌ Introuvable : {path}"
    try:
        regex = re.compile(pattern)
    except re.error as e:
        return f"❌ Regex invalide : {e}"
    
    results = []
    files_to_search = []
    if fp.is_file():
        files_to_search = [fp]
    else:
        for root, dirs, files in os.walk(fp):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '.git', '__pycache__', '.venv', 'venv')]
            for fname in files:
                if fname.startswith('.'):
                    continue
                if include:
                    patterns = [p.strip() for p in include.split(',')]
                    if not any(Path(fname).match(p) for p in patterns):
                        continue
                files_to_search.append(Path(root) / fname)
    
    for fpath in files_to_search[:500]:  # max 500 files
        try:
            for i, line in enumerate(fpath.read_text().split('\n'), 1):
                if regex.search(line):
                    rel = fpath.relative_to(PKA_DIR)
                    results.append(f"  {rel}:{i}: {line.strip()[:120]}")
                    if len(results) >= 50:
                        break
        except Exception:
            pass
        if len(results) >= 50:
            break
    
    if not results:
        return f"🔍 Aucun résultat pour '{pattern}' dans {path}"
    
    count = len(results)
    if count >= 50:
        return f"🔍 {count}+ résultats pour '{pattern}' dans {path} (50 premiers) :\n" + '\n'.join(results)
    return f"🔍 {count} résultat(s) pour '{pattern}' dans {path} :\n" + '\n'.join(results)

def tool_exec_shell(command: str) -> str:
    # Bloque les commandes manifestement dangereuses
    dangerous = ['rm -rf /', 'mkfs.', 'dd if=', '> /dev/sda', ':(){ :|:& };:']
    for d in dangerous:
        if d in command:
            return f"⛔ Commande bloquée (dangereuse) : {command}"
    
    try:
        result = subprocess.run(
            command,
            shell=True,
            cwd=str(PKA_DIR),
            capture_output=True,
            text=True,
            timeout=SHELL_TIMEOUT
        )
        out = result.stdout[:MAX_TOOL_OUTPUT]
        err = result.stderr[:2000]
        rc = result.returncode
        parts = []
        if out:
            parts.append(out)
        if err:
            parts.append(f"[stderr] {err}")
        if rc != 0:
            parts.append(f"[exit code: {rc}]")
        return '\n'.join(parts) if parts else f"[commande exécutée, pas de sortie]"
    except subprocess.TimeoutExpired:
        return f"⏱️ Commande timeout après {SHELL_TIMEOUT}s : {command}"
    except Exception as e:
        return f"❌ Erreur exécution : {e}"

def tool_write_file(path: str, content: str) -> str:
    fp = safe_path(path)
    try:
        fp.parent.mkdir(parents=True, exist_ok=True)
        fp.write_text(content)
        return f"✅ Fichier écrit : {path} ({len(content)} caractères)"
    except Exception as e:
        return f"❌ Erreur écriture : {e}"

def execute_tool(name: str, args: dict) -> str:
    """Route l'appel d'outil vers la bonne fonction."""
    try:
        if name == "read_file":
            return tool_read_file(args["path"], args.get("max_lines", 200))
        elif name == "list_dir":
            return tool_list_dir(args.get("path", "."))
        elif name == "grep_files":
            return tool_grep_files(args["pattern"], args.get("path", "."), args.get("include"))
        elif name == "exec_shell":
            return tool_exec_shell(args["command"])
        elif name == "write_file":
            return tool_write_file(args["path"], args["content"])
        else:
            return f"❌ Outil inconnu : {name}"
    except ValueError as e:
        return str(e)
    except Exception as e:
        return f"❌ Erreur outil {name} : {e}"

# ── Client ─────────────────────────────────────────────────────

client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
history = [{"role": "system", "content": system_prompt}]

print(f"🐶 Dobby — {PROVIDER} ({MODEL})")
print(f"   PKA : {PKA_DIR}")
print(f"   Outils : read_file, list_dir, grep_files, exec_shell, write_file")
print(f"   Tape 'exit' ou Ctrl+C pour quitter.\n")

# ── Activation ─────────────────────────────────────────────────

pointer_name = POINTER.replace(".md", "")
history.append({"role": "user", "content": f"Activation Dobby via {pointer_name} — confirme ta présence."})
try:
    resp = client.chat.completions.create(model=MODEL, messages=history)
    msg = resp.choices[0].message
    if msg.content:
        history.append({"role": "assistant", "content": msg.content})
        print(f"Dobby : {msg.content}\n")
    else:
        print("Dobby : (activé)\n")
except Exception as e:
    print(f"❌ Erreur API : {e}")
    sys.exit(1)

# ── REPL avec outils ───────────────────────────────────────────

def chat_loop():
    while True:
        try:
            user_input = input("JCH : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSession fermée.")
            break
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "/exit"):
            print("Session fermée.")
            break
        
        history.append({"role": "user", "content": user_input})
        
        # Boucle outil : on itère tant que le modèle demande des outils
        while True:
            try:
                resp = client.chat.completions.create(
                    model=MODEL,
                    messages=history,
                    tools=TOOLS,
                    tool_choice="auto"
                )
            except Exception as e:
                print(f"❌ Erreur API : {e}")
                # Retire le dernier message user pour ne pas bloquer
                history.pop()
                break
            
            msg = resp.choices[0].message
            
            if msg.tool_calls:
                # Le modèle veut utiliser des outils
                history.append(msg)
                
                for tc in msg.tool_calls:
                    tool_name = tc.function.name
                    try:
                        tool_args = json.loads(tc.function.arguments)
                    except json.JSONDecodeError:
                        tool_args = {}
                    
                    print(f"  🔧 {tool_name}({json.dumps(tool_args, ensure_ascii=False)[:100]})")
                    result = execute_tool(tool_name, tool_args)
                    
                    # Truncate si trop long
                    if len(result) > MAX_TOOL_OUTPUT:
                        result = result[:MAX_TOOL_OUTPUT] + "\n... (tronqué)"
                    
                    history.append({
                        "role": "tool",
                        "tool_call_id": tc.id,
                        "content": result
                    })
                
                # Continue la boucle — le modèle va répondre avec le résultat des outils
                continue
            
            else:
                # Réponse texte finale
                content = msg.content or ""
                history.append({"role": "assistant", "content": content})
                print(f"\nDobby : {content}\n")
                break

chat_loop()
