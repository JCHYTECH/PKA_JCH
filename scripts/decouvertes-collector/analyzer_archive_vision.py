"""
PKA DECOUVERTES Analyzer
Traite les messages en attente dans queue/, identifie les lieux,
génère des fiches Obsidian dans drafts/.

Model: unknown (créé ~2026-06-02, modèle non documenté)

Usage :
  python3 analyzer.py                         # Claude Haiku (défaut)
  python3 analyzer.py --cascade               # Cascade auto : qwen3.5 → haiku → sonnet → opus
  python3 analyzer.py --cascade --cascade-order ollama:qwen3.5,haiku,sonnet
  python3 analyzer.py --model sonnet          # Forcer un modèle spécifique
  python3 analyzer.py --limit 5               # Traiter seulement N fichiers
"""

import argparse
import base64
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

# ── OCR & EXIF (optionnels — fallback gracieux si absents) ──────────────────
try:
    from PIL import Image, ExifTags
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import pytesseract
    HAS_TESSERACT = True
except ImportError:
    HAS_TESSERACT = False

# PKA_ROOT doit être connu avant de charger les secrets
PKA_ROOT = Path(os.getenv("PKA_ROOT", str(Path(__file__).resolve().parents[2])))

# Charger depuis JCH_PRIVATE/ (protégé par .gitignore) avec fallback local
_env_path = PKA_ROOT / "JCH_PRIVATE" / "decouvertes.env"
if not _env_path.exists():
    _env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

# ── Chemins ───────────────────────────────────────────────────────────────────
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

OLLAMA_BASE = os.getenv("OLLAMA_BASE", "http://localhost:11435")

# ── Ordre cascade par défaut ────────────────────────────────────────────────────

CASCADE_ORDER = ["ollama:qwen3.5", "haiku", "sonnet", "opus"]
CASCADE_THRESHOLD = 0.7

# ── Cache déduplication ────────────────────────────────────────────────────
CACHE_DIR = BASE / ".cache"
CACHE_FILE = CACHE_DIR / "analyzed_places.json"
GMAPS_CSV = BASE / "lieux_google_maps.csv"
GMAPS_CSV_HEADER = "Name,Latitude,Longitude,Country,Region,Type,Confidence,Date,Notes"

def _load_cache() -> dict:
    """Charge le cache des lieux déjà analysés. Retourne {place_key: {date, nom_lieu}}."""
    if not CACHE_FILE.exists():
        return {}
    try:
        return json.loads(CACHE_FILE.read_text())
    except (json.JSONDecodeError, OSError):
        return {}

def _save_cache(cache: dict) -> None:
    """Sauvegarde le cache de déduplication."""
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))

def _cache_key(nom_lieu: str) -> str:
    """Génère une clé de cache normalisée à partir d'un nom de lieu."""
    return hashlib.sha256(
        nom_lieu.strip().lower().encode()
    ).hexdigest()[:16]

def _append_google_maps_csv(analysis: dict, gps: dict) -> None:
    """Ajoute une ligne au fichier CSV compatible Google My Maps (import direct).

    Si le pays n'est pas fourni par l'analyse LLM, tente un reverse geocode Nominatim.
    """
    import csv as _csv
    nom = analysis.get("nom_lieu", "").replace('"', '""')
    pays = analysis.get("pays", "").replace('"', '""')
    region = analysis.get("region", "").replace('"', '""')
    type_lieu = analysis.get("type_lieu", "")
    confidence = f"{analysis.get('confidence', 0):.0%}"
    date_str = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    notes = analysis.get("description", "")[:200].replace('"', '""')

    # Reverse geocode fallback si le pays est vide
    if not pays.strip():
        try:
            resp = requests.get(
                "https://nominatim.openstreetmap.org/reverse",
                params={"lat": gps["lat"], "lon": gps["lon"], "format": "json", "zoom": 3},
                headers={"User-Agent": "PKA_DECOUVERTES/1.0"},
                timeout=10,
            )
            data = resp.json()
            pays = data.get("address", {}).get("country", "")
            region = region or data.get("address", {}).get("state", "")
        except Exception:
            pass

    write_header = not GMAPS_CSV.exists()
    with open(GMAPS_CSV, "a", newline="", encoding="utf-8") as f:
        w = _csv.writer(f)
        if write_header:
            w.writerow(GMAPS_CSV_HEADER.split(","))
        w.writerow([nom, gps["lat"], gps["lon"], pays, region, type_lieu, confidence, date_str, notes])

# ── OCR & EXIF ──────────────────────────────────────────────────────────────

