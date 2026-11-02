# Sound Sources — European Insect Bioacoustics

## Objective

Identify reliable and automatable sources of European insect sound recordings suitable for:
- AI training
- BirdNET-like systems
- WildNexus acoustic biodiversity monitoring
- Environmental sound recognition

---

# 1. [[Xeno-Canto]]

https://[[Xeno-Canto]].org

## Interest

Currently the most strategic source for Orthoptera and many bioacoustic projects.

### Advantages
- Public API
- Automated download possible
- Rich metadata
- GPS coordinates
- License information
- Large European coverage
- Thousands of Orthoptera recordings

### API Example

```bash
https://xeno-canto.org/api/2/recordings?query=grp:orthoptera+cnt:belgium
```

### Available Data
- species
- country
- latitude/longitude
- date
- author
- license
- download URL

### Suitability
Excellent for:
- ML datasets
- automated pipelines
- BirdNET-like systems

---

# 2. BioAcoustica

https://bio.acousti.ca

## Interest

Scientific bioacoustic platform specialized in insect sounds.

### Advantages
- structured taxonomy
- academic quality
- open data
- downloadable recordings

### Suitability
Very good for:
- clean datasets
- scientific validation
- species-level annotation

---

# 3. iNaturalist

https://www.inaturalist.org

## Interest

Massive biodiversity observation platform with audio support.

### Advantages
- API available
- GPS data
- Europe well covered
- active ecosystem

### Issues
- variable sound quality
- mixed licenses
- requires filtering

### API Example

```bash
https://api.inaturalist.org/v1/observations
```

### Suitability
Good for:
- dataset enrichment
- geographic expansion
- rare species

---

# 4. ECOSoundSet

Scientific dataset dedicated to European Orthoptera and Cicadidae.

### Coverage
- Western Europe
- Belgium
- France
- Germany
- Netherlands
- Switzerland

### Advantages
- AI-ready
- annotated
- train/test splits
- very useful for deep learning

### Suitability
Excellent for:
- benchmarking
- initial model training
- validation

---

# 5. InsectSet459

Large insect sound dataset.

### Content
- ~26,000 recordings
- 459 species
- Orthoptera
- Cicadas

### Sources
Compiled from:
- [[Xeno-Canto]]
- iNaturalist
- BioAcoustica

### Advantages
- already cleaned
- ML-ready
- large scale

---

# 6. Freesound

https://freesound.org

## Interest

General-purpose sound platform.

### Advantages
- API
- huge library
- insect sounds available

### Issues
- not scientific
- metadata weak
- many artificial sounds

### Suitability
Useful for:
- ambience
- pretraining
- demos

---

# 7. DASA — Digital Animal Sound [[archive]]

https://www.dasarchive.org

Academic [[archive]].

### Interest
Potential future strategic source for:
- biodiversity datasets
- European scientific archives

---

# Recommended Initial Species (V0.1)

## Priority Species

1. Tettigonia viridissima
2. Gryllus campestris
3. Pholidoptera griseoaptera
4. Leptophyes punctatissima
5. Metrioptera roeselii
6. Cicada orni

---

# Technical Recommendations

## Audio Format

Preferred:
- WAV
- 48 kHz minimum

Reason:
Many insects produce high-frequency components.

---

# Recommended Architecture

## First Phase

Dataset collection:
- [[Xeno-Canto]]
- ECOSoundSet
- InsectSet459

## Second Phase

Dataset enrichment:
- BioAcoustica
- iNaturalist

## Third Phase

Ambient/pretraining data:
- Freesound
- Pixabay
- LaSonothèque

---

# Practical Workflow

1. Download recordings
2. Build metadata CSV
3. Manual quality check
4. Segment audio (1–3 s)
5. Generate spectrograms
6. Train first CNN classifier
7. Add geographic filtering
8. Improve iteratively

---

# Suggested WildNexus Architecture

Audio
→ segmentation
→ spectrogram
→ embeddings
→ classifier
→ geographic filtering
→ local storage
→ cloud synchronization

---

# Long-Term Vision

WildNexus could evolve toward a multi-taxa acoustic system:
- birds
- insects
- amphibians
- bats
- mammals

using:
- shared embeddings
- specialized classifiers
- biodiversity context filtering
