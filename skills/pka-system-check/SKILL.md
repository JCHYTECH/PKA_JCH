---
name: pka-system-check
description: Health-check automatique du système PKA — permissions, backups, pointers, todo drift, structure. Déclencher sur "check pka", "system check", "vérifie l'état du système".
---

# Skill — pka-system-check

## Déclencheurs
- "check pka", "system check"
- "vérifie l'état du système"
- "y a-t-il des problèmes ?"
- "nettoie les scories"
- Après toute modification structurelle majeure (onboarding, changement de config)

## Contexte système
- Script canonique : `/Users/jchavauxm5/PKA_JCH/scripts/pka_system_check.py`
- Sortie : stdout formatée avec statut (GREEN / ORANGE / RED)

## Procédure

### 1. Exécuter le check
```bash
cd /Users/jchavauxm5/PKA_JCH
python3 scripts/pka_system_check.py
```

### 2. Interpréter le statut

| Statut | Action |
|--------|--------|
| **GREEN** | Rien à faire. Confirmer "Système propre ✓" |
| **ORANGE** | Corrections non-bloquantes. Les appliquer si en YOLO, sinon les lister pour JCH |
| **RED** | Problèmes critiques. Appliquer les corrections immédiatement |

### 3. Corriger automatiquement (si YOLO)

Pour chaque finding :
- **Permissions** → `chmod 600 <fichier>`
- **Backup stale** → `python3 scripts/backup_team_db.py`
- **Pointer drift** → `python3 scripts/generate_tool_pointers.py`
- **Todo drift** → `python3 scripts/generate_todo.py`
- **ADAPTER-PROMPT stale** → mettre à jour le compteur de membres

### 4. Re-vérifier
Relancer le check après corrections pour confirmer GREEN.

## Règles
- Toujours appliquer les corrections de permissions sans attendre (sécurité)
- Ne jamais modifier team.db manuellement pour corriger un drift
- Le script est la source de vérité — ne pas remplacer son jugement
- Si le script échoue → signaler à JCH, ne pas essayer de corriger manuellement
