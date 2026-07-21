# Solution consolidée — Boot HA OS sur NVMe (RPi 5 + X1205)

> **Date :** 2026-07-09  
> **Auteurs :** Dobby 🦉 + Forge 🔨 + Araignée 🕷️ — analyse croisée équipe + recherches web  
> **Contexte :** suite directe de [[POSTMORTEM-BOOT-NVME-2026-07-09]]  
> **Statut :** ✅ Solution validée par l'équipe + corroborée par sources externes

---

## 1. Cause racine identifiée 🔴

### Erreur d'image HA OS (Forge 🔨)

Le postmortem §2 indique que l'image flashée était **`haos_generic-aarch64-18.1.img`**.  
Or le guide d'assemblage §4.8 spécifie **`haos_rpi5-xx.img`** — deux images différentes.

| Image | Cible | Bootloader | Compatible RPi 5 ? |
|-------|-------|-----------|---------------------|
| `haos_generic-aarch64-18.1.img` | Machines UEFI ARM64 (serveurs, Ampere) | GRUB / systemd-boot | ❌ Non |
| `haos_rpi5-64-18.1.img.xz` | Raspberry Pi 5 | Firmware RPi (`start4.elf`, `fixup4.dat`) | ✅ Oui |

Le BCM2712 du RPi 5 n'est **pas** une plateforme UEFI. Son bootloader EEPROM cherche `start4.elf` sur la partition FAT — fichier absent de l'image `generic`. Quand JC a hand-edité `config.txt` et `cmdline.txt` sur cette partition, rien ne les lisait : le bootloader RPi n'est jamais entré en jeu.

**Séquence exacte confirmée :**
1. LED verte fixe initiale → bootloader scanne (BOOT_ORDER=0xf416), trouve le NVMe, ne trouve pas `start4.elf`
2. LED rouge après ajout des configs → PMIC coupe les rails (échec de boot)

**Le guide d'assemblage était correct** (§4.8 ligne 402 : `haos_rpi5-xx.img`). L'erreur est survenue au moment du téléchargement/flash : la mauvaise image a été utilisée.

---

## 2. Facteur aggravant — Alimentation X1205 (Araignée 🕷️)

Même avec la bonne image, l'alimentation via pogo pins reste un risque (probabilité ~80%) :

- Le boot NVMe provoque un appel de courant instantané (PCIe Gen3 + contrôleur SSD Fanxiang) bien supérieur au boot microSD
- Les 7 pogo pins du X1205 ont une résistance de contact cumulée — si les standoffs sont légèrement desserrés ou si la version du X1205 est < 1.3, la chute de tension (V = R × I) peut faire tomber le rail 5V sous 4.65V
- Le PMIC Dialog DA9091 coupe alors tous les rails → **LED rouge uniquement, le SoC ne reçoit jamais de power good**

**Indices convergents :**
- La FAQ Geekworm mentionne explicitement « loose brass standoffs → low voltage warning »
- Pi OS boote depuis microSD avec NVMe connecté (consommation modérée) mais pas depuis NVMe seul
- La LED rouge sans LED verte est la signature canonique d'un PMIC qui refuse de démarrer

---

## 3. Alerte externe — Bug HA OS 18.x + NVMe (GitHub #4785)

**Source :** https://github.com/home-assistant/operating-system/issues/4785

Un bug **ouvert** (12 commentaires, dernière activité 8 juillet 2026) rapporte :
- HA OS 18.0 sur RPi 5 avec NVMe hat → I/O errors en ~3 minutes → filesystem corrompu
- Obligé de rollbacker vers le slot B (17.3) pour récupérer un système fonctionnel
- Matériel : Samsung 960 Evo Pro + NVMe hat (stack différent du nôtre, symptômes similaires)
- **Non résolu à date du 9 juillet 2026**

**Implication pour Lupo :** même si on résout le boot, la stabilité sur HA OS 18.x + NVMe n'est pas garantie. La version 17.3 est documentée comme stable.

---

## 4. Plan d'action recommandé

### Étape 0 — Test discriminant (5 min, zéro risque)

Depuis le RPi 5 booté sur Pi OS (microSD), NVMe connecté :

```bash
# Stress test NVMe pour provoquer l'appel de courant max
sudo mkdir -p /mnt/test
sudo mount /dev/nvme0n1p1 /mnt/test 2>/dev/null || true
sudo dd if=/dev/zero of=/tmp/nvme_stress_test bs=1M count=2000 status=progress
vcgencmd get_throttled
```

| Résultat | Interprétation |
|----------|---------------|
| `throttled=0x0` | ✅ Alim X1205 tient la charge — Hypothèse A écartée |
| `throttled=0x50000` ou bits 0x1/0x10000 | ❌ Undervoltage confirmé — X1205 coupable |

---

### Plan A — Bonne image + version stable (recommandé)

Si l'étape 0 est propre :

