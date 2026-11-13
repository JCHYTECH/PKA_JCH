#!/usr/bin/env python3
"""
generate_deck.py — Deck éducatif WildLens « AI Will Never Speak the Language of the Living ».

Génère :
  - un PPTX print-safe (fond Ivoire, texte Noir Terrain, accents Vert Terrain)
  - un markdown slide par slide (source pour Gamma / Google Slides)

Règle d'impression (JC) : jamais de fond noir ; gris 50% max. → fond Ivoire #F8F5F0,
texte noir, aucune slide sombre.

Usage : python3 generate_deck.py
"""

from __future__ import annotations

from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

# ── Charte WildLens (pka-brand-identity) ──────────────────────────────
IVOIRE = RGBColor(0xF8, 0xF5, 0xF0)      # fond
NOIR = RGBColor(0x0D, 0x0B, 0x09)        # texte
VERT = RGBColor(0x3D, 0x5A, 0x3E)        # accent WildLens
OCRE = RGBColor(0xC1, 0x7F, 0x3A)        # accent Arteon (secondaire)
GRIS = RGBColor(0x6B, 0x65, 0x60)        # texte secondaire (gris < 50%)

FONT_TITLE = "Arial"
FONT_BODY = "Georgia"
FONT_MONO = "Courier New"

OUT_DIR = Path(__file__).resolve().parent
PPTX_PATH = OUT_DIR / "AI-Will-Never-Speak-the-Language-of-the-Living.pptx"
MD_PATH = OUT_DIR / "ai-language-living-deck.md"

