# ADR-017 — Schéma métadonnées audio et format de fichiers

**Date :** 2026-07-05  
**Dernière mise à jour :** 2026-11-05 — volumes stéréo et preuves de compatibilité
**Statut :** accepté comme contrat ; validation matérielle ouverte
**Owner PKA :** [[Dobby]] + [[Forge]] + [[Chouette]]  
**Jalon :** M-02 — Prototype banc  

## Contexte

ADR-013 définit une cible stéréo à deux micros MEMS ; les références et l'interface des micros réellement en stock restent à confirmer. ADR-016 définit le cycle firmware audio (FFT 15 min + clip WAV 60 min). ADR-014 définit la transmission LoRa des features spectrales.

**Ce qui manque :** comment les clips WAV sont stockés sur la carte SD, quelles métadonnées les accompagnent, et comment ces fichiers sont compatibles avec les pipelines en aval — InsectNet (classification orthoptères) et NEXUS_ACOUSTIC (BirdNET, TweetyBERT, SoundPlot).

Le risque : si le format P0 est propriétaire ou incomplet, les clips devront être retraités manuellement avant alimentation des pipelines. Le WAV PCM et les sidecars JSON visent à limiter ce retraitement, mais le flux WildNexus SD → extraction → InsectNet/NEXUS_ACOUSTIC reste à démontrer. Selon les entrées réellement acceptées par chaque outil, une étape de déchiffrement, de mixdown mono, de resampling ou de conversion pourra être nécessaire.

## Décision

Le schéma et le format sont acceptés comme contrat d'implémentation. Leur validation matérielle et leur compatibilité avec les pipelines aval restent soumises aux tests de fin de document.

### 1. Format audio — WAV PCM 16-bit 16 kHz stéréo

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Conteneur | WAV (RIFF) | Standard lisible par les outils audio ; compatibilité des pipelines à démontrer sur fichiers réels |
| Encodage | PCM 16-bit signed little-endian | Standard non compressé, pas de codec à implémenter sur ESP32-S3 |
| Sample rate | 16000 Hz | Vise les entrées 16 kHz de BirdNET-Lite ; traitement stéréo et resampling à tester. Vérifier les exigences de chaque pipeline et taxon |
| Canaux | 2 (stéréo) | ADR-013 — deux micros, références et placement à valider |
| Duration clip P0 | 3 secondes | ADR-013 — 24 clips/jour = 4 608 000 octets de PCM, hors sidecars |
| Duration clip P1 | 10-30 secondes | Monitoring continu NEXUS_ACOUSTIC — configurable via downlink 0x06 |

**Données audio P0 :** 16000 Hz × 2 octets × 2 canaux × 3 s = **192 000 octets par clip**, hors en-tête WAV et JSON. À 24 clips/jour : **4 608 000 octets/jour**, soit environ **4,61 MB/jour** en notation décimale.

**Pourquoi pas 48 kHz ?** Le choix 16 kHz vise la compatibilité avec plusieurs pipelines oiseaux et limite le volume de données. Il impose une bande analysable inférieure à 8 kHz : il ne peut donc pas couvrir les vocalisations au-delà de cette fréquence. La couverture des orthoptères, amphibiens ou autres taxons n'est pas généralisée ; elle devra être établie par liste d'espèces cibles et protocole d'échantillonnage. Un passage à 48 kHz reste une option P1 si ces exigences le justifient.

**Upgrade path P1 :** si l'ICS-43434 est monté et le sample rate passe à 48 kHz, les fichiers P1 seront 3× plus gros (576 KB/clip), mais le format WAV reste identique. Seul le header change.

### 2. Convention de nommage

```
AUDIO/{NODE_ID}/{YYYY}/{MM}/{DD}/
  {NODE_ID}_{YYYYMMDD}_{HHMMSS}_{TYPE}.wav
  {NODE_ID}_{YYYYMMDD}_{HHMMSS}_{TYPE}.json
```

