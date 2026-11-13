#!/usr/bin/env python3
"""
pka_prompt_guard.py — Prompt Injection Scanner for PKA_JCH Inbox Pipeline.

Architecture:
  1. Pre-processing : HTML strip + Unicode normalization + invisible char extraction
  2. Detection     : Pattern matching, heuristic scoring, signature detection
  3. Scoring       : Weighted risk score 0–100
  4. Action        : Accept (<20) / Warn (20–50) / Quarantine (>50)

Usage:
  python scripts/pka_prompt_guard.py scan <file>
  python scripts/pka_prompt_guard.py scan --stdin
  python scripts/pka_prompt_guard.py scan --text "some text"
  python scripts/pka_prompt_guard.py scan-dir <directory>

Threat model (OWASP LLM01:2025 + field research):
  - Direct injection ("ignore all instructions", role hijacking)
  - Indirect injection (hidden in email body, PDF, web page)
  - Invisible Unicode (zero-width, tag chars, bidi overrides, homoglyphs)
  - Steganographic encoding (binary payloads in invisible chars)
  - Payload splitting / multi-turn grooming
  - System prompt extraction
  - Tool call simulation
  - Template injection (Jinja2, Django, Python format strings)
  - Encoded payloads (base64, hex, ROT13)
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
QUARANTINE_DIR = ROOT / "JCH_Inbox" / "00_INBOX" / ".quarantine"

# ──────────────────────────────────────────────────────────────────────
# LAYER 1 — Pre-processing: HTML stripping & Unicode normalization
# ──────────────────────────────────────────────────────────────────────

# Zero-width and invisible Unicode characters
ZERO_WIDTH_CHARS = {
    "\u200B",  # Zero Width Space
    "\u200C",  # Zero Width Non-Joiner
    "\u200D",  # Zero Width Joiner
    "\uFEFF",  # BOM / Zero Width No-Break Space
    "\u2060",  # Word Joiner
    "\u2061",  # Function Application
    "\u2062",  # Invisible Times
    "\u2063",  # Invisible Separator
    "\u2064",  # Invisible Plus
    "\u180E",  # Mongolian Vowel Separator
    "\u00AD",  # Soft Hyphen
    "\u034F",  # Combining Grapheme Joiner
    "\u061C",  # Arabic Letter Mark
    "\u115F",  # Hangul Choseong Filler
    "\u1160",  # Hangul Jungseong Filler
    "\u17B4",  # Khmer Vowel Inherent Aq
    "\u17B5",  # Khmer Vowel Inherent Aa
}

# Unicode Tag characters (U+E0000 to U+E007F) — used for ASCII smuggling
TAG_RANGE_START = 0xE0000
TAG_RANGE_END = 0xE007F

# Bidi override characters
BIDI_OVERRIDE_CHARS = {
    "\u202A",  # Left-to-Right Embedding
    "\u202B",  # Right-to-Left Embedding
    "\u202C",  # Pop Directional Formatting
    "\u202D",  # Left-to-Right Override
    "\u202E",  # Right-to-Left Override
    "\u2066",  # Left-to-Right Isolate
    "\u2067",  # Right-to-Left Isolate
    "\u2068",  # First Strong Isolate
    "\u2069",  # Pop Directional Isolate
}

# Homoglyph character pairs (visual lookalikes)
HOMOGLYPH_MAP = {
    # Latin → Cyrillic
    "a": "а", "A": "А", "e": "е", "E": "Е", "o": "о", "O": "О",
    "p": "р", "P": "Р", "c": "с", "C": "С", "T": "Т", "H": "Н",
    "x": "х", "X": "Х", "B": "В", "M": "М", "K": "К", "y": "у",
    # Latin → Greek
    "o": "ο", "O": "Ο", "n": "η",
    # Digits → lookalikes
    "0": "Ο", "1": "Ӏ",
}
# Reverse: Cyrillic/Greek → Latin suspicion
HOMOGLYPH_SUSPICIOUS = set()
for _latin, _fake in HOMOGLYPH_MAP.items():
    HOMOGLYPH_SUSPICIOUS.add(_fake)


def has_invisible_chars(text: str) -> list[str]:
    """Return list of invisible character types found."""
    found = set()
    for ch in text:
        if ch in ZERO_WIDTH_CHARS:
            found.add(f"zero-width: U+{ord(ch):04X}")
        elif TAG_RANGE_START <= ord(ch) <= TAG_RANGE_END:
            found.add(f"unicode-tag: U+{ord(ch):04X}")
        elif ch in BIDI_OVERRIDE_CHARS:
            found.add(f"bidi-override: U+{ord(ch):04X}")
    return sorted(found)


def has_homoglyphs(text: str) -> list[str]:
    """Return list of homoglyph characters found."""
    found = set()
    for ch in text:
        if ch in HOMOGLYPH_SUSPICIOUS:
            found.add(f"homoglyph: {ch!r} U+{ord(ch):04X}")
    return sorted(found)


def strip_invisible(text: str) -> str:
    """Remove all zero-width, tag, and bidi-override chars. Returns cleaned text."""
    cleaned = []
    for ch in text:
        cp = ord(ch)
        if ch in ZERO_WIDTH_CHARS:
            continue
        if TAG_RANGE_START <= cp <= TAG_RANGE_END:
            continue
        if ch in BIDI_OVERRIDE_CHARS:
            continue
        cleaned.append(ch)
    return "".join(cleaned)


def decode_unicode_tags(text: str) -> str:
    """Decode Unicode tag characters (U+E0000–U+E007F) as ASCII."""
    result = []
    for ch in text:
        cp = ord(ch)
        if TAG_RANGE_START <= cp <= TAG_RANGE_END:
            ascii_val = cp - TAG_RANGE_START
            if 0 <= ascii_val < 128:
                result.append(chr(ascii_val))
        else:
            result.append(ch)
    return "".join(result)


def decode_zero_width_binary(text: str) -> list[str]:
    """
    Decode binary messages encoded in zero-width chars.
    Scheme: U+200B=start, U+200C=0, U+2063=1, U+200D=end.
    Returns list of decoded strings found.
    """
    start_marker = "\u200B"
    end_marker = "\u200D"
    bit0 = "\u200C"
    bit1 = "\u2063"

    decoded = []
    i = 0
    while i < len(text):
        if text[i] == start_marker:
            bits = []
            i += 1
            while i < len(text) and text[i] != end_marker:
                if text[i] == bit0:
                    bits.append("0")
                elif text[i] == bit1:
                    bits.append("1")
                i += 1
            if i < len(text) and text[i] == end_marker:
                i += 1
            # Convert bits to ASCII
            if len(bits) >= 8:
                chars = []
                for j in range(0, len(bits) - len(bits) % 8, 8):
                    byte = bits[j:j+8]
                    val = int("".join(byte), 2)
                    if 32 <= val < 127:
                        chars.append(chr(val))
                if chars:
                    decoded.append("".join(chars))
        else:
            i += 1
    return decoded


def strip_html(text: str) -> str:
    """
    Extract ALL visible text from HTML, including hidden elements.
    Strips: <style>, <script>, HTML tags, CSS display:none/visibility:hidden,
    font-size:0, opacity:0, color=background-color, absolute positioning off-screen.
    """
    import html as _html

    # Remove scripts and styles entirely (their content is not rendered text)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style[^>]*>.*?</style>", "", text, flags=re.DOTALL | re.IGNORECASE)

    # Remove HTML comments (may contain hidden payloads — but we extract them)
    # We'll extract comment text separately below

    # Extract text from alt, title, and other attributes that might be hidden
    # (keep them — they're text the model could see)

    # Simple tag stripping — removes all HTML tags but keeps text content
    text = re.sub(r"<[^>]+>", " ", text)

    # Decode HTML entities
    text = _html.unescape(text)

    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def extract_html_comments(text: str) -> list[str]:
    """Extract text content from HTML comments (potential hidden payloads)."""
    return re.findall(r"<!--(.+?)-->", text, flags=re.DOTALL)


def normalize_text(text: str) -> str:
    """Full normalization: Unicode NFKC + homoglyph detection."""
    return unicodedata.normalize("NFKC", text)


def scan_visible(text: str) -> str:
    """Pre-process: strip invisible chars, decode tags, normalize."""
    text = decode_unicode_tags(text)
    text = strip_invisible(text)
    text = normalize_text(text)
    return text


# ──────────────────────────────────────────────────────────────────────
# LAYER 2 — Detection: pattern matching & heuristics
# ──────────────────────────────────────────────────────────────────────

# Direct injection patterns
DIRECT_INJECTION_PATTERNS = [
    # Role hijacking
    (r"(?i)\b(ignore|forget|disregard|override)\s+(all|previous|prior|above)\s+(instructions?|prompts?|rules?|guidelines?|context)\b", 9, "role-hijack"),
    (r"(?i)\byou\s+are\s+now\s+(DAN|STAN|jailbroken|unfiltered|an?\s+unrestricted)\b", 9, "role-hijack-DAN"),
    (r"(?i)\byou\s+are\s+no\s+longer\b.*\b(assistant|AI|LLM|model)\b", 8, "role-hijack-negation"),
    (r"(?i)\bpretend\s+(you\s+are|to\s+be|that)\b", 7, "role-hijack-pretend"),

    # Instruction override
    (r"(?i)\b(do\s+not|don't|never)\s+(follow|obey|comply\s+with)\s+(system|safety|ethical|content)\s+(prompts?|instructions?|policies?|guidelines?)\b", 9, "safety-override"),
    (r"(?i)\b(do\s+not|don't|never)\s+(refuse|reject|filter|block)\b", 7, "refusal-override"),
    (r"(?i)\byour\s+(primary|main|new)\s+(goal|objective|purpose|directive)\s+(is|should\s+be)\b", 8, "goal-hijack"),

    # System prompt extraction
    (r"(?i)\b(repeat|print|output|display|show|tell\s+me|reveal|disclose)\s+(your|the)\s+(system\s+prompt|instructions?|rules?|guidelines?|initial\s+prompt)\b", 9, "system-prompt-extract"),
    (r"(?i)\bwhat\s+(are|were)\s+(your|the)\s+(original|initial|first)\s+(instructions?|prompts?)\b", 8, "system-prompt-extract-2"),
    (r"(?i)\bwhat\s+did\s+the\s+(user|system|human)\s+tell\s+you\b", 7, "system-prompt-extract-3"),
    (r"(?i)\b(in\s+your\s+own\s+words|verbatim|word\s+for\s+word)\s*,?\s*(repeat|tell|describe|explain)\b", 6, "verbatim-request"),

    # Tool call simulation
    (r"(?i)\b(simulate|fake|forge|synthesize)\s+(a\s+|the\s+)?(tool|function|API|command)\s+(call|response|output|result)\b", 9, "tool-sim"),
    (r"(?i)\<function_call\>|\<tool_call\>|\{[\"']name[\"']\s*:", 9, "tool-sim-json"),

    # Data exfiltration
    (r"(?i)\b(send|forward|upload|POST|email|transmit|exfiltrate)\b.*\b(token|key|secret|password|credential|api.key|auth)\b", 10, "data-exfil"),
    (r"(?i)\bfetch\([\"']https?://", 8, "fetch-exfil"),
    (r"(?i)\bcurl\s+.*https?://.*\b(token|key|secret)\b", 9, "curl-exfil"),

    # Template injection
    (r"\{\{.*?\}\}", 8, "template-injection"),
    (r"\{\%.*?\%\}", 8, "template-injection-jinja"),
    (r"\$\{.*?\}", 7, "template-injection-shell"),
    (r"__import__\(|__builtins__|__subclasses__\(\)", 9, "python-rce"),

    # Encoded payloads
    (r"(?i)\beval\s*\(\s*(atob|btoa|base64|decode|fromCharCode)\b", 9, "encoded-eval"),
    (r"(?i)\batob\s*\(\s*[\"'][A-Za-z0-9+/=]{40,}[\"']\s*\)", 9, "base64-eval"),
    (r"(?i)\\x[0-9a-f]{2}\\x[0-9a-f]{2}\\x[0-9a-f]{2}", 7, "hex-escape-sequence"),

    # Memory poisoning
    (r"(?i)\b(remember|store|save|memorize)\s+(this|the\s+following)\s*(:\s*)?\s*(password|secret|key|token|instruction)", 9, "memory-poison"),
    (r"(?i)\b(from\s+now\s+on|going\s+forward|henceforth)\s*,?\s*(you\s+(must|will|should|are|always))\b", 7, "future-instruction"),

    # Agent tool abuse (careful: "format" is a common French word → not included)
    (r"(?i)\brm\s+-rf\b", 9, "destructive-cmd-rm"),
    (r"(?i)\bDROP\s+TABLE\b", 9, "destructive-cmd-sql"),
    (r"(?i)\b(shutdown|reboot)\s+(now|the\s+system)\b", 8, "destructive-cmd"),
    (r"(?i)\bdelete\s+(all|everything|the\s+(entire|whole))\b", 8, "destructive-cmd-delete"),
    (r"(?i)\bformat\s+[Cc]:", 8, "destructive-cmd-format"),
    (r"(?i)\b(execute|run)\s+(this|the\s+following)\s+(code|command|script|payload)\b", 8, "execute-payload"),
]

# Indirect / obfuscated patterns
OBFUSCATION_PATTERNS = [
    (r"(?i)\b(ROT13|base64|hex\s*encode)\b.*\b(decode|translate|convert)\b", 6, "obfuscation-request"),
    (r"(?i)\b(take\s+every\s+(second|third|nth)|concatenate|interleave)\b.*\b(letter|character|word)\b", 7, "payload-splitting"),
    (r"(?i)\bthis\s+(is|was)\s+(encoded|obfuscated|hidden|disguised)\b", 7, "self-referencing-obfuscation"),
]

# Additional heuristics
SUSPICIOUS_KEYWORDS = [
    "ignore all previous instructions",
    "ignore all instructions",
    "disregard above",
    "system: override",
    "new system prompt",
    "you are now in developer mode",
    "developer mode enabled",
    "jailbreak",
    "DAN mode",
    "do anything now",
    "sudo mode",
    "god mode",
    "unrestricted access",
    "bypass content filter",
    "ethical filter disabled",
    "no restrictions",
    "no censorship",
    "free mode",
]


# ──────────────────────────────────────────────────────────────────────
# LAYER 3 — Scoring engine
# ──────────────────────────────────────────────────────────────────────

@dataclass
class Finding:
    """A single detection finding."""
    category: str
    severity: int  # 1-10
    description: str
    match: str = ""
    location: str = ""

@dataclass
class ScanResult:
    """Complete scan result."""
    file_path: Optional[str] = None
    risk_score: int = 0
    verdict: str = "clean"
    findings: list[Finding] = field(default_factory=list)
    invisible_chars: list[str] = field(default_factory=list)
    homoglyphs: list[str] = field(default_factory=list)
    decoded_payloads: list[str] = field(default_factory=list)
    cleaned_text: str = ""
    original_length: int = 0
    cleaned_length: int = 0
    invisible_char_count: int = 0

    def to_dict(self) -> dict:
        return {
            "file": self.file_path,
            "risk_score": self.risk_score,
            "verdict": self.verdict,
            "findings": [
                {"category": f.category, "severity": f.severity,
                 "description": f.description, "match": f.match[:200],
                 "location": f.location}
                for f in self.findings
            ],
            "invisible_chars": self.invisible_chars,
            "homoglyphs": self.homoglyphs,
            "decoded_payloads": self.decoded_payloads,
            "invisible_char_count": self.invisible_char_count,
            "original_length": self.original_length,
            "cleaned_length": self.cleaned_length,
        }


def scan(text: str, file_path: Optional[str] = None) -> ScanResult:
    """Full pipeline: pre-process → detect → score."""
    result = ScanResult(file_path=file_path)
    result.original_length = len(text)

    # ── Phase 1: Invisible character detection (pre-cleaning) ──
    result.invisible_chars = has_invisible_chars(text)
    result.homoglyphs = has_homoglyphs(text)

    # Count invisible characters
    result.invisible_char_count = sum(
        1 for ch in text
        if ch in ZERO_WIDTH_CHARS
        or TAG_RANGE_START <= ord(ch) <= TAG_RANGE_END
        or ch in BIDI_OVERRIDE_CHARS
    )

    # ── Phase 2: Decode hidden payloads before stripping ──
    result.decoded_payloads = decode_zero_width_binary(text)

    # ── Phase 3: Extract HTML comments ──
    html_comments = extract_html_comments(text)

    # ── Phase 4: Strip HTML ──
    if re.search(r"<\s*(html|body|div|p|span|table|head)\b", text, re.IGNORECASE):
        result.findings.append(Finding(
            category="format", severity=3,
            description="HTML content detected — all text extracted for inspection",
            location="pre-processing"
        ))
    text_plain = strip_html(text)

    # ── Phase 5: Decode Unicode tags & strip invisible chars ──
    # Also check the HTML comments
    all_text_to_scan = text_plain + "\n" + "\n".join(html_comments)
    cleaned = scan_visible(all_text_to_scan)
    result.cleaned_text = cleaned
    result.cleaned_length = len(cleaned)

    # ── Phase 6: Pattern detection ──
    for pattern, severity, category in DIRECT_INJECTION_PATTERNS:
        for match in re.finditer(pattern, cleaned):
            result.findings.append(Finding(
                category=category, severity=severity,
                description=f"Pattern match: {category}",
                match=match.group(0),
                location=f"offset {match.start()}"
            ))

    for pattern, severity, category in OBFUSCATION_PATTERNS:
        for match in re.finditer(pattern, cleaned):
            result.findings.append(Finding(
                category=category, severity=severity,
                description=f"Obfuscation pattern: {category}",
                match=match.group(0),
                location=f"offset {match.start()}"
            ))

    # Keyword scanning
    cleaned_lower = cleaned.lower()
    for kw in SUSPICIOUS_KEYWORDS:
        if kw.lower() in cleaned_lower:
            result.findings.append(Finding(
                category="keyword-flag", severity=7,
                description=f"Suspicious keyword found: {kw}",
                match=kw
            ))

    # ── Phase 7: Heuristic scoring ──

    # Invisible character density
    if result.invisible_char_count > 0:
        density = result.invisible_char_count / max(result.original_length, 1)
        if result.invisible_char_count > 50:
            result.findings.append(Finding(
                category="invisible-density", severity=9,
                description=f"High invisible char count: {result.invisible_char_count} ({density:.1%})",
            ))
        elif result.invisible_char_count > 10:
            result.findings.append(Finding(
                category="invisible-density", severity=6,
                description=f"Moderate invisible char count: {result.invisible_char_count} ({density:.1%})",
            ))
        elif result.invisible_char_count > 2:
            result.findings.append(Finding(
                category="invisible-density", severity=3,
                description=f"Low invisible char count: {result.invisible_char_count}",
            ))

    # Hidden payloads decoded
    if result.decoded_payloads:
        for payload in result.decoded_payloads:
            result.findings.append(Finding(
                category="steganographic-payload", severity=9,
                description=f"Decoded hidden payload: {payload[:100]}",
                match=payload[:100]
            ))

    # Unicode tag chars detected
    for inv in result.invisible_chars:
        if inv.startswith("unicode-tag"):
            result.findings.append(Finding(
                category="unicode-tag-injection", severity=8,
                description=f"Unicode tag characters detected: {inv}",
            ))

    # Bidi override detected
    for inv in result.invisible_chars:
        if inv.startswith("bidi-override"):
            result.findings.append(Finding(
                category="bidi-override", severity=8,
                description=f"Bidi override characters detected — text order may be manipulated: {inv}",
            ))

    # Homoglyphs detected
    for hom in result.homoglyphs:
        result.findings.append(Finding(
            category="homoglyph", severity=5,
            description=f"Homoglyph character detected (potential filter bypass): {hom}",
        ))

    # Length anomaly (lots of invisible content stripped)
    if result.original_length > 0:
        stripped_ratio = 1.0 - (result.cleaned_length / result.original_length)
        if stripped_ratio > 0.3:
            result.findings.append(Finding(
                category="length-anomaly", severity=5,
                description=f"Over 30% of content was invisible/hidden: {stripped_ratio:.0%}",
            ))

    # ── Phase 8: Calculate risk score ──
    if result.findings:
        # Weighted score: sum of (severity^1.5) / sum of max possible, scaled to 100
        total_severity = sum(f.severity ** 1.5 for f in result.findings)
        # Cap and normalize
        result.risk_score = min(100, int(total_severity * 1.2))

    # ── Phase 9: Verdict ──
    if result.risk_score > 50:
        result.verdict = "quarantine"
    elif result.risk_score >= 20:
        result.verdict = "warn"
    else:
        result.verdict = "clean"

    return result


# ──────────────────────────────────────────────────────────────────────
# LAYER 4 — Action: accept / warn / quarantine
# ──────────────────────────────────────────────────────────────────────

def quarantine_file(file_path: Path, result: ScanResult) -> Path:
    """Move file to quarantine and save scan report alongside it."""
    QUARANTINE_DIR.mkdir(parents=True, exist_ok=True)

    dest = QUARANTINE_DIR / file_path.name
    # Avoid overwriting
    if dest.exists():
        stem = file_path.stem
        suffix = file_path.suffix
        counter = 1
        while dest.exists():
            dest = QUARANTINE_DIR / f"{stem}_{counter}{suffix}"
            counter += 1

    file_path.rename(dest)

    # Save scan report
    report_path = QUARANTINE_DIR / f"{dest.name}.guard-report.json"
    report_path.write_text(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))

    return dest


# ──────────────────────────────────────────────────────────────────────
# CLI
# ──────────────────────────────────────────────────────────────────────

def cmd_scan(args):
    """Scan a file or stdin."""
    if args.stdin:
        text = sys.stdin.read()
        file_path = "<stdin>"
    elif args.text:
        text = args.text
        file_path = "<inline>"
    else:
        file_path = args.file
        p = Path(file_path)
        if not p.exists():
            print(f"ERROR: File not found: {file_path}", file=sys.stderr)
            sys.exit(1)
        text = p.read_text(encoding="utf-8", errors="replace")

    result = scan(text, file_path=file_path)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        _print_report(result)

    # Action: quarantine if needed
    if result.verdict == "quarantine" and not args.stdin and not args.text and not args.dry_run:
        dest = quarantine_file(Path(file_path), result)
        print(f"\n🚫 QUARANTINED → {dest}")
        print(f"📋 Report → {dest}.guard-report.json")

    sys.exit(0 if result.verdict == "clean" else 1)


def cmd_scan_dir(args):
    """Scan all files in a directory."""
    p = Path(args.directory)
    if not p.is_dir():
        print(f"ERROR: Not a directory: {args.directory}", file=sys.stderr)
        sys.exit(1)

    results = []
    files = sorted(p.rglob("*"))
    # Skip quarantine dir
    files = [f for f in files if f.is_file() and ".quarantine" not in str(f)]

    # Skip binary and non-text files
    TEXT_EXTENSIONS = {".txt", ".md", ".json", ".csv", ".html", ".htm", ".xml",
                       ".yaml", ".yml", ".toml", ".py", ".js", ".ts", ".sh",
                       ".env", ".cfg", ".ini", ".log", ".css", ".sql", ".rst"}
    BINARY_EXTENSIONS = {".pdf", ".m4a", ".mp3", ".wav", ".mp4", ".png", ".jpg",
                         ".jpeg", ".gif", ".webp", ".zip", ".gz", ".tar", ".db",
                         ".sqlite", ".sqlite3", ".exe", ".dll", ".so", ".dylib",
                         ".bin", ".dat", ".pickle", ".pkl", ".woff", ".woff2",
                         ".ttf", ".otf", ".ico", ".icns"}

    for f in files:
        suffix = f.suffix.lower()
        if suffix in BINARY_EXTENSIONS:
            continue
        # For unknown extensions, try to detect binary content
        if suffix not in TEXT_EXTENSIONS:
            try:
                sample = f.read_bytes()[:1024]
                if b"\x00" in sample:
                    continue
            except Exception:
                continue
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        result = scan(text, file_path=str(f))
        results.append(result)

        if result.verdict != "clean":
            _print_report(result)
            if result.verdict == "quarantine" and not args.dry_run:
                dest = quarantine_file(f, result)
                print(f"  🚫 QUARANTINED → {dest}\n")

    clean = sum(1 for r in results if r.verdict == "clean")
    warn = sum(1 for r in results if r.verdict == "warn")
    quar = sum(1 for r in results if r.verdict == "quarantine")
    print(f"\n── Scan Summary ──")
    print(f"Files scanned : {len(results)}")
    print(f"Clean         : {clean}")
    print(f"Warn          : {warn}")
    print(f"Quarantined   : {quar}")


def _print_report(result: ScanResult):
    """Human-readable scan report."""
    verdict_emoji = {"clean": "✅", "warn": "⚠️", "quarantine": "🚫"}
    emoji = verdict_emoji.get(result.verdict, "❓")

    print(f"\n{'='*60}")
    print(f"{emoji} PROMPT GUARD — {result.file_path}")
    print(f"   Risk Score : {result.risk_score}/100 — {result.verdict.upper()}")
    print(f"   Size       : {result.original_length} chars → {result.cleaned_length} chars (clean)")
    print(f"   Invisible  : {result.invisible_char_count} chars")

    if result.invisible_chars:
        print(f"   ⚡ Invisible chars detected :")
        for inv in result.invisible_chars:
            print(f"      - {inv}")

    if result.homoglyphs:
        print(f"   ⚡ Homoglyphs detected :")
        for hom in result.homoglyphs:
            print(f"      - {hom}")

    if result.decoded_payloads:
        print(f"   ⚡ STEGANOGRAPHIC PAYLOADS DECODED :")
        for payload in result.decoded_payloads:
            print(f"      - {payload[:120]}")

    if result.findings:
        print(f"   Findings ({len(result.findings)}) :")
        for f in result.findings:
            print(f"      [{f.severity}/10] [{f.category}] {f.description}")
            if f.match:
                match_display = f.match[:100]
                print(f"             → {match_display}")

    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(
        description="pka_prompt_guard — Prompt Injection Scanner for PKA Inbox"
    )
    sub = parser.add_subparsers(dest="command")

    # scan
    scan_p = sub.add_parser("scan", help="Scan a file, stdin, or inline text")
    scan_p.add_argument("file", nargs="?", help="File to scan")
    scan_p.add_argument("--stdin", action="store_true", help="Read from stdin")
    scan_p.add_argument("--text", help="Inline text to scan")
    scan_p.add_argument("--json", action="store_true", help="Output JSON")
    scan_p.add_argument("--dry-run", action="store_true", help="Don't quarantine")

    # scan-dir
    dir_p = sub.add_parser("scan-dir", help="Scan all files in a directory")
    dir_p.add_argument("directory", help="Directory to scan")
    dir_p.add_argument("--dry-run", action="store_true", help="Don't quarantine")

    args = parser.parse_args()

    if args.command == "scan":
        cmd_scan(args)
    elif args.command == "scan-dir":
        cmd_scan_dir(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
