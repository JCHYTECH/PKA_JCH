# Séquence de flash — HA OS 18.3 (RPi 5 Lupo)

> **Date :** 2026-10-01 | **Orchestré par :** Dobby 🦉
> **Machine :** toutes les commandes s'exécutent sur **[M5]** (Mac), sauf mention.
> **Image :** `haos_rpi5-64-18.3.img.xz` — dernière stable, inclut le fix #5005 (corruption NVMe).
> **SHA256 :** `e148a92595059d71c8bbf4c80d66fcb9166b647e10024641936316402863c60f`
> **Taille compressée :** 330 382 588 octets (~315 Mo)

---

## Pré-requis
- MicroSD **Samsung PRO Endurance 256GB** (ou 128GB en secours)
- Lecteur SD (interne M5 ou adaptateur USB)
- Espace libre pour l'image décompressée

---

## Étape 1 — Téléchargement [M5]

```bash
cd /tmp
curl -L -o haos_rpi5-64-18.3.img.xz \
  https://github.com/home-assistant/operating-system/releases/download/18.3/haos_rpi5-64-18.3.img.xz
```

## Étape 2 — Vérifier l'intégrité [M5]

```bash
echo "e148a92595059d71c8bbf4c80d66fcb9166b647e10024641936316402863c60f  haos_rpi5-64-18.3.img.xz" | shasum -a 256 -c -
```
Attendu : `haos_rpi5-64-18.3.img.xz: OK`

## Étape 3 — Décompresser [M5]

```bash
xz -d haos_rpi5-64-18.3.img.xz
```
Produit `haos_rpi5-64-18.3.img` (image brute, plusieurs Go).

## Étape 4 — Identifier la microSD [M5]

```bash
diskutil list
```
Repère la microSD (taille ~250 Go pour la Endurance). **Note le `/dev/diskN`.**

## Étape 5 — Flasher [M5]

⚠️ **Vérifie DEUX FOIS le numéro de disque** — flasher le mauvais disque efface des données.

```bash
# Démonter d'abord
diskutil unmountDisk /dev/diskN

# Flasher (remplacer diskN, ex: disk4)
sudo dd if=haos_rpi5-64-18.3.img of=/dev/rdiskN bs=4m
```

Alternative GUI (plus sûr) : **balenaEtcher** ou **Raspberry Pi Imager** → sélectionner l'image `.img` + la microSD → Flash.

## Étape 6 — Boot [RPi]

1. Retirer le NVMe du stack X1205 (si présent).
2. Insérer la microSD flashée dans le RPi 5.
3. Brancher l'alim USB-C officielle 27W.
4. Attendre ~5 min le premier boot.

---

## Rappel — contournement si coincé en 18.0–18.2

`nvme.sgl_threshold=0` (cmdline kernel). Inutile sur 18.3 (fix inclus).

---

*Fichier généré par Dobby 🦉 — à exécuter dans l'ordre, machine [M5].*
