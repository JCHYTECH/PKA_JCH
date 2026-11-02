#!/usr/bin/env python3
"""
park4night.py — Enrichissement « où dormir en van » pour PKA DÉCOUVERTES.

Interroge l'API interne (non documentée) de park4night.com pour trouver les
spots de nuit autour d'un lieu, filtre par type/note, puis affine « vue /
tranquillité » en minant les commentaires des finalistes.

Conception anti-surcharge :
  - UN SEUL appel /api/places/around par lieu (filtre type côté serveur).
  - Le reste (note, services, description) est filtré LOCALEMENT.
  - Les commentaires (HTML, ~470 Ko) ne sont chargés que pour les top_k finalistes.
  - Cache local TTL 7 jours + rate-limit poli (intervalle min entre requêtes).
  - Repli gracieux : en cas d'échec, on renvoie ce qu'on a déjà.

Usage CLI :
  python3 park4night.py 48.04 7.30 --radius 20 --top 5 --min-rating 3.5

Réponse de l'API : JSON **encodé en base64** (quirk à gérer).

Model: deepseek-v4 (créé 2026-08-30)
"""

import argparse
import base64
import html as html_mod
import json
import re
import time
from pathlib import Path
from typing import Any, Optional

import requests

# ── Chemins ────────────────────────────────────────────────────────────────────
PKA_ROOT = Path(__file__).resolve().parents[2]
CACHE_FILE = (
    PKA_ROOT
    / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/.cache/park4night_cache.json"
)

# ── Config réseau / politesse ──────────────────────────────────────────────────
BASE = "https://park4night.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36"
)
MIN_INTERVAL = 1.5       # secondes entre deux requêtes HTTP (politesse)
TIMEOUT = 25             # secondes
CACHE_TTL = 24 * 3600    # 24 heures (donnée volatile — on refraîchit au moment de la planification)

_last_request = 0.0


# ── Vocabulaires (codes → libellés FR) ─────────────────────────────────────────
TYPES_FR = {
    "PN": "Nature", "P": "Parking jour/nuit", "AR": "Aire de repos",
    "APN": "Aire pique-nique", "ACC_G": "Aire CC gratuite",
    "ACC_P": "Aire CC payante", "ACC_PR": "Parking privé CC",
    "OR": "Off-road 4x4", "F": "Ferme/vignoble", "C": "Camping",
    "ASS": "Aire service (sans parking)", "PJ": "Parking jour",
    "EP": "Chez l'habitant", "DS": "Services extra", "PSS": "Parking CC sans services",
}

SERVICES_FR = {
    "caravaneige": "Caravaneige", "animaux": "Animaux acceptés",
    "point_eau": "Eau potable", "eau_noire": "Vidange eaux noires",
    "eau_usee": "Vidange eaux grises", "poubelle": "Poubelles",
    "wc_public": "WC publics", "douche": "Douches", "boulangerie": "Boulangerie",
    "electricite": "Électricité", "wifi": "WiFi", "piscine": "Piscine",
    "laverie": "Laverie", "gaz": "Gaz", "lavage": "Lavage CC",
    "gpl": "GPL", "donnees_mobile": "3G/4G",
}

# Types pertinents pour dormir en van (par défaut)
VAN_TYPES = ["ACC_G", "ACC_P", "ACC_PR", "C", "F", "PN", "P", "AR"]

# Mots-clés multilingues pour le scoring « vue / tranquillité »
VIEW_WORDS = [
    "vue", "view", "vista", "panorama", "panoramique", "belvedere", "belvédère",
    "point de vue", "dominante", "overlooking", "ausblick", "uitzicht",
]
CALM_WORDS = [
    "calme", "tranquille", "tranquilo", "tranquil", "quiet", "calm", "silence",
    "silencieux", "paisible", "peaceful", "reposant", "relaxing", "zen",
    "serein", "still",
]
NOISE_WORDS = [
    "bruit", "bruyant", "noise", "noisy", "route passante", "passage", "trafic",
    "traffic", "autoroute", "highway", "pas calme", "agité", "agite",
]


