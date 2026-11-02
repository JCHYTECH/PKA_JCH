Oui, les sources fournissent des listes détaillées du matériel, des composants électroniques et des outils logiciels nécessaires, principalement regroupées dans le **protocole M-02** et les **ordres d'achat du panier P0**.

### 1\. Matériel de base (Session initiale M-02)

Pour débuter les tests de mesure de consommation, les éléments suivants sont obligatoires :

* **Microcontrôleur :** 1 x ESP32-S3 DevKitC-1-N8R8 1, 2\.  
* **Outil de mesure :** 1 x Nordic Power Profiler Kit II (PPK2) 1, 3\.  
* **Informatique :** Un ordinateur (Mac mentionné dans le protocole) avec un câble USB-C (data) pour l'ESP32 et un câble USB pour le PPK2 1\.  
* **Connectique :** Câbles Dupont femelle-femelle et une table non conductrice pour les manipulations 1, 4\.

### 2\. Modules d'extension et capteurs (Tests étendus P0)

Ces composants sont requis pour valider les différentes phases du prototype complet :

* **Stockage :** Module microSD SPI 3.3V et carte microSD (8-32 Go, FAT32) 1, 5\.  
* **Vision :** Module caméra DVP OV5640 M12 1, 6\.  
* **Radio :** Module LoRa SX1262 ou RAK3172 1, 7, 8\.  
* **Détection :** Capteur PIR Panasonic EKMB1303111K 1, 2, 9\.  
* **Audio :** Micro MEMS I2S Knowles SPH0645LM4H-B (inclus dans le périmètre P0) 2, 10\.  
* **Éclairage :** LEDs IR 850 nm (Vishay VSLY3850) et 940 nm (Vishay VSLB3940) 2\.

### 3\. Alimentation et Électronique

Pour tester l'autonomie réelle selon l'ADR-005 :

* **Batteries :** 8 à 16 piles AA Lithium (Energizer L91) ou NiMH (Eneloop Pro) 2, 11\.  
* **Régulation :** Buck converter **TPS62840** (Iq très faible de 5 µA) 2, 12\.  
* **Accessoires :** Supports de piles AA (Keystone 2463), breadboards, câbles, et MOSFET Nexperia PMV16XN pour la coupure des périphériques 2, 13\.  
* **Outils d'atelier :** Alimentation de laboratoire (RD UM24C) 2\.

### 4\. Outils de Provisioning et Sécurité

Pour la phase de sécurisation du nœud (ADR-011) :

* **Hardware :** YubiKey PIV ou HSM physique pour stocker la Master Key hors ligne 14, 15\.  
* **Script :** Un script de provisioning spécifique (wildnexus\_provision.py) 16\.

### 5\. Logiciels requis

* **Développement :** Arduino IDE ou PlatformIO avec le package de cartes ESP32 d'Espressif 17\.  
* **Analyse énergie :** nRF Connect for Desktop et l'application **Power Profiler** 17, 18\.  
* **Gestion de projet :** Plane (synchronisé localement) pour le suivi des tâches 19, 20\.

Le budget total estimé pour ce premier lot de matériel (batch 1\) est d'environ **294 €** sur une enveloppe globale de 1 000 € 3, 6\.  
