# WildNexus — Protocole de lancement

**Version :** v0.2  
**Date :** 2026-06-16  
**Statut :** Actif — M-01 gelé, M-02 en cours (SOPs A→E complétées)  
**Propriétaire :** Jean-Claude Havaux — JCHYTECH  
**Pilotage :** [[Dobby]]  

---

## 1. Intention

Ce document définit le comportement attendu de [[Dobby]] quand JCH active le projet WildNexus.

L'objectif n'est pas de décrire le projet. Les documents fondateurs le font déjà. L'objectif est de préciser le mode d'exécution :
- quoi démarre ;
- dans quel ordre ;
- ce qui est automatisé ;
- ce qui remonte à JCH ;
- où l'état du projet est visible.

Principe directeur :

> JCH doit voir les décisions, les risques et les preuves. [[Dobby]] doit absorber le suivi, la coordination et la maintenance opérationnelle.

---

## 2. Sources De Vérité

Au lancement, [[Dobby]] travaille depuis ces références :

### 2.1 Fondation (immuables sauf décision JCH)
- `01_FOUNDATION/MASTER_ARCHITECTURE_WN.md` — architecture globale
- `00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md` — philosophie d'ingénierie
- `00_GOVERNANCE/WILDNEXUS_P0_SCOPE_LOCK.md` — périmètre P0 verrouillé

### 2.2 Décisions (ADR Index)
- `02_DECISIONS/WILDNEXUS_ADR_INDEX.md` — 10 ADRs acceptés (ADR-001 à ADR-010)
- Chaque ADR est un document autonome dans `02_DECISIONS/`

### 2.3 Ingénierie P0 (M-02 actif)
- `03_P0_ENGINEERING/PROTOCOLES/` — 12 SOPs (M-02 prototype banc fonctionnel)
  - ✅ Phase A→E complétées (ESP32 alive, deep sleep, PPK2, wake cycles, sim event)
  - ⬜ Phases F→J (microSD, LoRa, caméra, PIR, intégration)
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — simulation CI
- `03_P0_ENGINEERING/07_PROCUREMENT_BOM/` — shortlist WP02 + BOM Excel v0.2c

### 2.4 Pilotage
- Plane : projet `03_WILDNEXUS`
- Kanban : `JCH_Inbox/kanban.html`

Ordre d'autorité en cas de contradiction :
- décision explicite JCH ;
- non-négociables du document fondateur ;
- ADRs acceptés ;
- documents de pilotage Plane ;
- SOPs et skills agents.

Toute contradiction détectée doit devenir une décision documentée, pas une discussion diffuse.

---

## 3. État Actuel (2026-06-16)

### 3.1 Milestones

| Milestone | Statut |
|-----------|--------|
| **M-01** — Architecture P0 gelée | ✅ Complété — 10 ADRs acceptés, MCU ESP32-S3, caméra OV5640, LoRa SX1262 |
| **M-02** — Prototype banc fonctionnel | 🔵 En cours — SOPs A→E ✓, F→J en attente composants |
| **M-03** — Prototype terrain | ⬜ Après M-02 |
| **M-04** — Production P0/P1 | ⬜ Après M-03 |

### 3.2 Work Packages

| WP | Contenu | Statut |
|----|---------|--------|
| WP01 — Architecture | ADRs, choix composants, scope lock | ✅ Gelé |
| WP02 — Procurement | Shortlist, BOM, commandes | 🔵 Actif — v0.2c |
| WP03 — Firmware | SOPs, simulation, firmware P0 | 🔵 SOPs A→E faits |
| WP04 — Intégration HW | Caméra, LoRa, PIR, SD | ⬜ |
| WP05 — Tests terrain | PPK2, validation autonomie | 🔵 Banc en cours |
| WP06 — Documentation | Docs, guides, dashboards | 🔵 |

### 3.3 Équipement clé

| Équipement | Statut | Réf. commande |
|-----------|--------|---------------|
| ESP32-S3-DevKitC-1 (×3) | ✅ Reçu | Mouser #39411684 + Amazon |
| Nordic PPK2 | ✅ Reçu | Mouser #39411684 |
| Composants Mouser (mic, IR, PIR, buck, etc.) | ✅ Commandé | Mouser #39492997 |
| ESP32-CAM (dev DVP) | ⬜ À commander | A02a |
| OV5640 DVP (caméra finale) | ⬜ À commander | A02b AliExpress |
| microSD (banc) | ⬜ À acheter | Local |

### 3.4 Budget
- Enveloppe : **1 000 €**
- Engagé : **~785 €** (v0.2c, prix réels Mouser)
- Réserve : **~215 €**
- BOM Excel : `03_P0_ENGINEERING/07_PROCUREMENT_BOM/WILDNEXUS_BOM_P0_v0.2c.xlsx`

---

## 4. Actions Au Signal `go`

### 4.1 Contrôle Initial

[[Dobby]] commence par vérifier :
- que Plane répond ;
- que le projet `03_WILDNEXUS` est joignable ;
- que les ADRs 1-10 sont toujours acceptés (pas de nouveau ADR bloquant) ;
- que le BOM v0.2c reflète l'état réel des commandes ;
- que les SOPs non complétées (F→J) ont leurs prérequis disponibles.

Si un élément technique bloque, [[Dobby]] corrige ce qui peut l'être et ne sollicite JCH que si une action externe est nécessaire.

### 4.2 Synchronisation Projet

[[Dobby]] synchronise :
- milestones `M-01` à `M-04` — état réel vs Plane ;
- SOPs F→J — prérequis, blocages, composants manquants ;
- BOM — écarts entre commandé et reçu ;
- ADRs — nouveaux, modifiés, ou contestés ;
- risques actifs — avec owner.

