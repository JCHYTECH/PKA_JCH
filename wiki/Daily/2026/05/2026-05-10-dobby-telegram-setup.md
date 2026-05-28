---
date: 2026-05-10
tags: [daily]
type: daily
status: active
---

# 2026-05-10 — [[Dobby]] Telegram Bot + Équipe PKA

## Actions

- Transfert JCH Vault → PKA_JCH analysé et complété (fichiers dupliqués ou manquants traités)
- Déplacement fichiers techniques photo : API GBIF → 
- 26 tâches [[Obsidian]] archivées → 
- NUANCES (BESS) configuré : wiki 4 domaines (techniques/installation/concurrence/legal) posé, projet en standby
- [[Argus]] enrichi : analyse série/portfolio, score par concours, print-readiness, pipelines [[Héron]]/[[Nova]]/[[Miel]]/[[Corbeau]]
- Template profil myICOR inspiré créé (`TEAM/PROFIL-TEMPLATE.md`) : tagline, credo, persona, hobbies, collaboration narrée
- Profils enrichis : [[Forge]], [[Castor]], [[Corbeau]], [[Pie]] (myICOR-style)
- Dashboards mis à jour : hub.html (6 liens ARTEON cassés corrigés, [[Argus]]+[[Pie]] ajoutés, 24 membres) + organigramme.html (v15, NUANCES standby)
- [[Dobby]] renommé 🦉 → 🐶 Chihuahua ([[Claude]].md, TEAM/[[Dobby]].md, hub.html, organigramme.html, dobby_context.py)
- Bot Telegram [[Dobby]] créé et déployé : 
- Service launchd `com.pka.dobby` installé et opérationnel (KeepAlive, RunAtLoad, venv isolé)
- Bot Telegram validé : `/start` → réponse confirmée

## Décisions

- Canal de communication temps réel : **Telegram** retenu (API bot mature, voix native, gratuit, accès fichiers PKA local)
- Hosting bot : **Mac local** (accès nécessaire à team.db et JCH_Inbox)
- Presets [[Argus]] séparés des plugins : presets-argus/ = outputs liés aux photos, plugins/ = outils réutilisables
- Chihuahua [[Dobby]] = le vrai chien de JCH → identité plus personnelle et attachante

## Actions (session 2 — TTS Telegram)

- Intégration OpenAI TTS dans 
- `strip_markdown()` ajouté pour nettoyer le texte avant envoi TTS
- Commande `/vocal on|off` ajoutée pour basculer vocal/texte à la volée
- 
- `.env` enrichi : `OPENAI_TTS_VOICE=nova`, `TTS_ALSO_SEND_TEXT=false`
- Diagnostic launchd : `com.pka.dobby` identifié comme gestionnaire du bot (KeepAlive)
- Procédure de redémarrage propre établie : `launchctl unload/load`
- TTS validé en production : réponses vocales [[Nova]] opérationnelles

## Décisions (session 2)

- Provider TTS retenu : **OpenAI TTS** (déjà intégré, clé existante, 13 voix, multilingue)
- Voix retenue : **[[Nova]]** (par défaut, modifiable via 
- Mode : **vocal uniquement** (`TTS_ALSO_SEND_TEXT=false`) — pas de doublon texte
- Restart bot : toujours via `launchctl unload/load` — jamais `kill` + `python &`

## Actions (session 3 — CarPlay & AirPods)

- `TTS_ENABLED` ajouté comme variable d'env dans `bot.py` (lecture au démarrage)
- 
- iOS configuré : Announce Notifications → All Notifications pour Telegram
- Flux CarPlay validé : [[Dobby]] répond texte → Siri lit automatiquement
- Flux AirPods identique — fonctionne partout hors voiture

## Décisions (session 3)

- Mode par défaut : **texte** (`TTS_ENABLED=false`) — optimisé CarPlay/AirPods
- Voix [[Nova]] disponible à la demande : 
- Envoi vocal → toujours via micro Telegram (Siri ne peut pas envoyer à un bot Telegram)

## Prochaine étape

- Retrofitting des 19 profils équipe restants avec le nouveau template myICOR
- Tester autres voix OpenAI si [[Nova]] ne convient pas
