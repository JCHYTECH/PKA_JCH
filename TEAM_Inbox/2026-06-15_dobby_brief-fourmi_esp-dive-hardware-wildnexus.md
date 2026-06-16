# Brief — Concordance ESP-DIVE × WildNexus : Analyse Hardware & Composants

**De :** [[Dobby]] 🦉
**Pour :** Fourmi 🐜 (#31)
**Date :** 2026-06-15
**Priorité :** HIGH
**Contexte :** Évaluation hardware du projet ESP-DIVE pour mutualisation avec WildNexus P0.

---

## Contexte

ESP-DIVE est un sous-marin RC ESP32 avec caméra FPV. Son BOM (~$125) et ses choix de composants présentent des chevauchements avec le BOM WildNexus P0 (caméra, stockage, power management, connectique).

## Composants ESP-DIVE à évaluer

### Électronique active
| Composant | Unité | Prix unit. | Intérêt WildNexus |
|-----------|-------|-----------|-------------------|
| XIAO ESP32-S3 Sense | 1 | $13.99-23.99 | ESP32-S3 + OV2640 intégré = dev kit idéal |
| DRV8833 motor driver | 1 | $1.40 | Pas nécessaire (pas de moteurs) |
| Boost Converter 3.7→5V | 1 | $0.70 | Pertinent pour régulation batterie |
| Wireless Charger Qi TX+RX | 1 | $11.86 | Innovation : charge sans ouvrir boîtier |
| N-MOSFET SI2300DS | 1 | $0.14 | Driver LED/contrôle power |
| P-MOSFET SI2301DS | 1 | $0.07 | Latching power switch |
| BC847B NPN transistors | 2 | $0.18 | Circuit power latching |

### Power
| Composant | Spécification |
|-----------|--------------|
| Batteries | 2× 500mAh 1S LiPo en parallèle (1000mAh total) |
| Charge | Récepteur Qi 5V 1A → boost → batterie |
| Protection | Reed switch magnétique (power on/off sans ouvrir) |
| Monitoring | Voltage divider + ADC, alerte 3.5V |

### Connectique & Stockage
| Composant | Usage |
|-----------|-------|
| microSD | 4-64GB, stockage MJPEG |
| JST PH-2.0 | Alimentation batterie |
| U.FL → SMA → coax 5m | Antenne WiFi (spécifique sous-marin) |
| DC-005 Power Jack | Charge filaire alternative |

### Waterproofing
| Technique | Usage |
|-----------|-------|
| O-rings 3.5mm | Étanchéité tube acrylique |
| Heat-shrink tube | Protection connexions |
| PVC tubing 3×6mm | Passage ballast |
| Epoxy | Scellement permanent |

## Questions pour Fourmi

1. **BOM overlap** — Parmi les composants ESP-DIVE, lesquels sont identiques ou substituables à ceux du BOM WildNexus v0.2c ? Y a-t-il des économies d'échelle (commande groupée) ?

2. **Power management** — Le circuit de latching power (MOSFETs + reed switch) et le boost converter 3.7→5V sont-ils adaptés au profil de conso WildNexus (deep sleep, réveil PIR, pic caméra) ? Le reed switch magnétique est-il une alternative crédible au switch physique pour l'IP67 ?

3. **Charge sans fil** — Évaluer la faisabilité d'intégrer un module Qi dans le boîtier WildNexus. Contraintes : distance (épaisseur boîtier), puissance (5W suffisant ?), compatibilité outdoor (humidité, température).

4. **Waterproofing** — Les techniques ESP-DIVE (submersion) sont-elles adaptables au besoin WildNexus (IP67, pluie/condensation) ? Les O-rings + tube acrylique sont-ils overkill ou au contraire une bonne base ?

5. **Connectique terrain** — Le système de connecteurs JST + heat-shrink est-il robuste pour du terrain longue durée ? Comparer avec les connecteurs étanches IP67 standard.

## Livrable attendu

Tableau comparatif BOM avec 3 colonnes : composant ESP-DIVE / équivalent WildNexus / recommandation (adopter / adapter / ignorer). Format dans `TEAM_Inbox/`.

## Références

- PDF source : `JCH_Inbox/00_INBOX/ESP-DIVE_ Build an ESP32 RC Submarine...pdf`
- BOM WildNexus v0.2c : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/` (dernière version)
- Registre achats : `docs/system/registre-achats.md`
