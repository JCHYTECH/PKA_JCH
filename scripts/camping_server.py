#!/usr/bin/env python3
"""
camping_server.py — Serveur Flask mobile pour spots nuit van
PKA_JCH / Dobby

Usage :
    python3 scripts/camping_server.py
    → http://localhost:5000  (ou http://[IP-RPi]:5000 depuis le téléphone)

Dépendances :
    pip install flask requests geopy
"""

import json
import re
import time
from pathlib import Path

from flask import Flask, jsonify, render_template_string, request
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import requests as req

app = Flask(__name__)

# Cache simple : évite de spammer Overpass
_cache: dict = {}  # key=(lat_r,lng_r,radius) → {ts, results, reserves}
CACHE_TTL = 600    # 10 minutes

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
]

SOURCE_COLORS = {
    "OSM-camping":   "#27ae60",
    "OSM-motorhome": "#2ecc71",
    "OSM-ferme":     "#f39c12",
    "park4night":    "#e74c3c",
    "campspace":     "#3498db",
    "france-passion":"#9b59b6",
}


# ── Backend ───────────────────────────────────────────────────────────────────

def dist_km(lat1, lng1, lat2, lng2) -> float:
    return round(geodesic((lat1, lng1), (lat2, lng2)).km, 1)


def parse_osm_price(tags: dict) -> str:
    charge = tags.get("charge") or ""
    fee = tags.get("fee", "")
    if charge:
        charge = re.sub(r"(?i)\beur\b", "€", charge.strip())
        charge = re.sub(r"(?i)per night|par nuit|/night", "/nuit", charge)
        return f"~{charge}" if not charge.startswith("~") else charge
    if fee == "no":
        return "Gratuit"
    if fee == "donation":
        return "Libre"
    if fee == "yes":
        return "Payant"
    return ""


