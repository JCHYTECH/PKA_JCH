# 🔧 Git PKA — Fiche Dummies

> Les commandes Git que tu utilises vraiment pour ton vault PKA_JCH.

---

## 🚀 SAUVEGARDE RAPIDE

```bash
# La commande magique — sauvegarde tout et t'accompagne
pka-save
```

`pka-save` fait :
- Ajoute tous les fichiers modifiés (`git add -A`)
- Te demande un message de commit
- Te demande si tu veux ajouter une section à ta daily note
- Commit + log dans `wiki/log.md`

---

## 📋 COMMANDES ESSENTIELLES

| Commande | Ce que ça fait |
|----------|----------------|
| `pka-save` | Sauvegarde interactive complète |
| `git status` | Voir ce qui a changé |
| `git diff` | Voir le détail des changements |
| `git log --oneline -10` | Voir les 10 derniers commits |
| `git pull` | Récupérer les changements distants |
| `git push` | Envoyer tes commits |

---

## 🌿 BRANCHES

| Commande | Effet |
|----------|-------|
| `git branch` | Voir les branches locales |
| `git checkout -b nom-branche` | Créer et switcher sur une nouvelle branche |
| `git checkout main` | Revenir sur main |
| `git merge nom-branche` | Fusionner une branche dans la branche courante |

---

## ⏪ REVENIR EN ARRIÈRE

| Situation | Commande |
|-----------|----------|
| Annuler modifs d'un fichier (non commité) | `git checkout -- nom-fichier` |
| Annuler `git add` sur un fichier | `git reset HEAD nom-fichier` |
| Annuler le dernier commit (garder les modifs) | `git reset --soft HEAD~1` |
| Annuler le dernier commit (TOUT perdre) | `git reset --hard HEAD~1` |

---

## 🔄 SYNCHRONISATION

```bash
# Récupérer les changements du remote
git pull

# Envoyer tes commits
git push
```

---

## 🤖 AUTOMATIQUE (NE PAS TOUCHER)

| Tâche | Quand |
|-------|-------|
| `obsidian-git` | Plugin Obsidian → commit/push automatique |
| `pka_vault_maintenance.py` | Nuit (launchd) → wikilinks + git commit nocturne |

---

## ⚡ ASTUCES

- **`pka-save`** est ton meilleur ami — utilise-le en fin de session
- `git stash` — met de côté des modifs temporaires (`git stash pop` pour les récupérer)
- `git log --graph --oneline` — voir l'arbre des commits
- Les backups sont dans `TEAM/backups/`

---

*Fiche générée par Dobby 🦉 — 3 juin 2026*
