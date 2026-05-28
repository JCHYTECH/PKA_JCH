"""
Dobby — Bot Telegram PKA
Texte · Voix (Whisper) · Photos (Claude Vision) · Réponses vocales (OpenAI TTS)
"""

import asyncio
import io
import logging
import os
import re
import sqlite3
import tempfile
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import anthropic
from openai import OpenAI

from dobby_context import SYSTEM_PROMPT

# ── Configuration ────────────────────────────────────────────────────────────

load_dotenv()

TELEGRAM_TOKEN      = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID    = int(os.getenv("TELEGRAM_USER_ID"))
ANTHROPIC_API_KEY   = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY      = os.getenv("OPENAI_API_KEY")
PKA_ROOT            = os.getenv("PKA_ROOT", "/Users/jchavauxm5/PKA_JCH")

OPENAI_TTS_VOICE    = os.getenv("OPENAI_TTS_VOICE", "nova")
OPENAI_TTS_MODEL    = os.getenv("OPENAI_TTS_MODEL", "tts-1")
TTS_ALSO_SEND_TEXT  = os.getenv("TTS_ALSO_SEND_TEXT", "true").lower() == "true"

DB_PATH = Path(__file__).parent / "conversation.db"
MAX_HISTORY = 20

# ── État TTS (toggle /vocal) ─────────────────────────────────────────────────

tts_enabled = os.getenv("TTS_ENABLED", "true").lower() == "true"

# ── Logging ──────────────────────────────────────────────────────────────────

TOKEN_REDACTIONS = [
    (re.compile(r"(https://api\.telegram\.org/bot)[^/\s\"]+"), r"\1<redacted>"),
    (re.compile(r"(https://api\.telegram\.org/file/bot)[^/\s\"]+"), r"\1<redacted>"),
    (re.compile(r"\bbot\d+:[A-Za-z0-9_-]+"), "bot<redacted>"),
    (re.compile(r"\bbot\d+%3A[A-Za-z0-9_-]+"), "bot<redacted>"),
]


def redact_secrets(value: object) -> str:
    text = str(value)
    for pattern, replacement in TOKEN_REDACTIONS:
        text = pattern.sub(replacement, text)
    return text


class RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = redact_secrets(record.msg)
        if isinstance(record.args, tuple):
            record.args = tuple(redact_secrets(arg) for arg in record.args)
        elif isinstance(record.args, dict):
            record.args = {key: redact_secrets(value) for key, value in record.args.items()}
        return True


log_file = Path(__file__).parent / "dobby.log"
file_handler = logging.FileHandler(log_file)
file_handler.addFilter(RedactingFilter())

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
    handlers=[file_handler],
    force=True,
)
log = logging.getLogger(__name__)

for noisy_logger in ("httpx", "httpcore", "telegram"):
    logging.getLogger(noisy_logger).addFilter(RedactingFilter())
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

# ── Clients API ──────────────────────────────────────────────────────────────

claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

# ── Base de données — historique de conversation ──────────────────────────────

def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            role      TEXT    NOT NULL,
            content   TEXT    NOT NULL,
            created   TEXT    DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()

def load_history() -> list[dict]:
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT role, content FROM history ORDER BY id DESC LIMIT ?",
        (MAX_HISTORY,)
    ).fetchall()
    conn.close()
    return [{"role": r, "content": c} for r, c in reversed(rows)]

def save_message(role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("INSERT INTO history (role, content) VALUES (?, ?)", (role, content))
    conn.commit()
    conn.close()

def clear_history():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM history")
    conn.commit()
    conn.close()

# ── Sécurité — seul JCH peut interagir ──────────────────────────────────────

def is_authorized(update: Update) -> bool:
    uid = update.effective_user.id
    if uid != TELEGRAM_USER_ID:
        log.warning(f"Accès refusé — user_id inconnu : {uid}")
        return False
    return True

# ── Appel Claude ─────────────────────────────────────────────────────────────

def ask_claude(messages: list[dict]) -> str:
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    )
    return response.content[0].text

def ask_claude_vision(image_bytes: bytes, caption: str | None) -> str:
    import base64
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")
    prompt = caption or "Analyse cette image."
    response = claude.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": [
                {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_b64}},
                {"type": "text",  "text": prompt},
            ],
        }],
    )
    return response.content[0].text

# ── Transcription vocale (Whisper) ────────────────────────────────────────────

async def transcribe_voice(file_path: Path) -> str:
    if openai_client is None:
        return "[Transcription non disponible — OPENAI_API_KEY manquant dans .env]"
    with open(file_path, "rb") as f:
        result = openai_client.audio.transcriptions.create(
            model="whisper-1",
            file=f,
            language="fr",
        )
    return result.text

# ── TTS — génération audio depuis texte ──────────────────────────────────────

def strip_markdown(text: str) -> str:
    text = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", text)
    text = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()

async def generate_tts(text: str) -> bytes | None:
    if openai_client is None:
        log.warning("TTS ignoré — OPENAI_API_KEY manquant")
        return None
    try:
        clean_text = strip_markdown(text)
        response = openai_client.audio.speech.create(
            model=OPENAI_TTS_MODEL,
            voice=OPENAI_TTS_VOICE,
            input=clean_text,
            response_format="opus",
        )
        return response.content
    except Exception as e:
        log.error(f"Erreur TTS : {e}")
        return None

