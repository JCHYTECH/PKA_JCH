# Brief CAD — Meuble banquette Lupo V8

> Fiche descriptive autonome à remettre à une IA (ou une personne) spécialiste CAO.
> Objet : modéliser et coter précisément le meuble banquette du van Lupo, version V8.
> Source : `meuble-banquette-profiles-alu-v8.md` + `v8-plan.svg` + `v8-coin.svg` (même dossier).

---

## 0. Mission demandée au spécialiste CAD

Produire, à partir de ce brief uniquement (sans rien supposer de plus) :

1. Un **modèle 3D** des 3 caissons solidarisés (A + B + C).
2. Des **vues 2D cotées** : face, côté, dessus + un **détail d'angle** (plan + élévation).
3. Une **vue éclatée d'un coin** montrant l'équerre 3 voies et les 3 profilés.
4. Une **liste de coupes** régénérée depuis le modèle, à confronter à celle du §5.
5. La **vérification de boucle fermée** (§10).

---

## 1. Vue d'ensemble (enveloppe)

| | Valeur |
|---|---|
| Encombrement total | **920 × 540 × 256 mm** (Longueur × Profondeur × Hauteur) |
| Modules | A = **344** mm · B = C = **288** mm de largeur, empilés côte à côte sur la longueur |
| Hauteur hors tout | **256 mm** (contrainte : lit banquette passager) |
| Profondeur | **540 mm** (commun aux 3 modules) |
| Usage | 3 caissons ouverts, accès double sens (avant = allée / arrière = extérieur) |

Les 3 modules sont **identiques en profondeur (540) et hauteur (256)** ; seuls changent la largeur (344 vs 288) et le contenu des panneaux.

---

## 2. Matériaux

| Élément | Matière | Épaisseur | Rôle |
|---|---|---|---|
| Ossature | Profilé aluminium **2020** (T-slot) | section **20 × 20 mm** | 12 arêtes par module |
| Rainure | T-slot, ouverture **6 mm** sur les 4 faces | — | insertion panneaux + équerre + coulisses |
| Panneaux fixes | **Dibond** (sandwich alu/PolyEthylène) | **3 mm** | fond + côtés + volets |
| Table / assise | **HPL compact** | **12 mm** | couvercle coulissant |

---

## 3. Connecteur d'angle — équerre 3 voies iMetrx

