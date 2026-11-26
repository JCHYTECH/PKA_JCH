---
date: 2026-11-26
source: editorial-dobby
domain: pka/admin
type: registre-abonnements
lang: fr
---

# Registre des abonnements — PKA_JCH

> Registre vivant des abonnements **API / licences / services** de JCH. À mettre à jour à chaque nouvelle souscription.
> Colonnes : **Service · Usage · Plan · Coût · Paiement · Échéance · Désabonnement · Statut**.
> Les champs `?` sont à compléter par JCH (échéances, coûts et cartes exacts sont liés au compte).

---

## Actifs (payants ou prépayés)

| Service | Usage | Plan | Coût | Paiement | Échéance | Désabonnement | Statut |
|---------|-------|------|------|----------|----------|---------------|--------|
| **ElevenLabs** | Voix off (TTS) | Starter | ~5 $/mois | ? | ? | https://elevenlabs.io/app/subscription | ✅ actif |
| **Runway** | Vidéo IA (clips) | Crédits | ~0,12 $/s (Gen-4.5) | ? | ? | https://app.runwayml.com/billing | ✅ actif |
| **DeepSeek API** | LLM + search/fetch | Pay-per-use | ~0,75 $/1000 req (search) | ? | N/A (prépayé) | https://platform.deepseek.com | ✅ |
| **Tavily** | Recherche web | Pay-per-use | ? | ? | ? | https://app.tavily.com | 🔄 à réévaluer (remplacé par DeepSeek natif pour le scripté) |
| **OpenRouter** | Accès multi-modèles | Crédits prépayés | N/A | ? | N/A | https://openrouter.ai/settings/credits | ✅ |
| **Anthropic (Claude)** | LLM | Pay-per-use | N/A | ? | N/A | https://console.anthropic.com/settings/billing | ✅ |
| **OpenAI** | LLM | Pay-per-use | N/A | ? | N/A | https://platform.openai.com/settings/organization/billing | ✅ |
| **Gemini / Google AI Studio** | LLM + TTS + Veo | Pay-per-use | N/A | ? | N/A | https://aistudio.google.com | ✅ |
| **NVIDIA** | API | Pay-per-use | N/A | ? | N/A | ? | ✅ |
| **Ghost(Pro) — `wildens.ghost.io`** | ANCIEN hébergement Ghost.org (abandonné) | Ghost(Pro) | 18 USD/mois | **carte 8847** | ? | https://wildens.ghost.io/ghost | ⚠️ **à résilier** — remplacé par le self-host Hostinger ci-dessous |
| **Ghost — `wildlens.arteon.be`** | Blog / newsletter (NOUVEAU) | Self-host VPS Hostinger KVM 1 | 86,97 €/an (≈7,25 €/mois) | ? | 15/11/2027 | https://www.hostinger.com/vps/ghost-hosting | ✅ VPS payé + Ghost installé 15/11 — reste DNS/SSL/Mailgun/migration |
| **Adobe** (Lightroom/Photoshop) | Photo | Photography ? | ~10–12 $/mois | ? | ? | https://account.adobe.com/plans | ✅ (à confirmer) |
| **Microsoft 365** (jc.havaux@arteon.be — alias jc.havaux@jchytech.be) | Mail pro | ? | ? | ? | ? | https://admin.microsoft.com | ❌ non-admin — tenant géré par Orban 45 (CSP). jchytech.be → arteon.be (arrêt jchytech.be fin 2027) |
| **Canva** | Design / decks | Free ou Pro | 0 ou ~12 $/mois | ? | ? | https://www.canva.com/settings/billing | 🔄 en test |
| **Tailscale** | Réseau (van, M1, iPhone) | Free | 0 | — | N/A | https://login.tailscale.com/admin/settings/billing | ✅ |
| **Dropbox** | Stockage / sync cloud | ? | ? | ? | ? | https://www.dropbox.com/account/plan | ✅ actif |
| **1Password** | Gestionnaire de mots de passe | ? | ? | ? | ? | https://my.1password.com/profile | ✅ actif |
| **CleanMyMac 5** | Maintenance macOS | ? | ? | ? | ? | https://macpaw.com | ✅ actif (possible achat unique) |

## Gratuits / auto-hébergés (pas d'abonnement)

- **Telegram bot** (Dobby) — gratuit.
- **Gmail + Google Calendar** (`jc.havaux@gmail.com`) — gratuit · boîte de consolidation.
- **Yahoo Mail** (`jc_havaux@yahoo.com`) — gratuit · **OAuth ShuttleCloud → Gmail** (CLOS 24/11, ~3 600 mails importés, relève auto).
- **Home Assistant / Zigbee2MQTT / Mosquitto / Plane** — auto-hébergés.
- **Obsidian** — gratuit.

## Considérés mais NON souscrits

- **Gamma** — écarté (Canva choisi).
- **Veo** — écarté (Runway choisi).
- **NotebookLM** — écarté.

## Clés API présentes dans `~/.config/pka-jch/`

`anthropic_key.txt` · `api_keys` · `elevenlabs_api_key.txt` · `runway_api_key.txt` · `gmail_app_password.txt` · `kimi_key.txt` · `nvidia_key.txt` · `openrouter_key.txt` · `plane_api_token.txt` · `telegram_tokens` · `xc_api_key` · `outlook_config.json` · `token.json`

---

*À faire : JC complète les champs `?` (coût exact, carte, échéance) et confirme Dropbox / 1Password / CleanMyMac / Adobe / Microsoft / résiliation Ghost(Pro).*