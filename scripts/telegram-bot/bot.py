"""
Dobby — Bot Telegram PKA (Gemini)
Texte · Voix · Photos · Réponses vocales

Moteur IA : Google Gemini (texte + vision + audio + TTS)
Un seul modèle pour tout remplacer Claude + Whisper + OpenAI TTS.
"""

import asyncio
import base64
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
from google import genai

from dobby_context import SYSTEM_PROMPT

# ── Configuration ────────────────────────────────────────────────────────────

load_dotenv()

TELEGRAM_TOKEN      = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_USER_ID    = int(os.getenv("TELEGRAM_USER_ID"))
GEMINI_API_KEY      = os.getenv("GEMINI_API_KEY")
PKA_ROOT            = os.getenv("PKA_ROOT", "/Users/jchavauxm5/PKA_JCH")

GEMINI_TEXT_MODEL   = os.getenv("GEMINI_TEXT_MODEL", "gemini-2.5-flash")
GEMINI_TTS_MODEL    = os.getenv("GEMINI_TTS_MODEL", "gemini-2.5-flash-preview-tts")

DB_PATH = Path(__file__).parent / "conversation.db"
MAX_HISTORY = 20

# ── État TTS (toggle /vocal) ─────────────────────────────────────────────────

tts_enabled = os.getenv("TTS_ENABLED", "true").lower() == "true"
TTS_ALSO_SEND_TEXT = os.getenv("TTS_ALSO_SEND_TEXT", "true").lower() == "true"

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

for noisy_logger in ("httpx", "httpcore", "telegram", "google_genai"):
    logging.getLogger(noisy_logger).addFilter(RedactingFilter())
    logging.getLogger(noisy_logger).setLevel(logging.WARNING)

# ── Client Gemini ────────────────────────────────────────────────────────────

gemini_client = genai.Client(api_key=GEMINI_API_KEY) if GEMINI_API_KEY else None

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

# ── Appels Gemini ────────────────────────────────────────────────────────────

def ask_gemini(history: list[dict]) -> str:
    """Texte simple : envoie l'historique à Gemini."""
    if gemini_client is None:
        return "⚠️ Gemini non configuré — GEMINI_API_KEY manquant dans .env"

    # Convertir l'historique en format Gemini
    contents = []
    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    response = gemini_client.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=contents,
        config={
            "system_instruction": SYSTEM_PROMPT,
            "max_output_tokens": 1024,
        },
    )
    return response.text


def ask_gemini_vision(image_bytes: bytes, caption: str | None) -> str:
    """Analyse de photo : Gemini multimodal (vision intégrée, pas d'API séparée)."""
    if gemini_client is None:
        return "⚠️ Gemini non configuré"

    prompt = caption or "Analyse cette image en détail."
    image_b64 = base64.standard_b64encode(image_bytes).decode("utf-8")

    response = gemini_client.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": "image/jpeg", "data": image_b64}},
                ],
            }
        ],
        config={
            "system_instruction": SYSTEM_PROMPT,
            "max_output_tokens": 1024,
        },
    )
    return response.text


async def transcribe_voice_gemini(file_path: Path) -> str:
    """Transcription vocale : Gemini traite l'audio directement (pas de Whisper)."""
    if gemini_client is None:
        return "[Transcription non disponible — GEMINI_API_KEY manquant]"

    audio_bytes = file_path.read_bytes()

    response = gemini_client.models.generate_content(
        model=GEMINI_TEXT_MODEL,
        contents=[
            {
                "role": "user",
                "parts": [
                    {"text": "Transcris ce message vocal en français. Retourne uniquement la transcription, rien d'autre."},
                    {"inline_data": {"mime_type": "audio/ogg", "data": base64.standard_b64encode(audio_bytes).decode("utf-8")}},
                ],
            }
        ],
    )
    return response.text.strip()


def strip_markdown_for_tts(text: str) -> str:
    """Nettoie le markdown pour le TTS (Gemini TTS accepte du texte brut)."""
    text = re.sub(r"\*{1,2}(.+?)\*{1,2}", r"\1", text)
    text = re.sub(r"_{1,2}(.+?)_{1,2}", r"\1", text)
    text = re.sub(r"`(.+?)`", r"\1", text)
    text = re.sub(r"^#{1,6}\s+", "", text, flags=re.MULTILINE)
    text = re.sub(r"\[(.+?)\]\(.+?\)", r"\1", text)
    return text.strip()


def pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000, bits: int = 16, channels: int = 1) -> bytes:
    """Convertit du PCM brut en WAV (ajout du header 44 bytes)."""
    import struct
    byte_rate = sample_rate * channels * bits // 8
    block_align = channels * bits // 8
    data_size = len(pcm_data)
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF', 36 + data_size, b'WAVE', b'fmt ', 16,
        1, channels, sample_rate, byte_rate, block_align, bits,
        b'data', data_size
    )
    return header + pcm_data


