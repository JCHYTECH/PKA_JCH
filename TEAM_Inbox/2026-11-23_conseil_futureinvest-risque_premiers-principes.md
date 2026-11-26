JC,

## 1. Verdict net

**Ajuster, pas adopter telle quelle.** Les seuils 1 et 2 (perte journalière, drawdown) sont des garde-fous défensifs corrects — mais seulement *si* on les raccorde à un risque par trade de 0,5 %. Le seuil 3 (20 %/position, 2 positions, 40 % brut) est **inopérant dans le monde réel des futures** : il exprime une intention en pourcentage de capital, alors que l'unité indivisible d'un future est le *contrat*, dont le notionnel est un quantum fixe de 13 % à 130 % de ton equity. Tu ne peux pas doser à 20 % quand le plus petit pas fait 40 %, 52 % ou 129 %.

Autrement dit : **le cadrage mesure la bonne intention avec la mauvaise unité.** Ce n'est pas un problème de calibration de valeurs, c'est un problème de dimension physique. Un drawdown en % et une taille en % de notionnel décrivent un portefeuille d'actions ; un portefeuille de futures se décrit en **risque en euros au stop, en stress-loss par contrat, en marge immobilisée, et en exposition à des facteurs corrélés**.

## 2. Le VRAI risque à mesurer

Le risque qui tue un compte de futures n'est presque jamais « -10 % », c'est la **ruine par la trajectoire** — être liquidé sur un chemin, même si la direction finale était bonne. Les cinq vraies variables, aucune n'étant dans tes trois paramètres :

- **Le quantum de contrat.** Un contrat de blé CBOT ≈ 25 800 € de notionnel ; un limit-move de 40 ¢ = 1 840 €, soit **36,8 % de ta première tranche de 5 000 €**. Un seul jour de limite peut consommer trois fois ton budget de drawdown. À 50 000 €, le même limit-move ne coûte que 3,7 % — le paramètre change de nature avec la taille du capital, ce qu'un % fixe masque.
- **Le stress-loss, pas le stop.** Un stop ne remplit pas à son prix : limite journalière, gap d'ouverture, slippage. Le risque réel d'une position est *perte sous limit-move + gap + slippage + FX*, pas la distance du stop.
- **La marge et le buffer de variation.** À 5 000 €, la marge initiale d'un contrat de maïs ≈ 1 930 € (38,6 %), blé 55 %, soja 83 %, WTI 129 %. Deux positions à 5 000 € sont mathématiquement impossibles sans dépasser 100 % de marge. Le vrai plafond n'est pas « 20 % de notionnel », c'est « marge initiale ≤ 25 % et buffer ≥ 3× le stress-loss du portefeuille ».
- **La corrélation intra-complexe.** Blé/maïs/soja corrèlent 0,6–0,85 en régime normal, et convergent vers 1 en stress (sécheresse 2012, guerre 2022). « 2 positions » dans les céréales = **un seul pari à 40 %**, pas deux paris à 20 %. La diversification se mesure sur facteurs (complexe céréalier, beta USD, beta énergie), pas sur le nombre de lignes.
- **L'asymétrie d'exécution propre à ton profil.** Swing 1–4 semaines, données différées, validation humaine < 1 h/jour : tu traverses *par construction* des événements binaires connus (WASDE, acreage, OPEC). Un stop ne protège pas à travers un rapport USDA. Et le risque dominant — **le signal a vieilli avant exécution** — n'est mesuré par aucun des trois paramètres.

Il y a un faux objectif explicite : **optimiser des pourcentages de tableau de bord pour un moteur dont la contrainte limitante est ailleurs** (granularité, marge, corrélation, calendrier d'événements, latence de décision).

## 3. Arguments

**a) La granularité invalide le seuil 3.** Notionnels à 50 000 € d'equity : maïs 40 %, blé 52 %, soja 97 %, WTI 129 %, micro-WTI 13 %. Avec un plafond de 20 %/position, **seul le micro-WTI est tradable**. À la tranche de 5 000 €, *aucun* contrat agricole n'est tradable à un risque sensé. Le paramètre n'est donc pas « mal calibré » : il est soit inapplicable, soit, s'il est lu comme une marge, il autorise 4–5× de levier déguisé. L'ambiguïté d'unité *est* le bug.

**b) Les seuils 1 et 2 sont cohérents — mais seulement ensemble et avec R = 0,5 %.** Avec R (risque/trade) = 0,5 % : -10 % de drawdown = **20R** (vraie invalidation de process, pas du bruit), -1,3 %/jour = **2,6R** (les deux positions stoppées + slippage). C'est un jeu cohérent. Avec R = 1 %, le drawdown ne vaut plus que 10R : trop serré, il coupe un système positif sur du bruit. Donc **ne pas figer les trois nombres séparément : les calibrer comme un triplet (R, daily, DD) = (0,5 %, 2,6R, 20R)**.

