# Brief CAD — Meuble banquette Lupo V9

> Fiche autonome à remettre à une IA (ou personne) spécialiste CAO.
> Objet : modéliser et coter précisément le meuble banquette du van Lupo, version V9.
> Source : `meuble-banquette-profiles-alu-v9.md` + `v9-plan.svg` + `v9-coin.svg`.

---

## 0. Mission

Produire à partir de ce brief (sans rien supposer) :

1. Un **modèle 3D** des 3 caissons solidarisés (A + B + C).
2. Des **vues 2D cotées** : face, côté, dessus + détail d'angle (plan + coupe).
3. Une **vue éclatée d'un coin** (équerre 3 voies + goulotte + table).
4. Une **liste de coupes** régénérée, à confronter au §5/§6.
5. La **boucle fermée** (§10).

---

## 1. Enveloppe

- **Total : 920 × 540 × 256 mm** (Longueur × Profondeur × Hauteur hors tout).
- Modules : A = **344** · B = C = **288** mm de largeur, profondeur **540**, hauteur **256** (communes).
- 3 caissons ouverts, accès double sens (avant allée / arrière extérieur), table = assise coulissante.

---

## 2. Matériaux

| Élément | Matière | Cote |
|---|---|---|
| Ossature | Profilé aluminium **2020** (20×20) | rainure T-slot 6 mm |
| Goulotte | **U aluminium** | largeur intérieure **13–14 mm** |
| Panneaux fixes | Dibond | **3 mm** |
| Table / assise | HPL compact | **12 mm** |

---

## 3. Connecteur d'angle — équerre 3 voies iMetrx (UNIQUE)

- Équerre **3 voies** pour 2020, insérée dans la rainure, 4 trous, vis + clé incluses, zamak.
- **Un seul type de connecteur partout** : 24 unités (8 sommets × 3 modules).
- ⚠️ Cotes exactes de l'équerre à confirmer sur la pièce réelle (position des 4 trous, prise sur le 3ᵉ profilé).

---

## 4. Convention d'assemblage du coin (coupe droite, aucun onglet)

- **Rail profondeur** : passant, pleine longueur = **540 mm**.
- **Rail largeur** : buté contre le rail profondeur = largeur extérieure − 2×20 → **304** (A) / **248** (B/C).
- **Montant** : **204 mm** = 256 − 20 (bas) − 20 (haut) − 12 (table).
- **Les 4 rails du haut sont au même niveau** (Z 224–244), comme le cadre bas → **coin 3 voies propre aux 8 sommets**.

---

## 5. Liste de coupes — profilés 2020 (44 pièces)

| Pièce | Longueur | Qté | Total (mm) |
|---|---|---|---|
| Rail profondeur (haut + bas) | 540 | 12 | 6 480 |
| Rail largeur A (haut + bas) | 304 | 4 | 1 216 |
| Rail largeur B/C (haut + bas) | 248 | 8 | 1 984 |
| Montant vertical | 204 | 12 | 2 448 |
| **TOTAL** | | **44** | **12 128 ≈ 12,13 m** |

---

## 6. Liste de coupes — panneaux + goulotte

| Pièce | Qté | Dimensions (mm) | Matière |
|---|---|---|---|
| Fond A | 1 | 304 × 500 | Dibond 3 |
| Fond B/C | 2 | 248 × 500 | Dibond 3 |
| Côté | 6 | 500 × 204 | Dibond 3 |
| Volet A | 2 | 304 × 204 | Dibond 3 |
| Volet B/C | 4 | 248 × 204 | Dibond 3 |
| Table A | 1 | 344 × 540 | HPL 12 |
| Table B/C | 2 | 288 × 540 | HPL 12 |
| **Goulotte U** | 6 | 540 (long) × 13–14 (int.) | alu |

---

## 7. Agencement 3D (repère X = largeur, Y = profondeur, Z = hauteur ↑)

- **Cadre bas** (Z 0–20) : 2 rails profondeur (X 0–20 / L−20–L, Y 0–540) + 2 rails largeur (X 20–L−20, Y 0–20 / 520–540).
- **Cadre haut** (Z 224–244) : identique au cadre bas, translaté +224 en Z.
- **Montants** (4) : Z 20–224, aux 4 coins.
- **Goulottes** (2) : vissées sur le **dessus** des 2 rails profondeur hauts (Z 244–256), le long de Y.
- **Table** (Z 244–256) : HPL 12, bords gauche/droite dans les goulottes, dessus affleurant à 256. Sortie 300 mm vers Y+ ou Y−.
- **Ouverture intérieure** : X 20–L−20 (= 304/248) · Y 20–520 (= 500) · Z 20–224 (= 204).

---

## 8. Contraintes

- Assise **80 kg** ponctuel (table fermée → portée par les 4 rails hauts). Table sortie → goulotte porte la table seule (~20 kg).
- **Anti-grippage** : jeu 0,5–1 mm + glisseurs nylon sur les bords de table (évite le coincement en porte-à-faux).
- Volets 90° vers le bas, charnière piano arête basse, loquet haut contre le rail haut.
- Solidarisation A+B+C par chevilles Ø8 + loquets.

---

## 9. Boucle fermée (auto-vérification)

```
344 = 304 + 2×20      (A)
288 = 248 + 2×20      (B/C)
256 = 20 + 204 + 20 + 12   (hauteur : bas + montant + haut + table)
540 = 500 + 2×20      (profondeur intérieure)
920 = 344 + 288 + 288 (empreinte)
```

---

## 10. Points à confirmer

1. **Équerre iMetrx** : cotes exactes, position des 4 trous, prise sur le 3ᵉ profilé.
2. **Goulotte** : hauteur exacte (±2 mm) pour l'affleurement de la table à 256 ; largeur intérieure (13 ou 14 mm) selon le jeu visé.
3. **Sortie réelle** (300 mm) et anti-grippage → valider au prototype module A.
4. **Engagement des panneaux fixes en rainure** : cotes = ouverture libre ; pour tenue captive, +≈6 mm par bord engagé.
5. **Préhension des volets** : à décider (prise affleurante creusée).

---

*Brief V9 — 2026-11-08 par Dobby. Goulotte U rapportée, montant 204, équerre 3 voies unique, rails du haut abaissés au même niveau.*
