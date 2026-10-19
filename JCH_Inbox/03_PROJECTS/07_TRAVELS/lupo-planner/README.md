# Lupo Planner 🐺 — PWA de planification de roadtrips

> Projet créé par Dobby 🦉 — 2026-07-08
> Dossier : `JCH_Inbox/03_PROJECTS/07_TRAVELS/lupo-planner/`

---

## Concept

Une web app (PWA) qui unifie la recherche de spots de bivouac pour Lupo. Au lieu de jongler entre 8 applis (park4night, France Passion, Campspace, Huttopia, Campercontact, iOverlander…), tu ajoutes tes spots favoris manuellement (copier-coller des coordonnées) et tu les retrouves tous sur **une carte unique**, filtrable par pays, type, et priorité.

---

## Architecture

```
index.html          → Appli complète (HTML + CSS + JS vanilla, 754 lignes)
manifest.json       → PWA installable sur écran d'accueil
sw.js               → Service worker — cache offline (assets + tuiles OSM)
deploy.sh           → Script de déploiement (dev / HA / RPi)
```

- **Frontend** : Vanilla JS, Leaflet.js 1.9.4 (CDN), OpenStreetMap
- **Stockage** : IndexedDB (local, persistant, pas de backend)
- **Offline** : Service worker avec stratégie network-first pour les tuiles
- **Sync multi-device** : Export/Import JSON

---

## Fonctionnalités

### Carte
- Leaflet + OpenStreetMap, centrée sur l'Europe
- 6 pays : 🇫🇷 🇪🇸 🇮🇹 🇩🇪 🇧🇪 🇳🇱
- Marqueurs colorés par type de spot
- Popup avec nom, type, pays, coordonnées
- Clic sur la carte → remplit automatiquement les coordonnées du formulaire

### Spots
- Ajout : nom, GPS (lat/lng), type, pays, source, notes
- 6 types alignés sur priorités JC :
  - 🥇 Sauvage (rouge)
  - 🥈 Privé / Ferme (orange)
  - 🥉 Camping isolé (vert)
  - 🏕️ Camping (gris)
  - 🅿️ Aire (bleu)
  - 🏛️ POI / Visite (violet)
- Sources : park4night, France Passion, Campspace, Huttopia, Campercontact, iOverlander, Landvergnügen, Agricamper, España Discovery, autre
- Filtrage : par pays, type, recherche texte
- Favoris ★
- Marqué comme visité (opacité réduite)
- Édition et suppression

### Roadtrips
- Groupes de spots ordonnés (itinéraire)
- Visualisation sur la carte
- Création, modification, suppression

### Import / Export
- Export JSON (spots + roadtrips)
- Import JSON (fusion)
- Permet la synchro entre téléphone et laptop

---

## Déploiement

### Local (dev)
```bash
[M5] cd JCH_Inbox/03_PROJECTS/07_TRAVELS/lupo-planner
[M5] ./deploy.sh dev
# → http://localhost:8088
```

### Home Assistant (quand le RPi 5 sera monté dans Lupo)
```bash
[M5] cd JCH_Inbox/03_PROJECTS/07_TRAVELS/lupo-planner
[M5] ./deploy.sh ha
# → http://homeassistant.local:8123/local/lupo-planner/
# → Accessible dans le van, offline, via Tailscale
```

### RPi standalone
```bash
[M5] cd JCH_Inbox/03_PROJECTS/07_TRAVELS/lupo-planner
[M5] ./deploy.sh rpi
# → http://<rpi-ip>:8088
```

### Installation PWA sur téléphone
1. Ouvrir l'URL dans Safari (iOS) ou Chrome (Android)
2. « Ajouter à l'écran d'accueil »
3. L'icône 🐺 apparaît, l'appli s'ouvre en plein écran

---

## Data model

```js
spot = {
  id: uuid,
  name: string,
  lat: number, lng: number,
  type: 'sauvage' | 'prive' | 'camping_isole' | 'camping' | 'aire' | 'poi',
  country: 'FR' | 'ES' | 'IT' | 'DE' | 'BE' | 'NL',
  source: 'park4night' | 'france_passion' | 'campspace' | 'huttopia' |
          'campercontact' | 'ioverlander' | 'landvergnugen' |
          'agricamper' | 'espana_discovery' | 'other',
  notes: string,
  visited: boolean,
  favorite: boolean,
  createdAt: timestamp
}

roadtrip = {
  id: uuid,
  name: string,
  spotIds: [uuid],    // ordonné = itinéraire
  createdAt: timestamp
}
```

---

## Roadmap future

- [ ] Drag & drop pour réordonner les spots dans un roadtrip
- [ ] Import direct depuis URL park4night (scraping coordonnées)
- [ ] Calcul d'itinéraire entre spots (OSRM)
- [ ] Tuiles 100% offline (pré-téléchargement de zones)
- [ ] Intégration météo Windy dans la popup spot
- [ ] Dashboard Home Assistant (iframe panel)
- [ ] Synchronisation automatique via Tailscale/Syncthing

---

## Contexte

Voir aussi :
- `apps-roadtrip-lupo.md` — synthèse des apps/plateformes de bivouac par pays
- `fiche-technique-lupo-kelsey.md` — fiche technique du van
- `securite-van-lupo.md` — plan sécurité Lupo
