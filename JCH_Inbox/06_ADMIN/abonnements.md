---
date: 2026-11-01
source: editorial-dobby
domain: pka/admin
type: registre-abonnements
lang: fr
---

# Registre des abonnements — PKA_JCH

> Registre vivant des abonnements **API / licences** de JCH. À mettre à jour à chaque nouvelle souscription.
> Colonnes : **Service · Usage · Plan · Coût · Échéance · Désabonnement · Statut**.
> Les champs `?` sont à compléter par JCH (échéances et coûts exacts sont liés au compte).

---

## Actifs (payants ou prépayés)

| Service | Usage | Plan | Coût | Échéance | Désabonnement | Statut |
|---------|-------|------|------|----------|---------------|--------|
| **ElevenLabs** | Voix off (TTS) | Starter | ~5 $/mois | ? | https://elevenlabs.io/app/subscription | ✅ actif (2026-11-01) |
| **Runway** | Vidéo IA (clips) | Crédits | ~0,12 $/s (Gen-4.5) | ? | https://app.runwayml.com/billing | ✅ actif (2026-11-01) |
| **DeepSeek API** | LLM + search/fetch | Pay-per-use | ~0,75 $/1000 req (search) | N/A (prépayé) | https://platform.deepseek.com | ✅ |
| **Tavily** | Recherche web (`web_search`) | Pay-per-use / plan | ? | ? | https://app.tavily.com | ✅ |
| **OpenRouter** | Accès multi-modèles | Crédits prépayés | N/A | N/A | https://openrouter.ai/settings/credits | ✅ |
| **Anthropic (Claude)** | LLM | Pay-per-use | N/A | N/A | https://console.anthropic.com/settings/billing | ✅ |
| **OpenAI** | LLM | Pay-per-use | N/A | N/A | https://platform.openai.com/settings/organization/billing | ✅ |
| **Gemini / Google AI Studio** | LLM + TTS + Veo | Pay-per-use | N/A | N/A | https://aistudio.google.com | ✅ |
| **NVIDIA** | API | Pay-per-use | N/A | N/A | ? | ✅ |
| **Ghost** (wildlens.ghost.io) | Blog / newsletter | Ghost(Pro) ? | ~9–31 $/mois | ? | https://ghost.org/account | ✅ (à vérifier) |
| **Adobe** (Lightroom/Photoshop) | Photo | Photography ? | ~10–12 $/mois | ? | https://account.adobe.com/plans | ✅ (à confirmer) |
| **Microsoft 365** (jc.havaux@jchytech.be) | Mail pro | ? | ? | ? | https://admin.microsoft.com | ✅ (à confirmer) |
| **Canva** | Design / decks | Free ou Pro | 0 ou ~12 $/mois | ? | https://www.canva.com/settings/billing | 🔄 en test |
| **Tailscale** | Réseau (van, M1, iPhone) | Free | 0 | N/A | https://login.tailscale.com/admin/settings/billing | ✅ |

## Gratuits / auto-hébergés (pas d'abonnement)

- **Telegram bot** (Dobby) — gratuit.
- **Gmail + Google Calendar** — gratuit.
- **Home Assistant / Zigbee2MQTT / Mosquitto / Plane** — auto-hébergés (local, `_local/`).
- **Obsidian** — gratuit.

## Considérés mais NON souscrits

- **Gamma** — écarté (Canva choisi).
- **Veo** — écarté (Runway choisi).
- **NotebookLM** — écarté (ne fait pas de slides).

## Clés API présentes dans `~/.config/pka-jch/`

`anthropic_key.txt` · `api_keys` (OpenAI, Gemini, NVIDIA, OpenRouter, DeepSeek) · `elevenlabs_api_key.txt` · `runway_api_key.txt` · `gmail_app_password.txt` · `kimi_key.txt` · `nvidia_key.txt` · `openrouter_key.txt` · `plane_api_token.txt` · `telegram_tokens` · `xc_api_key` (à identifier) · `outlook_config.json` · `token.json`

---

*À faire : JC complète les champs `?` (coût exact + échéance) pour chaque service payant, et confirme Adobe/Microsoft/Ghost.*