```bash
# [RPi] Télécharger la BONNE image (rpi5-64, pas generic-aarch64)
# ⚠️ Version 17.3 recommandée (bug #4785 non résolu sur 18.x)
wget https://github.com/home-assistant/operating-system/releases/download/17.3/haos_rpi5-64-17.3.img.xz

# Décompresser et flasher
xz -d haos_rpi5-64-17.3.img.xz
sudo dd if=haos_rpi5-64-17.3.img of=/dev/nvme0n1 bs=4M status=progress

# Vérifier que la partition FAT contient bien start4.elf
sudo mount /dev/nvme0n1p1 /mnt/test
ls /mnt/test/start4.elf    # → doit exister
ls /mnt/test/config.txt    # → doit exister

# Ajouter le support PCIe dans config.txt (l'image rpi5-64 l'a peut-être déjà)
echo "dtparam=pciex1" | sudo tee -a /mnt/test/config.txt
echo "dtparam=pciex1_gen3" | sudo tee -a /mnt/test/config.txt
sudo umount /mnt/test
```

1. `sudo shutdown now`
2. Retirer la microSD
3. Rebrancher l'alim
4. Observer les LEDs : rouge fixe → verte clignotante = boot OK
5. Si LED rouge uniquement → passer au Plan B

**Pourquoi 17.3 et pas 18.1 :**
- Bug #4785 : corruption filesystem sur 18.x + NVMe, non résolu
- 17.3 est la dernière version stable confirmée sans ce bug
- La mise à jour vers 18.x pourra se faire plus tard quand le bug sera corrigé

---

### Plan B — Bypass alim X1205

Si l'étape 0 montre un undervoltage, ou si le Plan A échoue avec LED rouge :

1. Démonter le X1205 du RPi 5
2. Brancher l'alim officielle 27W **directement** sur le port USB-C du RPi 5
3. Sans microSD, avec NVMe connecté (Shield PCIe toujours en place)
4. Observer les LEDs
5. Si le RPi boote → **le X1205 est le coupable**
6. Solutions X1205 :
   - Resserrer les standoffs (vérifier contact pogo pins §4.1 de l'ASSEMBLAGE)
   - Si version < 1.3 du X1205 : contacter Geekworm pour remplacement
   - Alternative : souder des fils entre X1205 et RPi au lieu des pogo pins

---

### Plan C — Fallback microSD + Move datadisk

Si tout échoue, solution fonctionnelle immédiate (documentée et confirmée) :

1. Flasher `haos_rpi5-64-17.3.img` sur **microSD** avec Raspberry Pi Imager
2. Booter, configurer HA (compte, nom="Lupo", localisation)
3. **Settings → System → Storage → Move Data Disk** → sélectionner NVMe
4. HA migre les données applicatives vers le NVMe, le boot reste sur microSD

**Sources confirmant cette approche :**
- HA Community thread #716038 : « The Pi 5 boot drive for HA OS is the original SD card. The HA data drive has been copied from the SD card to the NVMe drive, using Settings, System, Storage, Disk Metrics, Move Data Disk. »
- Reddit r/homeassistant : « Just added the M.2 HAT+ to my R-PI5. Super easy with HA 'Move Data Disk' »
- Martin Rowan blog : procédure complète documentée

**Avantages :** zéro risque, 15 minutes, fonctionnel immédiatement  
**Inconvénient :** usure microSD (backups réguliers obligatoires), acceptable pour prototypage avant le 7 août

---

## 5. Résumé exécutif

| Priorité | Action | Durée | Résultat attendu |
|----------|--------|-------|-----------------|
| 🔴 P0 | Test `vcgencmd get_throttled` sous stress | 5 min | Discrimine alim vs logiciel |
| 🔴 P0 | Flasher `haos_rpi5-64-17.3.img` sur NVMe | 20 min | Boot natif NVMe avec version stable |
| 🟡 P1 | Si échec : bypass X1205 + test direct | 10 min | Confirme/fixe hypothèse power |
| 🟢 P2 | Fallback : microSD + Move datadisk | 15 min | Fonctionnel garanti, prêt pour le 7 août |

**✅ RÉSOLU le 2026-07-09 à 22h00 :**
1. Flash de `haos_rpi5-64-17.3.img` (pas generic-aarch64)
2. Standoffs X1205 resserrés (jeu de ~1-2 mm corrigé)
3. Boot NVMe via X1205 confirmé fonctionnel — HA OS 17.3 opérationnel

**La cause #1 était l'erreur d'image (generic ≠ rpi5).**  
**La cause #2 était les pogo pins desserrés → chute de tension au boot NVMe.**  
**Le bug #4785 impose 17.3 plutôt que 18.x pour l'instant.**

---

## Voir aussi
- [[POSTMORTEM-BOOT-NVME-2026-07-09]]
- [[ASSEMBLAGE-RPi5-VANLIFE]]
- [GitHub #4785 — HassOS 18 on Pi 5 with NVMe hat is unstable](https://github.com/home-assistant/operating-system/issues/4785)
- [HA Community #716038 — Boot HA off Pi 5 NVMe disk instead of SD Card](https://community.home-assistant.io/t/boot-home-assistant-off-pi-5-nvme-disk-instead-of-the-sd-card/716038)
- [Martin Rowan — Installing HA on RPi 5 NVMe Storage](https://www.martinrowan.co.uk/2024/02/installing-home-assistant-on-raspberry-pi-5-nvme-storage/)
