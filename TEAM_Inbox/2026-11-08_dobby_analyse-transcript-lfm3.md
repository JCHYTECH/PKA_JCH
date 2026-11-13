# Analyse transcript — Liquid AI LFM3 (1.7B « triple-hybride »)

> Dobby 🦉 — 2026-11-08 — Projet 01_AI_IT_TOOLS
> Source : `NoteGPT_Transcript_LFM3 l’IA locale franchit un nouveau cap (6× plus petit).txt` (YouTube, FR)

## Nature

Vulgarisation technique FR (~13,5 min), chaîne « nerds ». Présentation d'un modèle + explication d'architecture.

## Thèse

Liquid AI sort LFM3, un modèle 1,7B qui bat Qwen 2.5 7B (≈6× plus gros) sur des benchmarks agents grâce à une architecture « triple-hybride » ; quantisé 4-bit ≈ 1 Go → IA locale viable sur hardware modeste (dont RPi 5).

## Points clés

- 6 variantes : text, vision, audio, omni + 2 modèles de décision (D1 2B, D1 Omni 2B) qui renvoient une décision structurée (catégorie / score) sans générer de texte.
- Architecture 24 couches = 13 convolutions courtes + 5 sliding-window attention (256 tokens) + 6 global attention.
- Testé sur 14 combos hardware (smartphones, RPi 5, Apple / AMD) ; 1,8–2,8× plus rapide que le concurrent proche.
- KV cache ~1,6 Go @128k contexte (vs ~4,3 Go pour Qwen 2.5 4B).
- Compatible llama.cpp + MLX (Mac) ; poids ouverts sur Hugging Face.
- Licence : usage commercial gratuit réservé aux entreprises < 10 M$ de CA annuel.

## Confirmer

- ✅ **Établi** : Liquid AI (fondateurs issus du MIT) existe ; LFM3 et l'architecture hybride sont réels ; poids ouverts.
- ⚠️ **Affirmé (auteur)** : victoire sur Qwen 2.5 7B sur « plusieurs benchmarks agents » ; vitesses 1,8–2,8× ; chiffres KV cache.
- ❓ **Non prouvé / à vérifier** : date « présenté le 27 octobre 2024 » (incohérente avec le contexte 2026 — le transcript peut être ancien ou mal daté).
- Contrepoint de la source elle-même : « il reste en retrait sur certaines tâches, notamment la programmation ».

## Conseiller

- **Routing** : `01_AI_IT_TOOLS/99_REFERENCES/lfm3-liquid-ai_2026-11-08/`.
- **Impact croisé** : 🟡 WildNexus / edge-ai (modèle embarqué, RPi 5 testé → pertinent pour edge-ai-loop et le matériel WildNexus gelé) ; 🟢 AI_IT_TOOLS (MLX local sur M5 / M1).
- **Action proposée** : P2 — veille ; tester LFM3 1.7B quantisé en local (MLX sur M5) si on veut un modèle léger embarqué. Vérifier la date de sortie avant de baser une décision dessus.
