# Thread — IOT / Domotique

> Living document — mis à jour automatiquement par Dobby 🦉 en fin de session.
> **Dernière mise à jour** : 2026-07-11 — RPi 5 Lupo stabilisé SD boot, double instance résolue, NVMe en attente adaptateur USB
> **Statut** : 🔴 P0 — deadline 7 août 2026 (arrivée Lupo)

---

## Vue d'ensemble

Architecture domotique distribuée : HA Docker M5 + HA OS RPi 5 Esneux (serre + maison) + HA OS RPi 5 van (Westfalia Kelsey 2026 « Lupo »). Supervision unifiée iPhone via Tailscale. Focus P0 actuel : Lupo vanlife, deadline 7 août.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🔴 P0 | Lupo = priorité absolue jusqu'au 7 août |
| Vanlife — RPi | 🟢 | RPi 5 assemblé (SD 128 Go HA OS 17.3, hostname `lupo`), Healthy, boot fiable. Docker M5 coexiste sans conflit. |
| Vanlife — NVMe | ⚫ | NVMe Fanxiang 256 Go retiré physiquement. Décision : SD seule (pas de SSD). Adaptateur USB-NVMe non nécessaire. |
| Vanlife — Alim | 🔶 | Alim directe USB-C RPi (X1205 pogo pins insuffisants pour boot NVMe). X1205 conservé pour UPS (accus 18650). |
| Vanlife — Boîtier | ⏳ | X1201-C1 non monté (accès facile pour debug). À fermer avant le 7 août. |
| Vanlife — Capteurs | ⏳ | WiCAN Pro à commander (~82€), capteurs Zigbee (portes, frigo) à sélectionner. |
| Vanlife — CAN bus | 🟢 | Spéc complet : WiCAN Pro (HS-CAN + MS-CAN), 17+ entités HA, scénarios définis. |
| Serre Esneux | ⚪ | Gelé jusqu'à septembre (post-van). BOM 247€ prêt. |
| HA M5 | 🟢 | Docker opérationnel, Zigbee OK, `homeassistant` hostname. |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-07-11 | SD boot retenu pour Lupo | NVMe boot intermittent (pogo pins X1205 insuffisants), SD 128 Go fiable. Plan C de SOLUTION-BOOT-NVME. |
| 2026-07-11 | Hostname `lupo` + `ha supervisor repair` | Résout duplicate_os_installation entre RPi et Docker M5 |
| 2026-07-10 | UGREEN USB-NVMe Enclosure commandé | Pour wiper NVMe depuis M5, puis Move Data Disk |
| 2026-07-09 | WiCAN Pro retenu | OBD/CAN Ford Transit, ~82€, MS-CAN + HS-CAN, 17+ entités HA |
| 2026-07-09 | HA OS 17.3 obligatoire | Bug GitHub #4785 : 18.x + NVMe instable sur RPi 5 |
| 2026-06-13 | Architecture IoT distribuée — 3 HA locaux | Belgique (M5), Italie (RPi 5), Van (RPi 5) autonomes |

---

## Prochaine étape

**Action** : Swap SD 128 Go → Samsung PRO Endurance 256 Go (clone + extend partition)
**Deadline** : Session en cours (17 juillet)
**Responsable** : JC + Dobby

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-07-11 | RPi Lupo stabilisé : SD boot HA OS 17.3, hostname `lupo`, Healthy. Double instance HA résolue (ha supervisor repair). NVMe déconnecté, adaptateur USB commandé. | `MEMORY.md` §2026-07-10/11 |
| 2026-07-09 | Boot NVMe résolu (2 causes : image generic ≠ rpi5 + standoffs X1205). OBD/CAN analysé, WiCAN Pro retenu. Mouser reçu. | `TEAM_Inbox/2026-07-09_dobby_traitement-inbox-yolo.md` |
| 2026-07-08 | RPi 5 assemblé (SSD + UPS HAT + accus 18650). Tentative boot NVMe = échec. | — |
| 2026-07-03 | PV PI HAT reçu, SSD NVMe reçu. Thread file créé. | — |
| 2026-06-30 | RPi 5 + SSD + boîtiers Geekworm reçus (29/06). Van Westfalia Kelsey commandé. | — |

---

## Liens

- Hardware : `hardware-state.md` (section STATION-DOMO / IoT)
- Boot NVMe : `iot-van/SOLUTION-BOOT-NVME-2026-07-09.md`
- Assemblage : `iot-van/ASSEMBLAGE-RPi5-VANLIFE.md`
- CAN bus : `iot-van/specs/SPEC-CAN-BUS.md`
- Procurement : `11_IOT/_shared/procurement-register.md`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*