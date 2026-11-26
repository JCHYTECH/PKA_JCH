# Analyse transcript — Andrej Karpathy « Got Fed Up With YouTube. Claude Built Him His Own in 2 Hours »

> Date : 2026-11-14 · Dobby 🦉 · source NoteGPT (vidéo de veille IA, EN, ~8 min 40)

## Nature
Vidéo de veille IA (format « breakdown » d'actualité). Décrypte le projet **HackerTube** de Karpathy : un site de vidéos personnel bâti par un agent (Claude) à partir de 43 millions de commentaires Hacker News.

## Thèse
Un « feed » de recommandation peut être reconstruit avec **4 règles déterministes + un agent de lecture** — et le signal de qualité durable (qui recommande encore des années après) bat le signal d'engagement immédiat de YouTube.

## Points clés
- Pipeline : 43 M commentaires HN → 4 règles → **6 454 vidéos** (HackerTube), puis 47 k vidéos (TristanTube, seconde itération en ~3 min).
- **Règle 1 (code pur)** : chercher les liens YouTube dans les commentaires → ~100 k+ vidéos.
- **Règle 2 (filtre déterministe)** : une vidéo est retenue si ≥3 personnes l'ont liée dans ≥3 mois distincts, avec commentaire ≥100 caractères → **6 454**.
- **Règle 3 (IA)** : Claude Sonnet (coordonnés par Opus) lit ~40 k commentaires (~1 sur 1 000) et les labellise — recommandation / citation / blague / critique. ~4/10 sont des recommandations ; le reste = citations comme preuve.
- **Règle 4 (classement temporel)** : score = nombre de mois distincts de recommandation (léger bonus aux « raves ») — écrase les pics uniques (ex. vidéo épidémie 2020, 10 recommandations en 1 seul mois → score 1, retombe au milieu).
- Coût : ~500 M tokens en entrée (dont ~90 % = relecture d'instructions par les agents), ~5 M tokens de texte réel ; ~300 $ au prix liste (« by our math », estimation de la chaîne). Karpathy est sur abonnement.
- Rôle humain réduit à 4 actions : clé Google (détails vidéo), serveur loué, domaine acheté + pointé. Tout le reste par l'agent.
- Open-source + note « écrite pour agents IA » → réplicable. Variantes communautaires : app Apple TV, « Hacker Courses » (même méthode sur Reddit), un dev a sorti 317 vidéos pour ~4 $.

## Confirmer
- ✅ **Établi** (auto-rapporté + public) : existence du projet, méthode 4 règles, ordres de grandeur.
- ⚠️ **Affirmé** : le coût ~300 $ (estimation de la chaîne, pas de Karpathy).
- ❓ **Non prouvé** : la « supériorité » de HackerTube sur YouTube — Karpathy lui-même la qualifie de « taste, not a test ».

## Conseil — usage dans PKA
- **Impact direct :** ⚪ faible.
- **Impact pattern :** 🟡 réutilisable.

Le vrai enseignement n'est pas « refaire un HackerTube » mais le **pattern hybride** :
`filtre déterministe (100 % des données, quasi gratuit) → étiquetage LLM (échantillon) → classement temporel (anti-pic)`.

Résonances PKA :
1. **PHOTO_AI_JURY** — même logique que notre tri « RAW / analyse / évaluation » : l'IA assiste, le rang se gagne dans la durée (votes répétés), pas sur un pic.
2. **Keyworder / veille** — « filtre déterministe avant LLM » = exactement la règle PKA « grep/script d'abord, LLM ensuite ».
3. **WildLens** — « ranker par mois distincts de recommandation » = signal anti-clickbait, cohérent avec le positionnement éditorial (l'info qui dure vs le buzz).

## Recommandation
Ne pas adopter le site. **Capturer le pattern** (Forge) comme recette réutilisable pour tout « tri de contenu à grande échelle » — candidat pour une fiche veille dans `01_AI_IT_TOOLS`.

## Actions
- [ ] **P2 · Forge** — noter le pattern « 4 règles + agent lecteur » en recette veille (une ligne par règle suffit).
- [ ] **P3 · Dobby** — rien d'urgent ; garder en mémoire comme référence de coût (~300 $ / 500 M tokens sur un tri de 43 M commentaires).

## Routing
Source → `03_PROJECTS/01_AI_IT_TOOLS/99_REFERENCES/karpathy-hackertube_2026-11-14/`
