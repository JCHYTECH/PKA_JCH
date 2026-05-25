---
name: wildnexus-adr
description: Créer, mettre à jour ou valider un ADR WildNexus (Architecture Decision Record). Déclencher sur "crée un ADR", "passe l'ADR en accepté", "documente la décision", "mets à jour l'ADR".
---

# Skill — wildnexus-adr

## Déclencheurs
- "crée un ADR", "nouvel ADR"
- "passe l'ADR en accepté / proposé / remplacé"
- "documente la décision [sujet]"
- "mets à jour l'ADR-00X"
- "vérifie les ADRs"

## Contexte système
- ADR Index : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/WILDNEXUS_ADR_INDEX.md`
- Dossier ADRs : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/`
- Nomenclature fichier : `ADR-NNN-<slug-sujet>.md`
- Numérotation : séquentielle depuis ADR-001 — vérifier le dernier numéro dans l'index avant de créer

## Procédure — Créer un nouvel ADR

### 1. Identifier le numéro suivant
- Lire `WILDNEXUS_ADR_INDEX.md` pour trouver le dernier numéro utilisé
- Incrémenter de 1

### 2. Créer le fichier ADR avec le template
```markdown
# ADR-NNN — Titre court

**Date :** YYYY-MM-DD
**Dernière mise à jour :** YYYY-MM-DD
**Statut :** proposé
**Owner PKA :** <spécialiste PKA>
**Agent WildNexus :** `<agent-wildnexus>`
**Jalon :** <M-01 / M-02 / ...>

## Contexte
<Pourquoi cette décision est nécessaire. Contraintes terrain, techniques, budgétaires.>

## Décision proposée
<La décision retenue, avec justification.>

## Alternatives considérées
| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| ... | ... | ... | Retenu / Rejeté / À analyser |

## Conséquences
- <Impact sur les autres composants, ADRs liés, WPs concernés>

## Sources primaires consultées
- <URLs et références>

## Tests obligatoires avant acceptation
| Test | Critère minimal |
|------|----------------|
| ... | ... |

## Critère de révision
Réviser cette ADR si :
- <condition 1>
- <condition 2>
```

### 3. Ajouter à l'index
- Ouvrir `WILDNEXUS_ADR_INDEX.md`
- Ajouter une ligne dans le tableau principal :
  `| [ADR-NNN](ADR/ADR-NNN-<slug>.md) | Sujet | Owner PKA | agent | **Proposé** |`

## Procédure — Mettre à jour le statut d'un ADR

### Passer en Accepté
1. Ouvrir le fichier ADR
2. Modifier `**Statut :** proposé` → `**Statut :** Accepté`
3. Mettre à jour `**Dernière mise à jour :**` avec la date du jour
4. Mettre à jour `WILDNEXUS_ADR_INDEX.md` : statut → `**Accepté**`
5. Si la décision impacte le BOM → noter l'impact dans la section "Conséquences" et signaler à JCH

### Passer en Remplacé
1. Modifier le statut → `**Statut :** remplacé par ADR-NNN`
2. Créer le nouvel ADR qui remplace
3. Mettre à jour l'index avec les deux entrées

## Procédure — Vérifier l'état de tous les ADRs

1. Lire `WILDNEXUS_ADR_INDEX.md`
2. Lister les ADRs par statut (Accepté / Proposé / Remplacé)
3. Pour chaque ADR "Proposé" : identifier ce qui bloque l'acceptation
4. Signaler à JCH : quels ADRs sont en attente et pourquoi

## Règles absolues
- Un ADR "Proposé" ne bloque pas le travail mais doit être résolu avant la fermeture du jalon concerné
- Toute décision ferme communiquée par JCH → passer immédiatement en "Accepté" avec date
- Le BOM doit refléter le statut des ADRs (section ADR & Paniers du BOM Excel)
- Ne jamais modifier rétroactivement une décision sans créer un ADR de remplacement
