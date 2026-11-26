# Protocole Progress — WILDNEXUS P0 M-02

> **Fichier State** — lu avant toute affirmation sur l'avancement des protocoles.
> **Règle :** ne jamais déduire l'état d'un protocole d'un artefact, d'un code source ou d'un test hôte.
> **Dernière révision :** 2026-11-24 — SOP-01→05 (Phases A→E) re-validées au banc M5. Phase D/SOP-04 (22/11) et Phase E/SOP-05 (24/11) passées à `done`. Reprise P0 engineering (11/11) : SOP-16/17/18 créées, ADR-018 référencé, caveats sécurité SOP-08/09/13.
> **Statut :** repris — gates de reprise à lever avant montage (inventaire, factures, micros/PIR, matrice GPIO).

## 1. Lecture des statuts

- `done` : protocole exécuté sur le matériel indiqué, résultat consigné.
- `host done` : algorithme ou contrat testé sur ordinateur hôte uniquement.
- `pending` : exécution encore nécessaire.
- `blocked` : dépendance ou sécurité non résolue.

Les 37/37 tests hôte de juillet restent des résultats historiques à reproduire à la reprise si le code change. Ils ne valent ni validation ESP32-S3, ni intégration radio, ni preuve terrain.

## 2. Banc ESP32-S3 + PPK2 — phases A→E

| Phase | Description | Statut | Date | Résultat / prochaine preuve |
|-------|-------------|--------|------|------------------------------|
| A | ESP32 alive check (`wn_blink`) | done | 2026-06-16 | DevKit #1 fonctionnel ; re-validé 22/11 (ESP32-S3 QFN56 rev v0.2, MAC 58:e6:c5:74:7d:2c, flash 8 MB quad Micron, PSRAM 8 MB OPI) |
| B | Deep sleep 30 s | done | 2026-06-16 | Réveil observé ; re-validé 22/11 (4 réveils, intervalle 31,0 s) |
| C | Mesure deep sleep PPK2 | done | 2026-06-18 | 5 acquisitions ; ne représente pas le cycle produit complet. Re-validé 22/11 : 1061 µA médiane, pic boot 158 mA, cycle 30,0 s |
| D | Réveil court, 20 cycles | done | 2026-11-22 | 20/20 cycles (intervalle 17,5 s stable, zéro blocage) + 6/6 PPK2 (deep sleep 1062 µA, pic ~155 mA, actif ~2,55 s) — **GO** |
| E | Cycle simulé WildNexus | done | 2026-11-24 | Charge/evt 0.184 mAh, durée active 17.1 s, courant actif 38.7 mA (simulation delay, sans périphériques) |

## 3. SOP caméra, stockage, énergie et radio

| SOP | Description | Statut | Prochaine preuve / blocage |
|-----|-------------|--------|----------------------------|
| SOP-01 | ESP32 alive check | done | Phase A |
| SOP-02 | Deep sleep 30 s | done | Phase B |
| SOP-03 | PPK2 deep sleep | done | Phase C |
| SOP-04 | Wake short 20 cycles | done | Phase D — 20/20 cycles + 6/6 PPK2 (22/11) |
| SOP-05 | Simulation cycle événement | done | Phase E — charge/evt 0.184 mAh, deep sleep réf SOP-03 1062 µA (auto-ranging CLI non re-mesuré) |
| SOP-06 | microSD | pending | Carte 128 GB à confirmer ; écriture, relecture et coupures |
| SOP-07 | LoRa | blocked | Module non commandé au dernier état connu ; test avec gateway requis |
| SOP-08 | Caméra OV5640 | pending | Capture réelle, pinout et qualité jour/nuit |
| SOP-09 | PIR EKMB | pending | Relever la référence physique avant de figer les caractéristiques |
| SOP-10 | Batterie AA + buck | **blocked — suspendue** | Ne pas alimenter le pack tant que les gates ADR-005 et le schéma complet ne sont pas validés |
| SOP-11 | Benchmark Edge AI | blocked | SOP-08, dataset et modèles candidats ; benchmark sur ESP32-S3 |
| SOP-12 | Provisioning | pending | Configuration terrain réelle sans ordinateur portable |

SOP-10 ne doit plus être présentée comme un simple test en attente : l'ancienne séquence 6 AA et injection 3,3 V sur la broche 5 V a été retirée pour sécurité.

## 4. SOP audio

