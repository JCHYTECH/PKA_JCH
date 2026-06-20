# Voici le document de synthèse complet qui récapitule l'intégralité…

> Exporté depuis Apple Notes — créé le ?, modifié le 2026-05-30 15:51

�f�f�0Voici le document de synthèse complet qui récapitule l'intégralité de notre échange technique et de vos idées de projet pour votre Stylevan Origin Equinox 4 sur porteur Ford Transit Custom.
Vous pouvez le copier-coller pour conserver une [[trace]] écrite et structurée de votre future installation.



📑 CAHIER TECHNIQUE & PROJET IOT : STYLEVAN EQUINOX 4
Ce document synthétise les données techniques de l'architecture électrique d'origine et la feuille de route pour l'intégration d'un système domotique Home Assistant connecté à l'écosystème Apple.



🛠️ PARTIE 1 : Architecture Électrique d'Origine
L'aménagement Stylevan Origin repose sur des composants haut de gamme standardisés, centralisés par le fabricant italien CBE.

1. Localisation des Éléments (Porteur Ford Custom)
Contrairement aux versions sur d'autres porteurs, l'espace sous les sièges avant du Ford Custom est occupé par les batteries du véhicule.
Boîtier CBE DS300 & Disjoncteurs : Situés en partie basse du meuble central (sous le bloc cuisine/glacière), accessibles via une trappe technique amovible munie d'une grille d'aération.
Batterie Cellule : Batterie Lithium LiFePO4 de 150 Ah (sur versions récentes) installée au sol au centre du véhicule.

2. Le Cerveau Électrique : CBE DS300
Le boîtier DS300 centralise les fusibles de la cellule (formats Mini ou Standard selon les générations) :

￼
	•	Particularité Ford (Euro 6) : Le relais de couplage interne du DS300 est désactivé en usine pour laisser un Chargeur Booster DC/DC (ex: REDARC) gérer proprement la charge en roulant sans perturber l'alternateur intelligent du Ford.
Sondes de niveaux : Connectées à l'arrière du DS300. L'eau propre (80L) utilise une sonde CBE à tiges métalliques (mesure par paliers de 25%). Les eaux usées utilisent des vis sondes inox (contacteur plein/vide). En cas de fausse mesure, nettoyer le calcaire et les graisses des tiges avec du vinaigre blanc.



🧠 PARTIE 2 : Intégration du Raspberry Pi 5 (Home Assistant)
Le Raspberry Pi 5 exige une alimentation extrêmement stable de 5.1V / 5A via USB-C sous peine de plantage.

1. Alimentation Électrique Sécurisée
À proscrire : Utiliser le convertisseur 230V du van avec le bloc secteur d'origine (perte d'énergie par double conversion et risque de coupure en veille).
La bonne méthode : Alimentation directe sur le 12V de la cellule.
Composant requis : Un convertisseur abaisseur de tension (Buck Converter) étanche 12V vers 5V (5A / 25W minimum) avec sortie USB-C.
Raccordement : Branché sur le boîtier CBE DS300 via un "porte-fusible voleur" (dérivateur) repiqué sur le circuit F3 (Prises 12V) avec un fusible de 5A dédié.
Masse (-) : Connectée sur le gros goujon de masse générale -B2 du DS300 (éviter le châssis du Ford à cause des colles structurelles isolantes).
Sécurité coupure : Ajout d'une carte d'extension UPS (Alimentation Ininterrompue) avec batterie sur le Pi pour permettre un arrêt propre (Soft Shutdown) si le circuit général du van est coupé au panneau.
Fiabilité Route : Remplacer la carte MicroSD par un Mini SSD NVMe pour résister aux vibrations et éviter la corruption de données.



☀️ PARTIE 3 : Récupération des Données Solaires
Le panneau solaire All-Black de 236 Watts installé sur le toit relevable par Stylevan est géré par deux types de régulateurs d'origine, tous deux fermés informatiquement :
CBE PRS300 (PWM) : Connecté au DS300 pour l'affichage sur l'écran d'origine. Aucun port de communication.
Antarion (MPPT) : Meilleur rendement, mais protocole Bluetooth fermé propriétaire.

La Solution IoT (Écosystème Victron Energy)
Pour faire remonter la production solaire en temps réel dans Home Assistant, la méthode universelle consiste à :
Remplacer le régulateur d'origine par un Victron SmartSolar MPPT 75/15 ou 100/20 (repiquage direct des fils du panneau et de la batterie).
Ajouter un Victron SmartShunt sur la borne négative de la batterie Lithium pour mesurer l'intégralité des flux d'énergie (consommation frigo, chauffage, charge du booster).
Liaison avec le Pi 5 : Directement en Bluetooth (via l'intégration Victron BLE) ou via un câble VE.Direct vers USB branché sur le Raspberry Pi.



🍏 PARTIE 4 : Écosystème Apple (CarPlay & HomeKit)
L'interaction avec le van connecté se fait à travers vos équipements Apple du quotidien.

1. Sur la route : Apple CarPlay
L'application officielle Home Assistant Companion intègre CarPlay nativement.
L'icône apparaît sur l'écran Ford SYNC du tableau de bord.
Permet de configurer des Actions rapides textuelles de sécurité ou de confort en roulant (ex: vérifier le frigo, éteindre une lumière extérieure restée allumée).

2. Au bivouac et en balade : iPhone & iPad
iPad en Tablette Murale : Fixé dans l'habitacle, il sert de moniteur graphique principal pour surveiller l'autonomie, l'eau et les températures.
iPhone en balade : Grâce à une connexion internet dans le van (Routeur 4G 12V ou Cloud Home Assistant), vous gardez le contrôle à distance et recevez des alertes (ex: alerte de vol si le van bouge 
