  
  
  
  
## User : d'abord on resume le projet en partant de l'achat de la caméra  
## Assistant : Voici le résumé complet de votre projet, étape par étape, depuis l'achat du matériel jusqu'à son intégration intelligente dans votre minivan Westfalia :  
  
## 🛒 Étape 1 : Le Matériel de départ  
* **Les caméras** : Vous disposez de 3 mini-caméras de sécurité Wi-Fi génériques (alimentées en USB 5V) destinées à être réparties autour du van pour une surveillance à 360°.  
* **L'alimentation indépendante** : Pour éviter de percer le toit relevable, chaque caméra possède son propre bloc d'alimentation composé d'une batterie externe solaire de chantier (IP65, minimum 20 000 mAh).  
* **Le cerveau du système** : Un microcontrôleur **ESP32** relié à un module relais 5V, piloté à distance par votre système **Home Assistant** embarqué.  
  
  
  
## 🛠️ Étape 2 : La modification électrique (Le "Hack" USB)  
* Les caméras miniatures n'ont pas de mode veille et consomment trop pour rester allumées 24h/24 sur leurs batteries solaires.  
* **La solution** : Vous coupez le fil rouge (+5V) du câble USB de chaque caméra et vous le faites passer par le relais contrôlé by l'ESP32.  
* L'ESP32 est quant à lui branché sur la batterie 12V auxiliaire du Westfalia pour rester toujours disponible sur le réseau Wi-Fi du van.  
  
  
  
## 🧲 Étape 3 : L'installation extérieure (Zéro perçage)  
* **La préparation** : Vous nettoyez et dégraissez parfaitement la carrosserie ou la coque en polyester du toit relevable à l'aide d'alcool isopropylique.  
* **Le collage structurel** : Vous collez des embases métalliques ou des plots de fixation en plastique à l'aide de ruban adhésif ultra-puissant **3M VHB 5952**.  
* **La fixation amovible** :  
    * Les caméras sont aimantées sur les plaques métalliques collées.  
    * Les batteries solaires sont ceinturées par des colliers de serrage (Rilsan) sur les plots collés, ce qui permet de les décrocher facilement en cas de besoin.  
