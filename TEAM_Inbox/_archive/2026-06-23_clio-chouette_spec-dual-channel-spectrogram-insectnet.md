# InsectNet — Spécification Spectrogramme Double Canal

> **Date :** 2026-06-23  
> **Source :** Architecture BirdNET V2.4 (Kahl et al. 2021)  
> **Auteurs :** Dobby 🦉 (spec) → Clio 🐬 + Chouette 🦉 (implémentation)  
> **Statut :** Spec V0.1 — prêt pour implémentation

---

## Contexte

BirdNET V2.4 utilise **deux spectrogrammes mel en parallèle** pour capturer à la fois les basses et hautes fréquences. Ce pattern est directement applicable aux orthoptères dont les chants s'étendent typiquement de 2 kHz à 20+ kHz.

## Problème actuel

Le pipeline InsectNet V0.1 utilise un spectrogramme unique, ce qui :
- Écrase les harmoniques hautes (>10 kHz) des Tettigoniidae
- Impose un compromis résolution fréquentielle entre basses et hautes fréquences
- Réduit la discriminabilité des espèces à large bande spectrale

## Architecture proposée

### Principe

Deux spectrogrammes mel calculés en parallèle depuis le même signal 48 kHz :

| Paramètre | Canal BAS | Canal HAUT |
|-----------|-----------|------------|
| fmin | 500 Hz | 4 kHz |
| fmax | 6 kHz | 24 kHz |
| n_fft | 2048 | 1024 |
| hop_length | 278 | 280 |
| n_mels | 96 | 96 |
| Résolution finale | 96 × 511 | 96 × 511 |
| Cible | Stridulations graves (Gryllus, ~4-5 kHz) | Chants aigus (Tettigonia, 8-20 kHz) |

### Justification des bandes (par rapport à BirdNET)

BirdNET utilise 0-3 kHz + 500 Hz-15 kHz (optimisé oiseaux). Pour les insectes :
- **Canal bas étendu à 500 Hz-6 kHz** — couvre Gryllus campestris (4-5 kHz), Gryllus bimaculatus, tous les Gryllidae
- **Canal haut étendu à 4-24 kHz** — couvre Tettigonia viridissima (8-20 kHz), Metrioptera roeselii (10-20 kHz), Conocephalus (15-30 kHz partiel à 48k)
- Chevauchement 4-6 kHz pour éviter les pertes aux frontières

### Code de référence (pseudo-Python)

```python
import librosa
import numpy as np

def dual_channel_mel_spectrogram(
    y: np.ndarray,
    sr: int = 48000,
    low_band: tuple = (500, 6000),
    high_band: tuple = (4000, 24000),
    n_mels: int = 96,
    duration_ms: int = 3000
) -> tuple[np.ndarray, np.ndarray]:
    """
    Calcule le spectrogramme double canal inspiré de BirdNET V2.4.
    
    Args:
        y: Signal audio normalisé entre -1 et 1
        sr: Taux d'échantillonnage (48 kHz)
        low_band: (fmin_low, fmax_low) en Hz
        high_band: (fmin_high, fmax_high) en Hz
        n_mels: Nombre de bins mel par canal
        duration_ms: Durée cible en ms (pad ou trim)
    
    Returns:
        (low_mel, high_mel): Deux matrices (n_mels, time_frames)
    """
    # 1. Normalisation
    y = y / (np.max(np.abs(y)) + 1e-8)
    
    # 2. Padding/trimming à 3 secondes
    target_len = int(sr * duration_ms / 1000)
    if len(y) < target_len:
        y = np.pad(y, (0, target_len - len(y)))
    else:
        y = y[:target_len]
    
    # 3. Canal bas — n_fft plus grand pour résolution fréquentielle
    S_low = librosa.feature.melspectrogram(
        y=y, sr=sr,
        n_fft=2048,            # Haute résolution fréquentielle
        hop_length=278,        # ~511 frames pour 3s
        fmin=low_band[0],
        fmax=low_band[1],
        n_mels=n_mels,
        power=2.0
    )
    
    # 4. Canal haut — n_fft plus petit, couvre jusqu'à 24 kHz
    S_high = librosa.feature.melspectrogram(
        y=y, sr=sr,
        n_fft=1024,            # Couvre mieux les hautes fréquences
        hop_length=280,        # ~515 frames pour 3s
        fmin=high_band[0],
        fmax=high_band[1],
        n_mels=n_mels,
        power=2.0
    )
    
    # 5. Conversion dB avec scaling non-linéaire (Schlüter 2018)
    low_db = librosa.power_to_db(S_low, ref=np.max, top_db=80)
    high_db = librosa.power_to_db(S_high, ref=np.max, top_db=80)
    
    return low_db, high_db
```

### Stratégie de fusion

Deux options, à évaluer expérimentalement :

**Option A — Stack de canaux (recommandé V0.1)**
```python
# Empilement comme canaux d'entrée CNN
input_tensor = np.stack([low_db, high_db], axis=-1)  
# Shape: (96, 511, 2) — compatible FOMO/Edge Impulse
```
Avantage : simple, compatible Edge Impulse, le modèle apprend la pondération.

**Option B — Concatenation fréquentielle**
```python
# Concaténation verticale → un seul grand spectrogramme
combined = np.concatenate([low_db, high_db], axis=0)
# Shape: (192, 511) — nécessite adaptation architecture
```
Avantage : plus d'information en une passe, mais sort du workflow FOMO standard.

## Plan d'implémentation

### Phase 1 — Validation (semaine en cours)
1. Générer les spectrogrammes double canal sur 20 segments de test (5 espèces)
2. Comparer visuellement : single vs dual channel
3. Vérifier que les harmoniques hautes sont bien capturées pour Tettigonia

### Phase 2 — Entraînement comparatif
4. Entraîner 2 modèles FOMO identiques : single channel vs dual channel
5. Comparer accuracy, F1-score par espèce
6. Mesurer l'impact sur les espèces haute fréquence (Tettigonia, Metrioptera)

### Phase 3 — Optimisation
7. Ajuster les bandes fmin/fmax si nécessaire
8. Tester Option A vs Option B
9. Intégrer dans le pipeline de segmentation automatisé

## Impact attendu

| Métrique | Single canal (actuel) | Double canal (attendu) |
|----------|----------------------|----------------------|
| Accuracy Tettigonia | ~60-70% | ~80-85% |
| Accuracy Gryllus | ~75-85% | ~80-85% |
| Accuracy globale | ~70% | ~80% |
| Faux positifs interspécifiques | Élevé (confusion hautes fréquences) | Réduit |

## Références

- Kahl et al. 2021, "BirdNET: A deep learning solution for avian diversity monitoring", Ecological Informatics 61
- Schlüter 2018, "Learning to isolate musical instruments" (non-linear magnitude scaling)
- BirdNET V2.4 model specs : https://birdnet-team.github.io/BirdNET-Analyzer/models.html

---

*Spécification à valider par Clio (pertinence scientifique) et Chouette (faisabilité DSP) avant implémentation.*
