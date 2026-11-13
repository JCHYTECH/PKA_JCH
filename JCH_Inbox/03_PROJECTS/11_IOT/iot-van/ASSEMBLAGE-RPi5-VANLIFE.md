# Assemblage RPi 5 Vanlife — Guide pas à pas

> **Date :** 2026-07-01 — Tous les composants sont reçus.  
> **Projet :** 11_IOT — Station domotique embarquée Westfalia Kelsey  
> **Temps estimé :** 45-60 minutes  
> **Niveau :** Débutant éclairé (aucune soudure, tout se clipse/visse)

---

## 0. BOM — Ce que tu as reçu

| # | Composant | Référence | Emplacement |
|---|-----------|-----------|-------------|
| 1 | Raspberry Pi 5 4GB | — | Cœur |
| 2 | Alim officielle RPi 5 27W | USB-C PD 5V/5A | Externe |
| 3 | Refroidisseur actif RPi 5 | Ventilateur + dissipateur officiel | Sur le RPi |
| 4 | Geekworm X1205 UPS HAT | Pogo pins, 2× 18650 | **En dessous** du RPi |
| 5 | Geekworm X1201-C1 boîtier métal | ×2 reçus | Contient le stack |
| 6 | SSD Fanxiang NVMe M.2 256GB | 2280 | Slot NVMe |
| 7 | PCIe to M.2 NVMe Shield | ×2 reçus | **Au-dessus** du RPi |
| 8 | PV PI HAT | AutoEcology, 150 AUD | **Tout en haut** du stack GPIO |
| 9 | Sonoff ZBDongle-E | Zigbee 3.0 | Port USB |
| 10 | UGREEN USB Audio | Adaptateur audio | Port USB |

---

## 1. Préparation — Avant de toucher quoi que ce soit

### ⚡ Règle d'or anti-statique
- Pose ta main sur une surface métallique reliée à la terre (radiateur, châssis) avant de manipuler le RPi.
- Travaille sur une surface non conductrice (bois, carton, tapis antistatique).
- Évite les pulls en laine et les chats sur la table.

### 📦 Déballe tout et vérifie
```
[ ] RPi 5 dans sa boîte antistatique
[ ] Alim USB-C 27W + câble
[ ] Ventilateur + dissipateur officiel RPi 5
[ ] X1205 UPS HAT (carte verte) + 2 connecteurs 18650
[ ] X1201-C1 boîtier métal (2 pièces : haut + bas)
[ ] Vis, standoffs, écrous (fournis avec boîtier et HATs)
[ ] SSD Fanxiang 256GB (barrette verte/bleue, format 2280)
[ ] Shield PCIe → M.2 NVMe (carte PCB avec slot M.2)
[ ] PV PI HAT (carte avec connecteurs XT30 jaunes)
[ ] Sonoff ZBDongle-E (clé USB blanche)
[ ] UGREEN USB Audio (petit dongle)
[ ] Pince à épiler ou petit tournevis cruciforme
```

> **Note batteries 18650 :** Le X1205 nécessite 2 accus 18650 Li-Ion **non protégés** (flat top, pas button top). Vérifier que tu les as — pas listés dans le hardware-state.

---

## 2. Assemblage — Étape par étape

### Étape 1 — Montage du refroidisseur sur le RPi 5

1. Retire le RPi 5 de son blister antistatique.
2. Le **dissipateur** (plaque alu noire à ailettes) se fixe sur le SoC BCM2712 (la grosse puce au centre).
   - Retire le film plastique protecteur sous le dissipateur.
   - Aligne-le sur le SoC, appuie fermement 10 secondes.
3. Le **ventilateur** se connecte au port `FAN` du RPi 5 (petit connecteur blanc 4 pins, à droite du GPIO, marqué `FAN`).
   - Le connecteur a un détrompeur — il ne rentre que dans un sens.
   - Le ventilateur se visse ou se clipse sur le support intégré au boîtier X1201-C1 (voir étape 4).

---

