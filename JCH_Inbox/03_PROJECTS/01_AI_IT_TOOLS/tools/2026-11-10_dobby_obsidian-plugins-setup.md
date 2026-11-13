# Setup plugins Obsidian — 2026-11-10

> Trace Dobby 🦉 — reprise de session Obsidian interrompue + recommandations plugins pour PKA.

## État final des plugins communautaires actifs

`dataview`, `templater-obsidian`, `quickadd`, `obsidian-linter`, `obsidian-git`, `terminal`, `column-explorer`, `omnisearch`

## Modifications de la session

1. **Column Explorer** (`column-explorer`) — activé. Ajout de `JCH_Inbox` aux favoris (`data.json` → `"favorites": ["JCH_Inbox"]`).
   - ⚠️ Le plugin n'a pas de « dossier racine » natif : il part toujours de la racine du vault, avec favoris/épingles en accès rapide. Le dernier dossier ouvert est mémorisé entre les sessions.
2. **Iconize** (`obsidian-icon-folder`, id interne) — **supprimé** (dossier + entrée de liste).
   - Motif : projet déprécié (README « Project Deprecation and End of Maintenance », dernière release 2025-01-03).
   - NB piège : `obsidian-icon-folder` est l'**id interne** d'Iconize (Florian Woelki), pas un plugin distinct.
3. **Linter** (`obsidian-linter`) — configuré en jeu minimal (`data.json`) :
   - `yaml-timestamp` : activé, clés `dateCreated`/`dateModified` (convention template daily), format `YYYY-MM-DD`, source de vérité = filesystem.
   - `trailing-spaces` : activé.
   - `heading-blank-lines` : activé.
   - `lintOnSave` : **laissé OFF** — application à la demande (Cmd+P → « Lint the current file » / clic droit dossier → « Lint folder »).
4. **Omnisearch** (`omnisearch`) — installé v1.32.0 (release 2026-10-24, maintenu). Fichiers dans `.obsidian/plugins/omnisearch/`.
5. **Web Clipper** — extension navigateur (pas un plugin vault). Dossier destination `JCH_Inbox/00_INBOX/web-clips/` créé. Template recommandé :
   - Note name : `{{title}}`
   - Note location : `JCH_Inbox/00_INBOX/web-clips`
   - Properties : `source: {{url}}`, `author: {{author}}`, `published: {{published}}`, `tags: web-clip`
   - Note content : `# {{title}}` puis `{{content}}`

## Fichiers touchés

- `.obsidian/community-plugins.json`
- `.obsidian/plugins/column-explorer/data.json`
- `.obsidian/plugins/obsidian-linter/data.json`
- `.obsidian/plugins/omnisearch/` (nouveau)
- `.obsidian/plugins/obsidian-icon-folder/` (supprimé)
- `JCH_Inbox/00_INBOX/web-clips/` (nouveau)

## Recommandations écartées (anti usine à gaz)

- **Kanban / Projects** → Plane déjà en place.
- **Meta Bind / CustomJS / DB Folder** → outils puissants, inutiles ici.
- **Tasks / Excalidraw** → optionnels, non retenus pour l'instant (second tracker / Canvas suffit).
