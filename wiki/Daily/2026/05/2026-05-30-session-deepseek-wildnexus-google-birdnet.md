---
date: 2026-05-30
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-30 — session-deepseek-wildnexus-google-birdnet

## Session — 11:34 — session-deepseek-wildnexus-google-birdnet

### Contexte
- Modèle : deepseek
- Projet : WILDNEXUS

### Résumé
Session DeepSeek TUI v0.8.39. Diagnostic erreur Google OAuth 403 (JCH-PKA en mode Testing). Changement langue BirdNET-Pi DATABASE_LANG en→fr sur le RPi tkajch + regénération labels + redémarrage services. Documentation procédure dans BIRDNET_PI_ACCESS.md.

### Actions
Expliqué cause erreur 403 Google (écran consentement OAuth Testing), procédure résolution. Connecté SSH sur RPi BirdNET-Pi (100.84.45.93), modifié DATABASE_LANG=fr dans /etc/birdnet/birdnet.conf, exécuté install_language_label.sh, redémarré services birdnet_*. Ajouté section 'Changer la langue' dans BIRDNET_PI_ACCESS.md.

### Décisions
DATABASE_LANG=fr validé pour BirdNET-Pi. Procédure documentée pour futurs déploiements.

### Prochaines étapes
Vérifier projet Google Cloud JCH-PKA et pka-calandar-bridge — ajouter test users ou publier l'app OAuth.
