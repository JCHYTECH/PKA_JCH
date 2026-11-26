---
date: 2026-11-24
source: dobby
domain: ai-it-tools
project: AI_IT_TOOLS
status: note
type: note-technique
lang: fr
tags:
  - MoE
  - offload
  - ollama
  - modele-local
  - edge-ai
---

# Note technique — MoE offload : faire tourner un ~35 B sur une carte 8 Go

> Veille Kiara · IA locale (2026-11-18). Transcript : `99_REFERENCES/moe-offload-vram-8go_2026-11-18/`.
> Pertinence PKA : modèles locaux M1 (Ollama) + edge-ai-loop. Statut : note de compréhension, pas une action.

## Le principe (ce qui est établi)

- Un modèle **dense** charge tous ses poids à chaque token → impossible de dépasser la VRAM.
- Un **Mixture-of-Experts (MoE)** n'active qu'un sous-ensemble d'experts par token via un **routeur** :
  à chaque token, le routeur choisit **8 experts sur 256** (Qwen) ; seuls eux calculent.
- Conséquence : les experts inactifs peuvent rester **en RAM** (offload) — on ne garde en VRAM que
  les parties communes + les experts des premières couches.

## Chiffres annoncés (dires de la vidéaste, à confirmer au banc)

| Élément | Valeur annoncée |
|---|---|
| Modèle | Qwen ~35 B (Q4, ~20 Go) |
| En VRAM | ~6 Go (parties communes + experts de 8 couches) |
| En RAM | ~14,5 Go (experts des 32 autres couches) |
| Débit mesuré | 66 tok/s |
| Coût | à taille égale, le MoE « raisonne un peu moins bien » qu'un dense |

## Application PKA

- **M1 (32 Go, Ollama)** : déjà du MoE en pratique — `qwen3:30b-a3b` est un MoE 30 B / 3 B actifs.
  La RAM unifiée du M1 joue le rôle de l'« offload » sans pénalité GPU↔RAM. Aucune action nouvelle :
  la matrice le liste déjà. La vidéo confirme que la voie MoE est la bonne pour du « gros » en local.
- **Carte GPU 8 Go** (si JC en ajoute une, ex. eGPU) : la technique permet de charger un ~35 B au lieu
  d'un ~7 B. À considérer seulement si un besoin GPU réel apparaît.
- **edge-ai-loop (TinyML, ESP32)** : pertinence **faible** — le MoE offload vise des GPU/RAM, pas des
  microcontrôleurs. Ne pas transposer.

## Limites (honnêteté)

- MoE < dense à taille égale (qualité).
- Latence : un aller-retour RAM ≈ 5× plus lent que la VRAM (atténué par le faible nombre d'experts actifs).
- Piège de vocabulaire : « E4B » chez Gemma = *effective* (petit modèle téléphone), pas *experts*.

## Actions

- **P2 · (Dobby)** Rien d'urgent. Garder comme référence si la question « gros modèle local » revient.
- **P2 · (Forge)** Si eGPU envisagé un jour, comparer MoE-offload vs RAM unifiée M1 avant achat.
