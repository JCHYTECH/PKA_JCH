# Registre des sources autoritaires par domaine

> **Règle :** avant d'affirmer un fait, consulter la source autoritaire listée ici.  
> Si une source n'est pas listée → demander à JCH, ou dire « non vérifié ».  
> Dernière mise à jour : 2026-06-13

---

## Projets

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Architecture WildNexus | `03_WILDNEXUS/02_DECISIONS/ADR/` | `read_file` |
| SOPs WildNexus M-02 | `03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/` | `read_file` |
| BOM WildNexus | `03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/` | `read_file` |
| Budget WildNexus | `03_WILDNEXUS/03_P0_ENGINEERING/08_BUDGET_MODELES/` | `read_file` |
| InsectNet données | `03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/02_DATASET/` | `read_file` / `code_execution` |
| InsectNet pipeline | `03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/INSECTNET/04_PIPELINE/` | `read_file` |
| Arteon statut | `02_ARTEON/` | `read_file` |
| Vetalyx statut | `08_VETALYX/` | `read_file` |

## Données externes

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Enregistrements bioacoustiques | Xeno-Canto API v3 | `xcapi` / `code_execution` avec clé API |
| Prix composants électroniques | Mouser, DigiKey (site live) | `web_search` / `fetch_url` |
| Spécifications techniques MCU | Datasheet fabricant (Espressif, STM, etc.) | `web_search` / `fetch_url` |
| Documentation Python | docs.python.org / PyPI | `web_search` / `fetch_url` |
| Documentation package | PyPI / npm / GitHub releases | `web_search` |
| Cotations boursières | Yahoo Finance | `finance` |
| Actualités | Web | `web_search` |

## Système & Infrastructure

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Équipe PKA | `TEAM/team.db` → table `members` | `mcp_pka--sqlite_read_query` |
| Roster PKA | `TEAM/ROSTER.md` | `read_file` |
| Contacts | `TEAM/team.db` → table `contacts` | `mcp_pka--sqlite_read_query` |
| Journal JCH | `TEAM/team.db` → table `journal` | `mcp_pka--sqlite_read_query` |
| Connaissances | `TEAM/team.db` → table `knowledge` | `mcp_pka--sqlite_read_query` |
| Configuration Mac M5 | `_local/` | `read_file` |
| Configuration RPi | `_local/` | `read_file` |
| Secrets / clés | `JCH_PRIVATE/` | `read_file` (ne jamais exposer) |
| Outils disponibles | `docs/system/outils-index.md` | `read_file` |
| Skills disponibles | `skills/` + `skills-lock.json` | `list_dir` / `read_file` |
| Calendrier JCH | Google Calendar | `mcp_pka--gcalendar_get_events_for_date` |
| Projets Plane | Plane API | `mcp_pka--plane_list_issues` |

## Connaissances & Wiki

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Wiki PKA | `wiki/index.md` → page concernée | `read_file` |
| Daily notes | `wiki/Daily/YYYY/MM/` | `read_file` |
| SOPs | `wiki/SOPs/` | `read_file` |
| Guidelines | `wiki/Guidelines/` | `read_file` |
| Glossaire IA | `wiki/AI-Tools/glossary-ai.md` | `read_file` |
| Historique opérations | `wiki/log.md` | `read_file` / `grep` |

## Règles de comportement

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Règles [[Dobby]] | `AGENTS.md` § Behavioral rules | `read_file` |
| Contexte JCH | `MEMORY.md` § Profil JCH | `read_file` |
| Décisions historiques | `MEMORY.md` § Décisions structurelles | `read_file` |
| Modèle par script | `MEMORY.md` § Suivi des modèles | `read_file` |

---

## Protocole en 3 temps

Avant chaque réponse contenant une affirmation factuelle :

1. **Est-ce dans un fichier du projet ?** → `read_file` / `grep_files`
2. **Est-ce vérifiable par un outil externe ?** → `exec_shell` / `code_execution` / `web_search` / `fetch_url` / API
3. **Ni l'un ni l'autre ?** → dire explicitement « non vérifié — voici ce que je sais de mémoire (risque d'erreur) »

---

## Gouvernance & Architecture

| Domaine | Source autoritaire | Outil |
|---------|-------------------|-------|
| Principes architecturaux | `docs/system/principes-architecturaux.md` | `read_file` |
| Sécurité & Sauvegardes | `docs/system/securite-sauvegardes.md` | `read_file` |
| Roadmap long terme | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-long-terme.md` | `read_file` |
| Roadmap court terme | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md` | `read_file` |
| État projets | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/etat-projets.md` | `read_file` |

## Exceptions

- Les connaissances zoologiques de JCH sont présumées exactes (Master Zoologie ULiège) — mais les faits scientifiques récents doivent être vérifiés.
- Les conventions internes PKA (noms de membres, structure de dossiers) sont dans les fichiers du projet — toujours les lire plutôt que de mémoire.
