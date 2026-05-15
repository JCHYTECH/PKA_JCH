---
tags:
  - type/project
  - status/active
---
# Dimensionnement système mécanique

**Created:** 2026-02-17 11:38  
**Updated:** 2026-02-17 11:50  
**Messages:** 10

---

## Human
*2026-02-17 11:38*

je veux faire du focus stacking en macrophotographie avec un rail motorisé. je veux utiliser un niais 200mm comme rail et faire moi meme l'ensemble moteur et commande moteur pour faire tourner la vis du niais. J'i besoin de tes competences électronique pour me dire quel contrôleur je dois utiliser pour faire tourner le moteur pas à pas de X tours avec une vitesse ajustable et répéter ce cycle X fois. si je complet dans ma question ou te manque t'il des trucs

---

## Assistant
*2026-02-17 11:38*

Il te manque quelques infos, mais on peut déjà cadrer une architecture “propre” et te dire quel contrôleur choisir selon ton niveau (simple/fiable vs programmable).

Ce que tu veux faire, en clair
1) Faire avancer un chariot sur un rail (Nisi 200 mm) en tournant une vis (lead screw) avec un moteur pas-à-pas.
2) Paramétrer : distance par pas (ou nombre de tours), vitesse, éventuellement rampes d’accélération.
3) Répéter : “avance → pause (pour vibrations) → déclenche photo” X fois.

Contrôleur conseillé (3 options, du plus simple au plus robuste)

Option A – La plus simple et très fiable : microcontrôleur + driver stepper “STEP/DIR”
- Contrôleur : Arduino Nano / Uno (ou un ESP32 si tu veux écran/Wi-Fi plus tard).
- Driver : TMC2209 (silencieux, micro-pas fins, très bon pour du stacking) ou DRV8825 (moins cher, plus bruyant).
- Avantages : tu maîtrises exactement “X pas, à telle vitesse”, tu peux faire une pause, gérer un déclencheur appareil, ajouter un écran/encodeur.
- Inconvénient : il faut un petit firmware (mais c’est assez standard).

Option B – “Industrial-ish” mais encore simple : contrôleur stepper autonome type “pulse generator”
- Un petit boîtier “stepper pulse generator” (sortie STEP/DIR) + driver type TB6600/DM542.
- Tu règles au panneau : nombre de pulses, fréquence (vitesse), sens, cycles.
- Avantages : pas de code.
- Inconvénients : souvent moins “photo friendly” (timings de pause/déclenchement), ergonomie variable selon modèles.

Option C – Si tu veux un truc déjà pensé pour le stacking (mais tu fais quand même ton rail) : contrôleur dédié slider/stacking
- Ex : cartes type “slider/stack controller” (souvent Arduino-based mais déjà intégrées avec écran + menus).
- Avantages : tout est déjà dans l’interface (pas, pause, nb de vues, déclenchement).
- Inconvénients : tu n’es plus 100% sur du “DIY pur”, et parfois fermé/moins flexible.

Si tu me dis “je veux le minimum de code”, je te pousse vers B/C. Si tu veux un outil propre, évolutif, et précis, je te pousse vers A (Arduino/ESP32 + TMC2209).

