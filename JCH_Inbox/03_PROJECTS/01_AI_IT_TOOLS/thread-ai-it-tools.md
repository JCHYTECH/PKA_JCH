# Thread — AI_IT_TOOLS

> Living document — maintenu par Dobby 🦉 en fin de session sur `/save`.
> **Dernière mise à jour** : 2026-11-23 — Hammerspoon installé (bascule curseur entre écrans M5) ; file CUPS EPSON corrigée (.75) + `pka-print` outputorder=normal ; flux mail OAuth nettoyés (socle IMAP) + consentement Graph arteon.be préparé (lecture seule) ; 3 modèles Ollama cœur restaurés sur M1 (10 modèles / 85 Go)
> **Statut** : 🟢 actif

---

## Vue d'ensemble

Infrastructure IA et outils PKA — maintenance du système Dobby, skills, mémoire, modèles, et architecture multi-modèles (DeepSeek, Kimi, Grok, Claude, Gemini, Qwen). Hub OpenRouter structuré. Bootstrap mémoire v2 opérationnel. Interconnexion MCP Home Assistant locale et read-only vérifiée avec Kimi et DeepSeek.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟢 | Système stable, P0-P2 terminés (19/06) |
| Skills | 🟢 | **34 skills** (comptage 22/10), shadow système |
| Memory Layer | 🟢 | MEMORY.md + team.db + FTS5 (67 sessions indexées) + boucle autonome |
| Boucle mémoire | 🟢 | **Nouveau 22/10** — `bin/pka-memory-review` (review LLM + auto-skill), launchd quotidien 09:15 |
| Gouvernance MCP | 🟢 | **Nouveau 22/10** — `pka_mcp_guard.py` (registre + scan tool poisoning) |
| Tracing coûts | 🟢 | **Nouveau 22/10** — `pka_llm_trace.py`, table `llm_calls` |
| Banc mémoire | 🟢 | **Nouveau 22/10** — `pka_memory_eval.py`, hit@5 66,7 %, MRR 0,556 |
| Export portable | 🟢 | **Nouveau 22/10** — `pka_memory_export.py`, 322 faits atomiques |
| OpenRouter Hub | 🟢 | Restructuré 01/07, multi-modèle opérationnel |
| Grok / Codex | 🟠 | Prototype validé en `exec` : mémoire isolée, MCP, délégation, graphify ; TUI et intégrations externes non certifiés |
| Clôture Kimi | 🟢 | Skill `/save` créé ; invocation utilisateur et sauvegarde complète validées le 05/11 avec `kimi-code`. Le TUI Grok reste un essai distinct |
| MCP multi-clients | 🟡 | `ha-lupo-ro` configuré pour Kimi, DeepSeek et Claude ; appels capteurs réels réussis dans Kimi et DeepSeek. Claude nécessite une réauthentification Anthropic ; Codex a réussi OAuth HA mais ses modèles sont refusés par le compte. Aucun accès public pour ChatGPT Web |
| Code base | 🟢 | **126 scripts Python**, 57 binaires `bin/`, 117 fichiers `.md` |
| Miroir iMac↔M5 | 🟢 | Pont noVNC (websockify 6080 → VNC 5900 M5), launchd auto-start ; l'iMac 2017 affiche l'écran du M5 via Safari |
| Miroir iMac↔M1 | 🟢 | **Nouveau 13/11** — pont noVNC port 6081 → VNC 5900 M1 (VNC legacy activé via kickstart) ; l'iMac affiche l'écran du M1 via Safari |

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-11-23 | Périmètre Graph arteon.be réduit en lecture seule | App 31f92869 : Mail.Read, Calendars.Read, Contacts.Read, User.Read (déléguées). Mail.Send + écritures retirés pour faciliter le consentement Orban45 |
| 2026-11-23 | Roster Ollama M1 maintenu à 10 modèles | qwen2.5-coder 14b/32b et gemma3:27b jugés redondants ; re-téléchargés seulement à l'usage (gemma3:27b si Cozmo démarre) |
| 2026-11-11 | Pont noVNC pour le miroir iMac↔M5 | iMac 2017 non éligible AirPlay + partage d'écran Apple Ventura↔macOS 26 incompatible → noVNC navigateur (zéro install iMac, auto-start launchd) |
| 2026-11-07 | Recherche scriptée basculée sur DeepSeek natif | `bin/pka-search` (Search/Fetch, $0.75/1k) ; Tavily conservé pour l'interactif TUI et le MCP Lightroom |
| 2026-11-07 | Sous-agents ouverts en `deepseek-v4-flash` | Règle AGENTS.md (RÈGLE DÉLÉGATION) ; orchestrateur reste en `deepseek-v4-pro`. Le TUI 0.8.39 n'a pas de clé `[subagents]` — pilotage au niveau du `model` d'`agent_open` |
| 2026-11-06 | Relais MCP Home Assistant local et read-only pour les clients IA | Outils d’action filtrés ; Kimi et DeepSeek validés par appels réels. Ne pas exposer HA publiquement pour élargir les clients |
| 2026-11-05 | Prototype Grok séparé via Codex/OpenRouter | `bin/dobby.sh` inchangé ; capacités locales essentielles validées, limites explicites |
| 2026-11-05 | `/save` Kimi raccordé à la mémoire PKA | Le rituel Dobby partagé remplace la confusion avec le transcript Kimi |
| 2026-10-22 | **Boucle mémoire autonome** | `pka-memory-review` : review LLM (deepseek-chat), auto-skill, FTS, apply. Launchd 09:15 quotidien |
| 2026-10-22 | **Gouvernance MCP** | `pka_mcp_guard` — registre versionné + scan tool poisoning (OWASP ASI01) |
| 2026-10-22 | **Banc mémoire** | LoCoMo-like : hit@5 66,7 %, MRR 0,556, 306 tokens/requête |
| 2026-10-22 | **Retriever corrigé** | tokenisation (phrases entières ne matchaient jamais), classement par score, source State ajoutée |
| 2026-07-03 | Création skill `pka-thread-file` | Analyse Threads Memory System (Ev Chapman) — gap identifié : pas de living thread files par projet |
| 2026-07-03 | Template thread-file deployé | Standard unique pour tous les projets PKA |
| 2026-06-19 | Split SOUL/USER/MEMORY | Pattern Hermes — séparation personnalité / profil / connaissances |
| 2026-06-19 | Memory Nudge synchrone | Mode batch inefficace → passage en synchrone post-réponse |

