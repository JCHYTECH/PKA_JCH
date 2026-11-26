JC,

**1. Verdict net — AJUSTER, pas adopter, pas rejeter.**

Le jeu de paramètres n'est pas « prudent » : il est **mal calibré dans ses unités**, et cette erreur produit exactement le résultat inverse de l'intention. En euros, `20 %/position` sur 50 k€ = 10 000 € de marge. Or un contrat plein de blé pèse 27 500 $ de notionnel, le maïs 21 500 $, le soja 52 500 $ (vérifié par calcul, pas de mémoire). Donc 20 % de capital en marge ≈ 100 k€ de notionnel à levier 10× → **2× le capital par position, 4× en brut avec deux positions**, pas 40 %. Conséquence : le `MAX_DRAWDOWN = −10 %` est atteint après **5 % de mouvement adverse** sur une exposition 2×. Le blé fait ça en une semaine de météo normale. Le système meurt de bruit avant d'avoir rencontré un seul choc.

**2. L'upside qu'on rate**

Chiffrage illustratif (pas un backtest) : espérance 0,925 R par trade avec une hypothèse 55 % / 2,5R / 1R. À R = 2 % d'equity et 7 trades/an → **13,7 %/an théorique**. Sous contrainte de conviction bridée + halt binaire en cluster, le réalisé atterrit plutôt à 6 %. Sur 3 ans à 50 k€ : 59 551 € vs 70 246 € — **~10 700 € d'écart**, et l'écart croît mécaniquement avec les tranches 10 k puis le graduel. Ce n'est pas le coût de la prudence : c'est le coût d'un plafond qui transforme une thèse à queue épaisse en rendement linéaire médiocre.

Le vrai upside raté est structurel, pas arithmétique : **les pertes d'un système event-driven sur les grains sont corrélées** (blé, maïs, soja = un seul facteur météo/mer Noire). Deux positions à 20 % ne sont pas deux paris, c'est un pari à 40 % déguisé en diversification. Et le halt dur à −10 % se déclenche précisément dans l'état où le cluster de pertes précède la queue qui paie. On a acheté de la convexité et on la revend au pire moment.

**3. Arguments**

- **Le stop est anti-corrélé au payoff.** En trading de chocs agricoles, les rendements viennent de 2-3 fenêtres par an (météo US juin-août, récolte Amérique du Sud janvier-mars, géopolitique mer Noire). Ces fenêtres concentrent aussi les drawdowns. Un halt binaire à −10 % éjecte le système exactement avant le scénario qu'il était positionné pour capturer.
- **Le plafond interdit d'exprimer la conviction.** Le seul avantage réel du projet — lire un choc que le marché price mal — ne vaut que s'il peut se traduire en taille asymétrique. Un sizing uniforme à 20 % dilue un signal 3R en signal 1,2R. C'est la façon classique de rendre bon un edge médiocre.
- **Options fermées par le paramétrage actuel :** pyramiding sur gagnant ; concentration en fenêtre événementielle ; une troisième position énergie non corrélée quand les grains sont saturés ; **long gamma via options sur futures** (payoff asymétrique, prime bornée, donc parfaitement compatible avec le −1,3 %/jour) ; redéploiement des gains en cours de saison ; échelle de dé-risking progressive.
- **Risque invisible non compté : le FX.** Futures CME en USD, capital en EUR, non hedgé. À 4× de brut, un mouvement de 1 % EUR/USD = 4 % d'equity. Ce risque n'apparaît nulle part dans les trois paramètres — et c'est aussi un flux de rendement non exploité.
- **Incohérence documentaire à trancher.** L'architecture existante (`docs/2026-06-04_checklist-lancement.md`, `phase1-ibkr-setup.md`) fixait `MAX_POSITION_SIZE = 5 %` et signalait déjà que les grains pleins sont intenables sur petit capital (ETF WEAT/CORN/SOYB ou micro-futures MCL/MGC au démarrage). Le 20 % proposé est 4× ce provisoire, sans changement d'unité explicite. C'est un saut non documenté.

**4. Recommandation concrète**

- **Garder** `MAX_DAILY_LOSS = −1,3 %/jour` (hors débat).
- **Remplacer le halt binaire par une échelle :** −5 % → taille ×0,75 ; −8 % → ×0,5 ; −12 % → ×0,25 + revue ; **−15 % halt dur**. On conserve l'optionalité de capter la queue après un cluster au lieu de sortir du jeu.
- **Changer l'unité de sizing :** risque-au-stop de **1,5-2 % d'equity** par trade (~750-1 000 € sur 50 k€), taille dérivée de l'ATR. Puis échelle de conviction **1,0× / 1,5× / 2,0×** ce risque de base — le plafond devient 4 % d'equity en risque sur l'idée la plus forte, ce qui est le vrai levier d'upside.
- **Remplacer « 20 %, max 2, brut 40 % » par :** risque simultané total ≤ 6 % d'equity ; notionnel brut ≤ 2× capital ; **plafond par facteur** — max 2 positions dans le même complexe (grains = 1), +1 position énergie seulement si corrélation < 0,5.
- **Fenêtre de choc :** autoriser 1,5× le brut normal pendant une fenêtre événementielle validée (WASDE, bulletin sécheresse, décision export), avec sortie pré-définie et expiration datée (~10 jours). Le moyen le moins coûteux de monétiser l'edge.
- **Long gamma :** budget 0,5-1 % d'equity/an en options sur futures autour des fenêtres. Risque défini, compatible avec le frein quotidien, capte exactement les chocs que le système sait lire.
- **Tranches 5 k → 10 k :** libérer sur performance validée (≥ 60 trades, Sharpe > 1, DD réalisé < 8 %), pas sur calendrier.
- **Compter le FX** soit par hedge EUR/USD, soit en l'intégrant au budget de risque.

VERDICT: AJUSTER — garder −1,3 %/jour, remplacer le halt −10 % par une échelle de dé-risking jusqu'à −15 %, remplacer le sizing « 20 %/position » par un budget de risque 1,5-2 %/trade × échelle de conviction, plafonner par facteur et non par nombre, et ouvrir la fenêtre de choc + le long gamma ; ces paramètres, en l'état, brident un edge à queue épaisse et meurent de bruit avant de le toucher.