# .arbor/ — Arbor Research Trees (PKA)

Ce dossier contient les arbres d'hypothèses persistants de la skill `arbor-research`.
Un arbre = une recherche cumulative avec historique des hypothèses testées, élaguées, mergées.

## Structure

```
.arbor/
├── README.md
└── research/
    └── <project>/
        ├── tree.json          # Arbre canonique (machine-readable)
        ├── TREE.md            # Vue Markdown humaine
        ├── events.jsonl       # Log événementiel
        └── sessions/          # Une session par run
            └── <YYYY-MM-DD_slug>/
                ├── hypothesis.md
                ├── result.md
                └── artifacts/   # Logs PPK2, datasets, etc.
```

## Projets actifs

- `wildnexus/` — Optimisation hardware et firmware du nœud caméra-piège
- `vetalyx/` — Recherche diagnostic allergie animale
- `arteon/` — Optimisation SEO et contenu

## Conventions

- Les arbres sont versionnés dans Git (connaissance cumulative)
- Les artifacts lourds (>1MB) dans `sessions/*/artifacts/` sont dans `.gitignore`
- `tree.json` est la source de vérité machine ; `TREE.md` est généré pour lecture humaine
- Ne jamais modifier `tree.json` manuellement — utiliser les opérations Dobby (merge, prune, branch)

## Références

- Skill : `skills/arbor-research/SKILL.md`
- Protocole : `skills/arbor-research/arbor-loop.md`
- Template : `skills/arbor-research/idea-tree-template.md`
- Source : https://github.com/RUC-NLPIR/Arbor
