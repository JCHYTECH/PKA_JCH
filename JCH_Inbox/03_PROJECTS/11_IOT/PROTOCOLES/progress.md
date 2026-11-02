# Protocole Progress — IOT

> **Fichier State** — lu par Dobby avant toute affirmation sur l'avancement des protocoles.
> **Règle :** ne jamais déduire l'état d'un protocole d'artefacts. Ce fichier est la source unique.
> **Dernière mise à jour :** 2026-06-23 — Capteurs luminosité + orage recherchés

---

## Protocole : IoT Van — Phases

| Phase | Description | Statut | Date | Résultat | Notes |
|-------|-------------|--------|------|----------|-------|
| 1 | Prototype banc RPi 5 + 12V DC-DC | ⏳ pending | — | — | RPi 5 reçu, PV PI commandé (livraison août) |
| 2 | Configuration HA autonome | ⏳ pending | — | — | |
| 3 | Intégration Zigbee (Sonoff) | ⏳ pending | — | — | ZBDongle-E + SNZB-02DR2 reçus |
| 4 | Configuration Tailscale | ⏳ pending | — | — | |
| 5 | Test offline (alarme, frigo) | ⏳ pending | — | — | |

## Protocole : IoT Serre — Phases

| Phase | Description | Statut | Date | Résultat | Notes |
|-------|-------------|--------|------|----------|-------|
| 1 | Déploiement RPi 5 Esneux | ⏳ pending | — | — | BOM 247€ prêt, 5 phases |
| 2 | Capteurs serre (T°/H/sol) | ⏳ pending | — | — | Aqara T1 luminosité reçu, SHT31×2 dispo (Mouser) |
| 3 | HA dashboard serre | ⏳ pending | — | — | |
| 4 | Automatisation arrosage | ⏳ pending | — | — | Sonoff Smart Water Valve reçu |
| 5 | Monitoring long terme | ⏳ pending | — | — | |

---

## Capteurs — Recommandations d'achat

### Luminosité (équivalent nu Aqara T1)
| Capteur | Module | Prix | Interface | Notes |
|---------|--------|------|-----------|-------|
| **BH1750FVI** | GY-302 | ~2€ | I2C (3.3V) | Standard IoT chinois, 1-65535 lux, même puce que l'Aqara T1 |
| VEML7700-TR | VEML7700 | ~5€ | I2C (3.3V) | 0-120k lux, meilleur en basse lumière (aube/crépuscule) |

→ **Recommandé : GY-302 (BH1750)** — compatible ESP32, bibliothèque standard, ~2€

### Détecteur d'orage
| Capteur | Module | Prix | Interface | Notes |
|---------|--------|------|-----------|-------|
| **AS3935** | CJMCU-3935 | ~22€ | SPI ou I2C (3.3-5.5V) | Détection foudre jusqu'à 40 km, précision ~1 km, ESPHome natif |
| AS3935 | SparkFun SEN-15441 | ~30€ | SPI | Version US, documentation complète |

→ **Recommandé : CJMCU-3935 (AS3935)** — supporté par ESPHome, détecte approche et distance de l'orage

---

*Format standard PKA — créé le 2026-06-23, mis à jour avec capteurs luminosité + orage.*
