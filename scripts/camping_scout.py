#!/usr/bin/env python3
"""
camping_scout.py v2 — Recherche multi-sources de spots nuit en van
Auteur : Dobby / PKA_JCH

Architecture deux niveaux :
  Niveau 1 (toujours, sans navigateur) :
    - Overpass/OSM : campings, aires motorhome, fermes accueil, réserves naturelles
  Niveau 2 (optionnel, Playwright) :
    - park4night, campspace, france-passion, bienvenue-a-la-ferme

Usage :
    python3 camping_scout.py --location "Le Crotoy" --radius 15
    python3 camping_scout.py --location "Bayeux" --radius 20 --quick
    python3 camping_scout.py --location "Bayeux" --radius 20 --fp-user x --fp-pass y
    python3 camping_scout.py --location "Honfleur" --radius 15 --save

Dépendances :
    pip install requests geopy                     # niveau 1 seulement
    pip install playwright && playwright install chromium  # niveau 2
"""

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.parse
from datetime import datetime
from pathlib import Path

# ── Dépendances Niveau 1 ──────────────────────────────────────────────────────
try:
    import requests
    from geopy.geocoders import Nominatim
    from geopy.distance import geodesic
except ImportError:
    print("Dépendances manquantes. Installe :")
    print("  pip install requests geopy")
    sys.exit(1)

# ── Constantes ────────────────────────────────────────────────────────────────
PKA_ROOT = Path(__file__).parent.parent
PREFERENCES_PATH = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/PREFERENCES.md"
DEST_DIR = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/destinations"

HEADERS = {
    "name": "Nom",
    "source": "Source",
    "type": "Type",
    "address": "Adresse",
    "distance_km": "Distance (km)",
    "lat": "Latitude",
    "lng": "Longitude",
    "url": "URL",
    "description": "Description",
    "services": "Services",
    "price": "Prix",
    "rating": "Note",
    "jch_score": "Score JCH",
    "reserve_nearby": "Réserve proche",
}

SOURCE_COLORS = {
    "OSM-camping":      "#27ae60",
    "OSM-motorhome":    "#2ecc71",
    "OSM-ferme":        "#f39c12",
    "park4night":       "#e74c3c",
    "campspace":        "#3498db",
    "france-passion":   "#9b59b6",
    "bienvenue-ferme":  "#e67e22",
    "reserve-naturelle":"#1abc9c",
}

OVERPASS_MIRRORS = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://maps.mail.ru/osm/tools/overpass/api/interpreter",
]

# ── Utilitaires ───────────────────────────────────────────────────────────────

def geocode(location: str) -> tuple[float, float]:
    geolocator = Nominatim(user_agent="camping_scout_pka/2.0")
    for suffix in [", France", ", Europe", ""]:
        result = geolocator.geocode(location + suffix, timeout=10)
        if result:
            print(f"  📍 {location} → {result.latitude:.4f}, {result.longitude:.4f}")
            return result.latitude, result.longitude
    raise ValueError(f"Impossible de géocoder : {location}")


def dist_km(lat1, lng1, lat2, lng2) -> float:
    return round(geodesic((lat1, lng1), (lat2, lng2)).km, 1)


def overpass_query(query: str, timeout: int = 20) -> dict | None:
    """Requête Overpass avec fallback sur plusieurs mirrors."""
    for mirror in OVERPASS_MIRRORS:
        try:
            r = requests.post(
                mirror,
                data={"data": query},
                headers={"User-Agent": "camping_scout_pka/2.0"},
                timeout=timeout,
            )
            if r.status_code == 200:
                return r.json()
        except Exception:
            continue
    return None


def safe_text(page, selector: str, default: str = "") -> str:
    try:
        el = page.query_selector(selector)
        return el.inner_text().strip() if el else default
    except Exception:
        return default


# ── Scoring JCH ───────────────────────────────────────────────────────────────

