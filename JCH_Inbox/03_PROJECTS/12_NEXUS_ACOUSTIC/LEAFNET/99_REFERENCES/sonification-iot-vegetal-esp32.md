\# Projet de Sonification et IoT Végétal avec ESP32-S3\
\
Ce document synthétise les aspects techniques, matériels (hardware) et logiciels (software) pour concevoir un capteur IoT miniature de biodata sonification et de suivi scientifique végétal optimisé pour fonctionner sur batterie.\
\
\-\--\
\
\## 1. Principes Techniques : La Biodata Sonification\
\
La transformation de l\'activité d\'une plante en musique ou en données scientifiques repose sur le principe de la \*\*biodata sonification\*\*.\
\
1. \*\*Capture du signal électrique :\*\* On mesure les micro-fluctuations de la conductivité et de la résistance électrique des tissus végétaux à l\'aide de sondes conductrices non destructives (pinces crocodiles lisses ou patchs d\'électrodes ECG).\
2. \*\*Conditionnement du signal (Hardware) :\*\* Les signaux biologiques étant de l\'ordre du microvolt, ils transitent par un circuit amplificateur opérationnel (AOP à haute impédance comme le TLC2272 ou INA126) et un filtre passe-bas matériel pour éliminer les parasites environnementaux (50Hz, ondes radio).\
3. \*\*Numérisation :\*\* Le signal amplifié (ramené entre 0V et 3.3V) est lu par le convertisseur analogique-numérique (ADC) d\'un microcontrôleur.\
4. \*\*Interprétation et Communication :\*\* Les variations sont traduites en données exploitables (données agronomiques de stress ou messages musicaux MIDI pour piloter des synthétiseurs).\
\
\-\--\
\
\## 2. Choix du Matériel Miniature & Gestion d\'Énergie\
\
Pour concevoir un objet connecté (IoT) autonome et discret, la plateforme recommandée est la gamme \*\*Seeed Studio XIAO\*\* (versions ESP32-C3 ou ESP32-S3) :\
\* \*\*Taille ultra-réduite :\*\* \~ 2,1 cm x 1,7 cm (taille d\'un timbre-poste).\
\* \*\*PMIC intégré :\*\* Circuit de charge pour batterie LiPo 3.7V directement au dos de la carte.\
\* \*\*Consommation en Deep Sleep :\*\* Chute à environ \*\*44 µA\*\*, idéal pour maximiser l\'autonomie.\
\* \*\*Connectivité :\*\* Supporte le Wi-Fi, le Bluetooth (BLE) et le protocole basse consommation \*\*ESP-NOW\*\*.\
\
\### Architecture d\'Énergie (Règle d\'or sur Batterie)\
Pour éviter que le circuit amplificateur de la plante ne vide la batterie pendant que le microcontrôleur dort, le capteur n\'est pas branché sur le \`3.3V\` permanent. Il est alimenté par une broche numérique (ex: \`D0\`) activée uniquement au moment de la mesure.\
\
\-\--\
\
\## 3. Schéma de Câblage et Profilage (PPK2)\
\
Le \*\*Power Profiler Kit II (PPK2)\*\* de Nordic Semiconductor permet de mesurer la consommation réelle à haute fréquence.\
\
\### Connexion du PPK2 (Mode Source Meter à 3.7V)\
\* \*\*PPK2 \[VOUT\] (Rouge)\*\* ──\> Pastille \*\*\[BAT+\]\*\* au dos du XIAO\
\* \*\*PPK2 \[GND\] (Noir)\*\* ──\> Masse commune \*\*\[GND\]\*\* (XIAO + Capteur Plante)\
\* \*Note : Le câble USB du XIAO doit être débranché pendant la mesure pour ne pas fausser le profil énergétique.\*\
\
\### Diagramme d\'architecture matérielle globale :\
\
\`\`\`text\
┌──────────────────────────────────────┐\
│ Seeed Studio XIAO │\
│ │\
│ \[BAT+\] (Pastille au dos) ◄────────┼──────┐\
│ \[BAT-\] (Pastille au dos) ◄──────┐ │ │\
│ │ │ │\
│ \[GND\] ─────────────────────┐ │ │ │\
│ \[Pin D0\] ─── \[Alimentation\]┼──┐ │ │ │\
│ \[Pin A0\] \<── \[Signal analog\]┐ │ │ │ │\
└──────────────────────────────┼┼──┼─┼─┼──────┘\
││ │ │ │\
▼▼ ▼ │ │\
┌────────────────┐ │\
│ CAPTEUR PLANTE │ │\
│ (Ampli / GSR) │ │\
└────────────────┘ │\
┌──────────────────────┐ │\
│ BATTERIE LiPo 3.7V │ │\
│ │ │\
│ (Borne +) ───────────────────────────────────────┘\
│ (Borne -) ────────────────────────┘\
\`\`\`\
\
\-\--\
\
\## 4. Code Logiciel Optimisé (C++ Arduino)\
\
\### Émetteur : Le Capteur Miniature sur Batterie (XIAO ESP32)\
Ce code intègre des optimisations avancées : baisse de la fréquence CPU à 80MHz, initialisation radio agressive, coupure de l\'alimentation de la mémoire flash interne (\`VDDSDIO\`) et isolation des broches pour éliminer tout courant de fuite visible au PPK2.\
\
\`\`\`cpp\
#include \<esp_now.h\>\
#include \<WiFi.h\>\
#include \<esp_wifi.h\>\
\
#define TIME_TO_SLEEP 900 // Temps en secondes (900s = 15 minutes)\
#define uS_TO_S_FACTOR 1000000ULL // Facteur de conversion microsecondes -\> secondes\
\
const int PIN_ALIM_CAPTEUR = D0; // Broche d\'alimentation du capteur\
const int PIN_SIGNAL_PLANTE = A0; // Broche ADC (Lecture du signal)\
\
// Remplacer par la véritable adresse MAC de votre Hub Récepteur\
uint8_t broadcastAddress\[\] = {0x24, 0x0A, 0xC4, 0xXX, 0xXX, 0xXX};\
\
typedef struct struct_message {\
int id;\
float tensionPlante;\
} struct_message;\
\
struct_message mesDonnees;\
esp_now_peer_info_t peerInfo;\
\
void setup() {\
// OPTIMISATION 1 : Réduire la fréquence d\'horloge (Consomme 2x moins de mA pendant la mesure)\
setCpuFrequencyMhz(80);\
\
pinMode(PIN_ALIM_CAPTEUR, OUTPUT);\
digitalWrite(PIN_ALIM_CAPTEUR, HIGH); // Allumage de l\'amplificateur\
\
// OPTIMISATION 2 : Délai minimal de stabilisation à valider au PPK2\
delay(15);\
\
int valeurBrute = analogRead(PIN_SIGNAL_PLANTE);\
mesDonnees.tensionPlante = (valeurBrute \* 3.3) / 4095.0; // Conversion en Volts (12 bits)\
mesDonnees.id = 1; // Identifiant du capteur (permet le stacking de plusieurs plantes)\
\
digitalWrite(PIN_ALIM_CAPTEUR, LOW); // Extinction immédiate du capteur\
\
// OPTIMISATION 3 : Démarrage radio rapide pour protocole ESP-NOW (Envoi en \< 100ms)\
WiFi.mode(WIFI_STA);\
esp_wifi_start();\
\
if (esp_now_init() == ESP_OK) {\
memcpy(peerInfo.peer_addr, broadcastAddress, 6);\
peerInfo.channel = 0;\
peerInfo.encrypt = false;\
\
if (esp_now_add_peer(&peerInfo) == ESP_OK) {\
esp_now_send(broadcastAddress, (uint8_t \*) &mesDonnees, sizeof(mesDonnees));\
delay(5); // Temporisation matérielle minimale pour finaliser l\'émission\
}\
}\
\
entrerEnSommeilProfondUltra();\
}\
\
void loop() {}\
\
void entrerEnSommeilProfondUltra() {\
esp_wifi_stop();\
esp_wifi_deinit();\
\
// OPTIMISATION 4 : Couper l\'alimentation de la mémoire Flash interne en mode sommeil\
esp_sleep_pd_config(ESP_PD_DOMAIN_VDDSDIO, ESP_PD_OPTION_OFF);\
\
// OPTIMISATION 5 : Bloquer l\'état de la broche pour éviter les fuites de courant vers l\'AOP\
gpio_hold_en((gpio_num_t)PIN_ALIM_CAPTEUR);\
\
esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP \* uS_TO_S_FACTOR);\
esp_deep_sleep_start();\
}\
\`\`\`\
\
\### Récepteur : Le Hub Central (Alimenté sur Secteur)\
Ce module reste en écoute constante via le protocole ultra-rapide \*\*ESP-NOW\*\*. Il centralise et décode à la volée les paquets provenant de vos différents capteurs miniatures \"stackés\".\
\
\`\`\`cpp\
#include \<esp_now.h\>\
#include \<WiFi.h\>\
\
typedef struct struct_message {\
int id;\
float tensionPlante;\
} struct_message;\
\
donneesRecues struct_message;\
\
// Fonction exécutée automatiquement à la réception d\'un paquet radio\
void OnDataRecv(const esp_now_recv_info_t \* recvInfo, const uint8_t \*incomingData, int len) {\
memcpy(&donneesRecues, incomingData, sizeof(donneesRecues));\
\
char macStr\[18\];\
snprintf(macStr, sizeof(macStr), \"%02X:%02X:%02X:%02X:%02X:%02X\",\
recvInfo-\>src_addr\[0\], recvInfo-\>src_addr\[1\], recvInfo-\>src_addr\[2\],\
recvInfo-\>src_addr\[3\], recvInfo-\>src_addr\[4\], recvInfo-\>src_addr\[5\]);\
\
Serial.print(\"Données reçues du capteur Végétal \[ID \");\
Serial.print(donneesRecues.id);\
Serial.print(\" - MAC: \");\
Serial.print(macStr);\
Serial.print(\"\] -\> Tension mesurée : \");\
Serial.print(donneesRecues.tensionPlante, 3);\
Serial.println(\" V\");\
\
// Traitement applicatif (Ex: Envoi MQTT vers Home Assistant ou conversion en Note MIDI)\
if (donneesRecues.id == 1) {\
// Logique pour la plante numéro 1\
}\
}\
\
void setup() {\
Serial.begin(115200);\
\
WiFi.mode(WIFI_STA);\
WiFi.disconnect();\
\
if (esp_now_init() != ESP_OK) {\
Serial.println(\"Erreur d\'initialisation d\'ESP-NOW\");\
return;\
}\
\
esp_now_register_recv_cb(OnDataRecv);\
Serial.println(\"Hub Récepteur en ligne. En attente des données des plantes\...\");\
}\
\
void loop() {\
// Rien ici. Tout est géré de manière asynchrone par les interruptions matérielles.\
}\
\`\`\`\
\
\-\--\
\
\## 5. Perspectives d\'Évolution de l\'Objet Connecté\
Avec cette infrastructure basse consommation en place, le Hub central peut servir de passerelle pour :\
\* \*\*La création artistique :\*\* Mapper en temps réel les tensions reçues vers des notes ou des textures sonores (via les bibliothèques \`BLE-MIDI\` de l\'ESP32) pour piloter Ableton, Logic Pro ou une application mobile.\
\* \*\*La domotique (IoT) :\*\* Publier les messages en MQTT vers \*\*Home Assistant (via ESPHome)\*\* pour intégrer vos plantes dans l\'écosystème de votre maison (ex: déclencher une alerte visuelle lumineuse si la plante montre des signes électriques de stress hydrique).