Architecture recommandée (celle que je ferais pour un rail macro)
- Moteur : NEMA 17 (1.8°) couple correct, ou NEMA 14 si tu es ultra léger. Pour un chariot + boîtier + objectif macro + flash, NEMA17 est généralement plus serein.
- Driver : TMC2209 (en UART si tu veux régler le courant finement, sinon en standalone).
- Alimentation : 12 V (souvent suffisant) ou 24 V si tu veux plus de marge en vitesse/ couple à haut régime (24 V améliore souvent la tenue en vitesse).
- Contrôle : Arduino Nano (simple) ou ESP32 (plus confortable si écran + encodeur + menus).
- Interface utilisateur : encodeur rotatif + écran OLED (0.96") ou écran LCD 16x2.
- Déclenchement caméra : optocoupleur ou transistor + jack (selon Canon/Nikon/Sony). L’idée : isoler électriquement l’appareil.

Le point critique en stacking : ce n’est pas “X tours”, c’est “X microns”
Tu peux commander en tours, mais en pratique tu veux : pas = (pitch de vis / (pas moteur par tour * microsteps)).

Exemple (hypothétique) :
- vis au pas de 1 mm / tour
- moteur 200 pas/tour
- microstep 16
→ 1 pas micro = 1 mm / (200*16) = 0,0003125 mm = 0,3125 µm.
Donc tu peux faire des pas très fins, mais attention : les micro-pas ne garantissent pas une précision absolue sous charge, ils garantissent une “résolution de commande”. Pour du stacking, ça marche très bien si la mécanique est fluide et sans jeu.

Ce qu’il me manque pour te donner un choix “sans hésitation” (et te calculer les pas)
1) Le type exact de “vis” dans ton rail Nisi : c’est quoi le pitch (mm/tour) ? (ou le modèle exact du rail pour retrouver la spec)
2) La charge : boîtier + objectif + support (ordre de grandeur en kg) + si c’est horizontal ou incliné.
3) L’amplitude : tu veux faire du stacking sur combien de mm typiquement ? 2 mm ? 20 mm ?
4) La granularité de pas souhaitée : tu vises quoi comme pas entre images (en µm) pour tes sujets habituels ?
5) Tu veux déclencher l’appareil depuis le contrôleur, oui/non ? (si oui, marque de boîtier et type de prise remote)
6) Alimentation : secteur possible ? batterie (powerbank/12V) ? usage terrain ?

Réponse directe à “quel contrôleur je dois utiliser ?”
Sans autre contrainte : Arduino Nano + TMC2209 + NEMA17 + alim 12 V (ou 24 V si tu veux plus de vitesse). C’est le meilleur compromis précision/bruit/souplesse pour du focus stacking DIY.

Et pour ta dernière question : oui, ta question est “complète” sur l’idée générale, mais il manque surtout (1) le pitch de la vis et (2) la charge/usage. Donne-moi ces deux infos, et je te sors une recommandation dimensionnée (moteur, courant driver, microsteps réalistes, vitesse max utile, et une logique de cycle complète avec temps de pause + déclenchement).  
Il est 12:00 à Bruxelles.

---

## Human
*2026-02-17 11:44*

la charge sera de 2 kg environ

---

## Assistant
*2026-02-17 11:44*

Parfait. Avec 2 kg on peut dimensionner proprement le système sans tomber dans le surdimensionné inutile.

Je vais raisonner en mécanique pure, puis en électronique.

1. Hypothèses mécaniques (à confirmer)

Il me manque encore une donnée essentielle : le pas de la vis du rail Nisi 200 mm (mm par tour).  
Sur ce type de rail macro manuel, on est souvent autour de 1 mm / tour (parfois 0,8 mm ou 1,25 mm).

Je vais faire les calculs avec 1 mm / tour pour te donner un ordre de grandeur. Tu me confirmeras.

Configuration :
- Charge : 2 kg
- Montage horizontal (j’assume horizontal, dis-moi si incliné)
- Rail à vis trapézoïdale ou fine

Force gravitationnelle :  
F = 2 kg × 9,81 ≈ 19,6 N

En horizontal, ce n’est pas la gravité qui est dominante mais le frottement.  
Même avec un rail pas parfait, on est rarement au-dessus de 10–20 N équivalents.

Couple nécessaire (approximation)

Formule simplifiée pour vis sans fin :

T ≈ (F × p) / (2π × η)

où :
- F = force axiale
- p = pas (m)
- η = rendement (0,3 à 0,7 selon qualité)

Avec :
F = 20 N  
p = 0,001 m (1 mm)  
η ≈ 0,4 (valeur prudente)

T ≈ (20 × 0,001) / (2π × 0,4)  
T ≈ 0,02 / 2,51  
T ≈ 0,008 Nm

Même en multipliant par 5 pour sécurité, on est autour de 0,04 Nm.

Un NEMA17 classique fournit 0,4 à 0,6 Nm.

Conclusion mécanique :
Un NEMA17 est largement suffisant pour 2 kg sur un rail horizontal.  
Tu as une marge énorme, ce qui est bon pour travailler en micro-pas stable.