def compute_jch_score(spot: dict, reserves: list) -> tuple[int, str]:
    """
    Score de pertinence pour JCH (photo wildlife, réserves, aube/crépuscule).
    Retourne (score 0-10, nom réserve proche ou '').
    """
    score = 5
    nearby_reserve = ""

    # Proximité réserve naturelle (priorité JCH)
    lat = spot.get("lat")
    lng = spot.get("lng")
    if lat and lng:
        try:
            lat_f, lng_f = float(lat), float(lng)
            for r in reserves:
                d = dist_km(lat_f, lng_f, r["lat"], r["lng"])
                if d < 3:
                    score = min(10, score + 4)
                    nearby_reserve = f'{r["name"]} ({d} km)'
                    break
                elif d < 8:
                    score = min(10, score + 2)
                    if not nearby_reserve:
                        nearby_reserve = f'{r["name"]} ({d} km)'
        except (ValueError, TypeError):
            pass

    # Bonus type spot
    stype = spot.get("type", "")
    if "réserve" in stype.lower() or "nature" in stype.lower():
        score = min(10, score + 2)
    if "ferme" in stype.lower() or "passion" in spot.get("source", ""):
        score = min(10, score + 1)

    # Malus si distance > 15 km du centre
    try:
        d = float(spot.get("distance_km", 99))
        if d > 15:
            score = max(0, score - 1)
        if d > 20:
            score = max(0, score - 1)
    except (ValueError, TypeError):
        pass

    return score, nearby_reserve


# ── Prix ─────────────────────────────────────────────────────────────────────

def parse_osm_price(tags: dict) -> str:
    """Normalise les tags OSM de prix en texte lisible."""
    charge = tags.get("charge") or tags.get("fee:charge") or ""
    fee = tags.get("fee", "")
    fee_cond = tags.get("fee:conditional", "")

    if charge:
        # Nettoyer : "10 EUR per night" → "~10€/nuit", "5.00 EUR" → "~5€"
        charge = charge.strip()
        charge = re.sub(r"(?i)\beur\b", "€", charge)
        charge = re.sub(r"(?i)\bper night\b|\bpar nuit\b|/night", "/nuit", charge)
        charge = re.sub(r"(?i)\bper person\b|\bpar personne\b", "/pers", charge)
        return f"~{charge}" if not charge.startswith("~") else charge

    if fee == "no":
        return "Gratuit"
    if fee == "donation":
        return "Libre (donation)"
    if fee == "yes":
        if fee_cond:
            return f"Payant ({fee_cond[:40]})"
        return "Payant"
    if fee == "interval":
        return "Payant (durée)"
    if fee:
        return fee  # valeur non standard, on la retourne telle quelle

    return ""


# ── Niveau 1 — Overpass/OSM ───────────────────────────────────────────────────

