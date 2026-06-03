"""
PKA DECOUVERTES Analyzer
Traite les messages en attente dans queue/, identifie les lieux,
génère des fiches Obsidian dans drafts/.

Usage :
  python3 analyzer.py                    # Claude Haiku (défaut, moins cher)
  python3 analyzer.py --model sonnet     # Claude Sonnet
  python3 analyzer.py --model opus       # Claude Opus
  python3 analyzer.py --model ollama:qwen2.5vl:7b   # local, gratuit
  python3 analyzer.py --limit 5          # traiter seulement 5 fichiers
"""

import argparse
import base64
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")

# ── Chemins ───────────────────────────────────────────────────────────────────

PKA_ROOT   = Path(os.getenv("PKA_ROOT", "/Users/jchavauxm5/PKA_JCH"))
BASE       = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes"
QUEUE_DIR  = BASE / "queue"
DRAFTS_DIR = BASE / "drafts"
LOG_DIR    = BASE / "logs"

DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

# ── Modèles ───────────────────────────────────────────────────────────────────

CLAUDE_MODELS = {
    "haiku":  "claude-haiku-4-5-20251001",
    "sonnet": "claude-sonnet-4-6",
    "opus":   "claude-opus-4-8",
}

OLLAMA_BASE = "http://localhost:11434"

# ── Appels LLM ────────────────────────────────────────────────────────────────

def call_claude(model_id: str, prompt: str, image_b64: str | None = None) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    content = []
    if image_b64:
        content.append({
            "type": "image",
            "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64},
        })
    content.append({"type": "text", "text": prompt})
    resp = client.messages.create(
        model=model_id,
        max_tokens=2048,
        messages=[{"role": "user", "content": content}],
    )
    return resp.content[0].text


def call_ollama(model_name: str, prompt: str, image_b64: str | None = None) -> str:
    payload: dict = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    if image_b64:
        payload["messages"][0]["images"] = [image_b64]
    resp = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def call_model(model_arg: str, prompt: str, image_b64: str | None = None) -> str:
    if model_arg.startswith("ollama:"):
        return call_ollama(model_arg[7:], prompt, image_b64)
    model_id = CLAUDE_MODELS.get(model_arg)
    if not model_id:
        raise ValueError(f"Modèle inconnu : {model_arg}. Choix : haiku, sonnet, opus, ollama:<name>")
    return call_claude(model_id, prompt, image_b64)

# ── Nominatim — GPS depuis nom de lieu ───────────────────────────────────────

def geocode(analysis: dict) -> dict | None:
    # Essaie plusieurs variantes pour maximiser les chances de trouver
    candidates = [
        analysis.get("place_query"),
        analysis.get("nom_lieu"),
        f"{analysis.get('nom_lieu')} {analysis.get('ville')} {analysis.get('pays')}",
        f"{analysis.get('nom_lieu')} {analysis.get('region')} {analysis.get('pays')}",
    ]
    for query in candidates:
        if not query or not query.strip():
            continue
        try:
            resp = requests.get(
                "https://nominatim.openstreetmap.org/search",
                params={"q": query.strip(), "format": "json", "limit": 1},
                headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
                timeout=10,
            )
            data = resp.json()
            if data:
                return {
                    "lat": float(data[0]["lat"]),
                    "lon": float(data[0]["lon"]),
                    "display_name": data[0]["display_name"],
                }
        except Exception as e:
            print(f"  [geocode] erreur sur '{query}': {e}")
    return None

# ── Overpass API — réserves naturelles & restaurants ──────────────────────────

OVERPASS_URL = "https://overpass-api.de/api/interpreter"
OVERPASS_FALLBACK = "https://overpass.kumi.systems/api/interpreter"

