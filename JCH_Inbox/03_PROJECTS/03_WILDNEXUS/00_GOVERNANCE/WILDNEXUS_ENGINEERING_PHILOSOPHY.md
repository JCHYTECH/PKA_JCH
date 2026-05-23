# WildNexus — Philosophie d'ingénierie P0

**Date :** 2026-05-18  
**Owner :** Dobby  
**Statut :** Principe actif — s'applique à tous les WP

---

## Principe fondamental

> **Quand l'écart technique entre deux options est faible ou non discriminant pour le cas d'usage P0, retenir le produit le plus robuste au meilleur rapport qualité/prix. Ne pas sur-spécifier.**

Ce principe prime sur la recherche de l'optimum théorique. Un choix "assez bon, solide, disponible" est supérieur à un choix "légèrement meilleur sur le papier, fragile, rare ou coûteux".

---

## Critères de décision par ordre de priorité

1. **Adéquation au cas d'usage P0** — le composant remplit-il la fonction requise dans les conditions P0 ?
2. **Robustesse et disponibilité** — composant éprouvé, fournisseur fiable, stock EU accessible
3. **Rapport qualité/prix** — performance suffisante, pas maximale
4. **Évolutivité minimale** — ne pas fermer les portes P1/P2, mais ne pas les ouvrir à coût P0

---

## Application par WP

| WP | Implication pratique |
|----|---------------------|
| WP01 Conception & Architecture | Décisions d'architecture à un niveau d'abstraction raisonnable — pas de précision excessive sur les paramètres non bloquants pour M-01 |
| WP02 Hardware & Enclos | Composants : disponibilité EU et robustesse terrain priment sur performance marginale. Un composant à 80% de la performance max mais livrable en 5 jours bat un composant optimal à 12 semaines |
| WP03 Firmware ULP | Stack minimaliste — ne pas optimiser les états ULP avant d'avoir mesuré la consommation réelle. "Make it work, then make it efficient" |
| WP04 Edge AI | Classifieur binaire le plus simple atteignant le seuil P0 (animal / non-animal). Pas de sur-ingénierie du modèle avant validation terrain |
| WP05 Validation EVT | Protocole de validation suffisant pour décision go/no-go — pas exhaustif. Documenter ce qu'on observe, pas ce qu'on aurait voulu mesurer |
| WP06 Open Source | Documentation minimale viable pour reproduire le socle — pas une thèse |

---

## Ce que ce principe NE signifie PAS

- Il ne signifie pas ignorer les contraintes dures (IP67, autonomie 60 jours, IR-correction obligatoire).
- Il ne signifie pas choisir le moins cher par défaut.
- Il signifie : **ne pas dépenser de l'énergie à discriminer deux options quand la différence est non significative pour P0**.

---

## Origine

Décision JCH — 2026-05-18, suite à l'analyse du choix de lentille M12 (ADR-002) : les courbes MTF Lensation vs Evetar ne valent pas le temps nécessaire à les obtenir, car l'écart de performance est non discriminant pour le classifieur P0.