| Champ | Format | Exemple |
|-------|--------|---------|
| NODE_ID | hex 8 chars | `A1B2C3D4` |
| YYYYMMDD | date | `20260715` |
| HHMMSS | UTC time | `143000` |
| TYPE | `FFT` ou `CLIP` | `CLIP` |

**Exemple :**
```
AUDIO/A1B2C3D4/2026/07/15/A1B2C3D4_20260715_143000_CLIP.wav
AUDIO/A1B2C3D4/2026/07/15/A1B2C3D4_20260715_143000_CLIP.json
```

Les fichiers FFT ne génèrent pas de WAV — ils produisent uniquement un fichier JSON avec les 10 descripteurs spectraux (cf. §3). Le nom `FFT` est utilisé pour le sidecar JSON spectral.

### 3. Métadonnées — Sidecar JSON

Chaque clip WAV est accompagné d'un fichier JSON portant le même nom de base. Format :

```json
{
  "schema_version": "1.0",
  "project": "wildnexus",
  "node_id": "A1B2C3D4",
  "timestamp_utc": "2026-07-15T14:30:00Z",
  "timestamp_unix": 1752635400,
  "audio": {
    "format": "wav",
    "sample_rate": 16000,
    "bits_per_sample": 16,
    "channels": 2,
    "duration_sec": 3.0,
    "samples": 48000,
    "codec": "pcm_s16le"
  },
  "microphones": {
    "model": "SPH0645LM4H-B",
    "count": 2,
    "placement": "opposed",
    "baseline_mm": 120,
    "mic_l_status": "ok",
    "mic_r_status": "ok",
    "gain_db": 0
  },
  "environment": {
    "temperature_c": 18.5,
    "battery_mv": 5800,
    "light_lux": null,
    "humidity_pct": null
  },
  "spectral_features": {
    "centroid_hz": 4200.0,
    "rolloff_hz": 6500.0,
    "bandwidth_hz": 2800.0,
    "flatness": 0.32,
    "rms": 0.15,
    "zero_crossing_rate_hz": 3100.0,
    "entropy": 0.71,
    "peak_frequency_hz": 4700.0,
    "skewness": -0.42,
    "kurtosis": 2.1
  },
  "detection": {
    "event_type": "scheduled_audio_clip",
    "trigger_source": "timer_60min",
    "pir_triggered": false,
    "previous_motion_event": "2026-07-15T14:15:00Z"
  },
  "integrity": {
    "sha256": "a3f5e8...",
    "file_size_bytes": 192044,
    "crc16": 45012
  }
}
```

Les JSON de cette ADR sont des exemples de schéma, non des captures réelles. Les champs `microphones`, les mesures, les compteurs et les statuts doivent provenir du nœud et de son provisioning ; ils ne doivent pas être copiés comme des constantes de démonstration présentées comme des observations.

**Champs `null`** : les capteurs environnementaux non montés en P0 (BME688 consigné reçu mais pas sur le nœud prototype M-02) sont présents dans le schéma mais null. L'absence de valeur est explicite, pas une omission.

