# Forge 🛡️ — Analyse Hardware : Nœud Bioélectrique WN-BIO

**Date :** 2026-06-22
**Objet :** Réponse au brief Dobby — concept WN-BIO
**Document source :** `2026-06-22_concept-noeud-bioelectrique.md`

---

## 1. Réponses aux 5 questions

### Q1 — Faisabilité ADC 12-bit

L'ADC SAR 12-bit de l'ESP32-S3 a une résolution théorique de 0.8 mV par LSB sur une référence 3.3V (3300 mV / 4096). Après amplification ×100, un signal plante de 50 µV devient 5 mV → ~6 LSB. C'est **utilisable mais pas confortable**.

**Problème connu** : l'ADC de l'ESP32-S3 (comme tous les ESP32) a une non-linéarité marquée en dessous de ~100 mV et au-dessus de ~3.0V. La plage utile réelle est plutôt 150-2850 mV, soit ~9.5 bits effectifs.

**Verdict** : l'ADC intégré suffit pour du prototypage et de la détection de variations relatives (écart-type glissant). Pour des mesures absolues calibrées, un **ADS1115 16-bit I²C (~3 €)** serait préférable. Je recommande de démarrer avec l'ADC intégré et de prévoir le footprint ADS1115 en option sur le PCB.

**Note** : l'ESP32-S3 a DEUX ADC (ADC1, ADC2). ADC2 est partagé avec le Wi-Fi — à éviter. Utiliser ADC1 exclusivement.

---

### Q2 — Bruit de l'ampli

Le TLC2272 est un bon choix pour le prototypage (rail-to-rail, 9 nV/√Hz, faible offset). Mais pour une mesure différentielle plante→sol propre, un **ampli d'instrumentation (INA)** est plus adapté :

| Ampli | Bruit | CMRR | Coût | Verdict |
|---|---|---|---|---|
| TLC2272 | 9 nV/√Hz | 70 dB | ~2 € | OK proto, sensible au 50 Hz |
| INA828 | 7 nV/√Hz | 140 dB | ~5 € | Excellent, différentiel natif |
| AD620 | 9 nV/√Hz | 130 dB | ~4 € | Bon compromis prix/perf |

**Recommandation** : **AD620** pour le prototype. Le mode différentiel rejette le 50 Hz secteur, qui est le problème #1 en bioélectrique. Ajouter un filtre passe-bas RC 2ème ordre à ~30 Hz en sortie.

**Point bloquant** : sans blindage des câbles d'électrodes, le 50 Hz dominera le signal. Prévoir câble coaxial ou paire torsadée blindée. Coût additionnel ~1 €.

---

### Q3 — Budget énergétique

Estimation pour ESP32-S3 en mode échantillonnage continu + BLE advertising :

| Mode | Consommation |
|---|---|
| ADC continu + CPU Core 0 actif | ~25 mA |
| Core 1 + BLE advertising (100 ms interval) | ~15 mA |
| **Total actif** | **~40 mA @ 3.3V = 132 mW** |
| Deep sleep (pas d'échantillonnage) | ~10 µA |

Sur une 18650 3000 mAh : **~75 heures** en continu, **~3-4 jours** avec sleep cyclique 50%.

**Verdict** : viable pour station fixe (secteur/solaire). Trop gourmand pour satellite batterie autonome longue durée. Pour du terrain isolé, il faudrait :
- Échantillonnage par rafales (1 sec toutes les minutes)
- Ou déporter sur un MCU ultra-low-power (STM32U5) qui réveille l'ESP32-S3 uniquement pour la transmission

---

### Q4 — Intégration avec la caméra P0

Le Core 0 ne peut PAS gérer l'ADC continu ET la caméra simultanément. La capture caméra (DVP ou SPI) monopolise le CPU et le bus.

**Scénarios possibles :**

| Approche | Faisabilité | Impact P0 |
|---|---|---|
| ESP32-S3 dédié bio seul (satellite séparé) | ✅ Triviale | Ajout d'un nœud, pas de perturbation |
| ESP32-S3 partagé caméra+bio en temps partagé | ⚠️ Possible mais perte de données | Caméra prioritaire, bio en "best effort" |
| Satellite Smart STM32N6 + ESP32-S3 en coprocesseur bio | ✅ Élégant | Nécessite refonte satellite Smart |

**Recommandation** : nœud bioélectrique **dédié** séparé. Ne pas toucher au satellite P0 existant. Un ESP32-S3 seul + AD620 + électrodes dans son propre boîtier. Communication vers la base en BLE ou LoRa. Coût quasi identique, zéro risque sur P0.

---

### Q5 — Délai prototypage

| Étape | Durée estimée |
|---|---|
| Breadboard ESP32-S3 + AD620 + électrodes | 1-2 jours |
| Firmware échantillonnage ADC + BLE MIDI | 2-3 jours |
| Test sur plante réelle + visualisation données | 2-3 jours |
| **Total proto banc fonctionnel** | **1-2 semaines** |
| PCB prototype (optionnel) | +2 semaines (JLCPCB) |

Tous les composants sont disponibles chez Mouser/DigiKey en stock. Aucun délai d'approvisionnement bloquant.

---

## 2. Verdict global

**🟢 GO SOUS CONDITIONS**

Le concept est techniquement viable et peu risqué. Les conditions :

1. **Nœud dédié séparé** — ne pas intégrer au satellite P0 existant
2. **AD620** plutôt que TLC2272 pour le premier proto (rejet du 50 Hz)
3. **Câble blindé** pour les électrodes
4. **ADC intégré pour v1**, prévoir footprint ADS1115 pour v2
5. Ne pas viser l'autonomie batterie longue durée pour la v1 — commencer en station fixe

---

## 3. BOM estimatif — Proto banc WN-BIO v0.1

| Composant | Référence | Qté | Prix unit. | Total |
|---|---|---|---|---|
| MCU | ESP32-S3-DevKitC-1 | 1 | 8 € | 8 € |
| Ampli instrumentation | AD620ANZ | 1 | 4 € | 4 € |
| Électrodes | Tige acier inox ∅3mm × 100mm | 4 | 0.50 € | 2 € |
| Câble blindé | Coaxial RG174 1m | 2 | 1 € | 2 € |
| Résistances + condensateurs | Kit filtrage RC | 1 | 1 € | 1 € |
| Alimentation | Powerbank 5V USB-C | 1 | 5 € | 5 € |
| **TOTAL** | | | | **22 €** |

---

## 4. Risques techniques

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Signal noyé dans le 50 Hz | Élevée | Bloquant proto | AD620 différentiel + blindage + filtre 30 Hz |
| Variabilité entre plantes/électrodes | Moyenne | Résultats ininterprétables | Protocole de calibration standardisé |
| Dérive thermique de l'offset AD620 | Faible | Dérive lente des mesures | Compensation software (baseline glissante) |
| Oxydation électrodes acier inox | Moyenne | Dégradation signal sur 1-3 mois | Électrodes graphite ou Ag/AgCl pour version terrain |

---

## 5. Recommandation prochaine étape

1. **Commander les composants** (~22 €, 3 jours Mouser)
2. **Protocole de test** : une plante en pot (type Ficus ou Philodendron) + Arduino IDE + visualisation série
3. **Critère de succès** : détecter une variation de signal corrélée à l'arrosage (stress hydrique → réhydratation) en moins de 2 semaines

Si le proto banc est concluant → rédiger un ADR formel pour l'intégration P1.

---

*Analyse Forge 🛡️ — 2026-06-22*
