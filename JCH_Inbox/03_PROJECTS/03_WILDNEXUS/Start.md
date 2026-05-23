# WildNexus — Protocole de lancement

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** Protocole operationnel pre-go  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Pilotage :** Dobby  

---

## 1. Intention

Ce document définit le comportement attendu de Dobby quand JCH donne le `go` pour démarrer WildNexus.

L'objectif n'est pas de décrire le projet. Les documents fondateurs le font déjà. L'objectif est de préciser le mode d'exécution :
- quoi démarre ;
- dans quel ordre ;
- ce qui est automatisé ;
- ce qui remonte à JCH ;
- où l'état du projet est visible.

Principe directeur :

> JCH doit voir les décisions, les risques et les preuves. Dobby doit absorber le suivi, la coordination et la maintenance opérationnelle.

---

## 2. Sources De Vérité

Au lancement, Dobby travaille depuis ces références :
- `wildnexus-founding-document-v0.2.md`
- `wildnexus-plane-operating-model.md`
- `wildnexus-plane-seed-backlog.md`
- `WILDNEXUS_AGENT_MAPPING.md`
- `WILDNEXUS_P0_SCOPE_LOCK.md`
- `WILDNEXUS_P0_BUDGET_RANGE.md`
- `wildnexus-usage-policy-and-license-principles.md`
- `wildnexus-usage-matrix.md`
- `WildNexus_MASTER_ARCHITECTURE.md`
- `Agents/*/SKILL.md`

Ordre d'autorité en cas de contradiction :
- décision explicite JCH ;
- non-négociables du document fondateur ;
- document fondateur `v0.2` ;
- documents de pilotage Plane ;
- documents techniques et skills agents.

Toute contradiction détectée doit devenir une décision documentée, pas une discussion diffuse.

---

## 3. Actions Au Signal `go`

### 3.1 Contrôle Initial

Dobby commence par vérifier :
- que Plane répond ;
- que le projet `03_WILDNEXUS` est joignable ;
- que le backlog seed est déjà injecté ou peut être synchronisé ;
- que les documents de référence existent ;
- que la page web de pilotage est disponible ou doit être mise à jour.

Si un élément technique bloque le démarrage, Dobby corrige ce qui peut l'être et ne sollicite JCH que si une action externe est nécessaire.

### 3.2 Synchronisation Projet

Dobby synchronise :
- milestones `M-01` à `M-04` ;
- items `WP01` à `WP06` ;
- tâches `T01.1` à `T06.4` ;
- décisions critiques ;
- risques actifs ;
- documents de référence.

Le principe est l'idempotence : relancer la synchronisation ne doit pas créer de doublons.

### 3.3 Activation WP01

Le premier chantier actif est `WP01 — Conception & Architecture`.

Les fronts lancés en priorité sont :
- `T01.1` comparaison concurrents et calibration des seuils ;
- `T01.2` FTO, licence et exclusions d'usage ;
- `T01.3` préparation RF terrain ;
- `T01.4` benchmark caméra ;
- `T01.5` arbitrage MCU.

---

## 4. Orchestration Des Agents

### 4.1 Noyau Actif

Dobby active d'abord :
- `wildnexus-program-manager-system-architect`
- `wildnexus-camera-imaging`
- `wildnexus-firmware-ulp`
- `wildnexus-hardware-physical`
- `wildnexus-scientific-advisor`

Ces agents couvrent le système P0 minimal : architecture, image, firmware, énergie, mécanique, terrain et valeur scientifique des données.

### 4.2 Agents À La Demande

Dobby active seulement si nécessaire :
- `wildnexus-rf-propagation`
- `wildnexus-edge-ai-cv`
- `wildnexus-industrialisation`
- `wildnexus-bioacoustics-dsp`
- `wildnexus-research-development-project-writer`

Ces rôles ne doivent pas créer de complexité prématurée. Ils interviennent quand leur expertise répond à une tâche ou un risque précis.

---

## 5. Automatisation Attendue

### 5.1 Automates De Routine

