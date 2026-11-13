**Oui, la sécurisation physique est possible et même fortement recommandée**, car quiconque accède physiquement à l'habitacle de votre voiture peut débrancher le WiCAN PRO pour le voler, le réinitialiser en configuration d'usine ou se brancher directement sur le bus CAN du véhicule. [1, 2, 3]  
Voici les solutions physiques concrètes pour protéger votre installation :  
## 1. Utiliser un câble d'extension OBD-II profilé (Câble plat en Y)  
Laisser le WiCAN PRO branché directement sur la prise OBD d'origine le rend visible sous le tableau de bord, ce qui attire l'attention et gêne parfois les jambes.  
  
* Achetez un **câble d'extension OBD-II plat "ultra-low profile"** ou un **câble en Y**.  
* Branchez une extrémité sur la prise d'origine et cachez le WiCAN PRO profondément **derrière la garniture ou la console centrale**.  
* Fixez-le avec du ruban adhésif double-face ou des colliers de serrage (serflex). Un voleur opportuniste qui regarde sous le volant pensera que la prise est vide.  
## 2. Installer un verrou de port OBD (OBD Lock)  
Il existe des dispositifs de sécurité physiques conçus pour bloquer l'accès aux prises OBD. [4]  
  
* Il s'agit d'un **capuchon métallique ou en plastique renforcé** qui vient encliqueter et verrouiller la prise à l'aide d'une clé spécifique ou de vis de sécurité antivol (ex: empreinte Torx avec détrompeur). [4, 5, 6]  
* En déportant votre WiCAN PRO avec l'extension mentionnée au point 1, vous pouvez replacer la prise d'origine dans son logement et y visser un verrou OBD. Un attaquant extérieur verra une prise OBD totalement verrouillée et inviolable rapidement. [4]  
## 3. Désactiver les boutons physiques (si intégration permanente)  
Le WiCAN PRO possède des broches internes et des boutons (selon les révisions matérielles de MeatPi) permettant de forcer le mode flash ou le reboot.  
  
* Si vous logez le boîtier dans un endroit exigu ou un boîtier imprimé en 3D personnalisé, veillez à ce qu'**aucun bouton ne soit accessible de l'extérieur** sans démonter la garniture.  
## 4. Modifier le brochage de la prise (Le "Pin-Swapping")  
C'est la méthode ultime utilisée par les professionnels de la sécurité automobile.  
  
