---
name: dobby-voice
description: Interface vocale de Dobby — dictée (Whisper) et conversation native (Gemini Live, voix Ursa). Déclencher sur "dictée", "transcris", "voix", "parle à Dobby", "conversation vocale".
---

# Skill — dobby-voice

Interface vocale de Dobby. Deux modes complémentaires, plus la maintenance des clés.

## Déclencheur
- « dictée », « transcris ça », « prends la dictée » → mode Whisper
- « parle à Dobby », « conversation vocale », « voix Ursa » → mode Gemini Live

## Mode 1 — Dictée (Whisper)
Transcription voix → texte, collé dans le terminal.
```bash
scripts/whisper-dictate.sh            # enregistre, transcrit, colle
scripts/whisper-dictate.sh --print    # affiche au lieu de coller
```
- Nécessite : `ffmpeg`, `curl`, `jq` + serveur `whisper-server.py` sur `localhost:4444`
  (`launchctl load ~/Library/LaunchAgents/com.dobby.whisper-server.plist`).

## Mode 2 — Conversation native (Gemini Live)
Conversation vocale temps réel, audio natif — pas de Whisper, pas de TTS séparé.
```bash
bin/dobby-voice        # → scripts/gemini_voice.py (voix Ursa)
```
- Entrée : PCM 16 bits / 16 kHz (micro) · Sortie : PCM 16 bits / 24 kHz (voix Ursa)
- Arrêt : `Ctrl+C`
- Réglages (env) : `GEMINI_VOICE` (défaut `Ursa`), `MIC_DEVICE` (défaut `:1`)

## Maintenance
- `scripts/rotate_gemini_key.sh` — rotation des clés API Gemini (`~/.config/pka-jch/api_keys`)

## Voir aussi
- `_local/whisper-server.py` — serveur de transcription local
- `docs/system/` — setup voix/Gemini
