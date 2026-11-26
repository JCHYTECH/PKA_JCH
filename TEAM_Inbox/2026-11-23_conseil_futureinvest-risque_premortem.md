JC — Post-mortem, stance PRÉMORTEM. Un seul passage.

---

## 1) Récit de l'échec — « Il est parti en vrille en 11 semaines »

Lancement en février 2026 avec la tranche de 5 000 €. Deux marchés : WTI (via micro) et un grain (blé ou maïs). Tout tient trois semaines. Puis trois choses s'enchaînent, et aucune n'est un accident de marché — ce sont les paramètres qui n'existent pas.

**Semaine 4 — la dérive invisible en EUR.** Le dollar faiblit de ~8 % en six semaines (anticipation de baisses de taux Fed). Les positions, libellées en USD, sont *plates en USD* : le moteur ne déclenche aucun stop, l'algo affiche « neutre ». Mais le compte, lui, est en EUR. −8 % de change sur 40 % d'exposition brute = −3,2 % de capital *sans une seule mauvaise décision de trading*. Personne ne l'a vu venir parce qu'aucun paramètre ne mesure le P&L en devise de compte.

**Semaine 7 — le gap qui saute le stop.** Rapport USDA WASDE. Le maïs limite-up à l'ouverture de Chicago, position short prise la veille au soir. Le stop théorique était censé couper à −1,3 %/jour ; le marché ouvre **au-delà** du stop, ordre exécuté 3× plus bas. Un seul gap = −4 % de capital en une nuit. Le `MAX_DAILY_LOSS = −1,3 %` est intact sur le papier (mesuré sur le réalisé) et pourtant violé de 300 % dans les faits : c'est un garde-fou sur un marché continu appliqué à un instrument qui *discontinue*.

**Semaine 8 — l'arrêt dur touche, puis on double la mise.** Cumul FX + gap + deux faux signaux event-driven tardifs (données différées = dernier servi) → −10 %. Halt. Mais aucun paramètre ne dit *comment redémarrer*. JC, encore dans l'énergie du projet, repasse à la tranche 10 000 € « pour récupérer ». Pas d'échelle de ré-entrée → la deuxième tranche subit le même régime de risque, en taille double.

**Semaine 11 — abandon.** −28 % sur le capital engagé, la confiance est morte avant le capital. Le système est débranché. Ce n'est pas la stratégie qui a échoué : c'est le dimensionnement.

---

## 2) Le coupable — l'absence, pas le chiffre

Le coupable principal n'est pas `−1,3 %`, ni `−10 %`. C'est **`MAX_POSITION_SIZE = 20 %` exprimé en % de capital**.

En futures, « 20 % de position » ne veut rien dire tant qu'on ne précise pas *notionnel, marge ou risque*. Un contrat WTI plein = 1 000 barils × ~70 $ ≈ 70 000 $ de notionnel = **140 % d'un capital de 50 000 €**. La formulation en % de capital invite mécaniquement au sur-dimensionnement, parce que la granularité du contrat ne se plie pas au pourcentage. Le paramètre *a l'air* prudent et il est, en réalité, le plus dangereux des trois.

Coupables secondaires, tous des **paramètres manquants** :

- **Aucun budget FX.** Exposition USD sur capital EUR, sans plafond ni comptabilisation en EUR. Un mouvement de change peut consommer tout le drawdown autorisé à stratégie nulle.
- **Aucun contrôle du risque de gap / de blackout événementiel.** Un swing event-driven *dort* à travers les événements qui le font bouger (WASDE, OPEC, météo). `−1,3 %/jour` suppose un marché continu ; les grains et l'énergie ne le sont pas (limites de variation, gaps d'ouverture).
- **Aucune expiration de signal.** Données différées + validation humaine à <1 h/jour = file d'attente. Un signal validé 14 h plus tard n'est plus un signal : soit on exécute à contre-courant, soit on renonce — et le renoncement pousse au sur-dimensionnement compensatoire.
- **Aucune échelle de dé-risking entre −5 % et −10 %.** L'alerte à −5 % n'agit sur rien. Rien ne réduit la taille avant que le mur ne tombe.
- **Aucun plafond de facteur corrélé.** « Max 2 positions » sonne comme de la diversification ; deux positions blé/maïs = **un seul pari directionnel** déguisé en deux. 40 % brut peut être 40 % sur un unique facteur.

