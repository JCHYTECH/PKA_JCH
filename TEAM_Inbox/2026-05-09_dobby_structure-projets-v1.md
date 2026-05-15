# Structure des projets PKA_JCH — v1 stabilisée

**De :** Dobby  
**À :** Toute l'équipe  
**Date :** 2026-05-09  
**Objet :** Répertoire 03_PROJECTS — structure standard adoptée

---

## Ce qui a changé

Le répertoire `JCH_Inbox/03_PROJECTS/` est désormais stabilisé. Voici ce que vous devez savoir pour travailler correctement.

---

## Projets actifs — numérotation officielle

| # | Projet | Responsable principal |
|---|--------|-----------------------|
| 01 | AI_IT_TOOLS | Forge |
| 02 | ARTEON | Vega |
| 03 | FAUNE_AUTOUR | Forge + Lynx |
| 04 | NUANCES | TBD |
| 05 | PHOTO_AI_JURY | Argus + Lynx |
| 06 | PHOTO_NATURE | Lynx |
| 07 | TRAVELS | Corbeau |
| 08 | VETALYX | Vasco + Renard + Bruno |

---

## Structure standard d'un projet

```
NN_PROJECT/
  ├── INDEX.md          ← obligatoire
  ├── docs/             ← obligatoire
  │   └── media/        ← médias ici, jamais à la racine
  ├── archive/          ← obligatoire
  [optionnels]
  ├── content/          ← production éditoriale (fiches, newsletters, observations)
  ├── legal/            ← contrats et pactes actifs
  ├── tech/             ← développement logiciel/technique
  └── comms/            ← échanges externes institutionnels
```

**Règle absolue : `media/` vit dans `docs/`, jamais à la racine du projet.**

---

## Règles de dépôt

- Tout fichier produit pour un projet va dans le bon sous-dossier de `docs/` (ou `content/` si éditorial, `legal/` si juridique)
- Aucun fichier à la racine du projet sauf `INDEX.md`
- En cas de doute sur le sous-dossier → déposer dans `docs/` et signaler à Dobby

---

## À retenir pour les nouveaux projets

Quand Dobby crée un projet, la structure ci-dessus est appliquée automatiquement. Vous n'avez pas à la recréer.

---

*Dobby*
