# WildLens — Procédure de rédaction d'une édition

> Workflow canonique pour créer le brouillon du prochain numéro.
> Références : `ref/architecture-editoriale-v2.md` (format), `ref/wildlens-prompt-weekly-review.md` (veille), `scripts/wildlens_weekly.py edition` (squelette).
> Créé par Dobby 🦉 — 2026-11-22.

## 1. Thème de la semaine

- Mettre à jour `wildlens/theme-semaine.md` — une ligne = le thème de la prochaine édition.
- Ton selon la rotation hebdomadaire A/B/C : **Militant · Investigatif · Lyrique** (le militant est toujours porté par ① Le Cadre).

## 2. Matière (veille)

- Produire ou relire le brief hebdo via `ref/wildlens-prompt-weekly-review.md`
  (4-6 développements sélectionnés et scorés) → alimente **② Le Virage**.
- Sortie : `research/YYYY-MM-DD_weekly-photography-insights.md`.

## 3. Squelette

- `python3 scripts/wildlens_weekly.py edition`
  → génère `editions/final/wildlens-edition-{N}-template.md` (frontmatter + 4 sections).

## 4. Rédaction — 4 sections

| # | Section | Longueur | Rôle |
|---|---------|----------|------|
| ① | **Le Cadre** (The Frame) | 400-600 | Photo de JC + analyse, ton militant — l'image porte le propos |
| ② | **Le Virage** (The Shift) | 200-300 | Innovation technologique de la semaine (nouvelle techno / IA / outil) |
| ③ | **L'Objectif** (The Lens) | 300-400 | Sujet technique : la photographie comme instrument de connaissance — outils, méthodes, perspectives |
| ④ | **Le Constat** (The Record) | 100-150 | Dérive de destruction du vivant, factuelle + sourcée — systématique, angle pro-nature / anti-spécisme |

**Total visé :** 900-1300 mots.

**Template Markdown (source) :** titre → thème → **mots-clés** → sections (ligne de crédit + « Sources : » en fin) → Notes de publication → pied de page.
⚠️ **Ghost-level (hors Markdown) :** la **photo en tête** (feature image, au-dessus du titre) et le **sommaire cliquable** (TOC générée par le thème depuis les titres `##`). **Double-check obligatoire :** après publication, comparer le rendu Ghost au Markdown source — ne pas confondre les deux.

## 5. Photo + crédit

- Choisir la photo du Cadre (matière JC) + crédit exact :
  `*Espèce (nom latin) · boîtier · objectif · © JC Havaux / ARTEON*`

## 6. Mots-clés

- En tête d'édition, juste après le thème : `**Mots-clés :** …` (5-10 termes).

## 7. Vérification du Constat

- Fait vérifié + source + date. Ton sobre, sans polémique.

## 8. Checklist « Notes de publication »

- [ ] JC relire et valider
- [ ] Mots-clés en tête
- [ ] Crédits photo exacts
- [ ] `status:` du frontmatter : `draft` → `scheduled` (date programmée) → `published`

## 9. Dépôt

- EN : `editions/final/wildlens-edition-{N}-{slug}.md`
- FR : `editions/fr/wildlens-edition-{N}-{slug}.md`
- Les dates de publication/programmation vivent dans `thread-arteon.md` et `INDEX.md`,
  **pas** dans le frontmatter `date:` (qui garde la date de rédaction d'origine).

## Notes

- Ne pas déduire le statut du nom de fichier — lire `status:` du frontmatter.
- Publication Ghost : `wildlens.arteon.be`.
