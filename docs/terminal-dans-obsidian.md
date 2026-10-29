# Terminal dans Obsidian — mode d'emploi (vault PKA_JCH)

> Vérifié le 2026-10-29. Objectif : utiliser un terminal intégré dans Obsidian (à la VSCode) pour les commandes rapides dans le vault.
> Vault : `/Users/jchavauxm5/PKA_JCH` · macOS.

## État actuel du vault
- Plugins communautaires **activés** : `dataview`, `templater-obsidian`, `quickadd`, `obsidian-linter`, `obsidian-git`.
- **Aucun plugin « terminal » installé.**

## Recommandé : plugin « Terminal » (polyipseity)
Le plus mature — rendu **xterm.js** (la même techno que le terminal intégré de VSCode), onglets + splits, profils, historique restauré.

### Installation (GUI Obsidian)
1. Paramètres → **Community plugins** → activer (Turn on community plugins).
2. **Browse** → chercher **« Terminal »** (auteur *polyipseity*) → **Install** → **Enable**.
3. `Cmd+P` → **« Terminal: Open integrated terminal »**. (Raccourci par défaut : **`Cmd+Shift+H`** pour ouvrir à la racine du vault.)

### Alternatives
- **Lean Terminal** — vrai PTY dans le workspace, onglets épinglables, chemins/URLs cliquables, restaure cwd + scrollback.
- **Smart Workflow** — terminal Rust/PTY intégré (orienté workflow + IA).
- **Shell commands** — pas interactif : lance une commande depuis la palette et **capture la sortie dans une note**.

## Réglages macOS conseillés (plugin Terminal)
- **Répertoire de travail** : racine du vault (`/Users/jchavauxm5/PKA_JCH`).
- **PATH Homebrew** : si `git`, `pka`, `python` ne sont pas trouvés, vérifier que le profil shell charge `/opt/homebrew/bin` (ex. profil `zsh -l`, ou définir `PATH` dans le profil du plugin).
- **Profils utiles** :
  - `zsh` (shell par défaut)
  - `git` (raccourci pour `git status/diff/log` — `obsidian-git` est déjà installé, cohérent)
  - `python3` / `node` selon besoin
- Coller la sortie dans une note : `Cmd+Shift+V` (coller) après sélection/copie du terminal, ou via **Shell commands** (insertion directe).

## Sécurité
- Le plugin « Terminal » exécute un **vrai shell** → n'activer que des plugins de confiance, et rester dans un vault personnel.
- Ne jamais coller de commande non relue dans le terminal intégré (comme dans VSCode).

## Raccourcis (résumé)
| Action | Commande / raccourci |
|---|---|
| Ouvrir terminal intégré | `Cmd+P` → *Terminal: Open integrated terminal* |
| Ouvrir à la racine du vault | `Cmd+Shift+H` (défaut) |
| Basculer focus hors du terminal | `Ctrl+Shift+` ` |
| Nouveau terminal | palette → *Terminal: Open…* (choisir profil/types) |

## Bonnes pratiques « vault + git »
- Le repo est versionné (`obsidian-git` + git). Depuis le terminal intégré : `git status`, `git add`, `git commit`, `git push`.
- Pour les scripts PKA : `bin/pka`, `bin/pka-gate`, etc. — vérifier le PATH si non résolus.

---

*Guide à ranger dans `docs/`. Ajuster après installation réelle (noms de profils/raccourcis).*
