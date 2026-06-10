#!/bin/bash
# ask-gemma-wildnexus-audit.sh — Analyse complète WildNexus par gemma3
# À exécuter SUR M1 : bash ~/PKA_JCH/scripts/ask-gemma-wildnexus-audit.sh
# Depuis M5 : cat scripts/ask-gemma-wildnexus-audit.sh | ssh m1@100.73.212.110 bash

set -e
cd ~/PKA_JCH/projects/03_WILDNEXUS || { echo "Dossier WildNexus introuvable sur M1"; exit 1; }

CTX="/tmp/wildnexus_audit_context.txt"
echo "=== WILDNEXUS — CONTEXTE PROJET ===" > "$CTX"
echo "" >> "$CTX"

# FICHIER 1 : P0 Scope Lock
echo "--- 01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md ---" >> "$CTX"
if [ -f "01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md" ]; then cat "01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 2 : MASTER ARCHITECTURE (debut)
echo "--- 01_FOUNDATION/MASTER_ARCHITECTURE_WN.md (lignes 1-150) ---" >> "$CTX"
if [ -f "01_FOUNDATION/MASTER_ARCHITECTURE_WN.md" ]; then head -150 "01_FOUNDATION/MASTER_ARCHITECTURE_WN.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 3 : ADR-001 MCU
echo "--- 02_DECISIONS/ADR/ADR-001-choix-mcu-p0.md ---" >> "$CTX"
if [ -f "02_DECISIONS/ADR/ADR-001-choix-mcu-p0.md" ]; then cat "02_DECISIONS/ADR/ADR-001-choix-mcu-p0.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 4 : ADR-003 Radio
echo "--- 02_DECISIONS/ADR/ADR-003-choix-radio-lpwan-p0.md ---" >> "$CTX"
if [ -f "02_DECISIONS/ADR/ADR-003-choix-radio-lpwan-p0.md" ]; then cat "02_DECISIONS/ADR/ADR-003-choix-radio-lpwan-p0.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 5 : ADR-005 Energie
echo "--- 02_DECISIONS/ADR/ADR-005-energie-autonomie-p0.md ---" >> "$CTX"
if [ -f "02_DECISIONS/ADR/ADR-005-energie-autonomie-p0.md" ]; then cat "02_DECISIONS/ADR/ADR-005-energie-autonomie-p0.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 6 : ADR-006 Boitier
echo "--- 02_DECISIONS/ADR/ADR-006-boitier-ip67-montage-terrain.md ---" >> "$CTX"
if [ -f "02_DECISIONS/ADR/ADR-006-boitier-ip67-montage-terrain.md" ]; then cat "02_DECISIONS/ADR/ADR-006-boitier-ip67-montage-terrain.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 7 : ADR-007 Detection evenementielle
echo "--- 02_DECISIONS/ADR/ADR-007-detection-evenementielle-p0.md ---" >> "$CTX"
if [ -f "02_DECISIONS/ADR/ADR-007-detection-evenementielle-p0.md" ]; then cat "02_DECISIONS/ADR/ADR-007-detection-evenementielle-p0.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

# FICHIER 8 : Budget P0
echo "--- 03_P0_ENGINEERING/WILDNEXUS_P0_BUDGET_RANGE.md ---" >> "$CTX"
if [ -f "03_P0_ENGINEERING/WILDNEXUS_P0_BUDGET_RANGE.md" ]; then cat "03_P0_ENGINEERING/WILDNEXUS_P0_BUDGET_RANGE.md" >> "$CTX"; else echo "MANQUANT" >> "$CTX"; fi
echo "" >> "$CTX"

echo "" >> "$CTX"
echo "=== PROMPT ===" >> "$CTX"
cat >> "$CTX" << 'PROMPT'

Tu es consultant en ingénierie embarquée et IoT. Tu travailles en français. Tu fais une revue de conception critique.

Tu viens de lire les documents fondateurs du projet WildNexus (noeud caméra autonome d'observation écologique). Analyse les failles, risques et angles morts dans les 8 dimensions suivantes.

Pour chaque faille, donne obligatoirement :
- La faille / le risque (une phrase)
- La sévérité (Critique / Haute / Moyenne / Basse)
- La mitigation concrète (une phrase)
- UNE référence précise à un fichier, ADR ou donnée lue ci-dessus qui justifie ton analyse

Si tu cites un chiffre (autonomie, budget, capacité, portée radio, etc.), vérifie qu'il provient des fichiers ci-dessus. Ne fabrique pas de données.

Dimensions à couvrir :
1. Hardware et composants (MCU, caméra, stockage)
2. Autonomie et énergie (budget, batteries, régulateur)
3. Logiciel embarqué (filtre animal, détection événementielle, RTC)
4. Terrain et environnement (boîtier IP67, montage, condensation, fixation)
5. Transmission LPWAN (LoRa, portée forêt, bande passante)
6. Gestion de projet et scope (budget, jalons, supply chain)
7. Sécurité et intégrité (vol, corruption données, chiffrement)
8. Test et validation (comment valider les 60 jours, protocole test)

Conclus par :
- NOTE SUR 10 de la maturité du projet P0
- RECOMMANDATION UNIQUE la plus importante pour JCH

Sois impitoyable et précis. Tu as les vrais documents, utilise-les.
PROMPT

echo ""
echo "CONTEXTE: $(wc -l < "$CTX") lignes"
ollama run gemma3:12b-it-qat < "$CTX" 2>/dev/null
echo "=== FIN ==="