* *(Note pour le futur : En cas de revente du van, le ruban 3M VHB se retirera proprement à l'aide de fil de pêche et de WD-40, sans abîmer le vernis).*  
  
  
  
## 🤖 Étape 4 : L'intégration dans Home Assistant  
* L'ESP32 est flashé avec **ESPHome** pour déclarer un interrupteur virtuel.  
* Depuis votre smartphone ou l'écran tactile du van, vous pouvez couper ou allumer les caméras à la demande.  
* Des automatisations coupent le système sur la route pour économiser les batteries solaires et l'activent automatiquement en mode "Bivouac" la nuit ou dès que vous quittez le véhicule.  
## Souhaitez-vous maintenant que nous passions à la réalisation pratique en validant le schéma de câblage précis entre l'ESP32, le relais et vos caméras ?  
  
  
## User : on y va. d'abord pour info il y a a bord un raspeberry pi ou tourne home assistant. le raspeberry est alimenté en continu  
## Assistant : C’est une excellente configuration ! Puisque votre Raspberry Pi tourne en continu, le serveur Home Assistant est toujours disponible pour piloter le système, même lorsque vous dormez ou que vous quittez le van.  
## Entrons dans le vif du sujet avec la réalisation pratique du module de coupure.  
  
## 📐 Le Schéma de Câblage Électrique  
## Pour contrôler vos 3 caméras, vous allez utiliser un ESP32 couplé à une carte de 4 relais 5V (très courante et peu coûteuse). L'ESP32 va agir sur les relais comme vos doigts sur un interrupteur.  
## Voici comment brancher l'ensemble :  
  
## text  
```
       [ Batterie Solaire 5V ]           [ ESP32 ]          [ Batterie Aux 12V Van ]
                 │                           │                        │
                 ▼                           ▼                        ▼
       [ Câble USB Caméra ]           [ Carte Relais ]       [ Régulateur 12V->5V ]
        Fil Noir (Masse/GND) ───────────────► GND ◄─────────────────── GND
        Fil Rouge (+5V) ──► [Relais NO]       │
                            [Relais COM] ◄────┼──► Broche GPIO23

```
Utilisez le code avec précaution.  
  
  
## 1. Connexion de l'ESP32 et de la carte Relais  
* **Alimentation** : Reliez la broche **VIN (ou 5V)** de l'ESP32 et la broche **VCC** de la carte relais à la sortie 5V de votre régulateur branché sur la batterie 12V du van.  
* **Masse commune** : Reliez la broche **GND** de l'ESP32, la broche **GND** de la carte relais et le fil noir (GND) du régulateur ensemble.  
* **Commande** : Reliez une broche numérique de l'ESP32 (par exemple **GPIO23**) à l'entrée **IN1** de la carte relais. (Faites de même avec GPIO22 vers IN2 pour la deuxième caméra, et GPIO21 vers IN3 pour la troisième).  
  
## 2. Le "Hack" du câble USB des caméras  
## Prenez le câble USB qui part de la batterie externe solaire vers la caméra :  
* **Fil Noir (Masse)** : Ne le coupez pas, laissez-le aller directement de la batterie solaire à la caméra.  
* **Fil Rouge (+5V)** : Coupez-le au milieu.  
    * Connectez le côté qui vient de la batterie solaire sur la borne **COM** (Commun) du relais numéro 1.  
    * Connectez le côté qui va vers la caméra sur la borne **NO** (Normalement Ouvert) du relais numéro 1.  
## *Résultat* : Tant que l'ESP32 ne donne pas l'ordre, le relais reste ouvert, le courant ne passe pas, la caméra éteinte et sa batterie solaire ne se vide pas.  
  
  
  
## 💻 Étape Suivante : Le Code ESPHome  
## Pour que Home Assistant reconnaisse instantanément votre ESP32, nous allons utiliser l'extension ESPHome (à installer en 1 clic dans l'onglet *Modifications / Add-ons* de votre Home Assistant).  
## Voici le code complet à copier dans ESPHome pour vos 3 caméras :  
  
## yaml  
```
esphome:
  name: gestionnaire-cameras-van

esp32:
  board: esp32dev

# Connexion au Wi-Fi généré par le routeur de votre van
wifi:
  ssid: "Nom_Du_WiFi_De_Votre_Van"
  password: "Votre_Mot_De_Passe_WiFi"
  
  # Optionnel mais recommandé : fixe l'IP pour éviter les déconnexions
  manual_ip:
    static_ip: 192.168.1.50
    gateway: 192.168.1.1
    subnet: 255.255.255.0

# Active la découverte automatique dans Home Assistant
api:

logger:

# Configuration des 3 interrupteurs (Relais)
switch:
  - platform: gpio
    pin: GPIO23
    name: "Caméra Arrière (Recul)"
    icon: "mdi:camera-rear"
    
  - platform: gpio
    pin: GPIO22
    name: "Caméra Flanc Gauche"
    icon: "mdi:camera-left"

  - platform: gpio
    pin: GPIO21
    name: "Caméra Flanc Droit"
    icon: "mdi:camera-right"

```
Utilisez le code avec précaution.  
  
**Une fois ce code installé, vous verrez apparaître 3 boutons d'allumage sur votre tableau de bord Home Assistant.**  
## Est-ce que cette partie électrique vous paraît claire, ou préférez-vous que l'on détaille le choix exact des composants (type de relais, convertisseur 12V) avant de passer aux automatisations logicielles ?  
  
  
## User : detaille  
## Assistant : Pour que votre montage soit parfaitement fiable, résiste aux vibrations de la route et ne crée aucun risque de court-circuit dans le van, voici le détail exact des composants à choisir et la méthode d'assemblage.  
  
  
  
## 1. La liste précise des composants électroniques  
## Vous pouvez trouver ces pièces très facilement pour quelques euros sur les sites d'électronique (Amazon, AliExpress, ou des boutiques spécialisées comme Go Tronic) :  
* **Le Microcontrôleur : ESP32 NodeMCU (Modèle 30 ou 38 broches)**  
    * *Pourquoi ce modèle ?* : Choisissez une version avec des broches déjà soudées (*headers*). Le format "NodeMCU" ou "ESP32-WROOM" est le plus standard et dispose de suffisamment de broches GPIO pour piloter vos relais.  
* **Le module Relais : Carte 4 canaux Relais 5V (avec Optocoupleurs)**  
    * *Pourquoi ce modèle ?* : Prenez impérativement une carte relais spécifiée **"avec isolation par optocoupleur" (Low Level Trigger)**. L'optocoupleur sépare physiquement le circuit électrique de l'ESP32 du circuit des caméras. Si un court-circuit survient sur une caméra extérieure à cause de la pluie, l'ESP32 et votre Raspberry Pi restent totalement protégés.  
* **L'alimentation de l'ESP32 : Convertisseur Régulateur de tension 12V vers 5V (Type "Buck")**  
    * *Pourquoi ce modèle ?* : La tension d'une batterie auxiliaire de van varie (de 11,8V à l'arrêt à 14,4V lorsque l'alternateur charge). Ne branchez jamais l'ESP32 directement sur le 12V. Utilisez un petit boîtier convertisseur étanche (souvent utilisé pour les caméras de voiture) qui transforme cette tension fluctuante en un **5V pur et stable**.  
  
  
  
## 2. Le câblage pas-à-pas des broches (Côté Commande)  
## Pour relier l'ESP32 à la carte relais, utilisez des petits câbles de prototypage appelés câbles Dupont (Femelle-Femelle).  
1. **Alimentation des composants** :  
    * Connectez le fil **Rouge (+5V)** du convertisseur 12V/5V sur la broche **VIN** (ou 5V) de l'ESP32 **ET** sur la broche **VCC** de la carte relais.  
    * Connectez le fil **Noir (GND/Masse)** du convertisseur 12V/5V sur une broche **GND** de l'ESP32 **ET** sur la broche **GND** de la carte relais.  
2. **Signaux de commande** :  
    * Reliez la broche **GPIO23** de l'ESP32 à la broche **IN1** de la carte relais (Pilote la caméra arrière).  
    * Reliez la broche **GPIO22** de l'ESP32 à la broche **IN2** de la carte relais (Pilote la caméra gauche).  
    * Reliez la broche **GPIO21** de l'ESP32 à la broche **IN3** de la carte relais (Pilote la caméra droite).  
## *Note sur la carte relais : Vérifiez qu'un petit cavalier en plastique (jumper) est bien présent sur les broches nommées VCC et JD-VCC. Cela permet de partager la même alimentation 5V pour la logique et pour les bobines des relais.*  
  
  
  
## 3. Le câblage des borniers des relais (Côté Caméras)  
## À l'extrémité de la carte relais, vous trouverez des borniers bleus à vis pour chaque canal. Chaque relais possède 3 entrées : NO (Normalement Ouvert), COM (Commun), et NC (Normalement Fermé).  
## Pour chaque caméra, vous allez sectionner uniquement le fil rouge d'un câble d'extension USB :  
1. Dénudez le câble USB pour isoler le **fil rouge (+5V)** et le **fil noir (GND)**.  
2. Laissez le **fil noir** intact (il va directement de la batterie solaire à la caméra).  
3. Coupez le **fil rouge** en deux :  
    * Vissez le côté qui vient de la **batterie solaire** dans la borne **COM** du relais.  
    * Vissez le côté qui va vers la **caméra** dans la borne **NO** du relais.  
  
  
  
## 4. L'intégration propre dans le Westfalia  
## Pour éviter que les fils ne bougent ou ne s'usent avec les vibrations du van, rassemblez l'ESP32 et la carte relais dans un boîtier de dérivation électrique en plastique (type Plexo de Legrand).  
* Fixez le boîtier proprement à l'intérieur du van (par exemple, dans un placard haut ou près de votre centrale électrique Westfalia).  
* Utilisez des presse-étoupes ou du gel d'étanchéité si le boîtier est placé dans une zone soumise à l'humidité.  
## Une fois ces branchements physiques terminés, nous pourrons passer à l'étape logicielle dans Home Assistant. Souhaitez-vous que l'on commence à créer les premières automatisations (par exemple, allumer les caméras uniquement si le van est verrouillé et à l'arrêt) ?  
  
  
## User : oui. camera allumée à l'arret et que le van est verouillé. camere allumée à l'arret van verouillé, luminosité faible et commande manuel de mise ne marche pour surveillance nocturne. camera on lorsque le véhicule roule (fonction dashcam)  
## Assistant : Pour traduire ces règles en automatisations concrètes dans Home Assistant, nous allons utiliser les capteurs de votre van (l'état des portes, du contact, et la luminosité extérieure).  
## Voici la configuration exacte de vos trois scénarios logiques.  
  
  
  
## Scénario 1 : Protection Bivouac / Stationnement  
## Objectif : Allumer les caméras dès que vous quittez et verrouillez le véhicule.  
* **Déclencheur (Trigger) :** Le capteur de verrouillage du van passe à "Verrouillé" (*Locked*).  
* **Condition :** Le moteur du van est éteint (contact coupé).  
* **Action :** Activer (*Turn on*) les 3 interrupteurs des caméras.  
  
  
  
## Scénario 2 : Surveillance Nocturne Intuitive (Sommeil)  
## Objectif : Allumer automatiquement les caméras quand vous dormez à bord (van verrouillé de l'intérieur, nuit noire) OU par commande manuelle depuis votre lit.  
## Pour cela, nous allons créer deux déclencheurs distincts dans la même automatisation (le premier qui s'active déclenche l'allumage) :  
* **Déclencheurs (Triggers) :**  
    1. *Option Automatique* : La luminosité extérieure baisse sous un certain seuil (ex: 10 lux) **ET** le van est verrouillé.  
    2. *Option Manuelle* : Vous appuyez sur un bouton physique (type bouton sans fil Zigbee collé près du lit) ou sur un bouton virtuel de votre smartphone.  
* **Action :** Activer (*Turn on*) les 3 interrupteurs des caméras.  
  
  
  
## Scénario 3 : Mode Dashcam (Sécurité routière)  
## Objectif : Allumer les caméras dès que le van roule pour filmer l'environnement ou servir d'aide à la conduite.  
* **Déclencheur (Trigger) :** Le contact du véhicule passe à "ON" (Moteur démarré).  
* **Action :** Activer (*Turn on*) les 3 interrupteurs des caméras.  
  
  
  
## 💻 Code YAML des Automatisations pour Home Assistant  
## Voici le code à copier directement dans l'éditeur d'automatisations de Home Assistant (en remplaçant les noms des entités par les vôtres, comme binary_sensor.van_verrouille ou binary_sensor.moteur_contact) :  
  
## yaml  
```
# AUTOMATISATION 1 & 3 : MODE ROUTE ET STATIONNEMENT
id: 'gestion_cameras_van_principal'
alias: 'Van - Gestion des caméras (Route & Stationnement)'
description: 'Gère les caméras selon le contact du moteur et le verrouillage'
trigger:
  - platform: state
    entity_id: binary_sensor.van_verrouille
    to: 'on' # Signifie "Verrouillé"
    id: vehicule_verrouille
  - platform: state
    entity_id: binary_sensor.moteur_contact
    to: 'on' # Signifie "Moteur en marche"
    id: moteur_demarre
  - platform: state
    entity_id: binary_sensor.van_verrouille
    to: 'off' # Déverrouillé
    id: vehicule_deverrouille
condition: []
action:
  - choose:
      # Si on roule OU si le van est vide et verrouillé -> On allume
      - conditions:
          - or:
              - condition: trigger
                id: moteur_demarre
              - condition: and
                conditions:
                  - condition: trigger
                    id: vehicule_verrouille
                  - condition: state
                    entity_id: binary_sensor.moteur_contact
                    state: 'off'
        sequence:
          - service: switch.turn_on
            target:
              entity_id:
                - switch.camera_arriere_recul
                - switch.camera_flanc_gauche
                - switch.camera_flanc_droit
      # Si on déverrouille le van à l'arrêt (on revient au van la journée) -> On éteint pour économiser
      - conditions:
          - condition: trigger
            id: vehicule_deverrouille
          - condition: state
            entity_id: binary_sensor.moteur_contact
            state: 'off'
        sequence:
          - service: switch.turn_off
            target:
              entity_id:
                - switch.camera_arriere_recul
                - switch.camera_flanc_gauche
                - switch.camera_flanc_droit

---

# AUTOMATISATION 2 : SURVEILLANCE NOCTURNE A BORD
id: 'surveillance_nocturne_van'
alias: 'Van - Surveillance Nocturne'
description: 'Allume les caméras la nuit ou sur commande manuelle au lit'
trigger:
  - platform: numeric_state
    entity_id: sensor.luminosite_exterieure
    below: 10 # Seuil de pénombre (en lux)
    id: nuit_tombee
  - platform: state
    entity_id: input_boolean.bouton_panique_nuit # Votre commande manuelle (virtuelle ou bouton Zigbee)
    to: 'on'
    id: commande_manuelle
condition:
  # Pour l'allumage automatique de nuit, on vérifie qu'on est bien garé et fermé de l'intérieur
  - condition: state
    entity_id: binary_sensor.van_verrouille
    state: 'on'
action:
  - service: switch.turn_on
    target:
      entity_id:
        - switch.camera_arriere_recul
        - switch.camera_flanc_gauche
        - switch.camera_flanc_droit

```
Utilisez le code avec précaution.  
  
  
## 💡 Le Conseil "Confort" pour la nuit  
Puisque ces mini-caméras possèdent des petites LED d'état (souvent bleues ou rouges) et des LED infrarouges pour la vision nocturne, pensez à masquer les LED d'état visibles de l'intérieur du van avec un morceau de scotch opaque. Cela vous évitera d'avoir des lumières clignotantes parasites dans l'habitacle pendant que vous dormez sous la toile du Westfalia.  
## Pour finaliser l'installation logicielle, comment récupérez-vous actuellement les informations du van dans Home Assistant ? Utilisez-vous une clé OBD2 connectée au Raspberry Pi, des capteurs d'ouverture sans fil (Zigbee/Bluetooth) sur les portes, ou un boîtier de communication propre au Westfalia ?  
  
  
## User : clé obd2  
## Assistant : L’utilisation d’une clé OBD2 branchée sur la prise diagnostic de votre minivan (généralement située sous le tableau de bord, près des fusibles) est parfaite pour automatiser votre système. Elle permet de remonter des informations fiables et en temps réel directement dans votre Raspberry Pi.  
## Pour que vos automatisations de caméras fonctionnent à l'arrêt, il y a cependant un piège majeur à éviter, ainsi qu'une configuration spécifique à mettre en place.  
  
## ⚠️ Le piège de la prise OBD2 : Le contact coupé  
## Sur la majorité des véhicules du groupe Volkswagen/Ford/Mercedes (qui servent de base aux Westfalia modernes comme le Kelsey ou le Kepler), la prise OBD2 se comporte de deux manières différentes selon les constructeurs :  
1. **L'alimentation permanente** : La clé OBD2 reste allumée même quand le contact est coupé. C'est idéal pour notre projet, mais attention : si la clé OBD2 consomme trop, elle peut vider la batterie de démarrage (moteur) après plusieurs jours d'immobilisation.  
2. **L'alimentation après-contact** : La prise OBD2 s'éteint complètement quelques minutes après la coupure du moteur. Dans ce cas, Home Assistant perd la connexion avec la clé et ne peut plus savoir si le van est verrouillé.  
  
## 🛠️ La solution matérielle recommandée  
## Pour votre projet, vous devez impérativement utiliser une clé OBD2 équipée d'un mode veille automatique (Auto-Sleep), comme la Obdlink LX Bluetooth ou une clé vLinker MC+.  
* Ces clés basculent dans un mode à ultra-faible consommation (moins de 2 mA) dès que le moteur s'arrête.  
* Elles restent capables de détecter le protocole de verrouillage centralisé sur le réseau du van (le bus CAN) sans vider votre batterie.  
  
  
  
## 💻 Configuration dans Home Assistant  
## Pour faire communiquer votre clé OBD2 avec le Raspberry Pi, vous allez utiliser l'intégration officielle Torque ou, plus moderne et stable, l'intégration OBD2 / ELM327 via MQTT.  
## Une fois configurée, la clé OBD2 va créer des entités (capteurs) spécifiques dans votre Home Assistant. Voici comment les lier aux déclencheurs de vos automatisations :  
  
## 1. Détecter le "Moteur en marche" (Mode Dashcam)  
## Pour savoir si le véhicule roule, on n'utilise pas la vitesse (qui est à 0 au feu rouge), mais le régime moteur ou la tension du système.  
* **L'entité OBD2** : sensor.obd_engine_rpm (Tours par minute) ou sensor.obd_control_module_voltage (Tension).  
* **La règle logique** : Si les tours/minute passent au-dessus de 400 RPM, alors le moteur a démarré. Les caméras s'allument en mode Dashcam.  
  
## 2. Détecter le "Van Verrouillé" (Mode Bivouac)  
## Sur le réseau de données du véhicule, le verrouillage des portes envoie une commande spécifique.  
* **L'entité OBD2** : Selon les véhicules, cela remonte sous forme de statut binaire (portes verrouillées = on).  
* **Alternative universelle** : Si le protocole des portes de votre modèle de van est difficile à lire via l'OBD2, vous pouvez utiliser la **tension de la batterie de démarrage**. Lorsque vous quittez et verrouillez le véhicule, les calculateurs s'éteignent les uns après les autres et la tension de la batterie se stabilise (par exemple à 12,6V). Si le moteur est éteint et que la tension est stable depuis 5 minutes, Home Assistant en déduit que le van est en stationnement sécurisé.  
  
  
  
## 📝 Mise à jour de vos déclencheurs (Triggers) dans Home Assistant  
## Dans le code YAML que nous avons vu à l'étape précédente, il vous suffit de remplacer les détecteurs théoriques par les données réelles reçues de votre clé OBD2 :  
  
## yaml  
```
# Remplacer le déclencheur "moteur_demarre" par le régime moteur :
trigger:
  - platform: numeric_state
    entity_id: sensor.obd_engine_rpm
    above: 400
    id: moteur_demarre

# Remplacer le déclencheur "moteur_eteint" :
  - platform: numeric_state
    entity_id: sensor.obd_engine_rpm
    below: 100
    id: moteur_arrete

```
Utilisez le code avec précaution.  
  
**Si vous constatez que votre prise OBD2 se coupe complètement lorsque vous retirez la clé du contact, faites-le moi savoir. Nous pourrons contourner le problème en ajoutant un petit capteur d'ouverture de porte sans fil (type Zigbee) à 10 € sur la porte conducteur pour informer Home Assistant à coup sûr.**  
## Rencontrez-vous actuellement des difficultés pour faire remonter les données de votre clé OBD2 dans votre Raspberry Pi, ou la communication fonctionne-t-elle déjà ?  
  
  
## User : non revenons au powerbank, quel modele est le plus adequat vu la configuration nouvelle  
**Assistant : Avec l'intégration de votre ESP32, de votre Raspberry Pi en continu et de vos automatisations logiques, la donne change complètement.**  
Puisque l'ESP32 va couper l'alimentation des caméras la majeure partie de la journée (lorsque vous roulez ou en journée ensoleillée sans verrouillage), les caméras ne consommeront plus d'énergie en continu. Les batteries solaires n'ont donc plus besoin d'être surdimensionnées à 30 000 mAh.  
## Le critère technique le plus important devient désormais la fonction Pass-Through Charging (Charge traversante).  
  
## Le critère obligatoire : Le Pass-Through Charging réel  
La majorité des batteries solaires bas de gamme coupent leurs sorties USB dès que leur panneau solaire reçoit de la lumière pour se recharger. Dans votre cas, cela signifie que si le panneau solaire recharge la batterie en plein après-midi, vos caméras ne pourront pas s'allumer si vous verrouillez le van.  
## Il vous faut obligatoirement un modèle capable de recevoir l'énergie du soleil tout en alimentant la caméra en même temps.  
  
  
  
## Les 2 modèles de Powerbanks les plus adéquats  
  
Xtorm Rugged Solar Powerbank 10 000 mAh (XR101 / XR201)  
## C'est le modèle parfait pour votre nouvelle configuration optimisée.  
* **Pourquoi il est idéal** : La marque Xtorm intègre une fonction *Pass-Through* gérée électroniquement de manière très sécurisée (Check de sécurité en 6 couches). La batterie protège les cellules contre la surchauffe, ce qui est indispensable sur le toit en polyester d'un van en plein été.  
* **Spécificités** : Certifiée **IP65** (résiste aux tempêtes et projections sur l'autoroute). Sa capacité de 10 000 mAh suffit largement maintenant que l'ESP32 gère l'extinction des caméras. Elle est compacte, légère et intègre une encoche solide pour la ceinturer avec un collier de serrage sur vos plots collés au 3M VHB.  
  
Sandberg Outdoor Solar Powerbank 16 000 mAh (420-35)  
## Une excellente alternative si vous souhaitez une réserve d'énergie légèrement supérieure pour pallier plusieurs jours de pluie d'affilée en automne.  
* **Pourquoi elle est idéale** : Conçue spécifiquement pour le camping et les conditions extrêmes, la gamme Sandberg Outdoor gère parfaitement la charge simultanée (solaire + sortie USB). Son revêtement extérieur ultra-robuste amortit les vibrations constantes de la carrosserie lorsque le minivan roule.  
  
  
  
## 💡 L'astuce de branchement avec l'ESP32  
## Puisque le câble USB va désormais faire le trajet :  
Powerbank Solaire (sur le toit)** ➡️ **Boîtier ESP32/Relais (à l'intérieur du van)** ➡️ **Caméra (sur le toit)**,**  
Powerbank Solaire (sur le toit)** ➡️ **Boîtier ESP32/Relais (à l'intérieur du van)** ➡️ **Caméra (sur le toit)**,**  
assurez-vous d'utiliser des câbles USB de bonne qualité (avec des fils de section en cuivre suffisante) pour éviter les pertes de tension (chutes de tension en ligne) sur la longueur du trajet aller-retour vers le toit relevable.  
## Souhaitez-vous que l'on valide la méthode pour faire passer proprement ces câbles USB à travers la toile ou les joints du toit relevable de votre Westfalia ?  
  
  
## User : oui on valide la méthode  
## Assistant : La méthode de passage des câbles à travers le toit relevable de votre Westfalia Kelsey (ou similaire sur porteur Ford Transit Custom / VW) doit impérativement respecter deux règles : garantir une étanchéité parfaite à l'eau de pluie lors de trajets sur l'autoroute et éviter le pincement des câbles lors du repli de la toile.  
## Voici le protocole technique complet, éprouvé pour les vans aménagés, garantissant zéro perçage de la coque :  
  
## 1. Le cheminement le long du bras articulé (Pantographe)  
## C'est la solution standard utilisée par les constructeurs pour alimenter les éclairages du lit haut ou les panneaux solaires.  
* **Le principe** : Les câbles USB reliant l'intérieur du van (boîtier ESP32) aux batteries et caméras du toit doivent remonter en suivant l'un des bras articulés métalliques qui lèvent le toit.  
* **La mise en œuvre** : Fixez les câbles le long du bras métallique à l'aide de bandes Velcro ou de colliers Rilsan.  
* **La boucle d'aisance (Crucial)** : Laissez une boucle de câble lâche d'environ 10 à 15 cm au niveau des articulations du bras. Lorsque le toit se referme, le câble doit se plier naturellement sans jamais être tendu ni se coincer dans le mécanisme mécanique.  
  
## 2. Le passage à travers la toile de toit (Sans découpe)  
## Ne percez et ne découpez jamais la toile de tente de votre Westfalia sous peine de l'effilocher et de perdre l'étanchéité.  
* **La technique du soufflet arrière** : Sur la grande majorité des Westfalia, la toile est fixée à la carrosserie basse via un rail masqué par un joint ou un rabat en caoutchouc. À l'arrière du van (au niveau des charnières du toit), il existe un micro-espace naturel là où la toile rejoint les angles.  
* Faites passer vos fins câbles USB par ce coin arrière, juste sous le repli du joint d'étanchéité de la base du toit.  
  
## 3. La protection des câbles sur la coque supérieure (Extérieur)  
## Une fois les câbles sortis sur le toit rigide en polyester, ils vont courir à l'extérieur jusqu'aux caméras et aux powerbanks.  
* **Le cheminement** : Ne laissez aucun câble libre de bouger avec le vent. Utilisez des **mini-goulottes adhésives extérieures étanches** ou collez directement les câbles à plat sur le toit à l'aide de **ruban adhésif d'étanchéité en aluminium** (hautement résistant aux UV et aux intempéries).  
* **Le raccordement aux Powerbanks** : Branchez vos câbles sur les ports de vos batteries Xtorm ou Sandberg. Assurez-vous que le capuchon d'étanchéité en caoutchouc de la batterie enserre fermement votre fiche USB pour empêcher l'humidité d'entrer dans le connecteur.  
  
## 🔍 Check-list de validation avant fermeture du toit  
## Avant de valider définitivement votre installation, effectuez un test manuel à deux personnes :  
1. Une personne actionne lentement la descente du toit depuis l'habitacle.  
2. La seconde observe depuis le lit haut le comportement des câbles le long des bras métalliques.  
3. Vérifiez qu'aucune portion de câble ne s'invite entre le joint d'étanchéité en caoutchouc du toit et la carrosserie en tôle du van.  
## Votre projet est désormais entièrement ficelé, de l'achat à l'automatisation. Rencontrez-vous une dernière interrogation sur la configuration de vos scénarios dans ESPHome ou sur l'intégration visuelle de vos caméras sur le tableau de bord de votre smartphone ?  
  
  
## User : et si je mets un esp32 à chaque powerbnk ?  
## Assistant : C'est techniquement possible, mais cela va grandement complexifier votre installation et menacer l'autonomie de vos batteries solaires.  
## Placer un ESP32 extérieur au niveau de chaque powerbank introduit trois problèmes majeurs qu'il est indispensable de mesurer :  
  
## 1. Le piège de la consommation en veille (Le plus critique)  
## Pour que Home Assistant puisse envoyer l'ordre à un ESP32 d'allumer une caméra, cet ESP32 doit être connecté en Wi-Fi en permanence.  
* En mode actif connecté au Wi-Fi, un ESP32 consomme entre **80 mA et 120 mA en continu**.  
* Branché directement sur votre batterie solaire, un seul ESP32 consommerait environ **2,4 Ah par jour** uniquement pour "attendre" vos ordres. Multiplié par 3, vos powerbanks solaires s'épuiseraient à grande vitesse, avant même d'avoir allumé la moindre caméra.  
* *La fausse bonne idée du Deep Sleep* : Si vous passez l'ESP32 en mode sommeil profond (*Deep Sleep*), il ne consomme plus rien (quelques micro-ampères), mais **il coupe son Wi-Fi**. Home Assistant devient alors incapable de le réveiller à distance pour allumer une caméra. Un ESP32 en *Deep Sleep* ne peut se réveiller que de lui-même via un minuteur interne (par exemple toutes les heures) ou un capteur physique câblé.  
  
  
Voici la compilation intégrale de nos échanges depuis le résumé du projet, formatée de manière propre et prête pour votre documentation personnelle.  
Vous trouverez ci-dessous le fichier au format **Markdown (.md)**. Vous pouvez le copier-coller dans n'importe quel éditeur de texte (comme Notepad, VS Code ou l'éditeur de fichiers de Home Assistant) et l'enregistrer sous le nom projet_cameras_westfalia.md.  
```
# 🚐 Projet d'Installation de 3 Mini-Caméras Wi-Fi - Westfalia Kelsey

Ce document compile l'ensemble des étapes techniques, des choix de composants et des configurations logicielles pour l'installation d'un système de surveillance autonome à 360° sur le toit relevable d'un minivan Westfalia.

---

## 📋 1. Résumé Global du Projet (Point de Départ)

* **Les caméras** : 3 mini-caméras de sécurité Wi-Fi génériques (alimentées en USB 5V) réparties autour du van pour une surveillance complète.
* **L'alimentation indépendante** : Pour éviter de percer le toit relevable, chaque caméra possède son propre bloc d'alimentation composé d'une batterie externe solaire de chantier (IP65, minimum 10 000 à 20 000 mAh avec fonction *Pass-Through*).
* **Le cerveau du système** : Un microcontrôleur **ESP32** relié à un module relais 5V, branché sur la batterie auxiliaire 12V du van et piloté à distance par le système **Home Assistant** embarqué (qui tourne en continu sur un Raspberry Pi).
* **Le déclenchement intelligent** : Une clé **OBD2** connectée au Raspberry Pi transmet l'état du van en temps réel pour automatiser l'allumage des caméras.

---

## 🛠️ 2. Choix du Matériel et Montage Électrique

### Liste précise des composants à acheter
* **Microcontrôleur** : ESP32 NodeMCU (Modèle standard 30 ou 38 broches avec *headers* soudés).
* **Module Relais** : Carte 4 canaux Relais 5V équipée d'une **isolation par optocoupleur (Low Level Trigger)** pour protéger l'électronique en cas de court-circuit extérieur dû à la pluie.
* **Alimentation ESP32** : Convertisseur régulateur de tension 12V vers 5V (Type "Buck" étanche) connecté à la batterie auxiliaire 12V du Westfalia.
* **Powerbanks Solaires** : Modèles Outdoor IP65 gérant impérativement la charge traversante (*Pass-Through Charging*) comme la gamme **Xtorm Rugged Solar (XR101 / XR201)** ou **Sandberg Outdoor Solar 16000**.

### Sélection des broches sécurisées (GPIO)
Pour éviter tout clignotement ou comportement parasite des caméras lors du démarrage ou du reboot de l'ESP32, les broches suivantes (dites "safe") sont exclusivement utilisées :
* **GPIO 21** : Relais Caméra 1 (Arrière)
* **GPIO 22** : Relais Caméra 2 (Gauche)
* **GPIO 23** : Relais Caméra 3 (Droite)

### Le "Hack" du câble USB des caméras
Sur chaque câble USB reliant un powerbank à sa caméra :
1. Ouvrir la gaine extérieure.
2. Laisser le **fil noir (Masse/GND)** intact.
3. Sectionner le **fil rouge (+5V)** :
   * Relier le côté venant du powerbank à la borne **COM** (Commun) du relais.
   * Relier le côté allant vers la caméra à la borne **NO** (Normalement Ouvert) du relais.

### Schéma Électrique Complet

```text
[ SUR LE TOIT DU VAN ] (Circuit d'Alimentation Caméras)
─────────────────────────────────────────────────────────────────────────────────────────────
  ┌─────────────────────────┐               ┌──────────────────────────┐
  │ 3x POWERBANKS SOLAIRES  │               │    3x MINI CAMÉRAS       │
  │ (Sortie USB 5V)         │               │    (Entrée USB 5V)       │
  └────┬───────────────┬────┘               └────▲────────────────▲────┘
       │ [Fils Noirs]  │ [Fils Rouges +5V]       │ [Fils Noirs]   │ [Fils Rouges +5V]
       │ (Masse/GND)   │ (Alimentation)          │ (Masse/GND)    │ (Alimentation Coupée)
       │               │                         │                │
───────┼───────────────┼─────────────────────────┼────────────────┼──────────────────────────
       │               │                         │                │
[ À L'INTÉRIEUR DU VAN ] (Dans la boîte de dérivation technique)   │
───────────────────────────────────────────────────────────────────┼─────────────────────────
       │               │                         │                │
       │               └─────────────┐           │                │
       ▼                             ▼           ▼                │
  ┌─────────┐                  ┌───────────────────┐              │
  │ BORNES  │                  │   CARTE 4 RELAIS  │              │
  │  WAGO   │◄─────────────────┤   (Borniers Bleus)│              │
  │ (Masses)│                  │                   │              │
  └────▲────┘                  │  [Relais 1 COM] ◄─┘              │
       │                       │  [Relais 1 NO] ──────────────────┘
       │                       └─────────▲─────────┘
       │                                 │ 
       │ [Fil Noir GND]                  │ [3x Fils Dupont] (Signaux de Commande IN1, IN2, IN3)
       │                                 │ (Depuis Broches GPIO 21, 22, 23)
       │                                 │
       │                       ┌─────────┴─────────┐              ┌─────────────────────────┐
       │                       │      ESP32        │  ) ) Wi-Fi ( (│  RASPBERRY PI 4 / 5     │
       └───────────────────────┤ (GND)        (VIN)│              │  (Home Assistant OS)     │
                               └───────────────▲───┘              └─────────────────────────┘
                                               │
                                               │ [Fil Rouge +5V]
                                               │
                                     ┌─────────┴─────────┐
                                     │CONVERTISSEUR BUCK │
                                     │    12V vers 5V    │
                                     └─────────▲─────────┘
                                               │
                                               │ [+12V Après Fusible & Masse GND]
                                               │
                                     ┌─────────┴─────────┐
                                     │BATTERIE AUXILIAIRE│
                                     │     12V VAN       │
                                     └───────────────────┘
```

---

## 🧲 3. Fixation Mécanique et Passage des Câbles (Zéro Perçage)

### Protocole de collage de sécurité
* **Matériau** : Ruban adhésif double-face de grade industriel **3M VHB 5952** (couleur noire) ou **4910** (transparent).
* **Préparation de la surface** : Nettoyer le polyester du toit relevable ou la tôle, puis dégraisser impérativement à l'**alcool isopropylique** (ne pas utiliser de white-spirit ou d'acétone). Presser fortement pendant 30 secondes et attendre 24h à 72h avant de mettre en charge ou de rouler.
* **Technique de pose amovible** :
  * Coller une embase métallique plate au 3M VHB sur la carrosserie pour y poser le support magnétique de la caméra.
  * Coller des embases de fixation en plastique (plots de serrage) au 3M VHB autour de l'emplacement de la batterie solaire, puis sécuriser la batterie avec des colliers de serrage en plastique (Rilsan noirs résistants aux UV).

### Méthode pour décoller proprement le 3M VHB (Revente du van)
1. Glisser un **fil de pêche en nylon** ou du fil dentaire derrière l'objet et scier la mousse dans son épaisseur.
2. Chauffer le résidu de mousse restant au **sèche-cheveux** (pas de décapeur thermique).
3. Tirer sur l'adhésif parallèlement à la tôle (en l'étirant à plat) pour le peler.
4. Éliminer les traces de colle grasses à l'aide de **WD-40** ou d'un dissolvant aux agrumes, puis essuyer avec une microfibre.

### Cheminement des câbles vers le toit relevable
1. Faire remonter les câbles le long du **bras articulé (pantographe)** mécanique du toit relevable. Les fixer avec des bandes Velcro ou du Rilsan.
2. Laisser une **boucle d'aisance de 10 à 15 cm** aux articulations pour éviter les tensions ou les pincements lors de la fermeture du toit.
3. Faire traverser les câbles vers l'extérieur en profitant de l'espace naturel situé sous le rabat du joint en caoutchouc dans les coins arrières de la toile de toit (sans découper la toile).
4. Immobiliser les fils sur la coque extérieure du toit avec des **mini-goulottes adhésives** ou du **ruban d'étanchéité en aluminium** face aux UV et au vent.

---

## 💻 4. Configuration Logicielle (ESPHome)

Fichier YAML à injecter dans l'add-on ESPHome de Home Assistant pour programmer l'ESP32. La première installation nécessite de brancher l'ESP32 en USB sur le Raspberry Pi. Les suivantes se feront en Wi-Fi (OTA).

```yaml
esphome:
  name: gestionnaire-cameras-van

esp32:
  board: esp32dev

wifi:
  ssid: "Nom_Du_WiFi_De_Votre_Van"
  password: "Votre_Mot_De_Passe_WiFi"
  
  manual_ip:
    static_ip: 192.168.1.50
    gateway: 192.168.1.1
    subnet: 255.255.255.0

api:

logger:

switch:
  - platform: gpio
    pin: GPIO21
    id: relay_camera_1
    name: "Caméra Arrière (Recul)"
    icon: "mdi:camera-rear"
    restore_mode: ALWAYS_OFF

  - platform: gpio
    pin: GPIO22
    id: relay_camera_2
    name: "Caméra Flanc Gauche"
    icon: "mdi:camera-left"
    restore_mode: ALWAYS_OFF

  - platform: gpio
    pin: GPIO23
    id: relay_camera_3
    name: "Caméra Flanc Droit"
    icon: "mdi:camera-right"
    restore_mode: ALWAYS_OFF
```

---

## 🤖 5. Automatisations et Dashboard Home Assistant

### Logique d'automatisation (Via clé OBD2)
* **Mode Dashcam** : Si le régime moteur (`sensor.obd_engine_rpm`) dépasse 400 RPM, les 3 caméras s'allument.
* **Mode Bivouac** : Si le véhicule passe à l'état verrouillé et que le régime moteur est égal à 0, les caméras s'allument. Si le van est déverrouillé en journée à l'arrêt, elles s'éteignent pour économiser les powerbanks.
* **Mode Nuit** : Si le van est verrouillé et que la luminosité passe sous les 10 lux (ou sur activation d'un interrupteur manuel d'alerte près du lit), les caméras s'allument.

```yaml
id: 'gestion_cameras_van_principal'
alias: 'Van - Gestion des caméras (Route & Stationnement)'
description: 'Gère les caméras selon le contact du moteur et le verrouillage'
trigger:
  - platform: numeric_state
    entity_id: sensor.obd_engine_rpm
    above: 400
    id: moteur_demarre
  - platform: state
    entity_id: binary_sensor.van_verrouille
    to: 'on'

```
id: vehicule_verrouille  
  
* platform: state entity_id: binary_sensor.van_verrouille to: 'off' id: vehicule_deverrouille condition: [] action:  
* choose:  
    * conditions:  
        * or:  
            * condition: trigger id: moteur_demarre  
            * condition: and conditions:  
                * condition: trigger id: vehicule_verrouille  
                * condition: numeric_state entity_id: sensor.obd_engine_rpm below: 10 sequence:  
            *   
        *   
        * service: switch.turn_on target: entity_id: - switch.camera_arriere_recul - switch.camera_flanc_gauche - switch.camera_flanc_droit  
    *   
    * conditions:  
        * condition: trigger id: vehicule_deverrouille  
        * condition: numeric_state entity_id: sensor.obd_engine_rpm below: 10 sequence:  
        * service: switch.turn_off target: entity_id: - switch.camera_arriere_recul - switch.camera_flanc_gauche - switch.camera_flanc_droit ```  
    *   
*   
## Interface UI Lovelace pour Smartphone  
Code à insérer dans l'éditeur de carte (Manuel) de votre tableau de bord Home Assistant :  
```yaml  
type: vertical-stack  
cards:  
  
* type: grid title: "🚐 Statut Westfalia" columns: 2 square: false cards:  
    * type: tile entity: sensor.obd_engine_rpm name: "Moteur (RPM)" color: orange  
    * type: tile entity: binary_sensor.van_verrouille name: "Verrouillage" color: blue  
    * type: tile entity: sensor.luminosite_exterieure name: "Luminosité" color: amber  
*   
* type: entities title: "📹 Interrupteurs Caméras" show_header_toggle: true entities:  
    * entity: switch.camera_arriere_recul secondary_info: last-changed  
    * entity: switch.camera_flanc_gauche secondary_info: last-changed  
    * entity: switch.camera_flanc_droit secondary_info: last-changed  
*   
```
	•	type: button entity: input_boolean.bouton_panique_nuit name: "🔴 Mode Alerte Nuit (Lit haut)" show_state: false icon_height: 40px tap_action: action: toggle ```

```
```
Bon montage à vous dans votre Westfalia ! Si vous lancez les achats ou l'assemblage et qu'un détail technique vous bloque en cours de route, n'hésitez pas à **revenir vers moi** pour ajuster les plans.

```
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
  
**Vous avez dit : ok et peux tu en faire un fichier .md ?**  
  
  
  
  
  
  
  
  
  
  
  
  
Voici la compilation intégrale de nos échanges depuis le résumé du projet, formatée de manière propre et prête pour votre documentation personnelle.  
## Vous trouverez ci-dessous le fichier au format Markdown (.md). Vous pouvez le copier-coller dans n'importe quel éditeur de texte (comme Notepad, VS Code ou l'éditeur de fichiers de Home Assistant) et l'enregistrer sous le nom projet_cameras_westfalia.md.  
  
## markdown  
```
# 🚐 Projet d'Installation de 3 Mini-Caméras Wi-Fi - Westfalia Kelsey

Ce document compile l'ensemble des étapes techniques, des choix de composants et des configurations logicielles pour l'installation d'un système de surveillance autonome à 360° sur le toit relevable d'un minivan Westfalia.

---

## 📋 1. Résumé Global du Projet (Point de Départ)

* **Les caméras** : 3 mini-caméras de sécurité Wi-Fi génériques (alimentées en USB 5V) réparties autour du van pour une surveillance complète.
* **L'alimentation indépendante** : Pour éviter de percer le toit relevable, chaque caméra possède son propre bloc d'alimentation composé d'une batterie externe solaire de chantier (IP65, minimum 10 000 à 20 000 mAh avec fonction *Pass-Through*).
* **Le cerveau du système** : Un microcontrôleur **ESP32** relié à un module relais 5V, branché sur la batterie auxiliaire 12V du van et piloté à distance par le système **Home Assistant** embarqué (qui tourne en continu sur un Raspberry Pi).
* **Le déclenchement intelligent** : Une clé **OBD2** connectée au Raspberry Pi transmet l'état du van en temps réel pour automatiser l'allumage des caméras.

---

## 🛠️ 2. Choix du Matériel et Montage Électrique

### Liste précise des composants à acheter
* **Microcontrôleur** : ESP32 NodeMCU (Modèle standard 30 ou 38 broches avec *headers* soudés).
* **Module Relais** : Carte 4 canaux Relais 5V équipée d'une **isolation par optocoupleur (Low Level Trigger)** pour protéger l'électronique en cas de court-circuit extérieur dû à la pluie.
* **Alimentation ESP32** : Convertisseur régulateur de tension 12V vers 5V (Type "Buck" étanche) connecté à la batterie auxiliaire 12V du Westfalia.
* **Powerbanks Solaires** : Modèles Outdoor IP65 gérant impérativement la charge traversante (*Pass-Through Charging*) comme la gamme **Xtorm Rugged Solar (XR101 / XR201)** ou **Sandberg Outdoor Solar 16000**.

### Sélection des broches sécurisées (GPIO)
Pour éviter tout clignotement ou comportement parasite des caméras lors du démarrage ou du reboot de l'ESP32, les broches suivantes (dites "safe") sont exclusivement utilisées :
* **GPIO 21** : Relais Caméra 1 (Arrière)
* **GPIO 22** : Relais Caméra 2 (Gauche)
* **GPIO 23** : Relais Caméra 3 (Droite)

### Le "Hack" du câble USB des caméras
Sur chaque câble USB reliant un powerbank à sa caméra :
1. Ouvrir la gaine extérieure.
2. Laisser le **fil noir (Masse/GND)** intact.
3. Sectionner le **fil rouge (+5V)** :
   * Relier le côté venant du powerbank à la borne **COM** (Commun) du relais.
   * Relier le côté allant vers la caméra à la borne **NO** (Normalement Ouvert) du relais.

### Schéma Électrique Complet

```text
[ SUR LE TOIT DU VAN ] (Circuit d'Alimentation Caméras)
─────────────────────────────────────────────────────────────────────────────────────────────
  ┌─────────────────────────┐               ┌──────────────────────────┐
  │ 3x POWERBANKS SOLAIRES  │               │    3x MINI CAMÉRAS       │
  │ (Sortie USB 5V)         │               │    (Entrée USB 5V)       │
  └────┬───────────────┬────┘               └────▲────────────────▲────┘
       │ [Fils Noirs]  │ [Fils Rouges +5V]       │ [Fils Noirs]   │ [Fils Rouges +5V]
       │ (Masse/GND)   │ (Alimentation)          │ (Masse/GND)    │ (Alimentation Coupée)
       │               │                         │                │
───────┼───────────────┼─────────────────────────┼────────────────┼──────────────────────────
       │               │                         │                │
[ À L'INTÉRIEUR DU VAN ] (Dans la boîte de dérivation technique)   │
───────────────────────────────────────────────────────────────────┼─────────────────────────
       │               │                         │                │
       │               └─────────────┐           │                │
       ▼                             ▼           ▼                │
  ┌─────────┐                  ┌───────────────────┐              │
  │ BORNES  │                  │   CARTE 4 RELAIS  │              │
  │  WAGO   │◄─────────────────┤   (Borniers Bleus)│              │
  │ (Masses)│                  │                   │              │
  └────▲────┘                  │  [Relais 1 COM] ◄─┘              │
       │                       │  [Relais 1 NO] ──────────────────┘
       │                       └─────────▲─────────┘
       │                                 │ 
       │ [Fil Noir GND]                  │ [3x Fils Dupont] (Signaux de Commande IN1, IN2, IN3)
       │                                 │ (Depuis Broches GPIO 21, 22, 23)
       │                                 │
       │                       ┌─────────┴─────────┐              ┌─────────────────────────┐
       │                       │      ESP32        │  ) ) Wi-Fi ( (│  RASPBERRY PI 4 / 5     │
       └───────────────────────┤ (GND)        (VIN)│              │  (Home Assistant OS)     │
                               └───────────────▲───┘              └─────────────────────────┘
                                               │
                                               │ [Fil Rouge +5V]
                                               │
                                     ┌─────────┴─────────┐
                                     │CONVERTISSEUR BUCK │
                                     │    12V vers 5V    │
                                     └─────────▲─────────┘
                                               │
                                               │ [+12V Après Fusible & Masse GND]
                                               │
                                     ┌─────────┴─────────┐
                                     │BATTERIE AUXILIAIRE│
                                     │     12V VAN       │
                                     └───────────────────┘
```

---

## 🧲 3. Fixation Mécanique et Passage des Câbles (Zéro Perçage)

### Protocole de collage de sécurité
* **Matériau** : Ruban adhésif double-face de grade industriel **3M VHB 5952** (couleur noire) ou **4910** (transparent).
* **Préparation de la surface** : Nettoyer le polyester du toit relevable ou la tôle, puis dégraisser impérativement à l'**alcool isopropylique** (ne pas utiliser de white-spirit ou d'acétone). Presser fortement pendant 30 secondes et attendre 24h à 72h avant de mettre en charge ou de rouler.
* **Technique de pose amovible** :
  * Coller une embase métallique plate au 3M VHB sur la carrosserie pour y poser le support magnétique de la caméra.
  * Coller des embases de fixation en plastique (plots de serrage) au 3M VHB autour de l'emplacement de la batterie solaire, puis sécuriser la batterie avec des colliers de serrage en plastique (Rilsan noirs résistants aux UV).

### Méthode pour décoller proprement le 3M VHB (Revente du van)
1. Glisser un **fil de pêche en nylon** ou du fil dentaire derrière l'objet et scier la mousse dans son épaisseur.
2. Chauffer le résidu de mousse restant au **sèche-cheveux** (pas de décapeur thermique).
3. Tirer sur l'adhésif parallèlement à la tôle (en l'étirant à plat) pour le peler.
4. Éliminer les traces de colle grasses à l'aide de **WD-40** ou d'un dissolvant aux agrumes, puis essuyer avec une microfibre.

### Cheminement des câbles vers le toit relevable
1. Faire remonter les câbles le long du **bras articulé (pantographe)** mécanique du toit relevable. Les fixer avec des bandes Velcro ou du Rilsan.
2. Laisser une **boucle d'aisance de 10 à 15 cm** aux articulations pour éviter les tensions ou les pincements lors de la fermeture du toit.
3. Faire traverser les câbles vers l'extérieur en profitant de l'espace naturel situé sous le rabat du joint en caoutchouc dans les coins arrières de la toile de toit (sans découper la toile).
4. Immobiliser les fils sur la coque extérieure du toit avec des **mini-goulottes adhésives** ou du **ruban d'étanchéité en aluminium** face aux UV et au vent.

---

## 💻 4. Configuration Logicielle (ESPHome)

Fichier YAML à injecter dans l'add-on ESPHome de Home Assistant pour programmer l'ESP32. La première installation nécessite de brancher l'ESP32 en USB sur le Raspberry Pi. Les suivantes se feront en Wi-Fi (OTA).

```yaml
esphome:
  name: gestionnaire-cameras-van

esp32:
  board: esp32dev

wifi:
  ssid: "Nom_Du_WiFi_De_Votre_Van"
  password: "Votre_Mot_De_Passe_WiFi"
  
  manual_ip:
    static_ip: 192.168.1.50
    gateway: 192.168.1.1
    subnet: 255.255.255.0

api:

logger:

switch:
  - platform: gpio
    pin: GPIO21
    id: relay_camera_1
    name: "Caméra Arrière (Recul)"
    icon: "mdi:camera-rear"
    restore_mode: ALWAYS_OFF

  - platform: gpio
    pin: GPIO22
    id: relay_camera_2
    name: "Caméra Flanc Gauche"
    icon: "mdi:camera-left"
    restore_mode: ALWAYS_OFF

  - platform: gpio
    pin: GPIO23
    id: relay_camera_3
    name: "Caméra Flanc Droit"
    icon: "mdi:camera-right"
    restore_mode: ALWAYS_OFF
```

---

## 🤖 5. Automatisations et Dashboard Home Assistant

### Logique d'automatisation (Via clé OBD2)
* **Mode Dashcam** : Si le régime moteur (`sensor.obd_engine_rpm`) dépasse 400 RPM, les 3 caméras s'allument.
* **Mode Bivouac** : Si le véhicule passe à l'état verrouillé et que le régime moteur est égal à 0, les caméras s'allument. Si le van est déverrouillé en journée à l'arrêt, elles s'éteignent pour économiser les powerbanks.
* **Mode Nuit** : Si le van est verrouillé et que la luminosité passe sous les 10 lux (ou sur activation d'un interrupteur manuel d'alerte près du lit), les caméras s'allument.

```yaml
id: 'gestion_cameras_van_principal'
alias: 'Van - Gestion des caméras (Route & Stationnement)'
description: 'Gère les caméras selon le contact du moteur et le verrouillage'
trigger:
  - platform: numeric_state
    entity_id: sensor.obd_engine_rpm
    above: 400
    id: moteur_demarre
  - platform: state
    entity_id: binary_sensor.van_verrouille
    to: 'on'

```
Utilisez le code avec précaution.  
  
## id: vehicule_verrouille  
* platform: state entity_id: binary_sensor.van_verrouille to: 'off' id: vehicule_deverrouille condition: [] action:  
* choose:  
    * conditions:  
        * or:  
            * condition: trigger id: moteur_demarre  
            * condition: and conditions:  
                * condition: trigger id: vehicule_verrouille  
                * condition: numeric_state entity_id: sensor.obd_engine_rpm below: 10 sequence:  
        * service: switch.turn_on target: entity_id: - switch.camera_arriere_recul - switch.camera_flanc_gauche - switch.camera_flanc_droit  
    * conditions:  
        * condition: trigger id: vehicule_deverrouille  
        * condition: numeric_state entity_id: sensor.obd_engine_rpm below: 10 sequence:  
        * service: switch.turn_off target: entity_id: - switch.camera_arriere_recul - switch.camera_flanc_gauche - switch.camera_flanc_droit ```  
  
## Interface UI Lovelace pour Smartphone  
## Code à insérer dans l'éditeur de carte (Manuel) de votre tableau de bord Home Assistant :  
## ```yaml  
## type: vertical-stack  
## cards:  
* type: grid title: "🚐 Statut Westfalia" columns: 2 square: false cards:  
    * type: tile entity: sensor.obd_engine_rpm name: "Moteur (RPM)" color: orange  
    * type: tile entity: binary_sensor.van_verrouille name: "Verrouillage" color: blue  
    * type: tile entity: sensor.luminosite_exterieure name: "Luminosité" color: amber  
* type: entities title: "📹 Interrupteurs Caméras" show_header_toggle: true entities:  
    * entity: switch.camera_arriere_recul secondary_info: last-changed  
    * entity: switch.camera_flanc_gauche secondary_info: last-changed  
    * entity: switch.camera_flanc_droit secondary_info: last-changed  
* type: button entity: input_boolean.bouton_panique_nuit name: "🔴 Mode Alerte Nuit (Lit haut)" show_state: false icon_height: 40px tap_action: action: toggle ```  
  
```


```
  
  
  
  
  
  
  
  
