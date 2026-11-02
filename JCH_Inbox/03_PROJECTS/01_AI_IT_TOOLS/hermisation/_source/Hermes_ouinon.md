# Hermes : oui ou non ?

[[AI-system]]  
Date : 2026-05-25  
Objet : décision préliminaire sur l’intérêt d’intégrer Hermes Agent dans l’architecture AI personnelle/professionnelle.

---

## 1. Contexte

Le système actuel repose sur :

- un MacBook M5 comme poste principal ;
- un agent coordinateur appelé [[Dobby]] ;
- environ 26 agents spécialisés ;
- plusieurs projets à gérer :
  - développement d’appareillages ;
  - développement logiciel ;
  - projets wildlife / bioacoustique ;
  - gestion documentaire ;
  - projet de société de commercialisation ;
- utilisation de plusieurs modèles AI, notamment [[ChatGPT]] et [[Claude]] ;
- volonté de structurer progressivement une infrastructure persistante, exploitable et durable.

La difficulté actuelle n’est pas seulement technique. Elle concerne surtout :

- la structuration des choix ;
- la hiérarchisation des étapes ;
- la maîtrise du budget ;
- la localisation correcte des données ;
- la continuité entre les sessions ;
- la gouvernance des agents.

---

## 2. Question principale

Hermes Agent doit-il être intégré dans ce système ?

Réponse courte :

**Oui, mais pas comme remplacement de [[Dobby]], [[ChatGPT]] ou [[Claude]].**

Hermes doit être considéré comme une **couche de mémoire persistante, d’orchestration légère et d’automatisation continue**, à tester progressivement.

---

## 3. Ce que Hermes peut apporter

### 3.1 Mémoire persistante

Hermes peut aider à conserver une mémoire opérationnelle entre les sessions.

Intérêt pour les projets :

- conservation des décisions ;
- mémorisation des conventions ;
- capitalisation sur les workflows répétés ;
- réduction du besoin de tout réexpliquer à chaque fois.

Exemples utiles :

- règles de création de fichiers Markdown pour [[Obsidian]] ;
- conventions de classement des projets ;
- historiques de décisions techniques ;
- choix hardware validés ;
- architecture des agents ;
- workflows [[BirdNET]] / Raspberry / [[ESP32]] ;
- gestion des BOM et roadmaps.

---

### 3.2 Création progressive de compétences réutilisables

Hermes peut transformer certains processus répétés en compétences ou routines.

Exemples :

- créer un rapport `.md` téléchargeable ;
- générer une commande Terminal pour installer une note dans [[Obsidian]] ;
- structurer une fiche projet ;
- produire une BOM ;
- faire une revue d’architecture ;
- classer un document dans le bon dossier ;
- préparer un briefing pour [[Claude]] ou [[ChatGPT]].

---

### 3.3 Orchestration continue

Hermes peut être utile pour des tâches qui doivent continuer même lorsque le MacBook n’est pas activement utilisé.

Exemples :

- surveillance de dossiers ;
- réception de données envoyées par des Raspberry ou [[ESP32]] ;
- indexation de documents ;
- génération périodique de synthèses ;
- déclenchement de workflows [[n8n]] ;
- préparation de rapports ;
- interaction avec une base [[PostgreSQL]] ou [[Qdrant]].

---

### 3.4 Complémentarité avec [[ChatGPT]] et [[Claude]]

Hermes ne remplace pas les modèles de raisonnement avancé.

Répartition recommandée :

- **[[ChatGPT]]** : coordination générale, analyse transversale, multimodal, génération de documents.
- **[[Claude]]** : architecture logicielle, refactoring, raisonnement long, analyse critique.
- **[[Dobby]]** : coordinateur métier et orchestrateur conceptuel.
- **Hermes** : mémoire persistante, routines, automatisation, exécution continue.
- **Agents spécialisés** : exécution de tâches précises.

---

## 4. Ce que Hermes ne doit pas faire

Hermes ne doit pas être utilisé au départ pour :

