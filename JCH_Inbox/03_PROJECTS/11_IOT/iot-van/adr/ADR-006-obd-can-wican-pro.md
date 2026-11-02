# ADR-006 — Intégration données véhicule via OBD-II/CAN bus (WiCAN Pro)

**Date :** 2026-07-09
**Statut :** proposé
**Owner PKA :** [[Dobby]] (décision) / [[Forge]] (implémentation réseau) / [[Araignée]] (intégration HA)
**Jalon :** Phase 1 — Setup base

## Contexte

Le van est un Westfalia Kelsey 2026 sur porteur Ford Transit Custom 170CV 4x4 (« Lupo »). Le véhicule expose des données via son port OBD-II sur deux bus CAN :

- **HS-CAN** (500 kbps) — PCM 0x7E0 : vitesse, RPM, carburant, températures, turbo, DTC
- **MS-CAN** (125 kbps) — BCM 0x726 : état portes ×6, pression pneus ×6, batterie SOC/courant/tension

La BOM actuelle prévoit d'acheter des capteurs dédiés pour certaines de ces données (TPMS Bluetooth, BME280 extérieur). L'intégration CAN bus pourrait les remplacer gratuitement et enrichir les scénarios.

Contrainte forte : le CAN bus Ford s'endort après 30-60 min contact coupé. Les modules (PCM, BCM) cessent d'émettre. Le maintenir actif consommerait 200-500mA et viderait la batterie porteur en 4-5 jours.

## Décision

**Intégrer un WiCAN Pro (MeatPi, ~82€) sur le port OBD-II**, avec les caractéristiques suivantes :

- **MS-CAN obligatoire** — les données BCM (portes, pneus, batterie) sont sur le bus MS-CAN (pins OBD 3/11). Le WiCAN basic (38€) ne supporte pas le MS-CAN.
- **Sleep mode <1mA** en stationnement — pas de risque batterie
- **Periodic wake 5 min** — réveil programmé, poll BCM + PCM, push MQTT, re-sleep
- **PIDs Ford Transit prêts** — repo GitHub `WiCAN-Ford-Transit` avec 17+ PIDs déjà mappés
- **MQTT natif → HA** — firmware open source, dashboard prêt à l'emploi

**Les Aqara Zigbee (×9) sont conservés** pour la détection porte en temps réel en camping (CAN indisponible).

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| **WiCAN Pro (~82€)** | MS-CAN + HS-CAN ; PIDs Ford prêts ; sleep <1mA ; periodic wake ; MQTT natif ; firmware open source | Prix plus élevé que DIY ; dépendance firmware communautaire | **Retenu** |
| WiCAN basic (~38€) | HS-CAN fonctionnel ; MQTT ; pas cher | Pas de MS-CAN → pas de BCM (portes, pneus, batterie inaccessibles) | Écarté — MS-CAN critique |
| DIY ESP32 + SN65HVD230 (~15€) | Très bon marché ; ESP32 déjà en stock | MS-CAN hardware OK mais firmware à écrire ; reverse engineering complet des PIDs Ford ; pas de sleep mode natif ; effort disproportionné | Écarté — complexité |
| OBDLink MX+ (~130€) | Support MS/HS-CAN natif ; matériel pro fiable | 2× le prix du WiCAN Pro ; pas de PIDs Ford prêts ; pas de MQTT natif | Écarté — prix |
| Ne pas intégrer le CAN | 0€ ; pas de complexité | TPMS (20€) + BME280 (5€) à acheter ; perte de 6 scénarios (carburant, conso, DTC, turbo, Webasto, batterie) ; pas de redondance portes en roulage | Écarté — ratio coût/bénéfice |

## Conséquences

- ✅ 17+ entités HA exposées sans capteur physique : vitesse, RPM, carburant, conso, T°C moteur/air, turbo, DTC, portes ×6, pneus ×6, batterie
- ✅ TPMS Bluetooth supprimé de la BOM (-20€)
- ✅ BME280 extérieur supprimé de la BOM (-5€)
- ✅ GPS u-blox rétrogradé P2→P3 (vitesse via CAN, position seule conservée)
- ✅ 6 nouveaux scénarios : jauge carburant + range anxiety, conso réelle/trajet, DTC live, surveillance turbo, Webasto intelligent, alerte batterie porteur
- ✅ Redondance portes en roulage (CAN + Aqara = double confirmation)
- ⚠️ Delta net BOM : +57€ (WiCAN Pro 82€ - TPMS 20€ - BME280 5€)
- ⚠️ Cumulé avec DS300 Tap (-57€) : total optimisations = 0€ (neutre)
- ⚠️ Dépendance au repo communautaire `WiCAN-Ford-Transit` pour les PIDs — si le repo devient inactif, les PIDs restent documentés et reproductibles
- ⚠️ À valider sur véhicule réel : certains PIDs BCM marqués 🚧 dans le repo (en développement). Fallback : extraction via FORScan si nécessaire
- ⚠️ Commande à passer cette semaine (Crowd Supply ou Mouser Belgique) — délai ~2-3 semaines

## Critère de révision

Si plus de 3 PIDs BCM sont inaccessibles sur le Transit Custom 2026 après validation FORScan, réévaluer l'approche (fallback OBDLink MX+ ou abandon BCM et retour aux capteurs dédiés). Si le WiCAN Pro draine la batterie porteur > 5% par jour en mode stationnement, ajuster l'intervalle de periodic wake ou désactiver le wake et passer en mode roulage uniquement.
