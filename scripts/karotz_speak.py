#!/usr/bin/env python3
"""karotz_speak — passerelle Dobby → Karotz (avatar physique de Dobby 🦉).

Point d'entrée unique pour faire parler le lapin Karotz et piloter ses
expressions (oreilles, LED, sons) via l'API HTTP OpenKarotz.

C'est le « porte-parole » de Dobby : Dobby génère le texte, ce script le
pousse vers le TTS du lapin. Aucune dépendance tierce (stdlib uniquement).

Usage:
    dobby-speak "bonjour JC"              # le lapin prononce le texte
    echo "bonjour JC" | dobby-speak       # texte via stdin
    dobby-speak --ears 16,16 "bonjour"    # oreilles + parler
    dobby-speak --ears reset              # oreilles au repos
    dobby-speak --led FF0000              # LED rouge (period=500, pulse=1)
    dobby-speak --sound bip1              # joue un son de la bibliothèque
    dobby-speak --health                  # test de connexion

Config (variables d'environnement, défauts entre parenthèses):
    KAROTZ_IP    adresse du lapin (192.168.129.250)
    KAROTZ_PORT  port HTTP (80)
    KAROTZ_RETRIES  nb de tentatives TTS (3)
    KAROTZ_RETRY_DELAY  secondes entre tentatives (5)
"""

import argparse
import json
import os
import select
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

KAROTZ_IP = os.environ.get("KAROTZ_IP", "192.168.129.250")
KAROTZ_PORT = os.environ.get("KAROTZ_PORT", "80")
RETRIES = int(os.environ.get("KAROTZ_RETRIES", "3"))
RETRY_DELAY = int(os.environ.get("KAROTZ_RETRY_DELAY", "5"))
BASE = f"http://{KAROTZ_IP}:{KAROTZ_PORT}"


def _get(path, params=None, timeout=25):
    """GET /cgi-bin/<path>?params → (body_str, http_status)."""
    url = f"{BASE}/cgi-bin/{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": "dobby-speak/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", "replace"), resp.status


def health():
    """Test de connexion : renvoie (ok: bool, detail: str)."""
    try:
        body, status = _get("ears_reset", timeout=8)
        return status == 200, f"HTTP {status} — {body.strip()}"
    except urllib.error.URLError as e:
        return False, f"injoignable : {e.reason}"


def speak(text):
    """Fait parler le lapin. Retente sur WiFi intermittent. → (ok, detail)."""
    if not text or not text.strip():
        return False, "texte vide"
    last = ""
    for attempt in range(1, RETRIES + 1):
        try:
            body, status = _get("tts", {"text": text}, timeout=30)
            if status == 200:
                try:
                    j = json.loads(body)
                    if j.get("played") is True:
                        return True, f"joué (voix {j.get('voicelanguage', '?')}/{j.get('voicegender', '?')})"
                    if j.get("return") is True:
                        return True, body.strip()
                except json.JSONDecodeError:
                    pass
                # HTTP 200 mais réponse non interprétable
                return True, body.strip()
            last = f"HTTP {status} : {body[:120]}"
        except (urllib.error.URLError, TimeoutError, OSError) as e:
            last = f"{type(e).__name__}: {e}"
        if attempt < RETRIES:
            time.sleep(RETRY_DELAY)
    return False, f"échec après {RETRIES} tentatives ({last})"


def ears(left, right):
    """Positionne les oreilles (0–16)."""
    body, status = _get("ears", {"left": left, "right": right})
    return status == 200, body.strip()


def ears_reset():
    body, status = _get("ears_reset")
    return status == 200, body.strip()


def led(color, period=500, pulse=1):
    """Allume la LED (couleur hex, period ms, pulse 0/1)."""
    body, status = _get("leds", {"action": "light", "color": color, "period": period, "pulse": pulse})
    return status == 200, body.strip()


def sound(sound_id):
    """Joue un son de la bibliothèque (voir sound_list)."""
    body, status = _get("sound", {"id": sound_id})
    return status == 200, body.strip()


def _parse_ears(value):
    """'16,16' → (16,16) · 'reset' → None."""
    if value.lower() == "reset":
        return None
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("format attendu : left,right (ex 16,16) ou reset")
    return int(parts[0]), int(parts[1])


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="dobby-speak",
        description="Passerelle Dobby → Karotz : parler + expressions.",
    )
    parser.add_argument("text", nargs="?", help="texte à prononcer (sinon lu sur stdin)")
    parser.add_argument("--ears", type=_parse_ears, metavar="L,R|reset", default=False,
                        help="oreilles : left,right (0–16) ou reset")
    parser.add_argument("--led", metavar="RRGGBB", help="LED : couleur hexadécimale")
    parser.add_argument("--sound", metavar="ID", help="joue un son (id de sound_list)")
    parser.add_argument("--health", action="store_true", help="test de connexion")
    args = parser.parse_args(argv)

    if args.health:
        ok, detail = health()
        print(("✅ " if ok else "❌ ") + detail)
        return 0 if ok else 1

    # Expressions éventuelles (avant la parole)
    if args.ears is not False:  # --ears fourni
        if args.ears is None:   # --ears reset
            ok, detail = ears_reset()
            print(("✅ oreilles reset — " if ok else "❌ oreilles reset — ") + detail)
        else:                    # --ears left,right
            left, right = args.ears
            ok, detail = ears(left, right)
            print((f"✅ oreilles {left},{right} — " if ok else "❌ oreilles — ") + detail)

    if args.led:
        ok, detail = led(args.led)
        print(("✅ LED " + args.led + " — " if ok else "❌ LED — ") + detail)

    if args.sound:
        ok, detail = sound(args.sound)
        print(("✅ son " + args.sound + " — " if ok else "❌ son — ") + detail)

    # Texte : argument puis stdin (sans bloquer si stdin est vide/non-tty)
    text = args.text
    if text is None and not sys.stdin.isatty() and select.select([sys.stdin], [], [], 0)[0]:
        text = sys.stdin.read().strip()

    if text:
        ok, detail = speak(text)
        print(("✅ le lapin parle — " if ok else "❌ — ") + detail)
        return 0 if ok else 1

    # Ni texte ni action → usage court
    if text is None and args.ears is False and not args.led and not args.sound:
        parser.print_help()
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
