# Brief — Concordance ESP-DIVE × WildNexus : Analyse Firmware & Architecture

**De :** [[Dobby]] 🦉
**Pour :** [[Araignée]] 🕷️ (#30)
**Date :** 2026-06-15
**Priorité :** HIGH
**Contexte :** Projet ESP-DIVE (sous-marin ESP32 FPV) identifié comme source de réutilisation pour WildNexus P0.

---

## Contexte

JCH a déposé dans l'[[inbox]] un PDF Instructables décrivant ESP-DIVE : un sous-marin RC basé sur XIAO ESP32-S3 Sense avec caméra OV2640, enregistrement MJPEG sur microSD, contrôle WiFi. L'analyse révèle des chevauchements majeurs avec WildNexus P0.

## Specs ESP-DIVE

| Composant | Détail |
|-----------|--------|
| MCU | XIAO ESP32-S3 Sense |
| Caméra | OV2640, 800×600 SVGA, ~20 FPS |
| WiFi | 2.4 GHz AP mode, U.FL → SMA → 5m coax → antenne surface |
| Stockage | microSD (MJPEG via s60sc/ESP32-CAM_MJPEG2SD) |
| Firmware | Arduino IDE, lib s60sc |
| PCB | 4-layer JLCPCB |
| Power | 2× 500mAh 1S LiPo parallèle, charge sans fil Qi, boost 5V |
| Détection | Motion detection intégrée dans la lib |
| Budget | ~$125 |

## Questions pour [[Araignée]]

1. **Librairie s60sc/ESP32-CAM_MJPEG2SD** — Évaluer la qualité du code, sa compatibilité avec l'ESP32-S3 standalone (pas XIAO), et sa réutilisabilité pour le test harness caméra WildNexus. Le repo est https://github.com/s60sc/ESP32-CAM_MJPEG2SD

2. **Architecture WiFi vs LoRa** — ESP-DIVE utilise WiFi AP + antenne coaxiale 5m vers la surface (pour l'eau). WildNexus P0 cible LoRa SX1262 pour la télémétrie. Est-ce que la couche WiFi (AP mode, web server, MJPEG streaming) est réutilisable pour la config terrain et le debug ? Faut-il une architecture dual WiFi+LoRa ?

3. **XIAO vs ESP32-S3 standalone** — Le XIAO Sense intègre caméra, SD, antenne. WildNexus utilise un ESP32-S3 nu + OV5640 externe. Quels sont les adaptateurs/bibliothèques nécessaires ? La pin mapping est-elle documentée ?

4. **PCB Design** — ESP-DIVE a un PCB 4-layer chez JLCPCB. La méthodologie (Gerber, BOM, assembly) est-elle réutilisable comme template pour le PCB WildNexus ?

5. **Charge sans fil** — Le système Qi de ESP-DIVE est-il pertinent pour WildNexus (recharge terrain sans ouvrir le boîtier IP67) ? Quelles contraintes ?

## Livrable attendu

Réponse en 3 sections : (a) ce qui est directement réutilisable, (b) ce qui est adaptable avec modifications, (c) ce qui n'est pas pertinent. Format : 1-2 pages dans `TEAM_Inbox/`.

## Références

- PDF source : `JCH_Inbox/00_INBOX/ESP-DIVE_ Build an ESP32 RC Submarine With FPV Camera...pdf`
- WildNexus P0 : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md`
- Architecture : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/01_FOUNDATION/MASTER_ARCHITECTURE_WN.md`