- **Type** : équerre d'angle **3 voies** pour profilé 2020, **insérée dans la rainure**, **4 trous de fixation**, vis + clé incluses.
- **Matière** : zamak (alliage de zinc).
- **Rôle** : relier, à chaque sommet du caisson, **2 rails horizontaux + 1 montant vertical** (3 profilés perpendiculaires).
- ⚠️ **Cotes exactes à confirmer sur la pièce réelle** (dimensions de l'équerre, position des 4 trous, nature de la prise sur le 3ᵉ profilé). Voir §12.

---

## 4. Convention d'assemblage du coin (règle unique)

**Coupe droite, aucun onglet.** À chaque angle :

```
rail profondeur  ──────────────────  PASSANT (pleine longueur : 540)
rail largeur       ────────────────  BUTÉ (s'arrête contre le rail profondeur)
montant                   ▓          SANDWICH (entre cadre bas et cadre haut : 216)
```

Formules :

- `rail profondeur = profondeur extérieure = 540 mm`
- `rail largeur = largeur extérieure − 2×20 mm` → **304** (A) / **248** (B/C)
- `montant = hauteur − 2×20 mm` → **216 mm**

---

## 5. Liste de coupes — profilés 2020 (44 pièces)

| Pièce | Longueur | Qté | Total (mm) |
|---|---|---|---|
| Rail profondeur (haut + bas) — passant | 540 | 12 | 6 480 |
| Rail largeur A (haut + bas) — buté | 304 | 4 | 1 216 |
| Rail largeur B/C (haut + bas) — buté | 248 | 8 | 1 984 |
| Montant vertical | 216 | 12 | 2 592 |
| **TOTAL** | | **44 pièces** | **12 272 mm ≈ 12,27 m** |

Par module : 4 rails profondeur (2 bas + 2 haut) + 4 rails largeur (2 bas + 2 haut) + 4 montants = **12 arêtes**.

---

## 6. Liste de coupes — panneaux

| Panneau | Qté | Dimensions (mm) | Matière |
|---|---|---|---|
| Fond A | 1 | 304 × 500 | Dibond 3 |
| Fond B/C | 2 | 248 × 500 | Dibond 3 |
| Côté (gauche/droite) | 6 | 500 × 216 | Dibond 3 |
| Volet A | 2 | 304 × 216 | Dibond 3 |
| Volet B/C | 4 | 248 × 216 | Dibond 3 |
| Table / assise A | 1 | 344 × 540 | HPL compact 12 |
| Table / assise B/C | 2 | 288 × 540 | HPL compact 12 |

**Cotes = ouverture libre (intérieure).** Voir §12 pour l'engagement en rainure des panneaux fixes.

---

## 7. Quincaillerie (BOM)

| Élément | Qté | Précision |
|---|---|---|
| Coulisses Chambrelan D5DD (double développement) | 6 (3 paires) | alu, 20 kg/paire, butée 300 mm |
| Équerre 3 voies iMetrx | 24 | 8 sommets × 3 modules |
| T-nuts M4 | ~12 | fixation coulisses réglable |
| Charnière piano | 6 | 304 (A) / 248 (B/C) mm — arête basse des volets |
| Loquet à bascule | 6 | 1 par volet (haut) |
| Chevilles Ø8 + loquets de solidarisation | 4 + 2 | liaison entre modules |

---

## 8. Agencement 3D d'un coin (placement exact)

Repère : **X = largeur** (0 → L), **Y = profondeur** (0 → 540), **Z = hauteur** (0 → 256, vers le haut). Origine = coin bas-avant-gauche d'un module.

**Cadre bas** (Z ∈ [0, 20]) :
- Rail profondeur gauche : X ∈ [0, 20], Y ∈ [0, 540]
- Rail profondeur droit : X ∈ [L−20, L], Y ∈ [0, 540]
- Rail largeur avant : X ∈ [20, L−20], Y ∈ [0, 20]  ← **buté** entre les deux rails profondeur
- Rail largeur arrière : X ∈ [20, L−20], Y ∈ [520, 540]

**Cadre haut** (Z ∈ [236, 256]) : même tracé, translaté de +236 en Z.

**Montants** (4, Z ∈ [20, 236]) : aux 4 coins, X ∈ {0..20, L−20..L}, Y ∈ {0..20, 520..540}.

**Équerre 3 voies** : à chacun des 8 sommets, dans le coin intérieur, bras insérés dans les rainures, reliant rail profondeur + rail largeur + montant.

**Ouverture intérieure (libre)** : X ∈ [20, L−20] = **304 / 248**, Y ∈ [20, 520] = **500**, Z ∈ [20, 236] = **216**.

---

## 9. Contraintes fonctionnelles

- **Charge assise** : 80 kg ponctuel sur la table ; **table** ~20 kg.
- **Environnement** : van, vibrations + freinage/virage → le coin travaille en **cisaillement (racking)**.
- **Accès double sens** : volet avant (allée) et volet arrière (extérieur) rabattables à 90° vers le bas, charnière piano sur l'arête basse, loquet en haut.
- **Table = assise coulissante** : sort de **300 mm** vers l'avant OU l'arrière, sur 2 coulisses double sens montées sous le panneau HPL.
- **Solidarisation** : les 3 modules s'assemblent par chevilles Ø8 + loquets (pas de fixation permanente).

---

## 10. Boucle fermée (auto-vérification du modèle)

Le modèle doit respecter, sur chaque module :

```
344 = 304 + 2×20      (A)
288 = 248 + 2×20      (B/C)
256 = 216 + 2×20      (hauteur)
540 = 500 + 2×20      (profondeur intérieure)
920 = 344 + 288 + 288 (empreinte totale)
```

Toute égalité qui ne tombe pas juste = erreur de modélisation ou de coupe.

---

## 11. Livrables attendus

1. Modèle 3D (paramétrique si possible) — 3 modules solidarisés.
2. Vues 2D cotées : face / côté / dessus + détail d'angle.
3. Vue éclatée d'un coin (équerre + 3 profilés).
4. Liste de coupes régénérée (profilés + panneaux) — à confronter au §5/§6.
5. Rapport de boucle fermée (§10).

---

## 12. Points à confirmer (incertitudes assumées)

1. **Géométrie exacte de l'équerre iMetrx** : cotes hors tout, position des 4 trous, comment le 3ᵉ profilé (montant) est tenu (bras dédié ? prise en bout ?). → à mesurer sur la pièce réelle.
2. **Engagement des panneaux fixes en rainure** : cotes données à l'ouverture libre. Pour une tenue captive en rainure 6 mm, prévoir **≈ +6 mm par bord engagé** (fond ≈ 316×512, côté ≈ 512×228). Volets : pas de rainure (charnière), cote = ouverture libre.
3. **Coulisses D5DD** : cote d'extension exacte, position de la butée 300 mm, entraxe de fixation.
4. **Charnière piano** : position exacte (affleurante vs en retrait), visserie sur Dibond 3 mm.
5. **Préhension des volets** : à décider — privilégier une prise affleurante creusée (le volet reste à plat une fois rabattu).

---

*Brief rédigé le 2026-11-08 par Dobby — version canonique V8, connecteur équerre 3 voies iMetrx, convention coupe droite (profondeur passant / largeur buté / montant sandwich).*
