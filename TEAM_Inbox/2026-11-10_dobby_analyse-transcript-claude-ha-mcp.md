# Transcript — Connecter Claude à Home Assistant avec MCP (le tuto complet 2026)

> Analyse Dobby 🦉 — 2026-11-10 — skill `/analyse-transcript`
> Source : `NoteGPT_Transcript_Connecter Claude à Home Assistant avec MCP  le tuto complet 2026.txt`

---

## 1. Comprendre

**Nature** : tutoriel vidéo (~10 min 48 s), langue anglaise, format NoteGPT. Auteur = youtubeur domotique non nommé dans le transcript (chaîne non identifiée). Positionnement : vulgarisateur Home Assistant.

**Thèse** : Depuis une mise à jour récente, Home Assistant expose nativement un serveur MCP (Model Context Protocol). Ce MCP natif permet à une IA (Claude, ChatGPT, IA locale) de contrôler les devices et lire les états, mais **pas** de créer/modifier des dashboards ou des automatisations. Pour aller plus loin, l'auteur installe l'intégration custom **HA-MCP** via HACS, puis connecte Claude avec un contrôle fin des permissions par outil.

**Points clés** :
1. **MCP natif HA** : Settings → System → AI → activer MCP → liens de connexion générés directement. Périmètre limité : contrôle des devices + lecture des états uniquement.
2. **HA-MCP** (intégration custom, ajoutée via HACS → custom repository) : débloque la création/modification de dashboards et d'automatisations.
3. **Connexion Claude** : Customization → Connector → « Add custom connector » nommé « Home Assistant » + coller l'URL générée. L'authentification spéciale exige les identifiants d'un compte admin HA.
4. **Permissions par outil** : read-only tools (toujours autorisés), write tools (calendars, automations) — réglables en *approbation systématique* / *toujours autorisé* / *bloqué*.
5. **Accès distant** : pour qu'une IA externe contrôle HA, il faut du HTTPS (Tailscale, tunnel Cloudflare, reverse proxy). En local, pas besoin d'adresse exposée.
6. **Exemples concrets** : rapport d'état (2 lumières allumées, températures par pièce, humidité, moyenne T°, T° extérieure), création d'un dashboard mobile portrait en 1–2 min, proposition d'automatisations sur la base de ses 38 automatisations existantes.
7. **Idées d'automatisations proposées par l'IA** : chauffage calé sur le jour Tempo, préchauffage avant un jour rouge, notification fin de machine à laver (prise connectée), notification fin d'impression, alerte CO, vérification verrou connecté, résumé hebdo d'état des batteries.

---

## 2. Confirmer

- ✅ **Établi** : MCP est un protocole ouvert (porté par Anthropic) ; Home Assistant a bien intégré un serveur MCP natif dans ses versions récentes ; **HA-MCP** est une intégration HACS réelle (custom component open-source) ; le principe des « connectors » Claude est réel.
- ⚠️ **Affirmé par l'auteur** : la qualité et la rapidité des dashboards générés (1–2 min), le « presque illimité » des possibilités, et le périmètre exact « lecture/contrôle seulement » du MCP natif (dépend de la version HA, non précisée).
- ❓ **Non prouvé / incertain** : auteur et chaîne non identifiés, numéro de version HA absent, aucun lien/étude cité, nom exact de la repository HACS non affiché dans le transcript.

---

## 3. Conseiller

**Routing** : `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/99_REFERENCES/claude-ha-mcp_2026-11-10/` (mapping ingest : `homeassistant` → 11_IOT).

**Impact croisé PKA** :
- 🔴 **11_IOT / Vanlife** — HA Lupo est le P0. JC a déjà validé le MCP HA **read-only** (Kimi/DeepSeek). Ce tuto documente la marche à suivre pour passer au *write* (dashboards, automatisations) avec permissions maîtrisées.
- 🟡 **01_AI_IT_TOOLS** — connecteurs Claude, gestion fine des permissions par outil, MCP.
- ⚪ **04_PILOTAGE** — renforce la règle de sécurité déjà en vigueur : « ne pas exposer HA publiquement ».

**Actions proposées** :
- **P0 — Sécurité** : si le *write* MCP est activé sur HA Lupo, rester en read-only ou approbation systématique, et n'autoriser l'accès distant que via Tailscale/Cloudflare tunnel (jamais d'exposition publique).
- **P1 — Après correction de la sous-tension RPi** : tester la génération d'un dashboard mobile HA Lupo via MCP (lecture OK en read-only ; création exige le write).
- **P2 — Documentation** : référencer ce connecteur dans le thread IOT si ce n'est pas déjà fait.

---

## Synthèse

**Confirmé** : 3 établi · 2 affirmé · 2 non prouvé
**Livrable** : `TEAM_Inbox/2026-11-10_dobby_analyse-transcript-claude-ha-mcp.md`
**Routing** : `03_PROJECTS/11_IOT/iot-van/99_REFERENCES/claude-ha-mcp_2026-11-10/`