# ── Contenu du deck (source unique) ───────────────────────────────────
# kind: title | content | quote
SLIDES = [
    {
        "kind": "title",
        "title": "AI Will Never Speak the Language of the Living",
        "subtitle": "From the Voynich Manuscript to birdsong — why the machine sees patterns, not meaning",
        "notes": "Opening. The thesis in one line: the machine sees patterns; meaning requires a shared world.",
    },
    {
        "kind": "content",
        "title": "Every two years, the same headline",
        "bullets": [
            "“AI has deciphered the Voynich Manuscript.”",
            "Every claim is rejected by scholars.",
            "2018: “Hebrew encoded as anagrams” — collapsed.",
            "2026: still undeciphered.",
        ],
        "notes": "The Voynich is not the story — it is the symptom of a deeper limit.",
    },
    {
        "kind": "content",
        "title": "A real book, no known language",
        "bullets": [
            "600 years old, 200 pages.",
            "Plants that do not exist.",
            "A script that belongs to no known language.",
            "AI maps the structure perfectly — no translation.",
        ],
        "notes": "The word distribution is not random; it follows rules close to a natural language. Yet no meaning.",
        "visual": "Voynich manuscript page",
    },
    {
        "kind": "content",
        "title": "The rule: known language + large corpus",
        "bullets": [
            "Linear A, Rongorongo, Indus, Proto-Elamite, Phaistos — all “analyzed”, none decoded.",
            "AI decodes only when the language is known and the corpus is large.",
            "Herculaneum (June 2026): an entire scroll read for the first time.",
            "But those were Greek texts — a language we already read.",
        ],
        "notes": "Herculaneum is the real AI success. But it did not translate — it made legible what the ink had erased.",
        "visual": "Herculaneum scroll (X-ray unwrap)",
    },
    {
        "kind": "content",
        "title": "Structure is cheap. Meaning is not.",
        "bullets": [
            "Sperm whale “phonetic alphabet” (2024): structure, no meaning.",
            "Project CETI: massive data, no translation.",
            "It is the Voynich in acoustic form.",
        ],
        "notes": "A larger corpus does not help. What is missing is a key — a verifiable link between signal and referent.",
        "visual": "Sperm whale song spectrogram",
    },
    {
        "kind": "content",
        "title": "AI confuses meaning (Tel Aviv, 2026)",
        "bullets": [
            "Tested on toddler vocalizations — a language we partly understand.",
            "AI grouped sounds of different meaning together.",
            "AI separated sounds of identical meaning.",
            "Patterns, not significance.",
        ],
        "notes": "Even with a language we understand, the network sees patterns, not meaning.",
    },
    {
        "kind": "content",
        "title": "The brain is not enough",
        "bullets": [
            "Zebra finch: song reconstructed from neural activity alone.",
            "One lab decodes their dreams — different songs asleep.",
            "But this is motor production, not meaning.",
            "You can read the score without hearing the music.",
        ],
        "notes": "Knowing how a sound is made says nothing about what it means.",
        "visual": "Zebra finch + HVC brain schematic",
    },
    {
        "kind": "content",
        "title": "The flower we never see",
        "bullets": [
            "Bees see ultraviolet guides that we do not see.",
            "Humans hear 20 Hz – 20 kHz.",
            "Bat: 120 kHz. Dolphin: 150 kHz. Elephant: 5 Hz.",
            "We missed rodent ultrasound and elephant infrasound for decades.",
        ],
        "notes": "The umwelt — the perceptual world proper to each species (Jakob von Uexküll).",
        "visual": "UV flower (bee vision)",
    },
    {
        "kind": "content",
        "title": "Sound is only one axis",
        "bullets": [
            "Chemistry — pheromones.",
            "Electricity — electric fish “speak” in fields.",
            "Magnetism — bird navigation.",
            "Substrate vibration — spiders.",
            "Each is a wavelength we might forget — RGB without UV.",
        ],
        "notes": "Our own senses are a trap: we search for animal “language” with human ears, eyes, categories.",
    },
    {
        "kind": "content",
        "title": "Can AI deduce an unknown umwelt?",
        "bullets": [
            "No sensor → no data → no inference.",
            "AI cannot guess a signal no instrument has measured.",
            "Bird magnetoreception was found by experiment, not analysis.",
        ],
        "notes": "AI works on data. It cannot invent a channel from nothing.",
    },
    {
        "kind": "content",
        "title": "But AI can signal a missing channel",
        "bullets": [
            "Exoplanets: found by anomaly, not by sight.",
            "Dark matter: an unexplained residue.",
            "AI detects unexplained correlation → predicts an umwelt.",
            "The loop: measure → detect residue → hypothesize → build a sensor.",
        ],
        "notes": "That is a prediction, not a discovery. Characterizing the medium remains physics and sensors.",
        "visual": "Discovery loop diagram",
    },
    {
        "kind": "content",
        "title": "The dream is old",
        "bullets": [
            "Quran 27:16 — Solomon “taught the language of the birds”.",
            "Attar, The Conference of the Birds (1177).",
            "Gongye Chang (China) understood the birds.",
            "Hindu siddhi — “knowledge of the sounds of all beings”.",
            "Shamanism — the animal as teacher.",
        ],
        "notes": "The desire to speak with the living is universal — older than the algorithms.",
    },
    {
        "kind": "content",
        "title": "The real version: not translation, mutualism",
        "bullets": [
            "Greater honeyguide + Yao honey-hunters (Mozambique).",
            "The “brrr-hm” call, passed from father to son.",
            "The bird triples the odds of being guided.",
            "Spottiswoode proved the bird recognizes the exact call.",
            "Co-evolutionary shared signaling — neither “decodes” the other.",
        ],
        "notes": "This is the living answer to Solomon: meaning is shared, not decoded.",
        "visual": "Honeyguide + Yao honey-hunter",
    },
    {
        "kind": "content",
        "title": "Dialect disappears before the predator",
        "bullets": [
            "Song is learned → dialects.",
            "Alarm calls are innate → conserved.",
            "Facing a predator, selection freezes the signal.",
            "The “seet” call is identical across unrelated species.",
        ],
        "notes": "Marler's localization hypothesis (1955): a high, narrow sound is impossible for a predator to localize.",
        "visual": "“Seet” call spectrogram, convergent",
    },
    {
        "kind": "quote",
        "title": "The law, in one sentence",
        "quote": "Dialect is a luxury of signals that are not life-or-death.",
        "subtitle": "The moment a signal becomes a matter of survival, selection freezes it — and fuses it across species.",
        "notes": "Reconfirmed by the Cornell Lab, October 2025.",
    },
    {
        "kind": "content",
        "title": "Three things, which are one",
        "bullets": [
            "AI is a pattern machine, not a meaning machine.",
            "Our own umwelt is a trap.",
            "Meaning is not decoded — it is shared.",
        ],
        "notes": "The through-line of the whole essay.",
    },
    {
        "kind": "quote",
        "title": "Look long enough, precisely enough",
        "quote": "The machine maps what is measurable. The meaning belongs to the one who stays still, listens — and is willing to be looked back at.",
        "subtitle": "WildLens — understanding the living is not calculation, but belonging.",
        "notes": "Closing. Sources: Marler 1955; Seyfarth, Cheney & Marler 1980; Templeton 2005; Spottiswoode 2016; Cornell Lab 2025; Vesuvius Challenge 2026; Tel Aviv 2026.",
    },
]


# ── Build PPTX ────────────────────────────────────────────────────────
def _set_bg(slide, color):
    bg = slide.background
    bg.fill.solid()
    bg.fill.fore_color.rgb = color


def _add_text(slide, text, left, top, width, height, font, size, color, bold=False, italic=False):
    box = slide.shapes.add_textbox(left, top, width, height)
    tf = box.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    run = p.runs[0]
    run.font.name = font
    run.font.size = Pt(size)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.italic = italic
    return box


