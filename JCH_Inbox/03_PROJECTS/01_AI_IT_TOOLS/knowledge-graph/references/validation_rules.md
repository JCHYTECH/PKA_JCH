---
date: 2026-10-19
model: DeepSeek V4
type: reference
status: active
---

# Validation Rules — Obsidian Knowledge Graph

> **Source canonique :** `scripts/obsidian_knowledge_inventory.py` (constantes en tête de fichier).
> Ce document est un miroir de relecture pour l'étape 5 du skill `obsidian-knowledge-graph`.
> En cas de divergence, le script fait foi. Régénérer/relire après toute modification du script.

## Règle cardinale

Ne jamais modifier une note source sans validation explicite de JCH. Les wikilinks s'appliquent en dry-run d'abord.

## Termes exclus du wikilinking (`WIKILINK_EXCLUDED`)

| Terme | Raison |
|-------|--------|
| Apple | trop de faux positifs |
| ChatGPT | terme trop générique |
| Claude | aussi un prénom |
| Pi | raccourci trop vague — préférer Raspberry Pi 5 |
| Python | trop générique |

## Alias canonique (`CANONICAL_ALIASES`)

| Alias | Canonique |
|-------|-----------|
| Héron | Heron (forme sans accent retenue) |

## Termes ambigus (`AMBIGUOUS_TERMS`)

Vide. Tous les termes précédemment ambigus ont été résolus par JCH le 2026-05-25.
Les nouveaux termes ambigus s'ajoutent ici à la découverte — ne pas wikilinker automatiquement.

## Patterns à ignorer au dry-run (`SKIP_DRY_RUN_PATTERNS`)

- `httpswww.youtube.com` (transcripts, données brutes)

## Dossiers ignorés (`SKIP_PARTS`)

`.git`, `.pytest_cache`, `__pycache__`, `node_modules`, `.venv`, `venv`, `03_AUDIO_DOWNLOADS`

## Noms de sortie générés (`GENERATED_OUTPUT_NAMES`)

- `knowledge_dictionary.md`
- `review_queue.md`

## Agents fusionnés (hors `AGENT_NAMES`)

- **Ariane** → mergé dans **Forge** (retiré du scan le 2026-10-19)
- **Fourmi** → mergé dans **Araignée** (jamais présent dans le scan)
