# WildNexus — Glossaire humain

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** onboarding interne — à enrichir  
**Owner :** Dobby  

## Objet

Ce glossaire aide une personne qui entre dans WildNexus à comprendre rapidement le vocabulaire projet, sans devoir lire tous les documents techniques.

Il ne remplace pas les ADR, le document fondateur ou les fiches techniques. Il donne le sens opérationnel des termes dans **ce projet**.

---

## 1. Projet et phases

| Terme | Définition WildNexus |
|---|---|
| WildNexus | Infrastructure distribuée d'observation écologique. Le projet commence par un nœud caméra autonome, puis peut évoluer vers une plateforme scientifique multi-capteurs. |
| P0 | Première phase stricte : prouver un nœud caméra autonome crédible et déployable. P0 ne couvre pas toute la plateforme finale. |
| P1 | Phase d'intelligence scientifique avancée : bioacoustique, classification d'espèces, reconnaissance individuelle, gateways locales, exports scientifiques. |
| P2 | Phase écosystème : API publique, SDK, plugins, réseau collaboratif, cloud scientifique, orchestration multi-sites. |
| Scope creep | Dérive de périmètre : ajouter à P0 des fonctions séduisantes mais non nécessaires à la preuve du nœud caméra autonome. |
| P0 strict | Principe actuel : P0 reste limité au nœud caméra. Bioacoustique, Faune Autour, cloud, espèce fine et reconnaissance individuelle restent hors P0. |
| M-01 | Jalon "Architecture P0 gelée". Les choix caméra, MCU, radio, budget, risques juridiques et supply sont assez cadrés pour passer au prototype banc. |
| M-02 | Jalon "Prototype banc fonctionnel". Le système fonctionne sur banc avant déploiement terrain. |
| M-03 | Jalon "EVT terrain validé". Le prototype est testé en conditions réelles. |
| M-04 | Jalon "socle publié / communauté amorcée". Publication et documentation deviennent utilisables par des tiers. |
| WP | Work Package. Lot de travail structuré : WP01 études, WP02 hardware, WP03 firmware, WP04 IA, WP05 terrain, WP06 communauté. |

---

## 1bis. Nomenclature WildNexus

Cette section explique les codes utilisés dans les fichiers, décisions, tâches et livrables. Elle doit rester stable pour que les humains entrants puissent lire le projet sans décoder chaque document.

### Préfixes de documents

| Code | Signification | Exemple | Usage |
|---|---|---|---|
| `ADR` | Architecture Decision Record | `ADR-001-choix-mcu-p0.md` | Décision technique structurante : contexte, options, choix, conséquences, critères de révision. |
| `WILDNEXUS_` | Document projet transverse | `WILDNEXUS_P0_SCOPE_LOCK.md` | Document de référence interne WildNexus. |
| `WP` | Work Package | `WP02 Hardware & Enclos` | Lot de travail organisé par domaine et jalon. |
| `REORG` | Trace de reclassement | `archive/2026-05-23_pre_p0_lock/00_GOVERNANCE/REORG_2026-05-18.md` | Note historique expliquant un changement de structure documentaire. |

### Préfixes de jalons et tâches

| Code | Signification | Exemple | Usage |
|---|---|---|---|
| `M-XX` | Milestone / jalon | `M-01 Architecture P0 gelée` | Point de passage go/no-go ou validation de phase. |
| `TXX.Y` | Tâche opérationnelle | `T01.3 Radio / LPWAN` | Tâche suivie dans Plane ou dans les documents de cycle. |
| `DXX.Y` | Livrable | `D01.3 Rapport RF` | Document ou résultat attendu à la sortie d'une tâche. |
| `OBJ-XX` | Objectif vérifiable | `OBJ-01 Autonomie` | Objectif projet avec critère de validation. |
| `NN-XX` | Non-négociable | `NN-05 Exclusion militaire` | Engagement constitutionnel du projet, modifiable seulement par décision JCH. |
| `GOV-XX` | Gouvernance | `GOV-01 Mapping agents / PKA` | Tâche ou décision de pilotage, rôles, méthodes ou organisation. |
| `SUPPLY-XX` | Supply chain | `SUPPLY-01 Registre composants` | Suivi des composants, fournisseurs, disponibilité et alternatives. |

