# Mandat — [[Atlas]] 🐘 : Document Projet Vanlife IOT × WildNexus

**De :** [[Dobby]] 🦉  
**À :** [[Atlas]] 🐘  
**Date :** 2026-05-30

---

## Contexte

JCH prépare l'intégration domotique de son Stylevan Equinox 4 avec RPi 5 + Home Assistant. En parallèle, WildNexus utilise déjà un RPi 5 + BirdNET-Pi + Tailscale. Les deux projets partagent composants, logiciels, contraintes et leçons. Cette convergence doit être documentée.

## Livrable

Fichier : `JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/projet-vanlife-iot.md`

### Sections obligatoires

1. Résumé exécutif
2. Objectifs & critères de succès (SMART)
3. Périmètre & hors-périmètre
4. Architecture système (schéma fonctionnel)
5. Budget consolidé par phase
6. Planning (3 phases, jalons)
7. **Matrice de convergence WildNexus × Vanlife**
8. Gouvernance
9. Risques & mitigations
10. Exit conditions

### Matrice de convergence — points à couvrir

| Dimension | WildNexus | Vanlife IOT | Convergence |
|-----------|-----------|-------------|-------------|
| **Compute** | RPi 5, 8 Go | RPi 4/5 | Même plateforme, mêmes contraintes alim |
| **Alimentation** | 8×AA lithium + buck TPS62840 | LiFePO4 150 Ah + DC-DC 12V→5V | Leçon undervoltage Pi 5 applicable aux deux |
| **Stockage** | microSD industrielle (P0) → SSD prévu | SSD NVMe obligatoire | Leçon corruption microSD → SSD |
| **Réseau** | Modem LTE MF833U1 + Tailscale | Wi-Fi AP + 4G + Tailscale | Même modem LTE, même stack Tailscale |
| **Capteurs** | PIR Panasonic EKMB, micro MEMS Knowles | Zigbee Sonoff (T°, portes), GPS u-blox | Architecture edge identique |
| **Logiciel** | BirdNET-Pi (analyse audio IA) | Home Assistant OS (domotique) | Même OS de base, même Imager |
| **Dashboard** | Interface web BirdNET (port 80) | Lovelace + Apple HomeKit | Consultation mobile via Tailscale |
| **Fournisseurs** | Mouser, DigiKey, Arducam | Amazon, AliExpress, Sonoff | Mouser/DigiKey pour critiques |
| **Leçons terrain** | Undervoltage, corruption SD, conflit SQLite, ports erronés | Mêmes risques identifiés | Directement transposables |

### Divergences à expliquer

- **Custom vs COTS** : WildNexus = composants nus ; Vanlife = capteurs grand public
- **Autonomie** : WildNexus = 2 µA PIR ; Vanlife = batterie 150 Ah
- **OS** : Raspberry Pi OS Lite vs Home Assistant OS — même Pi, deux usages

## Sources

| Source | Usage |
|--------|-------|
| `stylevan-equinox4-cahier-technique-iot.md` | Base technique van |
| `rpi-vanlife-guide-complet.md` | Spécifications capteurs, YAML, leçons |
| `rpi-vanlife-mode-emploi.md` | Procédure installation |
| `2026-05-28_retour-test-maison-rpi-birdnet-mobile.md` | Leçons terrain RPi 5 |
| `2026-05-30_Dobby_procurement_WILDNEXUS_update.md` | Procurement consolidé |
| `2026-05-30_dobby_brief-garantie-vanlife.md` | Analyse garantie (attente [[Renard]]) |

## Contraintes

- Style exécutif — lisible en 10 minutes
- ~8-12 pages
- Markdown + wikilinks [[Obsidian]]
- Délai : 1 semaine
