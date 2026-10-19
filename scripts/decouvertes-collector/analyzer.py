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
import hashlib
import json
import os
import re
import sys
import shutil
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
HAS_TESSERACT_CLI = shutil.which("tesseract") is not None

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
GMAPS_CSV_HEADER = "Name,Description,Latitude,Longitude,Country,Region"

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
        desc = " · ".join(x for x in (pays, region, type_lieu) if x and str(x).strip())
        w.writerow([nom, desc, gps["lat"], gps["lon"], pays, region])

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
    """Extrait le texte via tesseract CLI (subprocess) — indépendant de pytesseract.

    Stratégie multi-passe : couleur PSM 6 → couleur PSM 3 → N&B PSM 6.
    Langue : eng (les packs fra/ita/deu ne sont pas installés sur cette machine).
    """
    import subprocess
    import tempfile

    if not shutil.which("tesseract"):
        return None
    candidates = []
    try:
        for psm in ("6", "3"):
            out = subprocess.run(
                ["tesseract", str(image_path), "stdout", "-l", "eng", "--psm", psm],
                capture_output=True, text=True, timeout=40,
            )
            t = out.stdout.strip()
            if t:
                candidates.append(t)

        # Passe N&B PSM 6 (fallback textes difficiles)
        if HAS_PIL:
            try:
                img = Image.open(image_path).convert("L")
                with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as tf:
                    img.save(tf.name)
                    nb_path = tf.name
                out = subprocess.run(
                    ["tesseract", nb_path, "stdout", "-l", "eng", "--psm", "6"],
                    capture_output=True, text=True, timeout=40,
                )
                t = out.stdout.strip()
                if t:
                    candidates.append(t)
            except Exception:
                pass

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

def extract_address_cities(text: str) -> list[str]:
    """Extrait les villes depuis des adresses type « Via X 34, Ville, Provincia di Y ».

    Les posts Instagram de lieux contiennent souvent l'adresse complète — la ville y
    est le meilleur ancrage géographique, mieux que le titre/la légende.
    """
    cities = []
    for m in re.finditer(
        r'(?:Via|Piazza|Corso|Viale|Strada|Località|Contrada|Largo|Borgo)\s+'
        r'[\w\s\.\d\'\-]{1,60}?,\s*'
        r'([A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\']+(?:\s+(?:di|del|de|della|delle|dei|degli|du|des|sur|en|in)\s+[A-ZÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ][\w\-\']+){0,3})',
        text,
    ):
        cities.append(m.group(1).strip())
    return cities


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

    # ── Adresse → ville (ex: "Via X, Cividale del Friuli, Provincia di Udine") ──
    for city in extract_address_cities(text):
        if city.lower() not in {r.lower() for r in results}:
            results.append(city)

    # ── Fallback : lieu unique (toujours tenté, dédupliqué) ──────────────
    single = extract_place_from_text(text)
    if single and single.lower() not in {r.lower() for r in results}:
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

def call_claude(model_id: str, prompt: str) -> str:
    """Appel texte uniquement — pas de vision."""
    import anthropic
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    resp = client.messages.create(
        model=model_id,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )
    return resp.content[0].text


def call_ollama(model_name: str, prompt: str) -> str:
    """Appel texte uniquement — pas de vision."""
    payload: dict = {
        "model": model_name,
        "messages": [{"role": "user", "content": prompt}],
        "stream": False,
    }
    resp = requests.post(f"{OLLAMA_BASE}/api/chat", json=payload, timeout=120)
    resp.raise_for_status()
    return resp.json()["message"]["content"]


def call_model(model_arg: str, prompt: str) -> str:
    """Appel LLM texte uniquement."""
    if model_arg.startswith("ollama:"):
        return call_ollama(model_arg[7:], prompt)
    model_id = CLAUDE_MODELS.get(model_arg)
    if not model_id:
        raise ValueError(f"Modèle inconnu : {model_arg}. Choix : haiku, sonnet, opus, ollama:<name>")
    return call_claude(model_id, prompt)


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
    model_order: list[str], threshold: float, text: str,
) -> dict | None:
    """Essaie les modèles dans l'ordre jusqu'à obtenir une confiance >= threshold."""
    best = None
    best_conf = -1.0

    for i, model_arg in enumerate(model_order):
        arrow = "→" if i > 0 else ""
        print(f"  {arrow} {model_arg}...", end=" ", flush=True)
        try:
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
        f"{analysis.get('nom_lieu')} {analysis.get('ville')} {analysis.get('pays')}",
        f"{analysis.get('nom_lieu')} {analysis.get('region')} {analysis.get('pays')}",
        analysis.get("nom_lieu"),
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


# ── Prompt ────────────────────────────────────────────────────────────────────
# (Vision prompts archivés dans analyzer_archive_vision.py — pipeline OCR→texte uniquement)

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

def slugify(name: str) -> str:
    """Slug sûr pour URL/nom de fichier : [A-Za-z0-9._-], sans accents, tronqué à 40."""
    import unicodedata
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[^A-Za-z0-9._-]+", "-", s).strip("-")
    return s[:40] or "lieu"


