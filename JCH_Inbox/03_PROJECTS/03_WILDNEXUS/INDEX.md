# [[03_WILDNEXUS]]

Projet actif : **WildNexus**  
Sous-titre : **infrastructure distribuee d'observation ecologique**

## Lecture rapide

- [Start.md]([[Start]].md) : protocole de demarrage operationnel.
- [01_FOUNDATION/[[MASTER_ARCHITECTURE_WN]].md](01_FOUNDATION/[[MASTER_ARCHITECTURE_WN]].md) : vision produit, architecture et cadrage.
- [01_FOUNDATION/[[wildnexus-founding-document-v0.2]].md](01_FOUNDATION/[[wildnexus-founding-document-v0.2]].md) : document fondateur consolide.
- [01_FOUNDATION/[[GLOSSAIRE_WN]].md](01_FOUNDATION/[[GLOSSAIRE_WN]].md) : glossaire humain pour nouveaux entrants.
- [01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md](01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md) : verrou de perimetre P0.
- [05_VISUALS_DASHBOARDS/[[WILDNEXUS_FLOWMAP]].md](05_VISUALS_DASHBOARDS/[[WILDNEXUS_FLOWMAP]].md) : logigramme multi-etages.
- [archive/2026-05-23_pre_p0_lock](archive/2026-05-23_pre_p0_lock/) : livrables et explorations pre-verrouillage P0.

## Structure du dossier

| Dossier | Contenu |
|---|---|
| [00_GOVERNANCE](00_GOVERNANCE/) | mapping agents, readiness M-01, pilotage Plane |
| [01_FOUNDATION](01_FOUNDATION/) | documents fondateurs, scope, usage [[policy]], diagnostic |
| [02_DECISIONS](02_DECISIONS/) | index ADR et [[decisions]] architecturales |
| [03_P0_ENGINEERING](03_P0_ENGINEERING/) | budget P0, registre supply, templates WP |
| [04_PRINT_EXPORTS](04_PRINT_EXPORTS/) | exports actifs a regenerer apres verrou P0 |
| [05_VISUALS_DASHBOARDS](05_VISUALS_DASHBOARDS/) | flowmaps, dashboards, vues HTML |
| [06_COMPONENTS](06_COMPONENTS/) | composants adjacents ou futurs : bioacoustique, Faune Autour |
| [07_AGENTS](07_AGENTS/) | agents WildNexus locaux et leurs `SKILL.md` |
| [08_TECH_NOTES](08_TECH_NOTES/) | notes techniques actives, graphify-notes, API |
| [data](data/) | donnees projet |
| [exports](exports/) | exports historiques ou externes |
| [archive](archive/) | contenus inactifs |
| [_quarantine](_quarantine/) | elements a verifier avant suppression, dont ancien dossier `VScode` |

## Governance

- [00_GOVERNANCE/[[WILDNEXUS_AGENT_MAPPING]].md](00_GOVERNANCE/[[WILDNEXUS_AGENT_MAPPING]].md)
- [00_GOVERNANCE/[[WILDNEXUS_CYCLE_01_M01_READINESS]].md](00_GOVERNANCE/[[WILDNEXUS_CYCLE_01_M01_READINESS]].md)
- [00_GOVERNANCE/[[wildnexus-plane-operating-model]].md](00_GOVERNANCE/[[wildnexus-plane-operating-model]].md)
- [00_GOVERNANCE/[[wildnexus-plane-seed-backlog]].md](00_GOVERNANCE/[[wildnexus-plane-seed-backlog]].md)
- [00_GOVERNANCE/[[WILDNEXUS_GLOSSARY_WEEKLY_CHECK]].md](00_GOVERNANCE/[[WILDNEXUS_GLOSSARY_WEEKLY_CHECK]].md)

## Foundation

- [01_FOUNDATION/[[MASTER_ARCHITECTURE_WN]].md](01_FOUNDATION/[[MASTER_ARCHITECTURE_WN]].md)
- [01_FOUNDATION/[[wildnexus-founding-document-v0.2]].md](01_FOUNDATION/[[wildnexus-founding-document-v0.2]].md)
- [01_FOUNDATION/[[GLOSSAIRE_WN]].md](01_FOUNDATION/[[GLOSSAIRE_WN]].md)
- [01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md](01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md)
- [01_FOUNDATION/[[wildnexus-usage-[[policy]]-and-license-principles]].md](01_FOUNDATION/[[wildnexus-usage-[[policy]]-and-license-principles]].md)
- [01_FOUNDATION/[[wildnexus-usage-matrix]].md](01_FOUNDATION/[[wildnexus-usage-matrix]].md)

## Decisions et P0

