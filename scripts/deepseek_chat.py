#!/usr/bin/env python3
"""
deepseek_chat.py — Session interactive DeepSeek (API OpenAI-compatible).
Chargé par dobby.sh --model deepseek
"""
import os
import sys
from pathlib import Path

PKA_DIR = Path(__file__).resolve().parent.parent

try:
    from openai import OpenAI
except ImportError:
    print("❌ openai SDK manquant — installer : pip install openai")
    sys.exit(1)

API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
if not API_KEY:
    print("❌ DEEPSEEK_API_KEY non définie.")
    sys.exit(1)

MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")

# Charge le system prompt depuis DEEPSEEK.md
system_file = PKA_DIR / "DEEPSEEK.md"
system_prompt = system_file.read_text() if system_file.exists() else "You are Dobby, PKA orchestrator."

client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com/v1")
history = [{"role": "system", "content": system_prompt}]

print(f"🐶 Dobby — DeepSeek ({MODEL})")
print(f"   PKA : {PKA_DIR}")
print(f"   Tape 'exit' ou Ctrl+C pour quitter.\n")

# Activation
history.append({"role": "user", "content": "Activation Dobby — confirme ta présence."})
try:
    resp = client.chat.completions.create(model=MODEL, messages=history)
    msg = resp.choices[0].message.content
    history.append({"role": "assistant", "content": msg})
    print(f"Dobby : {msg}\n")
except Exception as e:
    print(f"❌ Erreur API : {e}")
    sys.exit(1)

# REPL
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
    try:
        resp = client.chat.completions.create(model=MODEL, messages=history)
        msg = resp.choices[0].message.content
        history.append({"role": "assistant", "content": msg})
        print(f"\nDobby : {msg}\n")
    except Exception as e:
        print(f"❌ Erreur : {e}")
