# Décision — statut du dépôt `firmware/` (dépôt git imbriqué)

**Projet :** WildNexus — WILDNEXUS_DEVICE
**Date :** 2026-10-29
**Rédaction :** Dobby 🦉
**Statut :** À trancher par JCH (+ [[Forge]] technique)
**Portée :** documentation/ops — **aucun changement de code firmware**.

---

## 1. Constat

- Le dossier `WILDNEXUS_DEVICE/firmware/` contient **son propre dépôt git** (`.git/` présent).
- Le dépôt parent **PKA_JCH ne versionne aucun fichier de ce dossier** : `git ls-files …/firmware` = **0**.
- Conséquence : **le code firmware n'est PAS sauvegardé par le `git push` de PKA_JCH**. Il vit dans son propre dépôt, hors du périmètre de sauvegarde/versionnement du repo principal.

## 2. Risque

- **Perte non couverte** : si le remote firmware est absent/mal configuré, le code n'existe qu'en local.
- **Divergence silencieuse** : le repo parent et le repo firmware évoluent séparément sans lien versionné.
- **Reproductibilité** : un clone de PKA_JCH ne contient pas le firmware → build impossible sans étape manuelle.

## 3. Options

| Option | Description | Avantages | Inconvénients |
|---|---|---|---|
| **A. Sous-module git** (recommandé) | Ajouter `firmware/` comme **submodule** référençant un commit précis | Lien versionné, clone reproductible, historique séparé propre | Manipulation `git submodule` (init/update) |
| B. Subtree | Intégrer l'historique firmware dans PKA_JCH (git subtree) | Un seul repo, versionné ensemble | Historique mélangé, merges plus lourds |
| C. Dépôt séparé + doc | Laisser séparé, **documenter le remote + sauvegarde dédiée** | Simple, isolation | Pas de lien versionné dans PKA_JCH ; dépend de la rigueur backup |
| D. Intégration directe | Copier le firmware dans PKA_JCH (retirer le `.git` interne) | Tout-en-un | Perte de l'isolation/CI firmware ; à éviter si CI séparée |

## 4. Recommandation

**Option A (sous-module)** + **vérifier le remote du firmware** :
1. `git -C firmware remote -v` → confirmer qu'un remote existe et est poussé.
2. Si remote OK → l'ajouter comme submodule : `git submodule add <url> firmware` (remplacer le dossier actuel par le submodule).
3. Documenter la commande `git clone --recurse-submodules` dans le README racine.
4. Ajouter le firmware à la routine de sauvegarde (`bin/pka-backup`).

Si l'option A est jugée trop lourde pour P0 : **option C minimale** — au moins documenter le remote firmware + l'inclure dans la sauvegarde, pour ne pas dépendre d'un seul disque.

## 5. État actuel (à compléter par Forge)

- [ ] Remote firmware identifié : `git -C firmware remote -v` → ___________
- [ ] Firmware poussé sur son remote : oui / non
- [ ] Option retenue : A / B / C / D
- [ ] `.gitmodules` ajouté (si A)
- [ ] Sauvegarde firmware intégrée à `bin/pka-backup`

---

*Note de décision — ne modifie pas le code. À clore après arbitrage JCH/Forge.*
