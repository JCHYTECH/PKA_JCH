---
name: conception-mecanique
description: Checklist de vérification mécanique avant de figer un design (meuble, support, caisson, structure avec pièces mobiles). Déclencher sur « conception mécanique », « vérifie si ça tient », « interférence », « design structure », « ça tient la route », « mécaniquement ça tient ? ».
---

# Skill — conception-mecanique

Vérifier un design mécanique AVANT de le figer. 5 contrôles obligatoires, dans l'ordre.

## 1. Plan de mouvement / interférence

- Lister toutes les pièces mobiles (coulisse, tiroir, table, volet, porte).
- Pour chacune, tracer le **volume balayé** sur toute sa course.
- Vérifier qu'aucune pièce fixe (rail, montant, panneau, connecteur) n'entre dans ce volume.
- Règle clé : un mécanisme « dans le plan » d'un cadre fermé est **TOUJOURS bloqué** par les rails qui ferment ce plan → monter le guidage AU-DESSUS du cadre, ou abaisser/supprimer l'obstacle.

## 2. Chaîne de charge

- Pour chaque position (fermé / sorti / intermédiaire), identifier **qui porte quoi**.
- Le mécanisme (coulisse / goulotte / charnière) ne porte QUE la **charge mobile** (pièce + charge légère).
- La **charge statique** (personne, poids) passe par la **structure** (rails, montants), pas par le mécanisme.
- Vérifier le cas critique : **porte-à-faux** = pièce sortie + charge → moment de flexion sur le mécanisme.

## 3. Dégagement + anti-bascule

- Jeu minimal entre pièce mobile et guidage : **0,5–1 mm** (ni trop serré = grippage, ni trop lâche = ballottage).
- **Anti-bascule** en porte-à-faux : guidage long, glisseurs, ou épaulement.
- Tolérance thermique (l'alu se dilate) : le jeu doit absorber la dilatation (l'alu s'ouvre en chaud, se resserre en froid).

## 4. Chaîne dimensionnelle fermée

- Un seul référentiel (extérieur ou intérieur), déclaré en tête.
- Chaque pièce écrite en **formule** : `pièce = dimension_ext − Σ(contribution connecteur)`.
- **Boucle fermée** par axe : `dimension_ext = pièce + Σ(connecteurs)`. Si ça ne retombe pas pile → erreur.
- **Type de connecteur vérifié** (cube externe 20×20×20 vs équerre insérée — correction OPPOSÉE).

## 5. Environnement

- **Vibration** (van, machine) : visserie freinée, connecteurs anti-desserrage.
- **Humidité** : matériaux insensibles (alu, HPL, Dibond, inox) — pas de bois nu, pas d'acier non traité.

## Sortie

Verdict **GO** ou **À CORRIGER**, avec :
- les points faibles chiffrés,
- ce que JC doit valider au prototype.

## Voir aussi

- `SOUL.md` — règles « chaîne dimensionnelle fermée » et « conception mécanique (dégagement, interférence, charge) ».
- Contre-exemple vécu : meuble banquette v8→v9 (2026-11-08) — coulisses montées sur flanc intérieur = bloquées par les rails avant/arrière ; corrigé en montant la goulotte AU-DESSUS du cadre (montant 216→204).
