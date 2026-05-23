# WildNexus — Analyse note JCH + intégration BOM station bioacoustique/caméra

**Date :** 2026-05-22  
**Auteur :** Dobby — claude-sonnet-4-6  
**Sources analysées :**
- `JCH_Inbox/00_INBOX/Wildnexus.md` — note à vif de JCH
- `TEAM_Inbox/2026-05-22_dobby_wildnexus-resume-chat-hardware-architecture.md` — résumé de la discussion hardware précédente
- `JCH_Inbox/00_INBOX/fiche_specs_BOM_station_bioacoustique_camera.md` — BOM prototype figé
- Ensemble des documents fondateurs WildNexus (MASTER_ARCHITECTURE, P0_SCOPE_LOCK, ENGINEERING_PHILOSOPHY, ADR-001)

**Spécialistes consultés :** wildnexus-firmware-ulp · wildnexus-bioacoustics-dsp · wildnexus-camera-imaging · wildnexus-edge-ai-cv · wildnexus-hardware-physical · Chouette 🦉

---

## 1. Verdict global sur la note JCH

La note "à vif" de JCH est **cohérente avec le projet**. Elle décrit la vision produit complète — ce que WildNexus doit devenir, pas ce que P0 doit livrer demain. Elle mélange P0, P1 et P2 dans la même liste, ce qui est normal pour une note de vision. L'ADR-001 (ESP32-S3 MCU P0) et le SCOPE_LOCK restent valides.

---

## 2. Ce que la note confirme (validé par les spécialistes)

### Architecture tout-en-un pour P0
Chouette confirme : pour un poseur de pièges belge en forêt, le tout-en-un gagne à P0. Un seul boîtier, une seule maintenance. Le satellite/base devient pertinent à P1 quand on déploie plus de 3 nœuds.

### WiFi download — avec correctif BLE
En forêt dense, portée WiFi réelle = **15–25 m** (pas 50–100 m). L'utilisateur doit quitter le sentier, ce qui dérange la faune.  
Architecture correcte : **BLE pour la notification** (50–80 m à travers les arbres) + **WiFi uniquement pour le transfert de données** lorsque l'utilisateur est à portée.

### Capteurs retenus pour P0
| Capteur | Verdict P0 |
|---|---|
| Température | ✓ corrige seuils de détection + donnée biologique |
| Humidité | ✓ double usage : contexte bio + alerte condensation interne |
| Vibration / accéléromètre | ✓ détection vol ou chute, <2 € |
| Luminosité | ✓ pilote passage mode jour/nuit IR |
| Pression barométrique | ✗ hors P0 — aucune utilité opérationnelle immédiate |

### Batterie
LiFePO4 obligatoire pour le terrain belge en hiver. Li-Ion perd 40–50 % de capacité à -20°C.  
Format : rack 18650 × 4 extractible par trappe vissée avec joint remplaçable.  
Petite batterie interne (~500 mAh) pour RTC et fin d'écriture SD.

