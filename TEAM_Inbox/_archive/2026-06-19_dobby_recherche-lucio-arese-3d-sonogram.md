# Lucio Arese — Seeing Birdsong : Analyse technique
> Recherche pour PKA-JCH / InsectNet
> 2026-06-19 par Dobby 🦉

---

## L'artiste

**Lucio Arese** — artiste numérique italien. Projet « Seeing Birdsong » présenté à la 4ème Conférence sur les Vocalisations Ultrasoniques (Nencki Institute, Académie Polonaise des Sciences). Collaboration avec le réalisateur nature Thibault Noirot.

---

## La technologie

### Pipeline audio → 3D

```
Audio (WAV)
  │
  ├─► Analyse spectrale (librosa / Essentia)
  │     ├─ MFCC (Mel-Frequency Cepstral Coefficients)
  │     ├─ Spectral centroid, bandwidth, rolloff
  │     ├─ Zero-crossing rate
  │     └─ Chroma features
  │
  ├─► Embedding haute dimension (UMAP / t-SNE)
  │     └─ Réduction dimensionnelle → manifold 3D
  │
  └─► Rendu 3D interactif (Three.js / WebGL)
        ├─ X = Fréquence (2-12 kHz, le « sweet spot » aviaire)
        ├─ Y = Amplitude (A^0.6 pour booster les sons faibles)
        ├─ Z = Temps (100 frames à 60fps = 1.6s de « traînée sonique »)
        └─ Couleur = Index spectral (Cyan → Magenta, encode les harmoniques)
```

### C'est bien du 4D

| Dimension | Variable | Rendu |
|-----------|----------|-------|
| **X** | Fréquence (Hz) | Position horizontale |
| **Y** | Amplitude (dB) | Hauteur / élévation |
| **Z** | Temps (rolling) | Profondeur / traînée |
| **Couleur** | Indice spectral | 4ème dimension — encode le contenu fréquentiel |

---

## Outils identifiés

### Code open-source
| Outil | Dépôt | Rôle |
|-------|-------|------|
| **TronArese** | `github.com/arcesoftware/TronArese` | Moteur 3D WebGL pour spectrogramme oiseau |
| **Seeing Birdsong** | `lucioarese.net/seeing-birdsong` | Framework complet — spectral descriptors + ML embedding |
| **WaveDataVisualisation** | `github.com/Sarath19-web/WaveDataVisualisation` | Clone Python temps réel inspiré de Seeing Birdsong |

### Stack technique
| Couche | Technologie |
|--------|------------|
| Analyse audio | librosa, Essentia, ffmpeg |
| Descripteurs spectraux | MFCC, chroma, spectral centroid/bandwidth/rolloff |
| ML / Embedding | scikit-learn, UMAP, t-SNE |
| 3D temps réel | Three.js + WebGL + WebAudio API |
| Rendu offline | Python matplotlib (2D), Blender (3D export) |
| Interactivité | Orbit camera, zoom, molette, redémarrage |

---

## Applicabilité à InsectNet / PKA

### Ce qu'on peut faire avec nos 1 441 segments

| Niveau | Ce qu'on ferait | Outil |
|--------|----------------|-------|
| **1. Spectrogramme 2D** | Mel-spec classique 128 bands | Déjà prêt (insectnet_generate_spectrograms.py) |
| **2. Spectrogramme 3D** | Fréquence × Temps × Amplitude en relief | Python + matplotlib 3D / plotly |
| **3. Manifold 4D** | UMAP sur descripteurs spectraux → nuage de points 3D coloré par espèce | Python + sklearn + plotly |
| **4. Temps réel** | Visualisation WebGL d'un segment qui défile | Adapter TronArese (Three.js + WebAudio) |

### Le plus beau pour tes photos

Le **niveau 3 — Manifold 4D** — est exactement ce que Lucio Arese poste. Chaque espèce forme un « nuage » distinct dans l'espace 3D, avec une couleur différente. C'est élégant ET scientifiquement utile : on voit immédiatement si deux espèces ont des signatures acoustiques proches.

### Coût

| Niveau | Effort | Outil |
|--------|--------|-------|
| 2D spectrogram | ✅ Fait | Script existant |
| 3D spectrogram | ~1h | 20 lignes de Python + plotly |
| Manifold 4D | ~2h | 50 lignes Python + sklearn UMAP + plotly |
| Temps réel WebGL | ~4h | Adaptation TronArese |

---

## Sources

- `lucioarese.net/seeing-birdsong/` — Landing page
- `github.com/arcesoftware/TronArese` — Moteur 3D open-source (MIT?)
- `grokipedia.com/page/Seeing_Birdsong` — Description technique
- `mindbento.com/hn-top/seeing-birdsong` — TLDR + HN discussion
- YouTube : « Visualizing Bird Songs: A Mathematical Model »
