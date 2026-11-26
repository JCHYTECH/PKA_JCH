#!/usr/bin/env python3
"""Generate a standalone HTML review app for InsectNet segment QC."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parent.parent
BASE_DIR = (
    ROOT
    / "JCH_Inbox/03_PROJECTS/03_WILDNEXUS/06_COMPONENTS/BIOACOUSTIC/"
    / "INSECTNET"
)
DEFAULT_QC = BASE_DIR / "03_AUDIO_DOWNLOADS/segment_qc.csv"
DEFAULT_OUTPUT = BASE_DIR / "04_PIPELINE/insectnet-qc-review.html"
DEFAULT_PREVIEW_RATE = "1"

CSV_FIELDS = [
    "species_latin",
    "recording_id",
    "segment_index",
    "start_s",
    "duration_s",
    "segment_path",
    "spectrogram_path",
    "visual_qc",
    "qc_reason",
    "reviewed_by",
    "notes",
]

OPTIONAL_DISPLAY_FIELDS = [
    "auto_qc",
    "auto_reason",
    "auto_score",
    "active_pixel_ratio",
    "contrast_stddev",
    "mean_luminance",
    "audio_band_tag",
    "audio_band_reason",
    "dominant_freq_hz",
    "low_band_ratio",
    "mid_band_ratio",
    "high_band_ratio",
    "species_audio_status",
    "species_audio_median_hz",
    "species_audio_threshold_hz",
]


def file_uri(path: str) -> str:
    return "file://" + quote(str(Path(path)), safe="/:")


def load_qc(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def prepare_records(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for index, row in enumerate(rows):
        record = {field: row.get(field, "") for field in CSV_FIELDS}
        for field in OPTIONAL_DISPLAY_FIELDS:
            record[field] = row.get(field, "")
        record["id"] = str(index)
        record["audio_uri"] = file_uri(record["segment_path"]) if record["segment_path"] else ""
        record["spectrogram_uri"] = (
            file_uri(record["spectrogram_path"]) if record["spectrogram_path"] else ""
        )
        records.append(record)
    return records


def prepare_view_rows(rows: list[dict[str, str]], species: str | None = None) -> list[dict[str, str]]:
    filtered = [
        row
        for row in rows
        if not species or row.get("species_latin", "") == species
    ]
    band_order = {"audible": 0, "mixed": 1, "ultrasonic": 2, "unknown": 3, "": 3}
    auto_order = {
        "auto_keep_candidate": 0,
        "human_review": 1,
        "auto_reject_candidate": 2,
        "": 3,
    }

    def sort_key(row: dict[str, str]) -> tuple[int, int, float, int, str]:
        band = band_order.get(row.get("audio_band_tag", ""), 3)
        auto = auto_order.get(row.get("auto_qc", ""), 3)
        dominant = float(row.get("dominant_freq_hz", "0") or 0.0)
        recording = row.get("recording_id", "")
        segment = int(float(row.get("segment_index", "0") or 0))
        return (band, auto, dominant, segment, recording)

    return sorted(filtered, key=sort_key)


def species_options(rows: list[dict[str, str]]) -> list[str]:
    return sorted({row.get("species_latin", "") for row in rows if row.get("species_latin")})


def render_html(
    rows: list[dict[str, str]],
    title: str = "InsectNet QC Review",
    default_preview_rate: str = DEFAULT_PREVIEW_RATE,
) -> str:
    records = prepare_records(rows)
    species = species_options(records)
    records_json = json.dumps(records, ensure_ascii=False)
    species_json = json.dumps(species, ensure_ascii=False)
    preview_selected_1 = "selected" if default_preview_rate == "1" else ""
    preview_selected_05 = "selected" if default_preview_rate == "0.5" else ""
    preview_selected_025 = "selected" if default_preview_rate == "0.25" else ""
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <style>
    :root {{
      --bg: #f5f4ef;
      --panel: #ffffff;
      --ink: #17201b;
      --muted: #617067;
      --line: #d8ddd5;
      --keep: #1f7a4d;
      --reject: #a33b2f;
      --review: #7a641f;
      --accent: #315c7d;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      background: var(--bg);
      color: var(--ink);
      font: 14px/1.4 -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}
    header {{
      position: sticky;
      top: 0;
      z-index: 5;
      display: grid;
      grid-template-columns: minmax(220px, 1fr) auto;
      gap: 16px;
      align-items: center;
      padding: 14px 18px;
      border-bottom: 1px solid var(--line);
      background: rgba(245, 244, 239, 0.96);
      backdrop-filter: blur(8px);
    }}
    h1 {{
      margin: 0;
      font-size: 18px;
      font-weight: 700;
      letter-spacing: 0;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: flex-end;
      align-items: center;
    }}
    select, input, button, textarea {{
      font: inherit;
      border: 1px solid var(--line);
      background: #fff;
      color: var(--ink);
      border-radius: 6px;
    }}
    select, input {{
      min-height: 34px;
      padding: 0 10px;
    }}
    button {{
      min-height: 34px;
      padding: 0 12px;
      cursor: pointer;
      font-weight: 650;
    }}
    button.active[data-action="keep"] {{ background: var(--keep); color: #fff; border-color: var(--keep); }}
    button.active[data-action="reject"] {{ background: var(--reject); color: #fff; border-color: var(--reject); }}
    button.active[data-action="review"] {{ background: var(--review); color: #fff; border-color: var(--review); }}
    #exportCsv {{ background: var(--accent); color: #fff; border-color: var(--accent); }}
    main {{ padding: 18px; }}
    .stats {{
      display: flex;
      flex-wrap: wrap;
      gap: 10px;
      margin-bottom: 14px;
      color: var(--muted);
    }}
    .stat {{
      border: 1px solid var(--line);
      background: var(--panel);
      border-radius: 6px;
      padding: 6px 9px;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
      gap: 12px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      overflow: hidden;
      min-width: 0;
    }}
    .card img {{
      display: block;
      width: 100%;
      aspect-ratio: 2 / 1;
      object-fit: cover;
      background: #071015;
    }}
    .body {{ padding: 10px; }}
    .meta {{
      display: flex;
      justify-content: space-between;
      gap: 8px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .auto {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .auto span {{
      padding: 3px 6px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #f8faf7;
    }}
    .band {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .band span {{
      padding: 3px 6px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #fbfbfb;
    }}
    .species-audio {{
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      margin-bottom: 8px;
      color: var(--muted);
      font-size: 12px;
    }}
    .species-audio span {{
      padding: 3px 6px;
      border: 1px solid var(--line);
      border-radius: 5px;
      background: #fcfcfc;
    }}
    audio {{ width: 100%; height: 34px; margin-bottom: 8px; }}
    .actions {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 6px;
      margin-bottom: 8px;
    }}
    .fields {{
      display: grid;
      grid-template-columns: 1fr;
      gap: 6px;
    }}
    textarea {{
      width: 100%;
      min-height: 52px;
      resize: vertical;
      padding: 8px;
    }}
    .empty {{
      padding: 36px;
      text-align: center;
      color: var(--muted);
      border: 1px dashed var(--line);
      background: var(--panel);
      border-radius: 8px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>{title}</h1>
    <div class="toolbar">
      <select id="speciesFilter" aria-label="Species filter"></select>
      <select id="qcFilter" aria-label="QC filter">
        <option value="all">All QC</option>
        <option value="review">Review</option>
        <option value="keep">Keep</option>
        <option value="reject">Reject</option>
      </select>
      <select id="autoFilter" aria-label="Auto suggestion filter">
        <option value="all">All auto</option>
        <option value="auto_reject_candidate">Auto rejects</option>
        <option value="auto_keep_candidate">Auto keep candidates</option>
        <option value="human_review">Auto human review</option>
        <option value="none">No auto suggestion</option>
      </select>
      <select id="audioBandFilter" aria-label="Audio band filter">
        <option value="all">All bands</option>
        <option value="ultrasonic">Ultrasonic</option>
        <option value="audible">Audible</option>
        <option value="mixed">Mixed</option>
        <option value="unknown">Unknown</option>
      </select>
      <select id="previewMode" aria-label="Preview mode">
        <option value="1" {preview_selected_1}>Preview mode: original</option>
        <option value="0.5" {preview_selected_05}>Preview mode: 0.5x</option>
        <option value="0.25" {preview_selected_025}>Preview mode: 0.25x</option>
      </select>
      <input id="searchBox" type="search" placeholder="Recording ID">
      <button id="exportCsv">Export CSV</button>
    </div>
  </header>
  <main>
    <div class="stats" id="stats"></div>
    <section class="grid" id="cards"></section>
  </main>
  <script>
    const QC_RECORDS = {records_json};
    const SPECIES = {species_json};
    const REASONS = ["unreviewed", "good_pattern", "low_signal", "noise", "silence", "saturation", "ambiguous"];
    const CSV_FIELDS = {json.dumps(CSV_FIELDS)};

    const state = QC_RECORDS.map(record => ({{ ...record }}));
    const speciesFilter = document.getElementById("speciesFilter");
    const qcFilter = document.getElementById("qcFilter");
    const autoFilter = document.getElementById("autoFilter");
    const audioBandFilter = document.getElementById("audioBandFilter");
    const previewMode = document.getElementById("previewMode");
    const searchBox = document.getElementById("searchBox");
    const cards = document.getElementById("cards");
    const stats = document.getElementById("stats");

    function initFilters() {{
      speciesFilter.innerHTML = '<option value="all">All species</option>' +
        SPECIES.map(species => `<option value="${{escapeAttr(species)}}">${{escapeHtml(species)}}</option>`).join("");
      speciesFilter.addEventListener("change", render);
      qcFilter.addEventListener("change", render);
      autoFilter.addEventListener("change", render);
      audioBandFilter.addEventListener("change", render);
      previewMode.addEventListener("change", render);
      searchBox.addEventListener("input", render);
      document.getElementById("exportCsv").addEventListener("click", downloadCsv);
    }}

    function filteredRecords() {{
      const species = speciesFilter.value;
      const qc = qcFilter.value;
      const auto = autoFilter.value;
      const band = audioBandFilter.value;
      const query = searchBox.value.trim().toLowerCase();
      return state.filter(record =>
        (species === "all" || record.species_latin === species) &&
        (qc === "all" || record.visual_qc === qc) &&
        (auto === "all" || (auto === "none" ? !record.auto_qc : record.auto_qc === auto)) &&
        (band === "all" || (band === "unknown" ? !record.audio_band_tag : record.audio_band_tag === band)) &&
        (!query || record.recording_id.toLowerCase().includes(query))
      );
    }}

    function renderStats() {{
      const counts = state.reduce((acc, record) => {{
        acc[record.visual_qc] = (acc[record.visual_qc] || 0) + 1;
        return acc;
      }}, {{}});
      stats.innerHTML = [
        ["Total", state.length],
        ["Keep", counts.keep || 0],
        ["Review", counts.review || 0],
        ["Reject", counts.reject || 0],
        ["Shown", filteredRecords().length]
      ].map(([label, value]) => `<div class="stat">${{label}}: <strong>${{value}}</strong></div>`).join("");
    }}

    function render() {{
      const rows = filteredRecords();
      renderStats();
      if (!rows.length) {{
        cards.innerHTML = '<div class="empty">No matching segments.</div>';
        return;
      }}
      cards.innerHTML = rows.map(record => cardHtml(record)).join("");
      cards.querySelectorAll("button[data-action]").forEach(button => {{
        button.addEventListener("click", () => updateQc(button.dataset.id, button.dataset.action));
      }});
      cards.querySelectorAll("select[data-reason]").forEach(select => {{
        select.addEventListener("change", () => updateField(select.dataset.id, "qc_reason", select.value));
      }});
      cards.querySelectorAll("textarea[data-notes]").forEach(textarea => {{
        textarea.addEventListener("input", () => updateField(textarea.dataset.id, "notes", textarea.value));
      }});
      applyPreviewMode();
    }}

    function cardHtml(record) {{
      const reasonOptions = REASONS.map(reason =>
        `<option value="${{reason}}" ${{record.qc_reason === reason ? "selected" : ""}}>${{reason}}</option>`
      ).join("");
      return `<article class="card">
        <img src="${{escapeAttr(record.spectrogram_uri)}}" alt="Spectrogram ${{escapeAttr(record.recording_id)}} segment ${{escapeAttr(record.segment_index)}}">
        <div class="body">
          <div class="meta">
            <span>${{escapeHtml(record.species_latin)}}</span>
            <span>XC${{escapeHtml(record.recording_id)}} · seg ${{escapeHtml(record.segment_index)}} · ${{escapeHtml(record.start_s)}}s</span>
          </div>
          <div class="auto">${{autoHtml(record)}}</div>
          <div class="band">${{bandHtml(record)}}</div>
          <div class="species-audio">${{speciesAudioHtml(record)}}</div>
          <audio controls preload="none" src="${{escapeAttr(record.audio_uri)}}"></audio>
          <div class="actions">
            ${{actionButton(record, "keep", "Keep")}}
            ${{actionButton(record, "reject", "Reject")}}
            ${{actionButton(record, "review", "Review")}}
          </div>
          <div class="fields">
            <select data-reason="${{record.id}}">${{reasonOptions}}</select>
            <textarea data-notes="${{record.id}}" placeholder="Notes">${{escapeHtml(record.notes || "")}}</textarea>
          </div>
        </div>
      </article>`;
    }}

    function autoHtml(record) {{
      if (!record.auto_qc) return '<span>Auto suggestion: none</span>';
      return `<span>Auto suggestion: <strong>${{escapeHtml(record.auto_qc)}}</strong></span>
        <span>${{escapeHtml(record.auto_reason || "")}}</span>
        <span>score ${{escapeHtml(record.auto_score || "")}}</span>`;
    }}

    function bandHtml(record) {{
      if (!record.audio_band_tag) return '<span>Audio band: unknown</span>';
      return `<span>Audio band: <strong>${{escapeHtml(record.audio_band_tag)}}</strong></span>
        <span>${{escapeHtml(record.audio_band_reason || "")}}</span>
        <span>dominant ${{escapeHtml(record.dominant_freq_hz || "")}} Hz</span>`;
    }}

    function speciesAudioHtml(record) {{
      if (!record.species_audio_status) return '<span>Species audio: unknown</span>';
      return `<span>Species audio: <strong>${{escapeHtml(record.species_audio_status)}}</strong></span>
        <span>median ${{escapeHtml(record.species_audio_median_hz || "")}} Hz</span>
        <span>threshold ${{escapeHtml(record.species_audio_threshold_hz || "")}} Hz</span>`;
    }}

    function actionButton(record, action, label) {{
      const active = record.visual_qc === action ? " active" : "";
      return `<button class="${{active}}" data-id="${{record.id}}" data-action="${{action}}">${{label}}</button>`;
    }}

    function updateQc(id, value) {{
      const record = state.find(item => item.id === id);
      if (!record) return;
      record.visual_qc = value;
      record.reviewed_by = "JCH";
      if (value === "keep" && record.qc_reason === "unreviewed") record.qc_reason = "good_pattern";
      if (value === "reject" && record.qc_reason === "unreviewed") record.qc_reason = "ambiguous";
      render();
    }}

    function updateField(id, field, value) {{
      const record = state.find(item => item.id === id);
      if (!record) return;
      record[field] = value;
      record.reviewed_by = "JCH";
      renderStats();
    }}

    function applyPreviewMode() {{
      const rate = Number(previewMode.value || "1");
      cards.querySelectorAll("audio").forEach(audio => {{
        audio.playbackRate = rate;
        audio.preservesPitch = false;
        audio.mozPreservesPitch = false;
        audio.webkitPreservesPitch = false;
      }});
    }}

    function downloadCsv() {{
      const csv = [CSV_FIELDS.join(",")].concat(state.map(row =>
        CSV_FIELDS.map(field => csvEscape(row[field] || "")).join(",")
      )).join("\\n") + "\\n";
      const blob = new Blob([csv], {{ type: "text/csv;charset=utf-8" }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = url;
      link.download = "segment_qc_reviewed.csv";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    }}

    function csvEscape(value) {{
      const text = String(value);
      return /[",\\n]/.test(text) ? `"${{text.replaceAll('"', '""')}}"` : text;
    }}

    function escapeHtml(value) {{
      return String(value).replace(/[&<>"']/g, char => ({{
        "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
      }}[char]));
    }}

    function escapeAttr(value) {{
      return escapeHtml(value);
    }}

    initFilters();
    render();
  </script>
</body>
</html>
"""


def write_html(
    rows: list[dict[str, str]],
    output: Path,
    title: str,
    default_preview_rate: str = DEFAULT_PREVIEW_RATE,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        render_html(rows, title=title, default_preview_rate=default_preview_rate),
        encoding="utf-8",
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--qc", type=Path, default=DEFAULT_QC)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--title", default="InsectNet QC Review")
    parser.add_argument("--species", default="", help="Limit the generated view to one species")
    parser.add_argument(
        "--preview-rate",
        default=DEFAULT_PREVIEW_RATE,
        choices=["1", "0.5", "0.25"],
        help="Default preview playback rate",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    rows = load_qc(args.qc)
    rows = prepare_view_rows(rows, species=args.species or None)
    write_html(rows, args.output, args.title, default_preview_rate=args.preview_rate)
    suffix = f" for {args.species}" if args.species else ""
    print(f"Wrote QC review app with {len(rows)} records{suffix}: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