2. Choix moteur recommandé

Je te conseille :

NEMA 17  
- 1.8° (200 pas / tour)  
- 40 mm longueur  
- Couple nominal 0,45 Nm environ  
- Courant 1,5–1,7 A

Pas besoin d’un moteur 60 mm long. Trop inertiel pour ton usage.

3. Driver recommandé

Je te conseille clairement :

TMC2209

Pourquoi :
- Micro-pas jusqu’à 1/256
- Fonctionnement très fluide
- Silencieux
- Moins de vibrations que DRV8825
- Réglage du courant précis

Pour du focus stacking macro, la fluidité est plus importante que la puissance brute.

4. Résolution obtenue (si pas = 1 mm)

Moteur 200 pas / tour  
Micro-pas 16 (suffisant et stable)  
Donc 200 × 16 = 3200 micro-pas / tour

1 mm / 3200 = 0,0003125 mm = 0,3125 µm par micro-pas

Attention :
La résolution théorique n’est pas la précision réelle.
En pratique, la répétabilité utile sera plutôt de 2 à 5 µm.

Ce qui est parfait pour du stacking macro.

5. Contrôleur conseillé

Arduino Nano + TMC2209

Architecture :

Arduino  
→ STEP  
→ DIR  
→ ENABLE  
→ sortie déclencheur appareil (optocoupleur)

Ce que tu pourras programmer :

- Nombre de pas par image
- Vitesse de déplacement
- Temps de pause après mouvement (anti-vibration)
- Nombre total d’images
- Retour automatique en position initiale

Logique de cycle idéale pour stacking :

Pour i = 1 à X  
  - Déplacement N pas  
  - Attente 200–500 ms  
  - Déclenchement  
  - Attente temps d’exposition  
Fin

6. Vitesse recommandée

Pour du stacking macro, tu ne veux PAS aller vite.

Je recommande :
- 0,1 à 0,5 mm/s max
- Accélération douce (rampes obligatoires)

Bibliothèque Arduino idéale :
AccelStepper

Elle gère :
- rampes d’accélération
- mouvements précis en nombre de pas
- contrôle propre du timing

7. Alimentation

12 V 3 A est suffisant.

Si tu veux plus de confort :
24 V améliore la stabilité des micro-pas et la tenue à vitesse plus élevée.

Mais pour ton usage macro lent, 12 V suffit.

8. Points critiques à ne pas négliger

- Couplage moteur → vis : utiliser un accouplement flexible
- Supprimer le jeu axial
- Rail parfaitement aligné
- Base rigide (vibrations = ennemi du stacking)
- Désactiver le moteur après mouvement pour éviter résonance si nécessaire

9. Ce qu’il me manque encore

- Le pas exact de la vis du Nisi
- Orientation : toujours horizontal ?
- Tu veux déclenchement automatique du boîtier ? (quel modèle ?)
- Tu veux interface simple (3 boutons) ou écran + encodeur ?

Donne-moi le pas de la vis et je te fais :
- calcul exact des pas par micron
- configuration micro-pas optimale
- courant à régler sur le TMC2209
- architecture électrique complète

Il est 12:08 à Bruxelles.

---

## Human
*2026-02-17 11:45*

1 mm par tour

---

## Assistant
*2026-02-17 11:45*

Parfait : 1 mm/tour, c’est idéal. Avec ça on peut fixer une base “mécatronique” très propre.

Avec un moteur 1.8° (200 pas/tour) :

En micro-pas 16 (mon choix par défaut pour la stabilité en charge)  
200 × 16 = 3200 micro-pas / tour  
Donc 1 mm / 3200 = 0,0003125 mm = 0,3125 µm par micro-pas

Conversions utiles (micro-pas 16)
- 1 µm = 3,2 micro-pas
- 5 µm = 16 micro-pas
- 10 µm = 32 micro-pas
- 20 µm = 64 micro-pas
- 50 µm = 160 micro-pas
- 100 µm = 320 micro-pas