### Étape 2 — Préparation du X1205 UPS HAT

1. Sors le X1205 de son sachet.
2. Repère les **pogo pins** (7 petits cylindres dorés à ressort sur le dessus de la carte). C'est par là que le X1205 communique avec le RPi — **pas besoin de GPIO**, pas de nappe.
3. Repère les deux **emplacements 18650** (rectangles noirs avec ressort à une extrémité).
4. **N'insère PAS les accus maintenant** — on le fera à la fin.

---

### Étape 3 — Stacker X1205 + RPi 5

C'est l'étape la plus délicate. Le stack se fait dans cet ordre (de bas en haut) :

```
        ┌─────────────────────┐   ← GPIO 40 pins du RPi 5 (exposé)
        │     PV PI HAT       │   ← Étape 7
        ├─────────────────────┤
        │  NVMe Shield + SSD  │   ← Étape 5-6
        ├─────────────────────┤
        │      RPi 5          │
        ├─────────────────────┤
        │   X1205 UPS HAT     │   ← Étape 3
        └─────────────────────┘
```

1. Pose le X1205 **à l'envers** (pogo pins vers le haut) sur la table.
2. **Sans les accus**, aligne le RPi 5 au-dessus du X1205 :
   - Les trous de vis des 4 coins doivent correspondre.
   - Les pogo pins du X1205 touchent les **pastilles dorées sous le RPi 5** (marquées `POWER`, `GND`, `SDA`, `SCL`, etc.). Il y a 7 pastilles alignées près du bord du PCB.
   - ⚠️ **Vérification critique :** les pogo pins doivent être parfaitement alignés avec les pastilles. Un décalage d'1 mm → pas de contact → pas d'alimentation.

3. Fixe avec les **4 vis + standoffs fournis** :
   - Standoff (entretoise) côté X1205 → RPi 5 → vis par-dessus.
   - Serre **modérément** — c'est du PCB, pas une roue de camion. Dès que ça résiste, stop.
   - L'ensemble X1205+RPi 5 doit être rigide, sans jeu.

4. Vérifie visuellement par le côté : les pogo pins sont bien compressés contre le RPi ? Oui → on continue.

---

### Étape 4 — Mise en boîtier X1201-C1

