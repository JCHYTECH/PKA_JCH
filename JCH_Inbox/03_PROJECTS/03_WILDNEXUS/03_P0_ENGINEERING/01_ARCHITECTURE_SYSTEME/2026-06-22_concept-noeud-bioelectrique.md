# Concept : Nœud Bioélectrique WildNexus (WN-BIO)

**Date :** 2026-06-22
**Statut :** CONCEPT v1.0 — validé Forge 🛡️ (GO sous conditions)
**Phase cible :** P1 (post-P0, nœud dédié séparé — zéro impact P0)
**Origine :** Note Apple Notes ESP32-S3 du 2026-06-22 — analyse croisée Dobby
**Fiche parente :** WildNexus Hardware Architecture Study (2026-05-22)
**Avis Forge :** [`TEAM_Inbox/2026-06-22_forge_analyse-noeud-bioelectrique.md`](../../../../TEAM_Inbox/2026-06-22_forge_analyse-noeud-bioelectrique.md)

---

## 1. Résumé exécutif

Ajouter un **nœud bioélectrique dédié** à la constellation WildNexus. Un ESP32-S3 + ampli d'instrumentation AD620 capte les micro-fluctuations électriques des plantes et du sol — une modalité de données écologiques **absente** de tous les projets DIY concurrents (BirdWeather, AudioMoth, FieldKit).

**Verdict Forge : 🟢 GO SOUS CONDITIONS** — techniquement viable, ~22 € de proto banc, 1-2 semaines de développement.

---

## 2. Concept technique (v1.0 — révisé Forge)

### 2.1 Architecture

```
[Électrodes acier ∅3mm] → [Câble coaxial blindé RG174] → [AD620 (gain ×100)] → [Filtre RC 30Hz] → [ADC1 ESP32-S3] → [Core 0 : échantillonnage] → [Core 1 : BLE MIDI / LoRa]
```

### 2.2 Choix hardware (validés Forge)

| Étage | Choix initial (Dobby) | Choix révisé (Forge) | Raison |
|---|---|---|---|
| Ampli | TLC2272 | **AD620** | Rejet du 50 Hz secteur (CMRR 130 dB vs 70 dB) |
| ADC | Intégré 12-bit | Intégré v1, **footprint ADS1115** en réserve | ~9.5 bits effectifs suffisent pour variations relatives |
| Câblage | Non spécifié | **Coaxial blindé RG174** | Sinon 50 Hz domine le signal |
| Intégration P0 | Satellite partagé | **Nœud dédié séparé** | Zéro risque sur P0, communication BLE/LoRa vers la base |

### 2.3 BOM — Proto banc v0.1

| Composant | Référence | Qté | Prix unit. | Total |
|---|---|---|---|---|
| MCU | ESP32-S3-DevKitC-1 | 1 | 8 € | 8 € |
| Ampli instrumentation | AD620ANZ | 1 | 4 € | 4 € |
| Électrodes | Tige acier inox ∅3mm × 100mm | 4 | 0.50 € | 2 € |
| Câble blindé | Coaxial RG174 1m | 2 | 1 € | 2 € |
| Filtrage passif | Kit R+C (passe-bas 30 Hz) | 1 | 1 € | 1 € |
| Alimentation | Powerbank 5V USB-C | 1 | 5 € | 5 € |
| **TOTAL** | | | | **22 €** |

### 2.4 Budget énergétique

| Mode | Conso | Autonomie 18650 3000mAh |
|---|---|---|
| Continu (ADC + BLE) | ~40 mA | ~75 h |
| Sleep cyclique 50% | ~20 mA | ~6 jours |
| Rafales (1s/min) | ~2 mA moy. | ~60 jours |

⚠️ Pour station fixe (secteur/solaire) uniquement en v1. Terrain isolé → MCU ultra-low-power (STM32U5) en v2.

---

## 3. Protocole BLE MIDI (télémétrie)

| Octet | Champ | Valeurs |
|---|---|---|
| 1 | Type + Canal | 0x90 = Note On (événement capteur) |
| 2 | ID Capteur | 0-127 (plante A, plante B, sol, etc.) |
| 3 | Amplitude | 0-127 (signal normalisé) |

Bibliothèques ESP32-BLE-MIDI existantes. 3 octets/événement. Portée 10-100 m.

---

## 4. Applications écologiques

### 4.1 Stress hydrique végétal
Potentiels d'action électriques corrélés au stress hydrique. Détection **avant** symptômes visuels.

### 4.2 Rythmes circadiens
Cycles électriques jour/nuit des plantes → corrélation lumière/température/humidité.

### 4.3 Impédance du sol
Humidité par résistance entre électrodes — un seul circuit, deux mesures.

### 4.4 Détection de passage animal
Pic électrique au frôlement → « détecteur de passage » sans caméra, sans PIR.

---

## 5. Positionnement vs concurrence

| Projet | Caméra | Audio | Env. | Bioélectrique |
|---|---|---|---|---|
| BirdWeather | ❌ | ✅ | ❌ | ❌ |
| AudioMoth | ❌ | ✅ | ❌ | ❌ |
| FieldKit | ❌ | ❌ | ✅ | ❌ |
| **WildNexus P0** | ✅ | ❌ | ✅ | ❌ |
| **WildNexus + WN-BIO** | ✅ | ✅ (P1) | ✅ | ✅ |

---

## 6. Risques et mitigations

| Risque | Probabilité | Impact | Mitigation |
|---|---|---|---|
| Signal noyé dans le 50 Hz | Élevée | Bloquant proto | AD620 différentiel + blindage + filtre 30 Hz |
| Variabilité inter-plantes | Moyenne | Résultats ininterprétables | Protocole calibration standardisé |
| Dérive thermique AD620 | Faible | Dérive lente | Compensation software (baseline glissante) |
| Oxydation électrodes | Moyenne | Dégradation 1-3 mois | Graphite ou Ag/AgCl pour v2 terrain |

---

## 7. Prochaines étapes

- [x] Avis Forge — GO sous conditions (2026-06-22)
- [ ] Commande composants (~22 € Mouser, 3 jours)
- [ ] Proto breadboard : ESP32-S3 + AD620 + électrodes sur plante en pot
- [ ] Critère succès : détecter variation signal corrélée à l'arrosage (< 2 semaines)
- [ ] Si concluant → ADR formel + intégration registre capteurs WildNexus P1

---

*Généré par Dobby 🦉 — validé Forge 🛡️ — 2026-06-22*
