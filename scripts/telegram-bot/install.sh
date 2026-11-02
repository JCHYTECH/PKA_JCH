#!/bin/bash
# ═══════════════════════════════════════════════════════════════
#  Dobby Telegram Bot — Script d'installation automatique
#  Lance ce script UNE SEULE FOIS depuis le terminal.
#  Usage : bash install.sh
# ═══════════════════════════════════════════════════════════════

set -e  # arrêt immédiat si une commande échoue

BOT_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$BOT_DIR/venv"
PLIST_NAME="com.pka.dobby.plist"
LAUNCH_AGENTS="$HOME/Library/LaunchAgents"

echo ""
echo "🐶 Installation Dobby Telegram Bot"
echo "📁 Dossier : $BOT_DIR"
echo ""

# ── Étape 1 : Vérifier Python ────────────────────────────────
echo "① Vérification Python..."
if ! command -v python3 &>/dev/null; then
    echo "❌ Python 3 non trouvé. Installe-le depuis python.org"
    exit 1
fi
PYTHON_VERSION=$(python3 --version)
echo "   ✓ $PYTHON_VERSION"

# ── Étape 2 : Créer l'environnement virtuel ──────────────────
echo "② Création de l'environnement virtuel..."
if [ -d "$VENV_DIR" ]; then
    echo "   ℹ️  Environnement virtuel déjà existant — ignoré"
else
    python3 -m venv "$VENV_DIR"
    echo "   ✓ venv créé dans $VENV_DIR"
fi

# ── Étape 3 : Installer les dépendances ─────────────────────
echo "③ Installation des dépendances..."
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$BOT_DIR/requirements.txt" -q
echo "   ✓ Dépendances installées"

# ── Étape 4 : Vérifier le fichier .env ──────────────────────
echo "④ Vérification du fichier .env..."
if [ ! -f "$BOT_DIR/.env" ]; then
    echo ""
    echo "   ⚠️  Fichier .env manquant !"
    echo "   Action requise : copie .env.example en .env et remplis les valeurs :"
    echo "   cp $BOT_DIR/.env.example $BOT_DIR/.env"
    echo "   Puis édite $BOT_DIR/.env avec tes clés API"
    echo ""
    echo "   Relance ce script après avoir rempli .env"
    exit 1
fi

# Vérifier que les clés essentielles sont présentes
source "$BOT_DIR/.env"
MISSING=0
if [ -z "$TELEGRAM_TOKEN" ]; then echo "   ❌ TELEGRAM_TOKEN manquant dans .env"; MISSING=1; fi
if [ -z "$TELEGRAM_USER_ID" ]; then echo "   ❌ TELEGRAM_USER_ID manquant dans .env"; MISSING=1; fi
if [ -z "$ANTHROPIC_API_KEY" ]; then echo "   ❌ ANTHROPIC_API_KEY manquant dans .env"; MISSING=1; fi
if [ $MISSING -eq 1 ]; then exit 1; fi
echo "   ✓ .env complet"

# ── Étape 5 : Créer le plist launchd ────────────────────────
echo "⑤ Création du service launchd (démarrage automatique)..."

PYTHON_BIN="$VENV_DIR/bin/python3"
BOT_SCRIPT="$BOT_DIR/bot.py"
LOG_FILE="$BOT_DIR/dobby.log"

cat > "$LAUNCH_AGENTS/$PLIST_NAME" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.pka.dobby</string>

  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON_BIN</string>
    <string>$BOT_SCRIPT</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$BOT_DIR</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/usr/local/bin:/usr/bin:/bin</string>
  </dict>

  <key>StandardOutPath</key>
  <string>$LOG_FILE</string>

  <key>StandardErrorPath</key>
  <string>$LOG_FILE</string>

  <!-- Redémarre automatiquement si le bot plante -->
  <key>KeepAlive</key>
  <true/>

  <!-- Démarre au login -->
  <key>RunAtLoad</key>
  <true/>

  <!-- Attend 10 secondes avant de redémarrer après un crash -->
  <key>ThrottleInterval</key>
  <integer>10</integer>
</dict>
</plist>
PLIST

echo "   ✓ Plist créé : $LAUNCH_AGENTS/$PLIST_NAME"

# ── Étape 6 : Charger et démarrer le service ─────────────────
echo "⑥ Démarrage du service..."

# Décharger s'il était déjà chargé
launchctl unload "$LAUNCH_AGENTS/$PLIST_NAME" 2>/dev/null || true

# Charger et démarrer
launchctl load "$LAUNCH_AGENTS/$PLIST_NAME"
echo "   ✓ Service chargé"

sleep 2

# Vérifier que le bot tourne
if launchctl list | grep -q "com.pka.dobby"; then
    echo ""
    echo "═══════════════════════════════════════════════════"
    echo "  ✅ Dobby est en ligne !"
    echo ""
    echo "  Pour tester : envoie /start à ton bot Telegram"
    echo "  Logs : tail -f $LOG_FILE"
    echo "  Arrêter : launchctl unload $LAUNCH_AGENTS/$PLIST_NAME"
    echo "  Redémarrer : launchctl kickstart -k gui/\$(id -u)/com.pka.dobby"
    echo "═══════════════════════════════════════════════════"
else
    echo ""
    echo "⚠️  Le service semble ne pas avoir démarré."
    echo "   Vérifie les logs : cat $LOG_FILE"
fi