async def generate_tts_gemini(text: str) -> bytes | None:
    """Synthèse vocale via Gemini TTS (modèle preview-tts).
    Retourne du WAV (PCM + header) que Telegram accepte en audio.
    """
    if gemini_client is None:
        return None

    try:
        clean_text = strip_markdown_for_tts(text)
        response = gemini_client.models.generate_content(
            model=GEMINI_TTS_MODEL,
            contents=[{"role": "user", "parts": [{"text": clean_text}]}],
            config={
                "response_modalities": ["AUDIO"],
                "speech_config": {
                    "voice_config": {
                        "prebuilt_voice_config": {"voice_name": "Zephyr"}
                    }
                },
            },
        )
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                if 'audio' in part.inline_data.mime_type:
                    pcm = part.inline_data.data
                    # Extraire le sample rate du mime type si dispo
                    return pcm_to_wav(pcm)
        log.warning("TTS Gemini : pas de données audio dans la réponse")
        return None
    except Exception as e:
        log.error(f"Erreur TTS Gemini : {e}")
        return None


async def send_reply(update: Update, reply: str):
    """Envoie la réponse : vocal si TTS actif, texte toujours si TTS_ALSO_SEND_TEXT."""
    if tts_enabled:
        audio = await generate_tts_gemini(reply)
        if audio:
            await update.message.reply_audio(
                audio=io.BytesIO(audio),
                title="Dobby",
                performer="Gemini TTS"
            )
            if TTS_ALSO_SEND_TEXT:
                await update.message.reply_text(reply)
            return
    await update.message.reply_text(reply)

# ── Handlers ─────────────────────────────────────────────────────────────────

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text(
        "🐶 *Dobby en ligne.* Parle — je t'écoute. *(Gemini)*",
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
    engine = "Gemini 2.5 Flash" if gemini_client else "⚠️ non configuré"
    await update.message.reply_text(
        f"🐶 *PKA Status*\n"
        f"• Moteur : {engine}\n"
        f"• Membres actifs : {membres}\n"
        f"• Messages en contexte : {len(hist)}\n"
        f"• DB : TEAM/team.db ✓\n"
        f"• Vocal : {vocal_status}",
        parse_mode="Markdown",
    )

async def cmd_vocal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    global tts_enabled
    tts_enabled = not tts_enabled
    state = "activé ✅" if tts_enabled else "désactivé ❌"
    await update.message.reply_text(f"🐶 Mode vocal : {state}")

async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return
    await update.message.reply_text(
        "🐶 *Dobby Telegram — Gemini Edition*\n"
        "• Un message texte → je réponds\n"
        "• Un message vocal → je transcris et je réponds\n"
        "• Une photo → je l'analyse\n"
        "• /vocal → active/désactive la réponse vocale\n"
        "• /status → état du système\n"
        "• /clear → efface l'historique",
        parse_mode="Markdown",
    )

# ── Message handlers ─────────────────────────────────────────────────────────

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_authorized(update):
        return

    user_text = update.message.text
    log.info(f"TEXT reçu : {user_text[:80]}")

    await context.bot.send_chat_action(update.effective_chat.id, ChatAction.TYPING)

    save_message("user", user_text)
    history = load_history()

    try:
        reply = ask_gemini(history)
    except Exception as e:
        log.error(f"Erreur Gemini texte : {e}")
        reply = f"⚠️ Erreur Gemini : {e}"

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
        transcription = await transcribe_voice_gemini(tmp_path)
        log.info(f"Transcription : {transcription[:100]}")
    except Exception as e:
        log.error(f"Erreur transcription Gemini : {e}")
        transcription = f"[Erreur transcription : {e}]"
    finally:
        tmp_path.unlink(missing_ok=True)

    user_message = f"[Message vocal transcrit] : {transcription}"
    save_message("user", user_message)
    history = load_history()

    try:
        reply = ask_gemini(history)
    except Exception as e:
        log.error(f"Erreur Gemini texte : {e}")
        reply = f"⚠️ Erreur Gemini : {e}"

    save_message("assistant", reply)

    if tts_enabled:
        audio = await generate_tts_gemini(reply)
        if audio:
            await update.message.reply_audio(
                audio=io.BytesIO(audio),
                title="Dobby",
                performer="Gemini TTS"
            )
            if TTS_ALSO_SEND_TEXT:
                await update.message.reply_text(
                    f"🎙 {transcription}\n\n{reply}"
                )
            return

    await update.message.reply_text(
        f"🎙 {transcription}\n\n{reply}"
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
        reply = ask_gemini_vision(image_bytes, caption)
    except Exception as e:
        log.error(f"Erreur Gemini vision : {e}")
        reply = f"⚠️ Erreur analyse image : {e}"

    await update.message.reply_text(reply)

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    init_db()

    if gemini_client is None:
        log.error("GEMINI_API_KEY manquant — le bot ne peut pas fonctionner")
        return

    log.info("🐶 Dobby démarre — PKA Telegram Bot (Gemini)")

    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("clear",  cmd_clear))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("vocal",  cmd_vocal))
    app.add_handler(CommandHandler("help",   cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))

    log.info("✅ Bot actif — en attente de messages (Gemini)")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
