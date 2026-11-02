#!/bin/bash
# setup_ollama_m1.sh — Ollama + modèles recommandés pour M1 32 Go
# Usage : bash setup_ollama_m1.sh

set -e

echo "=== 1/5 Installation Ollama ==="
if ! command -v ollama &> /dev/null; then
    curl -fsSL https://ollama.com/install.sh | sh
else
    echo "Ollama déjà installé : $(ollama --version)"
fi

echo ""
echo "=== 2/5 Démarrage du serveur Ollama ==="
ollama serve &
sleep 3

echo ""
echo "=== 3/5 Téléchargement des modèles ==="
MODELS=(
    "qwen2.5:32b"
    "deepseek-r1:14b"
    "codestral:22b"
    "llama3.2:3b"
)

for model in "${MODELS[@]}"; do
    echo ""
    echo "--- Pull $model ---"
    ollama pull "$model"
done

echo ""
echo "=== 4/5 Libération RAM ==="
sudo purge 2>/dev/null || echo "(sudo purge non disponible — skip)"

echo ""
echo "=== 5/5 Vérification ==="
ollama list

echo ""
echo "=== Terminé ==="
echo "Modèles installés : 4"
echo ""
echo "Pour tester : ollama run qwen2.5:32b \"Bonjour\""
echo "API dispo sur : http://localhost:11434"
