# GL-001 — Conventions de nommage

Source de vérité pour le nommage de tous les fichiers de PKA_JCH. Tout fichier qui parle de nommage renvoie ici.

---

## 1. kebab-case pour les slugs

- Tout en minuscules.
- Mots séparés par des tirets simples.
- Pas de underscores, espaces, camelCase ni majuscules.
- ASCII uniquement dans les slugs — remplacer les accents par leur équivalent ASCII.

```
✓  pka-init-argus-plugin-lr
✓  vetalyx-analyse-financiere
✗  PKA_Init, vetalyx analyse, ArTEON-Legal
```

---

## 2. Préfixe ISO date sur les fichiers datés

Les fichiers attachés à un jour calendaire commencent par `YYYY-MM-DD-`.

Modèle : `YYYY-MM-DD-<slug>.<ext>`

S'applique à :

| Type | Chemin |
|------|--------|
| Daily notes | `wiki/Daily/YYYY/MM/YYYY-MM-DD-<slug>.md` |
| Images datées | `wiki/images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>` |
| Livrables équipe | `TEAM_Inbox/YYYY-MM-DD_<specialiste>_<slug>.md` |

---

## 3. Règles de slug

- Dériver le slug du sujet principal en 2 à 5 mots.
- Omettre les mots vides ("le", "la", "de", "des") sauf s'ils changent le sens.
- Pour les personnes : `prenom-nom` ou `titre-nom` si le titre fait partie de la référence habituelle.
- Pour les organisations : inclure assez de contexte pour disambiguïser.

```
✓  jean-claude-havaux
✓  dr-martin-cardiologue  (si deux Dr Martin)
✓  vetalyx-analyse-q1
```

---

## 4. Nommage des fichiers spécialistes

Modèle : `TEAM/<nom>.md` — nom en minuscule, sans séparateur.

```
TEAM/dobby.md
TEAM/sybil.md
TEAM/argus.md
```

Les dossiers projets dans `JCH_Inbox/03_PROJECTS/` utilisent des MAJUSCULES :

```
03_PROJECTS/ARTEON/
03_PROJECTS/VETALYX/
```

---

## 5. INDEX.md toujours en majuscules

Chaque section avec son propre index utilise le nom littéral `INDEX.md`. Pas de préfixe date, pas de minuscule.

---

## 6. Numérotation SOPs / Workstreams / Guidelines

- SOPs : `SOP-NNN-<slug>.md` — NNN sur 3 chiffres (`001`, `002`…)
- Workstreams : `WS-NNN-<slug>.md`
- Guidelines : `GL-NNN-<slug>.md`

Les numéros ne sautent pas. Un numéro retiré n'est réutilisé qu'après log explicite.

---

## 7. Livrables équipe

Les fichiers produits par les spécialistes et déposés dans `TEAM_Inbox/` suivent ce modèle :

`YYYY-MM-DD_<specialiste>_<slug>.md`

```
2026-05-09_renard_vetalyx-analyse-contrat.md
2026-05-09_sybil_patterns-semaine-19.md
```

Note : underscore comme séparateur de champs (date / spécialiste / sujet), kebab-case à l'intérieur du slug.

---

## 8. Images

`wiki/images/YYYY/MM/YYYY-MM-DD-<slug>.<ext>`

Le slug décrit l'image, pas son type. `2026-05-09-bernache-canada-vol.jpg` > `2026-05-09-photo.jpg`.

Si plusieurs images de la même source le même jour : ajouter `-1`, `-2`…

---

## 9. Gestion des collisions

Si deux fichiers auraient le même nom, ajouter un qualificatif court :

```
dr-martin-cardiologue.md
dr-martin-avocat.md
```

---

## 10. Caractères interdits dans les noms de fichiers

- Pas de tiret em (—)
- Pas de slash
- Pas de deux-points, point-virgule, point d'interrogation, astérisque
- Pas d'emoji dans les noms de fichiers (autorisés dans le contenu)

---

## Mises à jour

Si les règles changent, mettre à jour ce fichier uniquement. SOPs et Workstreams pointent ici — ils héritent automatiquement.
