# AI Image Detection — état de l'art & outil PKA

> 2026-10-22 · Dobby 🦉 · outil : `scripts/pka_ai_image_check.py`
> Demande JCH : « savoir si une photo est AI generated ou si une partie de l'image l'est ».

## Réponse courte

**Oui, mais pas par un détecteur magique.** Trois niveaux de fiabilité très inégaux :

| Niveau | Fiable ? | Réalité mesurée le 2026-10-22 |
|---|---|---|
| 1. Provenance (C2PA / EXIF) | **Oui, déterministe** | Fonctionne. Absence de manifeste ≠ image réelle. |
| 2. Classifieur ViT (Real/Fake) | **Non, inutilisable** | 12/12 vraies photos classées « IA ». |
| 3. Localisation par patchs | Dépend du niveau 2 | Dépend du classifieur → non fiable aujourd'hui. |

## Résultats de validation (mesurés, pas supposés)

**Jeu de test** : 12 photos réelles issues de `07_TRAVELS/pka-decouvertes/raw/images/`
(dashcam + smartphone, aucune manipulation IA connue) + 1 image synthétique générée.

| Modèle | Vraies photos | Image synthétique |
|---|---|---|
| `capcheck/ai-image-detection` | 12/12 → **FAKE 98 %** | FAKE 95 % |
| `dima806/ai_vs_real_image_detection` | 2/2 → **FAKE 99 %** | FAKE 95 % |
| `umm-maybe/AI-image-detector` | 2/2 → **artificial 98 %** | **human 90 %** ❌ |

**Conclusion** : les classifieurs publics sont surajustés aux distributions 2024-2025.
Le traitement smartphone moderne (HDR, débruitage, sharpening) produit des
statistiques proches de la synthèse → faux positifs systématiques. Un modèle
qui classe le synthétique comme « humain » et l'humain comme « artificiel » ne
peut pas servir de base à un jugement.

## Ce que l'outil fait aujourd'hui (niveau 1, fiable)

```bash
python3 scripts/pka_ai_image_check.py photo.jpg
python3 scripts/pka_ai_image_check.py dossier/ --report rapport.md
```

- **C2PA** (`c2pa-python` installé) : détecte un manifeste signé, l'action
  `trainedAlgorithmicMedia`, et les générateurs déclarés (DALL·E, Firefly, SynthID…).
- **EXIF/XMP** : appareil photo, logiciels. Distinction **génération** (marqueurs
  forts) vs **retouche** (« photoshop » seul ≠ preuve — corrigé après un faux
  positif sur une photo smartphone réelle).
- **Verdict** : `indéterminée` par défaut quand aucun signal. C'est volontaire.

```bash
# Classifieur (déconseillé, conservé pour expérimentation)
python3 scripts/pka_ai_image_check.py photo.jpg --with-model
```

## Le vrai risque à connaître

Midjourney v8 (mi-2026) **ne signe pas** en C2PA. Un screenshot ou un re-export
strip le manifeste. **L'absence de preuve n'est jamais une preuve d'absence** —
pour un jury photo, c'est la formulation à tenir.

## Pistes si on veut aller plus loin

1. **Entraîner un détecteur sur NOS images** : JCH produit des milliers de photos
   terrain ; un classifieur fine-tuné sur ce corpus + du synthétique récent
   serait bien plus fiable que les modèles publics.
2. **Venus-DeFakerOne** (arXiv 2026) — détection *et localisation* unifiées, code disponible.
3. **CLIP + artefacts fréquentiels (ondelettes)** — l'approche 2026 sérieuse ;
   les artefacts seuls ne suffisent plus.
4. **Intégration Argus** : en 6ᵉ axe « intégrité », mais **uniquement niveau 1**
   tant que le niveau 2 n'est pas fiable.
