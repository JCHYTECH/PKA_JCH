# Évaluation BioDCASE Task 3 2026 — TinyML pour Bioacoustique

> **Date :** 2026-06-23  
> **Auteur :** Araignée 🕷️ — Hardware & Systems Specialist  
> **Destinataires :** Dobby 🦉, Musaraigne 🐭, Forge 🔨, Clio 🐬  
> **Référence :** Brief Dobby `2026-06-23_dobby_analyse-birdnet-ecosysteme_integration-pka.md` (action n°6)

---

## Résumé exécutif

**⚠️ BioDCASE Task 3 2026 (TinyML pour bioacoustique) n'existe PAS en tant que challenge formalisé.** La recherche exhaustive (web, DCASE community, GitHub) n'a trouvé aucune trace de cette tâche. Ce qui existe réellement :

1. **BioDCASE Workshop 2026** — atelier satellite en ligne (date TBD) co-localisé avec DCASE 2026 Workshop (28-29 oct, Boston). Accepte des papiers de recherche. **Abstract deadline : 5 juillet 2026.**
2. **DCASE 2026 Challenge** — 7 tâches, deadline passée (15 juin 2026). Aucune tâche TinyML bioacoustique.
3. **DCASE 2024 Task 5 « Few-shot Bioacoustic Event Detection »** — dernière édition bioacoustique, discontinuée en 2025-2026.

**Recommandation : NO-GO pour une participation « challenge » (inexistant). GO conditionnel pour une soumission papier au BioDCASE Workshop 2026 + veille DCASE 2027.**

---

## 1. Analyse de l'existant : BioDCASE

### 1.1 Qu'est-ce que BioDCASE ?

BioDCASE est un **atelier satellite** (workshop) du DCASE Workshop, dédié à la bioacoustique computationnelle :

| Édition | Format | Date | Lieu |
|---------|--------|------|------|
| BioDCASE 2025 | Présentiel | 29 octobre 2025 | Barcelone (UPF) |
| BioDCASE 2026 | **En ligne** | TBD (octobre 2026) | Virtuel, co-localisé DCASE Boston |

**Source :** `dcase.community/workshop2026/` — « DCASE Workshop 2026 will be co-located with the BioDCASE Workshop (online workshop, date TBD), which focuses on Bio-acoustics. »

### 1.2 BioDCASE n'est PAS un challenge avec des tâches

Contrairement au challenge DCASE principal (qui a 7 tâches avec datasets, baseline, métriques et classement), BioDCASE est un **workshop académique** : soumission de papiers, présentations orales/poster, pas de classement compétitif.

**La mention « BioDCASE Task 3 » dans le brief Dobby est probablement une confusion avec :**
- Les anciennes tâches DCASE (Task 5 « Few-shot Bioacoustic Event Detection » en 2022-2024)
- Une anticipation non confirmée d'un challenge bioacoustique 2026

---

## 2. DCASE 2026 Challenge — État des lieux

### 2.1 Les 7 tâches officielles (deadline : 15 juin 2026 — CLOS)

| Task | Nom | Pertinence WILDNEXUS |
|------|-----|---------------------|
| T1 | Heterogeneous Audio Classification | ❌ Freesound, pas bioacoustique |
| T2 | Anomalous Sound Detection (machines) | ❌ Industriel |
| T3 | Semantic Acoustic Imaging (SELD) | ❌ Audio spatial, 4-canaux |
| T4 | Spatial Semantic Segmentation (S5) | ❌ Immersive audio |
| T5 | Audio-Dependent Question Answering | ❌ LALMs, QA |
| T6 | Audio Moment Retrieval | ❌ Retrieval text→audio |
| T7 | Domain-Agnostic Incremental Learning | ⚠️ Potentiel si données bioacoustiques |

**Aucune tâche TinyML spécifique en 2026.** La task historiquement « low-complexity » (ASC with device information) était T1 en 2025, mais a été remplacée en 2026 par « Heterogeneous Audio Classification » sans contrainte de complexité.

### 2.2 Calendrier DCASE 2026 (passé)

| Date | Événement |
|------|-----------|
| 1 février 2026 | Descriptions des tâches publiées |
| 1 avril 2026 | Lancement du challenge |
| 1 juin 2026 | Release des datasets d'évaluation |
| **15 juin 2026** | **Deadline soumissions (PASSÉE)** |
| 30 juin 2026 | Résultats publiés |

---

## 3. Historique : DCASE Few-shot Bioacoustic Event Detection