En pratique, je te conseille de travailler par pas “ronds” en micro-pas, typiquement 16, 32, 64, 80, 96, 128… selon le rapport de grandissement.

Le contrôleur que je te recommande (choix “sans regret”)
1) Arduino Nano (ou Pro Mini 5V si tu veux compact)  
2) Driver TMC2209 (en STEP/DIR; UART optionnel)  
3) Moteur NEMA17 40 mm, ~0,45 Nm, 1.5–1.7 A nominal  
4) Alimentation 12 V 3 A (ou 24 V 2–3 A si tu veux plus de marge, mais pas obligatoire en macro lente)

Pourquoi TMC2209 : très fluide, micro-pas propres, moins de vibrations = meilleure netteté, surtout à fort grandissement.

Ce que ton système doit savoir faire (et comment)
Entrées réglables :
- StepSize (en µm ou en micro-pas)
- Speed (micro-pas/s ou mm/s)
- PauseAfterMove (ms) pour amortir vibrations
- Shots (X, nombre d’images)
- (option) ReturnHome

Cycle typique stacking :
Pour i = 1..X
- Avancer de N micro-pas
- Pause 200–600 ms
- Déclenchement boîtier (contact “focus/shutter” ou shutter direct)
- Attendre la fin de pose + recyclage flash si flash

Réglages de départ (qui marchent bien)
- Micro-pas : 16
- Vitesse déplacement : 0,2 mm/s (donc 0,2 tour/s = 640 micro-pas/s)
- Accélération : faible (rampes indispensables)
- Pause anti-vibration : 300 ms (plus si tu es sur trépied léger)
- Step size : 10 µm (32 micro-pas) pour macro “standard”; 5 µm (16 micro-pas) si très fort grossissement

Électronique pratique : câblage minimal
- Arduino → TMC2209 : STEP, DIR, EN
- Alim 12 V → VMOT du driver + GND
- Condensateur près du driver (ex: 100 µF à 470 µF) entre VMOT et GND (important)
- Moteur 4 fils → A1/A2/B1/B2
- Déclenchement boîtier : optocoupleur (recommandé) ou transistor + jack, pour isolation galvanique

Le seul point où je ne veux pas deviner
Le déclenchement dépend de ton boîtier (Canon R10/90D par exemple) et du type de prise télécommande. Dis-moi simplement : tu veux déclencher comment ?
- via prise remote (jack) : parfait, simple
- via USB : faisable mais plus complexe
- tu déclenches à la main : ok, mais tu perds l’automatisation

Si tu veux, je te donne ensuite une “liste d’achats” précise (références typiques de NEMA17, TMC2209, alim, optocoupleur, encodeur+OLED) + un schéma de principe, et surtout les formules intégrées (µm ↔ micro-pas) avec un exemple de table “macro 1:1 / 2:1 / 3:1”.

Il est 12:11 à Bruxelles.

---

## Human
*2026-02-17 11:46*

ok j'ai pas envie de trop passer du temps à developer je vais donc opter pour la solution C. que me conseille tu ?

---

## Assistant
*2026-02-17 11:46*

D’accord, si tu veux éviter de “développer”, la meilleure solution C (contrôleur dédié, prêt à l’emploi) pour piloter TON rail (vis 1 mm/tour) se joue sur deux critères : 1) est-ce qu’il sort directement du STEP/DIR pour driver un moteur pas à pas “standard”, 2) est-ce qu’il sait déclencher l’appareil (câble ou IR) et gérer les pauses.

Dans l’écosystème macro, trois familles ressortent clairement.

1) Le “standard” très éprouvé, mais plutôt conçu en kit rail+contrôleur : Cognisys StackShot
Le StackShot est une référence, avec un contrôleur autonome (boutons + afficheur) et déclenchement caméra. Il est donné pour des pas très fins (jusqu’à l’ordre du micron en mode haute précision) et une logique de stack complète. citeturn0search1turn0search7turn0search25  
Point important : c’est typiquement vendu en système complet rail+contrôleur. Si ton objectif est de réutiliser ton rail Nisi, ce n’est pas toujours le chemin le plus simple/économique, sauf si tu acceptes d’acheter le système StackShot et de ne plus utiliser le Nisi. citeturn0search1