def fetch_osm_spots(center_lat: float, center_lng: float, radius_km: int, results: list) -> list:
    """
    Requête Overpass pour campings, aires motorhome, fermes, et réserves naturelles.
    Retourne la liste des réserves naturelles trouvées (pour scoring JCH).
    """
    print("\n🔍 Overpass/OSM...")
    radius_m = radius_km * 1000
    reserve_radius_m = radius_km * 2 * 1000

    query = f"""
[out:json][timeout:25];
(
  node["tourism"="camp_site"](around:{radius_m},{center_lat},{center_lng});
  way["tourism"="camp_site"](around:{radius_m},{center_lat},{center_lng});
  node["tourism"="caravan_site"](around:{radius_m},{center_lat},{center_lng});
  way["tourism"="caravan_site"](around:{radius_m},{center_lat},{center_lng});
  node["amenity"="parking"]["motorhome"="yes"](around:{radius_m},{center_lat},{center_lng});
  way["amenity"="parking"]["motorhome"="yes"](around:{radius_m},{center_lat},{center_lng});
  node["tourism"="camp_pitch"]["motorhome"="yes"](around:{radius_m},{center_lat},{center_lng});
  node["leisure"="nature_reserve"](around:{reserve_radius_m},{center_lat},{center_lng});
  way["leisure"="nature_reserve"](around:{reserve_radius_m},{center_lat},{center_lng});
  node["boundary"="protected_area"](around:{reserve_radius_m},{center_lat},{center_lng});
  way["boundary"="protected_area"](around:{reserve_radius_m},{center_lat},{center_lng});
);
out center;
"""

    data = overpass_query(query)
    if not data:
        print("  ⚠️  Overpass inaccessible — résultats OSM indisponibles")
        return []

    reserves = []
    count = 0

    for el in data.get("elements", []):
        tags = el.get("tags", {})
        if not tags:
            continue

        # Coordonnées
        if el["type"] == "node":
            lat, lng = el.get("lat"), el.get("lon")
        else:
            center = el.get("center", {})
            lat, lng = center.get("lat"), center.get("lon")

        if not lat or not lng:
            continue

        name = (
            tags.get("name")
            or tags.get("name:fr")
            or "(sans nom)"
        )
        leisure = tags.get("leisure", "")
        boundary = tags.get("boundary", "")
        tourism = tags.get("tourism", "")
        amenity = tags.get("amenity", "")

        # Réserves naturelles → scoring JCH, pas dans les résultats camping
        if leisure == "nature_reserve" or boundary == "protected_area":
            reserves.append({"name": name, "lat": lat, "lng": lng})
            continue

        # Type de spot
        if tourism in ("camp_site", "caravan_site"):
            spot_type = "Camping / Aire CC"
            source = "OSM-camping"
        elif amenity == "parking" and tags.get("motorhome") == "yes":
            spot_type = "Parking motorhome"
            source = "OSM-motorhome"
        else:
            spot_type = "Spot motorhome"
            source = "OSM-motorhome"

        # Services OSM
        services_parts = []
        if tags.get("sanitary_dump_station") == "yes":
            services_parts.append("vidange")
        if tags.get("water_point") == "yes" or tags.get("drinking_water") == "yes":
            services_parts.append("eau")
        if tags.get("electricity") == "yes":
            services_parts.append("électricité")
        if tags.get("shower") == "yes":
            services_parts.append("douches")
        if tags.get("toilet") == "yes" or tags.get("toilets") == "yes":
            services_parts.append("WC")

        stars = tags.get("stars", "")
        capacity = tags.get("capacity:motorhome") or tags.get("capacity", "")

        fiche_url = f"https://www.openstreetmap.org/{el['type']}/{el['id']}"
        if tourism:
            fiche_url = f"https://www.openstreetmap.org/{el['type']}/{el['id']}"

        results.append({
            "name": name,
            "source": source,
            "type": spot_type,
            "address": tags.get("addr:full") or tags.get("addr:city") or "",
            "distance_km": str(dist_km(center_lat, center_lng, lat, lng)),
            "lat": str(lat),
            "lng": str(lng),
            "url": fiche_url,
            "description": tags.get("description") or tags.get("note") or "",
            "services": ", ".join(services_parts),
            "price": parse_osm_price(tags),
            "rating": f"★{stars}" if stars else "",
            "jch_score": "",
            "reserve_nearby": "",
        })
        count += 1

    print(f"  ✅ {count} spots OSM · {len(reserves)} réserves naturelles dans le rayon étendu")
    return reserves


# ── Niveau 2 — Playwright scrapers ───────────────────────────────────────────

def check_playwright() -> bool:
    try:
        from playwright.sync_api import sync_playwright  # noqa: F401
        return True
    except ImportError:
        return False


