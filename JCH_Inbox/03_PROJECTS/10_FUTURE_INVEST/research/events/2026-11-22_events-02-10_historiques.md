---
project: Future Invest
type: event-library
created: 2026-11-22
status: scaffold consolidé — événements #2-10 (prix historiques à vérifier en Phase 2)
---

# Événements #2-10 — historiques (scaffold)

> Chaque événement = une fiche pour tester l'Event Analyzer (Phase 2). Régime
> classé : **choc d'offre** (météo/géopolitique/politique) vs **cascade de liquidité**
> vs **momentum crash**. Les prix exacts sont à vérifier lors du backtest.

## #2 — 2023-07 — Ban export riz Inde (choc d'offre politique)
- **Déclencheur :** l'Inde (~40 % du commerce mondial de riz) bannit l'export de riz blanc non-basmati (juillet 2023).
- **Chaîne :** politique indienne → restriction d'offre → prix riz +15-20 % (plus haut 15 ans) → substitution vers le blé → pression inflation alimentaire (Asie/Afrique).
- **Instruments :** riz (ZR), blé (ZW). **Opinion attendue :** haussier riz/blé 1-3 mois.
- **Leçon :** la politique publique (pas la météo) est le driver n°1 du riz.

## #3 — 2022-02 — Guerre Ukraine (choc d'offre géopolitique majeur)
- **Déclencheur :** invasion russe (24/02/2022).
- **Chaîne :** guerre → blé/maïs/engrais/tournesol (mer Noire) bloqués → blé +50-60 % (mars 2022) → engrais (urée) spike → énergie (gaz) spike.
- **Instruments :** blé (ZW), maïs (ZC), gaz (NG), urée. **Opinion :** haussier grains + énergie.
- **Leçon :** les chocs d'offre géopolitiques sont les plus violents et les plus durables.

## #4 — 2021-03 — Suez (choc logistique transitoire)
- **Déclencheur :** porte-conteneurs Ever Given bloque le canal 6 jours (23-29 mars 2021).
- **Chaîne :** blocage → fret en hausse → pétrole spike transitoire → retour à la normale en semaines.
- **Instruments :** pétrole (CL), fret (BDI). **Opinion :** haussier transitoire, réversible.
- **Leçon :** distinguer choc **réversible** (logistique) vs **structurel** (guerre, sécheresse).

## #5 — 2020-04 — Pétrole négatif (choc de demande + contrainte physique)
- **Déclencheur :** WTI à −37 $/baril (20/04/2020), effondrement demande COVID + stockage saturé.
- **Chaîne :** lockdown → demande −30 % → stockage plein → contango extrême → expirations forcées → prix négatif.
- **Instruments :** pétrole (CL). **Opinion :** baissier extrême, puis rebond quand l'offre s'ajuste.
- **Leçon :** le prix peut devenir **négatif** quand la contrainte physique (stockage) est saturée — un circuit-breaker doit l'anticiper.

## #6 — 2012 — Sécheresse maïs USA (choc d'offre météo)
- **Déclencheur :** pire sécheresse depuis 1956 dans le Midwest.
- **Chaîne :** sécheresse → rendements ↓ → stocks ↓ → maïs +50 %+ (vers 8 $+) → soja spike → rationnement/substitution.
- **Instruments :** maïs (ZC), soja (ZS). **Opinion :** haussier grains.
- **Leçon :** la météo (pas la demande) est le driver n°1 du maïs — d'où le surveillant sécheresse.

## #7 — 2010 — Embargo blé Russie (choc d'offre météo + politique)
- **Déclencheur :** sécheresse + incendies → la Russie bannit l'export de blé (août 2010).
- **Chaîne :** sécheresse → récolte ↓ → embargo → blé +60-80 % en quelques mois → émeutes alimentaires (corrélées au printemps arabe).
- **Instruments :** blé (ZW). **Opinion :** haussier fort.
- **Leçon :** météo + politique se combinent (le pire des deux mondes pour l'offre).

## #8 — 2008-10 — Lehman (cascade de liquidité, PAS choc d'offre)
- **Déclencheur :** faillite Lehman (15/09/2008).
- **Chaîne :** faillite → crédit gelé → margin calls → vente forcée de TOUT (or compris) → or −30 % (mars→oct) → dollar ↑.
- **Instruments :** tout, or (GC). **Opinion :** baissier généralisé à court terme (corrélations → 1).
- **Leçon :** en cascade, aucune « valeur refuge » ne tient (cf. spec régimes).

## #9 — 2020-03 — Or −12 % phase aiguë COVID (cascade de liquidité phase 1)
- **Déclencheur :** panique COVID (mars 2020).
- **Chaîne :** panique → vente forcée → or vendu AVEC les actions (−12 %) → phase 2 : assouplissement des banques centrales → or rebondit fortement.
- **Instruments :** or (GC). **Opinion :** baissier transitoire (phase 1), haussier ensuite (phase 2).
- **Leçon :** la cascade est en **deux temps** — le refuge ne protège qu'en phase 2.

## #10 — 2009-03 — Reversal momentum (momentum crash)
- **Déclencheur :** creux de marché (mars 2009), rebond violent.
- **Chaîne :** creux → rebond → les positions momentum (short) se retournent → le facteur momentum subit son pire drawdown.
- **Instruments :** indices, facteur momentum. **Opinion :** le momentum « crashe » au rebond.
- **Leçon :** le momentum crash est le symétrique du choc d'offre — le Risk Supervisor doit le détecter (spec régimes).

---

## Couverture des régimes (bilan)

| Régime | Événements |
|--------|-----------|
| Choc d'offre météo | #6, #7 |
| Choc d'offre géopolitique/politique | #2, #3 |
| Choc logistique transitoire | #4 |
| Choc de demande + contrainte physique | #5 |
| Cascade de liquidité | #8, #9 |
| Momentum crash | #10, + #1 (krach AI 2026) |

→ Les deux régimes du Risk Supervisor (cascade + momentum) sont couverts, ainsi
que les trois familles de chocs d'offre. À scorer en Phase 2 (cible ≥ 7/10).
