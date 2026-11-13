#!/usr/bin/env python3
"""
generate_full_gallery.py — Rich HTML gallery from 'full' template cache.
AnyVision-style layout: thumbnail, headline, labels with confidence,
species, description, composition, lighting, colors, print, ARTEON.
"""

import argparse, json, sys
from pathlib import Path
from datetime import datetime

def color_swatch(hex_color: str) -> str:
    return f'<span class="swatch" style="background:{hex_color}" title="{hex_color}"></span>'

def confidence_badge(label: str, conf: float) -> str:
    if conf >= 0.8: cls = "conf-high"
    elif conf >= 0.5: cls = "conf-mid"
    else: cls = "conf-low"
    return f'<span class="label-badge {cls}">{label} <small>{int(conf*100)}%</small></span>'

def generate(cache_path: str, photo_dir: str, output_path: str):
    cache = json.loads(Path(cache_path).read_text())
    photo_base = Path(photo_dir).expanduser().resolve()

    cards = []
    for fp, entry in cache.items():
        if entry.get("template") != "full":
            continue
        r = entry.get("result", {})
        fname = entry.get("file", "unknown")
        img_path = photo_base / fname
        if not img_path.exists():
            cand = list(photo_base.rglob(fname))
            img_path = cand[0] if cand else photo_base / fname
        rel = str(img_path.resolve()) if img_path.exists() else ""

        # Labels with confidence
        labels_html = ""
        for lb in r.get("labels", []):
            labels_html += confidence_badge(lb.get("label",""), lb.get("confidence",0))

        # Species
        sp = r.get("species") or {}
        species_html = ""
        if sp.get("primary"):
            conf = sp.get("confidence", 0)
            species_html = f'<span class="species-name">{sp["primary"]}</span>'
            if conf: species_html += f' <span class="species-conf">({int(conf*100)}%)</span>'
            if sp.get("alternatives"):
                species_html += f' <span class="species-alt">Alt: {", ".join(sp["alternatives"])}</span>'

        # Colors with swatches
        colors_html = ""
        for c in r.get("colors", []):
            hexc = c.get("hex", "#888")
            name = c.get("name", "")
            colors_html += f'<span class="color-chip">{color_swatch(hexc)} {name}</span>'

        # Keywords
        kw_html = ""
        for kw in r.get("keywords", []):
            kw_html += f'<span class="kw-chip">{kw}</span>'

        # Composition
        comp = r.get("composition", {})
        comp_html = f'{comp.get("cadrage","")} · {comp.get("règle","")} · {comp.get("fond","")}'

        # Lighting
        light = r.get("lighting", {})
        light_html = f'{light.get("qualité","")} · {light.get("direction","")} · {light.get("condition","")}'

        # Print
        pr = r.get("print") or {}
        print_html = ""
        if pr.get("paper"):
            print_html = f'🖨️ {pr["paper"]} — {pr.get("reason","")}'

        # ARTEON
        ar = r.get("arteon") or {}
        arteon_html = ""
        if ar.get("verdict"):
            v = ar["verdict"]
            color = {"accept":"#4CAF50","maybe":"#FF9800","reject":"#f44336"}.get(v,"#888")
            arteon_html = f'<span class="arteon-badge" style="border-color:{color};color:{color}">ARTEON: {v.upper()} ({ar.get("score","?")}/10)</span>'
            if ar.get("reason"):
                arteon_html += f' <span class="arteon-reason">{ar["reason"]}</span>'

        card = f"""
    <div class="card">
      <div class="card-left">
        <a href="file://{rel}" target="_blank">
          <img src="file://{rel}" loading="lazy" onerror="this.style.display='none'">
        </a>
      </div>
      <div class="card-right">
        <div class="card-header">
          <span class="headline">{r.get("headline", fname)}</span>
        </div>
        {f'<div class="card-species">{species_html}</div>' if species_html else ''}
        <div class="card-labels">{labels_html}</div>
        {f'<div class="card-desc">{r.get("description","")}</div>' if r.get("description") else ''}
        {f'<div class="card-kw">{kw_html}</div>' if kw_html else ''}
        <div class="card-meta">
          <div class="meta-row"><span class="meta-label">Composition</span> {comp_html}</div>
          <div class="meta-row"><span class="meta-label">Lumière</span> {light_html}</div>
          {f'<div class="meta-row"><span class="meta-label">Couleurs</span> {colors_html}</div>' if colors_html else ''}
          {f'<div class="meta-row"><span class="meta-label">Habitat</span> {r.get("habitat","")}</div>' if r.get("habitat") else ''}
          {f'<div class="meta-row"><span class="meta-label">Technique</span> {", ".join(r.get("technique",[]))}</div>' if r.get("technique") else ''}
          {f'<div class="meta-row"><span class="meta-label">Ambiance</span> {r.get("mood","")}</div>' if r.get("mood") else ''}
          {f'<div class="meta-row">{print_html}</div>' if print_html else ''}
          {f'<div class="meta-row">{arteon_html}</div>' if arteon_html else ''}
        </div>
      </div>
    </div>"""
        cards.append(card)

    html = f"""<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>PKA Vision — Full Analysis ({len(cards)} images)</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}}
h1{{text-align:center;color:#f0f6fc;margin-bottom:4px;font-size:1.4em}}
.subtitle{{text-align:center;color:#8b949e;margin-bottom:20px;font-size:.85em}}
.gallery{{display:flex;flex-direction:column;gap:14px;max-width:1100px;margin:0 auto}}
.card{{display:flex;gap:16px;background:#161b22;border-radius:12px;overflow:hidden;border:1px solid #30363d}}
.card:hover{{border-color:#58a6ff}}
.card-left{{flex:0 0 240px;display:flex;align-items:center;justify-content:center;background:#0d1117;min-height:160px;overflow:hidden}}
.card-left img{{max-width:240px;max-height:200px;object-fit:contain}}
.card-right{{flex:1;padding:14px 18px;display:flex;flex-direction:column;gap:8px}}
.card-header{{display:flex;justify-content:space-between;align-items:center}}
.headline{{font-weight:700;font-size:1.1em;color:#f0f6fc}}
.card-species{{font-size:.95em;color:#7ee787}}
.species-name{{font-weight:600}}
.species-conf{{color:#8b949e;font-size:.8em;margin-left:4px}}
.species-alt{{color:#8b949e;font-size:.8em;margin-left:8px;font-style:italic}}
.card-labels{{display:flex;flex-wrap:wrap;gap:5px}}
.label-badge{{padding:2px 8px;border-radius:10px;font-size:.75em;font-weight:600;color:#fff}}
.label-badge small{{opacity:.75;margin-left:2px}}
.conf-high{{background:#238636}}.conf-mid{{background:#9e6a03}}.conf-low{{background:#da3633}}
.card-desc{{font-size:.85em;color:#8b949e;line-height:1.5;font-style:italic;border-left:2px solid #30363d;padding-left:10px}}
.card-kw{{display:flex;flex-wrap:wrap;gap:4px}}
.kw-chip{{padding:1px 7px;border-radius:3px;font-size:.72em;background:#1c2128;color:#8b949e;border:1px solid #30363d}}
.card-meta{{display:flex;flex-direction:column;gap:4px;font-size:.82em}}
.meta-row{{color:#8b949e}}
.meta-label{{color:#58a6ff;font-weight:600;margin-right:6px}}
.color-chip{{display:inline-flex;align-items:center;gap:3px;margin-right:6px}}
.swatch{{display:inline-block;width:12px;height:12px;border-radius:3px;border:1px solid #30363d}}
.arteon-badge{{font-weight:700;font-size:.8em;border:1px solid;padding:1px 6px;border-radius:4px;margin-right:6px}}
.arteon-reason{{color:#8b949e;font-size:.9em}}
@media(max-width:640px){{.card{{flex-direction:column}}.card-left{{flex:0 0 auto;max-height:220px}}.card-left img{{max-width:100%;max-height:220px}}}}
</style></head><body>
<h1>🦉 PKA Vision — Full Analysis</h1>
<div class="subtitle">{len(cards)} images · {datetime.now().strftime('%Y-%m-%d %H:%M')}</div>
<div class="gallery">{''.join(cards)}</div>
</body></html>"""

    Path(output_path).write_text(html, encoding="utf-8")
    print(f"✅ Gallery: {output_path} ({len(cards)} cards)")

def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cache", required=True)
    p.add_argument("--photo-dir", required=True)
    p.add_argument("--output", default="PHOTO/keyword_gallery_full.html")
    a = p.parse_args()
    generate(a.cache, a.photo_dir, a.output)

if __name__ == "__main__":
    main()
