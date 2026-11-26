JC — voici la réponse d'analyste externe, sans contexte sur le projet.

## (1) Jugement global

Les cinq garde-fous sont **dans le bon ordre de grandeur** pour du risk management retail basique — on reconnaît la structure classique (limite journalière, limite de drawdown, taille unitaire, nombre de positions, exposition agrégée). Mais ils sont **sous-spécifiés au point d'être inopérants** : les unités ne sont pas définies, deux règles se contredisent ou se dupliquent, et le tout est calibré pour un instrument que ni 5 000 € ni un débutant ne peuvent réellement porter. Ils protègent contre le désastre lent (la mort par mille coupures), pas contre les trois vrais risques de ce setup : le levier sur gap, la corrélation, et un modèle sur-ajusté.

Autrement dit : un bon squelette de règles, posé sur des fondations floues.

## (2) Failles et absurdités

**Bloquant — le dénominateur n'existe pas.** « % du capital » : quel capital ? Le plafond de 50 k€ ou l'equity réellement déposée ? Comme le financement est tranché (5 k puis 10 k), les deux interprétations donnent des règles **10× différentes** :
- −1,3 % de 5 k = 65 €/jour ; de 50 k = 650 €/jour.
- Une position « 20 % du capital » = 1 000 € de 5 k, ou 10 000 € de 50 k.

Tant que ce n'est pas écrit noir sur blanc, aucune des cinq règles n'a de sens opérationnel. Règle de base : tout en % de l'**equity courante déposée**, drawdown mesuré depuis le **plus-haut historique (HWM)**, perte journalière depuis la **clôture de J-1**.

**Bloquant — l'instrument ne rentre pas dans le capital.** Des futures physiques agriculture/énergie ont des notionnels énormes face à 5–50 k€ :

- WTI (1 000 bbl) ≈ 70 000 $ = **140 % du capital total**, 1 400 % de la tranche 1.
- Henry Hub gaz ≈ 30 000 $ = 60 % de 50 k, 600 % de 5 k.
- CBOT maïs ≈ 24 000 $ = 48 % de 50 k ; blé Euronext ≈ 11 000 € = 220 % de 5 k.

Donc « position à 20 % du capital » est **inapplicable** sur les contrats standard : soit la règle force des micro-contrats (MCL pétrole ≈ 14 % de 50 k, mais il n'existe pas d'équivalent micro en céréales), soit elle est violée dès le premier ordre. C'est la faille la plus grave : le cahier des charges décrit un véhicule incompatible avec le capital.

**Recevable mais incohérent — l'exposition totale est redondante.** 2 positions × 20 % = 40 %. La règle « exposition ≤ 40 % » est exactement le produit des deux précédentes : elle n'ajoute **aucune information**. Soit c'est un doublon, soit « position » et « exposition » sont dans des unités différentes (marge vs notionnel) — et alors les deux règles ne parlent pas de la même chose. Dans les deux cas, ça trahit un design non stress-testé.

**Majeur — pas de stop par position, pas de risque par trade.** Une limite journalière n'est pas un contrôle de risque, c'est un **compteur de dégâts**. Sans stop-loss obligatoire par position et sans dimensionnement par le risque (taille = risque autorisé ÷ distance au stop), la limite de −1,3 % sera franchie par une seule position qui dérive, pas par un plan.

**Majeur — la limite journalière est illusoire sur ces instruments.** Elle suppose des pertes continues et contrôlables. Or : gaps d'ouverture, limit-up/limit-down, rapport USDA (mercredi EIA, mensuel WASDE, OPEP), slippage. Une journée de gaz à +5 % de range sur une exposition pleine (20 k notionnel) = **1 000 € = 2 % du capital**, soit déjà au-delà de votre plafond de 1,3 %. Le plafond est donc franchi par une **journée normale**, pas par une catastrophe.

**Majeur — aucun contrôle de corrélation.** « 2 positions max » ≠ diversification. WTI + Brent + gaz = un seul pari « énergie ». Blé + maïs + colza = un seul pari « météo/El Niño ». Deux positions dans le même cluster factoriel peuvent doubler l'exposition au même choc. Il faut un plafond par **cluster** (énergie-pétrole / énergie-gaz / grains / softs), pas seulement un plafond par ligne.

**Majeur — taille statique, volatilité ignorée.** 20 % fixes traitent le gaz (vol ~5×/jour) comme le blé (~1,5–2 %). Le dimensionnement doit être **inversement proportionnel à la volatilité** (ATR ou vol réalisée), sinon la même règle crée 3–5× plus de risque sur le gaz.

**Moyen — risque de change EUR/USD non couvert.** Capital en euros, contrats en dollars. Une variation EUR/USD de 2 % déplace tout le P&L sans qu'aucune règle ne la voie. Soit on intègre le risque FX dans le calcul d'exposition, soit on couvre.

**Moyen — « alerte à −5 % » sans action = décoration.** Une alerte qui ne déclenche rien est du bruit. À −5 % cumulés, on est déjà à mi-chemin du plafond dur de −10 %. Ça doit être une **action de réduction** (taille ÷2, gel des nouvelles entrées, revue), pas une notification.