### Codes de phases

| Code | Signification | Lecture |
|---|---|---|
| `P0` | Prototype terrain minimal crédible | Nœud caméra autonome uniquement. |
| `P1` | Version scientifique avancée | Bioacoustique, classification espèces, exports scientifiques, gateways. |
| `P2` | Écosystème distribué | API, SDK, cloud scientifique, réseau collaboratif. |
| `EVT` | Engineering Validation Test | Validation prototype, notamment terrain 30 jours pour P0. |
| `DVT` | Design Validation Test | Validation design plus avancée, après P0. |

### Codes techniques fréquents

| Code | Signification | Dans WildNexus |
|---|---|---|
| `MCU` | Microcontroller Unit | Cerveau basse consommation du nœud caméra. |
| `ULP` | Ultra Low Power | Contrainte centrale d'autonomie. |
| `LPWAN` | Low Power Wide Area Network | Famille radio longue portée basse consommation. |
| `LoRa` | Radio longue portée basse consommation | Candidat radio P0. |
| `LoRaWAN` | Protocole réseau au-dessus de LoRa | Option avec gateway privée ou réseau structuré. |
| `EU868` | Bande radio européenne 868 MHz | Bande cible pour tests radio en Belgique. |
| `BLE` | Bluetooth Low Energy | Configuration terrain/provisioning, pas alerte longue portée. |
| `IR` | Infrarouge | Vision nocturne. |
| `NoIR` | Sans filtre infrarouge permanent | Caméra plus adaptée à l'IR. |
| `MIPI CSI` | Interface caméra haute vitesse | Puissante mais souvent trop lourde pour P0 MCU strict. |
| `SPI` | Serial Peripheral Interface | Bus simple privilégié pour intégration MCU. |
| `I2C` | Inter-Integrated Circuit | Bus léger pour capteurs et périphériques simples. |
| `UART` | Liaison série asynchrone | Souvent utilisée pour modules radio ou debug. |
| `PSRAM` | Pseudo-static RAM | Mémoire externe utile pour images sur ESP32-S3. |
| `BOM` | Bill of Materials | Liste composants et coûts. |
| `FTO` | Freedom To Operate | Analyse de liberté d'exploitation PI. |
| `RGPD` | Règlement général sur la protection des données | Risque lié aux personnes capturées par caméra. |

### Convention de statut

| Statut | Sens |
|---|---|
| `proposé` | Hypothèse de travail structurée, non encore validée. |
| `accepté` | Décision retenue comme base de travail. |
| `remplacé` | Décision obsolète, conservée pour historique. |
| `ouvert` | Sujet actif, non résolu. |
| `fait` | Livrable produit ou tâche clôturée. |
| `à produire` | Document attendu mais non encore rédigé. |
| `à affiner` | Première version existante, précision insuffisante pour gel. |

### Commandes de session PKA

| Commande | Sens opérationnel | Usage |
|---|---|---|
| `/save` | Clôture interactive d'une session PKA. | À utiliser quand une session produit une décision, un déplacement de fichiers, une modification système ou une avancée projet. Si le client ne fournit pas de slash command native, exécuter `./bin/pka`. |
| `./bin/pka` | Raccourci court universel vers la sauvegarde interactive PKA. | Forme recommandée. Fonctionne quel que soit le modèle utilisé : Codex, Claude, Gemini, DeepSeek ou autre. |
| `./bin/pka-save` | Alias explicite vers `scripts/pka_save.py --interactive`. | Même usage que `./bin/pka`, conservé pour lisibilité et compatibilité. Capture titre, modèle, projet, résumé, actions, décisions et prochaines étapes. |
| `scripts/pka_save.py --model <modele> --project <projet>` | Sauvegarde non interactive ou semi-scriptable avec contexte modèle/projet. | À privilégier quand on veut tracer explicitement une session multi-modèles dans `wiki/Daily/` et `wiki/log.md`. |

