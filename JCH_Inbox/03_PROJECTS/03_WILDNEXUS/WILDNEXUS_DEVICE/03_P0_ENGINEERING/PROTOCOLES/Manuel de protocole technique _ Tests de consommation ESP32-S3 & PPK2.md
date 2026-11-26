### Manuel de protocole technique : Tests de consommation ESP32-S3 & PPK2

#### 1\. Informations de Référence et Contexte

Ce document définit le protocole opérationnel strict pour la session de métrologie énergétique du projet  **WildNexus** . L'objectif est de valider la consommation du microcontrôleur ESP32-S3 en modes sommeil et actif afin de garantir la viabilité de la logique P0.

* **Projet :**  WildNexus  
* **Date de session :**  08 juin 2026  
* **Matériel requis :**  1 × ESP32-S3 DevKit, 1 × Nordic Power Profiler Kit II (PPK2), 1 × Poste de travail (Mac), câbles Dupont.  
* **Durée estimée :**  \~2 heures (session complète).

##### Fichiers de référence

Chemin d'accès au fichier,Usage  
03\_P0\_ENGINEERING/03\_ENERGIE\_AUTONOMIE/2026-06-08\_protocole-m02-esp32s3-ppk2.md,Protocole technique complet (référence exhaustive).  
03\_P0\_ENGINEERING/03\_ENERGIE\_AUTONOMIE/2026-06-08\_mesures-esp32s3-ppk2\_template.csv,"Gabarit de saisie des mesures (Phases C, D et E)."

##### Vocabulaire technique

* **DUT (Device Under Test) :**  L'unité ESP32-S3 soumise aux tests.  
* **PPK2 (Power Profiler Kit II) :**  Instrument de précision utilisé pour alimenter le DUT et mesurer son courant.  
* **Source Meter :**  Mode de fonctionnement du PPK2 où il agit simultanément comme alimentation stabilisée et ampèremètre.  
* **Deep sleep :**  Mode de veille profonde de l'ESP32-S3 minimisant la consommation énergétique.  
* **Cycle événement :**  Séquence complète comprenant le réveil du MCU, l'exécution des tâches applicatives et le retour en sommeil.

#### 2\. Consignes de Sécurité et Précautions Matérielles

##### Règles de sécurité critiques

1. **Interdiction de double alimentation :**  Ne jamais alimenter l'ESP32 par USB et par PPK2 simultanément lors d'une mesure.  
2. **Usage exclusif USB :**  Le port USB de l'ESP32 est réservé uniquement au flashage du firmware.  
3. **Usage exclusif PPK2 :**  Le PPK2 doit être la seule source d'alimentation lors des phases de mesure.  
4. **État initial :**  Désactiver impérativement la sortie (OFF) du PPK2 avant toute manipulation de câblage sur l'ESP32.  
5. **Vérification de polarité :**  Contrôler deux fois les branchements : VOUT vers la broche 5V, GND vers GND.  
6. **Seuil de protection :**  Si le courant mesuré dépasse  **500 mA**  sans raison explicite, couper immédiatement la sortie et vérifier l'absence de court-circuit.  
7. **Protection GPIO :**  Ne jamais injecter une tension de 5V sur une broche GPIO de l'ESP32.\!WARNING  **Danger de destruction matérielle**  La double alimentation (USB \+ PPK2) ou une inversion de polarité provoquera des dommages irréversibles au DUT ou au PPK2. L'opérateur doit s'assurer que la sortie Power Profiler est sur "OFF" avant chaque changement de connectique.**Note sur les contraintes matérielles :**  Le DevKit utilisé intègre un régulateur de tension et des LEDs témoins qui augmentent artificiellement la consommation. Une mesure de  **150 µA**  en Deep sleep est considérée comme une contrainte matérielle documentée de la plateforme DevKit. Ces résultats seront validés ultérieurement sur un PCB nu optimisé.

#### 3\. Grille de Décision Go/No-Go

L'opérateur doit évaluer la viabilité de l'unité testée selon les seuils suivants :| Mesure | Go | Orange | No-Go || \------ | \------ | \------ | \------ || **Deep sleep** | \< 100 µA | 100 \- 150 µA | \> 200 µA || **Charge par événement** | \< 1.5 mAh | 1.5 \- 2.5 mAh | \> 2.5 mAh || **Autonomie (3 évt/h)** | ≥ 60 jours | 45 \- 60 jours | \< 45 jours || **Stabilité** | 100 cycles sans erreur | 1 \- 2 erreurs isolées | Blocage récurrent |  
**Instructions de clôture :**

* **Validation :**  Si les indicateurs sont "Go" ou "Orange", l'ESP32-S3 est validé pour l'intégration P0.  
* **Escalade :**  Si un critère est en "No-Go", alerter immédiatement  **[[Dobby]]**  pour organiser un arbitrage technique avec les équipes  **[[Castor]]**  et  **[[Forge]]** .

#### 4\. Phase A : Vérification du Matériel — ESP32 Alive (10 min)

**Objectif :**  Valider l'intégrité du DUT avant l'instrumentation.

1. Poser l'ESP32-S3 sur une surface isolante non conductrice.  
2. Connecter le câble USB-C entre le Mac et l'ESP32 ( **Le PPK2 doit rester physiquement débranché** ).  
3. Arduino IDE : Sélectionner la carte "ESP32-S3 DevKit" et le port série actif.  
4. Compiler et flasher le firmware wn\_blink.  
5. Ouvrir le moniteur série (115200 bauds).  
6. **Succès attendu :**  Affichage du message "WildNexus ESP32-S3 alive" chaque seconde.  
7. *Action corrective :*  Si le flashage échoue, maintenir le bouton  **BOOT**  enfoncé pendant l'upload.