**c) Mais R = 0,5 % est inatteignable sur les agricoles à petite taille.** R = 0,5 % de 5 000 € = 25 €. Le risque minimum d'un contrat de maïs même avec un stop à 1 % est ≈ 198 €, soit 4 % de la tranche. Pour tenir 25 €, il faudrait un stop à 0,125 % — à l'intérieur du bruit quotidien, touché mécaniquement. **La granularité force un risque par trade de 4 à 8 % sur les céréales à 5 000 €.** C'est précisément ce que le paramètre « 20 % » prétendait empêcher.

**d) Le drawdown est un indicateur retardé, pas un contrôle.** Il constate la perte, il ne la prévient pas. Le contrôle qui prévient, c'est le stress-loss par position et le buffer de marge. Garde le -10 % comme **disjoncteur de gouvernance**, pas comme outil de gestion.

**e) Le risque FX est absent.** P&L en USD, equity en EUR : +1 % d'EUR/USD sur 50 000 € de notionnel = 500 € = 1 % de l'equity. C'est un facteur de risque non couvert que ni le drawdown ni la taille en % ne voient.

## 4. Recommandation concrète

**Adopter** le seuil 1 (-1,3 %/jour), en le définissant comme 2,6R avec R = 0,5 % de l'equity *déployée* (pas du capital total).
**Adopter** le seuil 2 (-10 % dur) comme disjoncteur, avec palier intermédiaire : **-5 % = gel des nouvelles entrées + audit de validité du process** (pas une simple alerte), reprise conditionnée à revalidation. Et faire évoluer le seuil avec la tranche : -10 % de 5 000 € = 500 €, ce n'est pas -10 % de 50 000 € = 5 000 € ; le drawdown se mesure sur le **capital engagé**.
**Rejeter** le seuil 3 dans sa forme actuelle. Le remplacer par cinq contraintes en euros :

1. **Risque au stop ≤ 0,5 %** de l'equity par position (0,75 % après 30 trades live validés ; jamais > 1 %).
2. **Stress-loss ≤ 2 %** de l'equity par position, sous scénario *limit-move + gap + slippage + FX*, recalculé à chaque roll.
3. **Marge initiale totale ≤ 25 %** de l'equity ; **buffer de variation ≥ 3×** le stress-loss agrégé du portefeuille.
4. **Un seul pari par complexe** (céréales / énergie) ; stress-loss agrégé ≤ 3 % de l'equity.
5. **Exposition USD non couverte ≤ 50 %** de l'equity (ou hedge systématique dès la tranche 2).

Puis la règle qui rend le tout exécutable :
`contrats = floor( (R × equity) / (distance_stop × valeur_du_point) )` — **si le résultat < 1, le marché n'est pas tradable à cette taille ; on ne trade pas.**
Conséquence assumée : à 5 000 €, l'univers se réduit au **micro-WTI (MCL)** — marge ~13 %, stress-loss ~6,4 % de la tranche (encore trop : il faut descendre à 2 % en réduisant la durée de portage ou en attendant une tranche plus grosse). Les agricoles ne deviennent viables qu'autour de **30–50 k€** (1 contrat, stress 1–4 %). Deux options honnêtes : **relever la tranche 1 à 20–25 k€**, ou **assumer que les tranches 1–2 sont un laboratoire sur micro-énergie uniquement** et n'ouvrir les céréales qu'à la tranche 3.

Enfin, deux garde-fous manquants, non négociables :
- **Calendrier d'événements** : aucune entrée 24 h avant WASDE/USDA, 48 h avant OPEC ; taille divisée par deux avant un binaire connu ; aucune position dont le stress-loss > 2 % traverse un rapport.
- **Fraîcheur du signal** : âge maximal du signal à l'exécution (ex. ≤ 30 min pour l'entrée, ≤ 4 h pour la validation humaine), sinon on saute. C'est le vrai risque de « données différées », et aucun pourcentage de drawdown ne le mesure.

VERDICT: AJUSTER — adopter les seuils 1 et 2 *comme triplet cohérent avec R = 0,5 %*, rejeter le seuil 3 (inopérant sous la granularité des contrats), et le remplacer par un budget de risque en euros : risque-au-stop, stress-loss, marge+buffer, corrélation par complexe, exposition FX — avec la règle « < 1 contrat calculable ⇒ marché non tradable à cette taille ».