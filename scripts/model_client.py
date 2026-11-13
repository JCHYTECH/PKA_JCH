#!/usr/bin/env python3
"""
model_client.py
Forge 🦦 — Client unifié PKA. Lit model_config.json et retourne le bon client.
Usage : from model_client import get_client, get_model
"""

import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / "model_config.json"


def _load_config() -> dict:
    return json.loads(CONFIG_PATH.read_text())


def get_task_config(task: str) -> dict:
    """Retourne {provider, model} pour une tâche donnée."""
    cfg = _load_config()
    return cfg["tasks"].get(task, cfg["default"])


def get_model(task: str) -> str:
    return get_task_config(task)["model"]


def _get_api_key(provider_cfg: dict) -> str:
    key_env = provider_cfg.get("key_env")
    if key_env and os.environ.get(key_env):
        return os.environ[key_env]

    key_file = provider_cfg.get("key_file")
    if key_file:
        path = Path(key_file.replace("~", str(Path.home())))
        if path.exists():
            return path.read_text().strip()

    if key_env or key_file:
        locations = []
        if key_env:
            locations.append(f"${key_env}")
        if key_file:
            locations.append(key_file)
        raise RuntimeError(f"API key missing. Configure one of: {', '.join(locations)}")

    return provider_cfg.get("api_key", "none")


def get_client(task: str):
    """
    Retourne un client prêt à l'emploi pour la tâche.
    - anthropic  → anthropic.Anthropic()
    - openai     → openai.OpenAI()
    - google     → google.generativeai configuré
    - ollama     → openai.OpenAI(base_url=..., api_key="ollama")
    """
    cfg = _load_config()
    task_cfg = cfg["tasks"].get(task, cfg["default"])
    provider = task_cfg["provider"]
    provider_cfg = cfg["providers"][provider]

    if provider == "anthropic":
        import anthropic
        key_file = Path(provider_cfg["key_file"].replace("~", str(Path.home())))
        api_key = key_file.read_text().strip()
        return anthropic.Anthropic(api_key=api_key)

    if provider not in ("anthropic", "google"):
        # tous les providers OpenAI-compatibles (openai, ollama, kimi, deepseek…)
        import openai
        api_key = _get_api_key(provider_cfg)
        kwargs = {"api_key": api_key}
        if provider_cfg.get("base_url"):
            kwargs["base_url"] = provider_cfg["base_url"]
        return openai.OpenAI(**kwargs)

    if provider == "google":
        import google.generativeai as genai
        key_file = Path(provider_cfg["key_file"].replace("~", str(Path.home())))
        api_key = key_file.read_text().strip()
        genai.configure(api_key=api_key)
        return genai

    raise ValueError(f"Provider inconnu : {provider}")


def chat(task: str, messages: list[dict], system: str = None, **kwargs) -> str:
    """
    Interface unifiée : envoie messages au modèle de la tâche, retourne le texte.
    messages = [{"role": "user", "content": "..."}]
    """
    cfg = get_task_config(task)
    provider = cfg["provider"]
    model = cfg["model"]
    client = get_client(task)

    if provider == "anthropic":
        params = {"model": model, "max_tokens": kwargs.get("max_tokens", 4096), "messages": messages}
        if system:
            params["system"] = system
        response = client.messages.create(**params)
        return response.content[0].text

    if provider not in ("anthropic", "google"):
        all_messages = []
        if system:
            all_messages.append({"role": "system", "content": system})
        all_messages.extend(messages)
        response = client.chat.completions.create(
            model=model,
            messages=all_messages,
            max_tokens=kwargs.get("max_tokens", 4096),
        )
        return response.choices[0].message.content

    if provider == "google":
        import google.generativeai as genai
        gmodel = genai.GenerativeModel(model, system_instruction=system)
        history = []
        for m in messages[:-1]:
            role = "user" if m["role"] == "user" else "model"
            history.append({"role": role, "parts": [m["content"]]})
        chat_session = gmodel.start_chat(history=history)
        response = chat_session.send_message(messages[-1]["content"])
        return response.text

    raise ValueError(f"Provider inconnu : {provider}")


if __name__ == "__main__":
    import sys
    task = sys.argv[1] if len(sys.argv) > 1 else "default"
    cfg = get_task_config(task)
    print(f"Tâche '{task}' → {cfg['provider']} / {cfg['model']}")