Dobby automatise par défaut :
- lecture de l'état Plane ;
- détection des tâches bloquées ;
- synthèse des décisions ouvertes ;
- suivi des milestones ;
- repérage des documents modifiés ;
- génération de notes de statut ;
- rapprochement entre backlog, repo et documents fondateurs.

### 5.2 Automates De Preuve

Chaque livrable doit laisser une trace :
- document créé ou mis à jour ;
- lien vers fichier source ;
- item Plane associé ;
- statut du livrable ;
- décision ou prochaine action.

Un travail important sans trace dans le repo est considéré incomplet.

### 5.3 Automates De Cohérence

Dobby surveille :
- anciennes références d'agents ;
- contradictions de version ;
- écarts entre `Start`, backlog et document fondateur ;
- décisions prises mais non propagées ;
- risques identifiés sans owner.

Quand l'écart est mécanique, Dobby corrige. Quand l'écart implique une décision de fond, Dobby escalade.

---

## 6. Page Web Et Terminal

### 6.1 Page Web

La page web de pilotage doit montrer l'état consolidé du projet.

Elle doit exposer :
- statut global ;
- milestone courante ;
- tâches actives ;
- tâches bloquées ;
- décisions en attente JCH ;
- risques critiques ;
- derniers livrables ;
- prochain objectif.

Elle doit séparer clairement :
- information de suivi ;
- demande d'arbitrage ;
- risque critique.

### 6.2 Terminal

Le terminal sert aux interactions courtes et immédiates :
- signaler un blocage ;
- demander un arbitrage ;
- confirmer une action importante ;
- restituer un résultat de test ou de seed ;
- prévenir qu'une intervention externe est nécessaire.

### 6.3 Règle D'Escalade

La page web est la vue continue.  
Le terminal est le canal d'action.

Une décision critique doit apparaître dans les deux :
- visible dans la page web ;
- signalée dans le terminal.

---

## 7. Quand JCH Est Sollicité

Dobby sollicite JCH uniquement pour :
- modifier un non-négociable ;
- choisir entre deux options stratégiques réelles ;
- accepter un compromis coût / délai / performance ;
- valider un usage sensible dans la matrice de licence ;
- autoriser une action externe ou engageante ;
- arbitrer un conflit entre agents ou domaines.

Dobby ne sollicite pas JCH pour :
- renommer ou nettoyer un document ;
- synchroniser Plane ;
- produire une synthèse ;
- corriger une incohérence mécanique ;
- lancer une vérification technique de routine ;
- mettre à jour la page web avec l'état courant.

---

## 8. Première Définition De `M-01`

Le premier jalon à atteindre est :

> `M-01 — Architecture P0 gelée`

Critères minimaux :
- FTO ou pré-FTO suffisamment cadré ;
- modèle `source-available / ethical-source` confirmé dans les documents ;
- choix caméra documenté ;
- choix MCU documenté ;
- choix radio documenté ;
- hypothèses énergie P0 documentées ;
- risques critiques ouverts avec owner.

Tant que ces éléments ne sont pas présents, `M-01` reste ouvert.

---

## 9. Contrat De Sortie Du Lancement

La phase de lancement est terminée quand :
- Plane reflète le backlog WildNexus sans doublons ;
- la page web expose l'état de `WP01` ;
- les premières tâches critiques ont un owner ;
- les décisions JCH en attente sont visibles ;
- le repo contient les documents de référence à jour ;
- Dobby peut produire un statut fiable sans relire toute l'arborescence.

À partir de là, WildNexus fonctionne en cycle d'exécution.

---

## 10. Résumé

Au `go`, Dobby ne démarre pas une conversation de planification. Il démarre un système de pilotage.

Ce système :
- synchronise Plane ;
- lance `WP01` ;
- active les bons agents ;
- met à jour la page web ;
- archive les preuves ;
- isole les décisions JCH ;
- automatise le reste.

La règle opérationnelle est simple :

> Tout ce qui est routine est absorbé par le système. Tout ce qui engage la vision, le coût, le risque ou les non-négociables remonte à JCH.
