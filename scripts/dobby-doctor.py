#!/usr/bin/env python3
"""
dobby-doctor.py — Diagnostic des clés API PKA.
Teste toutes les clés configurées et produit un rapport de santé.
Usage : python3 scripts/dobby-doctor.py
"""
import os
import sys
import subprocess
import json
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError

PKA_DIR = Path(__file__).resolve().parent.parent
HOME = Path.home()
CONFIG_DIR = HOME / ".config" / "pka-jch"

# Couleurs terminal
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
BOLD = "\033[1m"
RESET = "\033[0m"

def ok(msg="OK"):
    return f"{GREEN}{msg}{RESET}"

def fail(msg="ÉCHEC"):
    return f"{RED}{msg}{RESET}"

def warn(msg):
    return f"{YELLOW}{msg}{RESET}"

def bold(msg):
    return f"{BOLD}{msg}{RESET}"

# ── Tests API ─────────────────────────────────────────────────────────────────

def test_endpoint(name, url, key, headers_extra=None, ok_status=200):
    """Test générique : GET url avec Bearer token. Retourne (status, message)."""
    headers = {"Authorization": f"Bearer {key}"}
    if headers_extra:
        headers.update(headers_extra)
    try:
        req = Request(url, headers=headers)
        resp = urlopen(req, timeout=10)
        return (True, f"{resp.status} — {name} répond")
    except HTTPError as e:
        body = e.read().decode(errors="replace")[:200]
        return (False, f"{e.code} — {body}")
    except URLError as e:
        return (False, f"Erreur réseau : {e.reason}")
    except Exception as e:
        return (False, str(e))