### Microphone en boîtier IP67
Membrane PTFE Gore-Tex obligatoire (pas de trou calibré — l'eau entre, les insectes bouchent, le MEMS meurt en 3 semaines). 1 seul micro suffit pour P0. Bonnette interne mousse contre le vent (ennemi n°1).

---

## 3. Les 3 tensions identifiées par les spécialistes (note JCH seule)

### Tension 1 — "BirdNET à bord" ≠ BirdNET complet
BirdNET Analyzer complet (25–50 MB RAM, Python, TFLite) ne tourne pas sur ESP32-S3. Ce n'est pas une limite à contourner, c'est une contrainte physique.

| Option | Hardware | Phase |
|---|---|---|
| BirdNET-lite quantisé INT8 (~1–2 MB) | ESP32-S3 + PSRAM 8 MB | P1 — 50–150 espèces locales, ~80 % précision |
| BirdNET complet | Raspberry Pi / RV1106 / RK3588 | P1 base ou satellite smart |
| VAD + envoi spectrogramme → cloud | ESP32-S3 | P1 si connectivité disponible |

**→ Résolue par le BOM** (voir section 5) : BirdNET cloud, filtrage local léger sur ESP32-S3.

### Tension 2 — "Tout le son va dans BirdNET" vs autonomie 60 jours
Enregistrement audio continu + inférence = batterie vidée en 12–20h. Incompatible avec la cible terrain.  
Seule voie viable : mode **événementiel**. L'ULP ESP32-S3 fait un VAD (~100–400 µA), réveille le cœur principal sur événement, analyse le clip.  
WildNexus est un **déclencheur d'événements écologiques**, pas un enregistreur continu.

### Tension 3 — ESP32 seul ne suffit pas pour la vision complète
L'ESP32-S3 solo peut faire : filtre animal/non-animal à 96×96 (80–150 ms/frame) + capteurs + WiFi + LoRa. C'est P0.  
Pour la vision complète (caméra haute qualité + BirdNET + vidéo H264 + IA) : **duo MCU**.

Architecture duo recommandée par les agents :
```
ESP32-S3 master     ←→     RV1106 (Rockchip, ~10 €)
- veille ULP                - caméra MIPI CSI
- PIR + réveil              - encode H264 hardware
- LoRa / BLE / WiFi         - NPU 0.5 TOPS
- capteurs environ.         - dort jusqu'au réveil
```

---

## 4. Mapping note JCH → phases WildNexus

| Élément de la note JCH | Phase |
|---|---|
| Caméra + SD + WiFi download + PIR + filtre image | P0 — conforme ADR-001 et SCOPE_LOCK |
| BLE notification + WiFi download | P0 — amélioration confirmée Chouette |
| Micro + BirdNET-lite + déclenchement audio | P1 |
| BirdNET complet embarqué (duo/trio) | P1 avec architecture duo ESP32-S3 + RV1106 |
| Temp / humidité / vibration / luminosité | P0 pour les 4 |
| Déclenchement par espèce spécifique | P1/P2 — nécessite classificateur espèce |
| Chauve-souris (ultrasons 100–200 kHz) | P2 — module dédié |

---

## 5. Intégration du BOM station bioacoustique/caméra

### Architecture figée dans le BOM
```
ESP32-S3 always-on (100–400 µA)
    ├─ microphones MEMS I2S × 2
    ├─ capteurs environnementaux
    ├─ GPS / RTC
    ├─ détection sonore légère (VAD)
    ├─ gestion énergie
    └─ réveil modules lourds
        ↓
Pi Zero 2W on-demand (coupé via load switch)
    ├─ caméra IMX708 12MP NoIR Wide
    ├─ LEDs IR 940 nm
    ├─ stockage média
    ├─ compression audio/image
    ├─ portail WiFi local
    └─ upload cloud
        ↓
Module 4G LTE Cat-1
        ↓
Cloud — BirdNET complet
```

### Ce que le BOM apporte
1. **La décision BirdNET est prise : cloud, pas embarqué.** Résout proprement la Tension 1.
2. **L'architecture "duo processeur dans un boîtier unique" est confirmée.** ESP32-S3 = Satellite Lite, Pi Zero 2W = Base — dans la même enceinte.
3. **Le coût est posé : 450–550 € prototype, 600–850 € pré-série.**

### Tensions entre le BOM et les décisions existantes

#### Tension A — P0 SCOPE_LOCK de facto abandonné
Le BOM intègre bioacoustique, GPS, 4G, double SD, capteur spectral — tout ce que le SCOPE_LOCK avait reporté en P1/P2. C'est un saut direct à un prototype P1 intégré. **Décision consciente à confirmer avec JCH.**

#### Tension B — LoRa absent du BOM ⚠️
L'ADR-003 radio avait retenu un module LPWAN pour les alertes. Le BOM l'a supprimé au profit de WiFi local + 4G.  
Conséquences : pas de notification longue portée sans SIM, pas de mode hors couverture 4G.  
Un module SX1262 coûte 8–12 € et consomme 2 µA en veille. **À ajouter à la BOM.**

#### Tension C — Latence de boot Pi Zero 2W ⚠️
Pi Zero 2W éteint via load switch → **30–60 secondes de boot Linux**. Le sanglier est reparti avant que la caméra soit opérationnelle.

Options :
- **Suspend to RAM** (~500 ms de réveil) — faisable mais complexe à stabiliser
- **RV1106** comme alternative (boot ~2–3 s, coût ~10 €, NPU intégré) — meilleur rapport latence/coût
- **Capture immédiate via ESP32-S3** (module OV5640 sur SPI) en attendant le boot Pi — solution intermédiaire

#### Tension D — IP65/66 vs IP67
Le BOM dit IP65/66. La philosophie P0 et l'ADR boîtier ciblaient IP67. Pour le terrain pluvieux belge avec ruisseaux → IP67 reste préférable.

### Intégration BOM dans les phases WildNexus

| Élément BOM | Statut recommandé |
|---|---|
| ESP32-S3 + PSRAM | P0 validé |
| 2 × MEMS INMP441/ICS-43434 + VAD | P1 |
| Pi Zero 2W on-demand | P1 prototype — surveiller latence boot |
| IMX708 12MP (caméra proto) | P1 |
| IMX462 Starvis (nocturne) | P1/pré-série |
| IR 940 nm | P0 confirmé |
| BME688 (temp/hum/pression/VOC) | P0 partiel — temp+hum oui, VOC en P1 |
| AS7341 spectral 11 canaux | P2 — à supprimer de la BOM proto |
| GPS u-blox M10 | P1 |
| RTC DS3231 | P0 obligatoire |
| 4G LTE Cat-1 | P1 |
| LoRa SX1262 | **À ajouter** — absent, 8–12 €, critique zones sans 4G |
| Double microSD | P1 — P0 = une seule SD |
| BMS + MPPT solaire | P0 LiFePO4 + USB-C ; solaire en P1 |
| Boîtier IP65/66 | P0 — passer à IP67 si possible |

---

## 6. Décisions ouvertes à confirmer avec JCH

**Décision 1 — On saute P0 ou on garde la progression ?**  
Le BOM à 500 € est un prototype P1 intégré. Un P0 caméra seul se ferait à ~150–200 €. Aller directement à la vision complète est possible mais triple la complexité et allonge le temps avant première validation terrain.

**Décision 2 — RV1106 ou Pi Zero 2W comme module média ?**  
Pi Zero 2W = accessible, communauté, HAT caméra officiel, mais boot 30–60 s.  
RV1106 = boot 2–3 s, moins cher, moins consommateur — écosystème plus niche.  
C'est le choix central de cette BOM.

**Décision 3 — BirdNET hybride ou purement cloud ?**  
Le BOM dit cloud. Acceptable si couverture 4G ou WiFi disponible. Pour des sites vraiment isolés, prévoir un mode "stocke et uploade au passage" avec tampon local.

---

## 7. Prochaine action recommandée

Si JCH confirme le BOM comme base de travail :

1. **Ajouter LoRa SX1262** à la BOM (8–12 €, critique pour zones sans 4G)
2. **Trancher RV1106 vs Pi Zero 2W** — tester la latence boot du Pi en suspend-to-RAM
3. **Cibler IP67** plutôt qu'IP65/66 pour le boîtier
4. **Rédiger ADR-004 Bioacoustique P1** — fige l'architecture duo MCU et la décision BirdNET cloud
5. **Forge** peut préparer le plan d'approvisionnement avec fournisseurs et variantes par bloc critique