def _accent_bar(slide, left, top, width, height, color):
    from pptx.enum.shapes import MSO_SHAPE
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shp.fill.solid()
    shp.fill.fore_color.rgb = color
    shp.line.fill.background()
    shp.shadow.inherit = False
    return shp


def build_pptx():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank = prs.slide_layouts[6]

    for s in SLIDES:
        slide = prs.slides.add_slide(blank)
        _set_bg(slide, IVOIRE)

        kind = s["kind"]

        if kind == "title":
            _accent_bar(slide, Inches(0.9), Inches(2.15), Inches(0.18), Inches(1.5), VERT)
            _add_text(slide, s["title"], Inches(1.35), Inches(2.05), Inches(10.6), Inches(1.6),
                      FONT_TITLE, 40, NOIR, bold=True)
            if s.get("subtitle"):
                _add_text(slide, s["subtitle"], Inches(1.35), Inches(3.75), Inches(10.6), Inches(1.2),
                          FONT_BODY, 22, GRIS, italic=True)
        elif kind == "quote":
            _accent_bar(slide, Inches(0.9), Inches(1.6), Inches(0.18), Inches(1.2), OCRE)
            _add_text(slide, s["title"], Inches(1.35), Inches(1.45), Inches(10.6), Inches(0.7),
                      FONT_TITLE, 20, GRIS, bold=True)
            _add_text(slide, "“" + s["quote"] + "”", Inches(1.35), Inches(2.5), Inches(10.6), Inches(2.2),
                      FONT_BODY, 30, NOIR, italic=True)
            if s.get("subtitle"):
                _add_text(slide, s["subtitle"], Inches(1.35), Inches(5.1), Inches(10.6), Inches(1.0),
                          FONT_BODY, 18, GRIS)
        else:  # content
            _accent_bar(slide, Inches(0.9), Inches(0.55), Inches(0.14), Inches(1.0), VERT)
            _add_text(slide, s["title"], Inches(1.35), Inches(0.5), Inches(11.0), Inches(0.9),
                      FONT_TITLE, 30, NOIR, bold=True)
            body = slide.shapes.add_textbox(Inches(1.35), Inches(1.6), Inches(11.0), Inches(5.4))
            tf = body.text_frame
            tf.word_wrap = True
            first = True
            for b in s.get("bullets", []):
                p = tf.paragraphs[0] if first else tf.add_paragraph()
                first = False
                p.text = "•  " + b
                p.space_after = Pt(10)
                run = p.runs[0]
                run.font.name = FONT_BODY
                run.font.size = Pt(20)
                run.font.color.rgb = NOIR

        # notes + footer
        notes = slide.notes_slide
        notes.notes_text_frame.text = s.get("notes", "")
        _add_text(slide, "WildLens · print-safe · Ivoire #F8F5F0",
                  Inches(0.9), Inches(7.05), Inches(5.0), Inches(0.3),
                  FONT_MONO, 9, GRIS)

    prs.save(str(PPTX_PATH))
    return PPTX_PATH


# ── Build Markdown ────────────────────────────────────────────────────
def build_markdown():
    lines = [
        "# AI Will Never Speak the Language of the Living",
        "### Deck éducatif WildLens — slide par slide (EN · print-safe : fond Ivoire, jamais de fond noir)",
        "",
        "> Règle d'impression : fond Ivoire `#F8F5F0`, texte Noir Terrain `#0D0B09`, accent Vert Terrain `#3D5A3E`, gris 50 % max.",
        "",
    ]
    for i, s in enumerate(SLIDES, 1):
        kind = s["kind"]
        lines.append(f"---\n\n## Slide {i} — {s['title']}")
        if kind == "title":
            if s.get("subtitle"):
                lines.append(f"\n*{s['subtitle']}*")
        elif kind == "quote":
            lines.append(f"\n> “{s['quote']}”")
            if s.get("subtitle"):
                lines.append(f"\n{s['subtitle']}")
        else:
            for b in s.get("bullets", []):
                lines.append(f"- {b}")
        if s.get("visual"):
            lines.append(f"\n**Visuel :** {s['visual']}")
        lines.append(f"\n**Note orateur :** {s.get('notes', '')}")
        lines.append("")
    lines.append("---\n\n*Sources : Marler 1955 · Seyfarth/Cheney/Marler 1980 · Templeton 2005 · Spottiswoode 2016 · Cornell Lab 2025 · Vesuvius Challenge 2026 · Tel Aviv 2026.*")
    MD_PATH.write_text("\n".join(lines), encoding="utf-8")
    return MD_PATH


if __name__ == "__main__":
    p = build_pptx()
    m = build_markdown()
    print(f"✅ PPTX  → {p}")
    print(f"✅ Markdown → {m}")
    print(f"   {len(SLIDES)} slides")