def test_deepseek():
    key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not key:
        key_file = CONFIG_DIR / "api_keys"
        if key_file.exists():
            for line in key_file.read_text().splitlines():
                if line.startswith("DEEPSEEK_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        return (False, "Clé non définie (ni env, ni api_keys)")
    return test_endpoint("DeepSeek", "https://api.deepseek.com/v1/models", key)


def test_kimi():
    key_file = CONFIG_DIR / "kimi_key.txt"
    if not key_file.exists():
        return (False, f"Fichier introuvable : {key_file}")
    key = key_file.read_text().strip()
    if not key:
        return (False, "Fichier vide")
    return test_endpoint("Kimi (Moonshot)", "https://api.moonshot.ai/v1/models", key)


def test_openrouter():
    key_file = CONFIG_DIR / "openrouter_key.txt"
    if not key_file.exists():
        return (False, f"Fichier introuvable : {key_file}")
    key = key_file.read_text().strip()
    if not key:
        return (False, "Fichier vide")
    # OpenRouter renvoie les crédits restants
    ok_status, msg = test_endpoint("OpenRouter", "https://openrouter.ai/api/v1/auth/key", key)
    if ok_status:
        try:
            req = Request("https://openrouter.ai/api/v1/auth/key",
                          headers={"Authorization": f"Bearer {key}"})
            data = json.loads(urlopen(req, timeout=10).read())
            credits = data.get("data", {}).get("credits", "?")
            return (True, f"Crédits restants : {credits}")
        except:
            return (True, msg)
    return (False, msg)


def test_gemini():
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        return (False, "GEMINI_API_KEY non définie")
    # Gemini n'utilise pas Bearer, on teste avec ?key=
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models?key={key}"
        req = Request(url)
        resp = urlopen(req, timeout=10)
        return (True, f"{resp.status} — Gemini répond")
    except HTTPError as e:
        body = e.read().decode(errors="replace")[:200]
        return (False, f"{e.code} — {body}")
    except Exception as e:
        return (False, str(e))


def test_anthropic():
    """Teste la config Anthropic (ant auth)."""
    try:
        result = subprocess.run(["ant", "auth", "status"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for line in result.stdout.splitlines():
                if "expires:" in line:
                    return (True, line.strip())
            return (True, "Profil OAuth actif")
        return (False, result.stderr.strip() or result.stdout.strip())
    except FileNotFoundError:
        return (False, "ant CLI non installé")
    except Exception as e:
        return (False, str(e))


def test_nvidia():
    key = os.environ.get("NVIDIA_API_KEY", "")
    if not key:
        # chercher dans api_keys
        key_file = CONFIG_DIR / "api_keys"
        if key_file.exists():
            for line in key_file.read_text().splitlines():
                if line.startswith("NVIDIA_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        return (False, "NVIDIA_API_KEY non définie")
    return test_endpoint("NVIDIA NIM", "https://integrate.api.nvidia.com/v1/models", key)


def test_openai():
    key = os.environ.get("OPENAI_API_KEY", "")
    if not key:
        key_file = CONFIG_DIR / "api_keys"
        if key_file.exists():
            for line in key_file.read_text().splitlines():
                if line.startswith("OPENAI_API_KEY="):
                    key = line.split("=", 1)[1].strip()
                    break
    if not key:
        return (False, "OPENAI_API_KEY non définie")
    return test_endpoint("OpenAI", "https://api.openai.com/v1/models", key)


def test_ollama():
    """Vérifie si Ollama tourne en local."""
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            models = [l.split()[0] for l in result.stdout.strip().splitlines()[1:] if l.strip()]
            return (True, f"Modèles locaux : {', '.join(models)}" if models else "Aucun modèle installé")
        return (False, result.stderr.strip())
    except FileNotFoundError:
        return (False, "Ollama non installé")
    except Exception as e:
        return (False, str(e))


# ── Diagnostic principal ──────────────────────────────────────────────────────

def main():
    print(f"\n{bold('🩺 Dobby Doctor — Diagnostic API PKA')}")
    print(f"   {PKA_DIR}\n")

    tests = [
        ("DeepSeek API", test_deepseek),
        ("Kimi (Moonshot)", test_kimi),
        ("OpenRouter", test_openrouter),
        ("Anthropic (Claude)", test_anthropic),
        ("Gemini", test_gemini),
        ("NVIDIA NIM", test_nvidia),
        ("OpenAI", test_openai),
        ("Ollama (local)", test_ollama),
    ]

    ok_count = 0
    fail_count = 0
    warn_count = 0

    for name, fn in tests:
        try:
            status, msg = fn()
        except Exception as e:
            status, msg = False, str(e)

        if status:
            symbol = f"{GREEN}✔{RESET}"
            ok_count += 1
        else:
            if "401" in msg or "403" in msg or "Invalid" in msg or "expir" in msg.lower():
                symbol = f"{RED}✘{RESET}"
                fail_count += 1
            else:
                symbol = f"{YELLOW}⚠{RESET}"
                warn_count += 1

        print(f"  {symbol} {bold(name):<22s} {msg}")

    print(f"\n  {bold('Résultat')} : ", end="")
    parts = []
    if ok_count: parts.append(f"{GREEN}{ok_count} OK{RESET}")
    if warn_count: parts.append(f"{YELLOW}{warn_count} avertissement(s){RESET}")
    if fail_count: parts.append(f"{RED}{fail_count} échec(s){RESET}")
    print(" · ".join(parts))

    # Résumé des actions
    if fail_count > 0:
        print(f"\n  {RED}⚠ Clés à renouveler :{RESET}")
        if not test_kimi()[0]:
            print(f"    → Kimi : https://console.moonshot.cn → nouvelle clé → ~/.config/pka-jch/kimi_key.txt")
        if not test_deepseek()[0]:
            print(f"    → DeepSeek : https://platform.deepseek.com/api_keys → ~/.config/pka-jch/api_keys")
        if not test_openai()[0]:
            print(f"    → OpenAI : https://platform.openai.com/api-keys → ~/.config/pka-jch/api_keys")
        if not test_nvidia()[0]:
            print(f"    → NVIDIA : https://build.nvidia.com → ~/.config/pka-jch/api_keys")
    if warn_count > 0:
        print(f"\n  {YELLOW}⚠ Points d'attention :{RESET}")
        if not test_gemini()[0]:
            print(f"    → Gemini : clé dans ~/.zshrc (export GEMINI_API_KEY)")

    print()

if __name__ == "__main__":
    main()
