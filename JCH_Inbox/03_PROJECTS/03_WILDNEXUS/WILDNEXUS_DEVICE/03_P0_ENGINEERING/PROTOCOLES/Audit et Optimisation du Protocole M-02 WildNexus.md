Cette analyse croise le protocole de test **M-02** avec les exigences stratégiques et techniques des **ADR** (Architecture Decision Records) et du **Scope Lock** de WildNexus.

### 1\. Incohérences ou contradictions avec les ADR

* **Omission de l'Edge AI (Contradiction majeure ADR-010) :** Le protocole M-02 actuel se concentre sur les périphériques matériels mais ignore le benchmark de l'inférence MobileNet-SSD 1\. L'ADR-010 stipule explicitement que l'impact énergétique de l'IA et sa latence (\< 2s) doivent être mesurés **avant la fermeture du jalon M-02** car ils constituent un "trigger" de migration vers un autre MCU 1-4.  
* **Absence du Microphone (Contradiction Scope Lock) :** Le document WILDNEXUS\_P0\_SCOPE\_LOCK inclut la "capture audio locale courte via micro mono" dans le périmètre P0 5\. Or, aucune phase du protocole M-02 ne prévoit le test de consommation du micro MEMS (Réf A06 dans le panier Mouser 6).  
* **Omission du Provisioning (Oubli ADR-011) :** L'ADR-011 demande qu'un test de provisioning complet (lecture Serial, dérivation et gravure eFuse) soit inclus dans WP04 pour M-02 7, 8\. Le protocole actuel ne mentionne pas cette manipulation critique pour la sécurité.

### 2\. Étapes trop vagues pour un opérateur débutant

* **Phase E (Simulation cycle) :** L'instruction "Firmware simulation" 9 ne précise pas quelles tâches l'ESP32-S3 doit simuler (ex: boucle active de 10s pour simuler une capture caméra ?). Sans cela, la mesure de charge (mAh) ne sera pas reproductible entre opérateurs.  
* **Calcul manuel (Phase E) :** Demander un calcul manuel (120 mA \* 11s / 3600\) 9 est une source d'erreur. La procédure devrait imposer l'utilisation de l'onglet "Charge" ou "Energy" de l'application Power Profiler 10\.  
* **Manipulation du port série :** L'instruction "maintenir BOOT pendant l'upload" 11 est vague. Un débutant risque de ne pas savoir quand relâcher ou si le port série change de nom après cette action.

### 3\. Risques de mauvais branchement ou de mesure invalide

* **Mode Ampere Meter (Phase J) :** Le branchement en série du PPK2 entre l'alimentation et le buck 12 est l'étape la plus risquée. Une erreur de polarité sur VIN/VOUT peut endommager le PPK2 ou le circuit 13\.  
* **Conflit USB/PPK2 :** Bien que cité en règle de sécurité 13, le risque d'alimenter simultanément par USB (pour le moniteur série) et par PPK2 reste élevé. L'opérateur doit impérativement utiliser le mode "Data only" de l'USB si possible, ou déconnecter physiquement le VOUT du PPK2 lors des flashs 14, 15\.  
* **Overhead du DevKit :** Le protocole note que le DevKit consomme plus 16, 17, mais ne donne pas de procédure pour neutraliser physiquement la LED "Power" ou le régulateur AMS1117 (si possible par coupure de piste), ce qui pourrait fausser le critère de "No-go" à \> 200 µA 16\.

### 4\. Modules ou pinouts à vérifier avant exécution

* **MicroSD (Phase F) :** Vérifier si le module possède un régulateur interne. Si branché sur le rail 3.3V de l'ESP32 alors qu'il attend du 5V en entrée, l'initialisation échouera 18, 19\.  
* **Caméra DVP (Phase H) :** Le protocole a raison d'interdire le câblage sans pinout exact 20\. Pour le modèle OV5640 (DVP M12) 21, 22, il faut valider si le module nécessite une tension XCLK externe fournie par l'ESP32.  
* **LoRa (Phase G) :** Le mapping suggéré utilise GPIO9 et GPIO10 pour les CS (LoRa/SD) 23\. Il faut vérifier que ces broches ne sont pas utilisées par la Flash/PSRAM interne de la version N8R8 choisie 6, 24\.

### 5\. Checklist opérateur pas-à-pas (Extraits critiques)

Étape,Action,Validation  
0.1,Installer nRF Connect \+ Power Profiler 25,Logiel OK  
1.1,Flash wn\_blink via USB-C (PPK2 débranché) 26,LED/Serial OK  
2.1,"PPK2 Source Mode @ 5.0V, Sortie OFF 27",Config OK  
2.2,"Câbler PPK2 (VOUT-\>5V, GND-\>GND) 27",Double check polarité  
3.1,"Flash wn\_deep\_sleep\_30s, PPK2 ON 14, 17",Mesure µA stable  
4.1,Nouveau : Test Inférence MobileNet-SSD VGA 1,Latence \< 2s  
5.1,"Insertion MicroSD \+ Flash wn\_sd\_test 18, 19",Fichier présent  
6.1,Nouveau : Test Provisioning (Script wildnexus\_provision.py) 7,eFuse verrouillé

### 6\. Matrice Go/No-Go ESP32-S3

Critère,Cible (Go),Zone Orange,No-Go (Migration STM32U5),Source  
Veille (carte),\< 100 µA,100-150 µA,\> 200 µA,"16, 28, 29"  
Cycle Event,\< 1.5 mAh,1.5-2.5 mAh,\> 2.5 mAh,"16, 30"  
Inférence IA,\< 2 s,2-4 s,OOM ou \> 4 s,"1, 3, 31"  
Autonomie (AA),\>= 60 jours,45-60 jours,\< 45 jours,"16, 32"  
Stabilité,100 cycles OK,1-2 erreurs,Blocage récurrent,"16, 33"

### 7\. Questions à résoudre avant le premier test réel

1. **L'audio (P0) :** Pourquoi le micro MEMS (A06) est-il absent du protocole alors qu'il est dans le Scope Lock ? 5, 34  
2. **Le matériel IA :** L'opérateur dispose-t-il d'un firmware compilé avec le modèle MobileNet-SSD quantisé pour mesurer la latence réelle ? 1, 3  
3. **L'alimentation finale :** Le buck TPS62840 (A08) est-il prêt sur breadboard pour la Phase J, ou teste-t-on uniquement sur le régulateur (inefficace) du DevKit ? 6, 35, 36  
4. **La Flash/PSRAM :** Le firmware utilisé gère-t-il bien la mise en sommeil de la PSRAM (souvent consommatrice en deep sleep) ? 37, 38

**Action recommandée :** Ajouter une **Phase K (Edge AI Bench)** et une **Phase L (Audio/Provisioning)** au document 2026-06-08\_protocole-m02-esp32s3-ppk2.md avant de lancer les mesures.  