- remplacer tous les agents existants ;
- gérer toute l’infrastructure ;
- faire tourner de gros modèles locaux ;
- piloter seul les décisions critiques ;
- stocker toutes les données ;
- devenir un système autonome incontrôlé.

Le risque principal serait de créer une couche supplémentaire de complexité avant d’avoir stabilisé l’architecture.

---

## 5. Décision recommandée

### Décision

**Oui à Hermes, mais uniquement sous forme de pilote limité.**

### Périmètre du pilote

Ne pas connecter directement les 26 agents.

Commencer avec 3 agents maximum :

1. Agent documentation / [[Obsidian]].
2. Agent architecture système.
3. Agent projet wildlife / bioacoustique.

Objectif du pilote :

- vérifier la stabilité ;
- tester la mémoire persistante ;
- mesurer l’utilité réelle ;
- éviter la complexité excessive ;
- documenter précisément les gains et les limites.

---

## 6. Architecture matérielle recommandée

### Phase actuelle

Utiliser le MacBook M5 comme cockpit principal :

- [[Obsidian]] ;
- [[ChatGPT]] ;
- [[Claude]] ;
- [[Dobby]] ;
- VSCode ;
- supervision des agents ;
- documents actifs.

Le MacBook reste la machine de travail humaine.

---

### Phase VPS

Un VPS peut être utile comme serveur permanent.

Rôle du VPS :

- héberger Hermes ;
- héberger des APIs légères ;
- recevoir des données depuis des appareils terrain ;
- faire tourner [[n8n]] ;
- héberger [[PostgreSQL]], [[Redis]] ou [[Qdrant]] léger ;
- servir de point de coordination Internet ;
- permettre une activité 24/7.

Configuration VPS conseillée pour commencer :

- 4 vCPU ;
- 16 Go RAM ;
- 160 à 320 Go SSD NVMe ;
- Ubuntu Server LTS ;
- [[Docker]] ;
- [[Tailscale]] ;
- Portainer ;
- sauvegarde automatique.

Hostinger peut être une option acceptable pour un pilote, surtout si la simplicité d’usage est prioritaire.

Pour une infrastructure plus robuste à long terme, comparer avec Hetzner ou OVHcloud.

---

### Phase Mac mini dédié

À moyen terme, un Mac mini dédié pourrait être utile.

Rôle :

- traitements locaux ;
- embeddings ;
- bases vectorielles plus lourdes ;
- agents persistants ;
- traitement audio ;
- [[BirdNET]] ;
- [[Whisper]] ;
- indexation documentaire ;
- automatisations locales.

Configuration conseillée :

- Mac mini M4 Pro ou supérieur ;
- 64 Go RAM recommandé ;
- 2 To SSD minimum.

---

### Phase NAS

Un NAS devient pertinent pour le stockage massif.

Rôle :

- archives projets ;
- photos wildlife ;
- sons ;
- vidéos ;
- datasets ;
- sauvegardes [[Obsidian]] ;
- rapports ;
- historiques ;
- backups des bases.

Le NAS ne doit pas être confondu avec le VPS.

---

## 7. Où localiser les données ?

### Données de travail actives

Localisation recommandée :

**MacBook M5**

Contenu :

- [[Obsidian]] principal ;
- notes en cours ;
- documents actifs ;
- scripts ;
- projets vivants ;
- brouillons ;
- fichiers de coordination.

---

### Données persistantes système

Localisation recommandée :

**VPS ou Mac mini selon la phase**

Contenu :

- mémoire active Hermes ;
- [[PostgreSQL]] ;
- [[Redis]] ;
- [[Qdrant]] léger ;
- logs ;
- queues ;
- workflows [[n8n]] ;
- APIs.

---

### Archives et datasets

Localisation recommandée :

**NAS**

Contenu :

- audio massif ;
- images ;
- vidéos ;
- spectrogrammes ;
- datasets wildlife ;
- sauvegardes longues ;
- versions stables ;
- exports.

