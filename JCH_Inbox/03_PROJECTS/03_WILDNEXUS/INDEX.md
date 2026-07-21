# [[03_WILDNEXUS]]

Projet actif : **WildNexus**  
Sous-titre : **infrastructure distribuée d'observation écologique**

## Lecture rapide

- [Start.md](00_GOVERNANCE/Start.md) : protocole de démarrage opérationnel — **source de vérité opérationnelle**.
- [01_FOUNDATION/MASTER_ARCHITECTURE_WN.md](01_FOUNDATION/MASTER_ARCHITECTURE_WN.md) : vision produit, architecture et cadrage — *document de cadrage initial (mai 2026)*.
- [01_FOUNDATION/wildnexus-founding-document-v0.2.md](01_FOUNDATION/wildnexus-founding-document-v0.2.md) : document fondateur consolidé — *DRAFT, validation JC en cours*.
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md) : glossaire humain pour nouveaux entrants.
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md) : verrou de périmètre P0.
- [02_DECISIONS/WILDNEXUS_ADR_INDEX.md](02_DECISIONS/WILDNEXUS_ADR_INDEX.md) : index des 14 ADRs.
- [03_P0_ENGINEERING/PROTOCOLES/progress.md](03_P0_ENGINEERING/PROTOCOLES/progress.md) : tracker de protocoles M-02 — **source de vérité d'avancement**.
- [05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md](05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md) : logigramme multi-étages.
- [09_PRODUCT_SHEETS/INDEX.md](09_PRODUCT_SHEETS/INDEX.md) : fiches produit (F1 FIELD, F2 FIELD+, S1 STATION, S2 STATION+, A1 Nexus Acoustic).

## Structure du dossier

| Dossier | Contenu |
|---|---|
| [00_GOVERNANCE](00_GOVERNANCE/) | Start.md, mapping agents, readiness M-01, philosophie d'ingénierie, pilotage Plane |
| [01_FOUNDATION](01_FOUNDATION/) | documents fondateurs, scope, usage policy, usage matrix, glossaire |
| [02_DECISIONS](02_DECISIONS/) | index ADR + 14 ADRs autonomes |
| [03_P0_ENGINEERING](03_P0_ENGINEERING/) | architecture système, hardware satellite, énergie/autonomie, connectivité mesh/LoRa/LTE, simulation (Wokwi + test harness), procurement BOM, budget, benchmarks, protocoles, **99_REFERENCES** (ESP-DIVE, PPK2, veille, datasheets) |
| [05_VISUALS_DASHBOARDS](05_VISUALS_DASHBOARDS/) | flowmaps, dashboards, vues HTML, diagrammes |
| [06_ADJACENT](06_ADJACENT/) | références vers projets extraits (NEXUS_ACOUSTIC, FAUNE_AUTOUR, InsectNet) |
| [07_AGENTS](07_AGENTS/) | briefs d'agents WildNexus |
| [08_TECH_NOTES](08_TECH_NOTES/) | notes techniques (reclassé 2026-06-19) |
| [09_PRODUCT_SHEETS](09_PRODUCT_SHEETS/) | fiches produit gamme complète (F1/F2/S1/S2/A1) |
| [99_INBOX_NOTES](99_INBOX_NOTES/) | notes de recherche non triées (caméra ESP32, OV5640, etc.) |
| [data](data/) | données projet (initialisé, vide pour l'instant) |

## Projets extraits (2026-06-19)

| Projet | Emplacement | Statut |
|--------|-------------|--------|
| **NEXUS_ACOUSTIC** | [../12_NEXUS_ACOUSTIC/](../12_NEXUS_ACOUSTIC/) | P1 — Bioacoustique, BirdNET, classification |
| **FAUNE_AUTOUR** | [../FAUNE_AUTOUR/](../FAUNE_AUTOUR/) | ⚪ Gelé — PWA GBIF |
| **InsectNet** | [../10_InsectNet/](../10_InsectNet/) | 🟡 Pipeline — Classification orthoptères |

## Verrou P0

Le périmètre P0 est strictement limité au nœud caméra autonome : capture jour/nuit, capture audio stéréo locale, détection événementielle, filtre embarqué animal / non-animal, LPWAN événementiel, stockage local, configuration terrain, autonomie minimale et boîtier IP67.

Explicitement hors P0 : bioacoustique (→ NEXUS_ACOUSTIC), Faune Autour (→ projet gelé), reconnaissance espèce fine (P1), reconnaissance individuelle (P1/P2), cloud scientifique complet (P2).

Référence : [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)

## Governance

- [00_GOVERNANCE/Start.md](00_GOVERNANCE/Start.md) — **protocole de lancement (source de vérité opérationnelle)**
- [00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md](00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md)
- [00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md](00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md)
- [00_GOVERNANCE/wildnexus-plane-operating-model.md](00_GOVERNANCE/wildnexus-plane-operating-model.md)
- [00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md](00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md)
- [00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md](00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md)

## Foundation

- [01_FOUNDATION/MASTER_ARCHITECTURE_WN.md](01_FOUNDATION/MASTER_ARCHITECTURE_WN.md) — *document de cadrage initial*
- [01_FOUNDATION/wildnexus-founding-document-v0.2.md](01_FOUNDATION/wildnexus-founding-document-v0.2.md) — *DRAFT*
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md)
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)
- [01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md](01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md)
- [01_FOUNDATION/wildnexus-usage-matrix.md](01_FOUNDATION/wildnexus-usage-matrix.md)

---

*Dernière mise à jour : 2026-06-30 — Nettoyage projet, alignement ADR, corrélations inter-fichiers.*