# Patterns pour détecter un nom de lieu dans du texte brut
_PLACE_PATTERNS = [
    # Français : "Château de X", "Abbaye de X", "Cathédrale de X"...
    # Le nom qui suit DOIT commencer par une majuscule (nom propre) — (?-i:) force la casse
    re.compile(r'(?i)(?:Château|Abbaye|Cathédrale|Basilique|Église|Collegiale'
               r'|Chapelle|Monastère|Forteresse|Citadelle|Tour|Pont|Lac'
               r'|Plage|Grotte|Cascade|Cirque|Col|Pic|Mont|Vallée'
               r'|Parc|Jardin|Réserve|Village|Hameau)\s+(?:du\s+|de\s+|des\s+|d\')?\s*'
               r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']+'),
    # Italien : "Piana di X", "Val di X", "Lago di X"...
    re.compile(r'(?i)(?:Piana|Val|Lago|Monte|Passo|Rifugio|Isola|Fiume'
               r'|Torre|Ponte|Castello|Chiesa|Duomo|Piazza|Lido|Spiaggia'
               r'|Baia|Golfo|Capo|Porto|Borgo|Santuario|Eremo'
               r')\s+(?:di|del|della|dei|degli|delle|san|sant\')?\s*'
               r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']+'),
    # "San X", "Santa X", "Sant'X" — toponymes italiens
    re.compile(r'(?i)(?:San|Santa|Sant)\s+(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']+'),
    # "X (Y — Z)" — lieu avec région entre parenthèses
    re.compile(r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\'\s]{3,40})\s*\((?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\'\s,]{2,30})\)'),
    # Allemand : "Schloss X", "Burg X", "X Brücke"... (mot suivant DOIT être capitalisé)
    re.compile(r'(?i)(?:Schloss|Burg|Kloster|Dom|Münster|Berg|Bach'
               r'|Wald|Insel|Brücke|Turm)\s+(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']{2,30}'),
    re.compile(r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']{2,30}\s+(?i:Brücke|Schloss|Burg|Berg|Wald)'),
    # Mots composés allemands : "Rakotzbrücke", "Xburg", "Xstein", "Xdorf", "Xbach"
    re.compile(r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[a-zàâäéèêëîïôöùûüç]{3,20}'
               r'(?i:brücke|brucke|burg|berg|stein|dorf|bach|feld|heim'
               r'|garten|schlucht|klamm|spitze|horn|kogel|gletscher'
               r'|see|tal|alp|wand|au|ach|ried|moos|egg|kopf|joch)'),
    # Anglais/International : "X Castle", "X Abbey", "X Cathedral"...
    re.compile(r'(?-i:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ])[\w\-\']{2,30}\s+'
               r'(?i:Castle|Abbey|Cathedral|Basilica|Church'
               r'|Monastery|Fortress|Citadel|Tower|Bridge|Lake'
               r'|Beach|Cave|Waterfall|Cirque|Pass|Peak|Mount|Valley'
               r'|Park|Garden|Reserve|Village|Hamlet|Falls|Canyon'
               r'|National\s+Park|Nature\s+Reserve)'),
    # Nom propre en MAJUSCULES suivi d'un tiret et d'une région (ex: "SISTERON - PROVENCA")
    # Priorité HAUTE : très fiable — capture un seul mot en majuscules avant le tiret
    re.compile(r'\b([A-Z][A-Z\']{3,30})\s*[-–—]\s*(?:PROVENCE|PROVENCA|BRETAGNE|ALSACE|CORSE|PACA|OCCITANIE|AUVERGNE|NORMANDIE|SAVOIE|ARDECHE|DORDOGNE|CAMARGUE|TOSCANA|LOMBARDIA|SICILIA|TRENTINO|BAVIERA|TIROL)\b',
               re.IGNORECASE),
    # Mot en majuscule suivi de "(01)" style département
    re.compile(r'([A-Z][a-zàâäéèêëîïôöùûüç\-]{3,}(?:\s[A-Z][a-zàâäéèêëîïôöùûüç\-]{3,}){0,3})\s*\(\d{2,3}\)'),
    # Nom propre isolé tout en MAJUSCULES (5+ lettres, filtré par blocklist)
    re.compile(r'\b([A-Z][A-Z\']{4,}(?:\s[A-Z][A-Z\']{2,}){0,2})\b'),
    # Nom propre en Title Case (ex: "Pantropica") — 7+ lettres, dernier recours
    re.compile(r"\b([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][a-zàâäéèêëîïôöùûüç']{6,}(?:\s[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][a-zàâäéèêëîïôöùûüç']{2,}){0,2})\b"),
    # Emoji lieu suivi d'un nom (priorité basse)
    re.compile(r'[📍🏰⛪🏞🏔🌊🏖]\s*[\w\s\-]{3,40}'),
]

def ocr_extract_text(image_path: Path) -> str | None:
    """Extrait le texte d'une image via OCR (tesseract). Retourne None si indisponible/échec.

    Stratégie multi-passe : essaie couleur PSM 6 → couleur PSM 3 → N&B PSM 6.
    Chaque passe est évaluée : si elle contient un lieu extractible, on la garde.
    Sinon on continue — le bruit Instagram UI ne doit pas court-circuiter le fallback.
    """
    if not HAS_TESSERACT or not HAS_PIL:
        return None
    try:
        img = Image.open(image_path)
        candidates = []

        # Passe 1 : couleur PSM 6
        t = pytesseract.image_to_string(img, lang='fra+eng+ita+deu', config='--psm 6')
        if t.strip():
            candidates.append(t.strip())

        # Passe 2 : couleur PSM 3
        t = pytesseract.image_to_string(img, lang='fra+eng+ita+deu', config='--psm 3')
        if t.strip():
            candidates.append(t.strip())

        # Passe 3 : N&B PSM 6 (fallback textes difficiles)
        gray = img.convert('L')
        t = pytesseract.image_to_string(gray, lang='fra+eng+ita+deu', config='--psm 6')
        if t.strip():
            candidates.append(t.strip())

        if not candidates:
            return None

        # Retourner le meilleur candidat : celui qui contient un lieu extractible,
        # ou à défaut le plus long (plus de texte = plus de chances)
        for text in candidates:
            if extract_place_from_text(text):
                return text
        return max(candidates, key=len)
    except Exception as e:
        print(f"  [ocr] échec : {e}")
        return None

