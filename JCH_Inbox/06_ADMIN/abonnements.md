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
| **Tavily** | Recherche web (`web_search` interactif + lightroom MCP) | Pay-per-use / plan | ? | ? | https://app.tavily.com | 🔄 à réévaluer — remplacé par DeepSeek natif (`bin/pka-search`) pour le scripté |
| **OpenRouter** | Accès multi-modèles | Crédits prépayés | N/A | N/A | https://openrouter.ai/settings/credits | ✅ |
| **Anthropic (Claude)** | LLM | Pay-per-use | N/A | N/A | https://console.anthropic.com/settings/billing | ✅ |
| **OpenAI** | LLM | Pay-per-use | N/A | N/A | https://platform.openai.com/settings/organization/billing | ✅ |
| **Gemini / Google AI Studio** | LLM + TTS + Veo | Pay-per-use | N/A | N/A | https://aistudio.google.com | ✅ |
| **NVIDIA** | API | Pay-per-use | N/A | N/A | ? | ✅ |
| **Ghost** (wildlens.arteon.be) | Blog / newsletter | Self-host sur VPS Hostinger KVM 1 (1 an) | 86,97 €/an TTC (≈7,25 €/mois) | 15/11/2027 | https://www.hostinger.com/vps/ghost-hosting | ✅ VPS payé + Ghost installé 15/11 — reste DNS/SSL/Mailgun/migration |
| **Adobe** (Lightroom/Photoshop) | Photo | Photography ? | ~10–12 $/mois | ? | https://account.adobe.com/plans | ✅ (à confirmer) |
| **Microsoft 365** (jc.havaux@arteon.be — alias jc.havaux@jchytech.be) | Mail pro | ? | ? | ? | https://admin.microsoft.com | ❌ non-admin — tenant géré par Orban 45 (CSP). jchytech.be → arteon.be (arrêt jchytech.be fin 2027). Domaine arteon.be : Gandi (registrar/DNS), web Hostinger, mail M365/Exchange. |
| **Canva** | Design / decks | Free ou Pro | 0 ou ~12 $/mois | ? | https://www.canva.com/settings/billing | 🔄 en test |
| **Tailscale** | Réseau (van, M1, iPhone) | Free | 0 | N/A | https://login.tailscale.com/admin/settings/billing | ✅ |

## Gratuits / auto-hébergés (pas d'abonnement)

- **Telegram bot** (Dobby) — gratuit.
- **Gmail + Google Calendar** (`jc.havaux@gmail.com`) — gratuit · **boîte de consolidation** (arteon.be forward + Yahoo POP3, 24/11).
- **Yahoo Mail** (`jc_havaux@yahoo.com`) — gratuit · **POP3 → Gmail** (import ShuttleCloud, 24/11) · 2FA + mot de passe renouvelés 24/11 · email jchytech.be retiré (forwarde vers arteon.be).
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