def scrape_park4night(page, center_lat, center_lng, radius_km, results):
    print("\n🔍 Park4Night...")
    try:
        from playwright.sync_api import TimeoutError as PWTimeout
    except ImportError:
        return

    zoom = 12 if radius_km <= 12 else 11
    url = f"https://park4night.com/fr/search?lat={center_lat}&lng={center_lng}&z={zoom}"
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(5)
    except Exception:
        print("  ⚠️  Timeout park4night")
        return

    # Tenter l'interception des données JSON via window.__NUXT__ ou similar
    nuxt_data = None
    try:
        nuxt_data = page.evaluate("() => JSON.stringify(window.__NUXT__ || window.__INITIAL_STATE__ || null)")
        if nuxt_data and len(nuxt_data) > 100:
            import json as _json
            parsed = _json.loads(nuxt_data)
            # Extraire les places si disponibles
            places = _extract_places_from_nuxt(parsed)
            if places:
                for p in places:
                    lat, lng = p.get("lat"), p.get("lng")
                    if not lat or not lng:
                        continue
                    d = dist_km(center_lat, center_lng, float(lat), float(lng))
                    if d > radius_km:
                        continue
                    results.append({
                        "name": p.get("name", "(sans nom)"),
                        "source": "park4night",
                        "type": p.get("type", "Spot"),
                        "address": p.get("city", ""),
                        "distance_km": str(d),
                        "lat": str(lat),
                        "lng": str(lng),
                        "url": f"https://park4night.com/fr/place/{p.get('id','')}",
                        "description": p.get("description", "")[:200],
                        "services": "",
                        "price": "",
                        "rating": str(p.get("note", "")),
                        "jch_score": "",
                        "reserve_nearby": "",
                    })
                print(f"  ✅ {len(places)} spots park4night (via données internes)")
                return
    except Exception:
        pass

    # Fallback : extraire liens visibles
    links = page.query_selector_all("a[href*='/fr/place/']")
    seen, count = set(), 0
    for link in links[:60]:
        try:
            href = link.get_attribute("href") or ""
            if href in seen or not href:
                continue
            seen.add(href)
            full_url = f"https://park4night.com{href}" if href.startswith("/") else href
            name = (link.get_attribute("title") or link.inner_text()[:60]).strip().replace("\n", " ")
            if not name:
                continue
            results.append({
                "name": name,
                "source": "park4night",
                "type": "Spot communautaire",
                "address": "",
                "distance_km": "?",
                "lat": "",
                "lng": "",
                "url": full_url,
                "description": "",
                "services": "",
                "price": "",
                "rating": "",
                "jch_score": "",
                "reserve_nearby": "",
            })
            count += 1
        except Exception:
            continue

    if count == 0:
        results.append({
            "name": f"[Voir manuellement park4night — {radius_km}km]",
            "source": "park4night",
            "type": "",
            "address": "",
            "distance_km": "?",
            "lat": str(center_lat),
            "lng": str(center_lng),
            "url": url,
            "description": "Ouvrir dans le navigateur",
            "services": "",
            "price": "",
            "rating": "",
            "jch_score": "",
            "reserve_nearby": "",
        })
    print(f"  ✅ {count} liens park4night extraits")


def _extract_places_from_nuxt(data, depth=0) -> list:
    """Recherche récursive de listes de places dans les données NUXT."""
    if depth > 6 or not data:
        return []
    if isinstance(data, list):
        if len(data) > 0 and isinstance(data[0], dict) and "lat" in data[0]:
            return data
        for item in data:
            r = _extract_places_from_nuxt(item, depth + 1)
            if r:
                return r
    if isinstance(data, dict):
        for v in data.values():
            r = _extract_places_from_nuxt(v, depth + 1)
            if r:
                return r
    return []


