# [[03_WILDNEXUS]]

Projet : **WildNexus — repris le 2026-11-11 (P0 engineering, décision JCH) ; gates de reprise à lever**
Sous-titre : **infrastructure distribuée d'observation écologique**
Sous-projet : **WILDNEXUS_DEVICE** (le nœud caméra P0) — ce dossier.

## Point d'entrée (2026-11-05)

Pour comprendre le projet sans confondre vision, état réel et preuves, suivre cet ordre :

1. [README du projet ombrelle](../README.md) — rôles de WILDNEXUS_DEVICE, INSECTNET et NEXUS_ACOUSTIC.
2. [Start.md](00_GOVERNANCE/Start.md) — **état réel, budget, sécurité et conditions de reprise ; source de vérité opérationnelle**.
3. **Cet INDEX** — carte des dossiers et accès aux documents de référence.
4. [Dossier technico-commercial](01_FOUNDATION/WILDNEXUS_DOSSIER_TECHNICO-COMMERCIAL_V0.md) — vision et approfondissement technico-commercial ; ne remplace ni `Start.md` ni les preuves d'avancement.

## Lecture rapide

- [Verrou de périmètre P0](01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md) — source de vérité du scope et matrice exigence → preuve.
- [Glossaire](01_FOUNDATION/GLOSSAIRE_WN.md) — vocabulaire pour nouveaux entrants.
- [Index des ADR](02_DECISIONS/WILDNEXUS_ADR_INDEX.md) — décisions techniques et statuts documentaires.
- [Avancement des protocoles](03_P0_ENGINEERING/PROTOCOLES/progress.md) — **source de vérité d'avancement et des preuves**.
- [Résumé exécutif](executive-summary.md) — synthèse externe sans promesse de performances non mesurées.
- [Budget énergie](03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/WP03_BUDGET-ENERGIE_ET_GATE-60J.md) — protocole WP03 et cible de 60 jours à démontrer.
- [Logigramme](05_VISUALS_DASHBOARDS/WILDNEXUS_FLOWMAP.md) — vue multi-étages.
- [Fiches produits](09_PRODUCT_SHEETS/INDEX.md) — visions F1 FIELD, F2 FIELD+, S1 STATION, S2 STATION+ et A1 Nexus Acoustic.

## Structure du dossier

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
| [99_REFERENCES](99_REFERENCES/) | références transverses : CCTP, Mont-le-Soie, caméra TKA, trafic gibier | référence |
| [data](data/) | données projet (placeholder et règles de dépôt) | actif |
| **firmware/** | code firmware — **dépôt git imbriqué, non versionné par PKA_JCH** ; cf. [décision firmware-repo](00_GOVERNANCE/WILDNEXUS_firmware-repo-decision.md) | actif (hors repo) |
| [**HISTORIQUE**](HISTORIQUE/) | documents anciens/superseded (fondation pré-bible, briefs, visuels, notes brutes, exec-summary v1) | archive |

Les numéros de dossiers restent stables pour préserver les liens ; un numéro absent ne justifie pas une renumérotation.

### Archives et références

- [Projet ombrelle `archive/`](../archive/) — archives communes aux trois sous-projets.
- [Device `HISTORIQUE/`](HISTORIQUE/) — anciens documents de vision, gouvernance, briefs et visuels du device.
- [Ingénierie `_archive/`](03_P0_ENGINEERING/_archive/) — anciens artefacts techniques ; le même principe vaut pour les `_archive/` locaux, notamment sous `07_PROCUREMENT_BOM/`.
- [Device `99_REFERENCES/`](99_REFERENCES/) — références transverses et contexte général du projet.
- [Ingénierie `99_REFERENCES/`](03_P0_ENGINEERING/99_REFERENCES/) — datasheets, références de conception et veille technique directement utiles au P0.

Une archive est une trace datée, jamais une source d'état actuel. Les mesures PPK2 historiques sont rangées dans `03_P0_ENGINEERING/_archive/99_REFERENCES/PPK2/`.

> **Repère historique — rangement 2026-10-29 :** anciens fichiers datés déplacés vers `HISTORIQUE/`, `01_SPECS` fusionné dans `99_REFERENCES`, notes techniques archivées et anciennes fondations absorbées par la bible V0. La présente révision ne déplace aucun dossier.

## Projets extraits

| Projet | Emplacement | Statut |
|--------|-------------|--------|
| **NEXUS_ACOUSTIC** | [../NEXUS_ACOUSTIC/](../NEXUS_ACOUSTIC/) | P1 — Bioacoustique, BirdNET, classification |
| **FAUNE_AUTOUR** | [../../06_PHOTO_NATURE/FAUNE_AUTOUR/](../../06_PHOTO_NATURE/FAUNE_AUTOUR/) | Gelé — PWA GBIF |
| **InsectNet** | [../INSECTNET/](../INSECTNET/) | Pipeline — Classification orthoptères |

## Verrou P0

Le périmètre P0 est limité au nœud caméra autonome : capture jour/nuit, cible audio stéréo locale, détection événementielle, filtre embarqué animal / non-animal, LPWAN événementiel, stockage local et configuration terrain. L'autonomie de 60 jours et la protection IP67 sont des **cibles à démontrer**, pas des performances acquises.

Explicitement hors P0 : classification bioacoustique de précision (→ NEXUS_ACOUSTIC et INSECTNET), Faune Autour (→ gelé), reconnaissance fine des espèces (P1), reconnaissance individuelle (P1/P2), cloud scientifique complet (P2), solaire (P1).

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

*Dernière mise à jour : 2026-11-11 — statut repris (P0 engineering), ordre de lecture, pointeurs projets, niveaux d'archives et distinction des références.*