- [02_DECISIONS/[[WILDNEXUS_ADR_INDEX]].md](02_DECISIONS/[[WILDNEXUS_ADR_INDEX]].md)
- [02_DECISIONS/ADR/[[ADR-001-choix-mcu-p0]].md](02_DECISIONS/ADR/[[ADR-001-choix-mcu-p0]].md)
- [02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md](02_DECISIONS/ADR/[[ADR-002-choix-camera-ir-p0]].md)
- [02_DECISIONS/ADR/[[ADR-003-choix-radio-lpwan-p0]].md](02_DECISIONS/ADR/[[ADR-003-choix-radio-lpwan-p0]].md)
- [02_DECISIONS/ADR/[[ADR-004-stockage-local-p0]].md](02_DECISIONS/ADR/[[ADR-004-stockage-local-p0]].md)
- [02_DECISIONS/ADR/[[ADR-005-energie-autonomie-p0]].md](02_DECISIONS/ADR/[[ADR-005-energie-autonomie-p0]].md)
- [02_DECISIONS/ADR/[[ADR-006-boitier-ip67-montage-terrain]].md](02_DECISIONS/ADR/[[ADR-006-boitier-ip67-montage-terrain]].md)
- [02_DECISIONS/ADR/[[ADR-007-detection-evenementielle-p0]].md](02_DECISIONS/ADR/[[ADR-007-detection-evenementielle-p0]].md)
- [02_DECISIONS/ADR/[[ADR-008-interface-capteurs-extensible-p0]].md](02_DECISIONS/ADR/[[ADR-008-interface-capteurs-extensible-p0]].md)
- [02_DECISIONS/ADR/[[ADR-009-architecture-satellite-base-cloud]].md](02_DECISIONS/ADR/[[ADR-009-architecture-satellite-base-cloud]].md)
- [03_P0_ENGINEERING/[[2026-05-23_WP01_architecture_freeze_summary]].md](03_P0_ENGINEERING/[[2026-05-23_WP01_architecture_freeze_summary]].md)
- [03_P0_ENGINEERING/[[WILDNEXUS_P0_BUDGET_RANGE]].md](03_P0_ENGINEERING/[[WILDNEXUS_P0_BUDGET_RANGE]].md)
- [03_P0_ENGINEERING/[[WILDNEXUS_SUPPLY_REGISTER]].md](03_P0_ENGINEERING/[[WILDNEXUS_SUPPLY_REGISTER]].md)
- [03_P0_ENGINEERING/WildNexus_P0_Autonomy_Model.xlsx](03_P0_ENGINEERING/WildNexus_P0_Autonomy_Model.xlsx)
- [03_P0_ENGINEERING/[[2026-05-23_WP02_hardware_matrix_encombrement_v0.1]].md](03_P0_ENGINEERING/[[2026-05-23_WP02_hardware_matrix_encombrement_v0.1]].md)

## Supports visuels et imprimables

- [../../99_SYSTEM/[[diagramming-standard]].md](../../99_SYSTEM/[[diagramming-standard]].md) : standard commun pour croquis et logigrammes.
- [05_VISUALS_DASHBOARDS/wildnexus-flowmap.html](05_VISUALS_DASHBOARDS/wildnexus-flowmap.html)
- [05_VISUALS_DASHBOARDS/wildnexus-dashboard.html](05_VISUALS_DASHBOARDS/wildnexus-dashboard.html)
- Les exports imprimables pre-verrouillage P0 sont archives dans [archive/2026-05-23_pre_p0_lock/04_PRINT_EXPORTS](archive/2026-05-23_pre_p0_lock/04_PRINT_EXPORTS/).

## Composants adjacents

- [06_COMPONENTS/BIOACOUSTIC](06_COMPONENTS/BIOACOUSTIC/) : composant bioacoustique P1 deferred.
- [06_COMPONENTS/FAUNE_AUTOUR_APP](06_COMPONENTS/FAUNE_AUTOUR_APP/) : application Faune Autour, projet adjacent ou composant P2 potentiel.

## Verrou P0

Le perimetre P0 est strictement limite au noeud camera autonome : capture jour/nuit, detection evenementielle, filtre embarque animal / non-animal, LPWAN evenementiel, stockage local, configuration terrain, autonomie minimale et boitier IP67.

Explicitement hors P0 :

- bioacoustique : P1 deferred ;
- Faune Autour : adjacent ou P2 ;
- reconnaissance espece fine : P1 ;
- reconnaissance individuelle : P1/P2 ;
- cloud scientifique complet : P2.

Reference : [01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md](01_FOUNDATION/[[WILDNEXUS_P0_SCOPE_LOCK]].md)