| SOP | Description | Statut | Preuve acquise / preuve restante |
|-----|-------------|--------|-----------------------------------|
| SOP-13 | Initialisation MEMS + capture stéréo | **blocked** | Vérifier la datasheet et l'interface des micros TDK reçus avant câblage ; code I2S seul insuffisant |
| SOP-14 | FFT 1024 + descripteurs | host done / hardware pending | Sinus 1 kHz, silence et bruit sur hôte ; refaire sur données et matériel du nœud |
| SOP-15 | WAV 3 s + sidecar JSON | host done / hardware pending | 11/11 tests hôte ; générer et relire les fichiers sur la SD du nœud |
| SOP-16 | Payload spectral 0x05 | host done / radio pending | 13/13 tests de codec hôte ; aucune transmission LoRa réelle |
| SOP-17 | Coexistence PIR + timer audio | pending | Routage testé sur hôte seulement ; concurrence matérielle et timing à mesurer |
| SOP-18 | Budget énergétique audio | pending | Mesures PPK2 des acquisitions, traitements, écritures et veilles ; aucune estimation ne vaut résultat |

## 5. Caméra et IA

| Test | Description | Statut | Prochaine preuve |
|------|-------------|--------|------------------|
| CAM-01 | Flash ESP32-CAM OV2640 via FT232RL | pending | Flash et capture sur le matériel reçu |
| CAM-02 | OV5640 DVP pinout + capture | pending | Images réelles et essais optiques |
| CAM-03 | Benchmark du modèle retenu | blocked | Dataset à constituer ; comparer les modèles puis mesurer précision, latence, RAM et énergie |

CAM-03 n'impose plus MobileNet-SSD. Le choix FOMO, MobileNet-SSD ou équivalent appartient au benchmark ADR-010. L'ancienne échéance du 15 juillet est supprimée.

## 6. Firmware intégré — tests hôte historiques

| Test | Description | Statut | Résultat consigné | Limite |
|------|-------------|--------|-------------------|--------|
| FW-01 | Structure `wildnexus-firmware` | done | ESP-IDF modulaire, commit a85f1a9 | Structure seulement |
| FW-02 | Codec ADR-014 caméra + spectral | host done | 13/13, commit a85f1a9 | Pas de preuve RF/gateway |
| FW-03 | Machine d'états double cycle | host done | 13/13, commit 131f6fb | Pas de concurrence matérielle mesurée |
| FW-04 | Module audio I2S/FFT/WAV | host done | 11/11 avec FW-05, commit 8c44793 | Capture I2S réelle non démontrée |
| FW-05 | Métadonnées audio JSON | host done | 11/11 avec FW-04, commit 8c44793 | Fichiers réels du nœud non validés |

| Suite hôte | Résultat historique |
|------------|--------------------:|
| Codec ADR-014 | 13/13 |
| State machine ADR-016 | 13/13 |
| Audio + métadonnées | 11/11 |
| **Total hôte** | **37/37** |

## 7. Chaîne d'alerte P0 — preuve spécifique WP05

| Étape | Statut | Critère de clôture |
|-------|--------|--------------------|
| Encodage nœud caméra/spectral | host done | Vecteurs de tests maintenus |
| Émission LoRa du nœud | blocked | Paquets observés avec paramètres et temps d'air documentés |
| Réception par la gateway | pending | Paquets réels reçus, erreurs et pertes journalisées |
| Décodage gateway | pending | Parser ADR-014 validé sur les deux types, CRC et compteurs compris |
| Journal local | pending | Événements rejouables et exportables, sans média transporté par LoRa |
| Downlink éventuel | pending | Commande reçue et exécutée sans dépasser les règles radio |

## 8. Dépendances critiques

```
Références micros/PIR → schéma et pinout → SOP-09/SOP-13
SOP-08 + dataset → SOP-11/CAM-03 → mesure énergie IA
SOP-13 → SOP-14/15 sur nœud → SOP-17/18
SOP-06 → clips/images réels sur SD → tests pipelines
Radio + gateway → SOP-07 → chaîne d'alerte complète
Gates ADR-005 → reprise SOP-10 → mesure du pack réel
Horodatage image↔audio (ADR-018 : NTP P0 / RTC DS3231 P1) → corrélation temporelle → terrain
Tous les cycles + radio + IA + pertes → WP03 → cible 60 jours
M-02 + ADR-018 + sécurité/RGPD/boîtier → EVT M-03
```

---

*Révision 2026-11-24 : SOP-01→05 (Phases A→E) re-validées au banc M5. Phase E/SOP-05 (24/11) : charge/evt 0.184 mAh, courant actif 38.7 mA, durée active 17.1 s ; deep sleep réf SOP-03 (1062 µA) — auto-ranging PPK2 CLI non fiable pour le sommeil (à re-mesurer via GUI nRF Connect si besoin).*
*Révision 2026-11-11 : reprise P0 engineering (JCH) ; SOP-16/17/18 créées ; ADR-018 référencé ; caveats sécurité SOP-08/09/13 ; statut gelé → repris.*
*Révision 2026-11-05 : statuts hôte/matériel séparés, SOP-10 suspendue, SOP-13 conditionnée aux micros réels, benchmark IA ouvert et preuve gateway ajoutée.*