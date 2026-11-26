# WildLens — Procédure de rédaction d'une édition

> Workflow canonique pour créer le brouillon du prochain numéro.
> Références : `ref/architecture-editoriale-v2.md` (format, 3 sections v3), `ref/wildlens-prompt-weekly-review.md` (veille), `scripts/wildlens_weekly.py edition` (squelette).
> Créé par Dobby 🦉 — 2026-11-22. Mis à jour 2026-11-24 (3 sections, décision panel lecteurs).

## 1. Thème de la semaine

- Mettre à jour `wildlens/theme-semaine.md` — une ligne = le thème de la prochaine édition.
- Ton selon la rotation hebdomadaire A/B/C : **Militant · Investigatif · Lyrique** (le militant est toujours porté par ① Le Cadre).

## 2. Matière (veille)

- Produire ou relire le brief hebdo via `ref/wildlens-prompt-weekly-review.md`
  (4-6 développements sélectionnés et scorés) → alimente **③ L'actualité technique**.
- Sortie : `research/YYYY-MM-DD_weekly-photography-insights.md`.

## 3. Squelette

- `python3 scripts/wildlens_weekly.py edition`
  → génère `editions/fr/wildlens-edition-{N}-template.md` (frontmatter + 3 sections).

## 4. Rédaction — 3 sections

| # | Section | Longueur | Rôle |
|---|---------|----------|------|
| ① | **Le Cadre** (The Frame) | 400-600 | Photo de JC + analyse, ton militant — l'image porte le propos |
| ② | **Le Constat** (The Record) | 100-200 | Dérive de destruction du vivant, factuelle + sourcée — systématique, angle pro-nature / anti-spécisme |
| ③ | **L'actualité technique** | 300-500 | Développement technique de la semaine — fusion de l'ancien Le Virage + L'Objectif |

**Total visé :** 900-1300 mots.

**Template Markdown (source) :** titre → thème → sections (ligne de crédit + « Sources : » en fin) → **mots-clés (en fin)** → Notes de publication → pied de page.
⚠️ **Ghost-level (hors Markdown) :** la **photo en tête** (feature image, au-dessus du titre) et le **sommaire cliquable** (TOC générée par le thème depuis les titres `##`). **Double-check obligatoire :** après publication, comparer le rendu Ghost au Markdown source — ne pas confondre les deux.

## 5. Photo + crédit

- Choisir la photo du Cadre (matière JC) + crédit exact :
  `*Espèce (nom latin) · boîtier · objectif · © JC Havaux / ARTEON*`

## 6. Mots-clés

- En fin d'édition, après la section ③ : `**Mots-clés :** …` (5-10 termes).

## 7. Vérification du Constat

- Fait vérifié + source + date. Ton sobre, sans polémique.

## 8. Checklist « Notes de publication »

- [ ] JC relire et valider
- [ ] Mots-clés en fin
- [ ] Crédits photo exacts
- [ ] `status:` du frontmatter : `draft` → `scheduled` (date programmée) → `published`

## 9. Dépôt

- FR (canonique, pivot 19/11) : `editions/fr/wildlens-edition-{N}-{slug}.md`
- EN : `editions/final/wildlens-edition-{N}-{slug}.md` (si traduction demandée)
- Les dates de publication/programmation vivent dans `thread-arteon.md` et `INDEX.md`,
  **pas** dans le frontmatter `date:` (qui garde la date de rédaction d'origine).

## Notes

- Ne pas déduire le statut du nom de fichier — lire `status:` du frontmatter.
- Publication Ghost : `wildlens.arteon.be`.