* Elle consiste à démonter les connecteurs (broches) à l'arrière de la prise OBD-II de la voiture pour **inverser l'ordre des fils** (par exemple, échanger le fil d'alimentation 12V avec une broche de données CAN). [7]  
* Vous fabriquez ensuite un **adaptateur adaptateur "inversé" sur mesure** que vous laissez branché entre la prise modifiée et votre WiCAN PRO caché.  
* *Résultat :* Si un pirate débranche votre système et tente de brancher sa propre clé de piratage sur votre prise OBD, l'inversion des fils détruira instantanément son matériel (court-circuit) ou rendra la communication impossible.  
Avez-vous de l'espace facilement accessible **derrière votre boîte à gants** ou **sous le volant** pour dissimuler le boîtier, ou souhaitez-vous des recommandations sur un **modèle de câble d'extension plat** adapté ?  
  
[1] ++[https://www.reddit.com](https://www.reddit.com/r/CarHacking/comments/1j61g1o/research_on_can_bus_vulnerabilities/)++  
[2] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/768)++  
[3] ++[https://www.facebook.com](https://www.facebook.com/groups/HomeAssistant/posts/4443992059205463/)++  
[4] ++[https://www.youtube.com](https://www.youtube.com/watch?v=QtQce4PAxW0&t=118)++  
[5] ++[https://www.digikey.fr](https://www.digikey.fr/fr/articles/basic-understanding-of-safety-circuits)++  
[6] ++[https://www.nbpower.com](https://www.nbpower.com/media/1492832/hsee-03-58-%C3%A9quipements-mobiles-et-lourds-motoris%C3%A9s.pdf)++  
[7] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/506)++  
  
  
Pour sécuriser efficacement votre boîtier **WiCAN PRO** et empêcher tout piratage (hack) de l'appareil ou de votre véhicule, vous devez restreindre ses accès réseau et sécuriser ses flux de données. Le WiCAN PRO étant branché directement sur le port OBD-II de votre voiture, un accès non autorisé pourrait permettre à un attaquant de lire, voire d'injecter des commandes sur le réseau informatique du véhicule (bus CAN). [1, 2]  
Voici les étapes essentielles pour le verrouiller :  
## 1. Modifier impérativement le mot de passe par défaut  
Par défaut, le point d'accès Wi-Fi généré par le boîtier utilise le mot de passe @meatpi#. Un attaquant à proximité de votre véhicule pourrait facilement s'y connecter. [3, 4]  
  
* Connectez-vous à l'interface web de votre WiCAN.  
* Allez dans l'onglet **Settings**.  
* Changez immédiatement le mot de passe du point d'accès (AP) pour un **mot de passe robuste et unique**. [4, 5, 6, 7]  
## 2. Désactiver le point d'accès (AP Mode) en déplacement  
Si le Wi-Fi du boîtier reste actif en permanence en mode Point d'Accès, n'importe qui croisant votre voiture ou stationné à côté peut tenter de s'y connecter. [4]  
  
* Configurez le Wi-Fi en mode **Station** (ou basculez automatiquement) pour qu'il se connecte uniquement au Wi-Fi sécurisé de votre domicile lorsque vous vous garez. [3, 5, 8, 9]  
* Sur les versions récentes du micrologiciel, privilégiez l'utilisation du **Bluetooth (BLE)** chiffré pour vos applications mobiles (comme Car Scanner) lorsque vous roulez. Le boîtier coupera le Wi-Fi et ne réactivera la connexion à votre réseau domestique qu'une fois de retour chez vous. [9]  
## 3. Activer et utiliser le tunnel VPN WireGuard  
Le WiCAN PRO intègre désormais nativement le support pour **WireGuard VPN**. [9, 10]  
  
* Si vous devez envoyer des données de télémétrie en temps réel (vers Home Assistant par exemple) lorsque vous êtes sur la route via un modem LTE/4G, **n'ouvrez jamais de ports sur votre routeur résidentiel**. [10]  
* Configurez le client WireGuard intégré au WiCAN PRO. Les données transiteront de manière totalement chiffrée à travers un tunnel sécurisé direct vers votre serveur domestique, invisible depuis l'internet public. [10, 11, 12, 13]  
## 4. Sécuriser les protocoles MQTT et Webhooks  
  
Si vous utilisez MQTT pour transmettre les données du véhicule à votre domotique : [5, 14]  
  
* N'utilisez pas de serveur MQTT ouvert sans authentification. Configurez obligatoirement un **nom d'utilisateur et un mot de passe fort** dédiés au WiCAN sur votre broker MQTT (comme Mosquitto). [5, 14]  
* Privilégiez l'usage de **MQTTS** (MQTT sécurisé par TLS) et **HTTPS** pour les webhooks, qui chiffrent les identifiants et les données du véhicule pour empêcher leur interception sur les réseaux Wi-Fi. [9]  
## 5. Configurer la mise en veille automatique (Deep Sleep)  
Un boîtier qui reste éveillé en permanence est une cible constamment disponible à l'attaque (en plus de vider votre batterie). [15]  
  
* Activez le **Sleep Mode** dans les paramètres de l'interface.  
* Configurez un seuil de tension de batterie (ex: en dessous de 12.2V) pour forcer le WiCAN PRO à entrer en veille profonde dès que le moteur est coupé. Un appareil éteint ne peut pas être piraté à distance. [5, 15, 16]  
## 6. Maintenir le micrologiciel (Firmware) à jour  
Les développeurs de MeatPi publient régulièrement des correctifs de sécurité et de nouvelles protections contre les instabilités ou vulnérabilités logicielles. [6, 17]  
  
* Allez régulièrement dans l'onglet de mise à jour du site officiel pour télécharger le dernier fichier .bin officiel et l'appliquer à votre boîtier. [5, 17]  
Souhaitez-vous de l'aide pour **générer les clés de configuration WireGuard** ou pour **sécuriser votre broker MQTT dans Home Assistant** afin d'y lier votre WiCAN en toute sécurité ?  
  
[1] ++[https://www.tiktok.com](https://www.tiktok.com/@unlearn_school/video/7530184816113880342)++  
[2] ++[https://meatpihq.github.io](https://meatpihq.github.io/wican-fw/factory-reset/factory-reset/)++  
[3] ++[https://meatpihq.github.io](https://meatpihq.github.io/wican-fw/home-assistant/integration/setup/)++  
[4] ++[https://meatpihq.github.io](https://meatpihq.github.io/wican-fw/config/wifi/)++  
[5] ++[https://www.youtube.com](https://www.youtube.com/watch?v=rxwOtW1x2NU&t=124)++  
[6] ++[https://www.youtube.com](https://www.youtube.com/watch?v=2fD17FKvqdc&t=601)++  
[7] ++[https://www.youtube.com](https://www.youtube.com/watch?v=czUIOKJehtw&t=212)++  
[8] ++[https://www.meatpi.com](https://www.meatpi.com/products/wican)++  
[9] ++[https://www.crowdsupply.com](https://www.crowdsupply.com/meatpi-electronics/wican-pro/updates/wican-pro-firmware-update-vpn-support-for-home-assistant)++  
[10] ++[https://www.reddit.com](https://www.reddit.com/r/homeassistant/comments/1ometf5/wican_pro_espnetlink_creating_a_secure_vpn_tunnel/)++  
[11] ++[https://jotelulu.com](https://jotelulu.com/fr-fr/assistance/tutoriels/comment-configurer-un-client-vpn-pour-depasser-limite-utilisateurs-de-reseau-prive/)++  
[12] ++[https://www.ouest-france.fr](https://www.ouest-france.fr/shopping/high-tech/vpn/comment-contourner-les-restrictions-dun-reseau-wi-fi-avec-un-vpn-7e9496b0-b66b-11f0-9097-68e77b575996)++  
[13] ++[https://coandmau.fr](https://coandmau.fr/lab/)++  
[14] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/discussions/728)++  
[15] ++[https://community.home-assistant.io](https://community.home-assistant.io/t/super-charged-wican-pro/1012782)++  
[16] ++[https://www.ouest-france.fr](https://www.ouest-france.fr/high-tech/telephonie/entretien-pirater-ou-espionner-un-telephone-a-distance-est-ce-si-facile-40109cb6-fa13-11ed-a003-8290333685fd)++  
[17] ++[https://github.com](https://github.com/meatpiHQ/wican-fw)++  
  
**Oui, la sécurisation physique est possible et même fortement recommandée**, car quiconque accède physiquement à l'habitacle de votre voiture peut débrancher le WiCAN PRO pour le voler, le réinitialiser en configuration d'usine ou se brancher directement sur le bus CAN du véhicule. [1, 2, 3]  
Voici les solutions physiques concrètes pour protéger votre installation :  
## 1. Utiliser un câble d'extension OBD-II profilé (Câble plat en Y)  
Laisser le WiCAN PRO branché directement sur la prise OBD d'origine le rend visible sous le tableau de bord, ce qui attire l'attention et gêne parfois les jambes.  
  
* Achetez un **câble d'extension OBD-II plat "ultra-low profile"** ou un **câble en Y**.  
* Branchez une extrémité sur la prise d'origine et cachez le WiCAN PRO profondément **derrière la garniture ou la console centrale**.  
* Fixez-le avec du ruban adhésif double-face ou des colliers de serrage (serflex). Un voleur opportuniste qui regarde sous le volant pensera que la prise est vide.  
## 2. Installer un verrou de port OBD (OBD Lock)  
Il existe des dispositifs de sécurité physiques conçus pour bloquer l'accès aux prises OBD. [4]  
  
* Il s'agit d'un **capuchon métallique ou en plastique renforcé** qui vient encliqueter et verrouiller la prise à l'aide d'une clé spécifique ou de vis de sécurité antivol (ex: empreinte Torx avec détrompeur). [4, 5, 6]  
* En déportant votre WiCAN PRO avec l'extension mentionnée au point 1, vous pouvez replacer la prise d'origine dans son logement et y visser un verrou OBD. Un attaquant extérieur verra une prise OBD totalement verrouillée et inviolable rapidement. [4]  
## 3. Désactiver les boutons physiques (si intégration permanente)  
Le WiCAN PRO possède des broches internes et des boutons (selon les révisions matérielles de MeatPi) permettant de forcer le mode flash ou le reboot.  
  
* Si vous logez le boîtier dans un endroit exigu ou un boîtier imprimé en 3D personnalisé, veillez à ce qu'**aucun bouton ne soit accessible de l'extérieur** sans démonter la garniture.  
## 4. Modifier le brochage de la prise (Le "Pin-Swapping")  
C'est la méthode ultime utilisée par les professionnels de la sécurité automobile.  
  
* Elle consiste à démonter les connecteurs (broches) à l'arrière de la prise OBD-II de la voiture pour **inverser l'ordre des fils** (par exemple, échanger le fil d'alimentation 12V avec une broche de données CAN). [7]  
* Vous fabriquez ensuite un **adaptateur adaptateur "inversé" sur mesure** que vous laissez branché entre la prise modifiée et votre WiCAN PRO caché.  
* *Résultat :* Si un pirate débranche votre système et tente de brancher sa propre clé de piratage sur votre prise OBD, l'inversion des fils détruira instantanément son matériel (court-circuit) ou rendra la communication impossible.  
Avez-vous de l'espace facilement accessible **derrière votre boîte à gants** ou **sous le volant** pour dissimuler le boîtier, ou souhaitez-vous des recommandations sur un **modèle de câble d'extension plat** adapté ?  
  
[1] ++[https://www.reddit.com](https://www.reddit.com/r/CarHacking/comments/1j61g1o/research_on_can_bus_vulnerabilities/)++  
[1] ++[https://www.reddit.com](https://www.reddit.com/r/CarHacking/comments/1j61g1o/research_on_can_bus_vulnerabilities/)++  
[2] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/768)++  
[2] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/768)++  
[3] ++[https://www.facebook.com](https://www.facebook.com/groups/HomeAssistant/posts/4443992059205463/)++  
[3] ++[https://www.facebook.com](https://www.facebook.com/groups/HomeAssistant/posts/4443992059205463/)++  
[4] ++[https://www.youtube.com](https://www.youtube.com/watch?v=QtQce4PAxW0&t=118)++  
[5] ++[https://www.digikey.fr](https://www.digikey.fr/fr/articles/basic-understanding-of-safety-circuits)++  
[6] ++[https://www.nbpower.com](https://www.nbpower.com/media/1492832/hsee-03-58-%C3%A9quipements-mobiles-et-lourds-motoris%C3%A9s.pdf)++  
[7] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/506)++  
[7] ++[https://github.com](https://github.com/meatpiHQ/wican-fw/issues/506)++  
  
  