# Mots en majuscules qui NE sont PAS des lieux (bruit Instagram/OCR)
_PLACE_BLOCKLIST = {
    'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT', 'SUN',
    'JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC',
    'SECRET', 'ROMANTIQUE', 'HABITE', 'DEPUIS', 'INSPIRA', 'TOILES',
    'SUGGESTED', 'FOLLOW', 'TRANSLATION', 'CREDITS', 'AUTOR', 'SEE',
    'HOURS', 'AGO', 'MORE', 'LIKE', 'THIS', 'THAT', 'WITH', 'FROM',
    'LINK', 'BIO', 'PHOTO', 'VIDEO', 'POST', 'SHARE', 'COMMENT',
    'FOR', 'YOU', 'AND', 'THE', 'NEW', 'NOW', 'HAS', 'WAS',
    'VIA', 'UNE', 'SUR', 'DANS', 'AVEC', 'POUR', 'PAR', 'EST',
    'SON', 'LES', 'DES', 'QUE', 'QUI', 'PAS', 'PLUS', 'AUX',
    'NOTRE', 'VOTRE', 'LEUR', 'TOUS', 'TOUT', 'TRES', 'BIEN',
    'CETTE', 'CES', 'MON', 'TON', 'SON', 'MES', 'TES', 'SES',
    'ELLE', 'ILS', 'ELLES', 'FAIRE', 'ETRE', 'AVOIR', 'DIRE',
    'ALORS', 'DONC', 'MAIS', 'AUSSI', 'MEME', 'DEJA', 'APRES',
    'ENCORE', 'TOUJOURS', 'JAMAIS', 'RIEN', 'PEUT', 'FAIT',
    'DEUX', 'LIEU', 'CARTE', 'PLAN', 'INFO', 'PAGE', 'SITE',
    'SEE', 'TRANSLATION', 'PRESENTA', 'OCCITANIA', 'PROVENCA',
    'CREDIT', 'CAPTION', 'LANTIQUITE', 'LABYRINTHIQUE', 'ROMANTIQUE',
    'PAINTING', 'BRIDGE', 'GERMANY', 'LOOKS', 'EARTHPIX', 'MEDIAPART',
    # Title Case (index 7) blocklist additions
    'Follow', 'Reels', 'Friends', 'Watch', 'Suggested', 'Again',
    'Pause', 'Sul', 'Mare', 'Prima', 'Posto', 'Perfetto', 'Rallentare',
    'Viaggio', 'Dopo', 'Fare', 'Passi', 'Ripartire', 'Exactly', 'Showed',
    'First', 'Place', 'Expect', 'Tropical', 'Rainforest', 'Netherlands',
    'Tommaso', 'Michele', 'Welcome', 'Friends', 'Pirie', 'Sacra', 'Comment',
}

def extract_places_from_text(text: str) -> list[str]:
    """Extrait TOUS les lieux du texte — gère les listes numérotées (posts itinéraires).

    Stratégie :
    1. Détecter une liste numérotée (ex: Romantic Road) → extraire chaque item
    2. Sinon, fallback sur extract_place_from_text() pour le lieu unique
    """
    results = []

    # ── Détection de liste numérotée ──────────────────────────────────────
    # Pattern: "1. Nom du lieu" ou "* 1. Nom du lieu" ou "1 - Nom du lieu"
    numbered = re.findall(
        r'(?:^|\n).*?(?:\*\s*)?\b(\d+)[\.\-][ \t]+'
        r'([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\'\(\)]+(?:[ \t]+(?:[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\'\(\)]+|ob|am|der|im|de|di|del|sur|en|au|aux|du|des|le|la|les|el|il|van|von|zum|zur)){0,4})',
        text, re.MULTILINE,
    )
    # Extraire seulement les noms de lieux (deuxième groupe), filtrer doublons
    seen = set()
    clean_numbered = []
    for num, name in numbered:
        name = name.strip()
        if name.lower() not in seen:
            seen.add(name.lower())
            clean_numbered.append(name)
    if len(clean_numbered) >= 3:
        # Filtrer les lignes parasites (mots trop génériques)
        blocklist_lower = {w.lower() for w in _PLACE_BLOCKLIST}
        for item in clean_numbered:
            clean = item.strip().rstrip("',-:;.!?")
            # Skip si trop court ou dans la blocklist
            if len(clean) < 4 or clean.lower() in blocklist_lower:
                continue
            # Skip si commence par un stop word
            first_word = clean.split()[0].lower() if clean.split() else ''
            if first_word in {'save', 'follow', 'share', 'comment', 'like', 'the', 'this', 'one', 'start', 'finish'}:
                continue
            results.append(clean)

    # ── Fallback : lieu unique ────────────────────────────────────────────
    if not results:
        single = extract_place_from_text(text)
        if single:
            results.append(single)

    return results


def extract_place_from_text(text: str) -> str | None:
    """Tente d'extraire un nom de lieu du texte OCR via patterns regex."""
    for i, pattern in enumerate(_PLACE_PATTERNS):
        # Pour les patterns à blocklist (10=MAJUSCULES, 11=Title Case), essayer
        # tous les matchs jusqu'à en trouver un qui passe la blocklist
        if i in (10, 11):
            for match in pattern.finditer(text):
                groups = match.groups()
                candidate = groups[0].strip() if groups else match.group(0).strip()
                words = candidate.split()
                # Nettoyer ponctuation trailing (', -, :, etc.)
                clean = [w.rstrip("',-:;.!?") for w in words]
                if i == 11:
                    place_words = [w for w in clean if w not in _PLACE_BLOCKLIST]
                else:
                    place_words = [w for w in clean if w.upper() not in _PLACE_BLOCKLIST]
                if place_words:
                    return ' '.join(place_words)
            continue

        match = pattern.search(text)
        if match:
            candidate = match.group(0).strip()
            # Pour MAJUSCULES+région (8) → extraire le groupe capturant
            if i == 8:
                groups = match.groups()
                if groups:
                    candidate = groups[0].strip()
            return candidate
    return None

