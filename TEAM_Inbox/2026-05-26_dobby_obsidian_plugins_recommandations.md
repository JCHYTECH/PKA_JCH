# 2026-05-26 — Recommandations [[Obsidian]] pour PKA_JCH

## Mandat

Analyser les plugins et configurations [[Obsidian]] utiles pour le vault PKA_JCH, maintenant que les wikilinks sont cohérents et que la vue graphe devient exploitable.

## Equipe mobilisee

- [[Dobby]] : orchestration et arbitrage.
- [[Corbeau]] : coherence [[knowledge]] graph et gouvernance documentaire.
- [[Sybil]] : journal quotidien, captures et routines de cloture.
- [[Forge]] : configuration technique, sauvegarde et automatisation locale.
- [[Furet]] : veille ecosysteme plugins [[Obsidian]].

## Etat local observe

Le vault utilise actuellement une configuration [[Obsidian]] minimale :

- Core plugins actifs : Graph, Backlinks, Canvas, Outgoing Links, Tags, Properties, Daily Notes, Templates, Workspaces, File Recovery, Sync, Bases, Web Viewer.
- Aucun plugin communautaire installe dans `.obsidian`.
- Vue graphe active, avec affichage des orphelins et liens non resolus conserve.
- Protocole PKA de wikilinking : liens stables, lisibles, peu ambigus, sans creation massive aveugle.

## Principe directeur

Installer peu de plugins, mais les choisir pour quatre fonctions :

1. Requetes et tableaux de bord.
2. Capture et normalisation des notes.
3. Controle qualite du vault.
4. Sauvegarde et versioning.

Tout plugin qui automatise des modifications massives doit rester sous controle manuel ou semi-automatique. Le graphe PKA doit rester gouvernable.

## Lot 1 — Installation recommandee maintenant

### Dataview

Priorite : haute.

Usage PKA :
- generer des vues dynamiques sur les notes Daily, SOPs, Workstreams, Knowledge ;
- lister les notes sans YAML minimal ;
- suivre les fichiers `status: draft`, `status: review`, `status: active` ;
- creer des tableaux de bord projet sans dupliquer l'information.

Decision : installer.

### Templater

Priorite : haute.

Usage PKA :
- creer des templates plus puissants que le core plugin Templates ;
- standardiser Daily, SOP, Workstream, Knowledge, projet, fiche contact ;
- pre-remplir dates, chemins, slugs et frontmatter.

Decision : installer, mais garder les templates simples.

### QuickAdd

Priorite : haute.

Usage PKA :
- capturer rapidement une idee, une decision, une note Daily, une entree projet ;
- router vers les bons dossiers sans friction ;
- reduire les fichiers errants dans `00_INBOX`.

Decision : installer apres Templater.

### Linter

Priorite : haute, mais usage prudent.

Usage PKA :
- normaliser frontmatter, titres, espaces, fins de fichier ;
- detecter les notes mal formees ;
- appliquer des corrections sur demande, pas en auto-save au depart.

Decision : installer, avec execution manuelle uniquement au debut.

### [[Obsidian]] [[Git]]

Priorite : haute si [[Git]] reste le filet de securite principal.

Usage PKA :
- commits automatiques ou semi-automatiques ;
- historique lisible des changements du vault ;
- retour arriere facile apres passe de wikilinking ou lint.

Decision : installer si le vault est gere en [[Git]] ; configurer en mode prudent.

## Lot 2 — Utile ensuite, selon usage

### Tasks

Usage PKA :
- consolider les cases a cocher `- [ ]` dans les Daily, projets, SOPs ;
- filtrer par date, dossier, tag, priorite.

Decision : installer si JCH veut gerer les actions dans [[Obsidian]] plutot que dans un outil externe.

### Calendar + Periodic Notes

Usage PKA :
- navigation plus confortable dans les Daily ;
- creation de notes hebdo/mensuelles si [[Sybil]] structure des revues periodiques.

