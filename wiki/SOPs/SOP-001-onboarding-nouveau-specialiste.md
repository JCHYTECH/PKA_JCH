# SOP-001 — Onboarding d'un nouveau spécialiste

- **Owner :** Bouvier 🐕
- **Co-owner recherche :** Furet 🦡
- **Déclenché par :** demande JCH ou Dobby détectant un gap de compétence
- **Références :** GL-001-conventions-nommage, TEAM/ROSTER.md, team.db

---

## Objectif

Ajouter un spécialiste à l'équipe de manière cohérente : identité forte, frontières claires, DB à jour avant tout fichier markdown. Furet fournit la recherche avant que Bouvier ne rédige le profil — c'est ce qui évite les spécialistes génériques.

---

## Étapes

### 1. Capturer le besoin (Dobby → Bouvier)

Dobby mandate Bouvier avec une phrase : ce que le nouveau spécialiste fera qu'aucun membre actuel ne peut faire. Si cette phrase est impossible à finir, le rôle n'est pas prêt.

### 2. Briefer Furet pour la recherche (Bouvier → Furet)

Bouvier écrit un brief de recherche à Furet. Questions obligatoires :

- Que fait concrètement le meilleur-du-monde dans ce rôle, au quotidien ?
- Quelles sont les compétences clés, et les anti-patterns (ce que les versions médiocres font) ?
- Quels livrables produit ce rôle ? À quoi ressemble un output excellent vs acceptable ?
- Quelles frontières ce rôle doit-il tenir ? Quelles demandes refuser ou renvoyer ?
- Candidats de nom : court, distinct, un mot, pas de collision avec l'équipe existante.
- Animal : cohérent avec la personnalité du rôle.

Furet livre un brief de 400 à 800 mots dans `TEAM_Inbox/YYYY-MM-DD_furet_research-<role-slug>.md`.

### 3. Choisir nom, animal et rôle (Bouvier)

À partir du brief Furet :

- **Nom :** un mot, court, distinct. Pas de collision avec les 24 membres existants.
- **Animal :** cohérent avec la persona — choisi avec soin, il structure l'identité.
- **Rôle :** une courte phrase. Ex : "Legal Counsel — Contracts & Advisory".

### 4. Écrire dans team.db en premier (Bouvier → Castor si besoin)

Avant tout fichier markdown, Bouvier insère le nouveau membre dans `team.db` :

```sql
INSERT INTO members (name, animal, role, status, tables_owned, hired_on, hired_by)
VALUES ('Nom', '🦌 Animal', 'Rôle', 'active', 'inbox', '2026-MM-DD', 'Bouvier');
```

Castor valide le schéma si une nouvelle table est nécessaire.

### 5. Créer TEAM/<nom>.md (Bouvier)

Créer `TEAM/<nom>.md` avec ce frontmatter et ces sections :

```markdown
---
id: <N>
name: <Nom>
animal: <emoji> <Nom animal>
role: <Rôle>
status: active
tables_owned: <tables>
hired_on: YYYY-MM-DD
hired_by: Bouvier
---

# <Nom> — <Rôle>

**Animal face:** <emoji> <Nom> — [une ligne sur ce que l'animal dit du rôle]

## Persona

[3-5 paragraphes. Identité concrète, pas générique. Tiré du brief Furet.]

## Responsabilités

[Liste claire. Ce que ce spécialiste fait, et pour qui.]

## Frontières

[Ce que ce spécialiste ne fait PAS. Où il renvoie et à qui.]

## Tables DB

[Tables qu'il possède en lecture/écriture.]
```

### 6. Mettre à jour TEAM/ROSTER.md (Bouvier)

Ajouter la ligne dans le tableau, incrémenter le numéro de version, mettre à jour la date.

### 7. Mettre à jour CLAUDE.md (Dobby)

Ajouter le membre dans le tableau Team Roster de `CLAUDE.md`.

### 8. Mettre à jour les Workstreams concernés (Bouvier)

Si le nouveau spécialiste intervient dans une orchestration récurrente, l'ajouter dans le Workstream correspondant dans `wiki/Workstreams/`.

### 9. Confirmer avec JCH (Bouvier → Dobby → JCH)

Dobby présente : résumé du brief Furet + profil du nouveau membre. Modifications uniquement après validation JCH.

### 10. Logger le recrutement (Dobby)

Dobby note le recrutement dans la daily note du jour : nom, rôle, brief Furet, fichier TEAM/.

---

## Erreurs fréquentes à éviter

- Sauter l'étape Furet — même pour un rôle "évident", la recherche révèle les anti-patterns.
- Créer le fichier markdown avant d'écrire dans `team.db` — la DB est la source de vérité.
- Coller le brief Furet dans TEAM/nom.md — le brief reste dans `TEAM_Inbox/`, le profil est le contrat.
- Oublier de mettre à jour ROSTER.md et CLAUDE.md — les deux doivent rester en sync avec team.db.
- Numéro d'ID non vérifié — toujours faire `SELECT MAX(id) FROM members;` avant d'insérer.
