# HARDWARE STATE — Single Source of Truth

> **Règle :** Dobby lit ce fichier AVANT de faire une affirmation sur le matériel.
> **Mise à jour :** immédiate après chaque info de JC (réception, commande, panne, prêt).
> **Ne pas déduire, ne pas deviner.** Si pas dans ce fichier → demander à JC.
> **Dernière mise à jour :** 2026-11-25 — **M1 câblé via TL-SG605E** (en8 1000baseT, IP `192.168.129.78`, route par en8, auto-login `m1` activé) ; débit ~2,88 Mo/s (cap amont ligne/répéteur). Kexts HighPoint x86_64 retirés. Lupo ✅ booté (HA `:8123` sur `192.168.129.27`) ; home ✅ en ligne ; EPSON IP .75 (MAC `d4:80:8b:a6:f1:c4`) ; Hammerspoon actif.

---

## WildNexus P0

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| Nordic PPK2 | 1 | ✅ REÇU | ~100€, utilisé actif |
| ESP32-S3-DevKitC-1 N16R8 | 2 | ✅ REÇU | Amazon MiMiU, 21,98€ |
| ESP32-CAM OV2640 (avec modules caméra) | 2 | ✅ REÇU | Hailege Amazon.de, ~25€, 21 juin |
| ESP32-CAM OV2640 (cartes seules) | 4 | ✅ REÇU | 23 juin |
| OV5640 DVP M12 | 5 | ✅ REÇU | 1× Camemake.eu (12 juin) + 4× AliExpress (24 juin) |
| USB-C TTL FT232RL | 3 | ✅ REÇU | AZDelivery Amazon, 9€, 21 juin |
| Commande Mouser #39492997 | 1 | ✅ REÇU | 8 juillet. MEMS TDK×2, IR 940nm×10, PIR×2, Buck TPS62840×5, Inductance 10µH×5, MOSFET SI2302×5, BME688×2, SHT31×2, Antenne LoRa×2, Dissipateur×4, Lot passifs CMS SparkFun 0603×1. 105,94€ + port. TPS62840DLCR arrivé avec 1 semaine d'avance sur ETA. |
| Miuzei Starter Kit Arduino | 1 | ✅ REÇU | 235 composants, breadboard — 10 juin |
| MP1584 DC-DC Step Down 3A | 5 | ✅ REÇU | Ultra-Small, réglable, remplace LM2596 — 3 juillet |
| Panier Mouser restant (11 composants BOM) | — | ⏳ À COMMANDER | ~279€ |

## STATION-DOMO / IoT

