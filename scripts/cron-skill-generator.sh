#!/bin/bash
# PKA Skill Generator — hebdomadaire (dimanche 22h)
# Analyse les patterns retro et propose des skills candidates
# Lance via launchd (com.dobby.skill-generator)
cd ~/PKA_JCH || { echo "PKA_JCH introuvable"; exit 1; }

PYTHON="/Library/Frameworks/Python.framework/Versions/3.13/bin/python3"

echo "[$(date)] Skill generator start"
$PYTHON scripts/pka_skill_generator.py --auto --days 14 2>&1
GEN_EXIT=$?
echo "[$(date)] Skill generator done (exit=$GEN_EXIT)"
