# Note — Améliorations skills en cache outil

> 2026-06-12 — Dobby  
> Les skills suivants sont chargés depuis le cache outil (Codex CLI / DeepSeek TUI) et ne peuvent pas être modifiés directement.  
> Ces améliorations sont à appliquer si les skills sont un jour resynchronisés ou réinstallés.

---

## ingest

- **Routing table obsolète** : `DIM3/docs/` n'existe plus. Ajouter `11_IOT`, `10_FUTURE_INVEST`, `05_PHOTO_AI_JURY`
- **Chemin VETALYX** : utilise `VETALYX/legal/` → devrait utiliser `08_VETALYX/`
- **linked_member PHOTO_NATURE** : `Lynx` → pourrait aussi être `Argus` ou `Nova`
- **Cross-ref** : ajouter "Pour extraire de la connaissance d'un fichier, voir `capture`"

## capture

- **Cross-ref** : ajouter "Pour router des fichiers complets, voir `ingest`"
- Les deux skills (`capture` et `ingest`) sont complémentaires mais aucun ne mentionne l'autre

## brief

- **Ajouter champ `priority`** (high/medium/low) dans le template de brief
- **Ajouter champ `deadline`** dans le template
- Ces champs existent dans la pratique informelle mais pas dans le skill

## status

- **Ajouter détection automatique** des tâches `pending` depuis > 7 jours avec indicateur ⚠️
- Cette détection est documentée dans la section "Règles" mais pas implémentée dans la procédure

## graphify

- **Cross-ref** : ajouter "Pour les wikilinks Obsidian, voir `obsidian-knowledge-graph`"
- **Skill obèse** (57 KB) — envisager de splitter en `graphify` (quick ref) + `graphify-full` (référence)

## delegate

- **Modèle-agnostique** : actuellement documenté pour DeepSeek TUI (`agent_open`, `agent_eval`). Ajouter note pour Claude Code (`task` tool) et autres modèles.