2) Contrôleur “réutilisable sur rails DIY” : MJKZZ (contrôleurs et kits)
MJKZZ vend des contrôleurs et des solutions orientées focus stacking, et ils indiquent explicitement que certains contrôleurs/solutions sont conçus pour leurs rails mais aussi pour d’autres projets/rails DIY (motion control). citeturn0search27turn0search5  
Avantage : c’est plus dans l’esprit “je garde mon rail, j’ajoute un moteur et un boîtier de contrôle” que StackShot.  
Inconvénient : il faut vérifier la compatibilité exacte côté moteur/driver (certains systèmes sont pensés comme un ensemble MJKZZ). Leur boutique montre des kits “rail + contrôleur IR/Wi-Fi/USB”, mais tu peux aussi partir sur leur contrôleur dédié si tu veux rester en DIY mécanique. citeturn0search2turn0search27

3) Contrôle via smartphone/PC (très peu de mise au point “dev”, mais moins autonome) : WeMacro
WeMacro est piloté via téléphone/ordinateur (Bluetooth) et annonce des pas très fins (jusqu’à 1 µm en mode précis) avec outils logiciels. citeturn0search12turn0search22  
Mais : c’est principalement un rail complet de leur écosystème. Si tu veux absolument ton Nisi, WeMacro est moins “plug-and-play” en réutilisation de mécanique.

Ce que je te conseille concrètement, en restant fidèle à ton cahier des charges (zéro dev, tu gardes le rail Nisi)
Option C la plus cohérente : partir sur un contrôleur qui sort du STEP/DIR et qui a un mode “stacking” (déplacement par pas + pause + déclenchement, répétition X fois).

Dans ce cadre, je te recommande de regarder en priorité :
A) Un contrôleur MJKZZ orienté DIY/rail externe (IR/Wi-Fi/USB selon ta préférence), parce qu’ils positionnent explicitement leur contrôleur comme utilisable sur d’autres projets DIY. citeturn0search27turn0search5  
B) Si tu acceptes de ne pas réutiliser le Nisi : StackShot (solution la plus “pro” et éprouvée, mais c’est un autre rail). citeturn0search1turn0search7turn0search25

Décision rapide (sans te renvoyer 15 questions)
1) Tu veux impérativement rester autonome sans PC/téléphone pendant la prise de vue → vise un contrôleur autonome type StackShot (mais alors plutôt en système complet) ou un contrôleur dédié DIY avec interface propre (MJKZZ/équivalent). citeturn0search7turn0search27  
2) Tu acceptes de piloter au smartphone/PC → WeMacro est très simple à l’usage, mais ça t’emmène vers leur écosystème rail. citeturn0search12

Deux questions qui changent tout (et je te donne ensuite un choix “final” + schéma de câblage sans dev)
1) Tu veux déclencher ton Canon (R10/90D) depuis le contrôleur via câble (idéal) ou tu t’en fiches (tu déclenches à la main / intervalomètre) ?  
2) Tu veux un système 100% autonome sur le terrain (sans PC/smartphone) ?

Si tu me réponds juste “câble oui/non” et “autonome oui/non”, je te donne une recommandation unique (produit/famille), et je te liste exactement : moteur NEMA17 à prendre, type de driver si requis, alim, câbles, et comment intégrer ça proprement sur la vis 1 mm/tour.

Il est 12:18 à Bruxelles.

---

## Human
*2026-02-17 11:49*

uhmmm . j'hésite pour la solution A es tu en mesure de faire une liste d'achat y compris déclenchement de mon 90D ou R10

---

## Assistant
*2026-02-17 11:49*

Oui. Si tu reviens vers la solution A (Arduino + driver), je peux te faire une liste d’achat cohérente, simple, sans exotisme, adaptée à ton Canon 90D et R10.

Je te propose une architecture robuste, stable et suffisamment “propre” pour du stacking macro sérieux, sans surcomplexité.

Configuration retenue

- Rail : Nisi, vis 1 mm / tour  
- Charge : 2 kg  
- Usage : stacking macro précis  
- Déclenchement : via prise télécommande Canon (pas USB)

