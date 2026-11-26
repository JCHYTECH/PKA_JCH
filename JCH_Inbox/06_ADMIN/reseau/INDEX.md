# Réseau — Inventaire des appareils actifs

> Photos de labels + infos (MAC, IP, série, rôle) des appareils actifs sur le réseau JCH (Esneux).
> Passerelle / DHCP : **192.168.128.1** — LAN `/23` (192.168.128.0/23).
> Règle : chaque nouvel appareil → photo du label + une ligne ici.

## Appareils

| Appareil | Rôle | MAC | IP | Série | Notes |
|----------|------|-----|----|-------|-------|
| Proximus B-box (Sagemcom Broadband) | Routeur / DHCP | `68:AB:A9:DD:DE:E0` (OCR, à confirmer) | 192.168.128.1 | `LK26029DP904075` (OCR, à confirmer) | 12V/2A · label : `proximus-box-sagemcom-label.jpeg` · admin via app MyProximus (web local fermé) |
| TP-Link RE450 | Répéteur Wi-Fi | `9e:da:c4:71:b6:79` | 192.168.129.5 | — | — |
| EPSON ET-8550 | Imprimante réseau | `D4:80:8B:A6:F1:C4` | 192.168.129.71 | — | mDNS `epsona6f1c4` · Wi-Fi canal 48 (5 GHz) · réservation DHCP à poser (IP .71) |
| TP-Link TL-SG605E | Switch Gigabit 5 ports (Easy Smart) | (à relever sur label) | (à relever) | — | Installé 25/11 derrière le RE450. **M1** `.78` (en8 1000baseT) + **RPi Home** `.57` (HA sur :80) + **RPi Lupo** `.27` (HA sur :8123) câblés |
| RPi 5 Lupo (HAOS `lupo`) | Serveur HA van · test au bureau | (à relever) | 192.168.129.27 | (série) | HA `:8123` · Tailscale `100.106.152.118` · SSH `:22` fermé |
| Box TV / Google Cast (`tvbox`) | Décodeur TV | `5C:22:DA:A3:28:1B` | 192.168.128.3 | — | Segment direct B-box · derrière le **CPL existant salon** |
| reMarkable 2.0 (tablette e-ink) | Tablette notes/lecture | `20:50:E7:03:F8:2E` | 192.168.129.79 | — | **SSH dropbear :22 ouvert** (WiFi + USB 10.11.99.1), user `root` · **OS 3.3.2.1666** (armv7l) · mDNS `remarkable.local` → 10.11.99.1 · détecté 25/11 |

## À faire

- [ ] **Refonte alim bureau** (25/11) : nettoyer le chaînage (2 prises, 1 disjoncteur 16 A) → plan + liste d'achat dans `reseau/bureau-refonte-alim.md`.
- [ ] **CPL bureau** (25/11) : topologie = B-box → CPL Base (mur) ⇒ CPL bureau sur **multiprise** → RE450. Instabilité = **CPL sur multiprise**. Fix : adaptateur **pass-through sur prise murale**. Réutiliser le **RE450 en mode AP** (uplink Ethernet CPL), pas en répéteur Wi-Fi. Vérifier le mode actuel du RE450.
- [ ] TL-SG605E : ✅ M1 + RPi Home + RPi Lupo câblés (25/11). Reste : relever **MAC/IP du switch** (management Easy Smart) pour compléter le tableau.
- [ ] Réserver l'IP de l'EPSON en DHCP — MAC `D4:80:8B:A6:F1:C4` → IP `.71`, via **app MyProximus** (web admin local fermé).
- [ ] Compléter la MAC de chaque appareil depuis son label.
- [ ] Noter les identifiants d'accès routeur (si utiles) — voir `JCH_PRIVATE/credentials-central.md`.
