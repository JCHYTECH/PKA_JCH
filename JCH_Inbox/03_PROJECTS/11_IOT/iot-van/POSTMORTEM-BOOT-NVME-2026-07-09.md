# Post-Mortem — Échec boot HA OS sur NVMe (RPi 5 + X1205)

> **Date :** 2026-07-09  
> **Session :** Dobby 🦉 + JC — 3h d'itérations  
> **Statut :** ❌ ÉCHEC — HA OS ne boote pas depuis le NVMe. LED rouge uniquement.

---

## 1. Ce qu'on a tenté de faire

Installer Home Assistant OS 18.1 sur le SSD NVMe Fanxiang 256GB d'un Raspberry Pi 5 équipé d'un stack Geekworm X1205 UPS HAT (pogo pins, bottom) + Shield PCIe → NVMe (top).

---

## 2. Ce qui fonctionne ✅

- **Pi OS Lite boote parfaitement** depuis la microSD, avec ou sans NVMe connecté
- **Le NVMe est détecté** sous Pi OS (`nvme0n1`, 238.5G, 8 partitions) grâce à `dtparam=pciex1` + `dtparam=pciex1_gen3` dans `/boot/firmware/config.txt`
- **Ethernet direct M5↔RPi fonctionne** : lien 1000baseT full-duplex via adaptateur USB-C AX88179B, SSH IPv6 link-local OK
- **Wi-Fi fonctionne** sous Pi OS (connecté à Proximus-Home-D858, IP 192.168.129.16)
- **EEPROM/bootloader** : mis à jour (mai 2026), BOOT_ORDER=0xf416, PCIE_PROBE=1, POWER_OFF_ON_HALT=1, PSU_MAX_CURRENT=5000
- **Flash HA OS** : image `haos_generic-aarch64-18.1.img` flashée avec succès sur `/dev/nvme0n1` via `dd`
- **Les fichiers de config HA OS** ont été écrits sur les partitions NVMe :
  - p1 (EFI) : `config.txt` avec `dtparam=pciex1` + `dtparam=pciex1_gen3`, `cmdline.txt` avec `ssid=... wpakey=...`
  - p8 (overlay data) : `/etc/NetworkManager/system-connections/wifi` + `ethernet`

---

## 3. Ce qui échoue ❌

### Symptôme principal
Quand on retire la microSD et qu'on tente de booter sur le NVMe seul :
- **LED rouge uniquement** (pas de LED verte)
- **Pas de boot** — le RPi ne démarre même pas le processus
- **Pas de réponse réseau** — ni Wi-Fi (192.168.129.16), ni Ethernet (192.168.100.2), ni mDNS (homeassistant.local)

### Chronologie des échecs
| Tentative | Config | Résultat |
|-----------|--------|----------|
| Boot NVMe sans microSD, avant toute config | LED verte fixe (bootloader cherche, ne trouve rien) |
| Boot NVMe avec Wi-Fi dans cmdline.txt | LED rouge uniquement |
| Boot NVMe avec Wi-Fi dans p8 overlay | LED rouge uniquement |
| Boot NVMe avec Ethernet + IP fixe dans p8 | LED rouge uniquement |

---

## 4. Hypothèses sur la cause racine

### Hypothèse A : Alimentation insuffisante via X1205 pogo pins ⚡ (probable)
Le X1205 alimente le RPi 5 via 7 pogo pins. Si le contact est imparfait, la tension chute sous charge — et le boot NVMe consomme plus que le boot microSD.
- **Indice :** LED rouge uniquement = le PMIC ne délivre pas les rails de tension
- **Indice :** Pi OS boote depuis microSD avec NVMe connecté (consommation modérée), mais pas depuis NVMe (consommation plus élevée au démarrage)
- **Indice :** La FAQ Geekworm mentionne explicitement ce problème (« loose brass standoffs → low voltage warning »)
- **Test à faire :** brancher l'alim officielle 27W directement sur le port USB-C du RPi 5 (en contournant le X1205), sans microSD, et voir si ça boote sur NVMe

