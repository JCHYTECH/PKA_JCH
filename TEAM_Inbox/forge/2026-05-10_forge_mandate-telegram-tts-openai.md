# Brief Forge — Réponses vocales Dobby via Telegram (OpenAI TTS)

**Date :** 2026-05-10  
**De :** Dobby  
**À :** Forge 🦦  
**Priorité :** Normale

---

## Contexte

Le bot Telegram de Dobby reçoit déjà des messages texte et vocaux de JCH et répond en texte. L'objectif est d'ajouter la capacité de répondre en **message vocal** en utilisant l'API TTS d'OpenAI.

---

## Objectif

Quand Dobby génère une réponse texte sur Telegram, la convertir en audio via OpenAI TTS et l'envoyer en **voice message** (format `.ogg` Opus, standard Telegram).

---

## Spécifications techniques

### API OpenAI TTS
- Endpoint : `POST https://api.openai.com/v1/audio/speech`
- Modèle recommandé : `tts-1` (latence faible) ou `tts-1-hd` (qualité supérieure)
- Format de sortie : `opus` (natif Telegram voice)
- Voix : à choisir parmi les 13 disponibles — **laisser configurable via une variable d'environnement** `OPENAI_TTS_VOICE`

### Comportement attendu
1. Dobby génère sa réponse texte (comportement actuel inchangé)
2. Le texte est envoyé à OpenAI TTS → retourne un fichier audio `.ogg`
3. Le bot envoie le fichier via `sendVoice` (Telegram Bot API)
4. **Option** : envoyer aussi le texte en parallèle (`sendMessage`) pour accessibilité

### Déclenchement
- **Par défaut** : toujours répondre en vocal
- **OU** : ajouter une commande `/vocal on|off` pour que JCH puisse basculer

### Variables d'environnement à ajouter
```
OPENAI_TTS_VOICE=nova          # voix par défaut (configurable)
OPENAI_TTS_MODEL=tts-1        # ou tts-1-hd
TTS_ALSO_SEND_TEXT=true       # envoyer aussi le texte écrit
```

---

## Livrables attendus

1. Code d'intégration TTS dans le pipeline Telegram existant
2. Variable `OPENAI_TTS_VOICE` configurable sans redéploiement
3. Test confirmé : JCH envoie un message → Dobby répond en vocal sur Telegram

---

## Notes

- La clé `OPENAI_API_KEY` est déjà en place (utilisée pour le LLM) — vérifier si elle couvre aussi le TTS ou si un quota séparé s'applique.
- Attention à la limite de taille Telegram pour les voice messages (max 50 MB — largement suffisant pour des réponses texte converties).
- Prévoir un fallback texte si l'appel TTS échoue.
