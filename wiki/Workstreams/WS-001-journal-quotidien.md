# WS-001 — Journal quotidien

- **Owners :** [[Sybil]] 🦔 (capture et écriture), [[Dobby]] 🦉 (routing et validation)
- **Références :** GL-001-conventions-nommage, SOP-001-onboarding-nouveau-specialiste
- **Déclencheur :** tout input JCH contenant une pensée, observation, rencontre, image ou note vocale destinée au journal.

---

## Objectif

Transformer les inputs quotidiens bruts en entrées PKM structurées. Le journal est l'inbox du vault. Les personnes, organisations et sujets mentionnés sont cross-linkés vers les tables correspondantes de `team.db` et vers les fichiers wiki pertinents.

---

## Inputs acceptés

| Type | Description |
|------|-------------|
| Texte | JCH saisit ou colle une pensée, note, décision |
| Image | Photo, screenshot, carte de visite |
| Audio | Note vocale (transcription par le modèle si possible, sinon flaggée) |

---

## Choreography

### Étape 1 — [[Dobby]] reçoit et route

[[Dobby]] identifie que l'input est destiné au journal et mandate [[Sybil]].

### Étape 2 — [[Sybil]] écrit l'entrée

- **Chemin :** `wiki/Daily/YYYY/MM/YYYY-MM-DD-<slug>.md`
- **Auto-création :** si 
- **Slug :** thème principal du jour, 2 à 5 mots, kebab-case ASCII. Voir GL-001.
- **Format :** markdown simple. Une entrée par jour. Si le jour a déjà une entrée, [[Sybil]] ajoute une nouvelle section — elle ne crée pas un second fichier.
- **Structure minimale :**

```markdown
---
date: YYYY-MM-DD
slug: <slug>
tags: [daily]
---

# YYYY-MM-DD — <Titre lisible>

## [Section thématique]

[Contenu]
```

### Étape 3 — [[Sybil]] gère les images

- **Chemin :** `wiki/images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>`
- **Auto-création :** même règle que le journal.
- **Embed dans l'entrée :** `![[images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>]]`
- L'image vit dans `wiki/images/`. L'entrée journal la référence. Jamais dupliquée.

### Étape 4 — [[Sybil]] cross-link vers team.db et wiki

Pour chaque entité mentionnée dans l'input, [[Sybil]] route selon ce tableau :

| Type de mention | Destination principale | Fichier wiki si pertinent |
|----------------|----------------------|--------------------------|
| Personne | `team.db → contacts` | `wiki/CRM/people/prenom-nom.md` (stub si absent) |
| Organisation / entreprise | `team.db → contacts` (category: company) | `wiki/CRM/orgs/org-slug.md` (stub si absent) |
| Sujet récurrent / domaine d'attention | `team.db → knowledge` | `wiki/Knowledge/[domaine]/topic-slug.md` |
| Habitude / rythme | `team.db → goals` (horizon: daily) | mention inline suffisante |
| Projet concret avec deadline | `JCH_Inbox/03_PROJECTS/[PROJET]/` | lien vers dossier existant |
| Objectif / aspiration | `team.db → goals` | mention inline avec lien DB |
| Document réel (contrat, passeport, certificat) | `JCH_Inbox/06_ADMIN/` ou `05_CONTEXT_JCH/` | mention inline avec chemin |

**Règle stub vs mention inline :**

Créer un stub quand l'entité a l'un de ces attributs :
- Un nom que JCH utilisera probablement à nouveau.
- Une propriété à retrouver plus tard (date d'expiration, deadline projet, horizon objectif).
- Une pertinence transversale (personne qui apparaît dans plusieurs contextes).

Mention inline uniquement si la référence est ponctuelle et ne reviendra pas.

En cas de doute : créer le stub. Un stub ne coûte rien. Une référence manquante détériore la connectivité du vault.

### Étape 5 — [[Sybil]] écrit dans team.db (journal table)

En parallèle du fichier markdown, [[Sybil]] insère ou complète l'entrée du jour dans 

| Champ | Contenu |
|-------|---------|
| `date` | YYYY-MM-DD |
| `title` | Titre lisible de l'entrée |
| `body` | Corps principal |
| `mood` | 1–10 (si JCH le donne) |
| `energy` | 1–10 (si JCH le donne) |
| `gratitude` | 1–3 éléments (si JCH le donne) |
| `intentions` | Intention du lendemain (si JCH le donne) |
| `highlight` | Moment clé du jour |
| `reflections` | Réflexion libre (jamais forcée) |
| `weather` | Météo (optionnel) |

Le fichier markdown et la table `journal` sont complémentaires — l'un est narratif, l'autre est structuré et requêtable.

### Étape 6 — Passe Librarian de [[Dobby]] (fin de session)

À la clôture de session, [[Dobby]] vérifie :

- Les liens vers `contacts`, `knowledge`, `goals` dans team.db sont cohérents.
- Les images sont dans `wiki/images/`, pas dupliquées dans `wiki/Daily/`.
- Chaque nouveau stub est minimal et bien placé.
- Aucun fait biographique ou contextuel n'est recopié depuis une fiche contacts existante — on lie, on ne redondance pas.

---

## Ce que ce Workstream ne fait pas

- Ne produit pas de rapports de recherche — c'est [[Furet]].
- Ne modifie pas les fiches contacts existantes — [[Sybil]] ajoute, [[Delphi]] édite.
- Ne traite pas les mails entrants — c'est le pipeline [[Pie]] → digest.
- Ne remplace pas la session guidée [[Sybil]] (introspection humeur/énergie) — ce WS couvre les inputs factuels. La session guidée est un mode distinct.

---

## Nommage

Toutes les questions de nommage renvoient à GL-001-conventions-nommage. Ne pas dupliquer les règles ici.
