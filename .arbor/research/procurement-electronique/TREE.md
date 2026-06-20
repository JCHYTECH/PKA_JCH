# Arbre de recherche — Compétence procurement électronique

**Projet :** procurement-electronique  
**Objectif :** Créer une compétence autonome de recherche et achat de composants électroniques  
**Créé :** 2026-06-18  
**Cycles max :** 10 | **Seuil convergence :** 1% | **Patience :** 3 cycles

---

## Arbre

```
ROOT (merged) — Flux manuel actuel
└── 1 (merged) ✅ — H1: Agent dual Mouser+DigiKey + optimisation panier
    ├── 2 (pending) — H2: Double-validation MPN (spec→API→datasheet)
    └── 3 (pending) — H3: Registre supply cumulatif (cache)
```

## Résultat Cycle 1

**Test sur BOM WildNexus (11 composants) :**
- Mouser: 10/11 trouvés, prix réels, liens directs
- DigiKey: 10/11 trouvés, prix réels, liens directs
- Arbitrage automatique: 5 Mouser, 5 DigiKey, 1 Aucun (KIT-14585)
- Paniers optimisés: Mouser 50.09€, DigiKey 63.98€ (gratuit)
- Économie frais de port: ~37€ vs 8 paniers manuels
- Checklist Chouette: alertes bande EU868, connecteur IPEX, LED IR faune

**Temps d'exécution: ~60s vs ~2h manuel → facteur ~120×**
