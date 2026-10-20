# ADR-017 — Schéma métadonnées audio et format de fichiers

**Date :** 2026-07-05  
**Statut :** accepté  
**Owner PKA :** [[Dobby]] + [[Forge]] + [[Chouette]]  
**Jalon :** M-02 — Prototype banc  

## Contexte

ADR-013 définit la couche acoustique hardware (2× SPH0645LM4H-B, I2S, stéréo). ADR-016 définit le cycle firmware audio (FFT 15 min + clip WAV 60 min). ADR-014 définit la transmission LoRa des features spectrales.

**Ce qui manque :** comment les clips WAV sont stockés sur la carte SD, quelles métadonnées les accompagnent, et comment ces fichiers sont compatibles avec les pipelines en aval — InsectNet (classification orthoptères) et NEXUS_ACOUSTIC (BirdNET, TweetyBERT, SoundPlot).

Le risque : si le format P0 est propriétaire ou incomplet, les clips devront être retraités manuellement avant alimentation des pipelines. Si le format est standardisé dès le départ, le flux est direct : WildNexus SD → extraction → InsectNet/NEXUS_ACOUSTIC sans conversion.

## Décision proposée

### 1. Format audio — WAV PCM 16-bit 16 kHz stéréo

| Paramètre | Valeur | Raison |
|-----------|--------|--------|
| Conteneur | WAV (RIFF) | Universel, lisible par BirdNET, InsectSet459, TweetyBERT, ffmpeg, Audacity |
| Encodage | PCM 16-bit signed little-endian | Standard non compressé, pas de codec à implémenter sur ESP32-S3 |
| Sample rate | 16000 Hz | Compatible BirdNET-Lite (RPi 5). InsectSet459 utilise 16-48 kHz. TweetyBERT résolution 2.7ms = ~6 samples à 16kHz |
| Canaux | 2 (stéréo) | ADR-013 — 2× SPH0645LM4H-B en opposition |
| Duration clip P0 | 3 secondes | ADR-013 — 13 MB/jour à ce rythme |
| Duration clip P1 | 10-30 secondes | Monitoring continu NEXUS_ACOUSTIC — configurable via downlink 0x06 |

**Taille fichier P0 :** 16000 Hz × 2 bytes × 2 channels × 3s = **192 KB par clip**

**Pourquoi pas 48 kHz ?** InsectSet459 contient des fichiers 48 kHz, mais BirdNET-Lite sur RPi 5 travaille à 16 kHz (resample interne). 16 kHz suffit pour les orthoptères < 8 kHz (couvre la majorité des espèces européennes). Les ultrasons (> 15 kHz) nécessitent l'upgrade ICS-43434 + 48 kHz — c'est P1. Pour TweetyBERT, 16 kHz est suffisant car le modèle a été entraîné sur des données oiseaux 16-44 kHz resamplées.

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

**Champs `null`** : les capteurs environnementaux non montés en P0 (BME688 reçu mais pas sur le nœud prototype M-02) sont présents dans le schéma mais null. L'absence de valeur est explicite, pas une omission.

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

| Carte | Capacité | Clips P0/jour | Clips P0 autonomie | Clips P1 continu | Prix |
|-------|----------|-------------|-------------------|-----------------|------|
| 32 GB | 32 000 MB | 13 MB | ~2 461 jours | ~2 jours | ~8€ |
| 64 GB | 64 000 MB | 13 MB | ~4 923 jours | ~4 jours | ~12€ |
| **128 GB** | 128 000 MB | 13 MB | ~9 846 jours | **~8 jours** | **~15€** |

**Recommandation P0 : 128 GB minimum.**

Raisons :
- P0 : 13 MB/jour → une 32 GB suffit largement (ans d'autonomie audio)
- P1 : monitoring continu NEXUS_ACOUSTIC à 16 kHz/16-bit/stéréo = 192 KB/s = 16,6 GB/jour. Une 128 GB donne ~8 jours de marge — suffisante entre deux passages de récupération SD.
- Écart de prix 32→128 = ~7€ — négligeable dans le budget 1000€
- Anticipe la transition P0→P1 sans changement de BOM

### 7. Compatibilité pipelines aval

| Pipeline | Format attendu | Compatibilité P0 | Action |
|----------|---------------|-----------------|--------|
| **BirdNET-Lite** (RPi 5) | WAV 16 kHz mono/stéréo | ✅ Direct — pas de conversion | BirdNET resample si >16kHz ; stéréo mixé en mono automatiquement |
| **InsectSet459** fine-tuning | WAV 16-48 kHz mono | ✅ Conversion : `ffmpeg -i input.wav -ac 1 output.wav` | Script automatisable |
| **TweetyBERT** (M5) | WAV/FLAC, 16-44 kHz | ✅ Direct ou resample librosa | TweetyBERT utilise librosa → gère tous sample rates |
| **SoundPlot** (3D viz) | WAV + timestamps | ✅ Direct + sidecar JSON | JSON fournit les métadonnées temporelles |
| **Camtrap-DP** (images) | JPEG + CSV metadata | N/A (séparé) | — |

### 8. Chiffrement SD et audio

ADR-010 §2 impose le chiffrement AES-128 des données SD. Les fichiers audio sont chiffrés au repos comme les images.

**Impact :** l'extraction SD nécessite le nœud (clé dérivée du serial MCU) ou la master key PKA. Pas de lecture directe sur PC sans le module de déchiffrement.

**Exception P0 :** sur le prototype banc M-02, le chiffrement peut être désactivé pour faciliter les tests. Activé obligatoirement à partir de M-03 (terrain).

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| WAV PCM 16-bit 16 kHz stéréo | Universel, pas de codec, compatible BirdNET/InsectSet/TweetyBERT | Taille ×10 vs FLAC | **Retenu P0** |
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
- Le BOM P0 doit inclure une carte microSD **128 GB minimum** (ajout ~7€ vs 32 GB — dans la réserve budget 111€).
- Le script d'extraction SD (Forge, à créer) déchiffre + copie + valide SHA-256 + route vers les projets.

## Tests obligatoires avant acceptation

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

*Créé le 2026-07-05 par Dobby 🦉 suite à l'audit de cohérence WildNexus ↔ InsectNet/NEXUS_ACOUSTIC. — Forge : implémentation firmware. — Chouette : validation format bioacoustique. — Clio : validation compatibilité scientifique.*
