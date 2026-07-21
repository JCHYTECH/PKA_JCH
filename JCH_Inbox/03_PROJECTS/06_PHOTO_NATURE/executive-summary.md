# PHOTO_NATURE — Executive Summary

> Document externe — partenaires éditoriaux, galeries.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**Workflow professionnel de photographie naturaliste — de la capture terrain au tirage d'art, automatisé par IA locale.**

---

## Le pipeline

```
Terrain ──→ Post-traitement ──→ IA Keyworder ──→ IA Critique ──→ Publication
(Canon)     (DxO/Lightroom)     (62 catégories)   (Argus)         (ARTEON/WildLens)
```

1. **Capture** — Canon R10 + 90D, RF 200-800mm, Tamron 150-600mm, macros Laowa
2. **Développement** — DxO PhotoLab, Lightroom, Helicon Focus, Topaz
3. **Keyworder IA** — Gemma4 (M5 local, ~18s/image) → 62 catégories taxonomiques → IPTC + XMP → lisible par Lightroom
4. **Critique IA** — Argus évalue la qualité (73.8/100 moyen, 81% acceptation)
5. **Publication** — ARTEON Gallery (tirages) ou WildLens (journal)

---

## Équipement

| Type | Modèle |
|------|--------|
| Boîtiers | Canon R10, Canon 90D |
| Téléobjectif | Canon RF 200-800mm |
| Zoom | Tamron 150-600mm |
| Macro | Laowa (plusieurs focales) |
| Impression | Epson ET-8550 |
| Logiciels | DxO PhotoLab, Lightroom, Photoshop, Helicon Focus, Topaz, Luminar Neo |

---

## Automatisation IA

- **Keyworder** : 100% autonome, zéro API Google, Gemma4 local sur M5
- **62 catégories** : faune (80+ espèces), flore (40+), comportements, saisons, lumières, compositions, habitats
- **Cache** : évite de re-traiter les images déjà tagguées
- **Sortie** : IPTC + XMP + HierarchicalSubject → import direct Lightroom

---

## Statut

| Composant | Statut |
|-----------|--------|
| Workflow capture | 🟢 Actif |
| Keyworder IA | 🟢 Déployé et fonctionnel |
| Presets Argus | 🟢 11 presets stockés |
| Intégration ARTEON | 🟢 Cross-réfs en place |

---

*Document destiné à un public externe. Pipeline détaillé : `06_PHOTO_NATURE/INDEX.md`*
