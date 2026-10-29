#!/usr/bin/env python3
"""
heron_paper.py
Héron 🦢 — Recommandation papier d'impression personnalisée.
Se base sur les données photo (couleur dominante, scores, sujet) pour
conseiller le papier optimal sur l'Epson ET8550.

Usage :
  python3 heron_paper.py --image-id ID_DB
  python3 heron_paper.py --filename "LrC to-9.jpg"
  from heron_paper import recommend   # usage depuis run_analysis.py
"""

import argparse
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "PHOTO" / "argus_critique.db"

# ── Catalogue papiers ET8550 ──────────────────────────────────────────────────
PAPERS = {
    "baryta": {
        "nom":         "Baryta Photographique 310g",
        "fini":        "Semi-brillant",
        "dmax":        2.4,
        "profil":      "Epson Enhanced Matte / profil ICC baryta custom",
        "forces":      "Noir profond, microcontraste exceptionnel, rendu argentique",
        "limites":     "Reflets sous lumière directe, coût élevé",
        "ideal_pour":  "Portraits serrés, forts contrastes, détail plumes/fourrure, N&B",
    },
    "lustre": {
        "nom":         "Lustre Premium 260g",
        "fini":        "Semi-brillant texturé",
        "dmax":        2.2,
        "profil":      "Epson Premium Lustre Photo Paper",
        "forces":      "Piqué maximal, couleurs saturées, polyvalent, reflets contrôlés",
        "limites":     "Moins de profondeur que la baryta",
        "ideal_pour":  "Action, oiseaux en vol, sujets nets sur fond épuré",
    },
    "fine_art_cotton": {
        "nom":         "Fine Art Cotton Smooth 300g",
        "fini":        "Mat texturé",
        "dmax":        1.8,
        "profil":      "Epson Ultra Premium Presentation Matte",
        "forces":      "Blanc chaud, texture sensible, zéro reflet, rendu peinture",
        "limites":     "Noirs moins profonds, moins adapté aux photos très contrastées",
        "ideal_pour":  "Ambiances douces, lumière rasante, tons pastels, paysages brumeux",
    },
    "metallique": {
        "nom":         "Papier Métallique 260g",
        "fini":        "Brillant métallisé",
        "dmax":        2.3,
        "profil":      "Epson Metallic Photo Paper",
        "forces":      "Amplification tons chauds, effet lumineux spectaculaire",
        "limites":     "Reflets intenses, ne convient pas aux tons froids",
        "ideal_pour":  "Golden hour, flamants, couchers de soleil, sujets à dominante chaude",
    },
    "coton_texture": {
        "nom":         "Coton Texturé Aquarelle 300g",
        "fini":        "Mat grainé",
        "dmax":        1.7,
        "profil":      "Epson Enhanced Matte",
        "forces":      "Grain visible, très artistique, zéro reflet",
        "limites":     "Pertes de détail fin, noirs peu profonds",
        "ideal_pour":  "Séries artistiques, macro flore, ambiances contemplatives",
    },
    "premium_glossy": {
        "nom":         "Premium Glossy Photo 255g",
        "fini":        "Brillant",
        "dmax":        2.35,
        "profil":      "Epson Premium Glossy Photo Paper",
        "forces":      "Couleurs vives, rapport qualité/prix, usage album",
        "limites":     "Empreintes digitales, reflets forts",
        "ideal_pour":  "Albums, tirages format moyen, usage quotidien",
    },
}


def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    h = hex_str.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))


def color_temperature(r: int, g: int, b: int) -> str:
    """Chaud / neutre / froid selon dominante RGB."""
    if r > b + 20:   return "chaud"
    if b > r + 20:   return "froid"
    return "neutre"


def contrast_level(score_exposition: int, score_technique: int) -> str:
    mean = (score_exposition + score_technique) / 2
    if mean >= 16:   return "fort"
    if mean >= 13:   return "moyen"
    return "faible"