### Hypothèse B : Incompatibilité HA OS 18.1 avec le SSD Fanxiang
Le SSD Fanxiang est un modèle chinois économique. Certains SSD NVMe nécessitent des paramètres kernel spécifiques.
- **Test à faire :** cloner Pi OS de la microSD vers le NVMe et tenter de booter. Si ça marche, le problème est HA OS, pas le hardware.

### Hypothèse C : HA OS 18.x ne lit pas config.txt sur la partition EFI
HA OS a changé de structure de boot en version 18.x. Il est possible que `config.txt` sur p1 ne soit pas pris en compte.
- **Test à faire :** flasher la version 17.3 (dernière stable avant 18.x) et comparer

### Hypothèse D : Problème mécanique de boot NVMe
Le RPi 5 tente de booter sur NVMe (BOOT_ORDER inclut `6`) et se bloque parce que le firmware NVMe du SSD ne répond pas correctement.
- **Test à faire :** débrancher le NVMe, booter Pi OS, rebrancher à chaud, cloner Pi OS → NVMe, tester le boot

---

## 5. Pistes testées et éliminées

| Piste | Résultat |
|-------|----------|
| dtparam=pciex1 absent | ✅ Ajouté, fonctionne sous Pi OS |
| BOOT_ORDER sans NVMe | ✅ Configuré (0xf416) |
| Wi-Fi non configuré | ✅ cmdline.txt + p8 overlay → pas d'effet |
| Pas d'Ethernet | ✅ Configuré avec IP fixe 192.168.100.2 → jamais joignable |
| EEPROM trop vieux | ✅ Mis à jour (mai 2026) |
| Clé USB import réseau | ❌ N'a pas fonctionné (fichier non sauvegardé au 1er essai, non détecté au 2e) |
| Dupont pin 6↔8 GPIO | ❌ Sans effet — l'auto-power-on X1205 est géré par résistance soudée |
| Hot-plug NVMe | ❌ Le bus PCIe ne détecte pas le SSD après rescan à chaud |

---

## 6. Prochaines étapes recommandées

### Priorité 1 — Tester l'alimentation directe
- Démonter le X1205 du RPi 5
- Brancher l'alim officielle 27W **directement** sur le port USB-C du RPi 5
- Sans microSD, avec NVMe connecté
- Observer les LEDs
- Si le RPi boote → **le X1205 est le coupable**

### Priorité 2 — Cloner Pi OS sur NVMe
- Depuis Pi OS (microSD) : `sudo dd if=/dev/mmcblk0 of=/dev/nvme0n1 bs=4M status=progress`
- Retirer microSD, booter
- Si ça boote → le hardware NVMe est OK, le problème est HA OS

### Priorité 3 — Essayer HA OS 17.3
- Version stable qui précède la refonte 18.x
- Moins de changements structurels, meilleure compatibilité RPi 5

### Priorité 4 — Revenir à microSD
- Si le NVMe reste problématique : installer HA OS sur microSD (sacrifier la fiabilité long terme, mais fonctionnel)
- Une microSD 128 Go A2 est acceptable pour du prototypage

---

## 7. Fichiers modifiés pendant la session

| Fichier | Modification |
|---------|-------------|
| `ASSEMBLAGE-RPi5-VANLIFE.md` | Section 4 réécrite (298→500 lignes) — procédure boot NVMe complète |
| `MEMORY.md` | Ajout session 2026-07-09 — diagnostic échec + correctif guide |
| `POSTMORTEM-BOOT-NVME-2026-07-09.md` | Ce fichier |

---

## 8. État actuel du matériel

- RPi 5 assemblé avec X1205 UPS HAT + Shield NVMe + SSD Fanxiang
- NVMe flashé avec HA OS 18.1 + configs réseau
- MicroSD flashée avec Pi OS Lite (Wi-Fi Proximus configuré)
- Adaptateur USB-C → Ethernet disponible pour lien direct M5↔RPi
- **LED : rouge uniquement** quand on tente le boot NVMe sans microSD

---

*Document rédigé par Dobby 🦉 à la demande de JC — 2026-07-09, 20h55.*
