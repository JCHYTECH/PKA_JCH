# SPEC-CAN-BUS — Interface OBD-II / CAN bus Ford Transit Custom

> **Statut :** spécification cible v1.1 — diagnostic distant fait, **intégration non validée**
>
> **Création :** 2026-07-09 · **Révision :** 2026-11-05 · Dobby 🦉
>
> **Véhicule cible :** Westfalia Kelsey 2026 — Ford Transit Custom 170 CV 4x4 « Lupo »
>
> **Matériel :** WiCAN Pro reçu et documenté comme physiquement installé ; RUT240 en stock
>
> **Procédure opérationnelle :** [`OPERATIONS-CAN-OBD.md`](../OPERATIONS-CAN-OBD.md)
>
> **Piste de PIDs :** [WiCAN-Ford-Transit](https://github.com/anthonysecco/WiCAN-Ford-Transit), dépôt communautaire à valider sur le véhicule réel

---

## 1. Objectif et état réel

Lire en consultation seule les données disponibles sur les bus CAN via le port OBD-II et les publier dans Home Assistant par MQTT. La cible historique est **17+ capteurs véhicule**, sans capteur additionnel lorsque le véhicule expose déjà la donnée.

**Au 2026-11-05 :** le registre HA inspecté contient 126 entités, mais **aucun appareil WiCAN et aucune entité CAN**. Le RPi est au bureau sur le Wi-Fi maison ; son Ethernet est désactivé et le RUT240 n'est pas connecté. Aucune remontée réelle, aucun PID et aucune compatibilité avec l'Exosfer OBD Protect ne sont donc validés.

Cette spécification ne doit plus être lue comme « validé, à implémenter » ni comme une preuve que toutes les données ci-dessous existent sur ce véhicule.

### Données recherchées — cibles

**HS-CAN / groupe motopropulseur :**
- vitesse, régime moteur, température de liquide de refroidissement ;
- niveau et débit de carburant, consommation dérivée ;
- pression d'admission, température d'air d'admission et extérieure ;
- charge moteur, position papillon, tension ECU et codes défaut.

**MS-CAN / carrosserie :**
- états des portes, hayon et capot ;
- pressions des pneus effectivement présents et adressables ;
- état de charge, courant et tension de la batterie porteur si exposés.

Les capteurs Zigbee de portes restent nécessaires pour les scénarios en camping : ils ne sont pas supprimés sur la promesse d'une future remontée CAN.

---

## 2. Architecture cible

```text
[Port OBD-II / Exosfer]
          │
          ▼
      [WiCAN Pro]
          │ Wi-Fi local du van
          ▼
[Teltonika RUT240 — 4G + LAN]
          │ Ethernet
          ▼
[RPi 5 HAOS — Mosquitto + Home Assistant]
          │
          ▼
[MQTT discovery → entités réellement supportées]
```

Tailscale fournit la supervision distante quand la connectivité le permet. Il ne remplace ni le LAN du van ni le broker local.

### 2.1 Choix matériel historique

Le WiCAN Pro a été retenu pour son support HS-CAN/MS-CAN, MQTT et sa gestion de veille, puis acheté début août 2026. Le WiCAN basic ne couvrait pas le besoin MS-CAN documenté. Cette décision n'est **plus une étape d'achat**.

Le RUT240 remplace la cible antérieure « RPi en point d'accès + dongle ZTE » pour le réseau du van. L'adressage et les credentials doivent être relevés sur place ; aucun secret ne figure dans cette spécification.

---

## 3. Données candidates dans Home Assistant

Les noms ci-dessous sont des **identifiants de conception**, non des entités créées. Les identifiants réels dépendront des messages MQTT et de la découverte. Un PID listé ne signifie ni supporté par le véhicule ni testé.

### 3.1 HS-CAN — PCM, requêtes candidates

| Identifiant envisagé | PID / requête candidate | Description | Unité |
|---|---|---|---|
| `sensor.vehicle_speed` | Mode 01, `0x0D` | Vitesse véhicule | km/h |
| `sensor.engine_rpm` | Mode 01, `0x0C` | Régime moteur | tr/min |
| `sensor.coolant_temp` | Mode 01, `0x05` | Température liquide refroidissement | °C |
| `sensor.fuel_level` | Mode 01, `0x2F` | Niveau carburant | % |
| `sensor.fuel_rate` | Mode 01, `0x5E` | Débit carburant | L/h |
| `sensor.intake_air_temp` | Mode 01, `0x0F` | Température air admission | °C |
| `sensor.ambient_air_temp` | Mode 01, `0x46` | Température extérieure | °C |
| `sensor.engine_load` | Mode 01, `0x04` | Charge moteur calculée | % |
| `sensor.throttle_position` | Mode 01, `0x11` | Position papillon | % |
| `sensor.manifold_pressure` | Mode 01, `0x0B` | Pression admission | kPa |
| `sensor.ecu_voltage` | Mode 01, `0x42` | Tension de commande ECU | V |
| `sensor.dtc_count` | Mode 03 | Codes défaut rapportés | — |

Les PIDs Mode 01 sont définis par SAE J1979, mais leur présence et leur interprétation restent propres au véhicule. La compatibilité n'est pas « quasi garantie » sans test.

### 3.2 MS-CAN — BCM, requêtes à confirmer

| Identifiant envisagé | PID candidat du dépôt communautaire | Donnée recherchée |
|---|---|---|
| `binary_sensor.door_driver` | `0x225B1D`, bit 0 | Porte conducteur |
| `binary_sensor.door_passenger` | `0x225B1D`, bit 1 | Porte passager |
| `binary_sensor.door_left_rear` | `0x225B1D`, bit 3 | Porte arrière gauche |
| `binary_sensor.door_right_rear` | `0x225B1D`, bit 4 | Porte arrière droite |
| `binary_sensor.door_luggage` | `0x225B1D`, bit 5 | Hayon/coffre |
| `binary_sensor.hood` | `0x225B1D`, bit 2 | Capot moteur |
| `sensor.tpms_front_left` | `0x222813` | Pression avant gauche |
| `sensor.tpms_front_right` | `0x222814` | Pression avant droite |
| `sensor.tpms_rear_left_outer` | `0x222816` | Pression arrière gauche extérieure |
| `sensor.tpms_rear_right_outer` | `0x222815` | Pression arrière droite extérieure |
| `sensor.tpms_rear_left_inner` | `0x222818` | Pression arrière gauche intérieure |
| `sensor.tpms_rear_right_inner` | `0x222817` | Pression arrière droite intérieure |
| `sensor.battery_soc` | `0x224028` | État de charge batterie |
| `sensor.battery_current` | `0x22402B` | Courant batterie |
| `sensor.battery_voltage_bcm` | `0x22402A` | Tension batterie |

Le mapping des bits, les six roues et les PIDs BCM doivent être vérifiés physiquement sur le Transit Custom 2026 et son aménagement Westfalia. Un outil Ford tel que FORScan peut aider au diagnostic, mais aucune écriture ECU n'est autorisée par cette spécification.

---

## 4. Alimentation, sommeil et sécurité

### 4.1 Comportement à établir

Le comportement du bus après coupure du contact, son délai d'endormissement et les réponses BCM doivent être mesurés sur Lupo. Les anciens délais de 30/60 minutes et l'alimentation permanente de l'OBD ne sont pas considérés comme vérifiés.

### 4.2 Réglages initiaux à évaluer

| Paramètre | Cible historique | Validation exigée |
|---|---|---|
| Veille WiCAN | `< 1 mA` | Mesure de courant réelle dans le montage final |
| Réveil périodique | 5 min | Utilité, reconnexion et effet sur les ECU |
| Coupure basse tension | `11,8 V` | Documentation, batterie réelle et test contrôlé |
| Réveil en roulage | Tension / activité à configurer | Pas de polling excessif ni réveil permanent du bus |

Une veille de 1 mA représente environ 0,024 Ah/jour **pour le module seul**, hors pertes, accessoires et réveils du véhicule. Ce calcul ne justifie pas l'affirmation « aucun risque batterie ».

### 4.3 Exosfer et garantie

L'Exosfer OBD Protect est reçu, mais son montage avec le WiCAN n'est pas documenté comme compatible. Vérifier d'abord le passage des signaux, l'alimentation, le verrouillage et les recommandations des fabricants.

« Lecture seule » ne suffit pas à affirmer un risque de garantie nul : le polling, les réveils du bus, le montage mécanique et la consommation permanente doivent aussi être considérés. Aucun flash ou écriture ECU n'est nécessaire pour le premier diagnostic.

---

## 5. Effets sur les scénarios — conditionnés aux tests

| Scénario | Apport CAN possible | Source à conserver |
|---|---|---|
| Porte oubliée / hayon ouvert | Confirmation vitesse/RPM et état véhicule si disponibles | Contact Zigbee + DS300 |
| Sécurité tiroirs | Vitesse et régime moteur si fiables | Règle existante testée |
| Détection intrusion | Redondance portes/capot éventuelle | Contacts Zigbee + PIR |
| Niveau carburant / autonomie | Données PCM et calcul après calibration | Jauge du véhicule |
| Consommation trajet | Débit + vitesse + distance, si disponibles | Relevé réel |
| Diagnostic moteur | DTC en lecture seule | Diagnostic constructeur |
| Pression pneus | Valeurs BCM si réellement exposées | Contrôle manuel / TPMS existant |
| Batterie porteur | SOC/courant/tension si disponibles | Mesure électrique |

Aucune économie de capteurs n'est actée avant validation. Les anciens chiffrages « −25 € » et « +57 € » sont historiques et ne constituent pas un budget actuel.

---

## 6. Procédure d'installation et recette

La checklist détaillée et les accès sont dans [`OPERATIONS-CAN-OBD.md`](../OPERATIONS-CAN-OBD.md).

### Phase 0 — Diagnostic distant terminé

- [x] WiCAN Pro identifié comme reçu/installé physiquement dans l'inventaire.
- [x] Absence d'appareil WiCAN et d'entités CAN dans le registre HA consulté.
- [x] Absence de liaison Ethernet RUT240 → RPi et de réseau van configuré.
- [ ] Présence physique et montage WiCAN/Exosfer revérifiés sur place.

### Phase 1 — Réseau et MQTT, localement

1. Alimenter le RUT240, relever son LAN et le relier au RPi par Ethernet.
2. Préserver l'accès HA existant pendant le changement et vérifier l'adressage.
3. Relever/sauvegarder le firmware et la configuration WiCAN ; **ne pas flasher systématiquement**.
4. Connecter WiCAN au Wi-Fi du RUT240 et au Mosquitto du RPi.
5. Observer les connexions et publications réelles avant d'attendre la découverte HA.

### Phase 2 — PIDs et véhicule

1. Vérifier la présence d'un appareil MQTT et les identifiants réellement créés.
2. Tester contact mis, moteur arrêté, puis moteur tournant à l'arrêt.
3. Importer seulement des PIDs candidats compris et réversibles ; consigner les réponses et non-réponses.
4. Comparer les mesures au tableau de bord ; tester les portes et pneus seulement si le BCM répond.
5. Vérifier l'Exosfer à chaque étape et ne jamais contourner sa protection.
6. Tester la reconnexion après redémarrage des équipements.

### Phase 3 — Veille et automatisation

1. Mesurer courant de veille et effet des réveils sur une durée représentative.
2. Valider ou corriger les seuils de sommeil et de coupure.
3. Créer dashboard et automatisations uniquement à partir d'entités éprouvées.
4. Conserver une solution de secours pour toute mesure de sécurité.

---

## 7. Risques et inconnues

| Risque | Probabilité | Réduction / preuve attendue |
|---|---|---|
| PIDs BCM ou PCM non supportés / mapping différent | **Inconnue** | Tests réels, comparaison constructeur, diagnostic Ford |
| Exosfer incompatible avec le montage | **Inconnue** | Inspection physique et tests sans contournement |
| Réseau local ou Wi-Fi instable | **Inconnue** | RUT240 câblé au RPi, test de reconnexion et portée |
| Consommation ou réveils du bus excessifs | **Inconnue** | Mesure de courant/tension et test de stationnement |
| Effet sur garantie ou diagnostic véhicule | **Inconnu** | Lecture seule, notices constructeurs, aucune promesse implicite |
| Topics MQTT mal mappés / entités dupliquées | **Inconnue** | Sauvegarde, discovery contrôlée et correspondance documentée |
| Perte d'accès HA pendant changement réseau | **Inconnue** | Intervention locale, conservation du chemin existant et retour arrière |

---

## 8. Critères d'acceptation

- [ ] RUT240, RPi, Mosquitto et WiCAN reliés selon le schéma réel documenté.
- [ ] Appareil WiCAN présent dans HA via des publications MQTT observées.
- [ ] Chaque entité acceptée possède un test et une valeur comparée au véhicule.
- [ ] Non-supports et entités indisponibles explicitement listés ; aucune valeur fictive.
- [ ] Compatibilité Exosfer tranchée et consignée.
- [ ] Sommeil, reprise et consommation mesurés ; risques résiduels documentés.
- [ ] Aucune automatisation de sécurité ne dépend d'une donnée non validée.

---

## 9. Références

- [WiCAN Pro — MeatPi Electronics](https://www.meatpi.com/products/wican-pro)
- [WiCAN firmware — documentation](https://github.com/meatpi-electronics/wican-fw)
- [WiCAN-Ford-Transit — dépôt communautaire](https://github.com/anthonysecco/WiCAN-Ford-Transit)
- [FORScan — diagnostic Ford](https://forscan.org/)
- [SAE J1979 / OBD-II PIDs](https://en.wikipedia.org/wiki/OBD-II_PIDs)
- [`SPEC-DS300-TAP.md`](../ds300-tap/SPEC-DS300-TAP.md)
- [`scenarios-algorithmes-vanlife.md`](../scenarios-algorithmes-vanlife.md)
- [`BOM-VANLIFE.md`](../BOM-VANLIFE.md) — historique à resynchroniser

---

*Révision documentaire du 2026-11-05 : achat/flash retirés du chemin initial, architecture RUT240 intégrée et résultats non mesurés explicitement distingués de la cible.*
