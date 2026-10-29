# [[03_WILDNEXUS]]

Projet actif : **WildNexus**
Sous-titre : **infrastructure distribuée d'observation écologique**
Sous-projet : **WILDNEXUS_DEVICE** (le nœud caméra P0) — ce dossier.

## ⭐ Point d'entrée (2026-10-29)

- 🟢 **[01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md](01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md)** — **LA BIBLE V0** : dossier technico-commercial consolidé (point zéro technique + revue expert). *À lire en premier.*
- **[executive-summary.md](executive-summary.md)** — résumé exécutif externe **v2 (aligné P0, sans surpromesse)**.
- **[03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/WP03_BUDGET-ENERGIE_ET_GATE-60J.md](03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/WP03_BUDGET-ENERGIE_ET_GATE-60J.md)** — WP03 : budget énergie + gate « 60 jours ».

## Lecture rapide

- [Start.md](00_GOVERNANCE/Start.md) : protocole de démarrage opérationnel — **source de vérité opérationnelle**.
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md) : **verrou de périmètre P0** (source de vérité du scope).
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md) : glossaire pour nouveaux entrants.
- [02_DECISIONS/WILDNEXUS_ADR_INDEX.md](02_DECISIONS/WILDNEXUS_ADR_INDEX.md) : index des ADRs (décisions techniques actives).
- [03_P0_ENGINEERING/PROTOCOLES/progress.md](03_P0_ENGINEERING/PROTOCOLES/progress.md) : tracker de protocoles M-02 — **source de vérité d'avancement**.
- [05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md](05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md) : logigramme multi-étages.
- [09_PRODUCT_SHEETS/INDEX.md](09_PRODUCT_SHEETS/INDEX.md) : fiches produit (F1 FIELD, F2 FIELD+, S1 STATION, S2 STATION+, A1 Nexus Acoustic).

## Structure du dossier (nettoyée 2026-10-29)

| Dossier | Contenu | Statut |
|---|---|---|
| [00_GOVERNANCE](00_GOVERNANCE/) | Start.md, philosophie, mapping agents, pilotage ; **note firmware-repo** | actif |
| [01_FOUNDATION](01_FOUNDATION/) | **bible V0**, scope lock, glossaire, usage policy/matrix | actif |
| [02_DECISIONS](02_DECISIONS/) | index ADR + ADRs | actif |
| [03_P0_ENGINEERING](03_P0_ENGINEERING/) | architecture, hardware, **énergie (WP03)**, protocoles, BOM, budget | actif |
| [05_VISUALS_DASHBOARDS](05_VISUALS_DASHBOARDS/) | FLOWMAP (les anciens visuels → HISTORIQUE) | allégé |
| [06_ADJACENT](06_ADJACENT/) | pointeur vers projets extraits | actif |
| [07_AGENTS](07_AGENTS/) | `Agents/` (définitions de rôles) ; briefs datés → HISTORIQUE | actif |
| [09_PRODUCT_SHEETS](09_PRODUCT_SHEETS/) | fiches produit F1/F2/S1/S2/A1 | actif |
| [99_REFERENCES](99_REFERENCES/) | références (CCTP, Mont-le-Soie, caméra TKA, trafic gibier) | référence |
| [data](data/) | données projet (placeholder) | actif |
| **firmware/** | code firmware — **dépôt git imbriqué, non versionné par PKA_JCH** ⚠️ cf. [00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md](00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md) | actif (hors repo) |
| [**HISTORIQUE**](HISTORIQUE/) | documents anciens/superseded (fondation pré-bible, briefs, visuels, notes brutes, exec-summary v1) | archive |

> ℹ️ **Rangement 2026-10-29** : (1) anciens fichiers datés → `HISTORIQUE/` ; (2) `01_SPECS` fusionné dans `99_REFERENCES` et supprimé (collision de préfixe) ; (3) `08_TECH_NOTES` et `99_INBOX_NOTES` déplacés dans `HISTORIQUE/` ; (4) `MASTER_ARCHITECTURE_WN`, `founding-document-v0.2` et `Dossier_de_Conception_v1` archivés (absorbés par la bible V0.2) ; (5) briefs 07_AGENTS de juin archivés. La racine ne garde que les points d'entrée actifs.

## Projets extraits

| Projet | Emplacement | Statut |
|--------|-------------|--------|
| **NEXUS_ACOUSTIC** | [../NEXUS_ACOUSTIC/](../NEXUS_ACOUSTIC/) | P1 — Bioacoustique, BirdNET, classification |
| **FAUNE_AUTOUR** | [../FAUNE_AUTOUR/](../FAUNE_AUTOUR/) | ⚪ Gelé — PWA GBIF |
| **InsectNet** | [../INSECTNET/](../INSECTNET/) | 🟡 Pipeline — Classification orthoptères |

## Verrou P0

Le périmètre P0 est strictement limité au nœud caméra autonome : capture jour/nuit, capture audio stéréo locale, détection événementielle, filtre embarqué animal / non-animal, LPWAN événementiel, stockage local, configuration terrain, autonomie ≥ 60 j, boîtier IP67.

Explicitement hors P0 : bioacoustique (→ NEXUS_ACOUSTIC), Faune Autour (→ gelé), reconnaissance espèce fine (P1), reconnaissance individuelle (P1/P2), cloud scientifique complet (P2), solaire (P1).

Référence : [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)

## Governance

- [00_GOVERNANCE/Start.md](00_GOVERNANCE/Start.md) — **protocole de lancement (source de vérité opérationnelle)**
- [00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md](00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md)
- [00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md](00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md)
- [00_GOVERNANCE/wildnexus-plane-operating-model.md](00_GOVERNANCE/wildnexus-plane-operating-model.md)
- [00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md](00_GOVERNANCE/WILDNEXUS_ENGINEERING_PHILOSOPHY.md)
- [00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md](00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md)
- [00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md](00_GOVERNANCE/WILDNEXUS_GLOSSARY_WEEKLY_CHECK.md)

## Foundation (actif)

- **[01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md](01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md)** — **bible V0**
- [01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)
- [01_FOUNDATION/GLOSSAIRE_WN.md](01_FOUNDATION/GLOSSAIRE_WN.md)
- [01_FOUNDATION/WILDMESH_project_brief.md](01_FOUNDATION/WILDMESH_project_brief.md)
- [01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md](01_FOUNDATION/wildnexus-usage-policy-and-license-principles.md)
- [01_FOUNDATION/wildnexus-usage-matrix.md](01_FOUNDATION/wildnexus-usage-matrix.md)

---

*Dernière mise à jour : 2026-10-29 — bible V0.2, exec v2, WP03 ; nettoyage de structure (HISTORIQUE), fusion 01_SPECS, note décision firmware.*