def overpass_query(query: str) -> dict | None:
    for mirror in OVERPASS_MIRRORS:
        try:
            r = req.post(
                mirror,
                data={"data": query},
                headers={"User-Agent": "camping_scout_pka/2.0"},
                timeout=20,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None


def fetch_spots(center_lat: float, center_lng: float, radius_km: int) -> tuple[list, list]:
    """Retourne (spots, reserves). Utilise le cache si disponible."""
    lat_r = round(center_lat, 3)
    lng_r = round(center_lng, 3)
    key = (lat_r, lng_r, radius_km)

    if key in _cache and (time.time() - _cache[key]["ts"]) < CACHE_TTL:
        return _cache[key]["results"], _cache[key]["reserves"]

    radius_m = radius_km * 1000
    reserve_m = radius_km * 2 * 1000

    query = f"""
[out:json][timeout:25];
(
  node["tourism"="camp_site"](around:{radius_m},{center_lat},{center_lng});
  way["tourism"="camp_site"](around:{radius_m},{center_lat},{center_lng});
  node["tourism"="caravan_site"](around:{radius_m},{center_lat},{center_lng});
  way["tourism"="caravan_site"](around:{radius_m},{center_lat},{center_lng});
  node["amenity"="parking"]["motorhome"="yes"](around:{radius_m},{center_lat},{center_lng});
  way["amenity"="parking"]["motorhome"="yes"](around:{radius_m},{center_lat},{center_lng});
  node["leisure"="nature_reserve"](around:{reserve_m},{center_lat},{center_lng});
  way["leisure"="nature_reserve"](around:{reserve_m},{center_lat},{center_lng});
);
out center;
"""
    data = overpass_query(query)
    if not data:
        return [], []

    results, reserves = [], []

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        if not tags:
            continue

        lat = el.get("lat") if el["type"] == "node" else el.get("center", {}).get("lat")
        lng = el.get("lon") if el["type"] == "node" else el.get("center", {}).get("lon")
        if not lat or not lng:
            continue

        name = tags.get("name") or tags.get("name:fr") or "(sans nom)"
        leisure = tags.get("leisure", "")
        tourism = tags.get("tourism", "")
        amenity = tags.get("amenity", "")

        if leisure == "nature_reserve":
            reserves.append({"name": name, "lat": lat, "lng": lng})
            continue

        source = "OSM-camping" if tourism in ("camp_site", "caravan_site") else "OSM-motorhome"
        spot_type = "Camping / Aire CC" if source == "OSM-camping" else "Parking motorhome"

        services = []
        if tags.get("sanitary_dump_station") == "yes": services.append("vidange")
        if tags.get("water_point") == "yes" or tags.get("drinking_water") == "yes": services.append("eau")
        if tags.get("electricity") == "yes": services.append("élec")
        if tags.get("shower") == "yes": services.append("douches")

        stars = tags.get("stars", "")

        results.append({
            "name": name,
            "source": source,
            "type": spot_type,
            "lat": lat,
            "lng": lng,
            "url_osm": f"https://www.openstreetmap.org/{el['type']}/{el['id']}",
            "services": ", ".join(services),
            "price": parse_osm_price(tags),
            "rating": f"★{stars}" if stars else "",
        })

    # Scoring JCH
    for spot in results:
        score = 5
        nearest_r = ""
        for rv in reserves:
            d = dist_km(spot["lat"], spot["lng"], rv["lat"], rv["lng"])
            if d < 3:
                score = min(10, score + 4)
                nearest_r = f"{rv['name'][:30]} ({d} km)"
                break
            elif d < 8:
                score = min(10, score + 2)
                if not nearest_r:
                    nearest_r = f"{rv['name'][:30]} ({d} km)"
        spot["jch_score"] = score
        spot["reserve_nearby"] = nearest_r

    _cache[key] = {"ts": time.time(), "results": results, "reserves": reserves}
    return results, reserves


# ── Routes ────────────────────────────────────────────────────────────────────

@app.route("/api/search")
def api_search():
    try:
        lat = float(request.args["lat"])
        lng = float(request.args["lng"])
        radius = int(request.args.get("radius", 10))
        radius = max(2, min(radius, 30))
    except (KeyError, ValueError):
        return jsonify({"error": "Paramètres invalides"}), 400

    spots, reserves = fetch_spots(lat, lng, radius)

    # Trier par distance depuis la position courante
    for s in spots:
        s["distance_km"] = dist_km(lat, lng, s["lat"], s["lng"])
    spots_sorted = sorted(spots, key=lambda x: x["distance_km"])

    return jsonify({
        "spots": spots_sorted,
        "reserves": reserves,
        "center": {"lat": lat, "lng": lng},
        "count": len(spots_sorted),
        "cached": True,  # simplifié
    })


@app.route("/api/geocode")
def api_geocode():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"error": "Paramètre q manquant"}), 400
    try:
        geolocator = Nominatim(user_agent="camping_scout_pka/2.0")
        result = geolocator.geocode(q + ", France", timeout=8)
        if not result:
            result = geolocator.geocode(q, timeout=8)
        if result:
            return jsonify({"lat": result.latitude, "lng": result.longitude, "name": result.address})
        return jsonify({"error": "Lieu introuvable"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def index():
    return render_template_string(HTML_APP)


# ── Interface mobile ──────────────────────────────────────────────────────────

HTML_APP = """<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="theme-color" content="#1a1a2e">
<title>Camping Scout</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
:root {
  --ink: #1a1a2e;
  --accent: #C17F3A;
  --green: #27ae60;
  --bg: #f5f4f0;
  --card: #ffffff;
  --muted: #888;
  --radius: 12px;
}
* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }
html, body { height: 100%; font-family: -apple-system, 'SF Pro Text', sans-serif; background: var(--bg); color: var(--ink); }

/* Header */
.header {
  background: var(--ink);
  color: white;
  padding: 12px 16px 10px;
  display: flex;
  align-items: center;
  gap: 10px;
  position: sticky;
  top: 0;
  z-index: 1000;
}
.header h1 { font-size: 1em; font-weight: 600; flex: 1; }
.status-dot { width: 8px; height: 8px; border-radius: 50%; background: #e74c3c; flex-shrink: 0; }
.status-dot.active { background: var(--green); animation: pulse 2s infinite; }
@keyframes pulse { 0%,100%{opacity:1} 50%{opacity:.5} }

/* Controls */
.controls {
  background: white;
  padding: 10px 16px;
  border-bottom: 1px solid #e8e4dc;
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.search-row {
  display: flex;
  gap: 8px;
}
.search-input {
  flex: 1;
  border: 1.5px solid #ddd;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 0.9em;
  outline: none;
}
.search-input:focus { border-color: var(--accent); }
.btn {
  background: var(--accent);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.85em;
  font-weight: 600;
  cursor: pointer;
  white-space: nowrap;
}
.btn:active { opacity: 0.8; }
.btn-gps {
  background: var(--ink);
  display: flex;
  align-items: center;
  gap: 5px;
}
.slider-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.82em;
  color: var(--muted);
}
.slider-row input[type=range] {
  flex: 1;
  accent-color: var(--accent);
  height: 4px;
}
.slider-val {
  color: var(--ink);
  font-weight: 600;
  min-width: 40px;
}

/* Map */
#map { height: 38vh; width: 100%; }

/* Results */
.results-header {
  padding: 8px 16px;
  font-size: 0.78em;
  color: var(--muted);
  background: var(--bg);
  border-bottom: 1px solid #e8e4dc;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.results-header strong { color: var(--ink); }

.spot-list {
  overflow-y: auto;
  padding: 10px 12px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.spot-card {
  background: var(--card);
  border-radius: var(--radius);
  padding: 12px 14px;
  border-left: 4px solid var(--green);
  box-shadow: 0 1px 4px rgba(0,0,0,.06);
}
.spot-card.score-high { border-left-color: #27ae60; }
.spot-card.score-mid  { border-left-color: #f39c12; }
.spot-card.score-low  { border-left-color: #bdc3c7; }

.spot-top {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 5px;
}
.spot-name {
  font-size: 0.92em;
  font-weight: 600;
  line-height: 1.3;
  flex: 1;
}
.spot-score {
  font-size: 0.72em;
  font-weight: 700;
  background: var(--ink);
  color: var(--accent);
  padding: 2px 7px;
  border-radius: 10px;
  white-space: nowrap;
  flex-shrink: 0;
}

.spot-meta {
  font-size: 0.78em;
  color: var(--muted);
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 6px;
}
.spot-meta span { display: flex; align-items: center; gap: 3px; }

.spot-reserve {
  font-size: 0.75em;
  color: #1abc9c;
  margin-bottom: 7px;
}

.spot-actions {
  display: flex;
  gap: 7px;
}
.btn-maps {
  background: #4285F4;
  color: white;
  border: none;
  border-radius: 7px;
  padding: 6px 12px;
  font-size: 0.78em;
  font-weight: 600;
  cursor: pointer;
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  text-decoration: none;
}
.btn-osm {
  background: #f0ede8;
  color: var(--ink);
  border: none;
  border-radius: 7px;
  padding: 6px 12px;
  font-size: 0.78em;
  cursor: pointer;
  text-decoration: none;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Loader */
.loader {
  display: none;
  text-align: center;
  padding: 30px;
  color: var(--muted);
  font-size: 0.85em;
}
.loader.visible { display: block; }
.spinner {
  width: 24px; height: 24px;
  border: 3px solid #eee;
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin .8s linear infinite;
  margin: 0 auto 10px;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty {
  display: none;
  text-align: center;
  padding: 30px 20px;
  color: var(--muted);
  font-size: 0.85em;
}
.empty.visible { display: block; }
</style>
</head>
<body>

<div class="header">
  <div class="status-dot" id="gps-dot"></div>
  <h1>🏕️ Camping Scout</h1>
  <span id="gps-label" style="font-size:.75em;opacity:.6">GPS…</span>
</div>

<div class="controls">
  <div class="search-row">
    <input class="search-input" id="search-input" type="text" placeholder="Lieu (ex: Honfleur)…" autocomplete="off">
    <button class="btn" onclick="searchByName()">Chercher</button>
    <button class="btn btn-gps" onclick="useGPS()">📍 Ici</button>
  </div>
  <div class="slider-row">
    <span>Rayon</span>
    <input type="range" id="radius-slider" min="2" max="25" value="10" step="1"
           oninput="onRadiusChange(this.value)">
    <span class="slider-val"><span id="radius-val">10</span> km</span>
  </div>
</div>

<div id="map"></div>

<div class="results-header">
  <span>Spots — triés par distance</span>
  <strong id="count-label">—</strong>
</div>

<div class="loader" id="loader">
  <div class="spinner"></div>
  Recherche en cours…
</div>
<div class="empty" id="empty">Aucun spot trouvé dans ce rayon.</div>

<div class="spot-list" id="spot-list"></div>

<script>
// ── État ──────────────────────────────────────────────────────────────────
let currentLat = null, currentLng = null;
let watchId = null;
let lastQueryLat = null, lastQueryLng = null, lastQueryRadius = null;
let lastQueryTs = 0;
let mapInstance = null;
let myMarker = null;
let spotMarkers = [];
let reserveMarkers = [];
const MIN_MOVE_M = 300;    // re-requête si déplacé de > 300m
const MIN_INTERVAL_S = 30; // pas plus d'une requête toutes les 30s

// ── Carte ─────────────────────────────────────────────────────────────────
function initMap(lat, lng) {
  if (mapInstance) {
    mapInstance.setView([lat, lng], 12);
    return;
  }
  mapInstance = L.map('map', { zoomControl: true }).setView([lat, lng], 12);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap'
  }).addTo(mapInstance);
}

function updateMyMarker(lat, lng) {
  if (!mapInstance) initMap(lat, lng);
  if (myMarker) {
    myMarker.setLatLng([lat, lng]);
  } else {
    myMarker = L.circleMarker([lat, lng], {
      radius: 8, color: 'white', fillColor: '#e74c3c',
      fillOpacity: 1, weight: 2.5
    }).bindTooltip('Vous êtes ici', { permanent: false }).addTo(mapInstance);
  }
}

function clearMapSpots() {
  spotMarkers.forEach(m => m.remove());
  reserveMarkers.forEach(m => m.remove());
  spotMarkers = [];
  reserveMarkers = [];
}

const SRC_COLORS = {
  'OSM-camping': '#27ae60',
  'OSM-motorhome': '#2ecc71',
  'OSM-ferme': '#f39c12',
  'park4night': '#e74c3c',
  'campspace': '#3498db',
  'france-passion': '#9b59b6',
};

function addSpotsToMap(spots, reserves) {
  clearMapSpots();

  reserves.forEach(rv => {
    const m = L.circleMarker([rv.lat, rv.lng], {
      radius: 9, color: '#1abc9c', fillColor: '#1abc9c',
      fillOpacity: 0.2, weight: 2, dashArray: '4,3'
    }).bindPopup(`<b>🌿 ${rv.name}</b><br><small>Réserve naturelle</small>`);
    m.addTo(mapInstance);
    reserveMarkers.push(m);
  });

  spots.forEach(s => {
    const color = SRC_COLORS[s.source] || '#888';
    const popup = `
      <b>${s.name}</b><br>
      <small>${s.type}</small><br>
      📏 ${s.distance_km} km
      ${s.price ? ' · ' + s.price : ''}
      ${s.reserve_nearby ? '<br>🌿 ' + s.reserve_nearby : ''}
      <br><a href="${googleMapsUrl(s.lat, s.lng)}" target="_blank">Google Maps →</a>
    `;
    const m = L.circleMarker([s.lat, s.lng], {
      radius: 7, color: 'white', fillColor: color, fillOpacity: 0.9, weight: 1.5
    }).bindPopup(popup);
    m.addTo(mapInstance);
    spotMarkers.push(m);
  });
}

// ── GPS ───────────────────────────────────────────────────────────────────
function startGPSWatch() {
  if (!navigator.geolocation) return;
  watchId = navigator.geolocation.watchPosition(
    pos => onPosition(pos.coords.latitude, pos.coords.longitude),
    err => console.warn('GPS:', err.message),
    { enableHighAccuracy: true, maximumAge: 10000, timeout: 15000 }
  );
}

function onPosition(lat, lng) {
  currentLat = lat;
  currentLng = lng;
  document.getElementById('gps-dot').classList.add('active');
  document.getElementById('gps-label').textContent =
    lat.toFixed(4) + ', ' + lng.toFixed(4);
  updateMyMarker(lat, lng);
  maybeAutoRefresh(lat, lng);
}

function maybeAutoRefresh(lat, lng) {
  const radius = parseInt(document.getElementById('radius-slider').value);
  const now = Date.now() / 1000;

  if (lastQueryLat !== null) {
    const moved = geodistM(lat, lng, lastQueryLat, lastQueryLng);
    const elapsed = now - lastQueryTs;
    if (moved < MIN_MOVE_M && elapsed < MIN_INTERVAL_S * 4) return;
    if (elapsed < MIN_INTERVAL_S) return;
  }
  doSearch(lat, lng, radius);
}

function geodistM(lat1, lng1, lat2, lng2) {
  const R = 6371000;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lat2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) *
            Math.cos(lat2*Math.PI/180) * Math.sin(dLng/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// ── Actions UI ────────────────────────────────────────────────────────────
function useGPS() {
  if (currentLat) {
    doSearch(currentLat, currentLng,
             parseInt(document.getElementById('radius-slider').value));
    mapInstance?.setView([currentLat, currentLng], 12);
  } else {
    navigator.geolocation?.getCurrentPosition(
      pos => {
        onPosition(pos.coords.latitude, pos.coords.longitude);
        doSearch(pos.coords.latitude, pos.coords.longitude,
                 parseInt(document.getElementById('radius-slider').value));
      },
      () => alert('GPS indisponible — utilise la recherche par lieu.')
    );
  }
}

async function searchByName() {
  const q = document.getElementById('search-input').value.trim();
  if (!q) return;
  showLoader();
  try {
    const r = await fetch('/api/geocode?q=' + encodeURIComponent(q));
    const data = await r.json();
    if (data.error) { alert(data.error); hideLoader(); return; }
    initMap(data.lat, data.lng);
    mapInstance.setView([data.lat, data.lng], 12);
    doSearch(data.lat, data.lng,
             parseInt(document.getElementById('radius-slider').value));
  } catch(e) { alert('Erreur réseau'); hideLoader(); }
}

let radiusTimer = null;
function onRadiusChange(val) {
  document.getElementById('radius-val').textContent = val;
  clearTimeout(radiusTimer);
  radiusTimer = setTimeout(() => {
    if (currentLat) doSearch(currentLat, currentLng, parseInt(val));
  }, 600);
}

function searchEnter(e) {
  if (e.key === 'Enter') searchByName();
}
document.getElementById('search-input').addEventListener('keydown', searchEnter);

// ── Requête API ───────────────────────────────────────────────────────────
async function doSearch(lat, lng, radius) {
  showLoader();
  lastQueryLat = lat;
  lastQueryLng = lng;
  lastQueryRadius = radius;
  lastQueryTs = Date.now() / 1000;

  try {
    const url = `/api/search?lat=${lat}&lng=${lng}&radius=${radius}`;
    const r = await fetch(url);
    const data = await r.json();
    hideLoader();
    renderResults(data.spots || [], data.reserves || []);
    addSpotsToMap(data.spots || [], data.reserves || []);
  } catch(e) {
    hideLoader();
    alert('Erreur réseau — vérifie ta connexion.');
  }
}

// ── Rendu résultats ───────────────────────────────────────────────────────
function googleMapsUrl(lat, lng) {
  return `https://maps.google.com/?daddr=${lat},${lng}`;
}

function scoreClass(s) {
  if (s >= 8) return 'score-high';
  if (s >= 5) return 'score-mid';
  return 'score-low';
}

function renderResults(spots, reserves) {
  const list = document.getElementById('spot-list');
  const countLabel = document.getElementById('count-label');
  const empty = document.getElementById('empty');

  countLabel.textContent = spots.length ? `${spots.length} spots` : '—';

  if (!spots.length) {
    list.innerHTML = '';
    empty.classList.add('visible');
    return;
  }
  empty.classList.remove('visible');

  list.innerHTML = spots.map(s => `
    <div class="spot-card ${scoreClass(s.jch_score)}">
      <div class="spot-top">
        <div class="spot-name">${s.name}</div>
        <div class="spot-score">★ ${s.jch_score}/10</div>
      </div>
      <div class="spot-meta">
        <span>📏 ${s.distance_km} km</span>
        ${s.price ? `<span>💶 ${s.price}</span>` : ''}
        ${s.services ? `<span>🔧 ${s.services}</span>` : ''}
        ${s.rating ? `<span>${s.rating}</span>` : ''}
      </div>
      ${s.reserve_nearby ? `<div class="spot-reserve">🌿 ${s.reserve_nearby}</div>` : ''}
      <div class="spot-actions">
        <a class="btn-maps" href="${googleMapsUrl(s.lat, s.lng)}" target="_blank">
          Google Maps →
        </a>
        <a class="btn-osm" href="${s.url_osm}" target="_blank">OSM</a>
      </div>
    </div>
  `).join('');
}

function showLoader() {
  document.getElementById('loader').classList.add('visible');
  document.getElementById('spot-list').innerHTML = '';
  document.getElementById('empty').classList.remove('visible');
}
function hideLoader() {
  document.getElementById('loader').classList.remove('visible');
}

// ── Init ──────────────────────────────────────────────────────────────────
initMap(46.5, 2.5);  // France centre par défaut
startGPSWatch();
</script>
</body>
</html>
"""

if __name__ == "__main__":
    import socket
    hostname = socket.gethostname()
    try:
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "127.0.0.1"

    print(f"\n🏕️  Camping Scout — serveur démarré")
    print(f"   Local   : http://localhost:5050")
    print(f"   Réseau  : http://{local_ip}:5050  ← depuis le téléphone")
    print(f"\n   Sur RPi : accède depuis ton iPhone via l'IP ci-dessus")
    print(f"   Ctrl+C  : arrêter\n")

    app.run(host="0.0.0.0", port=5050, debug=False)
