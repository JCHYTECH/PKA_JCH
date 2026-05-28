# Mandat [[Forge]] — Skill /ingest

**From:** [[Dobby]] 🦉 | **To:** [[Forge]] 🦦 | **Date:** 2026-05-01

## Objectif

Formaliser le processus de traitement de l'inbox JCH. Le skill `/ingest` doit permettre de vider `JCH_Inbox/00_INBOX/` en routant chaque fichier vers sa destination permanente, en le déplaçant, et en l'indexant dans `file_index`.

## Skill créé

`~/.claude/skills/ingest/SKILL.md` — opérationnel immédiatement via `/ingest`.

## Ce que fait /ingest

1. Scanne `JCH_Inbox/00_INBOX/`
2. Analyse chaque fichier (nom, extension, contenu si .md/.txt)
3. Route selon les règles de destination (voir SKILL.md)
4. Déplace vers la destination permanente
5. Insère dans `file_index` (team.db)
6. Rapport : tableau récapitulatif fichier → destination → statut

## Fichiers en attente dans 00_INBOX au moment du mandat

| Fichier | Routing prévu |
|---------|--------------|
| 
| 

## Table file_index — rappel schéma

```sql
file_index (
  id, filename, file_path, file_type, size_bytes,
  description, tags, owner, linked_member,
  inbox_direction, indexed_on, last_modified
)
```

## Règles opérationnelles

- Jamais de suppression — uniquement mv
- Jamais d'écrasement — suffixe `_2` si conflit
- Routing ambigu → demander JCH avant d'agir
- Indexation après déplacement, jamais avant

## Propriété

Ce skill appartient à [[Forge]]. Toute évolution des règles de routing passe par un brief à [[Dobby]] → [[Forge]].
