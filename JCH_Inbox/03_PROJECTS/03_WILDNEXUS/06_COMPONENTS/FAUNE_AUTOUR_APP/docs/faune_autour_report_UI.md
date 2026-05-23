# Faune Autour — Technical & Product Evolution Report  
Version: Consolidated roadmap v1.0 · May 2026

---

## 1. Project Context

Faune Autour is a mobile-first (PWA) application designed to display animal species observed around a user’s GPS location.

Current architecture:

GPS → GBIF API → species occurrences → UI (list + map)

Key characteristics:
- Static HTML (GitHub Pages)
- No backend
- GBIF as primary data source
- Leaflet for maps
- Local dictionary for names
- Wikipedia API for images

Limitations:
- Single data source
- No real-time sensing
- No intelligence layer

---

## 2. Strategic Objective

Transform the app into:

“What is around me now?”
+ What is likely present
+ What am I hearing now

---

## 3. Data Strategy

### Base
- GBIF (global backbone)

### Additional sources
- eBird (birds, high freshness)
- iNaturalist (photos + recent observations)

### Country layer
- France: INPN / OpenObs
- Italy: iNaturalist + GBIF
- Germany: GBIF.de + ArtenFinder
- Spain: GBIF.ES
- Netherlands: Observation.org / Waarneming

---

## 4. Data Fusion

Normalize and merge:

Input APIs → normalize taxon → merge → rank → output list

---

## 5. Sound Recognition

Use BirdNET (not Merlin)

Workflow:
User → record sound → send → BirdNET → results → compare with local species

---

## 6. Architecture

Target:

Frontend (PWA)
↓
Backend API
- /species-nearby
- /birds-nearby
- /inat-nearby
- /sound-detect
- /species-score

---

## 7. Scoring Model

Confidence =
- recency
- distance
- sources
- season
- reliability

---

## 8. Roadmap

### v8
- Multi-source data
- scoring
- country detection

### v9
- sound detection (BirdNET)

### v10
- species profiles
- history
- personal log

---

## 9. UX Modes

- Explorer
- Birds
- Listen
- Species profile

---

## 10. Constraints

- Static app insufficient → backend required
- API restrictions (eBird, etc.)

---

## 11. Final Vision

Faune Autour =
GPS biodiversity engine
+ real-time sound detection
+ intelligence layer

---

## 12. Next Steps

1. Build backend
2. Integrate eBird + iNaturalist
3. Add scoring
4. Add BirdNET
