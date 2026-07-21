# IOT / Domotique — Executive Summary

> Document externe — partenaires techniques, installateurs.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**Architecture domotique distribuée sur 3 sites (Belgique, Italie, van) — supervision unifiée, autonome, sans cloud.**

---

## Le concept

Une infrastructure domotique pensée pour un mode de vie multi-résidences :
- **Site 1 — Belgique (Esneux)** : serre connectée + maison
- **Site 2 — Italie (Trentin)** : résidence secondaire
- **Site 3 — Van** : Westfalia Kelsey 2026 (170CV, 4x4)

Chaque site est autonome (Home Assistant OS sur Raspberry Pi 5) et supervisé depuis un iPhone via Tailscale VPN. **Zéro cloud, zéro abonnement.**

---

## Architecture

```
[M5 Docker HA]          [RPi 5 HA OS Esneux]     [RPi 5 HA OS Van]
Belgique (base)         Serre + Maison            Véhicule nomade
     │                        │                         │
     └────────────────────────┼─────────────────────────┘
                              │
                    Supervision unifiée
                    iPhone via Tailscale
```

---

## Composants par site

### Serre Esneux
- Capteurs : température, humidité, luminosité (Aqara Zigbee)
- Actionneurs : électrovanne connectée (arrosage)
- Détecteur niveau liquide : ADS1115 + ESP32-C3 (DIY)
- BOM prêt : 247€, 5 phases de déploiement

### Van Westfalia Kelsey
- Hub : RPi 5 + SSD NVMe 256GB + PV PI HAT (solaire)
- Zigbee : capteurs température, alarme, frigo
- Autonome : offline-capable, synchronisation au retour
- Protection : boîtier métal Geekworm X1201-C1 + silentblocs + coating

---

## Statut

| Site | Statut |
|------|--------|
| HA M5 (base) | 🟢 Docker opérationnel, Zigbee OK |
| Serre Esneux | 🟡 BOM prêt, à assembler |
| Van | 🟡 Tout le hardware reçu, assemblage à lancer |
| Italie | ⚪ Planification |

---

## Budget

- **Dépensé** : ~300€ (RPi 5, Zigbee, capteurs, SSD, boîtiers)
- **PV PI HAT** : 150 AUD (~90€)
- **Reste à acquérir** : accus 18650 (UPS HAT)

---

*Document interne — infrastructure personnelle, pas de commercialisation prévue.*
