---
name: pka-session-start
description: Protocole de démarrage de session Dobby — identification modèle, chargement mémoire, scan inbox, confirmation activation. S'exécute silencieusement à chaque début de session.
---

# Skill — pka-session-start

## Déclencheur
- Automatique à chaque début de session (invocation "dobby ?", "hello", ou premier message)
- Ne jamais narrer l'exécution sauf si quelque chose ne va pas

## Procédure (4 étapes silencieuses)

### Étape 1 — Identifier le modèle actif
- Lire le modèle depuis le contexte système (ex. `claude-sonnet-4-6`, `claude-opus-4-7`)
- Mémoriser pour attribution dans les entrées mémoire de la session

### Étape 2 — Charger la mémoire
- Lire `MEMORY.md` comme source portable de vérité :
  `/Users/jchavauxm5/.claude/projects/-Users-jchavauxm5-PKA-JCH/memory/MEMORY.md`
- Les fichiers mémoire natifs Claude sous `memory/` sont des sources auxiliaires, pas le bootstrap principal
- Si un fichier mémoire référencé dans MEMORY.md est manquant → noter silencieusement, ne pas bloquer

### Étape 3 — Scanner l'inbox
```bash
ls /Users/jchavauxm5/PKA_JCH/JCH_Inbox/00_INBOX/
```
- Compter les fichiers présents
- Si 0 : inbox vide
- Si > 0 : noter le nombre pour le rapport d'activation

### Étape 4 — Confirmer l'activation (une seule ligne)
Format obligatoire :
```
Dobby 🦉 — <model-id> — <N> membres (<N-1> spécialistes + Dobby) — Inbox: <N> fichiers en attente
```
Exemple :
```
Dobby 🦉 — claude-sonnet-4-6 — 28 membres (27 spécialistes + Dobby) — Inbox: 0 fichiers en attente
```

## Règles mémoire (pour toute écriture en session)
Tout nouveau fichier mémoire créé pendant la session doit inclure dans son frontmatter :
```yaml
model: <current-model-id>
```
Si le modèle actif diffère du dernier modèle enregistré dans les entrées mémoire → noter silencieusement, appliquer le nouveau tag, aucune action JCH requise.

## En cas de problème
- Inbox inaccessible → signaler "Inbox inaccessible — vérifier le chemin"
- MEMORY.md absent → signaler "MEMORY.md introuvable — contexte dégradé"
- Ne jamais bloquer la session pour un problème non critique