def extract_exif_gps(image_path: Path) -> dict | None:
    """Extrait les coordonnées GPS des métadonnées EXIF. Retourne {lat, lon} ou None."""
    if not HAS_PIL:
        return None
    try:
        img = Image.open(image_path)
        exif = img.getexif()
        if not exif:
            return None
        gps_info = {}
        for tag_id, value in exif.items():
            tag_name = ExifTags.TAGS.get(tag_id, "")
            if tag_name == "GPSInfo":
                gps_info = value
                break
        if not gps_info:
            return None

        def _dms_to_dd(values):
            """Convertit (deg, min, sec) tuple en degrés décimaux."""
            d, m, s = [float(x) for x in values]
            return d + m / 60 + s / 3600

        lat = _dms_to_dd(gps_info[2])
        lon = _dms_to_dd(gps_info[4])
        if gps_info.get(1) == 'S':
            lat = -lat
        if gps_info.get(3) == 'W':
            lon = -lon
        return {"lat": lat, "lon": lon}
    except Exception:
        return None

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


def _extract_json(raw: str) -> dict:
    """Extrait un objet JSON d'une réponse LLM, tolérant aux formats variés."""
    raw = raw.strip()
    # Tente d'extraire d'un bloc ```json ... ```
    if "```" in raw:
        parts = raw.split("```")
        for p in parts:
            p = p.strip()
            if p.startswith("json"):
                p = p[4:]
            try:
                return json.loads(p)
            except json.JSONDecodeError:
                continue
    # Tente de trouver la première accolade { et dernière }
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end != -1:
        try:
            return json.loads(raw[start:end+1])
        except json.JSONDecodeError:
            pass
    # Dernier essai : la ligne complète
    return json.loads(raw)


def analyze_with_cascade(
    model_order: list[str], threshold: float,
    content_type: str, image_b64: str | None, text: str,
    hint: str | None = None,
) -> dict | None:
    """Essaie les modèles dans l'ordre jusqu'à obtenir une confiance >= threshold."""
    best = None
    best_conf = -1.0

    for i, model_arg in enumerate(model_order):
        arrow = "→" if i > 0 else ""
        print(f"  {arrow} {model_arg}...", end=" ", flush=True)
        try:
            if image_b64 and content_type in ("photo", "image", "image_with_caption", "screenshot"):
                raw = call_model(model_arg, get_vision_prompt(hint), image_b64)
            else:
                raw = call_model(model_arg, TEXT_PROMPT.format(text=text))

            analysis = _extract_json(raw)

            if not analysis.get("is_place", True):
                print(f"pas un lieu")
                continue

            conf = float(analysis.get("confidence", 0))
            nom = analysis.get("nom_lieu", "?")
            print(f"{nom} ({int(conf*100)}%)")

            if conf > best_conf:
                best = analysis
                best_conf = conf

            if conf >= threshold:
                print(f"  ✅ seuil {int(threshold*100)}% atteint — arrêt cascade")
                return analysis

        except Exception as e:
            print(f"erreur: {e}")

    if best:
        print(f"  ⚠️ meilleur score {int(best_conf*100)}% < {int(threshold*100)}%")
    return best


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


