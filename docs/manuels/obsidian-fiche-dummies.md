# 📝 Obsidian — Fiche Dummies

> Ton vault PKA_JCH dans Obsidian. Notes liées, [[daily]] notes, plugins.

---

## 🚀 DÉMARRAGE

| Action | Comment |
|--------|---------|
| Ouvrir le vault | Lancer Obsidian → `Open folder as vault` → sélectionner `PKA_JCH` |
| Graph (vue globale) | Icône graphe dans la barre latérale gauche |
| Rechercher | **Cmd+O** (ouvrir un fichier) ou **Cmd+Shift+F** (recherche dans tout le contenu) |
| Palette de commandes | **Cmd+P** — toutes les actions |

---

## 📂 STRUCTURE DU VAULT

```
PKA_JCH/
├── wiki/                  ← ton cerveau externe
│   ├── Daily/             ← notes quotidiennes (YYYY/MM/YYYY-MM-DD.md)
│   ├── Knowledge/         ← fiches de connaissance
│   ├── Guidelines/        ← règles et procédures
│   ├── SOPs/              ← procédures standardisées
│   ├── Workstreams/       ← suivi de projets
│   ├── log.md             ← journal des sessions PKA
│   └── index.md           ← point d'entrée
├── JCH_Inbox/             ← fichiers entrants, projets
├── TEAM/                  ← fiches des spécialistes
└── docs/                  ← documentation technique
```

---

## ✍️ CRÉER UNE NOTE

| Action | Raccourci |
|--------|-----------|
| Nouvelle note | **Cmd+N** |
| Daily note du jour | **Cmd+D** (grâce au plugin Daily Notes) |
| Lier une note existante | Taper `[[` → autocomplétion |
| Lier avec alias | `[[nom-de-fichier|texte affiché]]` |
| Ouvrir le lien | **Cmd+clic** sur un `[[wikilink]]` |

---

## 🔌 PLUGINS ACTIFS

| Plugin | Utilité |
|--------|---------|
| **Dataview** | Requêtes, listes dynamiques de notes |
| **Templater** | Templates avancés ([[daily]] note, fiches espèces) |
| **QuickAdd** | Ajout rapide de contenu, formulaires |
| **Linter** | Nettoyage automatique du markdown |
| **Obsidian Git** | Sauvegarde automatique vers Git |

---

## 🗂️ DAILY NOTES

| Action | Détail |
|--------|--------|
| Où sont-elles ? | `wiki/Daily/YYYY/MM/YYYY-MM-DD.md` |
| Template | `JCH_Inbox/90_TEMPLATES/obsidian/daily.md` |
| Ouvrir celle du jour | **Cmd+D** |
| Tag `#daily` | Toutes les [[daily]] notes sont taguées |

---

## 🧹 MAINTENANCE

| Tâche | Fréquence | Script |
|-------|-----------|--------|
| Wikilinks patchés | Nuit (launchd) | `scripts/pka_vault_maintenance.py` |
| Git auto-commit | Nuit (launchd) | via `obsidian-git` |
| Sauvegarde manuelle | Quand tu veux | `bin/pka-save` |

---

## ⚡ ASTUCES

- **Cmd+P** → tape `templater` → insère un template
- Pour voir toutes les notes qui pointent vers une note : backlinks (panneau de droite)
- Pour un tag : tape `#` dans une note
- Les `[[wikilinks]]` sont automatiquement maintenus par le patcher nocturne

---

*Fiche générée par [[Dobby]] 🦉 — 3 juin 2026*
