# IOT / Domotique — Executive Summary (v2)

> Document externe (partenaires techniques, installateurs). **Version 2.0 — 2026-10-29**, alignée sur l'état réel (thread 2026-10-22). Remplace la v1.0 (2026-07-03).
> Référence interne détaillée : `IOT_DOSSIER_TECHNIQUE_V0.md` (la bible).
> **Infrastructure personnelle — pas de commercialisation.**

## En une phrase

**Architecture domotique distribuée et autonome sur plusieurs nœuds (base Belgique, serre/maison Esneux, van Lupo, Italie), supervisée depuis un iPhone via Tailscale — zéro cloud, zéro abonnement.**

## Les nœuds

| Nœud | Rôle | État |
|---|---|---|
| **M5 Docker** (Belgique) | Base / dev Home Assistant | 🟢 opérationnel |
| **RPi 5 Esneux** | Serre + Maison | 🟡 hub à assembler, serre gelée (post-van) |
| **RPi 5 Van Lupo** | Véhicule nomade (Westfalia Kelsey 2026) | 🔴 **P0 — deadline 15/12/2026** |
| **RPi 5 Italie** | Résidence secondaire | ⚪ planifié |

Chaque nœud est autonome (Home Assistant OS), supervisé à distance via Tailscale.

## Van Lupo (priorité P0)

- **Hub** : RPi 5 4 Go, **SD 256 Go** (HAOS 18.3, boot stabilisé). NVMe abandonné (cause : pogo pins UPS < 5 A).
- **Alimentation** : passage **X1205 → Geekworm X1200** (5,1 V/5 A) — corrige les under-voltages. En attendant : alim USB-C directe.
- **Connectivité** : routeur **RUT240 (4G)** → internet van ; **WiCAN Pro** (OBD/CAN) installé → 17+ entités (vitesse, conso, portes, pneus, batterie…).
- **Capteurs** : Zigbee2MQTT (Sonoff ZBDongle-E) ; reste ~7 capteurs (~88 €) à commander.
- **RAM** : DS300 Tap (lecture tableau CBE) ; assiette déléguée à l'iPhone.

## Serein sur les coûts (honnête)

- **Van** : ~1 026 € (BOM historique) — **reste réel court terme ≈ 150 €** (capteurs + X1200). Le BOM 2026-07 est partiellement périmé (alim/stockage), en cours de resynchronisation.
- **Hub Esneux** : ~298 €.

## Points de vigilance (revue experts internes)

1. Config ESPHome `ds300-tap` à corriger (conflit GPIO) avant flash.
2. Convertisseur DC-DC **USB-C PD 5 A** à ajouter (exigé par l'ADR-001, absent du BOM).
3. UPS **X1200** à valider sur datasheet avant achat.
4. Canal Zigbee à décaler hors des canaux Wi-Fi 1/6/11.

## Stack

Home Assistant OS · RPi 5 · Zigbee (Z2M/ZHA) · MQTT (Mosquitto) · Tailscale · ESPHome · Victron (P3) · CAN/OBD (WiCAN Pro).

---

*Résumé externe aligné. Détail + revue experts : `IOT_DOSSIER_TECHNIQUE_V0.md`. Source opérationnelle : `thread-iot.md`.*