# ── Cache local ────────────────────────────────────────────────────────────────
def _load_cache() -> dict:
    if CACHE_FILE.exists():
        try:
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def _save_cache(cache: dict) -> None:
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def _cache_get(key: str) -> Optional[list]:
    entry = _load_cache().get(key)
    if not entry:
        return None
    if time.time() - entry.get("ts", 0) > CACHE_TTL:
        return None
    return entry.get("places")


def _cache_put(key: str, places: list) -> None:
    cache = _load_cache()
    cache[key] = {"ts": time.time(), "places": places}
    _save_cache(cache)


# ── HTTP (rate-limit + décodage) ───────────────────────────────────────────────
def _throttle() -> None:
    global _last_request
    wait = MIN_INTERVAL - (time.time() - _last_request)
    if wait > 0:
        time.sleep(wait)
    _last_request = time.time()


def _decode_response(b: bytes) -> Any:
    """L'API renvoie du JSON encodé en base64 (quirk). Gère les deux cas."""
    try:
        return json.loads(b)
    except Exception:
        return json.loads(base64.b64decode(b).decode("utf-8"))


def _http_get(url: str, params: Optional[dict] = None) -> Optional[Any]:
    _throttle()
    try:
        r = requests.get(
            url, params=params,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json"},
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return None
        return _decode_response(r.content)
    except Exception:
        return None


# ── API principale : places autour d'un point ─────────────────────────────────
def around(
    lat: float,
    lng: float,
    radius: int = 20,
    lang: str = "fr",
    types: Optional[list] = None,
    use_cache: bool = True,
) -> list:
    """Retourne les lieux park4night autour de (lat, lng).

    Le filtre `type` est appliqué côté serveur (prouvé). La réponse est un
    tableau de dicts (type, name, lat, lng, distance, rating, review, services,
    description, url, …).
    """
    types = types or VAN_TYPES
    cache_key = f"{round(lat, 2)},{round(lng, 2)},{radius},{','.join(types)}"
    if use_cache:
        cached = _cache_get(cache_key)
        if cached is not None:
            return cached

    params = {
        "lat": f"{lat:.6f}",
        "lng": f"{lng:.6f}",
        "radius": str(radius),
        "lang": lang,
        "filter": json.dumps({"type": types}),
    }
    data = _http_get(f"{BASE}/api/places/around", params=params)
    places = data if isinstance(data, list) else []

    if use_cache and places:
        _cache_put(cache_key, places)
    return places


# ── Commentaires (HTML de la fiche) ────────────────────────────────────────────
_COMMENT_RE = re.compile(r'feedback-article-content[^>]*>([\s\S]{0,600}?)<')
_TAG_RE = re.compile(r"<[^>]+>")


def place_comments(place_id: int, lang: str = "fr") -> list[str]:
    """Extrait le texte des commentaires depuis la page HTML de la fiche."""
    _throttle()
    try:
        r = requests.get(
            f"{BASE}/{lang}/place/{place_id}",
            headers={"User-Agent": USER_AGENT},
            timeout=TIMEOUT,
        )
        if r.status_code != 200:
            return []
        html = r.text
    except Exception:
        return []
    comments = []
    for raw in _COMMENT_RE.findall(html):
        text = _TAG_RE.sub(" ", raw)
        text = html_mod.unescape(text)
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) >= 20:
            comments.append(text)
    return comments


def score_vibe(comments: list[str]) -> dict:
    """Compte les signaux « vue / calme / bruit » dans les commentaires."""
    view = calm = noise = 0
    for c in comments:
        cl = c.lower()
        view += sum(1 for w in VIEW_WORDS if w in cl)
        calm += sum(1 for w in CALM_WORDS if w in cl)
        noise += sum(1 for w in NOISE_WORDS if w in cl)
    return {"view": view, "calm": calm, "noise": noise, "n_comments": len(comments)}


def _vibe_score(rating: Optional[float], sig: dict) -> float:
    """Note finale : note moyenne + bonus « vue/calme » borné et amorti.

    density    = (vue + calme − 2·bruit) / n_avis   (borné à ±1)
    confidence = min(n_avis/5, 1)                   (pleine confiance dès 5 avis)
    bonus      = density × confidence ∈ [-1, 1]     (amortit les petits échantillons)
    """
    base = float(rating or 0)
    n = sig["n_comments"]
    if n == 0:
        return round(base, 2)
    raw = sig["view"] + sig["calm"] - 2 * sig["noise"]
    density = max(-1.0, min(raw / n, 1.0))
    confidence = min(n / 5.0, 1.0)
    bonus = density * confidence
    return round(base + bonus, 2)


