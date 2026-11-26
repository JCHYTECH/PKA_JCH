# Proposition — Recadrage précis + crop guide overlays

> Dobby 🦉 — 2026-11-20 · Recherche + proposition (aucune implémentation).
> Contexte : Argus donne aujourd'hui un conseil qualitatif (« recadrer à droite pour
> donner de l'air à la queue »). Question : peut-on être plus précis ? Piste : overlays.

---

## Verdict

Oui. On peut passer d'une phrase à un **rectangle de recadrage exact en pixels**
+ un **overlay visuel** (grille de composition + recadrage proposé dessiné sur l'image).
Le « crop guide overlay » est exactement la bonne piste — et le champ est mature
(composition-aware cropping : Liu et al. 2010, Deep Cropping ICCV 2017, ASM-Net,
AesCrop, ProCrop).

## Architecture — 3 étages, coût ≈ 0

### Étage 1 — Localisation du sujet (gratuit, dans l'appel Opus existant)
Étendre le JSON qu'Argus retourne déjà, avec 3 champs :
- `subject_bbox` : [x, y, w, h] normalisé 0–1 (le sujet : adulte + poussin)
- `focal_point`  : [x, y] normalisé (l'œil / le point d'ancrage visuel)
- `gaze_direction` : "left" | "right" | "center" (sens du regard/mouvement)

→ Pas de nouveau modèle. C'est le modèle qui nous donne déjà la critique qui
localise aussi le sujet.

### Étage 2 — Calcul de recadrage (déterministe, `crop_advisor.py`)
- Génère des recadrages candidats, les score contre les guides de composition :
  règle des tiers, nombre d'or (phi grid), diagonale.
- Place le `focal_point` sur une intersection forte ; donne de **l'air dans le sens
  du regard** (répond directement au cas « air à droite de la queue »).
- Contraintes : ratio cible (3:2, 4:5, 1:1…), ne pas couper le sujet, **résolution
  minimale** (ex: ≥ 3000 px grand côté pour le tirage).

### Étage 3 — Overlay (PIL, déterministe)
- Rendu sur l'image : grille (tiers + phi + diagonale) + rectangle de recadrage
  proposé + bbox sujet + point focal.
- Sortie JPEG à côté du rapport PDF.

## Insight de la littérature — important

Les règles de composition sont un **vocabulaire, pas une doctrine** (Grid Maker Pro,
Digital Camera World). Le conseiller doit donc proposer **2–3 options** (tiers / or /
diagonale), pas une seule vérité. Le photographe choisit — l'outil rend visible le
dilemme, il ne le tranche pas à sa place.

## Test idéal

Le fou de Bassan est le cas parfait : sujet légèrement décentré (point AF à −366/+340,
donc à gauche du centre), regard/queue orientés vers la droite → besoin d'air à droite.
C'est exactement le scenario que l'overlay + le crop précis doivent résoudre.

## Différence avec l'existant

| | Aujourd'hui | Demain |
|---|---|---|
| Sortie | phrase qualitative | bbox + crop exact (px) + overlay |
| Composition | une seule suggestion | 2–3 options (tiers/or/diagonale) |
| Direction du regard | implicite | explicite (champ `gaze_direction`) |
| Contrôle print | non | résolution minimale garantie |

---

## Sources

- Optimizing Photo Composition (Liu et al. 2010) — https://www.cs.jhu.edu/~misha/ReadingSeminar/Papers/Liu10.pdf
- Deep Cropping (ICCV 2017) — https://openaccess.thecvf.com/content_ICCV_2017/papers/Wang_Deep_Cropping_via_ICCV_2017_paper.pdf
- ASM-Net (composition + saliency score map) — https://www.alphaxiv.org/abs/1911.10492
- ProCrop (professional compositions) — https://arxiv.org/html/2505.22490v1
- Composition overlays (thirds / phi / diagonal / spiral) — https://gridmakerpro.com/learn/composition-overlays-for-photographers
- Golden ratio vs rule of thirds — https://expertphotography.com/golden-ratio-vs-rule-of-thirds