Règle : la mémoire commune vit dans les fichiers PKA, pas dans le transcript d'un modèle. Sybil consolide automatiquement le soir, mais ne remplace pas la clôture explicite des décisions.

---

## 2. Matériel et architecture embarquée

| Terme | Définition WildNexus |
|---|---|
| Nœud caméra | Unité terrain autonome : caméra, détection, stockage, radio, énergie et boîtier. C'est le cœur du P0. |
| MCU | Microcontroller Unit. Microcontrôleur principal du nœud, responsable de la veille, du réveil, des interfaces et du pilotage des sous-systèmes. |
| ESP32-S3 | MCU candidat primaire proposé pour P0. Avantage : caméra, BLE/Wi-Fi, outillage rapide. Risque : consommation à prouver. |
| STM32U5 | MCU fallback basse consommation si ESP32-S3 échoue sur autonomie ou robustesse. |
| nRF54 / nRF54L15 | MCU/radio Nordic intéressant pour BLE basse consommation et sécurité, mais non prioritaire P0 car il ne remplace pas LPWAN et ne résout pas directement la caméra. |
| Raspberry Pi | Plateforme Linux utile pour prototypage, mais rejetée comme cœur permanent du nœud terrain P0 pour raisons de consommation, boot, SD et maintenance. |
| ULP | Ultra Low Power. Mode ou architecture permettant au système de dormir presque tout le temps pour préserver la batterie. |
| PSRAM | Mémoire externe rapide souvent nécessaire avec ESP32-S3 pour traiter ou bufferiser des images. |
| SPI | Bus série simple et courant entre MCU et périphériques. Important pour caméra SPI, stockage, radio ou capteurs. |
| I2C | Bus série léger pour capteurs et composants de configuration. |
| UART | Liaison série simple, souvent utilisée pour modules radio ou debug. |
| MIPI CSI | Interface caméra haute vitesse, fréquente sur modules avancés. Puissante mais plus lourde à intégrer sur microcontrôleur. |
| USB host | Fonction permettant de piloter un périphérique USB. Peut complexifier et alourdir un nœud basse consommation. |
| Power gating | Coupure électrique complète d'un sous-système quand il n'est pas utilisé, par exemple caméra ou IR. |

---

## 3. Image, caméra et vision nocturne

| Terme | Définition WildNexus |
|---|---|
| Caméra P0 | Caméra capable de produire une image exploitable de jour et de nuit sans imposer une architecture Linux permanente. |
| IR | Infrarouge. Éclairage nocturne invisible ou peu visible pour obtenir des images de nuit. |
| 850 nm | Longueur d'onde IR souvent plus efficace en image, mais parfois légèrement visible. |
| 940 nm | Longueur d'onde IR plus discrète, mais généralement moins efficace pour la portée et la sensibilité capteur. |
| IR-cut | Filtre qui bloque l'infrarouge en mode jour pour améliorer les couleurs, et peut être retiré en mode nuit. |
| NoIR | Caméra sans filtre IR-cut permanent, plus adaptée à la vision nocturne IR. |
| IMX462 | Capteur Sony STARVIS très intéressant pour basse lumière / proche IR. Dans WildNexus, référence qualité nocturne, pas choix P0 automatique. |
| IMX327 | Capteur Sony STARVIS basse lumière, également référence possible pour benchmark nocturne. |
| Arducam Mega SPI | Caméra SPI orientée microcontrôleurs. Candidate de benchmark pour P0 car elle simplifie l'intégration MCU. |
| M12 | Monture d'objectif compacte courante sur modules caméra embarqués. |
| Qualité image exploitable | Image suffisante pour valider présence animal / non-animal et, idéalement, permettre une identification visuelle humaine à distance cible. |
| Distance cible 5 m | Référence actuelle pour vérifier qu'une image jour/nuit est utile en terrain P0. |

---

## 4. Radio et connectivité