---

## TTD — Pending

- [ ] **P2 · — · (Dobby)** Maintenance continue — `pka-thread-file` + boucle mémoire à chaque fin de session
- [ ] **P1 · — · (Dobby)** Ajouter un mode observation/dry-run aux watch loops (inspiré SuperAgent : évaluer le signal, enregistrer ce qu'il ferait, sans agir)
- [ ] **P2 · — · (JC + Dobby)** Essayer le TUI/double-clic Grok ; le rituel `/save` Kimi est terminé et ne fait plus partie de cet essai
- [ ] **P2 · — · (JC + Dobby)** ACL Tailscale — durcir l'accès réseau (reporté 13/11) : (1) poser la politique ACL (filet `autogroup:admin`→`*:*` ; `autogroup:member`↔`autogroup:member` ; `autogroup:member`→`tag:van:8123/1883/22222`) ; (2) taguer `lupo` en `tag:van`. Procédure prête (cf. `tailscale status` + `credentials-central.md`).
- [x] **P2 · — · (Dobby)** Mot de passe VNC dédié appliqué sur M5 + M1 (13/11) — plus l'admin ; raccourcis + onglets à jour
- [x] **P1 · — · (JC)** FDA accordée à `sshd-keygen-wrapper` (13/11) → raccourcis Bureau `M5-ecran-novnc.webloc` + `M1-ecran-novnc.webloc` créés. **Reste** : Accessibilité (épinglage UI encore bloqué — System Events pend en SSH).
- [ ] **P1 · — · (JC)** Réserver l'IP de l'EPSON ET-8550 en DHCP (actuellement .75, instable .65→.71→.75) pour stabiliser la file d'impression réseau
- [ ] **P1 · attente Orban · (JC + Dobby)** Consentement Graph arteon.be (app 31f92869) + autorisation forward Gmail → re-cocher la règle forward Outlook + tester ; forwarder Yahoo vers Gmail

## TTD — Done (session 2026-11-06)

- [x] 2026-11-06 · MCP Home Assistant Lupo read-only configuré et vérifié dans Kimi et DeepSeek ; relais persistant loopback actif, aucune exposition Internet ; limites Claude/Codex/ChatGPT consignées
- [x] 2026-11-05 · Noyau Dobby/Grok validé : mémoire, MCP, délégation et graphify
- [x] 2026-11-05 · Skill Kimi `/save` créé, chargé en dry-run et revu indépendamment
- [x] 2026-11-05 · Invocation utilisateur `/save` et sauvegarde non interactive validées avec `kimi-code` ; Daily note, log, threads, TTD, Honcho et vérifications intégrés au rituel

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-11-23 | Flux mail OAuth nettoyés (archivés) + consentement Graph arteon.be préparé (lecture seule, app 31f92869) ; 3 modèles Ollama cœur restaurés sur M1 | `_local/archives/mail-oauth-dead-2026-11-23/`, `JCH_Inbox/06_ADMIN/reponse-orban45-2026-11-23.md` |
| 2026-11-23 | Hammerspoon installé (bascule curseur entre 3 écrans M5, ⌃⌥⌘←/→) ; file CUPS EPSON corrigée (.75) ; `bin/pka-print` fixé (IP + outputorder=normal) | `~/.hammerspoon/init.lua`, `bin/pka-print` |
| 2026-11-20 | Clipper iPad → inbox : vault iCloud « PKA Capture » + pull one-way (bin/pka-clip-pull, launchd 15 min) ; miroir lecture seule iPad→M5 | `bin/pka-clip-pull`, `bin/install-clip-pull-launchd.sh`, `_local/launchd-plists/com.dobby.pka-clip-pull.plist` |
| 2026-11-17 | TeamViewer M5 réparé : 4 LaunchDaemons désactivés (`.plist.disabled`) → renommage manuel + `launchctl bootstrap` Helper/service ; app stable, plus de crash | — |
| 2026-11-11 | Pont noVNC iMac↔M5 (miroir d'écran) : iMac 2017 affiche le M5 via Safari, auto-start launchd, correctif noVNC (type ARD retiré) | `_local/novnc/`, `_local/launchd-plists/com.dobby.m5-vnc-novnc.plist`, `wiki/Daily/2026/11/2026-11-11-imac-miroir-de-m5-via-novnc-pont-websocket.md` |
| 2026-11-07 | Veille DeepSeek V4 + intégration transcript TV privacy + inventaire magazine Photo : recherche native, sous-agents flash, skill analyse-transcript, matrice-modeles à jour | `bin/pka-search`, `skills/analyse-transcript/`, `wiki/Daily/2026/11/2026-11-07-veille-deepseek-v4-et-evolution-du-systeme-pka.md` |
| 2026-11-06 | Intégration des trois transcripts YouTube : MCP HA multi-clients, supervision et Time Machine côté IOT, test Lightroom et socle JCH côté PHOTO_AI_JURY | `scripts/ha_mcp_loopback_proxy.py`, `scripts/mcp_ha_lupo_readonly.sh`, `wiki/Daily/2026/11/2026-11-06-mcp-home-assistant-et-lightroom-testes.md` |
| 2026-11-05 | Invocation utilisateur `/save` exécutée avec succès dans Kimi ; TUI Grok toujours à tester séparément | `wiki/Daily/2026/11/2026-11-05-stabilisation-zigbee-rpi-et-revue-multiprojet.md` |
| 2026-11-05 | Prototype Grok validé et skill Kimi `/save` ; limites TUI et intégrations externes documentées | `bin/lancer-grok.command`, `.agents/skills/save/SKILL.md`, `wiki/Daily/2026/11/2026-11-05-validation-dobby-grok-et-save-kimi.md` |
| 2026-10-22 | Loop mémoire autonome + gouvernance MCP + tracing + banc + export portable ; retriever corrigé | `bin/pka-memory-review`, `scripts/pka_mcp_guard.py`, `pka_llm_trace.py`, `pka_memory_eval.py`, `pka_memory_export.py` |
| 2026-10-22 | Re-vérification des 8 projets (correction de 5 notes) | `2026-10-22_dobby_reverification-projets.md` |
| 2026-07-03 | Analyse Threads Memory System → skill pka-thread-file créé, template deployé, skill enregistré dans outils-index.md | `TEAM_Inbox/2026-07-03_dobby_analyse-threads-memory-system.md` |
| 2026-07-01 | Hub OpenRouter restructuré | — |
| 2026-06-19 | Split SOUL/USER/MEMORY, P0-P2 terminés | — |

---

## Liens

- INDEX : `03_PROJECTS/01_AI_IT_TOOLS/INDEX.md`
- Skills : `skills/` (30+ skills)
- Outils index : `docs/system/outils-index.md`
- Memory bootstrap : `docs/system/dobby-memory-bootstrap.md`

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`. Ne pas éditer manuellement.*