Le principe est l'idempotence : relancer la synchronisation ne doit pas créer de doublons.

### 4.3 Prochain Chantier Actif

Le chantier en cours est `WP02 — Procurement` + `WP03 — Firmware (SOPs F→J)`.

Les fronts lancés en priorité :
- **SOP-06** — Test microSD (nécessite carte SD + breakout SPI) ;
- **SOP-07** — Test LoRa (nécessite module RAK3172 ou équivalent) ;
- **SOP-08** — Test caméra OV5640 (nécessite ESP32-CAM ou OV5640 reçu) ;
- **Commandes en attente** : A02a (ESP32-CAM), A02b (OV5640), A07 (microSD), A19 (NULA).

---

## 5. Orchestration Des Agents

### 5.1 Noyau Actif

[[Dobby]] active pour les tâches courantes :
- **[[Forge]]** — firmware, intégration, scripts
- **[[Castor]]** — DB, schémas, données techniques
- **[[Fourmi]]** — hardware, banc de test, soudure
- **[[Araignée]]** — IoT, protocoles, connectivité
- **[[Nova]]** — imagerie, caméra, optique
- **[[Bruno]]** — budget, BOM, suivi financier

### 5.2 Agents À La Demande

[[Dobby]] active seulement si nécessaire :
- **[[Furet]]** — recherche composants, benchmarks
- **[[Sigma]]** — analyse données PPK2, modèles énergétiques
- **[[Atlas]]** — rédaction documents fondateurs
- **[[Milan]]** — veille concurrentielle
- **[[Hermine]]** — propriété intellectuelle

Ces rôles ne doivent pas créer de complexité prématurée.

---

## 6. Automatisation Attendue

### 6.1 Automates De Routine

[[Dobby]] automatise par défaut :
- lecture de l'état Plane ;
- détection des tâches bloquées ;
- synthèse des décisions ouvertes ;
- suivi des milestones vs réalité ;
- repérage des documents modifiés ;
- régénération du BOM Excel depuis la shortlist Markdown ;
- mise à jour de `Start.md` (ce fichier) après chaque changement structurel.

### 6.2 Automates De Preuve

Chaque livrable doit laisser une [[Trace]] :
- document créé ou mis à jour ;
- lien vers fichier source ;
- item Plane associé ;
- statut du livrable ;
- décision ou prochaine action.

Un travail important sans [[Trace]] dans le repo est considéré incomplet.

### 6.3 Automates De Cohérence

[[Dobby]] surveille :
- écarts entre ADRs acceptés et BOM (composant manquant = ADR non couvert) ;
- contradictions de version entre Markdown et XLSX ;
- écarts entre `Start.md`, ADR Index et réalité du repo ;
- décisions prises mais non propagées ;
- risques identifiés sans owner.

Quand l'écart est mécanique, [[Dobby]] corrige. Quand l'écart implique une décision de fond, [[Dobby]] escalade.

### 6.4 Régénération Automatique

Ce fichier doit être mis à jour automatiquement après :
- acceptation d'un nouvel ADR ;
- complétion d'une SOP M-02 ;
- réception d'une commande BOM ;
- changement de milestone.

Commande : `python3 scripts/update_wildnexus_start.py` (à créer si absent).

---

## 7. Page Web Et Terminal

### 7.1 Page Web

La page web de pilotage (kanban.html ou Plane) doit montrer :
- statut global ;
- milestone courante ;
- SOPs actives / bloquées ;
- commandes BOM en attente ;
- décisions en attente JCH ;
- risques critiques.

### 7.2 Terminal

Le terminal sert aux interactions courtes et immédiates :
- signaler un blocage ;
- demander un arbitrage ;
- confirmer une action importante ;
- restituer un résultat de test ou de mesure.

### 7.3 Règle D'Escalade

La page web est la vue continue.  
Le terminal est le canal d'action.

Une décision critique doit apparaître dans les deux.

---

## 8. Quand JCH Est Sollicité

[[Dobby]] sollicite JCH uniquement pour :
- modifier un non-négociable ;
- choisir entre deux options stratégiques réelles ;
- accepter un compromis coût / délai / performance ;
- valider un usage sensible dans la matrice de licence ;
- autoriser une action externe ou engageante ;
- arbitrer un conflit entre agents ou domaines.

[[Dobby]] ne sollicite pas JCH pour :
- renommer ou nettoyer un document ;
- synchroniser Plane ;
- produire une synthèse ;
- corriger une incohérence mécanique ;
- lancer une vérification technique de routine ;
- mettre à jour la page web avec l'état courant ;
- régénérer le BOM Excel ;
- mettre à jour ce fichier.

---

## 9. Contrat De Sortie Du Lancement

La phase de lancement est terminée quand :
- Plane reflète le backlog WildNexus sans doublons ;
- M-02 est complété (12 SOPs validées) ;
- M-03 est planifié avec ressources identifiées ;
- la page web expose l'état de tous les WPs ;
- le repo contient les documents de référence à jour ;
- [[Dobby]] peut produire un statut fiable sans relire toute l'arborescence.

À partir de là, WildNexus fonctionne en cycle d'exécution continu.

---

## 10. Résumé

Au signal `go`, [[Dobby]] active le système WildNexus depuis l'état actuel :

Ce système :
- synchronise Plane ;
- poursuit les SOPs M-02 en cours (F→J) ;
- active les bons agents ;
- met à jour la page web ;
- archive les preuves ;
- isole les décisions JCH ;
- régénère le BOM après chaque changement ;
- met à jour ce fichier après chaque jalon.

La règle opérationnelle est simple :

> Tout ce qui est routine est absorbé par le système. Tout ce qui engage la vision, le coût, le risque ou les non-négociables remonte à JCH.