**Spectral features** : les 10 descripteurs sont répétés dans le sidecar JSON du CLIP (mesurés sur ce clip), et aussi dans un sidecar JSON dédié pour les cycles FFT 15 min (qui n'ont pas de clip WAV).

### 4. Sidecar JSON spectral (FFT 15 min)

Pas de WAV — uniquement un JSON compact :

```json
{
  "schema_version": "1.0",
  "project": "wildnexus",
  "node_id": "A1B2C3D4",
  "timestamp_utc": "2026-07-15T14:15:00Z",
  "timestamp_unix": 1752635100,
  "type": "spectral_fft",
  "fft_config": {
    "size": 1024,
    "samples": 4096,
    "window": "hann",
    "hop_size": 2048
  },
  "spectral_features": {
    "centroid_hz": 4200.0,
    "rolloff_hz": 6500.0,
    "bandwidth_hz": 2800.0,
    "flatness": 0.32,
    "rms": 0.15,
    "zero_crossing_rate_hz": 3100.0,
    "entropy": 0.71,
    "peak_frequency_hz": 4700.0,
    "skewness": -0.42,
    "kurtosis": 2.1
  },
  "environment": {
    "temperature_c": 18.5,
    "battery_mv": 5800
  },
  "transmitted_lora": true,
  "lora_frame_counter": 142
}
```

### 5. Structure de répertoires sur SD

```
/sdcard/
├── DCIM/                          ← images caméra (Camtrap-DP, ADR-016)
│   └── {NODE_ID}_{YYYYMMDD}_{HHMMSS}.jpg
│   └── {NODE_ID}_{YYYYMMDD}_{HHMMSS}.json
├── AUDIO/                         ← clips + features spectrales
│   └── {NODE_ID}/
│       └── 2026/07/15/
│           ├── A1B2C3D4_20260715_141500_FFT.json
│           ├── A1B2C3D4_20260715_143000_CLIP.wav
│           ├── A1B2C3D4_20260715_143000_CLIP.json
│           └── ...
├── LOGS/
│   └── system_{YYYYMMDD}.log
└── CONFIG/
    └── node_config.json
```

Séparation `DCIM/` (caméra) et `AUDIO/` (audio) pour extraction indépendante.

### 6. Stratégie taille SD

| Carte | Audio P0 seul, hors JSON* | P1 continu 48 kHz/16 bits/stéréo* |
|-------|--------------------------|------------------------------------|
| 32 GB | ≈6 940 jours | ≈1,93 jour |
| 64 GB | ≈13 890 jours | ≈3,86 jours |
| **128 GB** | ≈27 780 jours | **≈7,72 jours** |

\* Capacités décimales nominales, sans espace réservé au système de fichiers, aux images, aux JSON, aux logs ni à la politique de rétention. Ce sont des maxima théoriques audio, pas des durées de fonctionnement autonome.

**Choix P0 : 128 GB, comme marge média à consolider, pas parce que l'audio seul l'exige.**

- P0 : 24 clips/jour = environ 4,61 MB de WAV/jour, plus 24 sidecars de clips et 96 JSON spectraux.
- P1 continu à 48 kHz : 192 000 octets/s = 16 588 800 000 octets/jour, soit ≈16,6 GB/jour ; 128 GB offre ≈7,7 jours théoriques audio seuls.
- Les images, la rétention, le chiffrement, l'endurance et l'espace libre doivent entrer dans le dimensionnement final ; aucune durée entre passages terrain n'est promise sans ces hypothèses.
- Le coût de la carte reste à confirmer dans le budget réconcilié.

### 7. Compatibilité pipelines aval

| Pipeline | Format attendu | Compatibilité P0 | Action |
|----------|---------------|-----------------|--------|
| **BirdNET-Lite** (RPi 5) | WAV 16 kHz | 🟡 À valider sur un clip réel | Tester explicitement le traitement des deux canaux ; ajouter un mixdown mono si nécessaire |
| **InsectSet459** fine-tuning | WAV 16-48 kHz mono | 🟡 Conversion prévue | `ffmpeg -i input.wav -ac 1 output.wav`, puis vérifier les exigences du pipeline |
| **TweetyBERT** (M5) | WAV/FLAC, entrée resamplée | 🟡 À valider | Tester `librosa.load()` et le resampling du clip réel |
| **SoundPlot** (3D viz) | WAV + timestamps | 🟡 À valider | Vérifier l'import du WAV et du sidecar JSON |
| **Camtrap-DP** (images) | JPEG + CSV metadata | N/A (séparé) | — |

### 8. Chiffrement SD et audio

ADR-010 §2 impose le chiffrement AES-128 minimum des données SD. Les fichiers audio sont chiffrés au repos comme les images.

**Impact :** l'extraction SD nécessite le nœud ou la procédure de récupération autorisée. La clé du nœud doit être dérivée de son identifiant et d'un secret de provisioning, conformément à ADR-010/011 ; le serial MCU seul n'est jamais un secret suffisant. La master key PKA n'est pas embarquée sur le nœud.

**Exception P0 :** sur le prototype banc M-02, le chiffrement peut être désactivé pour faciliter les tests. Activé obligatoirement à partir de M-03 (terrain).

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| WAV PCM 16-bit 16 kHz stéréo | Standard, pas de codec, tests possibles dans tous les pipelines cibles | Volume supérieur aux formats compressés ; stéréo à adapter si nécessaire | **Retenu P0, compatibilité à prouver** |
| FLAC | Compression sans perte, ~60% de WAV | Codec FLAC sur ESP32-S3 = complexité firmware, librairie lourde | P1 si besoin storage |
| Opus | Excellent ratio qualité/taille | Codec complexe, pas universel pour bioacoustique | Rejeté |
| MP3 | Compact | Compression avec perte, inacceptable pour bioacoustique scientifique | Rejeté |
| Pas de sidecar JSON | Simplicité | Métadonnées perdues, pipeline aval doit deviner | Rejeté |
| Métadonnées intégrées WAV (RIFF INFO) | Un seul fichier | Support partiel, champs limités, pas de features spectrales | Rejeté — JSON sidecar plus flexible |
| Sidecar CSV au lieu de JSON | Simplicité parsing | Pas de hiérarchie, pas de null explicite, pas de types | Rejeté — JSON standard pour bioacoustique (GBIF, Camtrap-DP) |

## Conséquences

- Le module `wn_audio_metadata.c` (ADR-016) génère le header WAV RIFF + le sidecar JSON à chaque clip.
- Le module `wn_storage.c` gère la structure de répertoires `AUDIO/{NODE_ID}/{YYYY}/{MM}/{DD}/`.
- Le parser gateway (Python) peut router les clips vers InsectNet (dossier `INSECTNET/raw_audio/`) ou NEXUS_ACOUSTIC (`NEXUS_ACOUSTIC/raw_audio/`) selon l'origine du nœud.
- Le BOM P0 doit inclure une carte microSD **128 GB minimum**. Son coût et la réserve budgétaire disponible sont à confirmer dans le suivi d'achats réconcilié ; cette ADR ne fige ni prix ni solde de trésorerie.
- Le script d'extraction SD (Forge, à créer) déchiffre + copie + valide SHA-256 + route vers les projets.

## Tests obligatoires pour la validation matérielle et la clôture M-02

| Test | Critère minimal |
|---|---|
| Fichier WAV lisible | `ffprobe` affiche : PCM s16le, 16000 Hz, 2 channels, 3.0s |
| Sidecar JSON valide | `jq .` parse sans erreur, tous les champs présents |
| Compatibilité BirdNET-Lite | BirdNET traite le WAV sans erreur de format |
| Compatibilité librosa (TweetyBERT) | `librosa.load()` réussit sur le WAV |
| Nommage respecté | Structure de répertoires `AUDIO/{NODE_ID}/...` conforme |
| 24 clips + 96 FFT | 24h de fonctionnement → 24 WAV + 96 JSON spectraux + 24 JSON clips sur SD |
| SHA-256 sidecar | Le hash dans le JSON correspond au hash calculé du WAV |

## Critère de révision

Réviser cette ADR si :
- BirdNET-Lite exige un sample rate différent de 16 kHz
- InsectSet459 fine-tuning nécessite des fichiers mono uniquement
- L'ICS-43434 (upgrade P1) nécessite 48 kHz et le format WAV 48 kHz pose des problèmes de stockage
- Le chiffrement AES-128 rend l'extraction SD trop lente pour des volumes P1
- Le sidecar JSON devient trop gros pour la SD (cas P1 avec features étendues)

---

*Créé le 2026-07-05 ; révisé le 2026-11-05 : 4,61 MB WAV/jour hors JSON, stockage recalculé et compatibilités maintenues comme tests obligatoires. L'acceptation du schéma n'est pas une validation matérielle.*
