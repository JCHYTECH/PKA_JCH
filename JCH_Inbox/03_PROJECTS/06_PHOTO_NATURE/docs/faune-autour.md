---
tags:
  - type/project
  - status/active
---
# Faune Autour — Dossier de projet
*Synthèse · Avril 2026*

---

## 1. Concept

Application mobile-first (PWA) affichant les animaux observés autour de la position GPS de l'utilisateur. Données issues de GBIF (Global Biodiversity Information Facility), qui agrège notamment les observations de [[observations.be]] / [[waarnemingen.be]].

**URL de production :** https://jchytech.github.io/faune-autour/faune-autour.html
**Hébergement :** GitHub Pages (repository `jchytech/faune-autour`)
**Format :** fichier HTML unique — pas de serveur, pas de dépendances externes hormis Leaflet (CDN cdnjs)

---

## 2. Historique des contacts API

**[[Natagora]] ([[observations.be]])** — contacté, pas de réponse.

**Observation International (observation.org)** — contacté à info@observation.org. Réponse de Nicoliene :
> "Our internal API is currently intended for use in our own applications and for business partners involved in funded projects. We redirect external developers to GBIF."

**Conclusion :** API interne fermée aux tiers individuels. GBIF est la voie officielle recommandée.

---

## 3. Source de données — GBIF

- API publique, gratuite, sans clé requise pour la lecture
- Endpoint principal : `https://api.gbif.org/v1/occurrence/search`
- Filtre géographique : polygone WKT (bounding box calculée autour du GPS)
- Filtre temporel : `eventDate` (12 mois glissants)
- Filtre taxonomique : `kingdomKey=1` (Animalia) pour le mode Explorer
- Filtre par espèce : `taxonKey` résolu via résolution en 3 étapes (voir ci-dessous)
- Données [[observations.be]] incluses dans GBIF avec délai de synchronisation (semaines à mois)

---

## 4. Architecture technique

**Stack :**
- HTML5 + CSS3 + JavaScript vanilla (pas de framework)
- Leaflet.js 1.9.4 via cdnjs.cloudflare.com
- API Wikipedia (Action API) pour les images
- GPS via `navigator.geolocation` (CoreLocation sur iPhone)

**Calculs géographiques :**
- Bounding box WKT à partir de lat/lon + rayon en km
- Distance Haversine pour afficher la distance de chaque observation

**Résolution du nom d'espèce (3 étapes) :**
1. Dictionnaire local embarqué (priorité, instantané)
2. GBIF `/species/search?vernacularName=...&language=fra` (noms français non couverts par le dict)
3. GBIF `/species/match?strict=true` (noms latins)

Seuls les rangs SPECIES / SUBSPECIES / VARIETY / FORM sont acceptés — les matchs trop larges (genre, famille, classe) sont bloqués avec message explicite.

---

## 5. Fonctionnalités actuelles (v7)

### Mode "Par espèce"
- Saisie nom français ou latin
- Autocomplétion depuis le dictionnaire local (dès 2 caractères)
- Slider rayon 1–10 km
- Résultats : liste des observations avec nom FR, nom latin, date, distance, localité
- Date de l'observation la plus récente en encadré
- Bouton "Voir sur la carte" → carte Leaflet avec tous les points
- Tap sur une carte → drawer avec photo Wikipedia + mini-carte

### Mode "Explorer autour"
- Slider rayon 1–10 km
- Sélecteur période : semaine / mois / année (12 mois max)
- Résultats groupés par classe (Oiseaux, Mammifères, Reptiles, etc.)
- Nom français en priorité (dictionnaire local en enrichissement si GBIF ne fournit pas de vernacularName)
- Nombre d'observations + date de dernière observation par espèce
- Distance calculée pour chaque espèce
- Bouton carte + drawer identiques au mode par espèce

### Drawer détail (tap sur une carte)
- Photo Wikipedia (Action API, `origin=*`, CORS-safe)
- Fallback Wikipedia FR si EN ne trouve pas d'image
- Mini-carte Leaflet centrée sur l'observation avec position utilisateur
- Fermeture par tap overlay ou bouton ✕

---

## 6. Dictionnaire local

Embarqué directement dans le HTML. ~110 entrées couvrant :
- Mammifères ([[Renard]], chevreuil, cerf, sanglier, blaireau, loutre, [[Castor]], chauves-souris...)
- Oiseaux (cigogne, [[Héron]], faucon, [[Chouette]], martin-pêcheur, hirondelle...)
- Reptiles (lézard, couleuvre, vipère, orvet...)
- Amphibiens (grenouille, crapaud, triton, salamandre...)
- Poissons (saumon, truite, brochet, anguille...)
- Insectes notables (lucane, machaon...)

**Structure :** tableau d'objets `{fr, latin}`, index bidirectionnel automatique.
**Extension :** ajouter des entrées dans `var DICT = [...]` dans le fichier HTML.

---

## 7. Versions produites

| Version | Changements principaux |
|---------|----------------------|
| v1 | Structure initiale, 2 modes, GPS, GBIF |
| v2 | Noms français, distances, carte Leaflet globale, date récente |
| v3 | Dictionnaire local + autocomplétion |
| v4 | CDN Leaflet migré sur cdnjs, carte réinitialisée proprement, 12 mois glissants |
| v5 | Drawer avec photo Wikipedia + mini-carte au tap |
| v6 | Fix tap iPhone (JSON.stringify remplacé par index _cardData) |
| v7 | Wikipedia Action API + origin=* (fix images), fallback Wikipedia FR |

---

## 8. Bugs connus et améliorations prévues

### À faire (prochaine session)
- Bouton clear (croix) sur le champ de recherche "Par espèce"
- Effacement automatique des résultats à la saisie

### Notes techniques
- Lenteur image Wikipedia : inhérente aux serveurs Wikimedia, non optimisable côté client
- Noms français GBIF : le `vernacularName` n'est pas systématiquement fourni par GBIF pour toutes les espèces — le dictionnaire local compense
- Embargo espèces rares : [[observations.be]] masque certaines localisations sensibles dans GBIF

---

## 9. Extensibilité prévue (non développée)

- **Multi-pays :** paramètre `datasetKey` GBIF prévu pour filtrer par dataset national
- **Multi-langues :** structure dictionnaire extensible (ajouter champ `nl`, `de`...)
- **Intégration apps tierces :** [[BirdNET]], Collins Bird Guide — architecture URL-scheme à définir
- **App native iOS :** si adoption large, migration Swift/SwiftUI possible ultérieurement

---

*Fichier généré le 15 avril 2026 · Faune Autour · jchytech.github.io*
