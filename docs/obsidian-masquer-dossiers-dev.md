# Obsidian — alléger le panneau Files (masquer les dossiers techniques)

> Vault PKA_JCH = tout le repo (notes + code). Le panneau Files affiche donc aussi `bin/`, `scripts/`, `tmp/`, `graphify-out/` et des fichiers de dev. Ce réglage les **masque visuellement** sans rien déplacer.

## Ce qui est masqué
- **Dossiers** : `bin/`, `scripts/`, `tmp/`, `graphify-out/`.
- **Fichiers racine** : `requirements.txt`, `skills-lock.json`, `jchavauxm5.code-workspace`, `session_*.json`, `*.md.bak`.
- **Pointeurs / bootstrap outils** : `AGENTS.md`, `DEEPSEEK.md`, `ADAPTER-PROMPT.md` (usage = terminal + DeepSeek uniquement ; ce ne sont pas des notes).

Tout le reste reste visible : `JCH_Inbox/`, `TEAM/`, `TEAM_Inbox/`, `docs/`, `wiki/`, `PHOTO/`, `JCH_PRIVATE/` + notes racine (`MEMORY`, `SOUL`, `USER`…).

## Comment c'est implémenté
1. **Snippet CSS** : `.obsidian/snippets/hide-dev-folders.css` (règles `display:none` via `:has()` sur `data-path`).
2. **Activé** dans `.obsidian/appearance.json` → `"enabledCssSnippets": ["hide-dev-folders"]`.
3. **Exclusions recherche/graphe** dans `.obsidian/app.json` → `"userIgnoreFilters": ["bin/","scripts/","tmp/","graphify-out/","requirements.txt","skills-lock.json","session_*.json"]`.

## Activer / rafraîchir
- Obsidian → `Cmd+P` → **« Reload app without saving »** (relit la config depuis le disque sans l'écraser).
- Ou Settings → **Appearance → CSS snippets** → vérifier que `hide-dev-folders` est **intégrée** (toggle).

## Revenir en arrière
- **Masquage visuel** : Settings → Appearance → CSS snippets → désactiver `hide-dev-folders` (ou supprimer le fichier CSS).
- **Exclusions** : Settings → Files & Links → « Excluded files » → retirer les entrées.
- Aucun fichier n'est déplacé : purement cosmétique.

## Modifier la liste
Éditer `.obsidian/snippets/hide-dev-folders.css` (ajouter/retirer des `data-path`) puis Recharger. Pour masquer aussi `JCH_PRIVATE/` par ex. :
```css
.nav-folder:has(> .nav-folder-title[data-path="JCH_PRIVATE"]) { display: none !important; }
```

## Notes
- `:has()` nécessite un Chromium récent (OK sur Obsidian 1.12).
- Si une future version d'Obsidian change les classes, ajuster les sélecteurs (`.nav-folder` / `.nav-folder-title` / `data-path`).