Incohérence structurelle, enfin : `−1,3 %/jour × 8 jours = −10,4 %`. Le garde-fou quotidien **est plus permissif que l'arrêt dur** — on peut toucher le mur du drawdown sans jamais avoir franchi la limite journalière. Les deux paramètres ne se protègent pas l'un l'autre.

---

## 3) Ce qu'il fallait fixer

Réécrire le dimensionnement autour du **risque au stop**, pas du capital :

- **RISK_PER_TRADE = 0,5–1,0 % de l'equity à la distance du stop.** Notionnel plafonné en second : `MAX_NOTIONAL_PER_CONTRACT ≤ 15 %` de l'equity, sinon rejet d'ordre. **Micro-contrats obligatoires au démarrage** (MCL, XC/XK/XS) — un contrat doit tenir dans la poche, pas l'inverse.
- **MAX_FX_EXPOSURE = 25 % de notionnel USD net**, ou couverture ; **tout P&L et tout stop calculés en EUR.** Le FX entre dans le drawdown, pas à côté.
- **EVENT_BLACKOUT = aucune entrée T−48 h → T+2 h autour de WASDE / OPEC / rapports de récolte**, exposition overnight plafonnée (≤ 20 % notionnel).
- **MAX_SIGNAL_AGE = 4 h (ou ouverture de session suivante)** : au-delà, le signal expire. La validation humaine devient un filtre, pas un entonnoir.
- **MAX_FACTOR_EXPOSURE = 20 % par facteur** — blé + maïs + soja comptent comme *un* facteur.
- **MAX_HOLDING_DAYS = 20** : sortie forcée en revue, pas de position zombie roulée à l'infini.
- **Échelle de dé-risking** : −5 % → taille ÷2 ; −7,5 % → flat-only ; −10 % → halt + cooldown 2 semaines + ré-entrée à 25 % de taille, +2,5 %/semaine si recovery. Et **MAX_WEEKLY_LOSS = −3,5 %** pour attraper les grappes de gaps que le journalier ne voit pas.
- **Garde-coût** : edge attendu ≥ 2 × (aller-retour + slippage estimé), sinon pas de trade. Avec données différées, le coût réel est structurellement supérieur à la moyenne.

On garde `−1,3 %/jour` (comme garde-fou souple) et `−10 % / −5 %` (comme mur dur et alerte) — mais ils cessent d'être l'ossature : ils deviennent la couche *basse* d'un système où le risque est d'abord borné par le stop, le FX et le facteur.

---

## 4) Verdict

Les trois paramètres proposés sont **directionnellement justes et dimensionnellement faux**. Ils raisonnent comme un portefeuille d'actions (notionnel continu, devise unique, pas de gap) appliqué à des futures levés, sur deux devises, avec des prix discontinus. `MAX_POSITION_SIZE = 20 %` est le maillon qui casse tout, non par excès de hardiesse affichée, mais par ambiguïté d'unité. La correction n'est pas de resserrer les chiffres : c'est de **changer la grandeur mesurée** (risque au stop, pas % de capital) et d'**ajouter les paramètres absents** (FX, blackout événementiel, expiration de signal, plafond de facteur, échelle de ré-entrée).

**VERDICT: AJUSTER — conserver −10 %/−5 % et −1,3 %/jour comme couches basses, mais remplacer MAX_POSITION_SIZE par RISK_PER_TRADE 0,5–1,0 % au stop + notionnel ≤15 %/contrat en micro-contrats, et ajouter 5 paramètres manquants : MAX_FX_EXPOSURE 25 %, EVENT_BLACKOUT T−48h/T+2h, MAX_SIGNAL_AGE 4 h, MAX_FACTOR_EXPOSURE 20 %, échelle de dé-risking/ré-entrée (−5 %→÷2, −7,5 %→flat, −10 %→cooldown 2 sem. + ré-entrée 25 %).**