def get_nearby_attractions(lat: float, lon: float, radius_km: int = 30) -> list[dict]:
    """Retourne jusqu'à 6 lieux touristiques/patrimoine dans le rayon."""
    radius_m = radius_km * 1000
    query = f"""
    [out:json][timeout:25];
    (
      nwr["tourism"="attraction"](around:{radius_m},{lat},{lon});
      nwr["historic"="castle"](around:{radius_m},{lat},{lon});
      nwr["historic"="monument"](around:{radius_m},{lat},{lon});
      nwr["historic"="church"](around:{radius_m},{lat},{lon});
      nwr["tourism"="viewpoint"](around:{radius_m},{lat},{lon});
      nwr["natural"="peak"](around:{radius_m},{lat},{lon});
      nwr["waterway"="waterfall"](around:{radius_m},{lat},{lon});
    );
    out center 15;
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
        tags = el.get("tags", {})
        if "historic" in tags:
            kind = "Patrimoine"
        elif tags.get("tourism") == "viewpoint":
            kind = "Point de vue"
        elif tags.get("natural") == "peak":
            kind = "Sommet"
        elif tags.get("waterway") == "waterfall":
            kind = "Cascade"
        else:
            kind = "Site touristique"
        results.append({
            "name": name,
            "type": kind,
            "lat": coords[0],
            "lon": coords[1],
        })
        if len(results) >= 6:
            break
    return results


def generate_html_report(
    lat: float, lon: float, nom_lieu: str,
    pays: str, region: str, ville: str,
    analysis: dict, van_info: str, meta: dict,
    reserves: list[dict], restaurants: list[dict],
    attractions: list[dict],
    reports_dir: Path, slug: str, today: str,
) -> Path | None:
    """Génère un rapport HTML standalone complet avec carte intégrée."""
    try:
        reports_dir.mkdir(parents=True, exist_ok=True)
        report_path = reports_dir / f"{today}_{slug}.html"

        import math as _math

        def _dist_km(lat2: float, lon2: float) -> str:
            d = _math.dist((lat, lon), (lat2, lon2)) * 111.32
            return f"{d:.0f} km" if d >= 1 else f"{int(d*1000)} m"

        # ── Marqueurs JS carte ──
        reserve_js = ",\n        ".join(
            f'L.marker([{r["lat"]}, {r["lon"]}], {{icon: reserveIcon}}).bindPopup("<b>🌿 {r["name"]}</b><br>{r["type"]}").addTo(map)'
            for r in reserves
        )
        resto_js = ",\n        ".join(
            f'L.marker([{r["lat"]}, {r["lon"]}], {{icon: restoIcon}}).bindPopup("<b>🍽 {r["name"]}</b><br>{r["cuisine"]}").addTo(map)'
            for r in restaurants
        )
        attr_js = ",\n        ".join(
            f'L.marker([{a["lat"]}, {a["lon"]}], {{icon: attrIcon}}).bindPopup("<b>⭐ {a["name"]}</b><br>{a["type"]}").addTo(map)'
            for a in attractions
        )

        # ── Confiance ──
        confidence = int(analysis.get("confidence", 0) * 100)
        conf_class = "conf-high" if confidence >= 80 else "conf-med" if confidence >= 50 else "conf-low"
        action_label = "Validé" if analysis.get("action") == "validated" else "À vérifier"
        gmaps = f"https://www.google.com/maps/search/{lat},{lon}"

        # ── Photos source ──
        photos_html = ""
        for mf in meta.get("media_files", []):
            fp = PKA_ROOT / mf["file_path"]
            if fp.exists():
                import base64 as _b64
                img_b64 = _b64.standard_b64encode(fp.read_bytes()).decode()
                photos_html += f'<div class="photo-card"><img src="data:image/jpeg;base64,{img_b64}" alt="Photo source" loading="lazy"></div>'

        # ── Table attractions ──
        attr_table = ""
        for a in attractions:
            attr_table += f'<tr><td>{a["name"]}</td><td>{a["type"]}</td><td class="km">{_dist_km(a["lat"], a["lon"])}</td><td class="link"><a href="https://www.google.com/maps/place/{a["name"].replace(" ","+")}" target="_blank">🔗</a></td></tr>'

        # ── Table restos ──
        resto_table = ""
        for r in restaurants:
            cuisine = r['cuisine'] if r['cuisine'] else "—"
            resto_table += f'<tr><td>{r["name"]}</td><td>{cuisine}</td><td class="km">{_dist_km(r["lat"], r["lon"])}</td><td class="link"><a href="https://www.google.com/maps/place/{r["name"].replace(" ","+")}" target="_blank">🔗</a></td></tr>'

        # ── Scores ──
        def _stars(n: int) -> str:
            return "★" * n + "☆" * (5 - n)

        html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{nom_lieu} — PKA Découvertes</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
  :root {{ --ivoire: #F8F5F0; --noir: #0D0B09; --ocre: #C17F3A; --sable: #E8E2DA; --sable-fonce: #D4CCC2; --ardoise: #4A5568; --gris: #6B7280; }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--ivoire); color: var(--noir); font-family: 'Inter', -apple-system, sans-serif; font-size: 14px; line-height: 1.6; padding: 16px 14px; }}
  h1, h2, h3, th {{ font-weight: 700; }}
  h1 {{ font-size: 22px; color: var(--ocre); margin-bottom: 2px; }}
  h2 {{ font-size: 12px; color: var(--ocre); margin: 22px 0 6px; padding-bottom: 2px; border-bottom: 2px solid var(--sable); text-transform: uppercase; letter-spacing: 0.05em; }}
  h3 {{ font-size: 11px; color: var(--ardoise); margin: 10px 0 4px; font-weight: 600; }}
  .km, .price {{ font-family: 'IBM Plex Mono', monospace; font-size: 11px; color: var(--ardoise); }}
  .header {{ margin-bottom: 12px; padding-bottom: 8px; border-bottom: 3px solid var(--ocre); }}
  .header-meta {{ font-size: 10px; color: var(--gris); margin-top: 2px; }}
  .status {{ display: inline-block; background: var(--ocre); color: #fff; padding: 1px 8px; font-size: 9px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 2px; }}
  .tagline {{ font-weight: 400; color: var(--gris); font-size: 12px; }}
  .card {{ background: var(--sable); padding: 8px 12px; margin: 6px 0; font-size: 12px; }}
  .rules {{ background: var(--sable); padding: 8px 10px; margin: 6px 0; font-size: 11px; border-left: 4px solid var(--ocre); line-height: 1.6; }}
  .table-wrap {{ width: 100%; overflow-x: auto; margin: 6px 0 10px; }}
  table {{ width: 100%; border-collapse: collapse; font-size: 10px; min-width: 400px; }}
  th {{ background: var(--sable-fonce); color: var(--noir); font-weight: 600; font-size: 9px; text-transform: uppercase; letter-spacing: 0.04em; padding: 6px 6px; text-align: left; white-space: nowrap; }}
  td {{ padding: 5px 6px; border-bottom: 1px solid var(--sable); vertical-align: top; }}
  tr:last-child td {{ border-bottom: none; }}
  .link a {{ color: var(--ocre); text-decoration: none; font-size: 12px; padding: 2px 4px; }}
  .map-container {{ height: 260px; margin: 8px 0; border: 2px solid var(--sable); position: relative; z-index: 1; }}
  #map {{ height: 100%; }}
  .legend {{ background: rgba(255,255,255,0.95); padding: 5px 8px; border-radius: 4px; font: 10px/1.4 sans-serif; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }}
  .legend i {{ width: 10px; height: 10px; display: inline-block; margin-right: 4px; border-radius: 50%; vertical-align: middle; }}
  .stars {{ color: var(--ocre); font-size: 13px; letter-spacing: 2px; }}
  .photo-gallery {{ display: flex; gap: 8px; overflow-x: auto; padding: 4px 0; }}
  .photo-card {{ flex: 0 0 auto; border-radius: 4px; overflow: hidden; border: 1px solid var(--sable); }}
  .photo-card img {{ height: 140px; display: block; }}
  .conf-high {{ background: #d4edda; color: #155724; }}
  .conf-med {{ background: #fff3cd; color: #856404; }}
  .conf-low {{ background: #f8d7da; color: #721c24; }}
  .footer {{ text-align: center; padding: 16px; color: var(--gris); font-size: 9px; }}
  .footer a {{ color: var(--ocre); }}
  @media (max-width: 500px) {{ h1 {{ font-size: 18px; }} .map-container {{ height: 200px; }} .photo-card img {{ height: 100px; }} }}
</style>
</head>
<body>

<div class="header">
  <div class="status">{action_label}</div>
  <h1>📍 {nom_lieu}</h1>
  <div class="tagline">{ville}, {region}, {pays} · {today} · {confidence}%</div>
  <div class="header-meta">
    📷 {_stars(analysis.get("interet_photo", 0))} &nbsp; 🌳 {_stars(analysis.get("interet_nature", 0))} &nbsp; 🏛 {_stars(analysis.get("interet_patrimoine", 0))}
  </div>
</div>

<div class="card">{analysis.get("description", "")}</div>

<div class="map-container"><div id="map"></div></div>

<h2>📸 Spots photo <span style="font-weight:400;font-size:10px;color:var(--gris)">— saison · astuce</span></h2>
<div class="rules">📷 <strong>Meilleure saison</strong> : printemps (avril-juin) ou automne (septembre-octobre) pour lumière rasante sur {nom_lieu}<br>
🌅 <strong>Heure idéale</strong> : tôt le matin ou fin d'après-midi<br>
🔭 <strong>Point de vue</strong> : à repérer sur place — privilégier un point en hauteur avec recul<br>
💡 <strong>Astuce</strong> : trépied pour poses longues (rivière, cascade), filtre polarisant si ciel clair</div>

{"<h2>⭐ À voir aux alentours <span style='font-weight:400;font-size:10px;color:var(--gris)'>— 30 km</span></h2><div class='table-wrap'><table><tr><th>Lieu</th><th>Type</th><th>Dist</th><th>Maps</th></tr>" + attr_table + "</table></div>" if attr_table else ""}

{"<h2>🍽 Restaurants <span style='font-weight:400;font-size:10px;color:var(--gris)'>— 15 km</span></h2><div class='table-wrap'><table><tr><th>Nom</th><th>Cuisine</th><th>Dist</th><th>Maps</th></tr>" + resto_table + "</table></div>" if resto_table else ""}

<h2>🚐 Accès minivan <span style="font-weight:400;font-size:10px;color:var(--gris)">— Stylevan Equinox IV</span></h2>
<div class="rules">{van_info}</div>

{"<div class='card' style='margin-top:10px'><div class='photo-gallery'>" + photos_html + "</div></div>" if photos_html else ""}

<div class="footer">
  PKA Découvertes · {today} · Telegram DECOUVERTES · {meta.get("author", "")}<br>
  GPS {lat:.4f}, {lon:.4f} · <a href="{gmaps}" target="_blank">Google Maps</a>
</div>

<script>
const map = L.map("map").setView([{lat}, {lon}], 11);
L.tileLayer("https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png", {{ attribution: "&copy; OSM", maxZoom: 18 }}).addTo(map);
L.circle([{lat}, {lon}], {{ radius: 50000, color: "__SABLE__", fillColor: "__SABLE__", fillOpacity: 0.08, weight: 2, dashArray: "6 8" }}).addTo(map);
L.marker([{lat}, {lon}]).bindPopup("<b>📍 {nom_lieu}</b>").addTo(map).openPopup();

const reserveIcon = L.divIcon({{ className: "", html: "🌿", iconSize: [20, 20], iconAnchor: [10, 10] }});
{reserve_js if reserve_js else "// Aucune réserve"};

const restoIcon = L.divIcon({{ className: "", html: "🍽", iconSize: [20, 20], iconAnchor: [10, 10] }});
{resto_js if resto_js else "// Aucun resto"};

const attrIcon = L.divIcon({{ className: "", html: "⭐", iconSize: [20, 20], iconAnchor: [10, 10] }});
{attr_js if attr_js else "// Aucune attraction"};

L.circle([{lat}, {lon}], {{ radius: 25000, color: "__ROUTE__", fillColor: "__ROUTE__", fillOpacity: 0.03, weight: 1, dashArray: "3 6" }}).addTo(map);

const legend = L.control({{ position: "bottomright" }});
legend.onAdd = function() {{
    const div = L.DomUtil.create("div", "legend");
    div.innerHTML = "<b>Légende</b><br><i style='background:__SABLE__'></i> 50 km<br><i style='background:__ROUTE__'></i> 25 km<br>⭐ Site · 🌿 Réserve · 🍽 Resto";
    return div;
}};
legend.addTo(map);
</script>
</body>
</html>""".replace("__SABLE__", "#C17F3A").replace("__ROUTE__", "#6B7280")
        report_path.write_text(html, encoding="utf-8")
        return report_path
    except Exception as e:
        print(f"  [html] erreur génération rapport : {e}")
        return None

