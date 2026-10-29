# Analyse geomodel — Post-filtre Spatial pour InsectNet via GBIF

> **Date :** 2026-06-23  
> **Source :** https://birdnet-team.github.io/geomodel/ + GitHub repo  
> **Auteur :** Dobby 🦉 → Clio 🐬  
> **Statut :** Analyse — faisabilité confirmée

---

## 1. Qu'est-ce que geomodel ?

BirdNET Geomodel est un **modèle spatio-temporel d'occurrence** qui post-filtre les détections acoustiques de BirdNET :

- **Entrée :** (latitude, longitude, semaine de l'année)
- **Sortie :** Probabilité d'occurrence par espèce
- **Usage :** Supprimer les détections d'espèces improbables à cette localisation/saison
- **Taille :** ~13 MB FP16 — assez petit pour mobile/embarqué

## 2. Architecture technique

```
Données GBIF (occurrences)
    ↓ mapping spatial
Grille H3 hexagonale
    ↓ Google Earth Engine
Features environnementaux (élévation, climat, land cover)
    ↓ fusion
Dataset combiné (Parquet)
    ↓ entraînement
Réseau de neurones multi-tâche
    ↓ inférence
(lat, lon, week) → [P(espèce_1), P(espèce_2), ..., P(espèce_N)]
```

### Points clés de l'architecture :

- **Grille H3 hexagonale** (Uber) — partition spatiale hiérarchique, pas de distorsion aux pôles
- **Encodage circulaire multi-harmonique** — lat/lon et semaine traités cycliquement (pas de discontinuité au 31 décembre)
- **Apprentissage multi-tâche** — reconstruction environnementale comme signal auxiliaire
- **Pas de données environnementales nécessaires à l'inférence** — le modèle encode les patterns spatiaux implicitement

## 3. Licence — Compatible !

| Composant | Licence |
|-----------|---------|
| Code source | **MIT** ✅ |
| Poids du modèle | CC BY-SA 4.0 (share-alike, pas NC) |

→ Code **librement réutilisable**. Modèle pré-entraîné sous SA (dérivés doivent rester SA).

## 4. Faisabilité d'un équivalent InsectNet

### Avantages décisifs :

1. **geomodel utilise déjà GBIF** — les données d'occurrence sont les mêmes que celles de notre projet Faune Autour
2. **Architecture agnostique aux espèces** — remplacer les oiseaux par les orthoptères = changer le dataset, pas le code
3. **Pipeline documenté** — le workflow GBIF → H3 → Earth Engine → entraînement est entièrement codé
4. **13 MB en inférence** — compatible Raspberry Pi, éventuellement ESP32-S3 avec PSRAM

### Ce qui change pour les insectes :

| Aspect | Oiseaux (geomodel actuel) | Orthoptères (notre version) |
|--------|--------------------------|----------------------------|
| Nombre d'espèces | ~10 000 | ~200 (européennes cibles) |
| Données GBIF | Très abondantes | Plus rares, biais géographique |
| Saisonnalité | Migration marquée | Émergence/activité thermique |
| Résolution spatiale | Continentale | Locale/régionale |
| Features clés | Climat, altitude | Température, humidité, végétation |

### Challenge spécifique : rareté des données GBIF pour les insectes

Les oiseaux ont des millions d'observations GBIF. Les orthoptères en ont beaucoup moins. Solutions :
- Utiliser **toutes** les occurrences européennes (pas seulement belges)
- Ajouter des features de température/humidité (déterminants pour l'activité des orthoptères)
- Accepter un modèle moins précis mais "good enough" pour le post-filtrage

## 5. Plan de prototype

### Phase 1 — Extraction données GBIF (1-2 jours)

```python
# Script inspiré de geomodel/data_pipeline/gbif_processing.py
# 1. Télécharger toutes les occurrences GBIF pour nos 5 espèces cibles
# 2. Filtrer : Europe, 2000-2026, coordonnées valides
# 3. Mapper sur grille H3 résolution 4-5 (~20-50 km²)
# 4. Extraire features environnementaux via Google Earth Engine
```

### Phase 2 — Entraînement (2-3 jours)

```python
# Réutiliser l'architecture geomodel telle quelle
# Remplacer la liste d'espèces : oiseaux → orthoptères
# Ajuster les hyperparamètres si nécessaire (moins d'espèces, moins de données)
```

### Phase 3 — Intégration (1-2 jours)

```python
# Post-filtre dans le pipeline InsectNet :
def filter_by_geomodel(detections, model):
    for det in detections:
        prob = model.predict(det.lat, det.lon, det.week)
        if prob[det.species] < threshold:  # ex: 0.1
            det.confidence *= 0.1  # pénalité
```

## 6. Estimation de réduction des faux positifs

Basé sur la littérature BirdNET (geomodel réduit les FP de 20-40% pour les oiseaux) :

| Scénario | Réduction FP attendue |
|----------|----------------------|
| Cas idéal (données GBIF abondantes) | 30-40% |
| Cas réaliste (orthoptères, données plus rares) | 15-25% |
| Cas minimal (quelques centaines d'observations) | 10-15% |

## 7. Recommandation Clio

**Verdict : GO pour prototypage.** Le code geomodel est MIT, utilise déjà GBIF, et l'architecture est agnostique aux espèces. Le principal risque est la rareté des données GBIF pour les orthoptères, mais même un modèle "faible" réduira significativement les faux positifs.

**Actions :**
1. [Clio] Télécharger les occurrences GBIF pour nos 5 espèces cibles + top 20 européennes
2. [Clio] Fork geomodel, remplacer la liste d'espèces, ré-entraîner
3. [Clio] Mesurer la réduction de FP sur notre dataset de test InsectNet V0.1
4. [Forge] Intégrer le post-filtre dans le pipeline d'inférence

**Dépendance :** Accès Google Earth Engine (compte Google requis, gratuit pour usage recherche).

---

*Ce rapport remplace le livrable de l'agent Clio (échec technique).*
