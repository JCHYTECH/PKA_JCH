# Catalogue des opérations — Harnais PKA

> Inventaire des opérations déclenchables depuis le dashboard web (Hub JCH).
> Complément de `docs/system/harnais-pka.md` (la carte) — ceci est le **catalogue d'actions**.
> Statut : 🟢 déjà dans le Hub · 🔵 CLI (bin/scripts/skills, à brancher) · ⚙️ automatique (launchd/cron, pas de déclenchement manuel).
> Généré par Dobby 🦉 2026-11-24 — source : scan `bin/` + `scripts/` + `skills/` + routes `dashboard_server.py`.

---

## 1. Modèles & LLM

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Lancer Dobby (par modèle : deepseek/openai/anthropic/kimi/codex/gemini/local) | `bin/dobby.sh --model X` | 🟢 Hub (`/modeles.html`) |
| Router un modèle (tâche → modèle + fallback) | `scripts/pka_model_router.py "<tâche>"` | 🔵 |
| Exécuter via OpenRouter (one-shot) | `scripts/or_route.py "…"` | 🔵 |
| Client unifié | `scripts/model_client.py` | 🔵 |
| Équilibrage & coûts API | `scripts/provider_balance.py` | 🟢 Hub (balances) |

## 2. Inbox & routage

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Router l'inbox | `bin/pka-route` · `skills/ingest` | 🔵 |
| Analyser l'inbox | `skills/inbox-analysis` | 🔵 |
| Notes Apple → inbox | `scripts/apple_notes_to_inbox.py` | 🔵 |
| Récupérer web-clips | `bin/pka-clip-pull` | ⚙️ |
| Surveiller l'inbox | `bin/pka-watch-inbox` | ⚙️ |

## 3. Transcripts & analyse

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Transcrire une URL (YouTube/podcast) | `bin/pka-transcript "<URL>"` | 🔵 |
| **Travailler un transcript** (comprendre/confirmer/conseiller) | `skills/analyse-transcript` | 🔵 |

## 4. Mémoire & knowledge

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Sauvegarder la session | `bin/pka-save` · `bin/pka` | 🔵 |
| Capturer une connaissance | `scripts/pka_memory_capture.py` | 🔵 |
| Revue mémoire | `bin/pka-memory-review` | 🔵 |
| Exporter la mémoire | `scripts/pka_memory_export.py` | 🔵 |
| Honcho (analyse session → USER.md) | `scripts/pka_honcho_analyze.py` | 🔵 |
| Rétrospective | `scripts/dobby_retro.py` | 🔵 |
| **Snapshot d'état** (State files + dérive) | `bin/pka-snapshot` · `scripts/pka_state_snapshot.py` | 🔵 |

## 5. Découvertes & voyages

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Voir découvertes / spots / circuits | `/api/decouvertes` · `/api/spots` · `/api/circuit` | 🟢 Hub |
| Enrichir « où dormir en van » (park4night) | `scripts/decouvertes-collector/` | 🟢 Hub |
| **Lire les snapshots PKA Découvertes** | `scripts/decouvertes-collector/` + `/api/place` | 🟢 Hub |
| Exporter découvertes → planner | `skills/decouvertes-to-planner` · `scripts/decouvertes-to-planner.py` | 🔵 |
| Exporter circuit GPX/KML | `/api/circuit.gpx` · `/api/circuit.kml` | 🟢 Hub |

## 6. Documents & impression

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Imprimer (md/txt/docx/html → PDF → EPSON) | `bin/pka-print` | 🔵 |
| Convertir en PDF | `scripts/md2pdf` | 🔵 |
| WildLens Ghost → PDF | `bin/wildlens-ghost-pdf` | 🔵 |

## 7. Recherche

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Recherche web native DeepSeek | `bin/pka-search` | 🔵 |
| Recherche instinct | `scripts/instinct_search.py` | 🔵 |