# ── Prompts ───────────────────────────────────────────────────────────────────

VISION_PROMPT_BASE = """Tu es l'agent PKA_DECOUVERTES. Analyse cette image.

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

# Prompt vision allégé — utilisé quand l'OCR a déjà extrait du texte.
# L'OCR fournit le texte visible ; le LLM n'analyse que le contenu visuel.
VISION_PROMPT_LIGHT = """Tu es l'agent PKA_DECOUVERTES. Analyse cette image.

Du texte a déjà été extrait de l'image par OCR (fourni ci-dessous en CONTEXTE).
Ton rôle : analyser uniquement les indices VISUELS que l'OCR ne peut pas lire.

Analyse :
- monuments, paysages, architecture caractéristique
- style régional (colombages alsaciens, toits en lauze, pierre dorée bourguignonne...)
- végétation, relief, côte, montagne, urbain
- drapeaux, plaques d'immatriculation, logos

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
Si le lieu est clairement identifiable, action = validated. Si incertain, action = needs_review.
"""

VISION_PROMPT = VISION_PROMPT_BASE  # rétrocompatibilité


def get_vision_prompt(hint: str | None = None, ocr_text: str | None = None) -> str:
    """Retourne le prompt vision adapté au contexte.

    - Si ocr_text est fourni : prompt allégé (analyse visuelle seule) + texte OCR en indice.
    - Si hint est fourni : prompt complet + indices utilisateur.
    - Sinon : prompt complet standard.
    """
    if ocr_text:
        return VISION_PROMPT_LIGHT + f"""

