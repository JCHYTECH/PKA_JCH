# [[03_WILDNEXUS]]

Projet actif : **WildNexus**  
Sous-titre : **infrastructure distribuée d'observation écologique**

## Lecture rapide

- [Start.md](Start.md) : protocole de démarrage opérationnel.
- [01_FOUNDATION/MASTER_ARCHITECTURE_WN.md](01_FOUNDATION/MASTER_ARCHITECTURE_WN.md) : vision produit, architecture et cadrage.
- [01_FOUNDATION/wildnexus-founding-document-v0.2.md](01_FOUNDATION/wildnexus-founding-document-v0.2.md) : document fondateur consolidé.
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md) : glossaire humain pour nouveaux entrants.
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md) : verrou de périmètre P0.
- [05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md](05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md) : logigramme multi-étages.
- [archive/2026-05-23_pre_p0_lock](archive/2026-05-23_pre_p0_lock/) : livrables et explorations pré-verrouillage P0.

## Structure du dossier

| Dossier | Contenu |
|---|---|
| [00_GOVERNANCE](00_GOVERNANCE/) | mapping agents, readiness M-01, pilotage Plane |
| [01_FOUNDATION](01_FOUNDATION/) | documents fondateurs, scope, usage policy, diagnostic |
| [02_DECISIONS](02_DECISIONS/) | index ADR et décisions architecturales |
| [03_P0_ENGINEERING](03_P0_ENGINEERING/) | architecture système, hardware satellite, énergie/autonomie, connectivité mesh/LoRa/LTE, simulation (Wokwi + test harness), procurement BOM, budget, benchmarks, protocoles, templates, **99_REFERENCES** (ESP-DIVE, PPK2, veille, datasheets) |
| [05_VISUALS_DASHBOARDS](05_VISUALS_DASHBOARDS/) | flowmaps, dashboards, vues HTML, diagrammes |
| [06_ADJACENT](06_ADJACENT/) | ponts vers projets adjacents : NEXUS_ACOUSTIC, FAUNE_AUTOUR, InsectNet |
| [07_AGENTS](07_AGENTS/) | briefs d'agents WildNexus |
| [08_TECH_NOTES](08_TECH_NOTES/) | notes techniques (reclassé 2026-06-19) |
| [data](data/) | données projet |
| [_quarantine](_quarantine/) | éléments à vérifier avant suppression |

## Projets extraits (2026-06-19)

| Projet | Emplacement | Statut |
|--------|-------------|--------|
| **NEXUS_ACOUSTIC** | [../12_NEXUS_ACOUSTIC/](../12_NEXUS_ACOUSTIC/) | P1 — Bioacoustique, BirdNET, classification |
| **FAUNE_AUTOUR** | [../FAUNE_AUTOUR/](../FAUNE_AUTOUR/) | ⚪ Gelé — PWA GBIF |
| **InsectNet** | [../10_InsectNet/](../10_InsectNet/) | 🟡 Pipeline — Classification orthoptères |

Ces projets étaient hébergés dans `06_COMPONENTS/` (renommé `06_ADJACENT/`). Ils sont désormais des projets autonomes.

## Verrou P0

Le périmètre P0 est strictement limité au nœud caméra autonome : capture jour/nuit, détection événementielle, filtre embarqué animal / non-animal, LPWAN événementiel, stockage local, configuration terrain, autonomie minimale et boîtier IP67.

Explicitement hors P0 :

- bioacoustique : P1 deferred → projet **NEXUS_ACOUSTIC** ;
- Faune Autour : adjacent ou P2 → projet **FAUNE_AUTOUR** (gelé) ;
- reconnaissance espèce fine : P1 ;
- reconnaissance individuelle : P1/P2 ;
- cloud scientifique complet : P2.

Référence : [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)

## Governance

- [00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md](00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md)
- [00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md](00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md)
- [00_GOVERNANCE/wildnexus-plane-operating-model.md](00_GOVERNANCE/wildnexus-plane-operating-model.md)
- [00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md](00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md)

## Foundation

- [01_FOUNDATION/MASTER_ARCHITECTURE_WN.md](01_FOUNDATION/MASTER_ARCHITECTURE_WN.md)
- [01_FOUNDATION/wildnexus-founding-document-v0.2.md](01_FOUNDATION/wildnexus-founding-document-v0.2.md)
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md)
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)
- [01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md](01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md)
- [01_FOUNDATION/wildnexus-usage-matrix.md](01_FOUNDATION/wildnexus-usage-matrix.md)

---

*Dernière mise à jour : 2026-06-19 — Réorganisation WildNexus (extraction NEXUS_ACOUSTIC, FAUNE_AUTOUR)*
