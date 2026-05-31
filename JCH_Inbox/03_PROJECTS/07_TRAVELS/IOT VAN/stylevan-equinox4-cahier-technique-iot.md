# Cahier Technique — Stylevan Equinox 4 × Home Assistant

> Document de synthèse enrichi. Base : conversation LLM du 2026-05-30. Enrichi par [[Dobby]] 🦉 avec les fichiers `07_TRAVELS/vanlife/` et les leçons WildNexus.
> Experts croisés : [[Forge]] 🦦 (intégration électrique), [[Chouette]] 🦉 (installation terrain), [[Renard]] 🦊 (garantie), [[Nova]] 🦋 (solaire)

**Véhicule :** Stylevan Origin Equinox 4 — Porteur Ford Transit Custom  
**Date :** 2026-05-30

---

## Table des matières

1. Architecture électrique d'origine (CBE DS300)
2. Intégration Raspberry Pi 5 + Home Assistant
3. Récupération des données solaires (Victron)
4. Écosystème Apple (CarPlay, HomeKit, Siri)
5. Capteurs & automatisations
6. Plan de déploiement par phases
7. Leçons terrain & risques

---

## 1. Architecture électrique d'origine (CBE DS300)

### Localisation

| Élément | Emplacement |
|---------|-------------|
| Boîtier CBE DS300 + disjoncteurs | Partie basse du meuble central (trappe technique avec grille d'aération) |
| Batterie cellule | Lithium LiFePO4 150 Ah, au sol centre véhicule |
| Batteries porteur | Sous les sièges avant (spécificité Ford Custom) |
| Relais couplage | Désactivé usine → charge gérée par REDARC DC/DC (alternateur intelligent Euro 6) |

### Carte des fusibles DS300

| Fusible | A | Circuit | IOT ? |
|---------|---|---------|--------|
| F1 | 20A | Éclairages LED cuisine/salon | ❌ |
| F2 | 20A | Spots liseuses lit arrière | ❌ |
| **F3** | **10A** | **Prises 12V + USB** | ✅ **Point de raccordement** |
| F4 | 10A | Chauffage / ECS Webasto | ❌ Critique |
| F5 | 10A | Pompe eau Shurflo | ❌ |
| F6 | 3A | Signal D+ (sécurités démarrage) | ❌ |
| F7 | 20A | Frigo compression Isotherm | ❌ Critique |
| F8 | 25A | Marchepied électrique | ❌ |

> **Avis [[Forge]] 🦦** : Repiquage sur F3 via porte-fusible dérivateur + fusible 5A dédié. Ne jamais repiquer sur F4 (chauffage) ni F7 (frigo) = sécurité alimentaire et médicale.

### Sondes de niveau CBE

| Cuve | Capacité | Sonde | Mesure |
|------|----------|-------|--------|
| Eau propre | 80 L | CBE tiges métalliques × 5 | Paliers 0/25/50/75/100% |
| Eaux usées | — | Vis inox × 2 | Plein/Vide |

> **Avis [[Renard]] 🦊** : En attente — analyse garantie si lecture parallèle sur bornier CBE. **Plan B** : capteurs ultrasons JSN-SR04T, zéro contact circuit.

---

## 2. Intégration Raspberry Pi 5 + Home Assistant

### Alimentation

| Règle | Détail |
|-------|--------|
| Proscrire | Convertisseur 230V → transfo Pi (double conversion, pertes) |
| Méthode | DC-DC 12V→5V, 5A/25W min, sortie USB-C |
| Raccordement + | Porte-fusible dérivateur sur **F3**, fusible 5A |
| Raccordement - | Goujon -B2 du DS300 (pas châssis : colles isolantes Ford) |
| Sécurité | UPS HAT avec batterie → shutdown propre |

> ⚠️ **Leçon WildNexus #1** : Pi 5 exige 5V/5A + câble USB-C PD e-mark. Sans cela : throttled=0x50000, reboots.

### Stockage

> ⚠️ **Leçon WildNexus #2** : Coupure secteur 30/05/2026 → microSD corrompue. SSD NVMe obligatoire.

---

## 3. Données solaires — Solution Victron

| Composant | Rôle | Connectique Pi |
|-----------|------|----------------|
| SmartSolar MPPT 75/15 ou 100/20 | Régulateur remplaçant PRS300/Antarion | VE.Direct → USB |
| SmartShunt 500A | Mesure flux batterie | VE.Direct → USB |

> **Avis [[Nova]] 🦋** : Les régulateurs CBE/Antarion sont des boîtes noires. Remplacer par Victron = seule solution fiable.

Budget : ~210€. Réversible (régulateurs d'origine remontables).

---

## 4. Écosystème Apple

- **CarPlay** : App Home Assistant Companion → icône sur Ford SYNC → actions rapides
- **iPad** : Dashboard mural sur Wi-Fi `VanLife_Network`
- **iPhone** : Contrôle distant via 4G + Tailscale
- **HomeKit Bridge** : QR code → app Maison → tout le van dans iOS → Siri (*"Dis Siri, température frigo ?"*)

---

## 5. Capteurs prévus

### Phase 1 — Base

| Capteur | Modèle | Emplacement | Qté | Prix |
|---------|--------|-------------|-----|------|
| T°/humidité | Sonoff SNZB-02D | Cellule | 1 | 5€ |
| Température | Sonoff SNZB-02D | Frigo | 1 | 5€ |
| Ouverture | Sonoff SNZB-04 | 5 portes (2 AV + 2 lat. + hayon) | 5 | 25€ |
| Clé USB Zigbee | Sonoff ZBDongle-E | Pi | 1 | 15€ |

> **Avis [[Chouette]] 🦉** : Adhésif 3M sur montants. Vérifier portée Zigbee hayon (~4m). Si faible → répéteur Sonoff S31 (~10€).

### Phases 2-3

| Capteur | Phase | Budget |
|---------|-------|--------|
| GPS u-blox 7/8 | 2 | 12€ |
| ESP32 + MPU6050 (inclinomètre) | 2 | 7€ |
| Jauges eau (CBE ou ultrasons) | 3 | 10-15€ |
| Victron solaire | 3 | ~210€ |

---

## 6. Plan de déploiement

### Phase 0 — Préparation (maintenant)
- Valider garantie avec [[Renard]] (brief 30/05)
- Commander Pi 5 + SSD + boîtier alu
- Commander convertisseur DC-DC USB-C PD 5A
- Commander clé Zigbee + capteurs
- Localiser physiquement DS300 et goujon -B2

### Phase 1 — Setup base (~1 week-end)
1. Pi 5 sur table → test alim secteur
2. Installer HA OS → Wi-Fi VanLife_Network
3. Appairer capteurs Zigbee → dashboard
4. HomeKit Bridge → Siri

### Phase 2 — Installation van (~1 jour)
1. Fixer Pi dans meuble central
2. Câbler alim sur F3 + masse -B2
3. Fixer 5 capteurs portes
4. Placer capteurs température
5. Test complet → iPad

### Phase 3 — Solaire & jauges (~1 week-end)
1. SmartSolar + SmartShunt
2. Données solaires dans HA
3. Jauges eau (CBE parallèle ou ultrasons)
4. Dashboard complet

---

## 7. Leçons & risques

| Risque | Impact | Mitigation | Source |
|--------|--------|------------|--------|
| Undervoltage Pi 5 | Critique | USB-C PD + câble 5A e-mark | WildNexus |
| Corruption stockage | Critique | SSD NVMe obligatoire | WildNexus |
| Conflit permissions DB | Bloquant | API REST, pas écriture directe | WildNexus |
| Garantie véhicule | Bloquant | Attente [[Renard]] | Brief 30/05 |
| Chaleur meuble | Dégradation Pi | Boîtier alu passif | — |
| Conso Pi 5 (~15W) | ~30 Ah/j sur 150 Ah | UPS shutdown si batterie < 20% | — |

---

## Références

- [[rpi-vanlife-guide-complet]] — Spécifications, schémas, budgets, YAML
- [[rpi-vanlife-mode-emploi]] — Mode d'emploi pas-à-pas (8 étapes)
- [[2026-05-28_retour-test-maison-rpi-birdnet-mobile]] — Leçons WildNexus alim/DB/GPS
- [[2026-05-30_dobby_brief-garantie-vanlife|Brief Renard — Garantie]] — En attente

---

*Document enrichi par [[Dobby]] 🦉 le 2026-05-30 — base LLM brute croisée avec 07_TRAVELS/vanlife/ et retours WildNexus.*
