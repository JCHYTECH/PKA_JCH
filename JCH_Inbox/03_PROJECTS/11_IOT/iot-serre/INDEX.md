# IOT Serre — Monitoring & Automatisation

> Projet extrait de `iot-home/` le 2026-06-22 par [[Dobby]]
> Hub partagé avec `iot-maison/` — RPi 5 + Home Assistant à Esneux

---

## Contexte

Serre de jardin 3m × 4m (12 m²) — Esneux, rue des Renards. Irrigation goutte-à-goutte sur récupération eau de pluie (Parkside). Fenêtres automatiques existantes.

---

## Architecture

```
[Capteurs serre] ←→ [Zigbee] ←→ [RPi 5 HA] ←→ [Dashboard]
                                         ↕ (même hub)
                                   [iot-maison/]
```

---

## Phases

| Phase | Composants | Budget | Statut |
|---|---|---|---|
| **1. Solaire** | Panneau + régulateur + batterie 12V | ~61 € | ⬜ |
| **2. Capteurs** | 2× humidité sol Zigbee, T°/HR Sonoff SNZB-02D, ultrason cuve JSN-SR04T, ESP32-CAM + ESP32 pont Zigbee | ~68 € | ⬜ |
| **3. Météo** | Ecowitt GW1100 + T/H/vent/pluie/pression | ~80 € | ⬜ |
| **4. Arrosage** | Électrovanne Parkside 12V, pompe eau pluie, goutteurs + filtre | ~30 € | ⬜ |
| **5. Ventilation** | Ventilateur axial 12V IP44 | ~20 € | ⬜ |
| **Total** | | **~247 €** | |

---

## Logique Home Assistant

1. 2 capteurs humidité sol → moyenne → si < SEUIL_SEC → arrosage
2. Si pluie détectée (station météo) → arrosage sauté
3. Si T° > SEUIL_CHAUD → ventilateur ON
4. Mode manuel dashboard

---

## Liens

- `_shared/hub-esneux.md` — Infrastructure partagée (RPi 5, Zigbee, réseau)
- `_shared/convergence-van-serre-capteurs.md` — Achats groupés avec van
- `iot-maison/` — Domotique maison (même hub)
- `iot-van/` — Domotique vanlife

---

*Généré par Dobby 🦉 — 2026-06-22*