| Terme | Définition WildNexus |
|---|---|
| LPWAN | Low Power Wide Area Network. Réseau longue portée basse consommation, adapté aux petits messages. |
| LoRa | Technologie radio longue portée basse consommation. Candidate principale pour les messages événementiels P0. |
| LoRaWAN | Protocole réseau au-dessus de LoRa. Utile avec gateways et infrastructure, mais plus complexe qu'un lien point-à-point. |
| EU868 | Bande radio européenne autour de 868 MHz. Impose des contraintes réglementaires dont le duty-cycle. |
| SX1262 | Transceiver LoRa Semtech pris comme référence technique pour P0. |
| Murata Type 1SJ | Module LoRa basé SX1262, candidat pour prototypage rapide. |
| RAK3172(H) | Module LoRa/LoRaWAN compatible EU868, candidat pour prototypage rapide. |
| Duty-cycle | Limite de temps d'émission radio autorisé. Critique en EU868 : WildNexus doit transmettre peu et court. |
| RSSI | Indicateur de puissance du signal reçu. Utilisé pendant les tests de portée. |
| SNR | Signal-to-noise ratio. Indique la qualité du signal radio par rapport au bruit. |
| Gateway | Point relais ou passerelle locale qui reçoit les messages des nœuds et peut les transmettre ailleurs. Hors obligation P0 stricte. |
| Mesh LoRa | Réseau où les nœuds relaient les messages entre eux. Rejeté pour P0 à cause de collisions, duty-cycle, latence et consommation. |
| BLE | Bluetooth Low Energy. Utile pour configuration terrain ou provisioning, pas pour alerte longue portée forêt. |
| LTE-M / NB-IoT | Connectivité cellulaire bas débit IoT. Possible P1/P2 ou sites critiques, mais pas baseline P0. |

---

## 5. Données, IA et standards

| Terme | Définition WildNexus |
|---|---|
| Edge AI | IA exécutée sur le nœud ou très près du capteur, sans dépendre d'un cloud. |
| Classificateur binaire | Modèle IA P0 qui répond seulement : animal probable / non-animal. Il ne fait pas la classification d'espèce en P0. |
| Classification d'espèce | Identification de l'espèce observée. Objectif P1, pas P0. |
| Reconnaissance individuelle | Reconnaître un individu au sein d'une espèce, par marquages, morphologie ou comportement. Objectif P1/P2. |
| Faux positif | Événement détecté comme animal alors qu'il ne l'est pas : feuilles, pluie, ombre, mouvement parasite. |
| Dataset | Jeu de données d'images, sons ou métadonnées utilisé pour tester ou entraîner un modèle. |
| Dataset annoté | Dataset dont les événements sont étiquetés manuellement ou semi-automatiquement : animal, non-animal, espèce, qualité image, etc. |
| Métadonnées | Données décrivant un événement : date, heure, nœud, batterie, score IA, type de capture, conditions, RSSI/SNR. |
| Camtrap-DP | Standard de données pour pièges photographiques. Cible de compatibilité scientifique P1. |
| GBIF | Global Biodiversity Information Facility. Plateforme mondiale de données biodiversité, cible possible pour exports P1. |
| BirdNET | Système d'identification bioacoustique des oiseaux. Pertinent pour composant bioacoustique P1, hors P0 strict. |

---

## 6. Terrain, validation et robustesse

| Terme | Définition WildNexus |
|---|---|
| EVT | Engineering Validation Test. Validation du prototype en conditions contrôlées ou terrain initial. M-03 exige un EVT terrain. |
| DVT | Design Validation Test. Validation plus avancée du design avant industrialisation. Post-P0 dans la trajectoire actuelle. |
| Site EVT | Site belge réel où tester au moins trois nœuds pendant 30 jours. |
| 30 jours EVT | Durée minimale de test terrain P0 pour extrapoler l'autonomie et observer les défaillances. |
| 60 jours batterie seule | Engagement minimum P0 d'autonomie sans apport solaire. |
| 6 mois avec solaire | Ambition produit, pas critère de validation P0. |
| IP67 | Niveau d'étanchéité visé pour le boîtier terrain : protection poussière et immersion temporaire. |
| Enclos / boîtier | Partie mécanique qui protège électronique, caméra, batterie et optique. Critique pour humidité, IR, condensation et montage terrain. |
| LiFePO4 | Type de batterie robuste et plus sûre, candidate pour alimentation P0. |
| Solaire | Apport énergétique possible pour ambition 6 mois, mais non requis pour prouver 60 jours batterie seule en P0. |
| PIR | Capteur infrarouge passif de mouvement. Utile comme déclencheur grossier, mais insuffisant seul contre les faux positifs. |

