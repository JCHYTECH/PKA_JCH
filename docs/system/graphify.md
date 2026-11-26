# Graphify — Knowledge Graph Extractor

> **Statut :** onboardé — 2026-06-03
> **Propriétaire :** [[Corbeau]] 🐦‍⬛ (#5, Knowledge Curator)
> **Version :** v0.4.29
> **Runtime :** Claude Code CLI uniquement (incompatible DeepSeek TUI / ChatGPT)

---

## Description

Graphify transforme n'importe quel corpus (code, docs, papiers, images, notes) en [[knowledge]] graph navigable avec :
- **Clustering par communautés** — détection de patterns entre concepts dans différents fichiers
- **Triple sortie** — HTML interactif, JSON GraphRAG-ready, GRAPH_REPORT.md
- **Audit trail honnête** — chaque edge taggé EXTRACTED / INFERRED / AMBIGUOUS

## Usage PKA

```
/graphify <path>                        # pipeline complet
/graphify <path> --mode deep            # extraction approfondie
/graphify <path> --update               # incrémental (fichiers nouveaux/modifiés)
/graphify query "<question>"            # BFS traversal
/graphify query "<question>" --dfs      # DFS — trace un chemin spécifique
/graphify path "ConceptA" "ConceptB"    # plus court chemin entre concepts
/graphify explain "ConceptName"         # explication en langage clair d'un nœud
```

## Utilisation existante dans PKA

- **WildNexus / Faune Autour** — 52 fiches dans `03_WILDNEXUS/08_TECH_NOTES/tech/graphify-notes/`
  - 7 communautés : GBIF Data Sources & APIs, Species Search & Geolocation Logic, Map & Detail Display, PWA App & Deployment, Brand & Visual Identity, Biodiversity Platforms, Distance Calculation
  - Extraction depuis le code source single-file `faune-autour_13.html`

## Pipeline PKA

1. [[Dobby]] ou un spécialiste identifie un corpus à graphifier
2. [[Corbeau]] exécute `/graphify` via Claude Code
3. Les outputs (markdown + JSON + HTML) sont déposés dans le dossier projet
4. [[Corbeau]] valide la cohérence éditoriale et connecte aux [[knowledge]] items existants dans `team.db`

## Contrainte technique

Graphify nécessite **Claude Code CLI** — il ne fonctionne pas sous DeepSeek TUI ni ChatGPT. Cette contrainte est documentée dans le profil de [[Corbeau]] (`TEAM/corbeau.md`).