> **Vue opérationnelle canonique du matériel Lupo :** `lupo-materiel.md` (par catégorie). Ce fichier reste le registre d'achats détaillé (prix, dates, sources).

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| Lupo (Ford Transit Custom Westfalia Kelsey) | 1 | ✅ REÇU | 30 juillet 2026 — véhicule livré, installation IOT en cours (deadline **15/12**, prolongée par JC le 19/10) |
| RPi 5 — hôte HAOS `lupo`, actuellement bureau Esneux | 1 hôte observé | ✅ BOOTÉ / HA EN LIGNE (25/11) | **8 Go mesurés**, modèle RPi 5 Rev 1.0, SD 256 Go, HAOS 18.3. **25/11 : a booté — HA joignable `http://192.168.129.27:8123` (HTTP 200), Tailscale `100.106.152.118` online, raccordé au switch TL-SG605E.** Le blocage SD du 23/11 n'est plus d'actualité. Achat historique : RPi 5 4 Go, Amazon, 132,09€, 10 juin ; écart RAM à vérifier sur facture/boîte. |
| Alim officielle RPi5 27W | 1 | ✅ REÇU | 15,32€ |
| Refroidisseur actif RPi5 | 1 | ✅ REÇU | 9,99€ |
| Geekworm X1205 UPS HAT | 1 | ✅ REÇU | AliExpress, 42,39€. Identification physique à revérifier : le wiki constructeur décrit deux accus **21700**, tandis que le stock ci-dessous mentionne des 18650. |
| Accus 18650 Flat 3400mAh CCC-5 SDIR18T | 20 | ✅ REÇU | Rose, 8 juillet 2026 |
| Geekworm X1201-C1 boîtier métal | 2 | ✅ REÇU | AliExpress, 18,59€, 29 juin |
| Sonoff ZBDongle-E (Zigbee) — Lupo | 1 | ✅ REÇU / DÉTECTÉ / OPÉRATIONNEL | Amazon, 25,32€, 7 juin 2026 ; coordinateur affecté au van. Déplacé du port noyau `1-2` vers `3-2` le 05/11, puis une relance Z2M : test initial de 10 min puis contrôle à 23:50, près de 3 h après le changement, sans nouvelle coupure USB ni sous-tension ; Z2M actif et MQTT connecté. Conserver ce port ; tester rallonge puis alimentation seulement en cas de récidive. |
| Sonoff ZBDongle-E (Zigbee) — maison + serre | 1 | ✅ OPÉRATIONNEL / M5 TEMPORAIRE | Amazon, ASIN B0B6P22YJC ; reçu le 6 novembre 2026. Branché sur M5, pont série relancé (v4) + Z2M up (EmberZNet 7.4.4, canal 15). AirGuard Serre ré-appairé (frais). **Valve d'eau + LuxSerre : périmés (juillet), à ré-appairer** — à localiser physiquement. En attendant un **RPi dédié permanent**. |
| SNZB-02DR2 Temphumid Zigbee — AirGuard Serre | 1 | ✅ RÉ-APPAIRÉ SUR M5 | 15,15€ ; ré-appairé du Lupo vers le M5 le 06/11 (canal 15, force-remove + permit-join + bouton). Mesures fraîches : 20,5 °C / 64,8 % / batterie 89 %, LQI 255/255. |
| SNZB-02UL AirGuard TH E-Ink — Lupo | 1 | ✅ RÉ-APPAIRÉ / MESURES FRAÎCHES | Silence radio 23 h (dernière trame 05/11 13:01, LQI 56/255). Rapproché physiquement + ré-appairé par Dobby le 06/11 (permit-join + maintien bouton 5 s) : re-interview OK, LQI 255/255, 18,8 °C / 66,1 % / batterie 100 %. Cause racine : lien radio faible (distance). Prix d'achat non renseigné. |
| Sonoff Smart Water Valve | 1 | ✅ REÇU | Électrovanne connectée |
| Sonoff ZBMiniR2 (Zigbee) | 1 | ✅ REÇU | 8 juillet — smart switch Zigbee |
| PV PI HAT | 1 | ✅ REÇU | 150 AUD, reçu 1er juillet (avance sur prévision 15/08) |
| ADS1115 ADC Module 16-bit I2C (Heemol) | 3 | ✅ REÇU | Heemol, 9,21€, reçu 2 juillet |
| ADS1115 ADC 16-bit I2C HW-19S | 3 | ✅ REÇU | 8 juillet — PCB vert |
| ESP32-C3 Super Mini (Heemol) | 3 | ✅ REÇU | Heemol, 15,98€, reçu 2 juillet — détecteur niveau liquide |
| Step-Down HW-133 3A 5V DC-DC (Tecnoiot) | 5 | ✅ REÇU | 8 juillet — buck 24V-9V → 5V fixe, ultra-small |
| Aqara Light Sensor T1 (GZCGQ11LM) | 1 | ✅ REÇU | Zigbee — appairé 2 juillet, friendly_name: LuxSerre |
| Power Supply Adapter HS24A (24V) | 1 | ✅ REÇU | 8 juillet — alim 24V pour sonde TL-136 |
| Sonde hydrostatique TL-136 | 1 | ✅ REÇU | 8 juillet — capteur 4-20mA, détecteur niveau liquide |
| BOYA BY-MM1 | 1 | ✅ REÇU | Micro shotgun |
| UGREEN USB Audio | 1 | ✅ REÇU | Adaptateur audio RPi |
| Teltonika RUT240 (routeur 4G/LTE) | 1 | ✅ EN STOCK | Passerelle internet van : SIM 4G → Ethernet → RPi 5. Alim 9-30V DC, Tailscale/WireGuard, RMS. Remplace le ZTE MF833U1 (dongle) pour le van. |
| PCIe to M.2 NVMe Shield | 2 | ✅ REÇU | 29 juin, pour SSD NVMe RPi 5 vanlife |
| SSD NVMe M.2 Fanxiang 256GB | 1 | ✅ REÇU | 1er juillet, pour RPi 5 vanlife |
| Assemblage RPi 5 `lupo` | 1 hôte observé | ✅ BOOTÉ (25/11) | RPi 5 **8 Go mesurés** + SD 256 Go + X1201-C1, au bureau. HAOS 18.3. **25/11 : booté — HA `:8123` sur `192.168.129.27`, Tailscale `100.106.152.118` online** (blocage SD du 23/11 levé). Auto-update sélectif : Supervisor + modules ; HAOS/Core manuels. Un dongle USB présent ; Z2M arrêté après déconnexion USB. Identifier physiquement UPS/accus avant modification ; reste silentblocs, coating et intégration van. |
| Samsung PRO Endurance 256GB microSD | 1 | ✅ REÇU | 17 juillet, Amazon. Remplace SD 128 Go actuelle pour HA OS 24/7. |
| Noctua NF-A4x10 PWM | 1 | ✅ REÇU | 19 juillet. Ventilateur 40×10mm silencieux pour RPi Lupo. |
| Reolink Argus MagiCam | 1 | ✅ REÇU | 17 juillet. Dashcam/sécurité Lupo, fixation aimantée. Voir `07_TRAVELS/Lupo/van technique/securite/camera-reolink-argus-magicam-lupo.md`. |
| Bidirectional Level Shifter 8CH | 2 | ✅ REÇU | 23 juillet — conversion 3.3V ↔ 5V, I2C/SPI/UART, pour RPi Lupo |
| XKC-Y25-V Capteur niveau liquide sans contact | 4 | ✅ REÇU | 25 juillet — XKeyes/EllyESTUDIO, non-contact, pour cuves Lupo |
| Module relais optocoupleur Arduino 12V 2CH | 3 | ✅ REÇU | 25 juillet — Shield, déclenchement haut/bas, optocoupleur |
| INMP441 MEMS Microphone omnidirectionnel I2S | 3 | ✅ REÇU | 25 juillet — Haute précision, basse conso, ESP32, acquisition vocale |
| GY-521 MPU-6050 IMU 6 axes (gyro + accéléro) | 4 | ✅ REÇU | 25 juillet — I2C, pour Arduino/ESP32. Inclinométrie ? Détection mouvement ? |
| Wolfbox G900 TriPro Bumper (miroir 12" 3 canaux : avant 4K IMX678 + arrière 2.5K + pare-chocs 1080P) | 1 | ✅ REÇU | livrée 13/10 (pack étendu, **378 €**). Version Stoßfänger, caméra pare-chocs IP67. Voir `07_TRAVELS/Lupo/van technique/securite/cameras-parking-dashcam-lupo.md` |
| Wolfbox OEM bracket (support rétro d'origine) | 1 | ✅ REÇU | reçu 13/10 — à faire fixer par Be Camper |
| Kit hardwire Wolfbox G900TriPro (mode parking) | 1 | ✅ REÇU | reçu 13/10, ~25€, fusible tap + coupure basse tension |
| Rallonge câble caméra arrière 10/15 m (G900TriPro) | 1 | ✅ REÇU | reçue 13/10, ~28€, pour van 5,45 m |
| microSD High Endurance 256 Go (dashcam) | 1 | ⏳ À COMMANDER | achetée plus tard (JC 13/10) — séparée de celle du RPi |

## RPi HOME « JC home » (maison + serre)

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| RPi 5 4 Go (hôte HAOS `homeassistant`) | 1 | 🟢 OPÉRATIONNEL | HAOS 18.5, Core 2026.11.0, HA sur **port 80**. Ethernet via switch **TL-SG605E** → DHCP `192.168.129.57` (/23), confirmé 25/11 (HA :80 + mDNS `homeassistant.local` OK). SSH debug 22222. |
| SD 64 Go | 1 | ✅ | Re-flashée 07/11 |
| Ventilateur actif | 1 | ✅ | Obligatoire — surchauffe sinon |
| Sonoff ZBDongle-E (Zigbee) | 1 | ✅ DÉTECTÉ | `/dev/ttyUSB0`, canal 15. 1 device joint (`serre_temp_hum`). `vanne_serre` + `LuxSerre` à ré-appairer. |
| Coque de protection | 1 | ✅ | Installée 12/11 — power-cycle + perte Ethernet le temps du re-câblage |

> **WiFi à prévoir en secours** (si capteurs trop loin → déplacer le RPi) : non configuré à ce jour. Méthode : `nmcli device wifi connect <SSID> password <PSK>` ou UI HA.

## ÉNERGIE NOMADE / Power Station (Lupo)

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| Bluetti Elite 100 V2 (power station) | 1 | ⏳ INTENTION / À COMMANDER | 1 024 Wh LiFePO4, onduleur 1 800 W sinus pur (surtension 2 700 W), entrée solaire 1 000 W, USB-C 140 W/100 W, 11,3 kg. Couvre le pic 230 V (Nespresso 1 310 W + MBP + iPad + iPhone + JBL ≈ 1 555 W) sans solliciter la batterie cellule. |
| Bluetti PV200 (panneau 200 W) | 1 | ⏳ INTENTION / À COMMANDER | Plié 59×63 cm, 7,3 kg, IP67, béquille, MC4. Déployé au sol sous l'auvent (à l'arrêt). Voc 26,1 V → compatible entrée 12–60 V. |
| Rallonge MC4 (5–10 m) | 1 | ⏳ INTENTION / À COMMANDER | Relie le PV200 (auvent) au Bluetti (cellule). |

*Recharge en roulant : Charger 1 (560 W, alternateur) en option — Charger 2 non retenu (pas de solaire + alternateur simultané).*

## IT / Divers

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| UGREEN USB-C → Micro USB ×2 | 2 | ✅ REÇU | 10 juin |
| UGREEN USB-C Ethernet Gigabit | 1 | ✅ REÇU | 10 juin |
| **TP-Link TL-SG605E** (switch Gigabit 5 ports, Easy Smart) | 1 | ✅ INSTALLÉ / OPÉRATIONNEL | Installé 25/11 derrière le répéteur **RE450** du bureau. **M1 câblé** : `en8` = 1000baseT full-duplex, IP **192.168.129.78**, route par défaut via en8. Débit ~2,88 Mo/s (plafond en amont ~22–26 Mbit/s, ligne/répéteur → le switch apporte stabilité, pas vitesse). Auto-login `m1` activé (indispensable : sur Mac headless, le verrou d'accessoire USB bloque le dongle sans session). RPi Home ✅ raccordé (`192.168.129.57`, HA `:80`) ; RPi Lupo ✅ raccordé (`192.168.129.27`, HA `:8123`). |
| **CPL — bureau (révision 25/11)** | 1 adaptateur pass-through | 📋 EN COURS D'ANALYSE | **Topologie réelle** : B-box —Eth→ CPL Base (prise murale) ⇒ secteur ⇒ **CPL bureau sur MULTIPRISE (mur)** → **RE450** → TL-SG605E. ⚠️ Instabilité probable = **CPL sur multiprise** (pas le Wi-Fi). Kit = **TP-Link TL-WPA8631P (AV2 Gigabit)**. **Recommandation** : (1) CPL bureau sur **prise murale via adaptateur pass-through** (modèle retenu : **TP-Link TL-PA7017P**, upgrade PA9020P ; multiprise derrière) ; (2) garder le **RE450 en mode AP** (uplink Ethernet CPL) → backhaul filaire + Wi-Fi AC1750 (meilleur qu'un CPL+WiFi 2,4 GHz). **Pas besoin** d'un CPL-répéteur, sauf boîtier unique / Wi-Fi bi-bande (→ Devolo G.hn = nouvelle paire incompatible AV2). Clé CPL commune. À confirmer : mode actuel du RE450 (AP vs répéteur Wi-Fi). |
| ZTE MF833U1 LTE USB Modem | 1 | ✅ REÇU | Dongle 4G USB pour internet van — voir briefs vanlife-iot. |
| WiCAN Pro (OBD/CAN Ford) | 1 | ✅ REÇU / INSTALLÉ PHYSIQUEMENT | 1er août 2026, ~82€, Mouser. MS-CAN + HS-CAN. Intégration HA/RUT240 et compatibilité Exosfer à valider ; 17+ entités visées, remontée non confirmée. Voir `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/specs/SPEC-CAN-BUS.md` |
| Exosfer OBD Protect | 1 | ✅ REÇU | Antivol électronique prise OBD. ⚠️ Compatibilité WiCAN Pro à vérifier. |
| SSD Time Machine | 1 | ⏳ À COMMANDER | Décision JC 2026-10-05. SSD 2 To min (USB-C/Thunderbolt), format APFS chiffré. Remplace le HDD 1 To `PKA_TimeMachine` (APFS saturé à 97%, LazyThinning bloqué à 99% CPU). |
| Hammerspoon | 1 | ✅ INSTALLÉ / ACTIF | 23/11 — `brew install --cask hammerspoon` (1.1.1). Config `~/.hammerspoon/init.lua` (24/11) : curseur `⌃⌥⌘→`/`⌃⌥⌘←` + déplacement fenêtre `⌃⌥⌘↑`/`⌃⌥⌘↓` entre les 3 écrans M5 (Built-in, LG Ultrawide, Apple TV AirPlay). Permission Accessibilité accordée. Sauvegarde `init.lua.bak-20261124`. |

## LEAFNET / WN-BIO

| Composant | Qté | Statut | Notes |
|-----------|-----|--------|-------|
| AD623ANZ | ? | ⏳ À COMMANDER | Ampli instrumentation |
| XIAO ESP32 | ? | ⏳ À ACQUÉRIR | Miniaturisation v0.2 |

---

*Source autoritaire. Synchronisé avec `docs/system/registre-achats.md`.*