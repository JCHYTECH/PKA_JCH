# WildNexus — Diagnostic Dobby 🦉

**Date :** 2026-05-18  
**Auteur :** Dobby — orchestration PKA_JCH  
**Périmètre :** analyse complète du projet `03_WILDNEXUS` — documentation, architecture, agents, gouvernance, exécution  
**Fichiers analysés :** 19 documents (831 + 706 + 319 + 262 + 607 + 198 + … lignes), 11 skills agents, 8 sous-répertoires

---

## Résumé exécutif

Le projet WildNexus est **remarquablement bien cadré pour un DRAFT v0.2**. La vision est claire, les non-négociables sont solides, le séquençage P0→P1→P2 est discipliné, les critères de sortie/pivot sont écrits à froid, et le dispositif juridique (source-available + exclusions d'usage) est pensé dès le départ. C'est un niveau de rigueur documentaire rare pour un projet à ce stade.

Ce diagnostic identifie **15 points d'amélioration**, classés par criticité : 3 bloquants, 7 importants, 5 de fond.

---

## 🔴 Bloquants ou structurels (à traiter avant le `go`)

### 1. Le document fondateur mélange quatre couches qu'il promet de séparer

Le §0 l'admet lui-même :

> « Ce document mélange volontairement quatre couches qui devront être séparées à terme : la doctrine fondatrice, le plan technique P0, la stratégie [de licence], et la gouvernance. »

Cette séparation n'a pas eu lieu. Résultat : 831 lignes où la vision côtoie les specs techniques (choix MCU, tension batterie), la matrice de licence, les work packages, et le budget. Un partenaire ou un conseil PI externe ne peut pas lire ce document sans être noyé dans du détail qui ne le concerne pas.

**Recommandation :** splitter en 4 fichiers indépendants avant le `go` :

| Fichier | Contenu | Public cible |
|---------|---------|-------------|
| `WILDNEXUS_CHARTER.md` | Non-négociables + vision + mission | Tout public |
| `WILDNEXUS_P0_PLAN.md` | Work packages + jalons + specs techniques | Équipe projet |
| `WILDNEXUS_LICENSE.md` | Dispositif juridique complet | Partenaires, conseil PI |
| `WILDNEXUS_GOVERNANCE.md` | Rôles, décisions, escalade | Équipe + JCH |

---

### 2. Les agents WildNexus et l'équipe PKA sont deux écosystèmes parallèles sans pont

Le projet définit 11 agents spécialisés (`wildnexus-program-manager-system-architect`, `wildnexus-firmware-ulp`, `wildnexus-camera-imaging`, etc.) avec leurs propres `SKILL.md`. Mais ils n'apparaissent **ni dans `team.db` ni dans le ROSTER PKA**. Aucun document n'explique quel spécialiste PKA backing quel agent WildNexus.

**Exemples de ponts évidents mais non documentés :**

| Agent WildNexus | Spécialiste PKA naturel | Justification |
|-----------------|------------------------|---------------|
| `wildnexus-scientific-data-protocols` | **Furet 🦡** | Recherche, positionnement concurrents (T01.1) |
| `wildnexus-firmware-ulp` | **Castor 🦫** | Architecture données, schéma P0 (§8.7) |
| Intégration Plane / CI/CD | **Forge 🦦** | Automatismes, scripts, dashboard |
| `wildnexus-mechanical-reliability-engineer` | **Chouette 🦉** | Terrain, installation, enclos, pièges |
| `wildnexus-camera-imaging` | **Nova 🦋** | Optique, capteurs, validation image |
| Licence / FTO / contrats | **Renard 🦊** | Déjà identifié comme owner juridique |
| `wildnexus-bioacoustics-dsp` | **Clio 🦜** | Littérature scientifique, BirdNET |
| Budget / financement | **Bruno 🐻** | Analyse ressources, modèle de coût |

**Recommandation :** créer un fichier `WILDNEXUS_AGENT_MAPPING.md` qui fait le pont entre les agents WildNexus et les spécialistes PKA, avec responsabilités claires et règles d'escalade. Intégrer les agents WildNexus dans `team.db` ou documenter explicitement pourquoi ils restent hors-roster.

---

### 3. Le budget (§13) a une structure mais aucun chiffre

Le §13 définit des catégories de coût (WP01→Moyen, WP02→Élevé, WP03→Faible…) mais renvoie à :

> « un document séparé JCHYTECH, non inclus dans la bible publique. »

La note v0.2 promet un modèle de coût lié au prix cible 900 € après D02.2 (BOM). **C'est trop tard.** Sans ordre de grandeur budgétaire :

- NN-08 (« indépendance financière ») n'est pas vérifiable — on ne sait pas si les ressources disponibles couvrent le minimum pour atteindre M-03
- Un dépassement en WP02 (fabrication PCB) n'a aucun cadre de référence pour être détecté
- La conversation investisseur post-POC n'a pas de base chiffrée

**Recommandation :** produire une estimation budgétaire même grossière (±30%) avant M-01. Bruno peut poser un cadre en 2h avec des fourchettes par WP. Exemple de granularité minimum :

| WP | Poste dominant | Fourchette estimée |
|----|---------------|-------------------|
| WP01 | FTO (conseil PI) + benchmark | X – Y k€ |
| WP02 | PCB ×5 + composants + enclos ×5 | X – Y k€ |
| WP03 | Temps JCH + outillage firmware | X – Y k€ |
| WP04 | Dataset + compute entraînement | X – Y k€ |
| WP05 | Déplacement + logistique EVT | X – Y k€ |
| WP06 | Infrastructure dépôt + comm | X – Y k€ |

---

## 🟡 Importants (ralentiront l'exécution s'ils ne sont pas traités)

### 4. L'application Faune Autour (03.02) est hébergée dans WildNexus mais n'a aucun lien documenté avec lui

Son README décrit une PWA indépendante utilisant l'API GBIF pour lister les observations animales autour d'une position GPS. **Aucune mention de WildNexus.** La question est légitime :

- Est-ce un composant WildNexus (future interface utilisateur des données collectées par les nœuds) ?
- Est-ce un projet séparé hébergé ici par commodité ?
- Est-ce un POC précurseur qui sera intégré plus tard ?

**Recommandation :** clarifier la relation dans l'INDEX.md et dans le README de Faune Autour. Si c'est un projet indépendant, le déplacer dans `03_PROJECTS/` comme `09_FAUNE_AUTOUR`. Si c'est un composant WildNexus P2, le documenter comme tel avec une section « Roadmap integration ».

---

### 5. Le composant bioacoustique (03.01) a du contenu détaillé… pour une fonctionnalité P1

Le répertoire contient :
- `Projet_bioacoustique.md` — document de pilotage
- `BirdNET-Go_RaspberryPi_iPhone_summary.md` — résumé technique
- `Faune_Autour_Acoustic_Project_Management.xlsx` — fichier Excel de gestion
- `Faune_Autour_Acoustic_Project_Report.md` — rapport de projet

C'est du travail sérieux. Mais le document fondateur est clair : **la bioacoustique n'est PAS un objectif P0.** Ce contenu détaillé crée une pression implicite pour élargir le scope P0 (« on a déjà fait tout ce travail, autant l'inclure »).

**Recommandation :** archiver ou tagger clairement `P1_DEFERRED` dans chaque fichier du répertoire, et ajouter un bandeau dans l'INDEX : « Contenu P1 — ne pas inclure dans le scope P0. »

---

### 6. Le dashboard HTML est statique — il sera obsolète au premier cycle

`wildnexus-dashboard.html` (607 lignes) est un bel objet visuel avec palette cohérente, barre de phases, cartes d'agents. Mais tout est codé en dur : statuts (`Défini`), milestones, phases. Il n'est connecté à aucune source de données (ni Plane, ni le repo).

**Recommandation :** deux options :
- **(a) Dynamique :** Forge écrit un script qui interroge Plane et regénère le dashboard → intégré dans `01_DASHBOARDS/`
- **(b) Maquette :** le fichier actuel est renommé `wildnexus-dashboard-mockup.html` et un vrai dashboard est créé dans `01_DASHBOARDS/wildnexus.html`

---

### 7. La licence et l'arbitrage juridique (T01.2) sont sur le chemin critique de M-01 mais n'ont pas de timeline

L'analyse FTO, le modèle `source-available / ethical-source`, et la rédaction de la licence sont **bloquants pour M-01**. Renard est identifié comme owner, mais :
- Aucune estimation de durée n'est fournie
- Un cabinet PI externe est mentionné comme « mobilisé si nécessaire » — sans être mandaté
- Le délai de réponse d'un cabinet PI est typiquement de 3-6 semaines pour une analyse FTO

**Recommandation :**
- Ajouter une estimation de durée pour T01.2 (fourchette : 4-8 semaines)
- Identifier et contacter le cabinet PI avant le `go`
- Envisager de découpler M-01 en deux sous-jalons :
  - **M-01a** (technique) : radio + caméra + MCU — peut avancer sans le juridique
  - **M-01b** (juridique) : FTO + licence — bloque la publication (M-04) mais pas le prototypage (M-02)

---

### 8. Aucun test automatisé — tout le plan de validation est manuel et terrain

Le plan de validation (§11) est entièrement basé sur des tests physiques (EVT 30 jours, immersion IP67, installation par non-technicien). C'est correct pour le hardware. Mais il n'y a **aucune infrastructure de test pour :**
- Le firmware (machine à états, OTA, chiffrement)
- L'IA embarquée (précision du classifieur, latence d'inférence, faux positifs sur dataset de test)
- Le protocole de communication LPWAN (simulation de perte de paquets, duty cycle)
- La configuration BLE (appairage, résilience)

**Recommandation :** ajouter des tâches légères :
- **WP03** : `T03.6 — Tests unitaires firmware + CI/CD` (framework de test embarqué, runner sur CI)
- **WP04** : `T04.5 — Pipeline d'évaluation automatisé du classifieur` (script Python, métriques, courbes ROC)

Même un coverage de 30% sur le firmware évitera des régressions coûteuses en phase EVT.

---

### 9. Le fichier `Start` (sans extension) est vide — artéfact à nettoyer

Un fichier de 0 octets nommé `Start` (sans extension) existe à la racine du projet, à côté de `Start.md`. Probablement un résidu de Finder ou d'éditeur.

**Recommandation :** supprimer `Start` (sans extension). Le fichier actif est `Start.md`.

---

### 10. Le répertoire `data/` est annoncé dans l'INDEX mais vide

L'INDEX.md le décrit comme « données projet ». Il est vide. Un lecteur qui suit l'INDEX s'attend à y trouver des données.

**Recommandation :** soit le peupler (même avec un `README.md` expliquant ce qui y sera stocké et sous quel format : datasets IR, logs EVT, exports Camtrap-DP), soit le retirer de l'INDEX jusqu'à ce qu'il contienne quelque chose.

---

## 🟢 Améliorations de fond (non urgentes, mais structurantes)

### 11. Pas de registre de décisions architecturales (ADR)

Le projet va prendre des décisions techniques lourdes et irréversibles à P0 :
- Choix du MCU (ESP32-S3 vs STM32U5 vs nRF54)
- Choix du module caméra (IMX462 vs IMX327)
- Standard radio (LoRa vs autre LPWAN)
- Chimie batterie (LiFePO4 vs Li-Ion)

Sans ADR, dans 6 mois personne ne saura pourquoi le STM32U5 a été préféré au nRF54, ni quelles alternatives ont été évaluées. Un nouvel ingénieur ou un partenaire technique n'aura que le résultat final, pas le raisonnement.

**Recommandation :** créer `tech/adr/` avec un template simple :

```markdown
# ADR-001 : Choix du MCU P0

**Date :** YYYY-MM-DD
**Statut :** proposé / accepté / remplacé
**Décideur :** wildnexus-embedded-platform-engineer

## Contexte
…

## Décision
…

## Alternatives considérées
| Option | Pour | Contre |
|--------|------|--------|
| … | … | … |

## Conséquences
…
```

T01.5 (sélection MCU) est le candidat parfait pour `ADR-001`.

---

### 12. La gateway est mentionnée dans l'architecture mais jamais détaillée dans le plan P0

L'architecture définit 3 types de nœuds (caméra, acoustique, gateway) mais les WPs P0 ne couvrent que le nœud caméra. La gateway est-elle :
- Un achat sur étagère (ex. carte LoRa + Raspberry Pi) ?
- Un développement spécifique ?
- Repoussée en P1 ?

**Recommandation :** clarifier dans le document fondateur ou dans un WP00 transverse. Si la gateway est un achat sur étagère, le mentionner avec un modèle candidat et un budget. Si elle est repoussée, l'indiquer explicitement pour éviter l'ambiguïté.

---

### 13. Les noms d'agents sont incohérents entre les documents

La table des matières du document fondateur référence :

- `wildnexus-mechanical-reliability-engineer`
- `wildnexus-power-systems-engineer`
- `wildnexus-imaging-systems-engineer`

Mais dans `Agents/`, on trouve :

- `wildnexus-hardware-physical`
- *(pas de power-systems-engineer dédié)*
- `wildnexus-camera-imaging`

Les noms ne correspondent pas. Un `grep` sur les noms d'agents dans tout le repo révélera d'autres incohérences.

**Recommandation :** aligner les noms d'agents entre :
1. Le document fondateur (table des matières §0)
2. Le répertoire `Agents/`
3. Le seed backlog Plane (`wildnexus-plane-seed-backlog.md`)
4. Le dashboard HTML

Une convention de nommage unique : `wildnexus-[domaine]` (ex. `wildnexus-camera-imaging`, `wildnexus-mechanical-enclosure`, `wildnexus-power-systems`).

---

### 14. Le plan de communication communautaire (Miel) est mentionné mais sans livrable concret avant M-04

T06.4 confie à Miel 🐝 la « stratégie visibilité sociale » mais c'est la seule tâche qui n'a pas de livrable concret avant M-04. Une « stratégie » est un document interne — pas un résultat visible pour la communauté.

**Recommandation :** définir un livrable minimum P0 pour Miel, par exemple :
- Un thread Twitter/Mastodon documentant l'EVT en temps réel (1 post/jour pendant 30 jours)
- Un article blog sur arteon.be présentant le prototype et la vision
- Une page `wildnexus.arteon.be` avec formulaire d'intérêt pour les bêta-testeurs

La communication communautaire doit commencer avant M-04, pas après.

---

### 15. L'`archive/` contient déjà un fichier — la dérive documentaire commence

`archive/Start-dobby-v0.1.md` est la première pièce archivée. C'est sain. Mais sans règle explicite, le répertoire `archive/` va gonfler de manière anarchique.

**Recommandation :** ajouter dans l'INDEX ou dans `Start.md` une règle simple :

> Tout document remplacé par une version supérieure est déplacé dans `archive/` avec la date d'archivage en préfixe (format `YYYY-MM-DD_`). L'archive n'est pas supprimée — elle conserve l'historique des décisions.

---

## Synthèse et priorisation

| Priorité | Nb | Actions | Impact si ignoré |
|----------|----|---------|-----------------|
| 🔴 Avant le `go` | 3 | Split doc fondateur, mapping agents, estimation budgétaire | Confusion équipe, doublons, budget inconnu |
| 🟡 Cycle 01 | 7 | Clarification Faune Autour, tag P1 bioacoustique, dashboard dynamique, timeline T01.2, tests firmware, nettoyage `Start` vide, `data/` | Ralentissement exécution, scope creep |
| 🟢 Fond | 5 | ADR, gateway, alignement noms agents, livrable Miel, règle archivage | Dette documentaire, ambiguïtés futures |

---

## Constat global

Le socle est solide. La vision est claire, les garde-fous sont en place, la discipline P0/P1/P2 est bien tenue. Les 15 points identifiés sont **mécaniques pour la plupart** — ils ne remettent pas en cause la vision, l'architecture, ni les non-négociables. Ce sont des corrections de forme, d'alignement, et de complétude qui transformeront un excellent DRAFT en un plan exécutable sans friction.

---

*Document généré par Dobby 🦉 — 2026-05-18 — PKA_JCH*  
*Prochaine revue : après traitement des 3 🔴 ou au prochain point JCH*
