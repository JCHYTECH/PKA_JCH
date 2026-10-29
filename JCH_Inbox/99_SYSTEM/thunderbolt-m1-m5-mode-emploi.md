---
title: Thunderbolt Bridge M1 ↔ M5 — Mode d'emploi
date: 2026-06-05
tags: [réseau, thunderbolt, M1, M5, setup]
---

# Thunderbolt Bridge M1 ↔ M5

Réseau point-à-point 40 Gb/s entre MacBook M1 (écran cassé) et MacBook M5.  
Débit mesuré : **~400 MB/s** via SMB.

## Prérequis

- Câble Thunderbolt 4 branché sur un **port Thunderbolt** des deux Macs (port gauche sur M1, port 2 sur M5 — icône ⚡)
- M1 allumé et éveillé (appuyer sur le bouton Touch ID si endormi)
- Clavier/souris externe sur M1 si couvercle fermé (sinon veille clamshell)

## Machines

| Machine | Rôle | IP Thunderbolt | User SSH |
|---------|------|---------------|----------|
| MacBook M5 (macOS Tahoe 26.4) | Principal | `10.0.0.1` | — |
| MacBook M1 (`MBP-de-M1`) | Secondaire | `10.0.0.2` | `m1` |

## Étape 1 — Configurer M5

Le service Thunderbolt Bridge s'appelle **`ok brudge `** (avec espace final) dans networksetup.

```bash
# [M5]
networksetup -setmanual "ok brudge " 10.0.0.1 255.255.255.0
```

Vérification :
```bash
# [M5]
networksetup -getinfo "ok brudge "
# → IP address: 10.0.0.1
```

## Étape 2 — Accéder au M1 (écran cassé)

### Via Screen Sharing (port 5900)
```bash
# [M5]
open vnc://192.168.129.14
```
Le M1 est à `192.168.129.14` sur le WiFi local (hostname : `mac`).

### Naviguer sans Dock
- Touche **Windows + Espace** → Spotlight → taper **Réglages système**

## Étape 3 — Configurer M1

**[M1 via Screen Sharing]**  
Réglages système → Réseau → **Thunderbolt Bridge** → Détails… → TCP/IP

- Configurer IPv4 : **Manuellement**
- Adresse IP : `10.0.0.2`
- Masque : `255.255.255.0`
- Routeur : vide

→ OK → Appliquer

> Si erreur "un autre périphérique utilise cette adresse" : revérifier M5 avec `ifconfig bridge0 | grep inet` et relancer l'étape 1.

## Étape 4 — Vérifier le lien

```bash
# [M5]
system_profiler SPThunderboltDataType | grep -A2 "Status:"
# → Status: Device connected / Speed: 40 Gb/s
```

Le ping peut être bloqué par le pare-feu M1 — utiliser ARP :
```bash
# [M5]
arp -n 10.0.0.2
# → 10.0.0.2 at 36:18:de:3e:b3:c0 on bridge0
```

## Étape 5 — Monter le disque M1 en écriture

```bash
# [M5]
open "smb://m1:5443@10.0.0.2/Macintosh HD"
```

Le volume apparaît dans `/Volumes/Macintosh HD-1` avec accès en écriture.

## Étape 6 — SSH via Thunderbolt

```bash
# [M5]
ssh m1@10.0.0.2
# mot de passe : 5443
```

Débit SSH/rsync : ~280 MB/s (limité par chiffrement CPU).  
Débit SMB : ~400 MB/s (recommandé pour gros transferts).

## Dépannage

| Symptôme | Cause | Solution |
|----------|-------|----------|
| `status: inactive` sur bridge0 | Câble non reconnu | Vérifier port Thunderbolt (pas USB-C simple), rebrancher |
| M1 non détecté dans `system_profiler` | M1 endormi | Appuyer Touch ID, ou brancher clavier externe |
| Ping timeout | Pare-feu M1 | Normal — utiliser ARP ou SSH pour tester |
| "Un autre périphérique utilise l'IP" | bridge0 M5 a drifté | Relancer `networksetup -setmanual "ok brudge " 10.0.0.1 255.255.255.0` |
| SMB read-only | Monté sans credentials | Remonter avec `smb://m1:5443@10.0.0.2/Macintosh HD` |
| SSH "Connection closed" | Mauvais username | Username M1 = `m1` (minuscule) |

## Backup automatique PKA_JCH → M1

Script : `scripts/backup_pka_m1.sh`  
Fréquence : toutes les 4h via launchd (`com.pka.backup-m1`)  
Log : `_local/backup_pka_m1.log`  
Si M1 non joignable : backup ignoré silencieusement.

```bash
# [M5] forcer un backup immédiat
launchctl start com.pka.backup-m1

# [M5] désactiver
launchctl unload ~/Library/LaunchAgents/com.pka.backup-m1.plist

# [M5] réactiver
launchctl load ~/Library/LaunchAgents/com.pka.backup-m1.plist
```

## Voir aussi

- [[Dobby]] — orchestrateur sessions PKA
- [[Forge]] — intégrations systèmes
