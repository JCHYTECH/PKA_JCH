---
date: 2026-05-17
type: rapport-hebdo
author: [[Dobby]]
tags: [rapport, jch, collaboration, meta]
---

# Rapport [[Dobby]] — Semaine du 12 au 17 mai 2026
### Comment mieux collaborer avec ton équipe PKA

---

## Ce que tu fais bien

**Tu corriges vite et sans ego.** Quand tu as vu que `todo-jch.html` était mal placé, tu l'as dit immédiatement, sans tourner autour du pot. C'est exactement ce type de feedback court qui me permet d'agir sans friction.

**Tu sais stopper une session.** Le `[Request interrupted]` n'est pas un problème — c'est une preuve que tu surveilles ce que je fais plutôt que de me laisser partir dans la mauvaise direction. Garde ce réflexe.

**Tu acceptes l'ambiguïté technique sans panique.** Quand j'ai signalé que `team.db` était vide et `file_index` inexistante, ta réponse `"on attends"` était la bonne décision. Tu n'as pas demandé une solution immédiate par réflexe. C'est sain.

---

## Patterns qui ralentissent nos sessions

### 1. Les demandes floues au départ coûtent des cycles entiers

> *"prends les fichiers dans inbox et deplace les dans les directory qui te semble adequat"*

"Qui te semble adéquat" me transfère une décision qui t'appartient. Je n'ai pas de vue sur tes priorités, tes conventions non écrites, ou ce que tu considères "logique". Résultat : je devine, je déplace, et tu corriges après. Ce n'est pas de la collaboration — c'est de la relecture déguisée.

**Ce que ça coûte :** 2 à 4 échanges supplémentaires par session pour rattraper les décisions que tu aurais pu cadrer en 30 secondes.

---

### 2. Tu questionnes les fichiers un par un, sans objectif déclaré

La séquence `dashboard.sh` → `dobby.sh` → `team.db` ressemble à une exploration improvisée. C'est légitime, mais sans contexte ("je fais un audit de la racine PKA" ou "je veux nettoyer avant de coder"), je réponds à chaque question isolément au lieu de t'offrir une vue d'ensemble cohérente.

**Ce que ça coûte :** des réponses fragmentées plutôt qu'un diagnostic structuré que tu pourrais réutiliser.

---

### 3. Les règles de routage ne sont nulle part

L'ingest a fonctionné, mais sur la base de mon interprétation. Si une autre session ou un autre agent fait le même exercice la semaine prochaine, le résultat sera différent. Tu n'as pas de règles écrites, donc chaque ingest repart de zéro — ou pire, diverge silencieusement.

**Ce que ça coûte :** de la dérive progressive dans la structure PKA, sans que tu t'en rendes compte avant que ce soit difficile à corriger.

---

## Habitudes concrètes à adopter

**Habitude 1 — La phrase de contexte en ouverture**
Avant toute commande ou demande, une phrase sur *pourquoi* tu fais ça :
> *"Je fais un audit rapide de la racine PKA avant de coder ce soir."*
> *"Je veux ingérer cette semaine sans créer de dette structurelle."*

Ça prend 10 secondes. Ça change la qualité de toute la session.

---

**Habitude 2 — Formuler tes demandes avec une contrainte**
Remplace les demandes ouvertes par des demandes contraintes :

| ❌ Flou | ✅ Contraint |
|---|---|
| "déplace où tu veux" | "déplace selon la structure existante, signale si tu hésites" |
| "c'est quoi ce fichier" | "dis-moi si ce fichier est utile, redondant, ou à archiver" |
| "on attends" | "on attends — crée un TODO dans team.db quand il sera prêt" |

---

**Habitude 3 — Créer un fichier `routing_rules.md` dans PKA**
Un fichier simple, 20 lignes, qui dit : *"Les `.html` de dashboard vont dans `/Dashboards/`. Les notes de réunion vont dans `/Notes/YYYY/`. Les scripts utilitaires vont dans `/scripts/`."*
Tu le tiens à jour. Je m'y réfère. L'ingest devient prédictible et auditable.

---

**Habitude 4 — Terminer les sessions avec une décision explicite**
`"on attends"` est une décision — mais elle n'est tracée nulle part. Prends l'habitude de terminer chaque session avec une ligne de clôture :
> *"/close — team.db en attente de schéma, rien d'urgent"*

Ça prend 5 secondes et ça évite de retrouver un contexte flou la prochaine fois.

---

## Défi de la semaine

> **Avant ta prochaine session d'ingest ou de déplacement de fichiers :**
> Écris `routing_rules.md` — même incomplet, même 10 lignes.
>
> Pas pour moi. Pour que *tu* puisses relire dans 3 semaines et comprendre pourquoi un fichier est là où il est.
>
> Si tu veux, on le construit ensemble en début de session. Mais c'est toi qui valides chaque règle. C'est ton PKA, pas le mien.

---

*Rapport généré par [[Dobby]] — Agent PKA de JCH*
*Semaine 2026-05-12 → 2026-05-17 · Basé sur 17 échanges analysés*