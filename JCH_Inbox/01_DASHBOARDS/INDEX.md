# DASHBOARDS — Index général

Dernière mise à jour : 2026-05-13

## Structure
| Dossier | Contenu |
|---|---|
| 00_INBOX | Zone d'atterrissage — fichiers entrants non traités |
| 01_DASHBOARDS | Index général et navigation |
| 02_COMPANY_JCH | Documents société — media, branding |
| 03_PROJECTS | Projets actifs — un sous-dossier par projet |
| 04_PILOTAGE_STRATEGIQUE | Pilotage transverse — priorités, arbitrages, roadmap, KPI |
| 05_CONTEXT_JCH | Contexte personnel JCH — CV, biographie, manifestes |
| 06_ADMIN | Administration, comptabilité, légal |
| 07_ARCHIVES | Archives — documents inactifs |
| 90_TEMPLATES | Templates réutilisables |
| 99_SYSTEM | Système — configuration, scripts |

## Dashboards HTML
| Page | Description |
|------|-------------|
| [Hub PKA](hub.html) | Hub superviseur : pilotage, projets, inbox, archives |
| [Modèles Dobby](modeles.html) | Sélecteur de modèles et lanceurs de discussion terminal |
| [Dobby Live](dobby-live.html) | Prototype voix temps réel Realtime 2 + tools PKA locaux |
| [Organigramme](organigramme.html) | Vue équipe PKA |

Note : l'ancienne page `1.html` a ete remplacee par `hub.html`.

## Lancement recommande
- Double-clic : `lancer-dashboard.command`
- Terminal : `./dashboardctl.sh open`
- Port fixe par defaut : `8787`

## Demarrage automatique macOS
- Installer au login : `./install-dashboard-launchd.sh`
- Retirer : `./uninstall-dashboard-launchd.sh`
- Service `launchd` : `com.jchytech.pka-dashboard`

## Projets 03
| Projet | Description | Statut |
|--------|-------------|--------|
| [01_AI_IT_TOOLS](../03_PROJECTS/01_AI_IT_TOOLS/INDEX.md) | Outils AI et ressources techniques transversales | Actif |
| [02_ARTEON](../03_PROJECTS/02_ARTEON/INDEX.md) | Plateforme éditoriale photographique naturaliste | Actif |
| [03_WILDNEXUS](../03_PROJECTS/03_WILDNEXUS/INDEX.md) | WildNexus : nœud caméra autonome P0 et observation écologique distribuée | Actif |
| [04_NUANCES](../03_PROJECTS/archive/reanimable/04_NUANCES/INDEX.md) | Consultance stratégique BESS | Archive reactivable |
| [05_PHOTO_AI_JURY](../03_PROJECTS/05_PHOTO_AI_JURY/) | Analyses et exports autour du jury critique photo | Actif |
| [06_PHOTO_NATURE](../03_PROJECTS/06_PHOTO_NATURE/INDEX.md) | Activités wildlife, impression et terrain | Actif |
| [07_TRAVELS](../03_PROJECTS/07_TRAVELS/INDEX.md) | Voyages, logistique van et repérages photo | Actif |
| [08_VETALYX](../03_PROJECTS/08_VETALYX/INDEX.md) | Diagnostic allergies animales, stratégie et marché EU | Actif |

## Archive recente
- [09_BOIS_CHEVREUILS](../07_ARCHIVES/09_BOIS_CHEVREUILS/INDEX.md) — archive projet de gestion forestiere

## Convention de nommage
- Fichiers : `AAAA-MM-JJ_nom-fichier.ext`
- Dossiers : `NOM-PROJET` en majuscules, sous-dossiers en minuscules