def recommend(data: dict) -> dict:
    """
    data doit contenir :
      avg_color_hex, score_exposition, score_nettete, score_technique,
      score_impact, score_total, tier, species (ou subject)
    Retourne {paper_key, paper, reason, second_choice, second_reason}
    """
    avg_hex  = data.get("avg_color_hex") or data.get("avg_color", {}).get("hex", "#888888")
    r, g, b  = hex_to_rgb(avg_hex)
    temp     = color_temperature(r, g, b)
    contrast = contrast_level(
        data.get("score_exposition", 14),
        data.get("score_technique",  14),
    )
    impact   = data.get("score_impact", 14)
    nettete  = data.get("score_nettete", 14)
    tier     = data.get("tier", "TRÈS BON")
    species  = data.get("species", "")

    # ── Logique de recommandation ─────────────────────────────────────────────

    # Sujet macro / flore / texture fine
    macro_keywords = ["macro", "fleur", "insect", "araign", "platane", "raiponce",
                      "champignon", "lichen", "mousse"]
    is_macro = any(k in species.lower() for k in macro_keywords)

    # Sujet action / oiseau en vol
    action_keywords = ["vol", "envol", "plongeon", "attaque", "capture", "chasse"]
    is_action = any(k in species.lower() for k in action_keywords)

    # Tons chauds : flamants, golden hour, renards, rapaces
    warm_keywords = ["flamant", "renard", "buse", "faucon", "aigle", "autour",
                     "coucher", "golden", "amber"]
    is_warm = temp == "chaud" or any(k in species.lower() for k in warm_keywords)

    # Ambiance douce / brume
    soft_keywords = ["brume", "brouillard", "neige", "givre", "hivern", "matin",
                     "cygneau", "petit", "jeune"]
    is_soft = any(k in species.lower() for k in soft_keywords)

    # Choix principal
    if is_warm:
        paper_key = "metallique"
        reason = (f"La dominante chaude de votre image ({avg_hex}) sera amplifiée "
                  f"par l'effet métallisé — les tons orangés et dorés prennent une "
                  f"profondeur lumineuse impossible à obtenir sur papier standard.")
        second_key = "lustre"
        second_reason = "Alternative plus sobre si vous préférez un rendu naturel sans effet."

    elif is_macro:
        paper_key = "coton_texture"
        reason = (f"Le grain du coton texturé apporte un souffle artistique aux sujets "
                  f"proches — il transforme une photo technique en œuvre sensible. "
                  f"Idéal pour vos macros où la texture prime sur le contraste.")
        second_key = "fine_art_cotton"
        second_reason = "Surface plus lisse si vous voulez conserver la précision des détails fins."

    elif is_action or nettete >= 16:
        paper_key = "lustre"
        reason = (f"Votre netteté ({nettete}/20) mérite un papier qui restitue chaque "
                  f"détail sans compromis. Le lustre offre le piqué maximal de notre "
                  f"gamme avec des reflets contrôlés — idéal pour les sujets nets sur fond épuré.")
        second_key = "baryta"
        second_reason = "Si votre photo a de forts contrastes, la baryta offrira des noirs encore plus profonds."

    elif is_soft or temp == "froid":
        paper_key = "fine_art_cotton"
        reason = (f"La dominante froide ({avg_hex}) et l'ambiance de votre image "
                  f"s'accorderont avec le blanc légèrement chaud du coton — "
                  f"il équilibre la froideur sans la trahir. La texture mat élimine "
                  f"tout reflet et donne une présence apaisante à l'impression.")
        second_key = "baryta"
        second_reason = "Si les noirs sont importants dans votre image, la baryta offrira plus de profondeur."

    elif contrast == "fort" or tier in ("EXCELLENT", "EXCEPTIONNEL"):
        paper_key = "baryta"
        reason = (f"Votre photo ({tier}, {data.get('score_total', 80)}/100) a le niveau "
                  f"pour tirer le meilleur d'un papier noble. La baryta offre le D-max "
                  f"le plus élevé de notre gamme — les noirs sont absolus, les hautes "
                  f"lumières restituées avec précision. C'est le papier des tirages "
                  f"d'exposition.")
        second_key = "lustre"
        second_reason = "Alternative moins coûteuse avec un excellent rendu si vous prévoyez plusieurs tirages."

    else:
        paper_key = "lustre"
        reason = ("Papier polyvalent et fiable — excellent rapport qualité/prix pour "
                  "un tirage soigné sans contrainte particulière.")
        second_key = "premium_glossy"
        second_reason = "Pour un album ou un usage quotidien à moindre coût."

    return {
        "paper_key":     paper_key,
        "paper":         PAPERS[paper_key],
        "reason":        reason,
        "second_key":    second_key,
        "second_choice": PAPERS[second_key],
        "second_reason": second_reason,
    }


def format_recommendation(rec: dict, species: str = "", score: int = 0) -> str:
    p  = rec["paper"]
    p2 = rec["second_choice"]
    lines = [
        f"## 🦢 Héron — Conseil Papier",
        f"",
        f"{'**Photo :** ' + species + '  ' if species else ''}",
        f"{'**Score :** ' + str(score) + '/100  ' if score else ''}",
        f"",
        f"### Recommandation principale : {p['nom']}",
        f"",
        f"> {rec['reason']}",
        f"",
        f"| | |",
        f"|--|--|",
        f"| Fini | {p['fini']} |",
        f"| D-max | {p['dmax']} |",
        f"| Profil ICC | `{p['profil']}` |",
        f"| Idéal pour | {p['ideal_pour']} |",
        f"| Limite | {p['limites']} |",
        f"",
        f"### Second choix : {p2['nom']}",
        f"",
        f"> {rec['second_reason']}",
        f"",
        f"---",
        f"*Conseil Héron 🦢 — Epson ET8550 · Service ARTEON*",
    ]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Héron — Recommandation papier")
    parser.add_argument("--image-id",  type=int,  default=None)
    parser.add_argument("--filename",  default=None)
    parser.add_argument("--client",    default="JCH")
    args = parser.parse_args()

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row

    if args.image_id:
        row = con.execute("SELECT * FROM analyses WHERE id=?", (args.image_id,)).fetchone()
    elif args.filename:
        row = con.execute(
            "SELECT * FROM analyses WHERE filename=? AND client_id=? ORDER BY id DESC LIMIT 1",
            (args.filename, args.client)
        ).fetchone()
    else:
        # Dernière analyse du client
        row = con.execute(
            "SELECT * FROM analyses WHERE client_id=? ORDER BY id DESC LIMIT 1",
            (args.client,)
        ).fetchone()
    con.close()

    if not row:
        print("❌ Photo non trouvée dans la base.")
        return

    data = dict(row)
    rec  = recommend(data)
    print(format_recommendation(rec, data.get("species", ""), data.get("score_total", 0)))


if __name__ == "__main__":
    main()