def scrape_campspace(page, center_lat, center_lng, radius_km, results):
    print("\n🔍 Campspace...")
    url = "https://campspace.com/fr/campspaces"
    try:
        page.goto(url, wait_until="networkidle", timeout=30000)
        time.sleep(3)
    except Exception:
        print("  ⚠️  Timeout campspace")
        return

    links = page.query_selector_all("a[href*='/fr/s/']")
    seen = {link.get_attribute("href") for link in links if link.get_attribute("href")}
    candidates = [
        (f"https://campspace.com{h}" if h.startswith("/") else h)
        for h in seen if h
    ]

    count = 0
    for fiche_url in candidates[:25]:
        try:
            page.goto(fiche_url, wait_until="domcontentloaded", timeout=20000)
            time.sleep(1)
            name = safe_text(page, "h1")
            if not name:
                continue

            lat_val, lng_val = "", ""
            map_link = page.query_selector("a[href*='maps.google'], a[href*='openstreetmap']")
            if map_link:
                href = map_link.get_attribute("href") or ""
                m = re.search(r"[?&]q=(-?\d+\.?\d*),(-?\d+\.?\d*)", href)
                if m:
                    lat_val, lng_val = m.group(1), m.group(2)

            dist = "?"
            if lat_val and lng_val:
                d = dist_km(center_lat, center_lng, float(lat_val), float(lng_val))
                if d > radius_km:
                    continue
                dist = str(d)

            service_els = page.query_selector_all("[class*='amenity'] li, [class*='service'] li")
            services = ", ".join([el.inner_text().strip() for el in service_els[:8]])

            results.append({
                "name": name,
                "source": "campspace",
                "type": "Chez l'habitant",
                "address": safe_text(page, "[class*='location'], [class*='city']"),
                "distance_km": dist,
                "lat": lat_val,
                "lng": lng_val,
                "url": fiche_url,
                "description": safe_text(page, "[class*='description']")[:200],
                "services": services,
                "price": safe_text(page, "[class*='price']"),
                "rating": safe_text(page, "[class*='rating'], [class*='score']"),
                "jch_score": "",
                "reserve_nearby": "",
            })
            count += 1
            print(f"  + {name} ({dist} km)")
        except Exception:
            continue

    print(f"  ✅ {count} spots campspace")


def scrape_france_passion(page, center_lat, center_lng, radius_km, results, fp_user, fp_pass):
    print("\n🔍 France Passion...")
    if not fp_user or not fp_pass:
        results.append({
            "name": "[Login requis — France Passion]",
            "source": "france-passion",
            "type": "Étape producteur",
            "address": "Utiliser --fp-user et --fp-pass",
            "distance_km": "?",
            "lat": "",
            "lng": "",
            "url": "https://www.france-passion.com/camping-caristes/la-carte-des-etapes",
            "description": "Gratuit avec adhésion annuelle (~30€)",
            "services": "",
            "price": "Gratuit (adhésion)",
            "rating": "",
            "jch_score": "",
            "reserve_nearby": "",
        })
        return

    try:
        page.goto("https://www.france-passion.com/mon-espace-adherent", wait_until="domcontentloaded", timeout=30000)
        time.sleep(2)

        user_field = page.query_selector("input[type='email'], input[name*='email'], input[id*='email']")
        pass_field = page.query_selector("input[type='password']")
        if not user_field or not pass_field:
            print("  ⚠️  Formulaire login France Passion introuvable")
            return

        user_field.fill(fp_user)
        pass_field.fill(fp_pass)
        submit = page.query_selector("button[type='submit'], input[type='submit']")
        if submit:
            submit.click()
        else:
            page.keyboard.press("Enter")
        time.sleep(3)

        page.goto(
            f"https://www.france-passion.com/camping-caristes/la-carte-des-etapes?lat={center_lat}&lng={center_lng}",
            wait_until="networkidle",
            timeout=30000,
        )
        time.sleep(4)

        etapes = page.query_selector_all(".etape, [class*='etape'], [class*='listing'] li, .step")
        count = 0
        for etape in etapes[:40]:
            try:
                name = safe_text(etape, "h2, h3, .name, strong") or etape.inner_text()[:60].strip()
                if not name:
                    continue
                link_el = etape.query_selector("a[href]")
                url_fiche = ""
                if link_el:
                    href = link_el.get_attribute("href") or ""
                    url_fiche = f"https://www.france-passion.com{href}" if href.startswith("/") else href
                results.append({
                    "name": name,
                    "source": "france-passion",
                    "type": "Étape chez producteur/vigneron",
                    "address": safe_text(etape, ".commune, .location"),
                    "distance_km": "?",
                    "lat": "",
                    "lng": "",
                    "url": url_fiche,
                    "description": safe_text(etape, ".description, .activite")[:150],
                    "services": "Étape gratuite (adhésion France Passion)",
                    "price": "Gratuit",
                    "rating": "",
                    "jch_score": "",
                    "reserve_nearby": "",
                })
                count += 1
            except Exception:
                continue
        print(f"  ✅ {count} étapes France Passion")

    except Exception as e:
        print(f"  ❌ Erreur France Passion : {e}")


