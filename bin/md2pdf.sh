#!/usr/bin/env bash
# md2pdf.sh — Convertit un/plusieurs fichiers Markdown en .docx + .pdf
#
# Usage :
#   md2pdf.sh fichier.md [fichier2.md ...]
#
# Sorties (à côté de chaque source) :
#   fichier.docx  — pandoc, mise en page Word propre
#   fichier.pdf   — HTML + CSS + Chrome headless, emoji couleur préservés
#
# Dépendances : pandoc + Google Chrome (déjà installés sur M5).
# Chemins avec espaces acceptés (toujours quoter les arguments).

set -u

CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

usage() {
  cat <<'EOF'
Usage : md2pdf.sh fichier.md [fichier2.md ...]

Convertit chaque fichier Markdown en :
  - fichier.docx  (pandoc)
  - fichier.pdf   (HTML + CSS + Chrome headless, emoji préservés)

Dépendances : pandoc, Google Chrome.
EOF
}

command -v pandoc >/dev/null 2>&1 || { echo "ERREUR : pandoc introuvable." >&2; exit 1; }
[ -x "$CHROME" ] || { echo "ERREUR : Google Chrome introuvable ($CHROME)." >&2; exit 1; }
[ $# -ge 1 ] || { usage; exit 1; }

# ── CSS embarqué (mise en page) ─────────────────────────────────────────────
CSS="$(mktemp /tmp/md2pdf-css.XXXXXX)"
cat > "$CSS" <<'EOF'
@page { size: A4; margin: 2cm 2.2cm; }
body { font-family: -apple-system, "Helvetica Neue", "Segoe UI", Arial, sans-serif; font-size: 10.5pt; line-height: 1.55; color: #1c1c1e; }
h1 { font-size: 21pt; color: #0b5394; border-bottom: 2px solid #0b5394; padding-bottom: 6px; }
h2 { font-size: 15pt; color: #0b5394; margin-top: 1.4em; border-bottom: 1px solid #ddd; padding-bottom: 4px; }
h3 { font-size: 12pt; color: #333; margin-top: 1.1em; }
h4 { font-size: 10.5pt; color: #444; }
code { font-family: "SF Mono", Menlo, Consolas, monospace; font-size: 9pt; background: #f2f2f7; padding: 1px 4px; border-radius: 3px; }
pre { background: #f2f2f7; padding: 10px 12px; border-radius: 5px; border: 1px solid #e0e0e0; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
table { border-collapse: collapse; width: 100%; margin: 1em 0; font-size: 9.5pt; }
th, td { border: 1px solid #ccc; padding: 5px 8px; text-align: left; }
th { background: #f0f0f0; }
hr { border: none; border-top: 1px solid #ddd; margin: 1.5em 0; }
blockquote { border-left: 3px solid #0b5394; margin-left: 0; padding-left: 12px; color: #555; }
EOF

WORK="$(mktemp -d /tmp/md2pdf.XXXXXX)"
trap 'rm -rf "$CSS" "$WORK"' EXIT

convert_one() {
  local md="$1"
  local base="${md%.*}"
  local html="$WORK/$(basename "$base").html"
  local style="$WORK/style.html"
  local profile="$WORK/profile"
  mkdir -p "$profile"

  echo "→ $md"

  # DOCX
  if pandoc "$md" -o "$base.docx"; then
    echo "   ✓ $base.docx"
  else
    echo "   ✗ échec DOCX : $md" >&2
    return 1
  fi

  # HTML (CSS embarqué)
  { printf '<style>\n'; cat "$CSS"; printf '\n</style>\n'; } > "$style"
  if ! pandoc "$md" -s -H "$style" -o "$html"; then
    echo "   ✗ échec HTML : $md" >&2
    return 1
  fi

  # PDF via Chrome headless (attente du fichier + kill propre, Chrome ne se ferme pas toujours)
  "$CHROME" --headless --disable-gpu --no-first-run --no-default-browser-check \
    --no-pdf-header-footer --user-data-dir="$profile" \
    --print-to-pdf="$base.pdf" "file://$html" >/dev/null 2>&1 &
  local cpid=$!
  local ok=0
  for _ in $(seq 1 90); do
    if [ -s "$base.pdf" ]; then ok=1; break; fi
    sleep 1
  done
  sleep 1   # laisser Chrome finaliser l'écriture
  kill "$cpid" 2>/dev/null || true
  wait "$cpid" 2>/dev/null || true

  if [ "$ok" -eq 1 ]; then
    echo "   ✓ $base.pdf"
  else
    echo "   ✗ échec PDF : $base.pdf (Chrome n'a pas produit le fichier en 90 s)" >&2
  fi
}

for md in "$@"; do
  if [ -f "$md" ]; then
    convert_one "$md"
  else
    echo "⚠ introuvable : $md" >&2
  fi
done
