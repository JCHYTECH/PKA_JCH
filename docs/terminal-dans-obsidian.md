# Terminal dans Obsidian — mode d'emploi (vault PKA_JCH)

> Vérifié le 2026-10-29. Objectif : terminal intégré dans Obsidian (à la VSCode) pour les commandes rapides dans le vault.
> Vault : `/Users/jchavauxm5/PKA_JCH` · macOS.

## État du vault (2026-10-29)
- Plugins communautaires : `dataview`, `templater-obsidian`, `quickadd`, `obsidian-linter`, `obsidian-git`, **`terminal`**.
- **Plugin « Terminal » (polyipseity) v3.29.0 installé et actif** → terminal intégré opérationnel. ✅

## Usage (confirmé)
- `Cmd+P` → **« Terminal: Open integrated terminal »**.
- Ouvrir à la racine du vault : **`Cmd+Shift+H`** (raccourci par défaut).
- Sortir du focus terminal (rendre les raccourcis Obsidian) : `Ctrl+Shift+` `.

## Réglages macOS conseillés
- **Répertoire de travail** : racine du vault (`/Users/jchavauxm5/PKA_JCH`).
- **PATH Homebrew** : si `git`, `pka`, `python` ne sont pas trouvés, fixer `PATH` (`/opt/homebrew/bin`, `/usr/local/bin`) via un profil `zsh -l` ou une variable d'env par profil du plugin.
- **Profils utiles** : `zsh`, `git`, `python3`, `node`.

## Mise à jour du plugin (méthode « fichier », sans UI)
Utile car l'auteur publie souvent ; permet aussi de réinstaller si besoin.
1. Récupérer les 3 assets de la dernière release :
   ```bash
   BASE="https://github.com/polyipseity/obsidian-terminal/releases/download/<TAG>"
   cd ~/PKA_JCH/.obsidian/plugins/terminal
   for f in main.js manifest.json styles.css; do curl -sL "$BASE/$f" -o "$f"; done
   ```
   `<TAG>` = dernière version (ex. 3.29.0 ; voir `https://api.github.com/repos/polyipseity/obsidian-terminal/releases/latest`).
2. S'assurer que `"terminal"` figure dans `~/PKA_JCH/.obsidian/community-plugins.json`.
3. Obsidian → `Cmd+P` → **« Reload app without saving »** (relit la config sans écraser l'ancienne).

> Méthode alternative UI : Paramètres → Community plugins → Browse → « Terminal » → Install → Enable.

## Alternatives (si souci)
- **Lean Terminal** — vrai PTY dans le workspace, onglets, chemins cliquables, restaure cwd + scrollback.
- **Smart Workflow** — terminal Rust/PTY intégré.
- **Shell commands** — non interactif : lance une commande et capture la sortie dans une note.

## Sécurité
- Le plugin exécute un **vrai shell** → vault de confiance uniquement ; release officielle de l'auteur (`polyipseity`).
- Ne pas coller de commande non relue (comme dans VSCode).

## Workflow « vault + git »
- Repo versionné + `obsidian-git`. Depuis le terminal intégré : `git status`, `git add`, `git commit`, `git push`.
- Scripts PKA : `bin/pka`, `bin/pka-gate`, etc. (vérifier le PATH si non résolus).

---

*Installé/mis à jour le 2026-10-29 via la méthode fichier (release 3.29.0). Backup config : `.obsidian/community-plugins.json.bak`.*
