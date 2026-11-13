# Analyse — 2 Transcripts NoteGPT : Obsidian + AI Note System

> Dobby 🦉 — DeepSeek V4 (TUI 0.8.39) — 2026-07-13
> Fichiers sources : `NoteGPT_Transcript_Pourquoi j'ai quitté Evernote pour Obsidian (1).txt` + `NoteGPT_Transcript_I Replaced Apple Notes With AI — Download My Exact Prompt.txt`

---

## Résumé

Deux transcripts d'une même chaîne YouTube (Sanja / Atelier Geek Pratique) sur le passage d'un système de notes classique (Evernote/Apple Notes) à **Obsidian + IA (Claude Code)**. Le second décrit un système complet « second brain » construit avec un seul prompt Claude Code.

---

## Transcript 1 — Pourquoi quitter Evernote pour Obsidian (FR, ~12 min)

**3 défauts d'Evernote (et de tout logiciel propriétaire) :**
1. **Données enfermées** — format propriétaire, pas portable
2. **Notes isolées** — pas de liens entre elles, plus tu en ajoutes moins tu retrouves
3. **Stagnation** — racheté par Bending Spoons, pas d'innovation

**Obsidian en contrepoint :**
- Fichiers Markdown → tes données t'appartiennent
- Liaisons entre notes → réseau de connaissance (graphe)
- Gratuit, pas bridé
- L'IA (« Lia ») aide à créer des connexions

---

## Transcript 2 — I Replaced Apple Notes With AI (EN, ~16 min)

**Système « second brain » basé sur Claude Code + Obsidian :**

| Fonctionnalité | Mécanisme |
|----------------|-----------|
| **Auto-filing** | L'IA classe les notes, crée/modifie/supprime selon règles |
| **Person tracking** | « Tim Cook is my contact at Apple » → connecte aux infos existantes |
| **Date tracking** | Détecte dates d'expiration, due dates, follow-ups → page « upcoming » |
| **Inbox processing** | « Clean up my inbox » → traite les quick captures |
| **Maintenance** | Déduplication, liens cassés, formatage, index |
| **Mobile** | Obsidian iOS + Claude Code remote control |

**Architecture technique :**
- 1 dossier = 1 vault Obsidian
- 1 prompt Claude Code qui construit tout
- Règles de filing dans le prompt
- Markdown + iCloud sync
- Pas de base de données, pas de backend

---

## Patterns identifiés — pertinence PKA

| Pattern | Transcript | Équivalent PKA | Gap |
|---------|-----------|----------------|-----|
| **Auto-filing par règles** | Transcript 2 | Skill `ingest` (route + déplace) | PKA déplace des fichiers, ne les réécrit pas |
| **Date tracking** | Transcript 2 | `follow_ups` dans team.db | Pas de scanning automatique de dates dans le texte |
| **Inbox processing** | Transcript 2 | Skill `inbox-analysis` + `ingest` | PKA fait une analyse complète, pas du quick-capture |
| **Maintenance workflow** | Transcript 2 | `pka-system-check` | PKA vérifie fraîcheur State, pas déduplication notes |
| **One prompt to build** | Transcript 2 | `BOOTSTRAP.md` | PKA a un bootstrap, pas un « build from scratch » |
| **Markdown ownership** | Transcript 1 | Tout PKA est en Markdown | ✅ Déjà aligné |
| **Knowledge graph** | Transcript 1 | `graphify` | ✅ Déjà présent |

---

## Impact projets

| Projet | Impact | Note |
|--------|--------|------|
| **AI_IT_TOOLS** 🟢 | 🔴 Majeur | 4 améliorations directes pour PKA : date scanning, maintenance, quick-capture, one-prompt |
| **ARTEON/WildLens** | ⚪ Léger | L'auteur mentionne un atelier payant, pas pertinent |

---

## Propositions

### 🔴 P0 — Date scanner pour PKA
- **Pattern** : comme le transcript 2 scanne les dates d'expiration, PKA pourrait scanner les fichiers INBOX/TEAM_Inbox pour détecter automatiquement des dates (deadlines, expirations, suivis)
- **Action** : Ajouter un flag `--scan-dates` à `pka_memory_capture.py` ou créer un script dédié
- **Bénéfice** : plus besoin de créer manuellement des follow_ups, le système les détecte

### 🟡 P1 — Quick-capture inbox
- **Pattern** : le transcript décrit un « inbox folder » où on dépose une pensée brute, et l'IA la traite plus tard
- **Action** : Ajouter un mode « quick » à `ingest` — l'utilisateur balance une phrase, Dobby la classe
- **Bénéfice** : réduire la friction de capture pour JC

### 🟡 P1 — Maintenance workflow script
- **Pattern** : `do maintenance` → déduplication, liens cassés, formatage, index
- **Action** : Créer `pka_maintenance.py` : détecter doublons dans team.db, liens Obsidian cassés, notes orphelines
- **Bénéfice** : santé du vault automatisée

### ⚪ P2 — One-prompt bootstrap amélioré
- **Pattern** : un seul prompt qui construit tout le système
- **Action** : Enrichir `BOOTSTRAP.md` pour qu'un nouveau modèle puisse reconstruire l'environnement PKA complet
- **Bénéfice** : onboarding modèle zero-effort

---

## Web validation

- **Obsidian** : confirmé, gratuit, Markdown, 2026 toujours leader des PKM
- **Claude Code** : outil de développement CLI par Anthropic, utilisé ici comme « OS pour notes »
- **Sanja / Atelier Geek Pratique** : chaîne YouTube FR de productivité tech, ~100k abonnés estimé

---

## Actions immédiates

| # | Action | Qui | Priority |
|---|--------|-----|----------|
| 1 | Ajouter `--scan-dates` à `pka_memory_capture.py` | Forge | 🔴 P0 |
| 2 | Créer mode quick-capture pour `ingest` | Forge | 🟡 P1 |
| 3 | Créer `pka_maintenance.py` | Forge | 🟡 P1 |
| 4 | Mettre à jour `outils-index.md` avec les nouveaux scripts | Dobby | Après Forge |

---

*Analyse terminée. Sources à archiver dans `01_AI_IT_TOOLS/99_REFERENCES/`.*