CONTEXTE (texte extrait de l'image par OCR — utilise ces indices en priorité) :
{ocr_text[:1500]}
"""
    if hint:
        return VISION_PROMPT_BASE + f"""

CONTEXTE FOURNI PAR L'UTILISATEUR (utilise ces indices en priorité) :
{hint}
"""
    return VISION_PROMPT_BASE

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

VAN_PROMPT = """Tu es un expert en voyage en minivan (hauteur 2m, longueur 5m, Stylevan Equinox IV Ford).

Lieu : {nom_lieu}, {region}, {pays}
Type : {type_lieu}
Description : {description}

Rédige une section pratique pour un voyageur en minivan. Sois TRÈS concret — donne des noms, distances en km, tarifs en € si connus.

1. **Accès** : type de route (D, N, A), état, praticabilité pour 2m de haut
2. **Parking** : nom du parking le plus proche, hauteur max en mètres, gratuit/payant (tarif)
3. **Nuit sur place** : camping-car autorisé ? aire officielle la plus proche (nom + distance km) ? stationnement nocturne toléré ?
4. **Services** : borne eau/électricité/vidange la plus proche (nom + km), supermarché (nom + km)
5. **Astuce vanlife** : meilleure saison, durée visite, heure idéale pour photos, spot secret si connu

Si tu ne connais pas un détail précis, ne l'invente pas — écris "à vérifier sur place".
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

def process_item(
    json_path: Path, model_arg: str,
    cascade_order: list[str] | None = None,
    cascade_threshold: float = CASCADE_THRESHOLD,
    hint: str | None = None,
) -> bool:
    meta = json.loads(json_path.read_text())
    slug = json_path.stem
    content_type = meta.get("content_type", "text")

    print(f"\n[{slug}] type={content_type} auteur={meta.get('author')}")

    # ── Analyse vision ou texte ────────────────────────────────────────────
    try:
        if meta.get("media_files") and content_type in ("photo", "image", "image_with_caption", "screenshot"):
            img_path = PKA_ROOT / meta["media_files"][0]["file_path"]
            if not img_path.exists():
                print(f"  Image introuvable : {img_path}")
                return False
            image_b64 = base64.standard_b64encode(img_path.read_bytes()).decode()
            print(f"  Vision → {img_path.name} ({img_path.stat().st_size // 1024} Ko)")

            # ── Pipeline OCR → EXIF → Cache → Vision ──────────────────────
            ocr_text = None
            exif_gps = None
            ocr_place = None

            # 1. EXIF GPS
            exif_gps = extract_exif_gps(img_path)
            if exif_gps:
                print(f"  📍 EXIF GPS : {exif_gps['lat']:.4f}, {exif_gps['lon']:.4f}")

            # 2. OCR
            if HAS_TESSERACT:
                ocr_text = ocr_extract_text(img_path)
                if ocr_text:
                    print(f"  🔍 OCR : {len(ocr_text)} caractères extraits")
                    ocr_place = extract_place_from_text(ocr_text)
                    if ocr_place:
                        print(f"  🏷 Lieu OCR détecté : {ocr_place}")

            # 3. Cache — si le lieu a déjà été identifié par OCR, vérifier le cache
            if ocr_place:
                cache = _load_cache()
                ck = _cache_key(ocr_place)
                if ck in cache:
                    cached = cache[ck]
                    print(f"  ⏭ Déjà analysé le {cached['date']} → skipping")
                    meta["analysis_status"] = "cached"
                    meta["cached_from"] = cached["date"]
                    json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
                    return False

            # 4. Construire le hint composite (EXIF + OCR + hint manuel)
            composite_hint = hint or ""
            if exif_gps:
                gps_hint = f"GPS: {exif_gps['lat']:.4f}, {exif_gps['lon']:.4f}"
                composite_hint = f"{gps_hint}\n{composite_hint}".strip()

            # 5. Analyse : OCR → texte seul, ou OCR+hint → vision légère, ou vision complète
            if ocr_place:
                # OCR a trouvé un nom de lieu → analyse texte seule (pas d'appel vision)
                print(f"  📝 Analyse texte seule (OCR: {ocr_place})")
                analysis = None
                if cascade_order:
                    analysis = analyze_with_cascade(
                        cascade_order, cascade_threshold,
                        "text", None, ocr_place,
                    )
                else:
                    raw = call_model(model_arg, TEXT_PROMPT.format(text=ocr_place))
                    analysis = _extract_json(raw)
            elif ocr_text or composite_hint:
                # OCR a trouvé du texte mais pas de lieu clair, ou on a un hint
                # → vision allégée avec le texte OCR en indice
                prompt_hint = ocr_text if ocr_text else composite_hint
                is_ocr = bool(ocr_text)
                print(f"  👁 Vision {'allégée (OCR)' if is_ocr else '(hint)'} → {len(prompt_hint)} chars d'indices")
                if cascade_order:
                    # Pour la cascade avec OCR, on passe le hint au lieu de l'ocr_text
                    analysis = analyze_with_cascade(
                        cascade_order, cascade_threshold,
                        content_type, image_b64, "",
                        hint=composite_hint,
                    )
                else:
                    raw = call_model(
                        model_arg,
                        get_vision_prompt(hint=composite_hint if not ocr_text else None, ocr_text=ocr_text),
                        image_b64,
                    )
                    analysis = _extract_json(raw)
            else:
                # Pas d'OCR, pas de hint → vision complète standard
                print("  👁 Vision complète (pas d'OCR)")
                if cascade_order:
                    analysis = analyze_with_cascade(
                        cascade_order, cascade_threshold,
                        content_type, image_b64, "",
                    )
                else:
                    raw = call_model(model_arg, get_vision_prompt(), image_b64)
                    analysis = _extract_json(raw)

        else:
            text = meta.get("text", "")
            if not text.strip():
                print("  Message vide — ignoré")
                return False
            print(f"  Texte → {text[:60]!r}")

            if cascade_order:
                analysis = analyze_with_cascade(cascade_order, cascade_threshold, content_type, None, text)
            else:
                raw = call_model(model_arg, TEXT_PROMPT.format(text=text))
                analysis = _extract_json(raw)

        if analysis is None:
            print("  Aucun modèle n'a identifié de lieu")
            meta["analysis_status"] = "skipped"
            json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
            return False

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

    # ── Cache : sauvegarder pour déduplication future ──────────────────
    nom_lieu = analysis.get("nom_lieu", "")
    if nom_lieu:
        cache = _load_cache()
        ck = _cache_key(nom_lieu)
        cache[ck] = {
            "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
            "nom_lieu": nom_lieu,
        }
        _save_cache(cache)

    # ── GPS via Nominatim
    gps = geocode(analysis)
    if gps:
        print(f"  GPS : {gps['lat']:.4f}, {gps['lon']:.4f}")
        # ── CSV Google Maps cumulatif
        _append_google_maps_csv(analysis, gps)
        print(f"  📍 → {GMAPS_CSV.name}")
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

    # ── Réserves naturelles, attractions, restaurants & rapport HTML
    reserves = []
    attractions = []
    restaurants = []
    report_path = None
    if gps:
        print("  Overpass → réserves naturelles (25 km)...")
        reserves = get_nature_reserves(gps["lat"], gps["lon"], radius_km=25)
        for r in reserves:
            print(f"    🌿 {r['name']} ({r['type']})")

        print("  Overpass → attractions touristiques (30 km)...")
        attractions = get_nearby_attractions(gps["lat"], gps["lon"], radius_km=30)
        for a in attractions:
            print(f"    ⭐ {a['name']} ({a['type']})")

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
            reserves, restaurants, attractions,
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
    parser.add_argument(
        "--cascade", action="store_true",
        help="Mode cascade : essaie les modèles dans l'ordre jusqu'à confiance >= seuil",
    )
    parser.add_argument(
        "--cascade-order", type=str, default=",".join(CASCADE_ORDER),
        help=f"Ordre des modèles en cascade (défaut: {','.join(CASCADE_ORDER)})",
    )
    parser.add_argument(
        "--cascade-threshold", type=float, default=CASCADE_THRESHOLD,
        help=f"Seuil de confiance pour arrêter la cascade (défaut: {CASCADE_THRESHOLD})",
    )
    parser.add_argument(
        "--hint", type=str, default=None,
        help="Indices contextuels à fournir au modèle (ex: 'village alpin français, colombages, torrent')",
    )
    args = parser.parse_args()

    cascade_order = None
    if args.cascade:
        cascade_order = [m.strip() for m in args.cascade_order.split(",")]
        print(f"Cascade : {' → '.join(cascade_order)} (seuil {int(args.cascade_threshold*100)}%)")
    else:
        print(f"Modèle : {args.model}")

    pending = sorted(QUEUE_DIR.glob("*.json"))
    # Filtrer uniquement les non encore analysés
    pending = [p for p in pending
               if json.loads(p.read_text()).get("analysis_status") == "pending"]

    if not pending:
        print("Queue vide — aucun élément en attente.")
        return

    print(f"Éléments en attente : {len(pending)}")
    if args.limit:
        pending = pending[:args.limit]
        print(f"Limite : {args.limit}")

    ok = 0
    for path in pending:
        if process_item(path, args.model, cascade_order, args.cascade_threshold, args.hint):
            ok += 1

    print(f"\nTerminé — {ok}/{len(pending)} fiches générées dans drafts/")


if __name__ == "__main__":
    main()