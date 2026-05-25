#!/bin/bash
# deploy_rpi.sh — Déploie l'agent procurement PKA sur le Raspberry Pi
# Usage : ./scripts/procurement/deploy_rpi.sh
# Depuis la racine du projet PKA_JCH

set -e

RPI_HOST="jchavaux@192.168.1.48"
RPI_DIR="/home/jchavaux/pka/procurement"
FIXTURES_DIR="$RPI_DIR/fixtures"

echo "🚀 Déploiement Procurement Agent → RPi ($RPI_HOST)"
echo ""

# 1. Créer les dossiers sur le RPi
echo "📁 Création arborescence RPi..."
ssh "$RPI_HOST" "mkdir -p $RPI_DIR $FIXTURES_DIR"

# 2. Transférer les scripts Python
echo "📤 Transfert scripts procurement..."
scp scripts/procurement/__init__.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/models.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/config.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/bom_parser.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/api_client.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/llm_reasoner.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/bom_writer.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/report_writer.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/cart_client.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/main.py "$RPI_HOST:$RPI_DIR/"
scp scripts/procurement/requirements.txt "$RPI_HOST:$RPI_DIR/"

# 3. Transférer les fixtures de test
echo "📤 Transfert fixtures..."
scp tests/procurement/fixtures/sample_bom.xlsx "$RPI_HOST:$FIXTURES_DIR/" 2>/dev/null || true
scp tests/procurement/fixtures/sample_bom.csv "$RPI_HOST:$FIXTURES_DIR/" 2>/dev/null || true
scp tests/procurement/fixtures/sample_bom.md "$RPI_HOST:$FIXTURES_DIR/" 2>/dev/null || true

# 4. Installer les dépendances
echo "📦 Installation dépendances Python sur RPi..."
ssh "$RPI_HOST" "pip3 install -r $RPI_DIR/requirements.txt --quiet"

echo ""
echo "✅ Déploiement terminé."
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📋 ÉTAPES SUIVANTES"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "1. WHITELISTING IP MOUSER"
echo "   Trouve ton IP publique :"
echo "   $ curl -s ifconfig.me"
echo "   → Ajoute cette IP sur developer.mouser.com (ton app → IP Whitelist)"
echo ""
echo "2. CONFIGURER LES CLÉS API SUR LE RPI"
echo "   $ ssh $RPI_HOST"
echo "   $ cat > ~/.procurement.env << 'EOF'"
echo "   MOUSER_API_KEY=ta_cle_mouser_ici"
echo "   ANTHROPIC_API_KEY=ta_cle_anthropic_ici"
echo "   EOF"
echo "   $ chmod 600 ~/.procurement.env"
echo ""
echo "3. TESTER EN MODE SIMULATION"
echo "   $ ssh $RPI_HOST"
echo "   $ cd $RPI_DIR"
echo "   $ python3 main.py --project TEST --bom fixtures/sample_bom.csv --output /tmp/test"
echo ""
echo "4. COMMANDE WILDNEXUS (quand clés configurées)"
echo "   $ python3 main.py --project WILDNEXUS \\"
echo "       --bom /chemin/vers/WILDNEXUS_BOM_P0_v0.2.xlsx \\"
echo "       --output ~/pka/TEAM_Inbox"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