# ── Orchestration ──────────────────────────────────────────────────────────────
def find_sleep_spots(
    lat: float,
    lng: float,
    radius: int = 20,
    types: Optional[list] = None,
    min_rating: float = 0.0,
    top_k: int = 5,
    fetch_comments: bool = True,
    lang: str = "fr",
) -> list[dict]:
    """Pipeline complet : autour → filtre note → top_k → commentaires → score.

    Retourne une liste triée (meilleur « vibe » en premier) de dicts :
      {name, type, type_label, lat, lng, distance, rating, review,
       services, services_label, url, vibe_score, view, calm, noise, n_comments}
    """
    places = around(lat, lng, radius=radius, lang=lang, types=types)

    candidates = []
    for p in places:
        rating = p.get("rating")
        if rating is None or float(rating) < min_rating:
            continue
        t = p.get("type") or {}
        candidates.append(
            {
                "id": p.get("id"),
                "name": p.get("name") or t.get("label", "?"),
                "type": t.get("code"),
                "type_label": TYPES_FR.get(t.get("code"), t.get("label", "?")),
                "lat": p.get("lat"),
                "lng": p.get("lng"),
                "distance": round(float(p.get("distance", 0)), 2),
                "rating": rating,
                "review": p.get("review", 0),
                "services": p.get("services", []),
                "services_label": [SERVICES_FR.get(s, s) for s in p.get("services", [])],
                "url": f"{BASE}{p.get('url', '')}" if p.get("url") else None,
                "description": (p.get("description") or "")[:200],
                "view": 0, "calm": 0, "noise": 0, "n_comments": 0,
                "vibe_score": float(rating or 0),
            }
        )

    # tri initial : meilleure note, puis plus proche
    candidates.sort(key=lambda x: (-(x["rating"] or 0), x["distance"]))

    if fetch_comments:
        # bassin élargi : le signal « vue/calme » doit pouvoir faire remonter un
        # spot classé légèrement plus bas sur la note/distance.
        pool = min(len(candidates), max(top_k, 6))
        for c in candidates[:pool]:
            if not c["id"]:
                continue
            comments = place_comments(c["id"], lang=lang)
            sig = score_vibe(comments)
            c.update(sig)
            c["vibe_score"] = _vibe_score(c["rating"], sig)

    candidates.sort(key=lambda x: (-x["vibe_score"], x["distance"]))
    return candidates[:top_k]


# ── CLI ────────────────────────────────────────────────────────────────────────
def main() -> None:
    ap = argparse.ArgumentParser(description="Trouver où dormir en van (park4night)")
    ap.add_argument("lat", type=float)
    ap.add_argument("lng", type=float)
    ap.add_argument("--radius", type=int, default=20)
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--min-rating", type=float, default=0.0)
    ap.add_argument("--types", default=",".join(VAN_TYPES), help="codes séparés par virgule")
    ap.add_argument("--no-comments", action="store_true", help="ne pas miner les commentaires")
    args = ap.parse_args()

    types = [t.strip() for t in args.types.split(",") if t.strip()]
    spots = find_sleep_spots(
        args.lat, args.lng, radius=args.radius, types=types,
        min_rating=args.min_rating, top_k=args.top,
        fetch_comments=not args.no_comments,
    )

    print(f"Spots de nuit autour de ({args.lat}, {args.lng}) — rayon {args.radius} km\n")
    if not spots:
        print("Aucun spot trouvé.")
        return
    for i, s in enumerate(spots, 1):
        svc = ", ".join(s["services_label"][:6]) or "—"
        print(f"{i}. {s['name']}  [{s['type_label']}]")
        print(f"   {s['distance']} km · note {s['rating']} · vibe {s['vibe_score']} "
              f"(vue {s['view']}, calme {s['calm']}, bruit {s['noise']})")
        print(f"   GPS {s['lat']}, {s['lng']}")
        print(f"   services: {svc}")
        print(f"   {s['url']}")
        print()


if __name__ == "__main__":
    main()
