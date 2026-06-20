---
name: pka-file-versioning
description: Sauvegarder la version précédente d'un fichier itératif avant toute modification significative. Déclencher automatiquement avant toute modification de BOM, ADR, registre, matrice, shortlist, budget.
---

# Skill — pka-file-versioning

## Déclencheur (automatique)
Avant toute modification significative d'un fichier itératif :
- BOM / shortlist achat (`.md` ou `.xlsx`)
- ADR (sauf changement de statut mineur)
- Registre composants / supply register
- Matrice hardware
- Budget / fichier financier
- Tout document versionné (contient `v0.X`, `v1.X` dans le nom)

Une modification est "significative" si elle change le contenu (pas juste la date ou le statut).

## Procédure

### 1. Identifier la version actuelle
- Lire le nom du fichier cible
- Extraire le numéro de version si présent (ex. `v0.2` → version courante)

### 2. Construire le nom de sauvegarde
Conventions :
- Fichier avec version dans le nom : `nom_vX.Y.ext` → copier tel quel (la nouvelle version aura un numéro incrémenté)
- Fichier sans version dans le nom : créer `nom_backup_YYYY-MM-DD.ext`

### 3. Sauvegarder avant modification

**Méthode A — Copie simple (par défaut) :**
```bash
cp "<chemin_original>" "<chemin_sauvegarde>"
```

**Méthode B — Git tag (recommandé pour fichiers versionnés) :**
```bash
git tag -a "backup/<nom-fichier>_vX.Y" -m "Backup avant modification de <fichier> vX.Y"
```
Le tag git évite la prolifération de fichiers `_backup` et garde l'historique dans le repo. Préférer cette méthode pour BOM, budget, ADR.

### 4. Procéder à la modification
- Modifier le fichier original (pas la copie)
- Incrémenter la version dans le contenu du fichier si applicable
- Mettre à jour la date

### 5. Confirmer à JCH
Format : `Version précédente sauvegardée : <nom_fichier_backup>`

## Exemples

| Fichier original | Sauvegarde créée |
|------------------|-----------------|
| `WILDNEXUS_BOM_P0_v0.2.xlsx` | Conserver tel quel, nouvelle version → `v0.3.xlsx` |
| `ADR-006-boitier.md` | `ADR-006-boitier_backup_2026-05-25.md` |
| `WILDNEXUS_SUPPLY_REGISTER.md` | `WILDNEXUS_SUPPLY_REGISTER_backup_2026-05-25.md` |

## Exceptions (pas de backup nécessaire)
- Changement de statut seul dans un ADR (Proposé → Accepté)
- Mise à jour de date uniquement
- Correction typo < 5 mots
- Fichiers générés automatiquement par script (ils peuvent être régénérés)
