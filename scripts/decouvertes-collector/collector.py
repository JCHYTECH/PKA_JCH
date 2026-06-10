"""
PKA DECOUVERTES Collector
Rôle unique : recevoir les messages du groupe Telegram DECOUVERTES
et les sauvegarder bruts dans pka-decouvertes/raw/.
Aucune analyse — aucune IA — passerelle fiable uniquement.

Model: unknown (créé ~2026-06-02, modèle non documenté)
Fixed: 2026-06-09 — TokenMaskFilter + RotatingFileHandler + JCH_PRIVATE isolation
"""

import json
import logging
import os
import re
from datetime import datetime, timezone
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update, Message
from telegram.ext import (
    Application,
    MessageHandler,
    filters,
    ContextTypes,
)

# ── Config ────────────────────────────────────────────────────────────────────

# PKA_ROOT doit être connu avant de charger les secrets
PKA_ROOT = Path(os.getenv("PKA_ROOT", str(Path(__file__).resolve().parents[2])))

# Charger depuis JCH_PRIVATE/ (protégé par .gitignore) avec fallback local
_env_path = PKA_ROOT / "JCH_PRIVATE" / "decouvertes.env"
if not _env_path.exists():
    _env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)

TOKEN    = os.getenv("DECOUVERTES_TOKEN")
GROUP_ID = int(os.getenv("DECOUVERTES_GROUP_ID"))

RAW_DIR   = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/raw"
QUEUE_DIR = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/queue"
LOG_DIR   = PKA_ROOT / "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/logs"

for d in (RAW_DIR / "text", RAW_DIR / "images", RAW_DIR / "links",
          RAW_DIR / "metadata", QUEUE_DIR, LOG_DIR):
    d.mkdir(parents=True, exist_ok=True)

# ── Logging ───────────────────────────────────────────────────────────────────

class TokenMaskFilter(logging.Filter):
    """Masque le token Telegram dans les logs (msg + args lazy %s)."""
    def filter(self, record):
        if TOKEN and len(TOKEN) > 20:
            record.msg = str(record.msg).replace(TOKEN, "***TOKEN***")
            if record.args:
                new_args = []
                for a in record.args:
                    if isinstance(a, str) and TOKEN in a:
                        new_args.append(a.replace(TOKEN, "***TOKEN***"))
                    elif not isinstance(a, (int, float, bool, type(None))) and TOKEN in str(a):
                        new_args.append(str(a).replace(TOKEN, "***TOKEN***"))
                    else:
                        new_args.append(a)
                record.args = tuple(new_args)
        return True

from logging.handlers import RotatingFileHandler

log_file = LOG_DIR / "collector.log"
file_handler = RotatingFileHandler(
    str(log_file), maxBytes=1_000_000, backupCount=3, encoding="utf-8"
)
file_handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(message)s"))

logging.basicConfig(
    level=logging.INFO,
    handlers=[file_handler],
    force=True,
)

# Appliquer le filtre sur le logger racine + loggers télégram/httpx
# pour masquer le token dans TOUS les logs, erreurs includes
token_filter = TokenMaskFilter()
logging.root.addFilter(token_filter)
for name in ("httpx", "telegram", "telegram.request", "telegram.ext"):
    logging.getLogger(name).addFilter(token_filter)

log = logging.getLogger(__name__)

# ── Helpers ───────────────────────────────────────────────────────────────────

URL_PATTERN = re.compile(r"https?://[^\s]+")

def extract_links(text: str | None) -> list[str]:
    return URL_PATTERN.findall(text) if text else []

def msg_slug(msg: Message) -> str:
    ts = datetime.fromtimestamp(msg.date.timestamp(), tz=timezone.utc)
    return f"{ts.strftime('%Y%m%d_%H%M%S')}_{msg.message_id}"

def build_metadata(msg: Message, content_type: str, media_files: list) -> dict:
    ts = datetime.fromtimestamp(msg.date.timestamp(), tz=timezone.utc)
    author = msg.from_user.username or msg.from_user.full_name or str(msg.from_user.id)
    text = msg.text or msg.caption or ""
    return {
        "telegram_message_id": str(msg.message_id),
        "telegram_group": "DECOUVERTES",
        "author": author,
        "datetime": ts.isoformat(),
        "content_type": content_type,
        "text": text,
        "links": extract_links(text),
        "media_files": media_files,
        "analysis_status": "pending",
        "place_candidates": [],
        "confidence": None,
    }

def save_metadata(slug: str, metadata: dict):
    meta_path  = RAW_DIR / "metadata" / f"{slug}.json"
    queue_path = QUEUE_DIR / f"{slug}.json"
    payload = json.dumps(metadata, ensure_ascii=False, indent=2)
    meta_path.write_text(payload)
    queue_path.write_text(payload)
    log.info(f"→ queue/{slug}.json")

def from_group(update: Update) -> bool:
    return update.effective_chat.id == GROUP_ID

# ── Handlers ─────────────────────────────────────────────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not from_group(update):
        return
    text  = msg.text or ""
    slug  = msg_slug(msg)
    links = extract_links(text)

    (RAW_DIR / "text" / f"{slug}.txt").write_text(text, encoding="utf-8")
    if links:
        (RAW_DIR / "links" / f"{slug}.json").write_text(
            json.dumps(links, ensure_ascii=False, indent=2))

    content_type = "link" if links and len(text.strip()) < 200 else "text"
    save_metadata(slug, build_metadata(msg, content_type, []))
    log.info(f"TEXT  [{slug}] {text[:60]!r}")


async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not from_group(update):
        return
    slug     = msg_slug(msg)
    tg_file  = await msg.photo[-1].get_file()
    img_path = RAW_DIR / "images" / f"{slug}.jpg"
    await tg_file.download_to_drive(str(img_path))

    caption = msg.caption or ""
    links   = extract_links(caption)
    if links:
        (RAW_DIR / "links" / f"{slug}.json").write_text(
            json.dumps(links, ensure_ascii=False, indent=2))

    media   = [{"file_path": str(img_path.relative_to(PKA_ROOT)), "media_type": "photo"}]
    ctype   = "image_with_caption" if caption else "image"
    save_metadata(slug, build_metadata(msg, ctype, media))
    log.info(f"PHOTO [{slug}] → {img_path.name}")


async def handle_document(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    if not from_group(update):
        return
    slug    = msg_slug(msg)
    doc     = msg.document
    ext     = Path(doc.file_name or "file").suffix or ".bin"
    tg_file = await doc.get_file()
    path    = RAW_DIR / "images" / f"{slug}{ext}"
    await tg_file.download_to_drive(str(path))

    mtype = "screenshot" if ext.lower() in (".jpg", ".jpeg", ".png", ".webp") else "document"
    media = [{"file_path": str(path.relative_to(PKA_ROOT)), "media_type": mtype}]
    save_metadata(slug, build_metadata(msg, mtype, media))
    log.info(f"DOC   [{slug}] → {path.name}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    if not TOKEN:
        raise RuntimeError("DECOUVERTES_TOKEN manquant dans .env")
    log.info("PKA DECOUVERTES Collector — démarrage")
    log.info(f"Groupe : {GROUP_ID} | Dépôt : {RAW_DIR}")

    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_document))

    log.info("En attente de messages DECOUVERTES…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
