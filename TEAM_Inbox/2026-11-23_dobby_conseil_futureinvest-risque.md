---
type: conseil-verdict
topic: FUTURE_INVEST — paramètres de risque
author: "[[Dobby]]" (chairman)
stances: [Contrarian, Premiers Principes, Expansionniste, Outsider, Prémortem]
created: 2026-11-23
mode: CONSEIL COMPLET (5 stances)
---

# CONSEIL — VERDICT

**Décision :** adopter les paramètres de risque proposés pour FUTURE_INVEST —
`MAX_DRAWDOWN_PCT = −10 %` (alerte −5 %), `MAX_POSITION_SIZE = 20 %/position`,
max 2 positions, exposition brute ≤ 40 % — pour un capital plafond 50 k€ (tranches
5 k → 10 k), swing event-driven sur futures agricoles + énergie.

**Recommandation : NO-GO sur le libellé proposé → CONDITIONNEL sur une réécriture en risque-unitaire.**

---

## Arguments pour (ce qu'il faut garder)

- **−10 % / −5 % est correct** comme *disjoncteur de gouvernance* : 4/5 stances le valident en tant que couche basse. Correct en ordre de grandeur pour un débutant à horizon 2-3 ans.
- **−1,3 %/jour est cohérent** comme garde-fou souple — à condition d'être raccordé à un risque/trade unitaire (R = 0,5 % → −1,3 % = 2,6R, −10 % = 20R).
- L'intention (borner la perte, démarrer petit) est juste et alignée sur le profil JC.

## Arguments contre (le défaut structurel)

1. **Erreur d'unité — le maillon qui casse tout.** `20 %/position` mélange notionnel, marge et risque. Un contrat plein de maïs ≈ 22–24 k€, blé ≈ 25 k€, soja ≈ 48–52 k€, WTI ≈ 63–70 k€ de notionnel → « 20 % » de 50 k€ est **inapplicable** (seul le micro-WTI y tient) ; lu comme marge, il autorise 4–5× de levier caché. Sur la tranche 5 k€, **aucun** contrat agricole n'est tradable à risque sain.
2. **−1,3 %/jour est illusoire sur du swing différé.** Un limit-move soja = 7× la limite journalière ; un gap WTI +8 % = 101 % du drawdown, en une nuit. Le gap saute le stop : la limite est violée *sans jamais être respectée*.
3. **« 2 positions » n'est pas de la diversification.** Blé/maïs/soja corrèlent 0,6–0,85 (→1 en stress) ; WTI/Brent ρ≈0,97. Deux positions dans le même complexe = un seul pari à 40 % déguisé.
4. **Le risque FX est absent.** P&L en USD, equity en EUR, non hedgé. −5 % d'EUR/USD = −2 % de capital à stratégie nulle, non compté dans les −1,3 %.
5. **Paramètres manquants** (5/5 stances) : risque-au-stop par position, blackout événementiel (WASDE/OPEC), expiration de signal, plafond par facteur, échelle de dé-risking, règle de tranches, kill-switch/marge buffer.

## Objection la plus forte (Contrarian)

> « Le −10 % n'est pas un plancher, c'est un ordre exécuté au prix du gap ou par le
> moteur de marge — donc à −13 %, −18 %, −20 %. Le paramètre n'échoue pas en régime
> normal ; il échoue exactement le jour où il compte. Un plafond qu'un gap week-end
> rend caduc n'est pas un garde-fou : c'est un rassurant. »

**Réponse (acceptée en totalité) :** l'objection est fondée et n'est pas un point de calibration — c'est une erreur de *grandeur mesurée*. On ne resserre pas les chiffres : on change l'unité (risque-au-stop, pas % de capital) et on ajoute les garde-fous absents. Le −10 % devient alors atteignable **seulement par une série** (20R à R = 0,5 %), jamais par un événement unique (stress-loss ≤ 2 %/position + blackout événementiel + micro-contrats + plafond FX).

## Dissent (désaccords résiduels entre stances)

- **Contrarian** maintient REJETER tel quel et exige le modèle risque-unitaire complet (0,5 %/trade, 1,5 % simultané, stress-gap ≤ 4 %, micro seuls à 50 k€, grains différés à ≥150 k€) — la stance la plus dure.
- **Expansionniste** avertit que le halt binaire à −10 % **éjecte le système avant la queue qui paie** (l'edge est concentré dans 2-3 fenêtres/an) → préfère une *échelle* de dé-risking (−5/−8/−12, halt −15 %) + fenêtre de choc + long gamma.
- **Outsider** ajoute le point de lucidité : sans edge, ces garde-fous ont ~32-64 % de proba de toucher −10 % en un an → la tranche 1 est un **frais de scolarité**, pas un capital à fructifier.

## Résidu de risque assumé

- La tranche 1 (5 k€) ne permet réellement que **du micro** (MCL/MGC/micro-indices) ; les grains agricoles — pourtant le cœur de l'edge documenté — ne deviennent viables qu'à **~30–50 k€**. Soit relever la tranche 1, soit assumer que les tranches 1-2 sont un « laboratoire micro-énergie » avant les céréales.
- Le signal event-driven en données différées restera structurellement en retard ; la latence de décision est le risque que **aucun** pourcentage ne mesure.

---

## Verdict final

Conserver `−10 %/−5 %` et `−1,3 %/jour` comme **couche basse** ; **remplacer**
`MAX_POSITION_SIZE = 20 %/position + 40 % brut` par un dimensionnement en **risque** :

1. `RISK_PER_TRADE = 0,5 %` de l'equity au stop (≤ 1 % après 30 trades validés) — taille dérivée de la distance au stop.
2. Notionnel par contrat **≤ 15 %** de l'equity ; **micro-contrats obligatoires** au démarrage.
3. **Stress-loss ≤ 2 %**/position (limit-move + gap + slippage + FX) ; marge initiale totale ≤ 25 %, buffer ≥ 3×.
4. **Plafond par facteur** (grains = 1 facteur, énergie = 1), pas par nombre de lignes.
5. **MAX_FX_EXPOSURE ≤ 25-50 %** de notionnel USD (ou hedge) ; P&L compté en EUR.
6. Paramètres manquants : blackout événementiel (T−48 h/T+2 h autour WASDE/OPEC), expiration de signal (≤ 4 h), échelle de dé-risking (−5 % → taille ÷2 ; −7,5 % → flat ; −10 % → cooldown 2 sem. + ré-entrée à 25 %), `MAX_WEEKLY_LOSS −3,5 %`, règle de tranches (jamais après une perte).

**À trancher par JC :** relever la tranche 1 à 20-25 k€ pour toucher les céréales dès le début, OU assumer un démarrage micro-énergie seul.

---
*Conseil complet — 5 stances en tâches durables. Analyses sources :*
`TEAM_Inbox/2026-11-23_conseil_futureinvest-risque_{contrarian,premiers-principes,expansionniste,outsider,premortem}.md`
