# WildNexus — Recommandations Dobby post-diagnostic

**Date :** 2026-05-18  
**Source analysée :** `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/2026-05-18_dobby_wildnexus-diagnostic.md`  
**Position Dobby :** diagnostic globalement juste, à resserrer en plan d'action court avant `go`.

## Verdict

WildNexus n'a pas un problème de vision. Le projet a un problème classique de passage entre document fondateur et système exécutable : trop de couches dans un même espace, des agents spécialisés non raccordés à la gouvernance PKA, et un coût encore trop implicite pour décider sereinement.

Le `go` ne doit pas attendre la perfection documentaire. Il doit attendre trois clarifications minimales : périmètre P0, gouvernance d'exécution, budget d'ordre de grandeur.

## Décisions recommandées

### 1. Garder un document fondateur, mais créer des annexes opératoires

Ne pas casser brutalement `wildnexus-founding-document-v0.2.md`. Il reste utile comme bible v0.2. En revanche, créer quatre annexes courtes :

- `WILDNEXUS_CHARTER.md`
- `WILDNEXUS_P0_EXECUTION_PLAN.md`
- `WILDNEXUS_LICENSE_AND_USAGE.md`
- `WILDNEXUS_GOVERNANCE.md`

Le document fondateur devient le texte constitutionnel consolidé ; les annexes deviennent les documents de travail.

### 2. Créer un pont PKA ↔ agents WildNexus avant toute exécution Plane

La recommandation du diagnostic est prioritaire. Les agents WildNexus ne doivent pas devenir une seconde équipe parallèle. Il faut un `WILDNEXUS_AGENT_MAPPING.md` indiquant :

- agent WildNexus
- spécialiste PKA référent
- périmètre exact
- livrables attendus
- escalade vers JCH ou Dobby

### 3. Chiffrer avant M-01, même grossièrement

Bruno doit produire un budget `P0 ±30%` avant le go opérationnel :

- FTO / PI externe
- composants et PCB x5
- boîtiers / impression / usinage
- batteries / solaire / alimentation
- outils de test terrain
- compute / dataset / IA
- communication et dépôt public

Sans cela, NN-08 reste une intention, pas une contrainte pilotable.

### 4. Verrouiller le scope P0 en trois exclusions écrites

Pour éviter le scope creep, ajouter un bandeau clair :

- bioacoustique = P1, hors P0 sauf contraintes d'interface
- Faune Autour = projet adjacent ou composant P2, pas livrable P0
- reconnaissance espèce fine = P1, P0 limite au filtre animal / non-animal

### 5. Ajouter deux work items manquants au backlog Plane

Le diagnostic pointe l'absence de tests automatisés. À ajouter :

- `T03.6 Tests firmware et simulation états critiques`
- `T04.5 Pipeline d'évaluation automatisé du classifieur`

Ajouter aussi :

- `T01.6 Budget P0 ordre de grandeur`
- `GOV-01 Mapping agents WildNexus vers spécialistes PKA`
- `DOC-01 Split annexes opératoires v0.3`

## Points du diagnostic à déclasser

Ces points sont valides mais ne doivent pas bloquer le go :

- dashboard dynamique : utile, mais peut rester maquette jusqu'au premier cycle Plane
- règle d'archive : hygiène documentaire, non critique
- suppression du fichier `Start` vide : nettoyage immédiat, mais sans enjeu stratégique
- `data/README.md` : utile, mais non bloquant

## Risques manquants dans le diagnostic

### Données personnelles et droit d'installation terrain

NN-09 couvre les personnes capturées, mais il faut un livrable terrain concret avant EVT :

- modèle de panneau d'information RGPD
- fiche base légale / intérêt légitime
- procédure de suppression ou floutage
- règles d'installation sur terrains tiers ou zones sensibles

### Chaîne d'approvisionnement

Le diagnostic parle coût, mais pas disponibilité. Pour un hardware P0, la disponibilité des modules caméra, MCU, radio, batterie et boîtier doit être suivie dès T01.5/T02.1.

Créer un mini registre :

- composant
- fournisseur primaire
- fournisseur alternatif
- délai
- risque d'obsolescence
- impact sur design

## Plan d'action recommandé

### Avant go

1. `WILDNEXUS_AGENT_MAPPING.md`
2. Budget P0 ±30%
3. Clarification Faune Autour / Bioacoustique / reconnaissance espèce fine hors P0
4. Ajout des work items manquants dans le backlog Plane

### Cycle 01

1. Annexes v0.3
2. Timeline T01.2 FTO / licence
3. ADR-001 choix MCU
4. Tests firmware minimum
5. Pipeline évaluation classifieur

### Nettoyage rapide

1. Supprimer `Start` vide
2. Ajouter `data/README.md`
3. Renommer dashboard en maquette ou le connecter plus tard à Plane

## Conclusion

Recommandation Dobby : `go conditionnel`, pas `no-go`.

Le projet peut avancer si les quatre préconditions avant go sont traitées. Le danger principal n'est pas technique à ce stade ; il est organisationnel : laisser les documents, agents, scopes P0/P1 et budgets évoluer en parallèle sans point de contrôle unique.
