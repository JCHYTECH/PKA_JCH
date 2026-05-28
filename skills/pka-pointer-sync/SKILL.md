---
name: pka-pointer-sync
description: Resynchroniser les fichiers pointers PKA ([[Claude]].md, AGENTS.md, GEMINI.md, DEEPSEEK.md) après un changement d'équipe ou de structure. Déclencher sur "mets à jour les pointers", "l'équipe a changé", "synchronise les fichiers système".
---

# Skill — pka-pointer-sync

## Déclencheurs
- Après tout recrutement (skill `onboarding-specialiste`)
- "mets à jour les pointers"
- "synchronise [[Claude]].md / AGENTS.md"
- "l'équipe a changé"
- Drift détecté entre les fichiers pointers (comptes membres différents)

## Contexte système
- Script canonique : `/Users/jchavauxm5/PKA_JCH/scripts/generate_tool_pointers.py`
- Source de vérité : `/Users/jchavauxm5/PKA_JCH/JCH_Inbox/99_SYSTEM/tool_pointer_config.json`
- Fichiers générés : `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `DEEPSEEK.md` (à la racine du projet)

## Procédure

### 1. Vérifier l'état actuel
```bash
python3 /Users/jchavauxm5/PKA_JCH/scripts/generate_tool_pointers.py --dry-run 2>/dev/null \
  || python3 /Users/jchavauxm5/PKA_JCH/scripts/generate_tool_pointers.py
```

### 2. Vérifier le nombre de membres dans team.db
```bash
sqlite3 /Users/jchavauxm5/PKA_JCH/TEAM/team.db "SELECT COUNT(*) FROM members WHERE active=1;"
```
Ce chiffre doit être cohérent avec :
- Le compte dans `CLAUDE.md` ("28 membres actifs")
- Le compte dans `TEAM/ROSTER.md`
- Le compte dans `tool_pointer_config.json`

### 3. Mettre à jour `tool_pointer_config.json` si nécessaire
Si le compte DB diffère du fichier config, mettre à jour `tool_pointer_config.json` :
- Champ `team_count` : nombre total membres actifs
- Champ 
- Champ `active_projects` : liste des projets actifs dans `JCH_Inbox/03_PROJECTS/`

### 4. Exécuter le générateur
```bash
cd /Users/jchavauxm5/PKA_JCH
python3 scripts/generate_tool_pointers.py
```

### 5. Vérifier les fichiers générés
Confirmer que les 4 fichiers contiennent le bon compte :
```bash
grep -h "membres actifs\|active members" CLAUDE.md AGENTS.md GEMINI.md DEEPSEEK.md
```

### 6. Rapport à JCH
Format : `Pointers synchronisés — <N> membres actifs dans les 4 fichiers`

## En cas d'erreur script
Si `generate_tool_pointers.py` échoue, mise à jour manuelle minimale :
1. Ouvrir `CLAUDE.md` → mettre à jour le bloc "Canonical PKA Overlay"
2. Répliquer le même chiffre dans `AGENTS.md`, `GEMINI.md`, `DEEPSEEK.md`
3. Signaler à JCH que la mise à jour manuelle a été effectuée et que le script doit être vérifié
