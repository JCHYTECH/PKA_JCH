---
date: 2026-05-09
slug: audit-structure-adapter-prompt-wiki
tags: [daily]
type: daily
status: active
---

# 2026-05-09 — Audit structure, ADAPTER-PROMPT, wiki

## Actions

- **Tour de la structure PKA_JCH** — renommages détectés et corrigés dans les .md : `01_HUB` → `01_DASHBOARDS`, `02_COMPANY` → `02_COMPANY_JCH`, `05_CONTEXT` → `05_CONTEXT_JCH`, `04_KNOWLEDGE` supprimé de l'index
- **[[Argus]] #23 + [[Pie]] #24 ajoutés** dans 
- **Typo chemin DB corrigée** dans [[Claude]].md : 
- **`wiki/index.md` nettoyé** — 6 catégories fantômes supprimées (seules AI-Tools et Daily existaient réellement)
- **`ADAPTER-PROMPT.md` créé** à la racine — bootstrap universel pour activer PKA_JCH dans n'importe quel LLM, adapté de myPKA (Paperless Movement) avec notre architecture réelle
- **Convention journal myPKA adoptée** — `wiki/Daily/YYYY/MM/YYYY-MM-DD-slug.md` ; 3 fichiers plats migrés avec slugs thématiques ; `sybil.md` mis à jour
- **Import myPKA Team Knowledge** — structure SOPs / Workstreams / Guidelines créée dans `wiki/` :
  - `GL-001-conventions-nommage.md`
  - `SOP-001-onboarding-nouveau-specialiste.md`
  - `WS-001-journal-quotidien.md`
  - INDEX.md pour chaque section ; `wiki/index.md` mis à jour
- **[[Sybil]] (#15)** confirmée comme équivalent Penn (myPKA) — pas de recrutement nécessaire
- **Audit qualité global PKA_JCH** — scan complet y compris dossiers cachés
- **Clé API Anthropic révoquée et renouvelée** — clé en clair trouvée ligne 40 de `.claude/settings.local.json` (dans une permission Bash historique)
- **`.claude/settings.local.json` nettoyé** — 70 permissions one-shot supprimées → 20 génériques récurrentes conservées ; hooks SessionStart + Stop maintenus
- **Nettoyage fichiers parasites** : `team.db copy` supprimé, `contexte_photo/` (dossier vide) supprimé, 29 `.DS_Store` supprimés

## Décisions

- **`.claude/` justifié pour les hooks uniquement** — SessionStart (/prime) et Stop (/save) restent utiles ; les permissions historiques n'ont pas vocation à s'accumuler
- **Convention myPKA adoptée pour le journal** — structure YYYY/MM/ + slug thématique, plus robuste pour la mémoire et l'indexation
- **[[Sybil]] = Penn de notre système** — pas d'overlap, pas de recrutement
- **ADAPTER-PROMPT.md dans le vault** — sert de base de migration vers tout nouveau LLM
- **Clés API : stockage exclusif dans `~/.config/pka-jch/anthropic_key.txt`** — jamais dans des fichiers de config

## Prochaine étape

- Traiter les 6 fichiers `Faune_Autour` dans `00_INBOX/` (projet bioacoustique — `/ingest`)
- Vérifier organigramme HTML (v14 — [[Argus]] + [[Pie]] non encore présents visuellement)
- Première session guidée [[Sybil]] (journal structuré avec humeur/énergie)
