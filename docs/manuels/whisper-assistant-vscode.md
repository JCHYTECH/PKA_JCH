# Whisper Assistant VS Code — Guide de fonctionnement

> Dernière mise à jour : 2026-07-08 — Dobby 🦉
> Statut : ✅ Opérationnel (français, insertion unique)

---

## Architecture

```
VS Code (Whisper Assistant v1.2.4, patchée)
  │
  │ 1. Ctrl+M → toggle recording
  │    → ffmpeg -f avfoundation -i :1 (MacBook Pro Microphone)
  │    → WAV 16kHz mono s16
  │
  │ 2. Ctrl+M → stop → POST localhost:4444/v1/audio/transcriptions
  │    → Authorization: Bearer localhost-key-must-be-set
  │    → response_format=verbose_json (hardcodé par l'extension)
  │
  ▼
whisper-server.py (Flask, launchd, KeepAlive)
  │
  │ 3. faster-whisper base (CTranslate2, CPU int8)
  │    → langue fr forcée (ignore le language=en de l'extension)
  │    → beam_size=5
  │
  │ 4. Retour verbose_json : {task, language, duration, text, segments}
  │
  ▼
speech-transcription.js (patché)
  │
  │ 5. Insertion directe via editor.edit() ou fallback clipboard paste
  │    → return undefined (évite le double insert par extension.js)
  │
  ▼
Texte inséré dans l'éditeur actif
```

## Composants

| Composant | Rôle | Emplacement |
|-----------|------|-------------|
| `whisper-server.py` | Serveur Flask OpenAI-compatible | `_local/whisper-server.py` |
| `com.dobby.whisper-server.plist` | Auto-start + restart (launchd) | `~/Library/LaunchAgents/` |
| `martinopensky.whisper-assistant` v1.2.4 | Extension VS Code (patchée) | `.vscode/extensions/` |
| `ffmpeg` 8.1.1 | Capture audio (AVFoundation, `:1` = MacBook Pro Microphone) | `/opt/homebrew/bin/ffmpeg` |
| Modèle `base` (Systran/faster-whisper-base) | Transcription CPU int8, fr | `~/.cache/huggingface/` |

## Settings VS Code

```json
"whisper-assistant.apiProvider": "localhost",
"whisper-assistant.apiKey": "localhost-key-must-be-set",
"whisper-assistant.customEndpoint": "http://localhost:4444",
"whisper-assistant.customRecordingCommand": "ffmpeg -y -f avfoundation -i :1 -ac 1 -ar 16000 -sample_fmt s16 $AUDIO_FILE"
```

## Usage

1. Ouvrir VS Code avec un fichier texte
2. Placer le curseur dans l'éditeur
3. `Ctrl+M` → parler en français
4. `Ctrl+M` → le texte transcrit est inséré

⚠️ **Ne pas utiliser `Ctrl+Shift+S`** — ce n'est pas le bon raccourci. Le binding par défaut est `Ctrl+M`.

## Patches appliqués à l'extension (v1.2.4)

### Patch 1 — `speech-transcription.js`
**Problème** : L'extension utilise `clipboardPasteAction` qui ne marche pas toujours + `language=en` hardcodé.
**Patch** : Insertion directe via `editor.edit()` + retour `undefined` pour éviter le double insert par `extension.js`.
**Sauvegarde** : `extension.js.bak` (fichier original).

### Patch 2 — `whisper-server.py`
**Problème** : L'extension envoie `response_format=verbose_json` mais le serveur ne retournait que `{"text": "..."}`.
**Patch** : Support complet de `verbose_json` (task, language, duration, text, segments).
**Patch** : Langue forcée à `fr` — ignore le `language=en` envoyé par l'extension.

## Gestion du serveur

```bash
# Statut
curl http://localhost:4444/health

# Redémarrer
launchctl unload ~/Library/LaunchAgents/com.dobby.whisper-server.plist
launchctl load ~/Library/LaunchAgents/com.dobby.whisper-server.plist

# Logs
tail -f _local/logs/whisper-server.err

# Tuer un ffmpeg orphelin
ps aux | grep "ffmpeg.*whisper-assistant" | grep -v grep | awk '{print $2}' | xargs kill -9
```

## Problèmes connus et résolutions (session 2026-07-08)

| Problème | Cause | Fix |
|----------|-------|-----|
| Transcription vide | Serveur ne retournait pas `verbose_json` | `whisper-server.py` modifié |
| Texte en anglais | Extension hardcode `language=en` | Serveur force `fr` |
| Texte en double | `speech-transcription.js` + `extension.js` inséraient tous les deux | Patch retourne `undefined` |
| `s` tapé au lieu d'enregistrer | Mauvais raccourci (`Ctrl+Shift+S` au lieu de `Ctrl+M`) | Utiliser `Ctrl+M` |
| iPhone se connecte | `:0` = JCH Microphone (Bluetooth) au lieu du micro built-in | `:1` = MacBook Pro Microphone |
| ffmpeg zombie | Process non tué après arrêt enregistrement | `kill -9` manuel |
| `-sample_fmt s16` manquant | Recording command incomplète | Settings VS Code corrigés |

## Améliorations futures (non bloquantes)

- **Modèle `small` (244M)** : meilleure précision française. Téléchargement HuggingFace bloqué par xet-read-token. Retenter avec `HF_HUB_DISABLE_XET=1`.
- **Insertion directe** : actuellement le fallback clipboard paste fonctionne, mais `editor=NULL` indique que le focus n'est pas dans un éditeur au moment de l'insertion. Investiguer.

## Voir aussi

- [[SOP-006|SOP-006 — Travail Obsidian + VS Code]]
- Session 2026-05-25 — diagnostic initial (speech timeout, MCP loop, disable AI)
