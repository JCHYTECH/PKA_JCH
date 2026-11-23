---
date: 2026-11-23
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-23 — Consolidation mail + consentement Graph arteon.be + modèles M1 restaurés

## Session — 23:36 — Consolidation mail + consentement Graph arteon.be + modèles M1 restaurés

### Contexte
- Modèle : deepseek-v4-pro
- Projet : 01_AI_IT_TOOLS

### Résumé
Nettoyage des flux mail OAuth morts (email_digest, gmail_gatekeeper, outlook_gatekeeper, outlook_imap) archivés dans _local/archives/mail-oauth-dead-2026-11-23/ ; réponse Orban45 préparée pour le consentement Graph lecture seule sur arteon.be (app 31f92869, client_id corrigé 14d82eec erroné) ; restauration des 3 modèles Ollama cœur du M1 (qwen2.5:32b, codestral:22b, llama3.2:3b) -> 10 modèles / 85 Go. Règle durable ajoutée : toujours donner le chemin complet d'un fichier.

### Actions
Archivage 21 fichiers OAuth morts ; vérif socle IMAP vivant (gmail_imap_digest --list OK, 3 non-lus) ; correction client_id Graph + permissions réduites en lecture seule sur l'app Azure ; rédaction reponse-orban45-2026-11-23.md + captures Azure vérifiées par OCR ; relance 3 pulls Ollama M1 en nohup + validation inférence (llama3.2:3b 2,3s, codestral:22b 15s) ; règle chemin d'accès ajoutée à SOUL.md + AGENTS.md.

### Décisions
Périmètre Graph réduit en lecture seule (Mail.Read, Calendars.Read, Contacts.Read, User.Read) — Mail.Send et écritures retirés ; garder Graph + forward Gmail (les 2 demandés à Orban) ; roster M1 maintenu à 10 (qwen2.5-coder 14b/32b et gemma3:27b jugés redondants, non re-téléchargés).

### Prochaines étapes
Attendre le consentement admin d'Orban45 (Roman Dillen) sur l'app 31f92869 + autorisation du forward externe ; puis re-cocher la règle forward Outlook et tester ; forwarder Yahoo vers Gmail côté Yahoo (sans Orban) ; optionnel : tirer gemma3:27b si le projet Cozmo démarre.