---

## 7. Juridique, licence et gouvernance

| Terme | Définition WildNexus |
|---|---|
| ADR | Architecture Decision Record. Document court qui capture une décision technique : contexte, options, choix, conséquences, critères de révision. |
| FTO | Freedom To Operate. Analyse visant à vérifier qu'un produit peut être développé/exploité sans bloquer sur des droits tiers. |
| PI | Propriété intellectuelle. Brevets, droits, marques, licences, savoir-faire. |
| RGPD | Règlement européen sur les données personnelles. Important car les caméras peuvent capturer accidentellement des personnes. |
| Source-available | Code ou design consultable, mais pas forcément open source au sens OSI. |
| Ethical-source | Licence ou politique d'usage qui impose des restrictions alignées avec des valeurs éthiques. |
| Exclusion militaire | Non-négociable WildNexus : interdiction d'usage militaire ou paramilitaire du matériel, logiciel, données et API. |
| Usage policy | Politique d'usage qui définit ce qui est autorisé, conditionnel ou interdit. |
| Plane | Outil de pilotage/backlog utilisé pour suivre les tâches, jalons, owners et livrables WildNexus. |
| Owner PKA | Spécialiste PKA responsable de la qualité et du suivi d'un livrable. |
| Agent WildNexus | Agent local spécialisé par domaine technique. Il produit l'expertise, mais reste rattaché à un owner PKA. |

---

## 8. Composants et dossiers du projet

| Terme | Définition WildNexus |
|---|---|
| `00_GOVERNANCE/` | Pilotage projet : mapping agents, readiness M-01, backlog Plane, réorganisation. |
| `01_FOUNDATION/` | Documents fondateurs : architecture, scope, document fondateur, usage policy, glossaire. |
| `02_DECISIONS/` | ADR et décisions techniques. |
| `03_P0_ENGINEERING/` | Ingénierie P0 structurée par domaines : architecture système, hardware satellite, énergie/autonomie, connectivité, IA edge/cloud, procurement/BOM, budget, benchmarks et registres. |
| `04_PRINT_EXPORTS/` | Supports imprimables ou consolidés pour travail papier. |
| `05_VISUALS_DASHBOARDS/` | Logigrammes, dashboards, vues HTML. |
| `06_COMPONENTS/BIOACOUSTIC/` | Matière bioacoustique P1, hors P0 strict. |
| `06_COMPONENTS/FAUNE_AUTOUR_APP/` | Application Faune Autour, projet adjacent ou futur composant P2. |
| `07_AGENTS/` | Agents WildNexus locaux et leurs fichiers `SKILL.md`. |
| `08_TECH_NOTES/` | Notes techniques exploratoires, notamment graphify-notes. |
| `_quarantine/` | Zone temporaire pour éléments à vérifier avant suppression ou reclassement. |

---

## 9. Références internes

- [INDEX.md](../INDEX.md)
- [MASTER_ARCHITECTURE_WN.md](MASTER_ARCHITECTURE_WN.md)
- [wildnexus-founding-document-v0.2.md](wildnexus-founding-document-v0.2.md)
- [WILDNEXUS_P0_SCOPE_LOCK.md](WILDNEXUS_P0_SCOPE_LOCK.md)
- [../02_DECISIONS/WILDNEXUS_ADR_INDEX.md](../02_DECISIONS/WILDNEXUS_ADR_INDEX.md)
- [../00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md](../00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md)

## À enrichir ensuite

- ajouter les termes issus des ADR-004 à ADR-008 ;
- ajouter les composants précis retenus après benchmark ;
- ajouter un mini schéma "qui décide quoi" pour les nouveaux contributeurs ;
- produire une version PDF imprimable si JCH veut l'utiliser en onboarding papier.
