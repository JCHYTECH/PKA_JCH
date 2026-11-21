# SELPHY CP1300 — Alimentation 12V (vanlife)

> Mini-fiche matérielle — Dobby 🦉 · 2026-11-12
> Imprimante photo Canon SELPHY CP1300 (dye-sub 10×15 cm) + batterie NB-CP2LH.
> Objectif : imprimer dans le van sur le 12 V, sans le bloc secteur Canon.

---

## Données d'origine (étiquette CA-CP200B + specs Canon)

| Élément | Valeur |
|---|---|
| Adaptateur d'origine | Canon CA-CP200B — **24 V · 1,8 A** (= 43 W) |
| Jack de sortie | **5,5 × 2,5 mm · centre-positif** |
| Batterie | NB-CP2LH — se recharge **dans** l'imprimante |
| Autonomie | ~72 tirages postcard/charge (Canon) — ~50–65 en pratique |
| Consommation | ~60 W pic, ~4 W veille |

## Solution retenue — boost DC-DC 12 V → 24 V

Le CA-CP200B n'est qu'un transformateur 230 V → 24 V. On le remplace par un **boost DC-DC 12 V → 24 V** alimenté par la prise allume-cigare.

## Panier (BOM) — 4 pièces

| # | Pièce | Référence | Prix |
|---|---|---|---|
| 1 | Convertisseur boost 12V→24V · 3A · 72W · IP67 | Uadme `B0DB1ZLTNH` | **14,95 €** (vérifié) |
| 2 | Porte-fusible lame en ligne 16AWG · fusible 5A inclus | Gebildet `B078X977PK` | **6,76 €** (vérifié) |
| 3 | Câble allume-cigare → jack 5,5 × 2,5 mm (pass-through) | — | ~5 € (non vérifié) |
| 4 | Jack 5,5 × 2,5 mm mâle · centre-positif | — | non vérifié |

## Montage

```
[allume-cigare] → [porte-fusible 5A] → [Uadme 12V→24V] → [jack 5,5×2,5 centre+] → SELPHY
```

1. Prendre le câble allume-cigare (n°3), couper son jack côté sortie.
2. Insérer le porte-fusible (n°2) sur le fil +12 V.
3. Brancher les fils sur l'entrée du Uadme (accepte 10–20 V).
4. Côté sortie 24 V, sertir/souder le jack 5,5 × 2,5 mm (n°4) en centre-positif.
5. **Contrôler la polarité au multimètre avant de brancher l'imprimante.**

## Points de vigilance

- **Sortie 24 V obligatoire** — pas 30 V, pas 220 V AC.
- **Jack 5,5 × 2,5 mm** — la plupart des accessoires sont en 2,1 mm ; vérifier.
- **Fusible 5 A** sur l'entrée (tirage réel ~4 A).
- Convertisseur ≥ 2 A en sortie (le Uadme fait 3 A, marge confortable).

## Produits écartés (historique)

- **ACOGEDO `B0HN3F2MX1`** — boost 12V/24V → **30 V** (+25 % hors spec). ❌
- **`B0CP66BBPQ`** — onduleur 12 V → **220 V AC** (mauvaise famille). ❌

---

*Source : specs Canon (CA-CP200B), relevé JC, recherche Amazon 12/11/2026.*