def query_overpass(query: str, timeout: int = 30) -> list[dict]:
    """Exécute une requête Overpass QL avec fallback si l'instance principale échoue."""
    for url in (OVERPASS_URL, OVERPASS_FALLBACK):
        try:
            resp = requests.post(
                url,
                data={"data": query},
                headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
                timeout=timeout,
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("elements", [])
        except Exception as e:
            if url == OVERPASS_URL:
                print(f"  [overpass] {url.split('/')[2]} → {e}, tentative fallback...")
            else:
                print(f"  [overpass] {url.split('/')[2]} → {e}")
    return []


def _extract_coords(element: dict) -> tuple[float, float] | None:
    """Extrait (lat, lon) depuis un élément Overpass (node/way/relation/center)."""
    if "lat" in element and "lon" in element:
        return (element["lat"], element["lon"])
    if "center" in element:
        return (element["center"]["lat"], element["center"]["lon"])
    return None


def get_nature_reserves(lat: float, lon: float, radius_km: int = 25) -> list[dict]:
    """Retourne jusqu'à 3 réserves naturelles/parcs nationaux/zones protégées dans le rayon."""
    radius_m = radius_km * 1000
    query = f"""
    [out:json][timeout:20];
    (
      nwr["leisure"="nature_reserve"](around:{radius_m},{lat},{lon});
      nwr["boundary"="national_park"](around:{radius_m},{lat},{lon});
      nwr["boundary"="protected_area"](around:{radius_m},{lat},{lon});
    );
    out center 10;
    """
    elements = query_overpass(query)
    results = []
    seen = set()
    for el in elements:
        name = el.get("tags", {}).get("name", "").strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        coords = _extract_coords(el)
        if not coords:
            continue
        reserve_type = "Réserve naturelle"
        if el.get("tags", {}).get("boundary") == "national_park":
            reserve_type = "Parc national"
        elif el.get("tags", {}).get("boundary") == "protected_area":
            reserve_type = "Zone protégée"
        results.append({
            "name": name,
            "type": reserve_type,
            "lat": coords[0],
            "lon": coords[1],
        })
        if len(results) >= 3:
            break
    return results


def get_restaurants(lat: float, lon: float, radius_km: int = 15) -> list[dict]:
    """Retourne jusqu'à 3 restaurants dans le rayon."""
    radius_m = radius_km * 1000
    query = f"""
    [out:json][timeout:20];
    (
      node["amenity"="restaurant"](around:{radius_m},{lat},{lon});
      way["amenity"="restaurant"](around:{radius_m},{lat},{lon});
    );
    out center 10;
    """
    elements = query_overpass(query)
    results = []
    seen = set()
    for el in elements:
        tags = el.get("tags", {})
        name = tags.get("name", "").strip()
        if not name or name.lower() in seen:
            continue
        seen.add(name.lower())
        coords = _extract_coords(el)
        if not coords:
            continue
        cuisine = tags.get("cuisine", "").capitalize()
        results.append({
            "name": name,
            "cuisine": cuisine if cuisine else "Cuisine variée",
            "lat": coords[0],
            "lon": coords[1],
        })
        if len(results) >= 3:
            break
    return results


def generate_html_report(
    lat: float, lon: float, nom_lieu: str,
    pays: str, region: str, ville: str,
    analysis: dict, van_info: str, meta: dict,
    reserves: list[dict], restaurants: list[dict],
    reports_dir: Path, slug: str, today: str,
) -> Path | None:
    """Génère un rapport HTML standalone complet avec carte intégrée."""
    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / f"{today}_{slug}.html"

        # ── Marqueurs JS pour la carte ──
        reserve_js = ",\n        ".join(
            f'L.marker([{r["lat"]}, {r["lon"]}]).bindPopup("<b>🌿 {r["name"]}</b><br>{r["type"]}").addTo(map)'
            for r in reserves
        )
        resto_js = ",\n        ".join(
            f'L.marker([{r["lat"]}, {r["lon"]}], {{icon: restoIcon}}).bindPopup("<b>🍽 {r["name"]}</b><br>{r["cuisine"]}").addTo(map)'
            for r in restaurants
        )

        # ── Scores visuels ──
        def score_bar(label: str, value: int, emoji: str) -> str:
            pct = value * 20
            return f'<div class="score-row"><span class="score-emoji">{emoji}</span><span class="score-label">{label}</span><div class="score-bar"><div class="score-fill" style="width:{pct}%"></div></div><span class="score-val">{value}/5</span></div>'

        # ── Réserves ──
        reserves_html = ""
        if reserves:
            reserves_html = '<div class="card"><h2>🌿 Réserves naturelles <span class="badge">25 km</span></h2><ul class="item-list">'
            for r in reserves:
                reserves_html += f'<li><strong>{r["name"]}</strong> — {r["type"]}</li>'
            reserves_html += "</ul></div>"
        else:
            reserves_html = '<div class="card"><h2>🌿 Réserves naturelles</h2><p class="muted">Aucune réserve trouvée dans un rayon de 25 km.</p></div>'

        # ── Restaurants ──
        restos_html = ""
        if restaurants:
            restos_html = '<div class="card"><h2>🍽 Restaurants <span class="badge">15 km</span></h2><ul class="item-list">'
            for r in restaurants:
                cuisine = f" — {r['cuisine']}" if r['cuisine'] else ""
                restos_html += f'<li><strong>{r["name"]}</strong>{cuisine}</li>'
            restos_html += "</ul></div>"
        else:
            restos_html = '<div class="card"><h2>🍽 Restaurants</h2><p class="muted">Aucun restaurant trouvé dans un rayon de 15 km.</p></div>'

        # ── Photos ──
        photos_html = ""
        for mf in meta.get("media_files", []):
            fp = PKA_ROOT / mf["file_path"]
            if fp.exists():
                import base64 as _b64
                img_b64 = _b64.standard_b64encode(fp.read_bytes()).decode()
                photos_html += f'<div class="photo-card"><img src="data:image/jpeg;base64,{img_b64}" alt="Photo source" loading="lazy"></div>'

        # ── Confiance ──
        confidence = int(analysis.get("confidence", 0) * 100)
        conf_class = "conf-high" if confidence >= 80 else "conf-med" if confidence >= 50 else "conf-low"
        action_label = "Validé" if analysis.get("action") == "validated" else "À vérifier"

        gmaps = f"https://www.google.com/maps/search/{lat},{lon}"

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nom_lieu} — PKA Découvertes</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {{
    --bg: #f8f9fa; --card: #ffffff; --text: #2c3e50; --muted: #7f8c8d;
    --accent: #2e7d32; --accent2: #e67e22; --blue: #2980b9;
    --shadow: 0 2px 8px rgba(0,0,0,0.08);
    --radius: 12px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
  .container {{ max-width: 900px; margin: 0 auto; padding: 16px; }}

  .header {{ background: linear-gradient(135deg, #1a3c34 0%, #2e7d32 100%); color: white; padding: 32px 24px; border-radius: var(--radius); margin-bottom: 20px; }}
  .header h1 {{ font-size: 1.8rem; margin-bottom: 6px; }}
  .header .sub {{ font-size: 0.95rem; opacity: 0.85; }}
  .header .meta-row {{ display: flex; flex-wrap: wrap; gap: 12px; margin-top: 12px; font-size: 0.85rem; }}
  .header .meta-row span {{ background: rgba(255,255,255,0.15); padding: 4px 10px; border-radius: 20px; }}

  .map-container {{ height: 420px; border-radius: var(--radius); overflow: hidden; margin-bottom: 20px; box-shadow: var(--shadow); }}
  #map {{ height: 100%; }}
  .legend {{ background: white; padding: 8px 12px; border-radius: 6px; box-shadow: 0 1px 5px rgba(0,0,0,0.2); font: 12px/1.5 sans-serif; }}
  .legend i {{ width: 12px; height: 12px; display: inline-block; margin-right: 5px; border-radius: 50%; vertical-align: middle; }}

  .card {{ background: var(--card); border-radius: var(--radius); padding: 20px 24px; margin-bottom: 16px; box-shadow: var(--shadow); }}
  .card h2 {{ font-size: 1.1rem; margin-bottom: 12px; display: flex; align-items: center; gap: 8px; }}
  .badge {{ font-size: 0.75rem; background: var(--bg); padding: 2px 8px; border-radius: 12px; font-weight: normal; }}

  .score-row {{ display: flex; align-items: center; gap: 10px; margin: 8px 0; }}
  .score-emoji {{ font-size: 1.2rem; width: 28px; }}
  .score-label {{ width: 110px; font-size: 0.9rem; }}
  .score-bar {{ flex: 1; height: 8px; background: #e9ecef; border-radius: 4px; overflow: hidden; }}
  .score-fill {{ height: 100%; background: var(--accent); border-radius: 4px; transition: width 0.6s ease; }}
  .score-val {{ font-weight: 600; font-size: 0.85rem; width: 32px; text-align: right; }}

  .item-list {{ list-style: none; }}
  .item-list li {{ padding: 8px 0; border-bottom: 1px solid #f0f0f0; }}
  .item-list li:last-child {{ border-bottom: none; }}

  .muted {{ color: var(--muted); font-style: italic; }}

  .photo-gallery {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 12px; }}
  .photo-card {{ border-radius: 8px; overflow: hidden; box-shadow: var(--shadow); }}
  .photo-card img {{ width: 100%; display: block; }}

  .conf-badge {{ display: inline-block; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.8rem; }}
  .conf-high {{ background: #d4edda; color: #155724; }}
  .conf-med {{ background: #fff3cd; color: #856404; }}
  .conf-low {{ background: #f8d7da; color: #721c24; }}

  .van-card {{ border-left: 4px solid var(--accent2); }}
  .van-card h2 {{ color: var(--accent2); }}

  .footer {{ text-align: center; padding: 24px; color: var(--muted); font-size: 0.8rem; }}
  .footer a {{ color: var(--blue); }}

  .btn {{ display: inline-block; padding: 8px 16px; border-radius: 20px; text-decoration: none; font-size: 0.85rem; font-weight: 600; }}
  .btn-maps {{ background: var(--blue); color: white; }}

  @media (max-width: 600px) {{
    .header h1 {{ font-size: 1.4rem; }}
    .map-container {{ height: 300px; }}
    .score-label {{ width: 90px; }}
    .photo-gallery {{ grid-template-columns: 1fr; }}
  }}
</style>
</head>
<body>
<div class="container">

  <div class="header">
    <h1>📍 {nom_lieu}</h1>
    <div class="sub">{analysis.get("type_lieu", "Lieu").capitalize()} — {ville}, {region}, {pays}</div>
    <div class="meta-row">
      <span>📅 {today}</span>
      <span>📷 {analysis.get("interet_photo", 0)}/5</span>
      <span>🌳 {analysis.get("interet_nature", 0)}/5</span>
      <span>🏛 {analysis.get("interet_patrimoine", 0)}/5</span>
      <span class="conf-badge {conf_class}">{confidence}% — {action_label}</span>
    </div>
  </div>

  <div class="map-container"><div id="map"></div></div>

  <div class="card">
    <h2>📝 Résumé</h2>
    <p>{analysis.get("description", "")}</p>
    <p style="margin-top:12px"><a class="btn btn-maps" href="{gmaps}" target="_blank">🗺 Ouvrir dans Google Maps</a></p>
  </div>

  <div class="card">
    <h2>📊 Intérêts</h2>
    {score_bar("Photo", analysis.get("interet_photo", 0), "📷")}
    {score_bar("Nature", analysis.get("interet_nature", 0), "🌳")}
    {score_bar("Patrimoine", analysis.get("interet_patrimoine", 0), "🏛")}
  </div>

  <div class="card van-card">
    <h2>🚐 Accès minivan <span class="badge">2m H · 5m L</span></h2>
    <div style="white-space: pre-line;">{van_info}</div>
  </div>

  {reserves_html}

  {restos_html}

  <div class="card">
    <h2>📸 Photos source</h2>
    <div class="photo-gallery">{photos_html if photos_html else '<p class="muted">Aucune photo</p>'}</div>
  </div>

  <div class="card">
    <h2>🔍 Indices d'identification</h2>
    <ul class="item-list">
      {''.join(f'<li>{i}</li>' for i in analysis.get("indices_utilises", []))}
    </ul>
  </div>

  <div class="footer">
    <p>Généré par PKA Découvertes · {today}<br>
    Source : Telegram — groupe DECOUVERTES · Auteur : {meta.get("author", "")}<br>
    GPS : {lat:.4f}, {lon:.4f} · <a href="{gmaps}" target="_blank">Google Maps</a></p>
  </div>

</div>

<script>
const map = L.map("map").setView([{lat}, {lon}], 10);

L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{
    attribution: "&copy; OpenStreetMap",
    maxZoom: 18,
}}).addTo(map);

L.circle([{lat}, {lon}], {{
    radius: 50000, color: "#2980b9", fillColor: "#2980b9",
    fillOpacity: 0.06, weight: 2, dashArray: "6 8",
}}).addTo(map);

L.marker([{lat}, {lon}])
    .bindPopup("<b>📍 {nom_lieu}</b>")
    .addTo(map)
    .openPopup();

const reserveIcon = L.divIcon({{ className: "", html: "🌿", iconSize: [24, 24], iconAnchor: [12, 12] }});
{reserve_js if reserve_js else "// Aucune réserve"};

const restoIcon = L.divIcon({{ className: "", html: "🍽", iconSize: [24, 24], iconAnchor: [12, 12] }});
{resto_js if resto_js else "// Aucun resto"};

L.circle([{lat}, {lon}], {{
    radius: 25000, color: "#27ae60", fillColor: "#27ae60",
    fillOpacity: 0.04, weight: 1, dashArray: "3 6",
}}).addTo(map);

const legend = L.control({{ position: "bottomright" }});
legend.onAdd = function() {{
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML = "<b>Légende</b><br>" +
        "<i style='background:#2980b9'></i> 50 km<br>" +
        "<i style='background:#27ae60'></i> Réserves 25 km<br>" +
        "🌿 Réserve · 🍽 Restaurant · 📍 Lieu";
    return div;
}};
legend.addTo(map);
</script>
</body>
</html>"""
        report_path.write_text(html, encoding="utf-8")
        return report_path
    except Exception as e:
        print(f"  [html] erreur génération rapport : {e}")
        return None

# ── Prompts ───────────────────────────────────────────────────────────────────

VISION_PROMPT = """Tu es l'agent PKA_DECOUVERTES. Analyse cette image.

Objectif principal : identifier le lieu photographié.

Extrais tous les indices visibles :
- texte, panneaux, enseignes, noms sur la photo
- monuments, paysages, architecture caractéristique
- drapeaux, plaques, logos
- végétation, relief, côte, montagne, ville

Retourne UNIQUEMENT un JSON valide avec ces champs :
{
  "nom_lieu": "nom le plus probable du lieu",
  "pays": "pays",
  "region": "région ou département",
  "ville": "ville ou commune proche",
  "type_lieu": "une valeur parmi : nature, monument, village, plage, montagne, foret, lac, autre",
  "description": "2-3 phrases décrivant ce qu'on voit et pourquoi c'est intéressant à visiter",
  "interet_photo": 0,
  "interet_nature": 0,
  "interet_patrimoine": 0,
  "van_friendly_observation": "ce que la photo révèle sur l'accessibilité (parking, espace, route)",
  "indices_utilises": ["liste des indices visuels qui ont guidé l'identification"],
  "confidence": 0.0,
  "action": "validated | needs_review",
  "place_query": "requête de recherche optimale pour trouver le lieu sur Google Maps"
}

Les scores sont de 0 à 5. confidence entre 0 et 1.
Si le lieu est clairement identifiable, action = validated.
Si incertain, action = needs_review.
"""

TEXT_PROMPT = """Tu es l'agent PKA_DECOUVERTES. Analyse ce message Telegram.

Message : {text}

Objectif : identifier si ce message parle d'un lieu touristique à visiter.

Si le message NE parle PAS d'un lieu (conversation, test, question, organisation...) :
Retourne UNIQUEMENT : {{"is_place": false}}

Si le message parle d'un lieu, retourne UNIQUEMENT un JSON valide avec ces champs :
{{
  "is_place": true,
  "nom_lieu": "nom du lieu",
  "pays": "pays",
  "region": "région",
  "ville": "ville ou commune",
  "type_lieu": "nature | monument | village | plage | montagne | foret | lac | autre",
  "description": "2-3 phrases sur l'intérêt du lieu",
  "interet_photo": 0,
  "interet_nature": 0,
  "interet_patrimoine": 0,
  "van_friendly_observation": "observations sur l'accessibilité minivan",
  "confidence": 0.0,
  "action": "validated | needs_review",
  "place_query": "requête de recherche optimale pour trouver le lieu sur Google Maps"
}}

Les scores sont de 0 à 5. confidence entre 0 et 1.
"""

VAN_PROMPT = """Tu es un expert en voyage en minivan (hauteur 2m, longueur 5m).

Lieu : {nom_lieu}, {region}, {pays}
Type : {type_lieu}
Description : {description}

Rédige une section pratique pour un voyageur en minivan avec :
1. **Accès** : type de route, praticabilité pour un grand véhicule
2. **Parking** : options connues, hauteur limite si applicable, gratuité
3. **Nuit sur place** : possible ? aire de camping-car ? interdit ?
4. **Services proches** : eau, électricité, vidange, supermarché
5. **Conseil visite** : meilleure saison, durée recommandée, heure idéale

Sois concis et pratique. Si tu n'as pas l'info, dis-le clairement.
"""

# ── Génération fiche Obsidian ─────────────────────────────────────────────────

def generate_note(
    meta: dict, analysis: dict, van_info: str, gps: dict | None,
    reserves: list[dict] | None = None,
    restaurants: list[dict] | None = None,
    report_path: Path | None = None,
) -> str:
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    nom   = analysis.get("nom_lieu", "Lieu inconnu")
    pays  = analysis.get("pays", "")
    region = analysis.get("region", "")
    ville  = analysis.get("ville", "")
    gps_str = f"{gps['lat']}, {gps['lon']}" if gps else "à compléter"
    gmaps   = f"https://www.google.com/maps/search/{gps['lat']},{gps['lon']}" if gps else ""

    yaml = f"""---
type: lieu_a_visiter
status: {analysis.get("action", "needs_review")}
source: telegram
source_group: DECOUVERTES
date_capture: {meta.get("datetime", today)[:10]}
date_analyse: {today}
auteur: {meta.get("author", "")}
pays: {pays}
region: {region}
ville: {ville}
nom_lieu: {nom}
gps: "{gps_str}"
van_friendly: incertain
parking: incertain
interet_photo: {analysis.get("interet_photo", 0)}
interet_nature: {analysis.get("interet_nature", 0)}
interet_patrimoine: {analysis.get("interet_patrimoine", 0)}
interet_van: 0
priorite: 3
confidence: {analysis.get("confidence", 0)}
tags:
  - decouvertes
  - lieu_a_visiter
  - {analysis.get("type_lieu", "autre")}
---"""

    media_section = ""
    for mf in meta.get("media_files", []):
        fp = PKA_ROOT / mf["file_path"]
        if fp.exists():
            media_section += f"\n![[{fp.name}]]"

    return f"""{yaml}

# {nom}

## Résumé

{analysis.get("description", "")}

## Pourquoi visiter

{analysis.get("description", "")}

## Intérêt photo

Score : **{analysis.get("interet_photo", 0)}/5**

## Intérêt nature

Score : **{analysis.get("interet_nature", 0)}/5**

## Intérêt patrimoine

Score : **{analysis.get("interet_patrimoine", 0)}/5**

## Accès minivan (2m hauteur · 5m longueur)

{van_info}

## Localisation

- GPS : `{gps_str}`
- [Ouvrir dans Google Maps]({gmaps})
- Pays : {pays} | Région : {region} | Ville : {ville}

## Source Telegram

- Groupe : DECOUVERTES
- Auteur : {meta.get("author", "")}
- Date : {meta.get("datetime", "")[:16]}
- Message : {meta.get("text", "") or "_(photo sans légende)_"}

## Indices d'identification

{chr(10).join(f"- {i}" for i in analysis.get("indices_utilises", []))}

## Score de confiance

**{int(analysis.get("confidence", 0) * 100)}%** — {analysis.get("action", "needs_review")}

## Photos source
{media_section if media_section else "_Aucun média_"}

## Rapport complet

""" + (
        f"[📄 Ouvrir le rapport HTML]({report_path.relative_to(PKA_ROOT)})" if report_path else "_Rapport non disponible_"
    ) + """

## Voir aussi

- [[Dashboard_DECOUVERTES]]
- [[07_TRAVELS/INDEX]]
"""

# ── Traitement d'un message ───────────────────────────────────────────────────

def process_item(json_path: Path, model_arg: str) -> bool:
    meta = json.loads(json_path.read_text())
    slug = json_path.stem
    content_type = meta.get("content_type", "text")

    print(f"\n[{slug}] type={content_type} auteur={meta.get('author')}")

    # ── Analyse vision ou texte
    try:
        if meta.get("media_files") and content_type in ("photo", "image", "image_with_caption", "screenshot"):
            img_path = PKA_ROOT / meta["media_files"][0]["file_path"]
            if not img_path.exists():
                print(f"  Image introuvable : {img_path}")
                return False
            image_b64 = base64.standard_b64encode(img_path.read_bytes()).decode()
            print(f"  Vision → {img_path.name} ({img_path.stat().st_size // 1024} Ko)")
            raw = call_model(model_arg, VISION_PROMPT, image_b64)
        else:
            text = meta.get("text", "")
            if not text.strip():
                print("  Message vide — ignoré")
                return False
            print(f"  Texte → {text[:60]!r}")
            raw = call_model(model_arg, TEXT_PROMPT.format(text=text))

        # Extraire le JSON de la réponse
        raw = raw.strip()
        if "```" in raw:
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        analysis = json.loads(raw)

        # Filtre messages non-lieu
        if not analysis.get("is_place", True):
            print("  Pas un lieu — ignoré")
            meta["analysis_status"] = "skipped"
            json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
            return False

    except Exception as e:
        print(f"  Erreur analyse : {e}")
        return False

    print(f"  Lieu identifié : {analysis.get('nom_lieu')} ({int(analysis.get('confidence', 0)*100)}%)")

    # ── GPS via Nominatim
    gps = geocode(analysis)
    if gps:
        print(f"  GPS : {gps['lat']:.4f}, {gps['lon']:.4f}")
    else:
        print("  GPS : non trouvé")

    # ── Info van (appel LLM — avant la carte pour l'inclure dans le rapport)
    try:
        van_prompt = VAN_PROMPT.format(
            nom_lieu=analysis.get("nom_lieu", ""),
            region=analysis.get("region", ""),
            pays=analysis.get("pays", ""),
            type_lieu=analysis.get("type_lieu", ""),
            description=analysis.get("description", ""),
        )
        van_info = call_model(model_arg, van_prompt)
    except Exception as e:
        van_info = f"_Erreur lors de la génération des infos van : {e}_"

    # ── Réserves naturelles, restaurants & rapport HTML
    reserves = []
    restaurants = []
    report_path = None
    if gps:
        print("  Overpass → réserves naturelles (25 km)...")
        reserves = get_nature_reserves(gps["lat"], gps["lon"], radius_km=25)
        for r in reserves:
            print(f"    🌿 {r['name']} ({r['type']})")

        print("  Overpass → restaurants (15 km)...")
        restaurants = get_restaurants(gps["lat"], gps["lon"], radius_km=15)
        for r in restaurants:
            cuisine_str = f" — {r['cuisine']}" if r['cuisine'] else ""
            print(f"    🍽 {r['name']}{cuisine_str}")

        slug = analysis.get("nom_lieu", "lieu-inconnu").replace(" ", "-").replace("/", "-")[:40]
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        reports_dir = BASE / "reports"
        print("  HTML → rapport complet...")
        report_path = generate_html_report(
            gps["lat"], gps["lon"],
            analysis.get("nom_lieu", "Lieu inconnu"),
            analysis.get("pays", ""),
            analysis.get("region", ""),
            analysis.get("ville", ""),
            analysis, van_info, meta,
            reserves, restaurants,
            reports_dir, slug, today,
        )
        if report_path:
            print(f"    → reports/{report_path.name}")

    # ── Fiche Obsidian
    note = generate_note(meta, analysis, van_info, gps, reserves, restaurants, report_path)
    nom_safe = analysis.get("nom_lieu", "lieu-inconnu").replace(" ", "-").replace("/", "-")[:40]
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    note_path = DRAFTS_DIR / f"{today}_{nom_safe}.md"
    note_path.write_text(note, encoding="utf-8")
    print(f"  → drafts/{note_path.name}")

    # Mettre à jour le statut dans le JSON
    meta["analysis_status"] = "analysed"
    meta["draft_path"] = str(note_path.relative_to(PKA_ROOT))
    json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))

    return True

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="PKA DECOUVERTES Analyzer")
    parser.add_argument(
        "--model", default="haiku",
        help="Modèle : haiku (défaut) | sonnet | opus | ollama:<name>",
    )
    parser.add_argument(
        "--limit", type=int, default=0,
        help="Nombre max de fichiers à traiter (0 = tous)",
    )
    args = parser.parse_args()

    pending = sorted(QUEUE_DIR.glob("*.json"))
    # Filtrer uniquement les non encore analysés
    pending = [p for p in pending
               if json.loads(p.read_text()).get("analysis_status") == "pending"]

    if not pending:
        print("Queue vide — aucun élément en attente.")
        return

    print(f"Modèle : {args.model}")
    print(f"Éléments en attente : {len(pending)}")
    if args.limit:
        pending = pending[:args.limit]
        print(f"Limite : {args.limit}")

    ok = 0
    for path in pending:
        if process_item(path, args.model):
            ok += 1

    print(f"\nTerminé — {ok}/{len(pending)} fiches générées dans drafts/")


if __name__ == "__main__":
    main()
