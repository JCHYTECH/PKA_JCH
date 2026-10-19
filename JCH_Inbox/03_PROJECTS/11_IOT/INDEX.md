# IOT — Index projet

> Projet créé le 2026-06-06 par [[Dobby]] 🦉
> Réorganisé le 2026-06-22 — 3 sous-projets distincts

---

## Description

Projets IoT (Internet of Things) transverses de JCH : vanlife, serre, maison off-grid. Stack technique partagée : RPi 5, Home Assistant, Zigbee, Tailscale.

---

## Sous-projets

| Projet | Hub | Lieu | Statut |
|---|---|---|---|
| [`iot-van/`](iot-van/) | RPi 5 dédié (12V DC-DC) | Westfalia Kelsey 2026 | Prototype banc |
| [`iot-serre/`](iot-serre/) | RPi 5 partagé (secteur + UPS) | Esneux | Ébauche — BOM prêt |
| [`iot-maison/`](iot-maison/) | Même RPi que serre | Esneux | Ébauche long terme |

---

## Architecture globale

```
┌─────────────────────────────────────────────────────┐
│  Esneux — Hub RPi 5 (secteur + UPS)                 │
│  ┌──────────────┐  ┌──────────────────┐             │
│  │ iot-serre/   │  │ iot-maison/      │             │
│  │ Zigbee       │  │ Zigbee + LoRa    │             │
│  │ Capteurs     │  │ Capteurs pièces  │             │
│  │ Arrosage     │  │ Énergie Victron  │             │
│  └──────────────┘  └──────────────────┘             │
│         ↕ même HA, même Zigbee, même dashboard      │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│  Van — Hub RPi 5 (12V DC-DC + X1201 UPS)            │
│  ┌──────────────┐                                   │
│  │ iot-van/     │                                   │
│  │ Zigbee       │                                   │
│  │ Capteurs     │                                   │
│  │ Solaire      │                                   │
│  └──────────────┘                                   │
│         ↕ HA dédié, Tailscale                       │
└─────────────────────────────────────────────────────┘
```

---

## Structure du projet

```
11_IOT/
├── INDEX.md                          ← Ce fichier
├── executive-summary.md              ← Résumé exécutif
├── thread-iot.md                     ← Living document
├── iot-van/                          ← Projet vanlife Lupo 🐺
│   ├── BOM-VANLIFE.md                ← BOM maître
│   ├── scenarios-algorithmes-vanlife.md ← Scénarios & algorithmes
│   ├── ASSEMBLAGE-RPi5-VANLIFE.md    ← Guide assemblage hardware
│   ├── PROCEDURE-APPAIRAGE-ZIGBEE-2026-10-05.md ← Appairage capteurs Zigbee
│   ├── docs/                         ← Documentation générale
│   │   ├── stylevan-equinox4-cahier-technique-iot.md
│   │   ├── rpi-vanlife-guide-complet.md
│   │   ├── rpi-vanlife-mode-emploi.md
│   │   └── synthese-vanlife-iot.md
│   ├── briefs/                       ← Mandats, briefs, documents fondateurs
│   ├── rpi-config/                   ← Fichiers config OS RPi 5 (.txt)
│   ├── specs/                        ← Specs composants (INMP441, etc.)
│   ├── adr/                          ← Architecture Decision Records
│   ├── ds300-tap/                    ← Interface CBE DS300
│   ├── carplay/                      ← Intégration CarPlay
│   ├── archive/                      ← Documents obsolètes
│   ├── assets/                       ← Captures, images
│   └── 99_REFERENCES/                ← Références externes
├── iot-serre/                        ← Projet serre Esneux
├── iot-maison/                       ← Projet maison Esneux
├── _shared/                          ← Ressources partagées
│   ├── panier-amazon-van-serre.html  ← Panier groupé (v3)
│   ├── convergence-van-serre-capteurs.md
│   ├── hub-esneux.md
│   ├── detecteur-niveau-liquide/
│   └── procurement-register.md
├── PROTOCOLES/                       ← Protocoles de déploiement
└── 99_INBOX_NOTES/                   ← Notes brutes archivées
```

## Ressources partagées

| Fichier | Contenu |
|---|---|
| [`_shared/panier-amazon-van-serre.html`](_shared/panier-amazon-van-serre.html) | 🛒 Panier groupé Amazon (v4 : 33 articles, 282€) |
| [`_shared/convergence-van-serre-capteurs.md`](_shared/convergence-van-serre-capteurs.md) | Plan d'achat groupé van + serre (v4 : 257€, 27 items) |
| [`_shared/hub-esneux.md`](_shared/hub-esneux.md) | Infrastructure RPi 5 partagée serre + maison |
| [`iot-van/BOM-VANLIFE.md`](iot-van/BOM-VANLIFE.md) | 📋 BOM maître IoT Vanlife (tous sous-projets) |
| [`iot-van/ds300-tap/`](iot-van/ds300-tap/) | Interface passive ESP32 sur connecteur CBE DS300 |

---

## Inventaire RPi — Tous projets

| # | Projet | Modèle | Rôle | Alim | Statut |
|---|---|---|---|---|---|
| 1 | IOT Vanlife | RPi 5 4 Go | HA embarqué | DC-DC 12V + X1205 UPS + PV PI HAT | ✅ **Tout reçu** — voir [ASSEMBLAGE](iot-van/ASSEMBLAGE-RPi5-VANLIFE.md) |
| 2 | IOT Esneux | RPi 5 8 Go | HA serre + maison | Secteur + X1201 UPS | 📋 BOM ~298 € |
| 3 | NEXUS_ACOUSTIC | RPi 5 | BirdNET-Go 24/7 | Secteur + UPS | 📋 À planifier |
| 4 | WildNexus P1 | RPi 5 | Base Nexus | À définir | 🔮 Prototype futur |
| **Total** | | **4 RPi 5** | | | |

> Décision 2026-06-22 : séparés pour le moment. Fusion Esneux possible (HA + BirdNET sur le même Pi).

---

## Sous-systèmes partagés

- [`detecteur-niveau-liquide/`](_shared/detecteur-niveau-liquide/SPEC-DETECTEUR-NIVEAU-HYDROSTATIQUE.md) — Sonde hydrostatique TL-136 + ESP32 + ADS1115 (serre — van utilise DS300 Tap)
- [`iot-van/ds300-tap/`](iot-van/ds300-tap/SPEC-DS300-TAP.md) — Interface ESP32 sur connecteur CBE DS300 16 broches (vanlife)

## Stack transverse

- RPi 5 / ESP32-S3 / Home Assistant OS
- Zigbee (Sonoff ZBDongle-E) + LoRa (extérieur)
- Tailscale / WireGuard
- Capteurs : Aqara, Sonoff, Ecowitt
- Solaire : Victron VE.Direct/MQTT

---

## Spécialistes

- **Araignée 🕷️** — BOM serre, capteurs, ESPHome
- **Atlas 🗺️** — Template projet, documentation
- **Forge 🛡️** — Hardware, ADR-005 vanlife

---

*Généré par Dobby 🦉 — 2026-06-22*
