#!/usr/bin/env python3
"""
generate_keyword_gallery.py — HTML visual gallery from photo keyword cache.
One card per photo: thumbnail left, keywords right, grouped by category.

Usage:
  python3 scripts/generate_keyword_gallery.py --cache 06_PHOTO_NATURE/keyword_cache.json --photo-dir "/Users/jchavauxm5/Desktop/LrC To /" --output PHOTO/keyword_gallery.html
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# ── Color palette per keyword category ────────────────────────────────────────
CAT_COLORS = {
    "Faune":         "#4CAF50",   # green
    "Flore":         "#8BC34A",   # light green
    "Comportement":  "#FF9800",   # orange
    "Saison":        "#2196F3",   # blue
    "Moment":        "#03A9F4",   # light blue
    "Lumière":       "#FFC107",   # amber
    "Composition":   "#9C27B0",   # purple
    "Habitat":       "#795548",   # brown
    "Technique":     "#607D8B",   # blue grey
    "Ambiance":      "#E91E63",   # pink
    "Auto":          "#9E9E9E",   # grey
    "paysage":       "#00BCD4",   # cyan
}

def kw_category(kw: str) -> str:
    """Extract top-level category from keyword like 'Faune|oiseau|mésange'."""
    return kw.split("|")[0] if "|" in kw else "paysage"

def kw_label(kw: str) -> str:
    """Extract display label: everything after first |, or whole string."""
    parts = kw.split("|")
    return " › ".join(parts[1:]) if len(parts) > 1 else kw

def group_keywords(keywords: list[str]) -> dict[str, list[str]]:
    """Group flat keywords by category, sorted by category priority."""
    order = ["Faune", "Flore", "Comportement", "Saison", "Moment",
             "Lumière", "Composition", "Habitat", "Technique", "Ambiance", "Auto", "paysage"]
    groups: dict[str, list[str]] = {k: [] for k in order}
    for kw in keywords:
        cat = kw_category(kw)
        if cat in groups:
            groups[cat].append(kw_label(kw))
        else:
            if "autres" not in groups:
                groups["autres"] = []
            groups["autres"].append(kw_label(kw))
    return {k: v for k, v in groups.items() if v}


def generate_html(cache_path: str, photo_dir: str, output_path: str):
    """Read cache, generate HTML gallery."""

    cache = json.loads(Path(cache_path).read_text())
    photo_base = Path(photo_dir).expanduser().resolve()

    # Build cards
    cards = []
    for fp, entry in cache.items():
        fname = entry.get("file", "unknown")
        kws = entry.get("keywords", [])
        conf = entry.get("confidence", 0)
        img_path = photo_base / fname

        # Check if image still exists
        if not img_path.exists():
            # Try in subdirs
            candidates = list(photo_base.rglob(fname))
            img_path = candidates[0] if candidates else photo_base / fname

        rel_path = str(img_path.resolve()) if img_path.exists() else ""

        groups = group_keywords(kws)

        # Build keyword HTML blocks
        kw_html = ""
        for cat, items in groups.items():
            color = CAT_COLORS.get(cat, "#757575")
            kw_html += f'<div class="kw-group"><span class="kw-cat" style="background:{color}">{cat}</span>'
            for item in items:
                kw_html += f'<span class="kw-tag">{item}</span>'
            kw_html += '</div>'

        conf_pct = int(conf * 100) if isinstance(conf, (int, float)) else 0
        conf_color = "#4CAF50" if conf_pct >= 70 else "#FF9800" if conf_pct >= 40 else "#f44336"

        card = f"""
    <div class="card">
      <div class="card-left">
        <a href="file://{rel_path}" target="_blank">
          <img src="file://{rel_path}" loading="lazy" onerror="this.style.display='none'">
        </a>
      </div>
      <div class="card-right">
        <div class="card-header">
          <span class="card-filename">{fname}</span>
          <span class="card-conf" style="color:{conf_color}">{conf_pct}%</span>
        </div>
        <div class="card-kw">{kw_html}</div>
      </div>
    </div>"""
        cards.append(card)

    # Build full HTML
    html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Photo Keyword Gallery — {len(cards)} images</title>
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #1a1a2e; color: #eee; padding: 20px; }}
  h1 {{ text-align: center; margin-bottom: 8px; font-size: 1.5em; color: #fff; }}
  .subtitle {{ text-align: center; margin-bottom: 24px; color: #888; font-size: 0.9em; }}

  .controls {{
    display: flex; gap: 8px; flex-wrap: wrap; justify-content: center; margin-bottom: 24px;
  }}
  .filter-btn {{
    padding: 6px 14px; border: 1px solid #444; border-radius: 16px; background: #16213e; color: #ddd;
    cursor: pointer; font-size: 0.85em; transition: all .15s;
  }}
  .filter-btn:hover {{ background: #0f3460; border-color: #666; }}
  .filter-btn.active {{ background: #533483; border-color: #7b2ff7; color: #fff; }}

  .gallery {{ display: flex; flex-direction: column; gap: 12px; max-width: 1000px; margin: 0 auto; }}

  .card {{
    display: flex; gap: 16px; background: #16213e; border-radius: 10px; overflow: hidden;
    border: 1px solid #2a2a4a; transition: border-color .2s;
  }}
  .card:hover {{ border-color: #533483; }}

  .card-left {{
    flex: 0 0 220px; display: flex; align-items: center; justify-content: center;
    background: #0a0a1a; min-height: 150px; overflow: hidden;
  }}
  .card-left img {{
    max-width: 220px; max-height: 180px; object-fit: contain; display: block;
  }}

  .card-right {{ flex: 1; padding: 14px 16px; display: flex; flex-direction: column; gap: 8px; }}

  .card-header {{ display: flex; justify-content: space-between; align-items: center; }}
  .card-filename {{ font-weight: 600; font-size: 0.95em; color: #fff; }}
  .card-conf {{ font-weight: 700; font-size: 0.85em; }}

  .card-kw {{ display: flex; flex-direction: column; gap: 6px; }}

  .kw-group {{ display: flex; flex-wrap: wrap; align-items: center; gap: 5px; }}
  .kw-cat {{
    padding: 2px 8px; border-radius: 10px; font-size: 0.7em; font-weight: 700;
    text-transform: uppercase; letter-spacing: .5px; color: #fff; margin-right: 2px;
  }}
  .kw-tag {{
    padding: 2px 8px; border-radius: 4px; font-size: 0.78em;
    background: #0f3460; color: #ccc;
  }}

  .stats {{ text-align: center; margin-top: 32px; padding: 16px; color: #666; font-size: 0.8em; border-top: 1px solid #2a2a4a; }}

  .card.hidden {{ display: none; }}

  @media (max-width: 640px) {{
    .card {{ flex-direction: column; }}
    .card-left {{ flex: 0 0 auto; max-height: 200px; }}
    .card-left img {{ max-width: 100%; max-height: 200px; }}
  }}
</style>
</head>
<body>

<h1>🦉 Photo Keyword Gallery</h1>
<div class="subtitle">{len(cards)} images · Généré le {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}</div>

<div class="controls" id="controls">
  <button class="filter-btn active" onclick="filter('all')">Toutes</button>
  <button class="filter-btn" onclick="filter('Faune')">🐾 Faune</button>
  <button class="filter-btn" onclick="filter('Flore')">🌿 Flore</button>
  <button class="filter-btn" onclick="filter('paysage')">🏔 Paysage</button>
  <button class="filter-btn" onclick="filter('Comportement')">🎬 Comportement</button>
  <button class="filter-btn" onclick="filter('Lumière')">💡 Lumière</button>
  <button class="filter-btn" onclick="filter('Printemps')">🌸 Printemps</button>
  <button class="filter-btn" onclick="filter('Automne')">🍂 Automne</button>
  <button class="filter-btn" onclick="filter('Habitat')">📍 Habitat</button>
</div>

<div class="gallery" id="gallery">
{''.join(cards)}
</div>

<div class="stats">
  Keywords générés automatiquement par gemma4 (Ollama local) · Tags <span style="color:#9E9E9E">Auto</span> = confiance du modèle · Cliquer sur l'image pour ouvrir en plein écran
</div>

<script>
function filter(cat) {{
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
  document.querySelectorAll('.card').forEach(card => {{
    if (cat === 'all') {{ card.classList.remove('hidden'); return; }}
    const kws = card.querySelector('.card-kw').textContent;
    card.classList.toggle('hidden', !kws.includes(cat));
  }});
}}
</script>

</body>
</html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ Gallery written: {output_path}")
    print(f"   {len(cards)} cards, {sum(len(json.loads(Path(cache_path).read_text())[fp]['keywords']) for fp in cache)} total keywords")


def main():
    parser = argparse.ArgumentParser(description="Generate HTML keyword gallery")
    parser.add_argument("--cache", required=True, help="Path to keyword_cache.json")
    parser.add_argument("--photo-dir", required=True, help="Root photo directory")
    parser.add_argument("--output", default="PHOTO/keyword_gallery.html", help="Output HTML path")
    args = parser.parse_args()

    cache_p = Path(args.cache)
    if not cache_p.exists():
        sys.exit(f"❌ Cache not found: {args.cache}")

    generate_html(args.cache, args.photo_dir, args.output)


if __name__ == "__main__":
    main()
