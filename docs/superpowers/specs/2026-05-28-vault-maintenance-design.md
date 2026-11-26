---
date: 2026-05-28
model: claude-sonnet-4-6
type: design-spec
status: validated
topic: vault-maintenance
---

# Spec — PKA Vault Maintenance Nightly

## Contexte

Le vault `PKA_JCH` accumule des dérives au fil du temps : wikilinks manquants, fichiers mal placés, commits en retard. Ce document spécifie un script autonome de maintenance nocturne qui corrige automatiquement ce qui est sans risque et signale ce qui requiert une intervention manuelle.

## Architecture

```text
scripts/pka_vault_maintenance.py          ← entry point unique
scripts/modules/wikilink_patcher.py       ← détecte + corrige wikilinks manquants
scripts/modules/file_placement_checker.py ← détecte fichiers mal placés
scripts/modules/git_nightly_commit.py     ← staging + commit automatique
scripts/launchd/pka.vault.maintenance.plist ← planifié à 02:00 chaque nuit
scripts/logs/vault_maintenance.log        ← log erreurs critiques uniquement
```

### Flow d'exécution

1. `wikilink_patcher` scanne tous les `.md` → insère wikilinks manquants → log fichiers modifiés
2. `file_placement_checker` vérifie placement selon règles → log anomalies
3. `git_nightly_commit` : `git add` + `git commit` daté si fichiers modifiés
4. Toute exception → log dans `scripts/logs/vault_maintenance.log`, les étapes suivantes continuent (fail-safe)

**Politique de silence :** aucune sortie si tout est OK. Log uniquement si erreur critique ou si commit > 50 fichiers (seuil configurable).

---

## Module 1 — Wikilink Patcher

### Règles de détection et correction

| Cas | Action |
| --- | --- |
| Membre équipe mentionné en prose sans `[[...]]` | Wrap → `[[NomMembre]]` |
| Nom de fichier `.md` existant cité sans wikilink | Wrap → `[[nom-fichier\|Titre]]` |
| Fin de fichier sans `## Voir aussi` alors que cross-refs existent | Ajoute la section |

### Source des noms membres

Requête live sur `TEAM/team.db` → `SELECT name FROM members WHERE status='active'`. Pas de liste codée en dur.

### Garde-fous

- Ne modifie pas les blocs de code (` ``` `), frontmatter YAML, ni les URLs
- Ne double-wrappe pas un `[[...]]` existant
- Fichiers exclus du scan : `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `DEEPSEEK.md`, `MEMORY.md`, `ROSTER.md`
- Dossiers exclus : `.obsidian/`, `__pycache__/`, `node_modules/`

### Périmètre

Scan récursif de `JCH_Inbox/`, `TEAM/`, `TEAM_Inbox/`, `docs/`.

---

## Module 2 — File Placement Checker

### Règles de placement

| Pattern | Dossier attendu |
| --- | --- |
| `YYYY-MM-DD_*.md` ([[daily]] notes) | `JCH_Inbox/01_DASHBOARDS/` |
| `*_rapport_*.md`, `*_delivery_*.md` | `TEAM_Inbox/` |
| `*.py` hors `scripts/` | Anomalie signalée |
| `*.plist` hors `scripts/launchd/` | Anomalie signalée |
| Fichiers directement à la racine de `JCH_Inbox/` | Anomalie signalée |

### Action

Détection + log uniquement — **pas de déplacement automatique**. Déplacer un fichier peut briser des wikilinks [[Obsidian]], des imports [[Python]], ou des launchd plists. Le log liste : chemin actuel, dossier attendu.

---

## Module 3 — [[Git]] Nightly Commit

### Commandes

```bash
git add JCH_Inbox/ TEAM/ TEAM_Inbox/ docs/ scripts/
git commit -m "chore(vault): nightly maintenance YYYY-MM-DD"
```

### Exclusions [[Git]]

- Exclusions absolues : `JCH_Inbox/99_SYSTEM/security/`, `*.env`, `*.token`, `*credentials*`, `*_token.json`
- Si 0 fichier modifié → skip silencieux, pas de commit vide
- Si commit échoue (hook, conflit) → log l'erreur, pas de retry

---

## Planification launchd

- **Schedule :** quotidien à 02:00
- **Label :** `com.pka.vault.maintenance`
- **Log stdout/stderr :** `scripts/logs/vault_maintenance.log`
- **Working directory :** `/Users/jchavauxm5/PKA_JCH`

---

## Seuils configurables

| Paramètre | Défaut | Description |
| --- | --- | --- |
| `max_files_silent` | 50 | Au-delà, log le nombre de fichiers commités |
| `scan_paths` | `["JCH_Inbox", "TEAM", "TEAM_Inbox", "docs"]` | Dossiers scannés |
| `excluded_files` | voir garde-fous | Fichiers système exclus du wikilink patch |

## Voir aussi

- [[pka_system_check]] — audit sécurité + amélioration système (script complémentaire)
- [[GOVERNANCE]] — gouvernance du vault
- [[MEMORY]] — mémoire portative de session