#### 5\. Phase B : Préparation au Sommeil Profond — Deep Sleep Prep (10 min)

**Objectif :**  Configurer le logiciel pour les mesures de courant de veille.

1. Flasher le firmware wn\_deep\_sleep\_30s via la liaison USB.  
2. Ouvrir le moniteur série et confirmer la réception du message "WildNexus deep sleep test".  
3. Observer un cycle complet (30 secondes) pour valider le réveil automatique.  
4. Fermer le moniteur série.

**\! POINT DE RUPTURE : BASCULE D'ALIMENTATION**   **DÉBRANCHER LE CÂBLE USB DE L'ESP32 AVANT TOUTE INTERVENTION SUR LE PPK2.**

#### 6\. Phase C : Installation du PPK2 et Mesure Deep Sleep (20 min)

##### Configuration Logicielle (Power Profiler)

* **Mode :**  Source Meter.  
* **Tension de sortie :**  5.0 V.  
* **Limite de courant :**  500 mA.  
* **État initial :**  Sortie sur OFF.  
* **Action :**  Cliquer sur "[[Start]]" pour préparer l'acquisition.

##### Procédure de Branchement (Ordre impératif)

1. **Brancher le fil noir :**  PPK2 GND → ESP32 GND.  
2. **Brancher le fil rouge :**  PPK2 VOUT → ESP32 5V.  
3. Vérifier visuellement que VOUT ne touche aucune broche GPIO.

##### Procédure de Mesure

1. Activer la sortie PPK2 dans le logiciel Power Profiler.  
2. Observer la courbe pendant au moins 2 minutes.  
3. Identifier les pics de réveil cycliques (30s).  
4. Effectuer un zoom sur les plateaux de repos pour mesurer le courant de base.

##### Diagnostic technique

Observation,Signification  
Pics cycliques toutes les 30s,✅ Firmware et matériel opérationnels.  
Courant nul / Pas de pic,Câblage défectueux ou sortie logicielle sur OFF.  
Courant très élevé constant,Court-circuit ou échec de l'entrée en mode sleep.  
Deep sleep mesuré en mA,Consommation excessive du DevKit (à documenter).

#### 7\. Phases D & E : Mesures de Cycle (Réveil et Simulation)

##### Phase D : Réveil court (30 min)

1. **\! POINT DE RUPTURE :**  Débrancher le PPK2, rebrancher l'USB.  
2. Flasher le firmware wn\_wake\_short.  
3. **\! POINT DE RUPTURE :**  Débrancher l'USB, rebrancher le PPK2 (GND puis VOUT).  
4. Mesurer sur  **20 cycles** .  
5. **Attentes :**  Pic actif de 2 à 3 secondes, suivi d'un retour net au niveau Deep Sleep.

##### Phase E : Cycle simulé WildNexus — Logique P0 (30 min)

Ce test simule une séquence active de  **11 secondes**  décomposée comme suit :

* Réveil PIR : 2s  
* Capture Caméra : 5s  
* Écriture SD : 2s  
* Transmission LoRa : 2s  
1. **\! POINT DE RUPTURE :**  Débrancher le PPK2, rebrancher l'USB.  
2. Flasher wn\_event\_simulated.  
3. **\! POINT DE RUPTURE :**  Débrancher l'USB, rebrancher le PPK2.  
4. Mesurer sur  **10 cycles** .

##### Extraction des données (CSV)

Pour chaque cycle, extraire précisément les headers suivants :

* courant\_actif\_moyen\_mA  
* duree\_active\_s  
* charge\_evenement\_mAh (Utiliser l'onglet "Charge" du Power Profiler pour une intégration précise).

#### 8\. Analyse des Données et Calculs d'Autonomie

##### Méthodologie de calcul

L'autonomie est calculée pour une batterie Lithium 4S1P (3000 mAh) avec une fréquence de 3 événements par heure.**Étape 1 : Calcul de la consommation journalière**   $$\\text{Consommation (mAh/jour)} \= \\text{Charge/événement (mAh)} \\times 3 \\text{ évt/h} \\times 24 \\text{ h}$$**Étape 2 : Calcul de l'autonomie**   $$\\text{Autonomie (jours)} \= \\frac{3000 \\text{ mAh}}{\\text{Consommation (mAh/jour)}}$$

##### Scénarios de référence

* **Scénario Nominal (Succès) :**  
* Charge/événement :  **0.37 mAh**  
* Consommation journalière :  $0.37 \\times 72 \= 26.64 \\text{ mAh/jour}$  
* Autonomie :  **\~113 jours**  (Validation ✅)  
* **Scénario Critique (Échec) :**  
* Charge/événement :  **1.5 mAh**  
* Consommation journalière :  $1.5 \\times 72 \= 108 \\text{ mAh/jour}$  
* Autonomie :  **\~28 jours**  (Critère No-Go ❌)

##### Clôture de la session

1. Compléter le fichier 2026-06-08\_mesures-esp32s3-ppk2\_template.csv.  
2. Comparer les résultats finaux aux seuils de la Section 3\.  
3. En cas de non-conformité, déclencher le protocole d'escalade vers les équipes [[Castor]] et [[Forge]] pour arbitrage sur une potentielle migration MCU.

