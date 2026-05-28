---
name: obsidian-knowledge-graph
description: Piloter l'inventaire, le dictionnaire, les dry-runs et l'application controlee des wikilinks [[Obsidian]] pour le vault PKA_JCH. Declencher sur "wikilink le vault", "dry-run [[Obsidian]]", "mets a jour le knowledge graph", "genere le dictionnaire [[Obsidian]]", "applique les wikilinks valides".
---

# Skill - obsidian-knowledge-graph

## Declencheurs

- "wikilink le vault"
- "dry-run [[Obsidian]]"
- "mets a jour le knowledge graph"
- "genere le dictionnaire [[Obsidian]]"
- "applique les wikilinks valides"
- "teste 5 fichiers"

## Sources

- Script canonique : `/Users/jchavauxm5/PKA_JCH/scripts/obsidian_knowledge_inventory.py`
- Projet : `/Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/`
- Regles de validation : `references/validation_rules.md`

## Principe

Le skill orchestre le graphe [[Obsidian]], mais ne remplace pas le script.

Par defaut :

- generer les index et rapports ;
- proposer les wikilinks en dry-run ;
- ne jamais modifier les notes source sans validation explicite de JCH ;
- garder les termes ambigus hors automatisation.

## Procedure

### 1. Verifier l'etat [[Git]]

```bash
cd /Users/jchavauxm5/PKA_JCH
git status --short
```

Si le worktree contient des changements non lies, les ignorer sauf s'ils touchent le script, les tests ou le projet [[Obsidian]].

### 2. Regenerer l'inventaire

```bash
python3 scripts/obsidian_knowledge_inventory.py
```

Verifier que la sortie donne :

```text
notes=<N> projects=<N> agents=<N> technologies=<N>
```

### 3. Lire les sorties critiques

Verifier au minimum :

- `knowledge_dictionary.md`
- `review_queue.md`
- `wikilink_dry_run_5.md` si un dry-run a ete demande

### 4. Dry-run wikilinks

Pour un test, utiliser le rapport genere par le script :

```text
JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/obsidian-knowledge-graph/wikilink_dry_run_5.md
```

Valider dans le rapport :

- aucun terme ambigu lie automatiquement ;
- aucun remplacement dans des backticks ;
- aucun lien double autour de `[[liens]]` existants ;
- le nombre de fichiers reste limite au lot demande.

### 5. Application reelle

Ne pas appliquer de wikilinks reels sauf si JCH dit explicitement :

- "applique"
- "valide ces 5 fichiers"
- "go modification reelle"

Avant toute application :

1. relire `references/validation_rules.md` ;
2. limiter le lot ;
3. produire ou montrer le diff attendu ;
4. appliquer ;
5. lancer les tests ;
6. commit si le worktree est propre et coherent.

### 6. Verification

Apres modification du script ou des rapports :

```bash
python3 -m pytest tests/test_obsidian_knowledge_inventory.py
```

Pour une passe plus large :

```bash
python3 -m pytest tests/test_obsidian_knowledge_inventory.py tests/test_pka_save.py tests/test_pka_save_shortcut.py
```

## Rapport a JCH

Format court :

```text
Obsidian KG - <action> terminee.
Rapport : <chemin>
Fichiers proposes : <N>
Lignes proposees : <N>
Tests : <resultat>
Git : <clean/commit>
```
