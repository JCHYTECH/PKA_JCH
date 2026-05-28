---
name: onboarding-specialiste
description: Pipeline complet de recrutement d'un nouveau spécialiste PKA. Déclencher sur "recrute", "on a besoin de quelqu'un pour X", "gap de compétence", "nouvel agent", "embauche".
---

# Skill — onboarding-specialiste

## Déclencheurs
- "recrute un spécialiste pour X"
- "on a besoin de quelqu'un qui sait faire X"
- "gap de compétence", "personne dans l'équipe pour X"
- "nouvel agent", "embauche", "nouveau membre"

## Contexte système
- Roster actif : `TEAM/ROSTER.md`
- Base de données : `TEAM/team.db` (tables `members`, `responsibilities`) — **source de vérité**
- Dossier membres : `TEAM/<nom>.md`
- Recrutement gelé sauf analyse ou suggestion [[Dobby]] (voir mémoire 
- Nombre actuel : 28 membres (27 spécialistes + [[Dobby]])

## Règle préalable
Avant de lancer le pipeline, vérifier dans `TEAM/ROSTER.md` qu'aucun membre existant ne couvre déjà le besoin. Si couverture partielle → évaluer d'abord une extension de responsabilités.

## Pipeline en 10 étapes

### Étape 1 — [[Dobby]] identifie le gap
- Décrire précisément la compétence manquante
- Identifier pourquoi aucun membre actuel ne peut couvrir
- Rédiger un brief de recherche pour [[Furet]]

### Étape 2 — [[Furet]] recherche le profil
[[Furet]] reçoit un brief structuré :
```
Compétence cible : <domaine précis>
Contexte PKA : <pourquoi ce besoin existe>
Questions à résoudre :
  1. Quel profil exact (expertise, outils, méthodes) ?
  2. Quels livrables typiques pour JCH ?
  3. Quelles tables team.db ce rôle devrait posséder ?
  4. Frontières avec les membres existants ?
```
Livrable [[Furet]] : brief 400–800 mots.

### Étape 3 — [[Bouvier]] conçoit le persona
À partir du brief [[Furet]], [[Bouvier]] définit :
- **Nom** : prénom français ou animal francophone, unique dans le roster
- **Animal** : espèce cohérente avec le caractère du rôle
- **Rôle** : titre court, sans généricité
- **Tables owned** : liste précise des tables team.db
- **Responsabilités** : 3–5 lignes
- **Frontières** : ce que ce membre NE fait PAS

### Étape 4 — Écriture dans team.db (AVANT tout fichier markdown)
```sql
INSERT INTO members (name, animal, role, tables_owned, active)
VALUES ('<nom>', '<animal emoji> <espèce>', '<rôle>', '<tables>', 1);

INSERT INTO responsibilities (member_name, responsibility, domain)
VALUES ('<nom>', '<responsabilité 1>', '<domaine>'),
       ('<nom>', '<responsabilité 2>', '<domaine>');
```
**Règle absolue : DB d'abord, markdown ensuite.**

### Étape 5 — Créer `TEAM/<nom>.md`
Structure obligatoire :
```markdown
# <Nom> — <Animal emoji> <Espèce>

**Rôle :** <titre>
**Tables owned :** <liste>

## Persona
<3–5 lignes de caractère, style, manière de travailler>

## Responsabilités
- <item 1>
- <item 2>
- ...

## Frontières
Ce que <Nom> ne fait pas :
- ...

## Livrables types
- ...
```

### Étape 6 — Mettre à jour `TEAM/ROSTER.md`
Ajouter la ligne au tableau du roster avec numéro, nom, animal, rôle, tables.

### Étape 7 — Mettre à jour `CLAUDE.md` (tableau Team Roster)
Ajouter la ligne correspondante dans le tableau de la section "Team Roster".

### Étape 8 — Exécuter le sync des pointers
```bash
python3 /Users/jchavauxm5/PKA_JCH/scripts/generate_tool_pointers.py
```
Met à jour [[Claude]].md, AGENTS.md, GEMINI.md, DEEPSEEK.md avec le nouveau nombre de membres.

### Étape 9 — Mettre à jour la mémoire
- Ouvrir `/Users/jchavauxm5/.claude/projects/-Users-jchavauxm5-PKA-JCH/memory/project_recruitment_pause.md`
- Noter le nouveau total de membres et la date

### Étape 10 — Présenter à JCH
[[Dobby]] introduit le nouveau membre :
```
Nouveau membre recruté : <Nom> <emoji>
Rôle : <titre>
Spécialité : <domaine>
Première mission disponible : <tâche en attente si existante>
```

## Règles absolues
- Ne jamais créer le markdown avant d'avoir écrit dans team.db
- Ne jamais créer un rôle générique — chaque membre a une expertise précise
- [[Furet]] doit toujours précéder [[Bouvier]] — pas de recrutement sans recherche
- Vérifier l'absence de doublon dans le roster avant tout recrutement
- Le recrutement est gelé par défaut — ne lancer que sur gap avéré ou suggestion [[Dobby]]
