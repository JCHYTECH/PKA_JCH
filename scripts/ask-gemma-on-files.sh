#!/bin/bash
# shell/ask-gemma-on-files.sh — Exécute gemma3 sur M1 avec fichiers locaux
# Usage:
#   ssh m1@100.73.212.110 "bash -s" < ask-gemma-on-files.sh
#
# Ou directement depuis M5 :
#   cat ask-gemma-on-files.sh | ssh m1@100.73.212.110 bash

set -e

cd ~/PKA_JCH

# Lister les fichiers disponibles
FILES=(
  projects/03_WILDNEXUS/01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md
  projects/03_WILDNEXUS/01_FOUNDATION/MASTER_ARCHITECTURE_WN.md
  projects/03_WILDNEXUS/02_DECISIONS/ADR/ADR-001-choix-mcu-p0.md
  projects/03_WILDNEXUS/02_DECISIONS/ADR/ADR-005-energie-autonomie-p0.md
)

echo "=== FICHIERS ===" > /tmp/context.txt
for f in "${FILES[@]}"; do
  if [ -f "$f" ]; then
    echo "--- $f ---" >> /tmp/context.txt
    head -100 "$f" >> /tmp/context.txt
    echo "" >> /tmp/context.txt
  fi
done

echo "=== PROMPT ===" >> /tmp/context.txt
cat >> /tmp/context.txt << 'PROMPT'
A partir des fichiers ci-dessus, repond en francais de facon concise:
1. Quel MCU est choisi et pourquoi ?
2. L'autonomie de 60 jours est-elle credible ?
3. Quels sont les 2 plus gros risques techniques ?
4. Recommendation #1 pour le P0 ?

Utilise uniquement les fichiers ci-dessus. Max 250 mots.
PROMPT

echo "Requete envoyee a gemma3..."
ollama run gemma3:12b-it-qat < /tmp/context.txt 2>/dev/null