Decision : installer si le journal devient un cockpit quotidien.

### Omnisearch

Usage PKA :
- recherche plus rapide et plus riche dans un vault qui grossit ;
- utile surtout si PDFs, images OCRisees ou gros corpus documentaire deviennent centraux.

Decision : installer si la recherche native devient insuffisante.

### Tag Wrangler

Usage PKA :
- renommer et fusionner des tags sans casse ;
- auditer les tags proliferants.

Decision : installer plus tard, quand la taxonomie aura suffisamment de volume.

## Lot 3 — A eviter pour l'instant

### Auto Link Title

Peut etre pratique pour les URL, mais risque de creer du bruit si utilise massivement. PKA privilegie les liens internes et les references gouvernees.

### Plugins IA dans [[Obsidian]]

A eviter tant que l'architecture multi-modeles PKA/[[Codex]]/[[Claude]]/Gemini n'est pas stabilisee. Les [[decisions]] et memoires doivent rester dans les fichiers PKA, pas dans des conversations ou index opaques de plugin.

### Plugins de graph avance

A reporter. La vue graphe native suffit pour valider la coherence. Avant d'ajouter une couche visuelle avancee, il faut finaliser dictionnaire, aliases et review queue.

## Configurations core recommandees

### Files & Links

- `Use [[Wikilinks]]` : oui.
- `Detect all file extensions` : utile pour integrer PDF, images, scripts et documents au graphe documentaire.
- `New link format` : chemin relatif ou shortest path stable, a fixer une fois.
- `Default location for new notes` : `JCH_Inbox/00_INBOX/` ou dossier `wiki/raw/`, selon le pipeline choisi.
- `Default location for attachments` : `wiki/images/` ou `wiki/assets/`, pas racine du vault.

### Daily Notes

- Nouveau chemin recommande : `wiki/Daily/YYYY/MM/YYYY-MM-DD-<slug>.md`.
- Template dedie : `wiki/90_TEMPLATES/daily.md` ou equivalent local.
- Eviter la coexistence durable entre anciennes Daily plates et nouvelles Daily classees.

### Graph

Groupes de couleur recommandes :
- `path:TEAM/` pour les specialistes.
- `path:JCH_Inbox/03_PROJECTS/` pour les projets.
- `path:wiki/Daily/` pour le journal.
- `path:wiki/Knowledge/` pour la connaissance consolidee.
- `path:wiki/SOPs/ OR path:wiki/Workstreams/` pour les procedures.

Filtres utiles :
- garder les liens non resolus visibles pendant la phase de nettoyage ;
- masquer les attachments si la vue devient illisible ;
- conserver les orphelins tant que le protocole wikilink n'est pas stabilise.

### Properties

Schema minimal a standardiser :

```yaml
type:
status:
dateCreated:
dateModified:
tags:
owner:
project:
```

Valeurs `type` initiales :
- [[daily]]
- [[knowledge]]
- [[sop]]
- [[workstream]]
- project
- specialist
- [[inbox]]
- decision
- vendor
- contact

Valeurs `status` initiales :
- [[inbox]]
- draft
- review
- active
- archived

## Roadmap courte

1. Installer Dataview, Templater, QuickAdd, Linter.
2. Creer les templates PKA minimaux.
3. Ajouter un dashboard Dataview `wiki/INDEX-dashboard.md`.
4. Tester Linter sur 5 notes seulement.
5. Installer [[Obsidian]] [[Git]] apres verification de l'etat [[Git]] du vault.
6. Ajouter Tasks/Calendar/Periodic Notes seulement si le journal devient un espace de pilotage quotidien.

## Decision [[Dobby]]

Le bon premier lot est :

- Dataview
- Templater
- QuickAdd
- Linter
- [[Obsidian]] [[Git]]

Pas plus au depart. Le systeme PKA a deja une architecture forte ; trop de plugins introduiraient du bruit et des automatismes concurrents.