# ── Génération output ─────────────────────────────────────────────────────────

def save_csv(results: list, path: Path):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(HEADERS.keys()))
        writer.writerow(HEADERS)
        writer.writerows(results)
    print(f"\n💾 CSV : {path}")


def generate_html(results: list, reserves: list, center_lat: float, center_lng: float,
                  radius_km: int, location_name: str, path: Path):
    """Carte Leaflet + tableau — style compatible PKA/ARTEON."""

    markers = []
    for r in results:
        if r.get("lat") and r.get("lng"):
            try:
                markers.append({
                    "lat": float(r["lat"]),
                    "lng": float(r["lng"]),
                    "name": r["name"],
                    "source": r["source"],
                    "type": r.get("type", ""),
                    "address": r.get("address", ""),
                    "distance": r.get("distance_km", "?"),
                    "url": r.get("url", ""),
                    "price": r.get("price", ""),
                    "rating": r.get("rating", ""),
                    "services": r.get("services", ""),
                    "jch_score": r.get("jch_score", ""),
                    "reserve_nearby": r.get("reserve_nearby", ""),
                })
            except (ValueError, TypeError):
                pass

    reserve_markers = [
        {"lat": rv["lat"], "lng": rv["lng"], "name": rv["name"]}
        for rv in reserves if rv.get("lat") and rv.get("lng")
    ]

    def sort_key(r):
        try:
            return float(r.get("distance_km", 99))
        except (ValueError, TypeError):
            return 99

    sorted_results = sorted(results, key=sort_key)

    table_rows = ""
    for r in sorted_results:
        color = SOURCE_COLORS.get(r["source"], "#888")
        url = r.get("url", "")
        link = f'<a href="{url}" target="_blank">🔗</a>' if url else ""
        score = r.get("jch_score", "")
        score_cell = f'<b>{score}/10</b>' if score else "—"
        reserve = r.get("reserve_nearby", "")
        table_rows += f"""
        <tr>
            <td><span class="badge" style="background:{color}">{r['source']}</span></td>
            <td>{r['name']}</td>
            <td>{r.get('type','')}</td>
            <td>{r.get('address','')}</td>
            <td>{r.get('distance_km','?')}</td>
            <td>{score_cell}</td>
            <td><small style="color:#1abc9c">{reserve}</small></td>
            <td>{r.get('services','')}</td>
            <td>{r.get('price','')}</td>
            <td>{link}</td>
        </tr>"""

    legend_items = "".join([
        f'<span class="badge" style="background:{c}">{s}</span>'
        for s, c in SOURCE_COLORS.items()
    ])

    generated = datetime.now().strftime("%d/%m/%Y %H:%M")

    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>🏕️ Spots nuit — {location_name} ({radius_km} km)</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {{
    --ink: #1a1a2e;
    --accent: #C17F3A;
    --bg: #f8f7f4;
    --white: #ffffff;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Inter', -apple-system, sans-serif; background: var(--bg); color: var(--ink); font-size: 13px; }}
  header {{ background: var(--ink); color: white; padding: 14px 20px; }}
  header h1 {{ font-size: 1.05em; font-weight: 600; letter-spacing: 0.02em; }}
  header small {{ opacity: 0.55; font-size: 0.82em; display: block; margin-top: 2px; }}
  #map {{ width: 100%; height: 48vh; border-bottom: 2px solid var(--accent); }}
  .legend {{ padding: 8px 16px; background: white; border-bottom: 1px solid #e0ddd6; display: flex; flex-wrap: wrap; gap: 5px; align-items: center; font-size: 0.78em; }}
  .legend strong {{ margin-right: 4px; color: #666; }}
  .badge {{ display: inline-block; padding: 2px 7px; border-radius: 3px; color: white; font-size: 0.72em; font-weight: 600; white-space: nowrap; }}
  .jch-note {{ background: #1a1a2e; color: #C17F3A; padding: 6px 16px; font-size: 0.78em; }}
  table {{ width: 100%; border-collapse: collapse; }}
  thead th {{ background: var(--ink); color: white; padding: 7px 10px; text-align: left; position: sticky; top: 0; font-weight: 500; font-size: 0.78em; white-space: nowrap; }}
  tbody tr:nth-child(even) {{ background: #f0ede8; }}
  tbody tr:hover {{ background: #e8e3da; }}
  tbody td {{ padding: 6px 10px; border-bottom: 1px solid #e0ddd6; vertical-align: middle; }}
  .table-wrap {{ overflow: auto; max-height: 38vh; }}
  footer {{ text-align: center; padding: 8px; font-size: 0.72em; color: #999; background: white; border-top: 1px solid #eee; }}
  a {{ color: var(--accent); text-decoration: none; }}
  a:hover {{ text-decoration: underline; }}
</style>
</head>
<body>

<header>
  <h1>🏕️ Spots nuit en van — {location_name}</h1>
  <small>Rayon {radius_km} km · {len(results)} spots · {len(reserve_markers)} réserves naturelles · {generated}</small>
</header>

<div id="map"></div>

<div class="legend">
  <strong>Sources :</strong>{legend_items}
</div>
<div class="jch-note">
  🦉 Score JCH = proximité réserves naturelles + type spot. 10/10 = spot idéal pour photo aube/crépuscule.
</div>

<div class="table-wrap">
<table>
  <thead>
    <tr>
      <th>Source</th><th>Nom</th><th>Type</th><th>Adresse</th><th>Distance</th>
      <th>Score JCH</th><th>Réserve proche</th><th>Services</th><th>Prix</th><th>🔗</th>
    </tr>
  </thead>
  <tbody>
    {table_rows}
  </tbody>
</table>
</div>

<footer>camping_scout.py v2 · PKA_JCH · {generated}</footer>

<script>
const CENTER = [{center_lat}, {center_lng}];
const RADIUS_KM = {radius_km};
const MARKERS = {json.dumps(markers, ensure_ascii=False)};
const RESERVES = {json.dumps(reserve_markers, ensure_ascii=False)};
const COLORS = {json.dumps(SOURCE_COLORS)};

const map = L.map('map').setView(CENTER, 11);
L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
  attribution: '© OpenStreetMap contributors'
}}).addTo(map);

L.circle(CENTER, {{
  radius: RADIUS_KM * 1000,
  color: '#C17F3A',
  fillColor: '#C17F3A',
  fillOpacity: 0.04,
  weight: 1.5,
  dashArray: '6,4'
}}).addTo(map);

L.circleMarker(CENTER, {{radius:8, color:'#1a1a2e', fillColor:'#C17F3A', fillOpacity:1, weight:2}})
  .bindTooltip('{location_name}', {{permanent:true, direction:'top', className:''}})
  .addTo(map);

// Réserves naturelles (JCH)
RESERVES.forEach(rv => {{
  L.circleMarker([rv.lat, rv.lng], {{
    radius: 10, color: '#1abc9c', fillColor: '#1abc9c', fillOpacity: 0.25, weight: 2,
    dashArray: '4,3'
  }}).bindPopup(`<b>🌿 ${{rv.name}}</b><br><small>Réserve naturelle</small>`).addTo(map);
}});

// Spots camping
MARKERS.forEach(m => {{
  const color = COLORS[m.source] || '#888';
  const score = m.jch_score ? ` · Score JCH : ${{m.jch_score}}/10` : '';
  const reserve = m.reserve_nearby ? `<br>🌿 ${{m.reserve_nearby}}` : '';
  const popup = `
    <b>${{m.name}}</b><br>
    <span style="background:${{color}};color:white;padding:1px 6px;border-radius:3px;font-size:0.8em">${{m.source}}</span>
    ${{m.type ? ' · ' + m.type : ''}}<br>
    ${{m.address ? '📍 ' + m.address + '<br>' : ''}}
    ${{m.distance != '?' ? '📏 ' + m.distance + ' km' : ''}}${{score}}<br>
    ${{m.services ? '🔧 ' + m.services.substring(0,80) + '<br>' : ''}}
    ${{m.price ? '💶 ' + m.price + '<br>' : ''}}
    ${{reserve}}
    ${{m.url ? '<br><a href="' + m.url + '" target="_blank">🔗 Voir la fiche</a>' : ''}}
  `;
  L.circleMarker([m.lat, m.lng], {{
    radius: 7, color: 'white', fillColor: color, fillOpacity: 0.9, weight: 1.5
  }}).bindPopup(popup).addTo(map);
}});
</script>
</body>
</html>"""

    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"🗺️  Carte HTML : {path}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Camping-Car Scout v2 — spots nuit multi-sources avec scoring JCH"
    )
    parser.add_argument("--location", "-l", required=True,
                        help="Lieu central (ex: 'Le Crotoy', 'Honfleur')")
    parser.add_argument("--radius", "-r", type=int, default=15,
                        help="Rayon en km (défaut: 15)")
    parser.add_argument("--quick", action="store_true",
                        help="Mode rapide — Overpass/OSM uniquement, sans navigateur")
    parser.add_argument("--fp-user", help="Email France Passion")
    parser.add_argument("--fp-pass", help="Mot de passe France Passion")
    parser.add_argument("--headless", action="store_true",
                        help="Playwright en mode headless (sans fenêtre)")
    parser.add_argument("--output-dir", default=".",
                        help="Répertoire de sortie (défaut: répertoire courant)")
    parser.add_argument("--save", action="store_true",
                        help=f"Sauvegarder dans {DEST_DIR}")
    args = parser.parse_args()

    has_playwright = check_playwright()

    print(f"\n🏕️  Camping-Car Scout v2")
    print(f"   Lieu     : {args.location}")
    print(f"   Rayon    : {args.radius} km")
    print(f"   Mode     : {'rapide (OSM only)' if args.quick else 'complet'}")
    print(f"   Playwright: {'✅' if has_playwright else '❌ (installer pour park4night/campspace)'}")
    if not has_playwright and not args.quick:
        print("\n   💡 Pour les sources communautaires (park4night, campspace) :")
        print("      pip install playwright && playwright install chromium")
    print()

    print("📍 Géocodage...")
    try:
        center_lat, center_lng = geocode(args.location)
    except ValueError as e:
        print(f"❌ {e}")
        sys.exit(1)

    results = []

    # Niveau 1 — Overpass/OSM (toujours)
    reserves = fetch_osm_spots(center_lat, center_lng, args.radius, results)

    # Niveau 2 — Playwright (si disponible et pas --quick)
    if not args.quick and has_playwright:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=args.headless)
            ctx = browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/124.0",
                viewport={"width": 1280, "height": 800},
                locale="fr-FR",
            )
            page = ctx.new_page()
            scrape_park4night(page, center_lat, center_lng, args.radius, results)
            scrape_campspace(page, center_lat, center_lng, args.radius, results)
            scrape_france_passion(page, center_lat, center_lng, args.radius, results,
                                  args.fp_user, args.fp_pass)
            browser.close()
    elif not args.quick and not has_playwright:
        print("\n⚠️  Playwright non installé — niveau 2 ignoré (park4night, campspace, france-passion)")

    # Scoring JCH
    print("\n⭐ Calcul scores JCH...")
    for spot in results:
        score, reserve = compute_jch_score(spot, reserves)
        spot["jch_score"] = str(score)
        spot["reserve_nearby"] = reserve

    print(f"\n📊 Total : {len(results)} spots")

    # Output
    output_dir = DEST_DIR if args.save else Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    slug = args.location.replace(" ", "_").replace("/", "-")
    csv_path = output_dir / f"camping_scout_{slug}.csv"
    html_path = output_dir / f"camping_scout_{slug}.html"

    save_csv(results, csv_path)
    generate_html(results, reserves, center_lat, center_lng, args.radius,
                  args.location, html_path)

    print(f"\n✅ Résultats disponibles :")
    print(f"   open '{html_path}'")


if __name__ == "__main__":
    main()
