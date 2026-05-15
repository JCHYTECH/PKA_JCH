---
title: Graphify — Workflow JCH
type: reference
created: 2026-04-24
tags: [graphify, workflow, obsidian, claude-code, jch-vault]
---

# Graphify — Workflow JCH

Document de référence pour l'utilisation de Graphify avec ton JCH VAULT, issu de la session d'installation du 2026-04-24.

## Contexte et choix d'architecture

### Ce qu'est Graphify

Skill pour Claude Code (et d'autres assistants IA) qui transforme un dossier de fichiers (code, docs, PDFs, images) en graphe de connaissances interrogeable. Produit :
- `graph.html` — graphe interactif navigable dans un navigateur
- `GRAPH_REPORT.md` — résumé plain-text des god nodes, communautés, connexions surprenantes
- `graph.json` — graphe persistant interrogeable via `graphify query`
- `cache/` — cache SHA256 pour re-runs incrémentaux

### Ce qu'il n'est pas

- **Pas un plugin Obsidian.** Il peut seulement exporter un vault Obsidian via le flag `--obsidian`.
- **Pas de sync bidirectionnelle.** L'export Obsidian est un snapshot écrasé à chaque run.
- **Pas un outil de code distant.** Il scanne des fichiers locaux uniquement.

### Package installé

- Commande CLI : `graphify`
- Package PyPI : `graphifyy` (double `y` — `graphify` simple est un autre package sans lien)
- Méthode d'installation utilisée : `uv tool install graphifyy`
- Skill registré via : `graphify install` → `~/.claude/skills/graphify/SKILL.md`

## Architecture retenue (Option B)

### Principe

Le JCH VAULT iCloud reste source de vérité. Les outputs lourds de Graphify (cache, HTML, JSON) restent **hors iCloud**. Seul l'export Obsidian (fichiers `.md` propres) revient dans le vault.

### Structure

```
~/Documents/graphify-work/
└── faune-autour/                       # Copie locale du corpus (hors iCloud)
    ├── [notes copiées du vault]
    └── graphify-out/                   # Cache, graph.html, graph.json — LOCAL UNIQUEMENT
        ├── graph.html
        ├── graph.json
        ├── GRAPH_REPORT.md
        ├── manifest.json
        ├── cost.json
        └── cache/

JCH VAULT/0-ai-it-tools/PROJET faune-autour/
├── [notes originales — SOURCE DE VÉRITÉ, ne pas toucher via graphify]
└── graphify-notes/                     # Export Obsidian généré (écrasé à chaque run)
    ├── [notes .md avec liens [[...]]
    └── ...
```

### Règles

1. Éditer les notes **uniquement** dans `PROJET faune-autour/` (pas dans `graphify-notes/`).
2. Le dossier `graphify-notes/` est un **output généré** — tout changement manuel y sera écrasé au prochain run.
3. Avant chaque run, synchroniser la copie locale avec le vault via `rsync`.
4. Attendre qu'iCloud ait fini de descendre les dernières modifs avant le `rsync` (icône nuage dans Finder).

## Procédure — Premier run propre

### Phase 1. Nettoyage de l'ancien état

```bash
# Vérifier ce qui existe (sécurité)
ls "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/"

# Supprimer uniquement graphify-out/ (pas les notes à côté)
rm -rf "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/graphify-out"

# Vérifier que les notes originales sont intactes
ls "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/"
```

### Phase 2. Créer la structure locale

```bash
mkdir -p ~/Documents/graphify-work/faune-autour
cd ~/Documents/graphify-work/faune-autour
pwd  # doit afficher /Users/jchavauxm5/Documents/graphify-work/faune-autour
```

### Phase 3. Copier le corpus du vault vers le local

```bash
rsync -av --delete \
  --exclude 'graphify-out' \
  --exclude 'graphify-notes' \
  --exclude '.DS_Store' \
  "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/" \
  ~/Documents/graphify-work/faune-autour/
```

Points clés :
- `-av` : archive + verbose
- `--delete` : supprime dans la destination ce qui n'est plus dans la source
- Le slash final après `faune-autour/` est **crucial** (copie le contenu, pas le dossier)

Vérifier :
```bash
ls ~/Documents/graphify-work/faune-autour/
```

### Phase 4. Lancer Graphify

```bash
cd ~/Documents/graphify-work/faune-autour
graphify . --obsidian --obsidian-dir "/Users/jchavauxm5/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/graphify-notes"
```

Note : on utilise `graphify` (shell zsh), pas `/graphify` (Claude Code). Les deux fonctionnent, la syntaxe diffère selon le contexte d'appel.

### Phase 5. Vérification

```bash
# graphify-out/ bien en local (hors iCloud)
ls ~/Documents/graphify-work/faune-autour/graphify-out/

# graphify-notes/ bien dans le vault, contenu .md
ls "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/graphify-notes/" | head -20

# Ouvrir le graphe interactif
open ~/Documents/graphify-work/faune-autour/graphify-out/graph.html
```

Dans Obsidian : `JCH VAULT → 0-ai-it-tools → PROJET faune-autour → graphify-notes`. Tu dois voir des notes liées par `[[...]]`. `Cmd+G` pour le graphe natif Obsidian.

## Workflow récurrent

Quand des notes ont été modifiées dans Obsidian et que tu veux régénérer :

```bash
# 1. Re-sync vault → local
rsync -av --delete \
  --exclude 'graphify-out' \
  --exclude 'graphify-notes' \
  --exclude '.DS_Store' \
  "$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/" \
  ~/Documents/graphify-work/faune-autour/

# 2. Re-run en mode incremental (--update)
cd ~/Documents/graphify-work/faune-autour
graphify . --update --obsidian --obsidian-dir "/Users/jchavauxm5/Library/Mobile Documents/iCloud~md~obsidian/Documents/JCH VAULT/0-ai-it-tools/PROJET faune-autour/graphify-notes"
```

Le `--update` ne retraite que les fichiers modifiés depuis la dernière fois (SHA256). Beaucoup plus rapide que le premier run.

## Requêter le graphe

Une fois `graph.json` généré, plusieurs commandes permettent d'interroger le graphe :

```bash
cd ~/Documents/graphify-work/faune-autour

# Question libre
graphify query "comment X se connecte à Y ?"

# Traverser un chemin précis entre deux noeuds
graphify path "NoeudA" "NoeudB"

# Explication détaillée d'un noeud
graphify explain "NomDuNoeud"

# Budget token pour la query
graphify query "..." --budget 1500
```

## Ajouter un nouveau projet

Pour un autre projet (Arteon, WILDLENS, etc.), répliquer la structure :

```bash
mkdir -p ~/Documents/graphify-work/<nom-projet>
```

Et adapter les chemins dans les commandes ci-dessus. Les conventions retenues :
- Nommage : tout en minuscules, tirets, sans espaces (`faune-autour`, pas `Faune Autour`)
- Un dossier par projet dans `~/Documents/graphify-work/`
- Un sous-dossier `graphify-notes/` dédié dans chaque dossier projet du vault

## Pièges rencontrés et règles à retenir

### Distinction `/graphify` vs `graphify`
- **Dans Claude Code (session interactive)** : `/graphify .` avec slash initial
- **Dans shell zsh** : `graphify .` sans slash
- Si on tape `/graphify` dans zsh, zsh cherche un fichier à la racine `/` et échoue avec `no such file or directory: /graphify`

### Graphify ne scanne que du local
Graphify ne sait pas lire un repo GitHub distant. Pour analyser un repo :
- Soit cloner localement : `git clone https://github.com/.../repo.git`
- Soit utiliser `graphify add <url>` pour ajouter des fichiers ponctuels (papers, tweets)

### `graphify-out/` toujours placé dans le dossier scanné
Depuis la v0.4.32, `graphify-out/` est toujours créé **à l'intérieur** du dossier passé en argument. On ne peut pas le rediriger ailleurs. C'est la raison pour laquelle on scanne depuis `~/Documents/graphify-work/` (hors iCloud) et pas directement depuis le vault.

### Sortir de Claude Code avant les commandes shell de vérification
Dans une session Claude Code, les commandes comme `head`, `ls`, `cat` sont interprétées comme des outils Claude Code, pas comme des commandes shell. Pour avoir la sortie brute, taper `/exit` (ou `Ctrl+D`) d'abord.

### Ne jamais lancer `graphify .` dans `~`
Scannerait tout le home, consommation API massive, probable échec. Toujours vérifier le `pwd` avant.

### Toujours vérifier `manifest.json` après un run
Contient la liste des fichiers effectivement scannés. Permet de confirmer que le corpus ciblé a bien été traité.

## État courant (au 2026-04-24)

- `uv` installé et opérationnel
- `graphifyy` installé via `uv tool install`, CLI `graphify` sur le PATH
- Skill Claude Code installé (`graphify install` exécuté)
- Un premier run a été fait dans `JCH VAULT/0-ai-it-tools/PROJET faune-autour/` (corpus = notes projet, pas code source)
- Workflow Option B pas encore appliqué — à faire au prochain créneau

## Références

- Doc officielle : https://graphify.net/
- Repo : https://github.com/safishamsi/graphify
- PyPI : https://pypi.org/project/graphifyy/