1. Le boîtier X1201-C1 est en deux parties :
   - **Base** (fond, avec ouvertures pour les ports)
   - **Couvercle** (dessus, avec grille d'aération)

2. Pose la **base** du boîtier sur la table.
3. Insère le stack X1205+RPi 5 dans la base :
   - Les ports USB/Ethernet/HDMI du RPi 5 s'alignent avec les découpes arrière.
   - Il y a des **encoches** dans la base qui guident le positionnement.

4. Fixe le RPi 5 à la base avec les vis fournies (4 points).
5. Le **ventilateur** se fixe sur le couvercle (intérieur, au-dessus du SoC) :
   - Il y a un emplacement prévu avec des trous de vis.
   - Oriente le ventilateur pour que le flux d'air aspire du bas vers le haut (label visible depuis l'intérieur = bon sens).
   - Connecte le câble au port `FAN` du RPi 5 (déjà fait à l'étape 1).

---

### Étape 5 — Installation du SSD sur le Shield NVMe

1. Prends le **Shield PCIe → M.2 NVMe** (carte PCB avec un slot M.2).
2. Repère le slot M.2 — un connecteur long avec 4-5 broches, une vis de fixation à l'autre extrémité.
3. Insère le SSD Fanxiang 256GB :
   - Oriente le SSD : les connecteurs dorés vers le slot, l'étiquette vers le haut.
   - Angle d'insertion : ~30°, enfonce jusqu'au clic.
   - Rabats le SSD à plat, fixe avec la vis M.2 (petite vis cruciforme fournie).

---

### Étape 6 — Montage du Shield NVMe sur le RPi 5

1. Sur le RPi 5, repère le **connecteur PCIe** (petit connecteur blanc étroit, 16 pins, à gauche du GPIO, marqué `PCIE`).
2. Le Shield NVMe se monte au-dessus du RPi 5 :
   - Utilise les standoffs longs fournis avec le Shield.
   - Le connecteur PCIe du Shield s'aligne avec celui du RPi 5.
   - ⚠️ Le câble nappe PCIe est **déjà soudé** sur le Shield — branche l'autre extrémité sur le connecteur `PCIE` du RPi 5. Détrompeur : le fil rouge/coloré de la nappe va vers le bas (pin 1).

3. Fixe le Shield avec les 4 vis aux coins. Laisse le GPIO 40 pins **exposé** — le PV PI HAT va s'y brancher.

---

### Étape 7 — PV PI HAT (tout en haut)

1. Le PV PI HAT se branche sur le **connecteur GPIO 40 pins** du RPi 5 :
   - Les pins dépassent à travers le Shield NVMe (normal, ils sont stackables).
   - Aligne le connecteur femelle du PV PI avec les pins mâles du GPIO.
   - ⚠️ Vérifie que toutes les pins sont droites avant d'enfoncer.
   - Appuie fermement et uniformément — ça doit s'enfoncer de ~5-6 mm.

2. Le PV PI HAT a deux connecteurs **XT30 jaunes** :
   - L'un pour le **panneau solaire** (marqué SOLAR ou PV INPUT)
   - L'autre pour la **batterie LiFePO4 12V** (marqué BATTERY)
   - Ne branche rien pour l'instant — on câblera ça dans le van.

3. Fixe les standoffs si fournis (le PV PI peut rester sur les pins sans fixation supplémentaire, c'est assez rigide).

---

### Étape 8 — Fermeture du boîtier

1. Vérifie qu'aucun câble n'est coincé.
2. Pose le **couvercle** du X1201-C1 sur la base :
   - Les 4 trous de vis s'alignent.
   - Le connecteur du ventilateur ne doit pas être pincé.
3. Visse les 4 vis du couvercle.

---

### Étape 9 — Insertion des accus 18650

1. Ouvre la trappe à accus sur le **dessous** du boîtier (ou sur le côté du X1205, selon le modèle).
2. Insère **2 accus 18650 Li-Ion flat top** :
   - Respecte la polarité (+ et −) indiquée dans le compartiment.
   - Le ressort = pôle négatif (−).
   - Le contact plat = pôle positif (+).
3. Referme la trappe.

---

## 3. Câblage externe

### Alimentation
```
Prise 12V batterie cellule
   │
   ├── Porte-fusible 5A (au plus près de la batterie)
   │
   ├── Convertisseur DC-DC 12V→5V USB-C PD (non reçu ? vérifier)
   │
   └── Alim officielle RPi 5 27W → USB-C RPi 5
```

> **Note :** L'alim officielle RPi 5 fonctionne sur 230V AC. Pour le 12V DC du van, il faut un **convertisseur DC-DC 12V→5V USB-C PD 5A** (non listé dans le hardware-state). En attendant, utiliser l'alim secteur pour les tests sur banc.

### Dongles USB
```
RPi 5 ports USB :
  ├── USB 2.0 (noir) → Sonoff ZBDongle-E (Zigbee)
  ├── USB 2.0 (noir) → Libre
  ├── USB 3.0 (bleu) → UGREEN USB Audio
  └── USB 3.0 (bleu) → Libre
```

### Panneau solaire (quand acheté)
```
Panneau solaire → câble XT30 → PV PI HAT (SOLAR)
Batterie LiFePO4 12V → câble XT30 → PV PI HAT (BATTERY)
```

---

## 4. Configuration boot NVMe & installation HA OS

> **⚠️ Ne pas sauter cette section.** Le RPi 5 ne boote PAS sur NVMe par défaut.
> Flasher HA OS directement sur le SSD sans les étapes ci-dessous = écran noir garanti.
> **Temps estimé :** 45-60 min. **Prérequis critique :** une microSD (≥ 8 Go).

### 4.0 — Prérequis : ce dont tu as besoin

- [ ] **MicroSD ≥ 8 Go** — indispensable. Impossible de configurer le bootloader sans elle.
- [ ] **Câble USB-C PD e-mark 5A** — le RPi 5 négocie 5V/5A via Power Delivery. Un câble standard = max 3A = undervoltage = `throttled=0x50000`.
- [ ] **Alim officielle RPi 5 27W** (pour le banc — le convertisseur DC-DC 12V→5V viendra plus tard).
- [ ] **Câble HDMI + écran** (pour voir ce qui se passe au premier boot).
- [ ] **Clavier USB** (optionnel mais utile si le SSH ne répond pas).

---

### 4.1 — Vérification critique : pogo pins X1205 (2 min)

> C'est la cause n°1 de « ça ne s'allume pas » d'après la FAQ officielle Geekworm.

1. **Avant de brancher l'alim**, regarde le stack par le côté avec une lampe.
2. Vérifie que chaque pogo pin (7 cylindres dorés sur le X1205) est **compressé** contre sa pastille sous le RPi 5.
3. Si un pogo pin flotte dans le vide → les standoffs sont trop longs ou mal vissés.
4. Les 4 vis doivent être **fermes** (pas écrasées, mais sans jeu).

**Validation :** le stack X1205+RPi 5 ne bouge pas quand tu le secoues doucement.

---

### 4.2 — Premier boot sur microSD (15 min)

> On installe Raspberry Pi OS Lite sur microSD pour configurer le bootloader.
> Le SSD NVMe reste branché dans le Shield — on va le détecter depuis l'OS microSD.

**[M5]** Flasher la microSD avec Raspberry Pi Imager :

1. **Device :** Raspberry Pi 5
2. **OS :** Raspberry Pi OS (other) → **Raspberry Pi OS Lite (64-bit)**
3. **Storage :** la microSD
4. **Edit Settings (⚙️) :**
   - Hostname : `tkajch`
   - Username : `jchavaux` / mot de passe
   - Wi-Fi : configurer le réseau local (ou sauter si Ethernet)
   - SSH : activer (mot de passe)
   - Timezone : Europe/Brussels, layout : be
5. Écrire. Insérer la microSD dans le RPi 5.

**Brancher et booter :**
1. Alim USB-C → RPi 5. Écran HDMI branché.
2. LED rouge fixe + LED verte clignotante = boot OK.
3. Si rien ne s'allume → problème pogo pins (retour §4.1).
4. Attendre ~2 min, se connecter :
```bash
[M5] ssh jchavaux@tkajch.local
```

---

### 4.3 — Mise à jour du bootloader EEPROM (5 min)

```bash
# Vérifier la version actuelle
sudo rpi-eeprom-update
# → doit afficher la version installée et la dernière disponible

# Mettre à jour
sudo rpi-eeprom-update -a

# ⚠️ NE PAS rebooter maintenant — on configure d'abord le BOOT_ORDER.
```

---

### 4.4 — Configuration NVMe dans l'EEPROM (5 min)

```bash
sudo rpi-eeprom-config --edit
```

Dans l'éditeur nano, modifier/ajouter :

```
BOOT_ORDER=0xf416
PCIE_PROBE=1
POWER_OFF_ON_HALT=1
```

| Paramètre | Signification |
|-----------|--------------|
| `BOOT_ORDER=0xf416` | SD (`1`) → USB (`4`) → NVMe (`6`) → retry (`f`). Le `6` est absent par défaut. |
| `PCIE_PROBE=1` | Force la détection du bus PCIe au démarrage. |
| `POWER_OFF_ON_HALT=1` | Coupe le 5V GPIO quand le Pi est éteint (économie). |

Ctrl+O → Enter → Ctrl+X. **Ne pas rebooter encore.**

---

### 4.5 — Activation du port PCIe dans config.txt (2 min)

Le port PCIe du RPi 5 est **désactivé par défaut**. Sans l'overlay, le SSD NVMe est invisible.

```bash
sudo nano /boot/firmware/config.txt
```

Ajouter à la fin :

```
# Activer le port PCIe pour NVMe
dtparam=pciex1

# Forcer PCIe Gen 3 — obligatoire pour compatibilité SSD (Fanxiang et marques chinoises)
dtparam=pciex1_gen3
```

> `dtparam=pciex1` est **obligatoire**. `dtparam=pciex1_gen3` est fortement recommandé — sans lui, certains SSD provoquent erreurs I/O et kernel panic. Source : wiki Geekworm + forums RPi.

---

### 4.6 — Suppression de l'avertissement 5A (2 min)

Le X1205 délivre 5A, mais le RPi ne le sait pas et affiche un avertissement au boot.

```bash
sudo rpi-eeprom-config --edit
```
Ajouter à la fin :
```
PSU_MAX_CURRENT=5000
```
Ctrl+O → Enter → Ctrl+X.

---

### 4.7 — Premier reboot & vérification NVMe (5 min)

```bash
sudo reboot
```

Attendre (~1-2 min), puis :

```bash
ssh jchavaux@tkajch.local

# 🔍 LE TEST CRITIQUE — le SSD est-il visible ?
lsblk
# → doit montrer nvme0n1 (SSD NVMe) + mmcblk0 (microSD)

# Si nvme0n1 n'apparaît PAS :
# 1. Vérifier dtparam=pciex1 dans /boot/firmware/config.txt
# 2. Vérifier la nappe PCIe : fil rouge → pin 1
# 3. Vérifier le SSD bien enfoncé dans le slot M.2
# 4. Ajouter dtparam=pciex1_gen3 si pas déjà fait

# Vérifier l'absence d'undervoltage
vcgencmd get_throttled
# → doit retourner throttled=0x0
# → si throttled=0x50000 : problème d'alim / câble non PD

# Vérifier la tension d'entrée
vcgencmd pmic_read_adc | grep EXT5V_V
# → doit afficher ~5.0-5.2V

# Vérifier le X1205
sudo i2cdetect -y 1
# → doit montrer 0x32 ou 0x36 (adresse I2C du X1205)
```

---

### 4.8 — Flasher Home Assistant OS sur le SSD (15 min)

> Le bootloader sait maintenant booter sur NVMe. On installe HA OS.

**Méthode A — Depuis le Mac M5 (recommandé) :**

```bash
# [M5] Télécharger HA OS pour RPi 5 : https://www.home-assistant.io/installation/raspberrypi
# Démonter le SSD du Shield, le brancher au Mac via adaptateur USB-NVMe
[M5] diskutil list                          # repérer /dev/diskX
[M5] sudo diskutil unmountDisk /dev/diskX
[M5] sudo dd if=haos_rpi5-xx.img of=/dev/rdiskX bs=4m status=progress
```

**Méthode B — Depuis le RPi 5 (si pas d'adaptateur USB-NVMe) :**

```bash
# Sur le RPi 5 (booté microSD), télécharger et flasher directement
wget https://github.com/home-assistant/operating-system/releases/download/.../haos_rpi5-xx.img.xz
xz -d haos_rpi5-xx.img.xz
sudo dd if=haos_rpi5-xx.img of=/dev/nvme0n1 bs=4m status=progress
```

---

### 4.9 — Premier boot HA OS sur NVMe (10-20 min)

1. **Retirer la microSD** du RPi 5 (le bootloader est dans l'EEPROM, plus besoin de la SD).
2. Vérifier que le SSD est dans le Shield NVMe.
3. Rebrancher l'alim USB-C.
4. **C'est long.** HA OS télécharge les conteneurs Docker. La LED verte clignote activement.
5. Ne pas débrancher avant **20 minutes**.
6. Navigateur → `http://tkajch.local:8123` → attendre « Preparing Home Assistant » → écran de création de compte.

---

### 4.10 — Configuration initiale HA

1. Créer un compte (nom, mot de passe).
2. Nommer l'installation : « Lupo ».
3. Localisation : important pour automatisations (lever/coucher du soleil).
4. Laisser HA découvrir les appareils réseau.

**Validation finale :**
- [ ] `http://tkajch.local:8123` affiche le dashboard HA
- [ ] Compte créé, dashboard visible
- [ ] Pas de reboot intempestif pendant l'installation

---

## 5. Vérifications matérielles

| Check | Commande / Méthode | Attendu |
|-------|-------------------|---------|
| Pogo pins X1205 | Visuel, lampe côté stack | Tous compressés contre pastilles RPi |
| Ventilateur tourne | Écouter au boot | Souffle léger |
| Pas d'undervoltage | `vcgencmd get_throttled` | `throttled=0x0` |
| Tension entrée 5V | `vcgencmd pmic_read_adc \| grep EXT5V_V` | 5.0-5.2V |
| SSD reconnu | `lsblk` | `nvme0n1` |
| X1205 UPS | `i2cdetect -y 1` | Adresse 0x32 ou 0x36 |
| PV PI HAT | `dmesg \| grep -i pv` | Device reconnu |
| Zigbee dongle | `lsusb` | Sonoff ZBDongle |
| Audio USB | `lsusb` | UGREEN device |
| Température CPU | `vcgencmd measure_temp` | < 50°C idle |
| GPIO stack intact | `gpio readall` | Tous les pins visibles |

---

## 6. Prochaines étapes (dans l'ordre)

### Déjà fait ✅
- [x] RPi 5 assemblé (X1205 + NVMe Shield + SSD + ventilateur)
- [x] Accus 18650 ×20 reçus (8 juillet 2026) — 2 dans X1205, 18 en réserve
- [x] Boîtier X1201-C1 ×2 reçus

### Phase 1 — Setup logiciel (cette semaine)
- [ ] **Bootloader NVMe** → suivre §4.1 à §4.7 avec une microSD **(priorité absolue)**
- [ ] **Flasher HA OS** → §4.8-4.10
- [ ] **Tailscale** → module complémentaire HA (accès distant)
- [ ] **Zigbee** → Sonoff ZBDongle-E + appairer SNZB-02D
- [ ] **Access Point Wi-Fi** → `VanLife_Network` (dashboard sans box)

### Phase 2 — Quand le van est livré
- [ ] Mise en boîtier X1201-C1 (attendre setup logiciel stable)
- [ ] Convertisseur DC-DC 12V→5V USB-C PD 5A
- [ ] Câblage batterie cellule → fusible 5A → convertisseur → RPi
- [ ] Dongle 4G USB (rend Tailscale utile 24/7)

### Phase 3 — Futur
- [ ] Capteurs Zigbee additionnels
- [ ] PV PI HAT + panneau solaire + batterie LiFePO4
- [ ] Dashboard mobile personnalisé (Lovelace YAML)
- [ ] Automatisations : alerte frigo, niveau eau, batterie faible

---

## Références

- `docs/rpi-vanlife-guide-complet.md` — Guide conceptuel complet
- `docs/rpi-vanlife-mode-emploi.md` — Mode d'emploi post-install (Zigbee, dashboard, WiFi AP)
- `adr/ADR-003-ssd-nvme-boot.md` — Décision SSD NVMe obligatoire
- `_shared/hub-esneux.md` — Architecture stack RPi + HATs
- `ADR-005-plateforme-hardware-rpi5-vs-x86.md` — Décision RPi 5 « armuré »
- Geekworm X1205 Wiki : https://wiki.geekworm.com/X1205
- Geekworm NVMe Boot Guide : https://wiki.geekworm.com/NVMe_SSD_boot_with_the_Raspberry_Pi_5
- PV PI Manager : https://github.com/lukeditria/pv-pi-manager

---

*Généré par Dobby 🦉 — 2026-07-01, révisé 2026-07-09 — Correction bootloader NVMe (leçons terrain JC).*
