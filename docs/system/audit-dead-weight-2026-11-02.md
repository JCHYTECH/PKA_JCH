# Audit dead weight — 2026-11-02

Méthode : scan de 68 sessions DeepSeek TUI (`_local/sessions/` + racine), extraction des
3722 commandes `exec_shell`, des 44 `load_skill`, des mentions textuelles, croisées avec
l'inventaire réel des skills/scripts + plists launchd + références croisées.

## Chiffres clés

- **Skills** : 69 au total (35 maison + 34 génériques) → **9 chargés** (`load_skill`), **60 jamais chargés (87 %)**.
- **Scripts** : 224 fichiers (`scripts/` + `bin/`) → **42 jamais référencés** (ni sessions, ni launchd, ni croisements).

## Conclusion (corrigée après question de JC)

Les 27 skills maison jamais chargés sont **tous rédigés et substantiels** (1,7 à 8,8 Ko).
Le problème n'est **pas le stock, c'est le déclenchement** : ce sont des skills utiles mais
dormants, redondants, ou oubliés — pas inutiles. Archiver en bloc ne résoudrait rien.

## Tri en 3 colonnes (27 skills jamais chargés)

### A. ANCRER — garder + écrire le déclencheur (22)
| Skill | Déclencheur à ancrer |
|---|---|
| `arbor-research` | « recherche autonome », « hypothèse → expérience » |
| `bench-loop` | exécution SOP hardware (WildNexus) |
| `bioacoustics-qc-playbook` | tri/QC bioacoustique (WildNexus) |
| `compound-memoire` | après une correction de JC (« apprends de cette erreur ») |
| `conseil` | décision difficile (« passe ça au conseil ») |
| `decision-gate` | AVANT toute action destructive/sortante (à câbler automatiquement) |
| `decouvertes-to-planner` | export découvertes → Lupo Planner |
| `dobby-voice` | « dictée », « transcris », « parle à Dobby » |
| `edge-ai-loop` | optimisation TinyML (WildNexus) |
| `forge-loop` | revue de code / « auto-fix » |
| `gmail_imap_fetch` | « récupère mes mails » |
| `iot-vanlife` | domotique van Lupo (IoT) |
| `jade-traduction-bilingue` | traduction VETALYX/DIAHO |
| `pka-pointer-sync` | après un changement d'équipe/pointers |
| `pka-thread-file` | fin de session projet |
| `seo-loop` | optimisation SEO (Arteon/WildLens) |
| `sigma-loop` | validation données financières (Sigma) |
| `status` | « statut », « où en est l'équipe » |
| `system-improvement-ingest` | analyse d'un document → améliorations système |
| `vente-occasion` | vente d'un objet d'occasion (Belgique) |
| `wildnexus-adr` | « crée un ADR » WildNexus |
| `wildnexus-bom` | génération BOM WildNexus |

### B. FUSIONNER — redondant avec un script ou un autre skill (4)
| Skill | Fusionne avec |
|---|---|
| `capture` | `ingest` (les deux = entrée knowledge ; garder `ingest`) |
| `pka-weekly-report` | `bin/dobby-weekly-report` (le script fait déjà le rapport) |
| `wildnexus-benchmark-loop` | `bench-loop` (même boucle, générique vs spécifique) |
| `pka-print` | `bin/pka-print` (le script imprime déjà) |

### C. ARCHIVER — obsolète (1, à confirmer)
| Skill | Raison |
|---|---|
| `obsidian-knowledge-graph` | projet wikilinks Obsidian probablement terminé |

## Scripts orphelins (rappel)

- **À garder** : launchers GUI (`lancer-*.command`, 6), rotations de clés (`rotate_*_key.sh`, 4), serveurs MCP (`mcp_*`, 3).
- **À archiver** : installateurs/désinstallateurs launchd (~10) + migrations one-shot (`migrate_*`, `seed_*`, `build_vetalyx_*`, `rpi_*`, 8) — rejouables depuis git.
- **À examiner** (~10) : `dropbox_watch`, `google_calendar_bridge`, `pka_cost_tracker`, `pka_kanban_bootstrap`, etc.

## Prochaine action

Le vrai chantier : **ancrer les déclencheurs** des 22 skills utiles dans un index central
(« quand X arrive → charge le skill Y »), pour que Dobby les rappelle au bon moment.
Ensuite seulement : fusionner les 4 redondants, archiver les obsolètes.