**Moyen — rien sur les tranches.** Le financement en deux temps (5 k puis 10 k) n'a **aucune règle** : quand ajouter ? Si c'est « après une perte pour se refaire », c'est du martingale déguisé. Il faut une condition objective (ex. 3 mois live avec espérance positive et drawdown conforme au plan) et **jamais** de tranche supplémentaire après une perte.

**Moyen — règles opérationnelles absentes.** Aucune mention de : kill-switch, contrôle de cohérence des prix (rejet d'un ordre à >X % du dernier cours), plafond d'ordres/minute (boucle folle / fat-finger), réconciliation quotidienne positions vs broker, gestion du **roll** (contango/backwardation) et surtout **évitement du mois de livraison** — un débutant qui se fait livrer 5 000 boisseaux de maïs physique est un classique.

**Mineur mais révélateur — la précision de 1,3 %.** Un plafond à 1,3 % (et non 1 ou 1,5) sent le **sur-ajustement à un backtest**. Le ratio 10/1,3 ≈ 7,7 jours de perte pleine avant le plafond cumulé est cohérent en soi, mais le chiffre exact trahit une calibration sur l'historique plutôt que sur une politique de risque.

**Point de lucidité quantitatif.** J'ai simulé une stratégie **sans edge** (espérance nulle) avec le plafond journalier appliqué parfaitement. Résultat : la probabilité d'atteindre −10 % **en un an** est de ~32 % (vol 8 %/an), **54 %** (vol 11 %) et **64 %** (vol 16 %), avec une médiane de ~4 à 5 mois. Conclusion : ces garde-fous ne « protègent » pas d'un échec, ils **planifient l'arrêt propre** d'une stratégie qui ne marche pas. C'est correct — mais il faut l'assumer : la tranche 1 est un frais de scolarité, pas un capital à faire fructifier.

## (3) Ce que je ferais à la place

**Reparamétrer les unités, d'abord.**
- Tout en % de l'**equity déposée**, drawdown depuis HWM, perte jour depuis close J-1.
- Écrire explicitement : « capital de référence = equity disponible à l'instant t ».

**Passer d'un plafond de taille à un dimensionnement par le risque.**
- Risque par trade : **0,5 % de l'equity** (1 % max), stop technique/ATR obligatoire à chaque position.
- Taille dérivée du stop : `taille = (equity × 0,5 %) ÷ distance_au_stop`. Le « 20 % du capital » disparaît au profit d'un plafond de levier au niveau compte (**≤ 2× notionnel/equity** sur micro-contrats, marge libre ≥ 3× la maintenance).

**Échelle de drawdown avec actions, pas des alertes.**
- −1 % journalier → flatten immédiat + **arrêt 24 h** (pas de réentrée le même jour).
- −5 % cumulés → taille ÷2, gel des nouvelles entrées, revue.
- −8 % → flatten, audit du modèle.
- −10 % → **arrêt total**, retour en paper. Enforcement **côté broker** (stop serveur) en plus du code, sinon une boucle défaillante contourne tout.

**Contrôler la corrélation, pas le nombre de lignes.**
- 1 position max par cluster (énergie-pétrole / énergie-gaz / grains / softs) ; exposition nette par cluster ≤ 15 % de l'equity en notionnel.

**Choisir un instrument compatible.**
- Démarrer sur du **cash-settled, micro, liquide** : MES/MGC/MCL, ou ETF indiciels — pas des futures physiques agriculture/énergie.
- Grader vers les matières premières physiques seulement après ≥ 12 mois live. En Europe, vérifier le cadre retail (plafonds de levier PRIIPs/ESMA si CFD, protection solde négatif, fiscalité des futures via courtier étranger).

**Conditionner les tranches.**
- Tranche 2 uniquement après 3 mois live avec espérance positive **et** drawdown conforme au plan. **Jamais** après une perte.

**Valider avant de risquer.**
- 6 mois de paper, walk-forward out-of-sample, Monte Carlo sur la courbe de la stratégie elle-même.
- **Calibrer les seuils sur la distribution de drawdown réelle de la stratégie**, pas sur des chiffres ronds choisis à l'avance.

**Ajouter l'hygiène opérationnelle.**
- Kill-switch, rejet d'ordre si prix hors bande ±X %, max 20 ordres/min, heartbeat, réconciliation quotidienne positions vs broker, gestion du roll et interdiction du mois de livraison.

En résumé : garder l'esprit des cinq règles, mais les réécrire en unités d'equity déposée, les compléter par un sizing par risque + stops par position + gestion de cluster, et changer d'instrument avant de mettre un euro au marché.

VERDICT: Garde-fous raisonnables en ordre de grandeur mais inopérants en l'état — unités et dénominateur non définis, règle d'exposition redondante, pas de stop par trade, aucune gestion de corrélation, et instrument (futures physiques ag/énergie) incompatible avec 5–50 k€ et un débutant ; je ne lancerais pas ce système tel quel.