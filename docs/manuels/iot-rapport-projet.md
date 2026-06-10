# 🚐 IoT Van & Maison — Rapport projet pour responsable

**Date :** 2026-06-09  
**Rédigé par :** [[Dobby]] 🦉 (PKA Orchestrator)  
**Propriétaire du projet :** Jean-Claude Havaux (JCH)

---

## 1. Qu'est-ce que le projet IoT ?

Deux sous-projets IoT qui partagent la même pile technique :

### 🚐 IoT Van
Équiper le **Stylevan Equinox 4** (Ford Transit Custom) d'un système domotique embarqué :
- **RPi 5 + Home Assistant** (cerveau du van)
- **Capteurs Zigbee** : température cellule, température frigo, ouverture 5 portes
- **GPS** : position, itinéraire, géolocalisation
- **Solaire Victron** : panneaux 280W, MPPT, batterie LiFePO₄ 150Ah
- **Dashboard** : iPad (Wi-Fi van) + iPhone (4G/Tailscale) + Siri (HomeKit)
- **Alarme** : capteurs portes, PIR extérieur

### 🏠 IoT Maison (off-grid)
Domotique de la maison autonome en Italie/Trentin :
- Capteurs environnementaux (température, humidité, qualité air)
- Gestion énergie (solaire, batterie)
- Structure similaire, mais pas encore démarrée (dossier `iot-home/` à créer)

---

## 2. Où en est le projet ?

**Statut :** Phase 0 — En attente validation garantie  
**Prochaine étape :** Commander le matériel et assembler le setup de base

### Phases

| Phase | Contenu | Budget | Statut |
|-------|---------|--------|--------|
| **Phase 0 — Préparation** | Validation juridique garantie van, commande matériel | ~5€ (câbles, connecteurs) | 🟡 **Bloqué** — attente [[Renard]] (garantie) |
| **Phase 1 — Setup base** | Flash SSD HA OS, Wi-Fi van, appairage Zigbee, dashboard Lovelace, HomeKit + Siri, test stabilité 24h | ~246 € | 🔴 À venir |
| **Phase 2 — Installation van** | Fixation Pi, câblage alim + 12V, pose 5 capteurs portes + 2 températures, tests complets | ~56 € | 🔴 À venir |
| **Phase 3 — Solaire & jauges** | SmartSolar MPPT, SmartShunt, données solaires, jauges eau, dashboard énergie complet | ~225 € | 🔴 À venir |
| **Total** | | **~600 €** | |

---

## 3. Architecture technique

```
Capteurs Zigbee ─┐
Capteurs portes ─┼── Sonoff ZBDongle-E ── RPi 5 8Go ── iPad (dashboard local)
GPS u-blox 7 ────┘                 │            ├── iPhone (4G + Tailscale)
Solaire Victron ───── MPPT 100/20 ─┘            └── Ford SYNC (CarPlay)
                                                      
Alimentation : LiFePO₄ 150Ah → F3 DS300 → DC-DC 12V→5V PD 5A
```

### Composants clés Phase 1 (déjà validés)

| Composant | Modèle | Prix |
|-----------|--------|------|
| Raspberry Pi 5 8 Go | RPi5-8GB | ~80 € |
| Boîtier alu passif | Flirc RPi 5 | ~15 € |
| SSD NVMe 128 Go | Samsung/WD | ~20 € |
| Adaptateur NVMe | Pimoroni NVMe Base | ~25 € |
| Convertisseur DC 12V→5V USB-C PD 5A | DFRobot DFR1017 | ~10 € |
| Clé Zigbee | Sonoff ZBDongle-E | ~20 € |
| Capteurs température | Sonoff SNZB-02 ×2 | ~16 € |
| Capteurs ouverture porte | Aqara MCCGQ11LM ×5 | ~40 € |
| **Total Phase 1** | | **~246 €** |

### Phase 2 — extensions
- GPS u-blox 7 (12 €)
- ESP32 + MPU6050 inclinomètre (10 €)
- Module relais 12V (5 €)
- PIR extérieur IP65 (12 €)
- Spot LED extérieur 12V (5 €)

### Phase 3 — solaire
- Victron SmartSolar MPPT 100/20 (~140 €)
- Victron SmartShunt 500A (~75 €)

---

## 4. Convergence avec WildNexus

Les deux projets partagent la même infrastructure réseau et les mêmes leçons terrain :

| Ressource | WildNexus | IoT Van | Mutualisation |
|-----------|-----------|---------|--------------|
| RPi 5 | Cerveau de la base locale | Cerveau du van | Achats groupés |
| Modem LTE | MF833U1 | MF833U1 | Même modèle |
| VPN | Tailscale | Tailscale | Même tailnet |
| Leçons terrain | Undervoltage, corruption SD | Mêmes risques | Capitalisées |
| Stockage | microSD industrielle | SSD NVMe | Éviter corruption |

**Différence majeure :** WildNexus tourne sous RPi OS Lite (Linux), IoT Van tourne sous HA OS (Buildroot optimisé domotique).

---

## 5. Équipe

| Rôle | Agent PKA | Responsabilité |
|------|-----------|----------------|
| Orchestrateur | [[Dobby]] 🦉 | Pilotage, coordination |
| Intégration électrique | [[Forge]] 🦦 | Câblage, alim, BOM |
| Installation terrain | [[Chouette]] 🦉 | Montage van, fixation |
| Garantie & conformité | [[Renard]] 🦊 | Analyse juridique garantie |
| Solaire | [[Nova]] 🦋 | Dimensionnement Victron |
| IoT transverse | [[Araignée]] 🕷️ | Architecture IoT globale |
| Rédaction docs | [[Atlas]] 🐘 | Guides, modes d'emploi |

---

## 6. Blocages actuels

| Blocage | Impact | Solution |
|---------|--------|----------|
| 🔴 **Garantie van non validée** | Aucun achat ni câblage possible | [[Renard]] 🦊 analyse juridique — brief envoyé le 30/05 |
| 🔴 Pas de spécialiste IoT maison | IoT Home non démarré | Mandat [[Furet]] en cours pour recrutement |
| 🟡 IoT Home dossier vide | Aucun document | Créer structure après recrutement |

---

## 7. Budget consolidé

| Phase | Budget |
|-------|--------|
| Phase 0 — Outillage diagnostic (testeur FNB58) | ~35 € |
| Phase 1 — Setup base (RPi, SSD, capteurs, alim) | ~246 € |
| Phase 2 — GPS, inclinomètre, relais, PIR | ~56 € |
| Phase 3 — Victron solaire + jauges eau | ~225 € |
| Marge imprévus | ~40 € |
| **Total** | **~600 €** |

---

## 8. En résumé

```
Phase 0 (garantie)   →   Phase 1 (base)   →   Phase 2 (van)   →   Phase 3 (solaire)
🟡 bloqué                🔴 prêt à lancer    🔴 prêt à lancer    🔴 prêt à lancer
```

Le projet IoT Van est bien documenté, budgété, planifié — mais **bloqué sur la validation juridique de la garantie du constructeur**. Une fois levé, le matériel peut être commandé et assemblé en 4 week-ends (~600 €).

---