async def send_reply(update: Update, reply: str):
    """Envoie la réponse : vocal si TTS actif, texte toujours si TTS_ALSO_SEND_TEXT."""
    if tts_enabled:
        audio = await generate_tts(reply)
        if audio:
            await update.message.reply_voice(voice=io.BytesIO(audio))
            if TTS_ALSO_SEND_TEXT:
                await update.message.reply_text(reply, parse_mode="Markdown")
            return
    await update.message.reply_text(reply, parse_mode="Markdown")

# ── Handlers ─────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text(
        "🐶 *Dobby en ligne.* Parle — je t'écoute.",
        parse_mode="Markdown",
    )

async def cmd_clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    clear_history()
    await update.message.reply_text("🐶 Historique effacé. Nouvelle conversation.")

async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    import sqlite3 as sq
    db = sq.connect(f"{PKA_ROOT}/TEAM/team.db")
    membres = db.execute("SELECT COUNT(*) FROM members WHERE status='active'").fetchone()[0]
    db.close()
    hist = load_history()
    vocal_status = "✅ activé" if tts_enabled else "❌ désactivé"
    await update.message.reply_text(
        f"🐶 *PKA Status*\n"
        f"• Membres actifs : {membres}\n"
        f"• Messages en contexte : {len(hist)}\n"
        f"• DB : TEAM/team.db ✓\n"
        f"• Vocal : {vocal_status} (voix : {OPENAI_TTS_VOICE})",
        parse_mode="Markdown",
    )

async def cmd_vocal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    global tts_enabled
    args = context.args
    if args and args[0].lower() == "on":
        tts_enabled = True
    elif args and args[0].lower() == "off":
        tts_enabled = False
    else:
        tts_enabled = not tts_enabled
    state = "activé ✅" if tts_enabled else "désactivé ❌"
    await update.message.reply_text(f"🐶 Réponses vocales {state}.")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text(
        "🐶 *Commandes disponibles*\n\n"
        "/start — démarrer\n"
        "/status — état du système PKA\n"
        "/clear — effacer l'historique de conversation\n"
        "/vocal — activer/désactiver les réponses vocales\n"
        "/vocal on|off — forcer l'état\n"
        "/help — cette aide\n\n"
        "Tu peux aussi m'envoyer :\n"
        "• Un message texte → je réponds\n"
        "• Un message vocal → je transcris et je réponds\n"
        "• Une photo → je l'analyse (Argus dans la boucle)",
        parse_mode="Markdown",
    )

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    user_text = update.message.text
    log.info(f"TEXT reçu : {user_text[:80]}")

    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    save_message("user", user_text)
    history = load_history()

    try:
        reply = ask_claude(history)
    except Exception as e:
        log.error(f"Erreur Claude : {e}")
        reply = f"⚠️ Erreur Claude : {e}"

    save_message("assistant", reply)
    await send_reply(update, reply)

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    log.info("VOICE reçu — téléchargement en cours")
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    voice_file = await update.message.voice.get_file()

    with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp:
        await voice_file.download_to_drive(tmp.name)
        tmp_path = Path(tmp.name)

    try:
        transcription = await transcribe_voice(tmp_path)
        log.info(f"Transcription : {transcription[:100]}")
    finally:
        tmp_path.unlink(missing_ok=True)

    user_message = f"[Message vocal transcrit] : {transcription}"
    save_message("user", user_message)
    history = load_history()

    try:
        reply = ask_claude(history)
    except Exception as e:
        log.error(f"Erreur Claude : {e}")
        reply = f"⚠️ Erreur Claude : {e}"

    save_message("assistant", reply)

    if tts_enabled:
        audio = await generate_tts(reply)
        if audio:
            await update.message.reply_voice(voice=io.BytesIO(audio))
            if TTS_ALSO_SEND_TEXT:
                await update.message.reply_text(
                    f"🎙 _{transcription}_\n\n{reply}",
                    parse_mode="Markdown",
                )
            return

    await update.message.reply_text(
        f"🎙 _{transcription}_\n\n{reply}",
        parse_mode="Markdown",
    )

async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    log.info("PHOTO reçue — téléchargement en cours")
    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    photo = update.message.photo[-1]  # meilleure résolution
    photo_file = await photo.get_file()

    with tempfile.NamedTemporaryFile(suffix=".jpg", delete=False) as tmp:
        await photo_file.download_to_drive(tmp.name)
        image_bytes = Path(tmp.name).read_bytes()
        Path(tmp.name).unlink(missing_ok=True)

    caption = update.message.caption or None

    try:
        reply = ask_claude_vision(image_bytes, caption)
    except Exception as e:
        log.error(f"Erreur vision : {e}")
        reply = f"⚠️ Erreur analyse image : {e}"

    await update.message.reply_text(reply, parse_mode="Markdown")

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    init_db()
    log.info("🐶 Dobby démarre — PKA Telegram Bot")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("clear",  cmd_clear))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("vocal",  cmd_vocal))
    app.add_handler(CommandHandler("help",   cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    log.info("✅ Bot actif — en attente de messages")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
