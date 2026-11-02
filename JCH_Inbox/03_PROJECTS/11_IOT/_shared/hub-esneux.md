# Hub Esneux — Infrastructure partagée Serre + Maison

> RPi 5 + Home Assistant OS + UPS — cœur domotique de la propriété d'Esneux
> Partagé entre `iot-serre/` et `iot-maison/`
> Décision : **Option B — SSD + UPS** (extra solide)

---

## Architecture

```
┌──────────────────────────────────────┐
│  X1201-C1 Boîtier métal              │
│  ┌────────────────────────────────┐  │
│  │  X1001 NVMe HAT + SSD 128 Go   │  │ ← TOP (espace réservé)
│  │  M.2 2280 NVMe (PCIe Gen2 x1)  │  │
│  ├────────────────────────────────┤  │
│  │  RPi 5 (8 Go)                  │  │
│  ├────────────────────────────────┤  │
│  │  X1201 UPS (pogo pins)         │  │ ← BOTTOM (ultra-fin)
│  │  2× 18650 Li-Ion               │  │
│  │  I2C safe shutdown             │  │
│  │  Auto power-on                 │  │
│  └────────────────────────────────┘  │
│  + refroidisseur actif intégré       │
└──────────────────────────────────────┘
         ↕ Alim secteur 230V
    Coupure → X1201 shutdown propre
```

---

## BOM — Hub Esneux (~298 €)

| Composant | Référence | Prix est. | Statut |
|---|---|---|---|
| RPi 5 | Raspberry Pi 5 8 Go | ~188 € | À commander |
| UPS | Geekworm X1201 V1.1 (bottom, pogo pins) | ~25 € | À commander |
| NVMe HAT | Geekworm X1001 PCIe→M.2 (top, 2280) | ~15 € | À commander |
| SSD | M.2 NVMe 128 Go 2280 (WD Green ou Kingston NV2) | ~20 € | À commander |
| Boîtier | Geekworm X1201-C1 (métal, refroidisseur actif) | ~20 € | À commander |
| Alim | USB-C PD 5V 5A officielle RPi 5 | ~15 € | À commander |
| Accus | 2× 18650 Li-Ion 3500mAh (Samsung 35E) | ~15 € | À commander |
| **Total** | | **~298 €** | |

> Le X1201 se monte **en dessous** du RPi 5 (pogo pins, pas GPIO). Le X1001 se monte **au-dessus**. Le boîtier X1201-C1 a l'espace réservé pour les deux. Stack 100 % Geekworm, tout-en-un, zéro bricolage.

---

## Protections anti-corruption

| Couche | Protection |
|---|---|
| **Stockage** | SSD NVMe — pas de carte SD, 10× plus résistant aux coupures |
| **UPS** | X1201 → batterie 18650 → shutdown propre via I2C |
| **Filesystem** | OverlayFS read-only sur partition système HA OS |
| **Watchdog** | Hardware watchdog `/dev/watchdog` + systemd |
| **Backup** | Automatique config HA → Mac M1 via Tailscale |

---

## Stack logicielle

- **OS** : Home Assistant OS (bare metal sur RPi 5)
- **Zigbee** : ZHA ou Zigbee2MQTT via Sonoff ZBDongle-E
- **MQTT** : Mosquitto (broker local)
- **VPN** : Tailscale (accès distant)
- **Companion** : M1 Mac pour Frigate/Whisper (optionnel, activable plus tard)

---

## Capteurs partagés

Ces capteurs servent aux deux sous-projets :

| Capteur | Usage Serre | Usage Maison |
|---|---|---|
| Station météo Ecowitt | Pluie → skip arrosage, T° ext → ventilation | T° ext, pluie, vent → dashboard |
| Capteur T°/HR extérieur | Référence climatique | Confort, alerte gel |

---

## Dashboard

Un dashboard Home Assistant unifié :
- Vue « Serre » : humidité sol, arrosage, T°, ventilation, timelapse
- Vue « Maison » : T°/HR pièces, énergie, sécurité
- Vue « Météo » : station Ecowitt

---

*Décision Dobby 🦉 — 2026-06-22*
