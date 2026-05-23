---
type: procedure
domain: birdnet
dateCreated: 2026-05-16
tags:
  - birdnet
  - raspberrypi
  - wifi
  - iphone
  - hotspot
---

[[birdnet]]

# BirdNET-Go – Gestion Wi‑Fi et hotspot iPhone

## Objectif

Configurer un Raspberry Pi utilisant BirdNET-Go afin de :

- fonctionner automatiquement sur le Wi‑Fi maison
- basculer sur le hotspot iPhone lorsqu’aucun Wi‑Fi fixe n’est disponible
- permettre une utilisation mobile sur le terrain

---

# 1. Vérifier le gestionnaire réseau

Ouvrir le Terminal du Raspberry Pi :

```bash
nmcli device status
```

Si `wlan0` apparaît, le Wi‑Fi est bien géré.

---

# 2. Activer le hotspot sur l’iPhone

Sur l’iPhone :

Réglages → Partage de connexion

Activer :

- Autoriser les autres utilisateurs

Noter :

- le nom du hotspot (SSID)
- le mot de passe

Exemple :

- SSID : iPhone-JCH
- Password : MacroPhoto2026

---

# 3. Connecter le Raspberry Pi au hotspot

Lister les réseaux :

```bash
nmcli dev wifi list
```

Connexion :

```bash
sudo nmcli dev wifi connect "iPhone-JCH" password "MacroPhoto2026"
```

Le réseau sera mémorisé automatiquement.

---

# 4. Vérifier les réseaux enregistrés

```bash
nmcli connection show
```

---

# 5. Définir les priorités réseau

Wi‑Fi maison prioritaire :

```bash
sudo nmcli connection modify "Maison-Wifi" connection.autoconnect-priority 10
```

Hotspot iPhone secondaire :

```bash
sudo nmcli connection modify "iPhone-JCH" connection.autoconnect-priority 5
```

---

# 6. Vérifier l’adresse IP

```bash
hostname -I
```

Exemple :

```text
172.20.10.2
```

Accès BirdNET-Go :

```text
http://172.20.10.2:8080
```

---

# 7. Installer Avahi pour raspberrypi.local

```bash
sudo apt install avahi-daemon
```

Ensuite :

```text
http://raspberrypi.local:8080
```

---

# 8. Vérifier BirdNET-Go

Docker :

```bash
docker ps
```

Ou service :

```bash
systemctl status birdnet-go
```

---

# 9. Configuration recommandée terrain

- Raspberry Pi 5
- BirdNET-Go sous Docker
- hotspot iPhone
- powerbank USB-C PD
- accès via Safari iPhone

---

# 10. Recommandation avancée

Installer :

- Tailscale
- ou Zerotier

Pour retrouver facilement le Raspberry Pi à distance.
