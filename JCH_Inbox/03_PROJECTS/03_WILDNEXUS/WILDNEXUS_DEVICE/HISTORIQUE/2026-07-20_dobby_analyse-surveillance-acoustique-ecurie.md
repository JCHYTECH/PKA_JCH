# Note de démarrage — Surveillance acoustique d'écurie par IA

> Dobby 🦉 — DeepSeek V4 — 2026-07-20
> Analyse INBOX : « Alors on va discuter d'un projet destiné à déterminer les événements… »
> Projet : **Écurie Connectée** (nom temporaire — à définir avec les partenaires)

---

## 1. Résumé exécutif

Ce document est une synthèse préliminaire destinée à être décortiquée et discutée avec nos partenaires scientifiques et techniques. Il pose les bases d'un système de surveillance acoustique d'écurie capable de classifier automatiquement les sons ambiants (chevaux, intrusions, feu, nuisibles) et de déclencher des alertes.

**Conclusion clé : le projet est techniquement faisable avec les briques PKA existantes (WildNexus + InsectNet/NEXUS_ACOUSTIC). Un projet jumeau académique (Savonia, Finlande) valide l'approche.**

---

## 2. Périmètre fonctionnel

### 2.1 Sons à classifier

| Catégorie | Événements | Priorité |
|-----------|-----------|----------|
| **Chevaux — normaux** | Mange, boit, marche, se couche, gratte le sol | 🟢 Baseline |
| **Chevaux — vigilance** | Hennit, tape mur/porte, chamaillerie, stéréotypies (tic à l'appui) | 🟡 Monitoring |
| **Chevaux — urgence** | Cheval coincé/coincé au box, détresse, coup violent | 🔴 Alarme |
| **Intrusions animales** | Oiseaux, rongeurs (rats/souris), chauves-souris | 🟡 Monitoring |
| **Intrusions humaines** | Pas, voix, portes (hors heures normales) | 🔴 Alarme |
| **Incendie** | Crépitement, alarme feu existante, fumée (combinaison capteurs) | 🔴🔴 Critique |
| **Ambiants extérieurs** | Vent, pluie, orage, circulation | ⚪ Filtrer |

### 2.2 Architecture fonctionnelle

```
Capteurs audio (mics) → Edge AI (ESP32/RPi) → Classification locale → Alerte (push/SMS/sirène)
                                                        ↓
                                              Stockage SD local + Cloud (audit)
```

---

## 3. Briques techniques existantes (PKA)

### 3.1 WildNexus — Module satellite audio (P0 Engineering)

Le hardware et firmware audio de WildNexus est directement réutilisable :

| Composant | Spécification | Fichier source |
|-----------|--------------|----------------|
| **Micros** | 2× Knowles SPH0645LM4H-B, I2S digital MEMS | `SOP-13-i2s-mems-stereo.md` |
| **Fréquence** | 16 kHz, 16-bit, stéréo | idem |
| **MCU** | ESP32-S3 DevKit | `wn_config.h` (pinout I2S: BCLK=15, WS=16, DIN0=7, DIN1=6) |
| **Capture** | Clips WAV 3s, buffer 192000 bytes | `SOP-15-clip-wav-json.md` |
| **Stockage** | microSD 128GB (SPI: CS=39, SCK=40, MISO=41, MOSI=42) | idem |
| **FFT** | 1024 points, Hann window, 10 descripteurs spectraux | `SOP-14-fft-features.md` |
| **Métadonnées** | Sidecar JSON (schema v1.0) | `SOP-15-clip-wav-json.md` |
| **Autonomie** | Deep sleep 30s entre captures | Toutes les SOPs |
| **Enclosure** | NEMA 4X outdoor (boîtier étanche) | `02_HARDWARE_SATELLITE/` |
| **Connectivité** | LoRa, WiFi, LTE (en développement) | `04_CONNECTIVITE_MESH_LORA_LTE/` |
| **Firmware** | Testé sur host (gcc) + ESP32-S3 | `firmware/main/modules/wn_audio.c` |

> **Statut WildNexus :** SOP-13 (I2S) → SOP-14 (FFT) → SOP-15 (WAV+JSON) validées sur banc. Module audio fonctionnel, prêt pour itération suivante.

### 3.2 InsectNet / NEXUS_ACOUSTIC — Pipeline de classification audio

| Composant | Spécification | Source |
|-----------|--------------|--------|
| **Modèle** | CNN 4 couches Conv2D, 330K paramètres, F1 macro 0.98 (5 espèces) | `04_MODELS/baseline-results.md` |
| **Entrée** | Mel-spectrogrammes, segments 3s | `scripts/pipeline/` |
| **Preprocessing** | Filtrage par fréquence, segmentation QC automatique | `01_SCOPE/insectnet-v0.1-scope.md` |
| **Export** | ONNX (edge deployable → TFLite pour ESP32) | Pipeline documenté |
| **Dataset** | InsectSet459 (26K fichiers, 459 espèces) — protocole d'annotation réplicable | `INSECTNET/` |
| **Pipeline** | xcapi → segmentation → spectrogrammes → QC → entraînement | 13 scripts Python |
| **API** | REST/MQTT documentés dans fiches produit WildNexus | Fiches produit WN |
| **Dashboard** | HTML interactif (visualisation des résultats) | Fiches produit WN |

> **Statut InsectNet :** V0.1 validée. Migration M5→M1 en attente (accès rsync). Pipeline prêt pour transfert méthodologique.

---

## 4. Recherche web — État de l'art

### 4.1 Projet jumeau : Savonia University (Finlande) 🔥

Le projet **« Tekoälyä talleille »** (AI pour écuries) de Savonia UAS est quasiment identique au projet décrit par JC :

- **Approche hybride** : autoencoder (détection d'anomalies) + classifier supervisé (PANNs/CNN14)
- **Feature extraction** : PANNs CNN14 pré-entraîné sur AudioSet → embeddings 2048-dim
- **Classifieur** : 3 couches denses + dropout (~1M paramètres)
- **Fenêtrage** : clips 2 secondes
- **Anomaly detection** : autoencoder entraîné sur sons normaux → erreur de reconstruction élevée = anomalie
- **Stratégie** : labelisation initiale large → autoencoder détecte les anomalies → annotation humaine → fine-tuning du classifieur
- **Conclusion Savonia** : « *The expected outcome is a reliable and scalable AI-driven model to work as a backend for our stable alert app.* »

**URL** : https://www.savonia.fi/en/articles-pro/monitoring-stable-soundscapes-ai-model-selection-and-development-plans/

> 🎯 **Recommandation :** Contacter l'équipe Savonia (Johannes Geisler, Aki Happonen) pour un échange technique. Leur approche est exactement celle qu'on devrait suivre.

### 4.2 Autres références pertinentes

| Référence | Pertinence | Lien |
|-----------|-----------|------|
| **Animal Sound Classification (ArXiv 2407.03440)** | MFCC + Bi-LSTM + attention, benchmark dataset animaux | arxiv.org/abs/2407.03440 |
| **ML in Acoustics (Nature 2025)** | Review complète des techniques ML pour classification audio | nature.com/articles/s44384-025-00021-w |
| **Horse behaviour DL (Taylor & Francis 2026)** | Classification comportementale équine par deep learning | tandfonline.com/doi/full/10.1080/01652176.2026.2665442 |
| **Nordic Thingy:53 + Edge Impulse (bioRxiv 2025)** | Validation plateforme Edge AI pour comportement équin (accéléromètre) | biorxiv.org/content/10.64898/2025.12.05.692598v1 |
| **Fire detection barns (NFPA 150)** | Normes détection incendie écuries — complément audio → fumée/chaleur | uspasecurity.com/fire-protection-guide-for-horse-barns-nfpa-150/ |

---

## 5. Feuille de route proposée

### Phase 0 — Pré-projet (2 semaines)

| Action | Responsable | Livrable |
|--------|-------------|----------|
| Contacter Savonia (Johannes Geisler) pour échange technique | JC | Compte-rendu réunion |
| Valider le scope avec partenaires vétérinaires/équestres | JC + experts métier | Liste priorisée des événements |
| Étude de faisabilité : adapter firmware WildNexus pour streaming continu | Forge | Spec technique |

### Phase 1 — Dataset et protocole (1 mois)

| Action | Responsable | Livrable |
|--------|-------------|----------|
| Définir protocole d'enregistrement (placement micros, durée, fréquence) | Clio + Araignée | Document protocole |
| Enregistrer 10h+ de sons d'écurie (normal + événements simulés) | JC + partenaires | Dataset brut |
| Annotation initiale (experts équestres) — large labelling | JC + vétérinaires | Dataset annoté v0.1 |
| Installer module WildNexus audio dans écurie pilote | Araignée | Déploiement terrain |

### Phase 2 — Modèle AI (1-2 mois)

| Action | Responsable | Livrable |
|--------|-------------|----------|
| Autoencoder : entraînement sur sons normaux → détection anomalies | Musaraigne + Clio | Modèle anomaly detection |
| Classifieur : fine-tuner CNN InsectNet sur dataset écurie | Clio | Modèle classification v0.1 |
| Export ONNX → TFLite pour ESP32-S3 | Musaraigne | Modèle edge deployable |
| Intégration pipeline streaming (remplacer capture 3s périodique par continu) | Forge | Firmware v2 |

### Phase 3 — Pilote (1 mois)

| Action | Responsable | Livrable |
|--------|-------------|----------|
| Déploiement 2-3 modules dans écurie pilote | Araignée | Installation terrain |
| Dashboard monitoring + alertes (push/SMS) | Chouette + Forge | Interface opérateur |
| Validation avec experts (vétérinaires, soigneurs) | JC + partenaires | Rapport validation |
| Itération sur faux positifs/négatifs | Clio + Musaraigne | Modèle v0.2 |

---

## 6. Analyse de risques

| Risque | Probabilité | Impact | Mitigation |
|--------|------------|--------|------------|
| **Dataset insuffisant** — pas assez d'événements rares (feu, intrusion) | Élevée | Critique | Approche autoencoder (Savonia) : détecte l'anormal sans l'avoir vu. Simuler événements. |
| **Bruit ambiant** — environnement agricole bruyant | Élevée | Moyen | Micros directionnels, filtrage DSP, plusieurs positions |
| **Faux positifs** — alertes intempestives = rejet utilisateur | Moyenne | Élevé | Phase pilote avec seuils conservateurs, interface de feedback |
| **Autonomie énergétique** — pas de prise dans l'écurie | Faible | Moyen | WildNexus P0 déjà en deep sleep. Batterie Li-Ion 18650 + panneau solaire optionnel. |
| **Acceptation** — réticence des propriétaires | Moyenne | Élevé | Co-design avec utilisateurs finaux dès Phase 0. |

---

## 7. Impact cross-projet PKA

- 🔴 **WILDNEXUS** — Majeur. Extension directe du module audio satellite vers un nouveau domaine applicatif. Valide la plateforme.
- 🔴 **NEXUS_ACOUSTIC** — Majeur. Nouvelle classe de sons (mammifères domestiques), enrichit le pipeline.
- 🟡 **InsectNet** — Élevé. Transfert méthodologique : pipeline classification audio, CNN, QC automatique.
- 🟡 **IOT** — Élevé. Nouveau cas d'usage IoT van → IoT bâtiment agricole.
- 🟢 **VETALYX** — Modéré. Convergence potentielle avec la télémédecine vétérinaire équine.
- ⚪ **ARTEON/WildLens** — Léger. Contenu éditorial potentiel (innovation agritech).

---

## 8. Prochaines actions immédiates

1. **JC** : Contacter Savonia (johannes.geisler@savonia.fi) pour un échange — ils ont 6 mois d'avance sur le même sujet.
2. **JC** : Identifier une écurie pilote partenaire.
3. **Dobby** : Créer un dossier projet `13_ECURIE_CONNECTEE` et un thread file.
4. **Forge** : Estimer l'effort d'adaptation firmware WildNexus (streaming continu vs. capture 3s).
5. **Clio** : Étudier PANNs/CNN14 (AudioSet) vs. CNN InsectNet pour la classification.

---

*Document préparatoire — ne constitue pas un engagement projet. Destiné à alimenter la discussion avec les partenaires.*
