# Procédure de construction — Meuble banquette v9 (aluminium 2020 · goulotte coulissante)

> Construction par phases. Outillage : scie à métaux, clé Allen, cutter, tournevis, équerre, mètre, lime. Perceuse optionnelle (fixation goulotte).
> Références : `meuble-banquette-profiles-alu-v9.md` (design) · `v9-plan.svg` (plan) · `v9-coin.svg` (détail) · `v9-coupes.xlsx` (coupes/BOM).

---

## Phase 0 — Préparation (coupes + commandes)

1. **Profilés** : couper les **44 profilés 2020** :
   - rails profondeur **540 mm** (passants), rails largeur **304/248 mm** (butés), montants **204 mm**.
   - Scie à métaux, trait droit, aucun onglet.
2. **Panneaux** (faire découper) :
   - Dibond 3 mm : fonds (304×500 / 248×500), côtés (500×204), volets (304×204 / 248×204).
   - HPL compact 12 mm : 3 tables (344×540 / 288×540), angles avant R5–R10 (CNC).
3. **Goulotte U 13–14 mm** : 6 longueurs de 540 mm (2 par module).
4. **Quincaillerie** : 24 équerres 3 voies iMetrx (vis + clé incluses), T-nuts M5, glisseurs nylon, 6 charnières piano, 6 loquets.

> **Règle de coupe (boucle fermée)** : `344 = 304 + 2×20` · `288 = 248 + 2×20` · `256 = 20 + 204 + 20 + 12` · `540 = 500 + 2×20`.

---

## Phase 1 — Ossature (3 cages carrées)

1. **Cadre bas** : 2 rails profondeur (540) + 2 rails largeur (304/248), reliés par **4 équerres 3 voies**. Rails largeur butés contre les rails profondeur.
2. **Cadre haut** : identique (4 rails + 4 équerres 3 voies). **Les 4 rails au même niveau** (Z 224–244).
3. **Montants** : 4 × 204 mm, entre les cadres bas et haut, sur les équerres 3 voies.
4. **Équerrage** : diagonales égales avant serrage à fond.
5. Répéter pour les 2 autres modules.

> ⚠️ Ne pas trop serrer avant l'équerrage : les équerres se rattrapent dans la rainure.

---

## Phase 2 — Panneaux (fond + côtés)

1. **Fond** : Dibond (304×500 / 248×500) dans les rainures des 4 rails bas.
2. **Côtés** : Dibond (500×204) dans les rainures des rails haut/bas + montants.
3. **Fixation** : tenus par la rainure ; si jeu, 1–2 vis ponctuelles dans les montants.

---

## Phase 3 — Goulotte + table (coulisse)

1. **Goulottes** : visser 2 goulottes U sur le **dessus** des 2 rails profondeur hauts (T-nuts M5 dans la rainure supérieure). Affleurement : dessus de table à 256 mm.
2. **Table** : glisser le HPL 12 dans les goulottes. Coller les **glisseurs nylon** sur les bords de table (anti-grippage).
3. **Contrôle** : sortie 300 mm avant ET arrière, à plat, sans gripper. Ajuster le jeu si nécessaire.

---

## Phase 4 — Volets (faces avant/arrière)

1. **Charnière piano** sur l'arête basse de chaque volet + rail bas.
2. **Loquet à bascule** en haut, contre le rail haut (Z 224–244).
3. **Contrôle** : volet rabattu à plat (90°), sans accrocher.

---

## Phase 5 — Finitions et contrôles

1. **Assise** : 80 kg sur table fermée → stable (la table repose sur les 4 rails hauts).
2. **Coulisse** : table sortie 300 mm → goulotte porte la table seule (~20 kg), pas de coincement.
3. **Volets** : ouverture/fermeture, loquets francs.
4. **Solidarisation** : A + B + C par chevilles Ø8 + loquets.
5. **Conduite** : volets fermés + loquets, table rentrée.

---

*Procédure v9 — 2026-11-08. Prototype : module A seul d'abord.*