────────────────────────
LISTE D’ACHAT RECOMMANDÉE
────────────────────────

1) Moteur pas à pas

Type : NEMA 17  
Spécifications conseillées :
- 1.8° (200 pas / tour)
- 40 mm de longueur
- Couple ~0,45 Nm
- Courant nominal 1,5 à 1,7 A
- Arbre 5 mm

C’est largement suffisant pour 2 kg sur rail horizontal.

────────────────────────

2) Driver moteur

Modèle recommandé : TMC2209

Pourquoi :
- Mouvement très fluide
- Micro-pas fins
- Moins de vibrations que DRV8825
- Idéal macro

Version simple (mode STEP/DIR sans UART) suffit.

Prévoir :
- Radiateur pour le driver
- Condensateur 100 à 470 µF entre VMOT et GND (obligatoire)

────────────────────────

3) Contrôleur

Arduino Nano (ATmega328P, version classique 5V)

Pourquoi :
- Compact
- Ultra documenté
- Stable
- Suffisant pour ton usage

Alternative plus moderne : ESP32 (si un jour tu veux WiFi/écran tactile), mais Nano suffit.

────────────────────────

4) Interface utilisateur (simple et efficace)

- 1 écran OLED 0.96” I2C (SSD1306)
- 1 encodeur rotatif avec bouton intégré
- 1 bouton Start/Stop
- 1 bouton Home (optionnel)

Cela permet :
- Réglage du pas en µm
- Réglage vitesse
- Nombre d’images
- Pause anti-vibration

────────────────────────

5) Déclenchement Canon 90D / R10

Les deux utilisent une prise télécommande Canon type E3 (jack 2.5 mm).

Il te faut :

- 1 câble télécommande Canon E3 vers jack 2.5 mm
- 1 optocoupleur PC817 (ou équivalent)
- 1 résistance 220–330 Ω côté Arduino
- 1 transistor ou second optocoupleur si tu veux gérer focus + shutter séparément

Le schéma simple :

Arduino → résistance → LED interne optocoupleur  
Sortie optocoupleur → court-circuite shutter à GND

Avantage :
Isolation électrique complète entre rail et boîtier.

C’est important pour protéger ton 90D / R10.

────────────────────────

6) Alimentation

Alimentation 12 V 3 A (minimum)

Option terrain :
- Batterie 12 V LiFePO4
- Ou convertisseur boost depuis powerbank USB-C PD

Le TMC2209 fonctionnera très bien en 12 V pour ton usage lent.

────────────────────────

7) Couplage mécanique

- Accouplement flexible 5 mm → diamètre vis rail
- Support moteur (à fabriquer ou acheter universel NEMA17 bracket)
- Visserie M3 pour moteur

Important :
Accouplement flexible pour absorber les micro-défauts d’alignement.

────────────────────────

8) Divers indispensable

- Plaque d’expérimentation ou PCB prototypage
- Boîtier pour l’électronique
- Câbles Dupont
- Interrupteur général
- Fusible 2–3 A

────────────────────────
RÉGLAGES CONSEILLÉS AU DÉPART
────────────────────────

Micro-pas : 16  
Vitesse : 0,2 mm/s  
Pause après mouvement : 300 ms  
Pas macro 1:1 : 10 µm (32 micro-pas)  
Pas macro fort grossissement : 5 µm (16 micro-pas)

────────────────────────
Ce que je peux te fournir ensuite
────────────────────────

Si tu veux continuer :

1) Schéma de câblage clair (moteur + driver + Arduino + Canon)
2) Code Arduino prêt à charger (avec AccelStepper)
3) Table µm ↔ micro-pas pour ton rail 1 mm/tour
4) Recommandation de courant exact à régler sur le TMC2209
5) Option “retour automatique en position initiale”

Dis-moi :

– Tu veux un système minimaliste (3 boutons, pas d’écran)  
ou  
– Interface confortable avec écran OLED ?

Et confirmes-moi : tu déclenches bien via prise E3 sur le 90D/R10 ?

Il est 12:25 à Bruxelles.

---