## 8. Photo & image

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Vision locale (analyse/OCR image) | `bin/pka-vision` · `scripts/pka_vision_scan.py` | 🔵 |
| Keyworder photo | `scripts/photo_keyworder.py` | 🔵 |
| Analyse EXIF | `scripts/exif_analysis.py` | 🔵 |
| Publier Instagram | `scripts/instagram_post.py` | 🔵 |
| Vérif image générée par IA | `scripts/pka_ai_image_check.py` | 🔵 |

## 9. Backup, sync & sécurité

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Sauvegarde PKA | `bin/pka-backup` | 🔵 |
| Sync → M1 | `bin/sync-to-m1` · `bin/m1-sync` | 🔵 |
| Miroir iCloud | `bin/pka-icloud-mirror` | 🔵 |
| Rotation clés API | `scripts/rotate_*_keys.sh` | 🔵 |
| Garde-fou pré-action | `bin/pka-gate` · `skills/decision-gate` | 🔵 |

## 10. Surveillance & automatisation

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Watchers (inbox/host/box/deadline/freshness/bluetti) | `bin/pka-watch-*` | ⚙️ |
| Boucles (loop/chain/persist) | `bin/pka-loop` · `bin/pka-chain` · `bin/pka-persist` | 🔵 |
| Kanban | `scripts/pka_kanban_service.py` | 🟢 Hub |
| Plane (issues) | `scripts/mcp_plane_server.py` · MCP plane | 🔵 |

## 11. Email & agenda

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Récupérer les mails (IMAP) | `scripts/gmail_imap_fetch.py` · `skills/gmail_imap_fetch` | 🔵 |
| Digest des mails | `scripts/gmail_imap_digest.py` | ⚙️ |
| Agenda Google | `scripts/google_calendar_bridge.py` · MCP gcalendar | 🔵 |

## 12. Voix & audio

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Dictée (Whisper) | `scripts/whisper-dictate.sh` · `bin/dobby-voice` | 🔵 |
| Parler (TTS ElevenLabs) | `scripts/tts_elevenlabs.py` · `bin/dobby-speak` | 🔵 |
| Parler (Karotz) | `scripts/karotz_speak.py` | 🔵 |
| Conversation temps réel | `/api/realtime/call` | 🟢 Hub |

## 13. Délégation & spécialistes

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Conseil multi-perspectives | `skills/conseil` | 🔵 |
| Générer un brief | `skills/brief` | 🔵 |
| Déléguer à un spécialiste | 31 spécialistes `TEAM/` + `agent_open` | 🔵 |

## 14. Projets spécifiques

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| WildNexus : BOM / ADR / bench-loop | `skills/wildnexus-bom` · `wildnexus-adr` · `bench-loop` | 🔵 |
| InsectNet : bioacoustique (QC, segment, inventory) | `scripts/insectnet_*.py` | 🔵 |
| Vetalyx : rapport allergie | `scripts/build_vetalyx_rapid_allergy_report.py` | 🔵 |
| FutureInvest : veille matières | `scripts/futureinvest_commodity_watch.py` | ⚙️ |
| Vente occasion | `skills/vente-occasion` | 🔵 |
| Traduction bilingue Jade | `skills/jade-traduction-bilingue` | 🔵 |

## 15. Système & maintenance

| Opération | Déclencheur | Statut |
|-----------|-------------|--------|
| Health-check système | `scripts/pka_system_check.py` · `skills/pka-system-check` | 🔵 |
| Maintenance vault | `scripts/pka_vault_maintenance.py` | ⚙️ |
| Vérif structure | `scripts/pka_structure_check.py` | 🔵 |
| Nettoyage artefacts | `bin/pka-cleanup` | 🔵 |
| Graphify (update/query) | `bin/pka-graphify-auto` · `graphify` | 🔵 |

---

## Synthèse

- **Total opérations recensées : ~65** (hors watchers/automations internes).
- **Déjà dans le Hub : ~10** (lancement modèle, kanban, file-index, découvertes, balances, voix temps réel).
- **À brancher dans le Hub : ~50** — c'est le chantier « interface de lancement ».
- **Automatiques (pas de bouton) :** watchers, digest, vault maintenance, veille matières.

*Catalogue v1 — Dobby 🦉 2026-11-24.*