La seule tâche bioacoustique de l'histoire DCASE :

| Édition | Task | F-score meilleur système | Baseline |
|---------|------|--------------------------|----------|
| DCASE 2022 | Task 5 | ~55% (estimation) | Template matching |
| DCASE 2023 | Task 5 | ~60% (estimation) | Prototypical networks |
| **DCASE 2024** | **Task 5** | **65.2%** (XF_NUDT, logmel+U-Net) | Prototypical 41.6% |

### 3.1 Caractéristiques DCASE 2024 Task 5

| Paramètre | Valeur |
|-----------|--------|
| **Type** | Few-shot sound event detection (5-shot) |
| **Classes** | Mammifères + oiseaux (multi-espèces par dataset) |
| **Dataset dev** | 4.8 GB, 8 subsets (CHE, CT, MGE, MS, QU, DC, CHE23, CW) |
| **Dataset eval** | 3.2 GB, 66 fichiers audio, 8 subsets |
| **Métrique** | Event-based F-score (macro-averaged) |
| **Contrainte** | 5 annotations POS par enregistrement pour fine-tuning |
| **Modèles utilisés** | U-Net frame-level, CNN + fine-tuning, prototypical networks, cosine similarity |
| **Features** | Log-mel spectrograms, PCEN, MFCC, Chromagram |
| **Pas de contrainte TinyML** | Aucune limite de complexité/modèle |

**Source :** `dcase.community/challenge2024/task-few-shot-bioacoustic-event-detection-results`

---

## 4. Compatibilité avec le stack WILDNEXUS/LEAFNET

### 4.1 Stack actuel documenté

| Composant | Spécification | Responsable |
|-----------|--------------|-------------|
| **MCU cible** | ESP32-S3 (240 MHz, 512 KB SRAM, 16 MB Flash) | Araignée 🕷️ |
| **Framework ML** | TensorFlow Lite Micro + Edge Impulse | Musaraigne 🐭 |
| **Architecture** | FOMO (object detection) → MobileNet/CNN en fallback | Musaraigne 🐭 |
| **Quantification** | INT8 | Musaraigne 🐭 |
| **Pipeline** | PIR (EKMB) → wake ESP32 → inférence TFLite → capture OV5640 | Araignée 🕷️ |
| **Protocoles** | MQTT, ESP-NOW, LoRa, WiFi | Araignée 🕷️ |
| **Audio** | NEXUS_ACOUSTIC en développement (BirdNET ecosystem analysis) | Clio 🐬, Chouette 🦉 |

### 4.2 Gap analyse pour un challenge TinyML bioacoustique

| Exigence probable | Statut WILDNEXUS | Gap |
|-------------------|------------------|-----|
| Modèle acoustique on-device | ❌ Stack actuellement visuel (caméra) | **Majeur** — pas de pipeline audio sur ESP32-S3 |
| Quantification INT8 | ✅ Compétence Musaraigne | — |
| Dataset bioacoustique | ⚠️ InsectNet (insectes), pas encore intégré TinyML | Moyen |
| Prétraitement audio (mel, PCEN) | ❌ Non implémenté sur MCU | **Majeur** — besoin DSP embarqué |
| Few-shot learning | ❌ FOMO = supervised, pas few-shot | **Majeur** — paradigme différent |
| Benchmark énergétique | ✅ PPK2, profilage conso | — |
| Contrainte SRAM/Flash stricte | ✅ Compétence cœur Musaraigne | — |

### 4.3 Matrice de compatibilité

| Dimension | Compatibilité | Note |
|-----------|---------------|------|
| Hardware (ESP32-S3) | 🟡 Partielle | OK pour inférence audio légère, mais pas de DSP hardware |
| Edge Impulse / TFLite Micro | 🟢 Bonne | Stack maîtrisé par Musaraigne |
| Pipeline audio embarqué | 🔴 Absent | Tout à construire (acquisition I2S, FFT, mel) |
| Dataset bioacoustique | 🟡 En cours | InsectNet dispo, NEXUS_ACOUSTIC en R&D |
| Few-shot / méta-learning | 🔴 Absent | Compétence non développée |
| Optimisation énergétique | 🟢 Bonne | Protocoles PPK2 rodés |

---

## 5. Opportunités réelles (vs. le « BioDCASE Task 3 » fantôme)

### 5.1 Option A — BioDCASE Workshop 2026 (PAPER)