def generate_place_json(
    lat: float, lon: float,
    analysis: dict, van_info: str, meta: dict,
    reserves: list[dict], restaurants: list[dict], attractions: list[dict],
    data_dir: Path, slug: str, today: str,
) -> Path | None:
    """Écrit les données structurées d'un lieu en JSON (consommé par place.html)."""
    try:
        data_dir.mkdir(parents=True, exist_ok=True)
        media_files = [mf.get("file_path") for mf in meta.get("media_files", [])]
        payload = {
            "slug": slug,
            "nom_lieu": analysis.get("nom_lieu", "Lieu inconnu"),
            "pays": analysis.get("pays", ""),
            "region": analysis.get("region", ""),
            "ville": analysis.get("ville", ""),
            "gps": {"lat": lat, "lon": lon},
            "scores": {
                "photo": analysis.get("interet_photo", 0),
                "nature": analysis.get("interet_nature", 0),
                "patrimoine": analysis.get("interet_patrimoine", 0),
                "van": analysis.get("interet_van", 0),
            },
            "type_lieu": analysis.get("type_lieu", ""),
            "confidence": analysis.get("confidence", 0),
            "action": analysis.get("action", "needs_review"),
            "description": analysis.get("description", ""),
            "van_info": van_info,
            "reserves": reserves,
            "restaurants": restaurants,
            "attractions": attractions,
            "media_files": media_files,
            "source": {
                "author": meta.get("author", ""),
                "datetime": meta.get("datetime", ""),
                "text": meta.get("text", ""),
            },
            "date_analyse": today,
        }
        path = data_dir / f"{slug}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return path
    except Exception as e:
        print(f"  [json] erreur génération données : {e}")
        return None


# ── Génération fiche Obsidian ─────────────────────────────────────────────────

def generate_note(
    meta: dict, analysis: dict, van_info: str, gps: dict | None,
    reserves: list[dict] | None = None,
    restaurants: list[dict] | None = None,
    slug: str | None = None,
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
        f"[📄 Ouvrir la fiche interactive](http://127.0.0.1:8787/place.html?name={slug})" if slug else "_Fiche non disponible_"
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

    # ── Pipeline OCR → LLM texte ─────────────────────────────────────────
    try:
        if meta.get("media_files") and content_type in ("photo", "image", "image_with_caption", "screenshot"):
            img_path = PKA_ROOT / meta["media_files"][0]["file_path"]
            if not img_path.exists():
                print(f"  Image introuvable : {img_path}")
                return False
            print(f"  📷 {img_path.name} ({img_path.stat().st_size // 1024} Ko)")

            # 1. OCR
            ocr_text = None
            ocr_places = []
            if HAS_TESSERACT_CLI:
                ocr_text = ocr_extract_text(img_path)
                if ocr_text:
                    print(f"  🔍 OCR : {len(ocr_text)} caractères")
                    ocr_places = extract_places_from_text(ocr_text)
                    if ocr_places:
                        for place in ocr_places:
                            print(f"  🏷 {place}")
                    else:
                        print(f"  ⚠️ Aucun lieu détecté dans le texte OCR")
                else:
                    print(f"  ⚠️ OCR vide")
            else:
                print(f"  ⚠️ pytesseract non installé")

            # 2. Si pas de lieu trouvé → skip
            if not ocr_places:
                print(f"  ⏭ Rien à analyser")
                meta["analysis_status"] = "skipped"
                json_path.write_text(json.dumps(meta, ensure_ascii=False, indent=2))
                return False

            # 3. Construire le texte LLM : candidats + texte OCR complet (tronqué)
            #    Corrige les échecs où le 1er candidat regex est faux/générique
            #    ("CASTELLO DA" vs "Castello di Duino", "Santa Maria" vs l'adresse).
            candidates = " | ".join(ocr_places)
            ocr_trim = (ocr_text or "").strip()
            text_for_llm = f"{candidates}\n\nTexte OCR complet :\n{ocr_trim[:1600]}"

        else:
            text_for_llm = meta.get("text", "")
            if not text_for_llm.strip():
                print("  Message vide — ignoré")
                return False
            print(f"  Texte → {text_for_llm[:60]!r}")

        # 4. Appel LLM texte
        if cascade_order:
            analysis = analyze_with_cascade(cascade_order, cascade_threshold, text_for_llm)
        else:
            raw = call_model(model_arg, TEXT_PROMPT.format(text=text_for_llm))
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

    # ── Réserves naturelles, attractions, restaurants & données lieu
    reserves = []
    attractions = []
    restaurants = []
    data_path = None
    slug = slugify(analysis.get("nom_lieu", "lieu-inconnu"))
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
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

        print("  JSON → données lieu...")
        data_path = generate_place_json(
            gps["lat"], gps["lon"],
            analysis, van_info, meta,
            reserves, restaurants, attractions,
            BASE / "data", slug, today,
        )
        if data_path:
            print(f"    → data/{data_path.name}")

    # ── Fiche Obsidian
    note = generate_note(meta, analysis, van_info, gps, reserves, restaurants, slug)
    note_path = DRAFTS_DIR / f"{today}_{slug}.md"
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