---

### Code et agents

Localisation recommandée :

**[[Git]] privé + copie NAS**

Contenu :

- agents ;
- scripts ;
- prompts système ;
- workflows ;
- API ;
- configurations [[Docker]] ;
- versions de [[Dobby]].

---

## 8. Roadmap proposée

### Étape 1 — Cartographie

Objectif :

Comprendre clairement le système existant.

Actions :

- lister les 26 agents ;
- définir leur rôle ;
- identifier leurs entrées/sorties ;
- noter les modèles utilisés ;
- identifier les données nécessaires ;
- documenter les dépendances ;
- supprimer les doublons.

Livrable :

`AI_System_Blueprint.md`

---

### Étape 2 — Pilote Hermes local ou VPS

Objectif :

Tester Hermes sur un périmètre réduit.

Actions :

- installer Hermes ;
- créer 3 agents pilotes ;
- connecter une petite mémoire persistante ;
- documenter les résultats ;
- vérifier les gains réels.

Livrable :

`Hermes_Pilot_Report.md`

---

### Étape 3 — Mise en place VPS

Objectif :

Créer un point central permanent.

Actions :

- choisir Hostinger, Hetzner ou OVHcloud ;
- installer Ubuntu Server ;
- installer [[Docker]] ;
- installer [[Tailscale]] ;
- installer Portainer ;
- déployer Hermes ;
- déployer [[PostgreSQL]] ;
- déployer [[n8n]] ;
- définir les sauvegardes.

Livrable :

`VPS_AI_Infrastructure.md`

---

### Étape 4 — Gouvernance documentaire

Objectif :

Éviter le chaos documentaire.

Actions :

- définir les règles de localisation ;
- définir les dossiers maîtres ;
- définir les permissions d’écriture des agents ;
- interdire l’écriture libre partout ;
- organiser [[Obsidian]] ;
- créer un registre des fichiers critiques.

Livrable :

`AI_Data_Governance.md`

---

### Étape 5 — Extension progressive

Objectif :

Étendre seulement après validation.

Actions :

- ajouter progressivement d’autres agents ;
- intégrer les projets wildlife ;
- connecter les appareils terrain ;
- intégrer les données audio ;
- ajouter NAS ;
- ajouter Mac mini si besoin confirmé.

---

## 9. Budget préliminaire

### Niveau 1 — Pilote minimal

Budget estimé :

- VPS : 15 à 40 €/mois ;
- stockage additionnel : faible ;
- logiciels open source : 0 € ;
- temps de configuration : significatif.

Décision :

À faire.

---

### Niveau 2 — Infrastructure confortable

Budget estimé :

- VPS : 25 à 60 €/mois ;
- NAS : 500 à 1 500 € selon disques ;
- sauvegardes : 5 à 20 €/mois ;
- éventuel Mac mini : 1 500 à 3 000 € selon configuration.

Décision :

À envisager après pilote.

---

### Niveau 3 — Infrastructure avancée

Budget estimé :

- VPS plus puissant ;
- Mac mini dédié haut de gamme ;
- NAS robuste ;
- sauvegardes externes ;
- éventuellement GPU serveur.

Décision :

À éviter au démarrage.

---

## 10. Recommandation finale

Hermes est pertinent si on le positionne correctement.

Il doit être vu comme :

**une couche de continuité, de mémoire et d’automatisation**,  
et non comme un cerveau central unique.

La séquence recommandée est :

1. cartographier le système existant ;
2. tester Hermes sur 3 agents ;
3. utiliser un VPS comme hub permanent ;
4. garder les données de travail principales sur le MacBook ;
5. réserver le NAS aux archives et datasets ;
6. ajouter un Mac mini uniquement si les traitements locaux deviennent lourds ;
7. éviter toute complexité inutile au départ.

Conclusion :

**Hermes : oui, mais uniquement en pilote contrôlé.**

La priorité immédiate reste :

**structurer l’architecture avant d’augmenter la puissance.**