| Paramètre | Valeur |
|-----------|--------|
| **Type** | Soumission papier académique |
| **Abstract deadline** | **5 juillet 2026** (12 jours !) |
| **Final submission** | 12 juillet 2026 |
| **Notification** | 6 septembre 2026 |
| **Workshop** | Octobre 2026 (en ligne) |
| **Format** | 4-6 pages, IEEE template |

**Sujet possible :** *« Towards TinyML Bioacoustic Monitoring on ESP32-S3: A FOMO-based Architecture for Low-Power Insect Detection »*

**Effort estimé :** 40-60 heures/personne
- Rédaction papier : 20h
- Expériences benchmark : 15h (si pipeline audio partiel)
- Révision/feedback : 10h

### 5.2 Option B — Veille DCASE 2027

- Suivre l'appel à tâches DCASE 2027 (probablement janvier-février 2027)
- Proposer une tâche « TinyML Bioacoustic Event Detection » si l'appel est ouvert
- Préparer le stack en amont (pipeline audio, dataset, baseline)

### 5.3 Option C — BirdCLEF+ 2026 (Kaggle)

- Mentionné par Dobby comme « bon benchmark »
- Non vérifié (recherche web infructueuse)
- À investiguer par Clio 🐬

---

## 6. Bénéfices pour WILDNEXUS

| Bénéfice | Valeur | Via |
|----------|--------|-----|
| **Benchmark externe** | 🟡 Moyen | Papier BioDCASE > challenge (pas de classement) |
| **Visibilité académique** | 🟢 Élevée | BioDCASE = communauté ciblée bioacoustique |
| **Validation hardware** | 🟢 Élevée | Publier des benchmarks ESP32-S3 en bioacoustique |
| **Networking** | 🟢 Élevé | Workshop virtuel, accès aux experts (Cornell, QMUL, TAU) |
| **Crédibilité TinyML** | 🟢 Élevée | Positionne WILDNEXUS dans l'écosystème TinyML audio |
| **Dataset public** | 🟡 Moyen | Si on publie un dataset insectes annoté |

---

## 7. Recommandation

### Verdict : **NO-GO pour « BioDCASE Task 3 2026 »** (n'existe pas)

### GO conditionnel pour les alternatives :

| Action | Priorité | Deadline | Owner suggéré |
|--------|----------|----------|---------------|
| **1. Valider GO/NO-GO papier BioDCASE** | 🔴 Urgent | 28 juin 2026 | Dobby + Araignée |
| **2. Rédiger abstract BioDCASE** | 🔴 Urgent | 5 juillet 2026 | Clio + Musaraigne |
| **3. Benchmark audio ESP32-S3** | 🟡 Court terme | 10 juillet 2026 | Araignée + Musaraigne |
| **4. Veille DCASE 2027 call for tasks** | 🟢 Moyen terme | Janvier 2027 | Clio |
| **5. Investiguer BirdCLEF+ 2026** | 🟡 Court terme | 30 juin 2026 | Clio |

### Conditions pour GO papier BioDCASE :
- ✅ Accord Dobby sur l'investissement 40-60h
- ✅ Disponibilité Musaraigne pour benchmark INT8 audio
- ✅ Pipeline audio minimal fonctionnel (I2S capture → mel → inférence) avant le 10 juillet
- ⚠️ Si le pipeline audio n'est pas prêt → soumettre un « position paper » ou « work-in-progress »

---

## 8. Sources

| Source | URL | Contenu |
|--------|-----|---------|
| DCASE 2026 Challenge | `dcase.community/challenge2026/` | 7 tâches, pas de bioacoustique TinyML |
| DCASE 2026 Workshop | `dcase.community/workshop2026/` | BioDCASE co-localisé, abstract 5 juillet |
| DCASE 2024 Task 5 Results | `dcase.community/challenge2024/task-few-shot-bioacoustic-event-detection-results` | Meilleur F-score 65.2% |
| DCASE 2025 Workshop | `dcase.community/workshop2025/` | BioDCASE 2025 présentiel Barcelone |
| Dobby BirdNET Analysis | `TEAM_Inbox/2026-06-23_dobby_analyse-birdnet-ecosysteme_integration-pka.md` | Mention « BioDCASE Task 3 » |
| Profil Araignée | `TEAM/araignee.md` | Stack ESP32-S3, firmware, bench |
| Profil Musaraigne | `TEAM/musaraigne.md` | Edge Impulse, TFLite, INT8, FOMO |

---

*Rapport terminé. Fichier à archiver dans `03_PROJECTS/03_WILDNEXUS/02_RESEARCH/` après décision Dobby.*
