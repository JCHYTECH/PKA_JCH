# MEMORY — PKA_JCH
> Connaissances accumulées, décisions, chronologie des événements.
> Dernière mise à jour : 2026-10-22 — boucle mémoire autonome (auto-review LLM)

- [2026-10-22] [Veille — Outils] : Kiro (Renaud Dékode) évalué — front-end navigateur multi-modèles (API + local Ollama/LM Studio), non intégré (pas d'agent, silo IndexedDB, pas de pont vers team.db/MEMORY.md).

- [2026-10-21] [VETALYX — Mail Chine] : Configuration du gatekeeper Gmail pour les partenaires chinois — forward manuel vers Dobby en place, whitelist à étendre pour l'automatisation (adresse chinoise manquante).

- [2026-10-20] [GIT — Purge historique] : 88 Go → 617 Mo via `filter-repo --strip-blobs-bigger-than 10M`. Backup `.git.bak`, push force nécessaire.

- [2026-10-20] [VETALYX — Email] : Configuration du gatekeeper Gmail pour les partenaires chinois, whitelist mise à jour.

- [2026-10-19] [VOICE — Dictée fluide] : Boucle vocale opérationnelle (transcription + TTS) via `voice_dobby.py`. Solution testée et livrée.

- [2026-10-19] [TECH — Rétroviseur Tourneo] : Ford Tourneo Custom 2026 — procédure démontage rétroviseur intérieur (embase métal collée, clip 45°, cache plastique) + doc officielle V710 partagée.

- [2026-10-13] [IOT — Bluetti] : Bluetti Elite 100V2 — docs techniques et devis Be Camper prêts pour l'installation van Lupo.

- [2026-10-13] [Réflexion — Vivant] : Suite de la réflexion sur la définition du vivant (08/10) : raffinement quantique (Schrödinger, Löwdin, Bell/Aspect), affinement de la sélection (dérive, niveaux, MEPP, evo-devo), mutagénèse stress-induite (Luria-Delbrück, Radman, Cairns), Anthropocène comme accélérateur de sélection/mutation. Consolidé : `05_CONTEXT_JCH/Reflexion-vivant-quantique-selection-anthropocene.md` + texte grand public `Reflexion-vivant-texte-grand-public.md` + esquisse manifeste sonore `Reflexion-vivant-manifeste-sonore.md`. Manifeste photo WildLens : `02_ARTEON/wildlens/manifeste.md`.

- [2026-10-13] [IOT — Lupo Dashcam] : Intégration du montage dashcam Wolfbox G900 TriPro Bumper (3 canaux, caméra calandre incluse) dans le message de devis Be Camper (`message-devis-becamper.md` rév. 3, backup `_backup_2026-10-13.md`). **Tout reçu 13/10 : dashcam + kit hardwire + OEM bracket + rallonge 10/15 m** (bracket à faire fixer par Be Camper). MicroSD reportée (achat plus tard). Reste : montage (deadline 01/11).

- [2026-10-06] [IOT — Lupo Caméras] : Plan caméras parking + dashcam validé par JC. Contraintes : radars avant trop prudents → caméra de grille avant (IP69) ; caméra de recul d'usine masquée par le porte-vélo → caméra arrière montée HAUT sur hayon ; rétro intérieur obstrué par le mobilier → rétroviseur numérique. Choix final : **Wolfbox G900 TriPro Bumper** (miroir 12" 3 canaux : avant 4K IMX678 + arrière 2.5K étanche + pare-chocs avant 1080P) — remplace G840S + caméra de grille séparée. VIOFO A229 Pro(-W) écartée : meilleure dashcam mais pas d'aide au recul ni vue permanente. ⚠️ Prendre la version « Stoßfänger » (pare-chocs), pas « Kabinen ». Reolink MagiCam conservée en sécurité/bivouac. Livrable : 07_TRAVELS/van technique/securite/cameras-parking-dashcam-lupo.md. **Acheté 06/10** (G900 TriPro Bumper pack étendu, 378 €). Reste : montage (deadline 01/11).

- [2026-10-04] [Système — Améliorations agentiques] : Analyse de l'usage JCH sur 5 mois → 4 étapes implémentées. (1) host-watch : `scripts/pka_host_watch.py` + launchd quotidien 08:15 (disque, Time Machine, CPU) — attrape Time Machine cassé 4,5 mois. (2) snapshot + dérive : `scripts/pka_state_snapshot.py` (--check/--write/--actions) → `etat-snapshot.md` page consolidée ; fraîcheur + références obsolètes + contradictions. (3) moteur top-3 actions + watch-list intégrés au snapshot. (4) consolidation : `bin/pka` CLI unifié (save/snapshot/actions/check/host/drift/watch/memory) + règle « spécialistes à la demande » dans SOUL.md. Dérives corrigées : INDEX.md + PREFERENCES.md → Westfalia Kelsey, etat-projets.md → RPi boot résolu.

- [2026-10-04] [IOT — Bluetti] : Prix via API Shopify EU : Elite 100 V2 499€ + Charger 2 399€. Alerte `scripts/bluetti_price_watch.py` + launchd 08:00. Procédure `07_TRAVELS/van technique/ELECTRICITE/installation-bluetti-elite100v2-charger2-lupo.md`. Installateur : Be Camper (Baelen/Eupen), message devis `message-devis-becamper.md`.

- [2026-10-04] [Système — Time Machine] : Backup cassé 4,5 mois (dernière 14/05, HDD 92% plein, backupd bloqué). Nettoyage : ~107 Go supprimés (caches + modèles LLM .ollama/.lmstudio), 120 Go exclus du backup (8 chemins). Reste à faire par JC : `sudo tmutil stopbackup` + reboot.

- [2026-10-04] [HA — Guide] : Rapport `11_IOT/iot-van/2026-10-04_rapport-guide-HA-vanlife-gemini.md` + 3 documents Gemini déplacés vers `11_IOT/guide installation HA/`.

- [2026-08-31] [IOT — Lupo] : Van Lupo arrivé le 30/07/2026. Deadline installation IOT reportée du 31/08 au 01/11/2026. Pointers réalignés (30→31 spécialistes, +Scarabée #34). Suivi #4 PV PI clôturé (reçu 01/07).

- [2026-08-31] [DÉCOUVERTES — Batch 115] : 115 screenshots SITES traités. Analyzer débloqué (OCR pytesseract → tesseract CLI `eng` ; geocode Nominatim désambiguïsé : nom+région+pays d'abord). Résultat : 139 fiches lieux individuels + 7 circuits → `circuits/`. 36 fiches « à_enrichir » (split des listes via `split_circuits.py`). 1 doublon retiré (La Scarzuola = Scarzuola). 115 originaux archivés `07_ARCHIVES/sites-2026-08-31/`. À revoir : IMG_4436/4482/4484 (mis-identifications LLM), IMG_0793 (skipped). Nouveaux scripts : `triage_ocr.py`, `split_circuits.py`.

- [2026-08-30] [DÉCOUVERTES — Pipeline] : Pipeline finalisé/validé. Analyzer OCR (tesseract fra/eng/ita/deu) + EXIF + LLM. Sortie data-driven : JSON par lieu (`data/<slug>.json`) + template unique `place.html` (remplace les reports HTML lourds — `generate_html_report` supprimé, 176 lignes). 22 fiches validées → `validated_places/` (12 du jour + 10 backlog juin), `drafts/` vide, toutes `status: validated`. Nettoyage `.html.md` → `.html` (4 fichiers).

- [2026-08-30] [DÉCOUVERTES — park4night] : Module `scripts/decouvertes-collector/park4night.py`. API interne non documentée de park4night.com (`/api/places/around`, réponse base64, filtre `type`) + minage commentaires HTML (signal vue/calme/bruit multilingue) + scoring amorti (bonus = densité × min(n/5,1)). Décision : usage just-in-time (au moment de la planification), cache TTL 24h, jamais de pré-fetch. Correction clé `ANTHROPIC_API_KEY` de `JCH_PRIVATE/decouvertes.env` (périmée) → recopiée depuis `~/.config/pka-jch/api_keys`.

- [2026-08-30] [DÉCOUVERTES — Dashboard] : 3 endpoints ajoutés à `dashboard_server.py` (`/api/decouvertes`, `/api/place?name=`, `/api/sleep?lat=&lng=`) + pages `decouvertes.html` (liste groupée par pays, bouton « Où dormir ? ») et `place.html` (fiche + carte Leaflet) + lien hub. Skill `pka-decouvertes` créé (MODE A inbox SITES / MODE B Telegram) — déclencheurs « decouvertes inbox », « decouvertes telegram ».

- [2026-08-18] [VETALYX — Contrat-cadre v3 + Checklist DIAHO] : Fusion socle Renard v2 (bilingue, droit belge) + ajouts ABO → **v3 consolidée** (`FF-Contrat-Cadre_VETALYX_DIAHO_Renard_2026-08-18_v3-mission-preparation-strategique.md`, 20 articles). Ajouts : mission de préparation stratégique d'implantation Europe (100 K€ + 20 K€ validations cliniques/sérothèque), DIAHO **actionnaire fondateur 40 % dès la constitution** (apport PI Art 5:7 CSA), Article 16 conflit d'intérêts (CSA 5:76 / CIR 185/2). 10 annexes en placeholders « à finaliser » (pas de génération détaillée). Quality Agreement rédigé → déplacé `_drafts/`. **Checklist DIAHO** 22 éléments (2 tableaux FR/ZH) pour l'entrée au capital, revue ZH « Jade à confirmer » (`2026-08-18_dobby_checklist-documents-diaho-entree-capital-FR-ZH.md`). ⚠️ Découverte : le contrat ABO (Alain BOSSELOIR) repart du draft français du 03/05 — régression vs Renard v2 (perte ZH + droit français rapiécé en « belge/Bruxelles ???? »). Reste : pacte d'actionnaires, qualification AFMPS/FAMHP, ZH intégrale v3.

- [2026-08-17] [Investigation — Trafic de gibier] : Rapport `rapport_trafic_gibier.md` approfondi (OSINT). Correction majeure : procès « discrimination » transport maritime = **P&O Ferries** (relaxe 20/12/2018, Boulogne-sur-Mer), pas Brittany Ferries. Plaignantes : **Gibovendée + Envol de Retz** (condamnées 5 000 € + 10 000 €). Noms vérifiables rares : époux **Souriau** (cochongliers, Nyons 1999) ; affaire **Hoogstraten/Anvers** (GVA 17/09/24 ; « 8 prévenus » à confirmer, noms non publiés, jugement non publié JUPORTAL ; cas connexe Vertrijk condamné HLN 07/08/25) ; AFSCA « Cellule 3 » (aucun nom). NON VÉRIFIÉ : Serraille, venaison Isère, fauconnerie 90 k€/830 k€, Deux-Sèvres 100 k oiseaux, « 9 t/sem ». Livrable : `TEAM_Inbox/2026-08-17_dobby_analyse-trafic-gibier.md`. Source : `03_PROJECTS/03_WILDNEXUS/99_REFERENCES/rapport_trafic_gibier_2026-08-17/`.

- [2026-08-07] [IOT — Lupo] : Arrivée Lupo reportée au 31 août 2026. Délai supplémentaire de 24 jours pour finaliser l'installation IOT Van. WiCAN Pro reçu (01/08), hardware quasi complet. Reste : coating, silentblocs, PV PI HAT, commande capteurs Zigbee, préparation install.

- [2026-07-24] [IOT — Bridge MQTT assiette] : Bridge rechargé (launchd) + bug batterie corrigé : Sensor Logger envoie `batteryLevel` (0-1), pas `level`. Mapping + extracteur mis à jour (×100 → %). Dashboard Van Lupo : compass-card v3.5.0 intégré, widgets glance avec icônes, direction supprimée (redondante).

- [2026-07-24] [AI_IT_TOOLS — Compass-card] : Compass-card v3.5.0 (tomvanswam) installé via HACS et intégré au dashboard Van Lupo. Remplace la jauge « Cap ». Config : `indicator_sensors → sensor.lupo_test_m5_van_cap`, `arrow_inward`, labels N/E/S/O, `language: fr`. 

- [2026-07-24] [AI_IT_TOOLS — HACS] : HACS 2026.7.2 installé sur HA M5 (Docker). Redémarrage OK. Activation GitHub à finaliser côté JC dans l'UI (Paramètres → Intégrations → HACS).

- [2026-07-24] [Vetalyx — Courrier Dr Wu] : Courrier stratégique FR d'Alain, JC, Jacques, Peiwen au Dr Wu traduit en chinois par Jade 🦩. Contenu : création Vetalyx, priorité IgE totales LFIA chien/chat, budget validation clinique 20 000 €, proposition visioconférence. Traduction bilingue sauvegardée dans `TEAM_Inbox/2026-07-24_jade_traduction-courrier-dr-wu-FR-CN.md`. Source `.docx` déplacée dans `08_VETALYX/Dixun Juillet/`. ⚠️ Noms d'entités chinoises (浙大迪迅, 迪亚霍) et noms de collaborateurs (李燕, 刘毅, 钟伟伟) à faire vérifier par JC auprès du Dr Wu avant envoi.
> 
> **SOUL.md** → personnalité et règles de comportement de Dobby
> **USER.md** → profil de JCH, setup technique, projets actifs
> **MEMORY.md** → ce fichier — connaissances, décisions, historique

---

## Session 2026-07-23 — Maintenance PKA + INBOX Lupo + Test assiette iPhone

- [2026-07-23] [Système — Maintenance] : PKA system check passé GREEN. 27 permissions corrigées (0644→0600), backup team.db frais, pointers régénérés (32 membres dans stubs), todo drift résolu. Zigbee log perms fix via launchd plist `com.dobby.zigbee-log-perms` (toutes les 30 min). `generate_tool_pointers.py` inclut désormais le roster count dans les stubs.

- [2026-07-23] [IOT — INBOX] : 7 fichiers traités : 5 docs légaux Lupo → `JCH_PRIVATE/`, 2 photos van → `07_TRAVELS/van technique/`. Faux positifs `pka_prompt_guard.py` sur binaires PDF/JPEG — à corriger.

- [2026-07-23] [IOT — Hardware] : Bidirectional Level Shifter 8CH ×2 reçu (STATION-DOMO/IoT). Boîtier X1201-C1 confirmé monté (correction thread). MPU6050 supprimé de la BOM — l'iPhone gère l'assiette. Panier Amazon v8 : 12 articles / ~179€.

- [2026-07-23] [IOT — Assiette] : Test iPhone→MQTT→HA réussi sur M5. Sensor Logger publie sur `esneux/iphone`, le pont `pka_mqtt_discovery_bridge.py` relaye vers HA. Corrections appliquées : (1) mot de passe Mosquitto = `Dobby2026!` (D majuscule, pas `dobby2026!`), (2) bridge forcé MQTTv5 + PYTHONUNBUFFERED, (3) extracteur `sensor_logger` ajouté au bridge pour parser le JSON nested de Sensor Logger (radians→degrés). Convention topics : `<lieu>/<source>` = `esneux/iphone` (maison) vs `lupo/assiette` (van).

- [2026-07-18] [AI_IT_TOOLS — Automatisation] : 3 améliorations d'automaticité : (1) `pka-watch-inbox` → notification macOS à chaque nouveau fichier, (2) `pka-watch-freshness` → alerte quotidienne 8h30 si State files CRITICAL, (3) `pka-memory-hook` → extraction post-session des décisions/règles/patterns depuis TEAM_Inbox. 8 daemons launchd actifs au total.

- [2026-07-18] [AI_IT_TOOLS — Veille] : 2 transcripts NoteGPT traités : (1) Constrained decoding / structured output (logit masking, GBNF grammars, OpenAI/Anthropic) — déjà implémenté dans DeepSeek V4. (2) Memori — moteur mémoire open-source SQL-native pour agents LLM — PKA a déjà team.db + MEMORY.md + pka_memory_capture.py, plus sophistiqué. Références dans `01_AI_IT_TOOLS/99_REFERENCES/`.

## Session 2026-07-18 — Clonage SD Lupo + Règle hardware

- [2026-07-18] [IOT — Hardware] : Clonage SD 128 Go → Endurance 256 Go terminé avec succès. SD→SSD→SD en deux étapes (107 Mo/s en lecture, ~5 min en écriture). RPi boote sur Endurance 256 Go, HA OS accessible via IP directe (pont Ethernet M5). Règle réseau ajoutée : .local ne traverse pas le bridge macOS, toujours utiliser l'IP directe. Carte prête pour Lupo. Échec initial : `dd` direct SD→SD sur même hub USB → 1,3 Mo/s, 58 Go en 12h. Solution : SD source → SSD M5 (107 Mo/s via slot interne) → Endurance 256. **Règle : ne jamais cloner SD→SD sur même bus USB. Toujours passer par le SSD interne en intermédiaire.**

## Session 2026-07-17 — Hardware Lupo : SD Endurance + Argus MagiCam reçus

- [2026-07-17] [IOT — Hardware] : Samsung PRO Endurance 256GB microSD ✅ REÇU (Amazon). Remplace SD 128 Go actuelle. Reolink Argus MagiCam ✅ REÇU. Tout le hardware STATION-DOMO/IoT est maintenant livré (sauf WiCAN Pro en backorder).
- [2026-07-17] [IOT — Décision] : **NVMe Fanxiang retiré physiquement du RPi. Décision confirmée : SD seule, pas de SSD.** L'adaptateur USB-NVMe n'est plus nécessaire. Le RPi Lupo fonctionne en microSD boot uniquement.
- [2026-07-17] [IOT — Thread] : Thread-iot.md mis à jour — NVMe marqué ⚫ retiré, prochaine étape = swap SD 128→Endurance 256.

- [2026-07-17] [IOT — Sécurité] : Fiche sécurisation physique/réseau WiCAN PRO (ChatGPT) traitée depuis INBOX. 4 méthodes physiques + volet réseau. Référencée dans `11_IOT/iot-van/securite/obd/`. Complément à `OPERATIONS-CAN-OBD.md`.

- [2026-07-17] [AI_IT_TOOLS — Build] : P2 Loop Engineering terminés : `bin/pka-chain` (orchestrateur cross-loop, fichier .chain, --dry-run, --continue-on-error, quick-check.chain exemple), `bin/pka-persist` (persistence post-session, --once nohup + --schedule launchd, tasks.json). Toute la stack Loop Engineering PKA est complète (7/7 actions, P0+P1+P2).

- [2026-07-17] [AI_IT_TOOLS — Build] : P1 Loop Engineering terminés : `bin/pka-dashboard` (HTML statique, 6 loops, dark mode), `bin/pka-watch-deadline` (parse dates FR, J-X, alertes markdown, plist launchd 9h), skill `compound-memoire` (erreur→règle SOUL.md, workflow 3 étapes, seuils de confiance). Dashboard + deadline testés avec succès.

- [2026-07-17] [AI_IT_TOOLS — Build] : Forge a implémenté les 2 P0 Loop Engineering : `bin/pka-loop` (commande /loop unifiée, 6 loops, syntaxe courte + anatomie Cherny 6 params) et `bin/pka-watch-inbox` (surveillance INBOX, logs JSON, alertes markdown, plist launchd). Testés —help, --dry-run, --once, --daemon. Rapport : `TEAM_Inbox/2026-07-17_forge_p0-loop-engineering.md`.

## Session 2026-07-17 (soir) — INBOX : Analyse Loop Engineering

- [2026-07-17] [AI_IT_TOOLS — Veille] : Analyse approfondie Loop Engineering — sources primaires Cherny (Anthropic), Osmani (Google), Steinberger (OpenAI). Corpus : cocodedk/loop-engineering (11 docs), addyosmani.com. PKA a ~2 ans d'avance sur le concept. Découvertes clés : (1) compound Cherny = erreur→CLAUDE.md automatique, (2) watch-for-work > wait-for-command, (3) anatomie 6 parties (trigger→scope→action→budget→stop→report). 7 actions dont 2 P0 : commande /loop unifiée, watch-for-INBOX. Livrables : analyse initiale + complétive dans `TEAM_Inbox/`.

## Session 2026-07-16 (soir) — CAN/OBD + Capteurs + Scarabée

- [2026-07-16] [IOT — CAN/OBD] : WiCAN Pro commandé en backorder chez Mouser (~82€). OBDLink LX101 reçu mais incompatible (Bluetooth, HS-CAN seul, pas de MS-CAN). Procédure complète créée : `OPERATIONS-CAN-OBD.md` (6 étapes, flash firmware, config WiFi/MQTT, preset PIDs Ford, power management, validation).
- [2026-07-16] [IOT — Réseau] : AP WiFi `VanLife_Network` configuré sur Lupo RPi (à activer via UI HA, pas CLI — échec `ha network update --wifi-mode ap`). Dongle 4G ZTE MF833U1 (✅ REÇU) documenté. Architecture finale : RPi 5 = hub unique (AP WiFi + passerelle 4G). Mot de passe stocké dans `JCH_PRIVATE/credentials-central.md`.
- [2026-07-16] [IOT — Capteurs] : Panier Amazon vanlife réduit à 172€ (vs 282€). SNZB-02D ×3 supprimés → remplacés par BME688 + SHT31 du stock WildNexus (Mouser #39492997). Fiche technique `SPEC-CAPTEUR-ENV.md` créée : ESP32-C3 + BME688 + SHT31 = T°/HR/Pression/IAQ pour 0€. Firmware ESPHome inclus.
- [2026-07-16] [IOT — Panier] : Fichier `panier-vanlife-amazon.html` v6 — 11 articles, 172€, 4 niveaux de priorité avec liens Amazon Belgique.
- [2026-07-16] [Système — Équipe] : Recrutement Scarabée 🪲 (#34) — Concepteur 3D & Fabrication Additive. Première mission : boîtier station météo Lupo. Pipeline onboarding exécuté (DB → markdown → roster → pointers). Équipe : 32 membres (31 spécialistes + Dobby).
- [2026-07-16] [IOT — Hardware] : ZTE MF833U1 ajouté au `hardware-state.md` (✅ REÇU). WiCAN Pro marqué COMMANDÉ (backorder).

## Session 2026-07-16 — Incorporation architecture + migration ZHA→Z2M

- [2026-07-16] [Système — Gouvernance] : 3 documents créés depuis `Prompt_Dobby_PKA_JCH_Master_Architecture.md` : `principes-architecturaux.md` (6 principes), `securite-sauvegardes.md` (confidentialité 🔴🟡🟢 + backup), `roadmap-long-terme.md` (vision 1/3/5 ans). Référencés dans AGENTS.md, outils-index.md, sources-verite.md. Source archivée dans `01_AI_IT_TOOLS/99_REFERENCES/`.
- [2026-07-16] [WILDNEXUS — Stratégie] : Analyse Dossier de Conception v1 (JC, 16/07). Proposition d'élargissement : biodiversité → santé écosystémique (orages AS3935, incendie BME688, cavitation, VOC). Recommandation Scénario B : P0 enrichi BME688 + AS3935 + PM2.5 (~35€/station, délai +2 sem). Cavitation → P1 recherche. Livrable : `TEAM_Inbox/2026-07-16_dobby_analyse-wildnexus-dossier-conception.md`.
- [2026-07-16] [Système — Veille] : Analyse transcript Ev Chapman « Threads Memory System » (avril 2026). Système à 2 dossiers (threads + daily logs) + script nocturne + second brain. PKA couvre déjà tous les cas d'usage avec plus de profondeur (team.db, graphify, 30 agents). Validation externe de l'approche PKA. Livrable : `TEAM_Inbox/2026-07-16_dobby_analyse-threads-memory-system.md`.
- [2026-07-16] [IoT Van — Lupo RPi] : Migration ZHA → Zigbee2MQTT terminée. ZHA désinstallé, Z2M v2.12.1 installé et opérationnel. Dongle Sonoff ZBDongle-E V2 reconnu (firmware EmberZNet 8.0.2, adapter `ember`). Mosquitto OK, MQTT connecté (user `homeassistant` + `addons`). Réseau Zigbee vierge — prêt à appairer. Contournement : pont TCP série homeassistant:8486 (superviseur refusait de monter le device). Stickers Lupo déplacés vers `07_TRAVELS/vanlife/deco/`.

## Session 2026-07-15 — Nettoyage structure PKA_JCH

- [2026-07-15] [Système — Nettoyage] : Fichiers pilotage stratégique réalignés (WILDNEXUS gelé septembre, IOT Van P0 7 août). 14 session JSONs → `_local/sessions/`, MEMORY.md.bak ×2 → `_local/archives/`, 23 .DS_Store supprimés. `tests/`, `deploy/`, symlink `Wadden_Vanlife.html` supprimés.
- [2026-07-15] [IoT — Wishlist] : Monitoring batterie X1205 dans HA — pas d'intégration native pour X120x (RPi 5). Piste : script Python I2C → MQTT via Terminal & SSH add-on. Repo `lovwyr/HA-Geekworm_X120x` ne couvre que X1204. Forum HA confirme « nothing yet ».
- [2026-07-15] [IoT — Lupo RPi config] : Credentials récupérés via USB CONFIG + SSH debug port 22222. Tailscale 0.28.1 installé et authentifié. IP Tailscale : `100.106.152.118`. HA Core 2026.7.2, HA OS 17.3, hostname `lupo`. WiFi Proximus, Ethernet `end0` désactivé. Terminal & SSH add-on présent mais port 22 non exposé.
- [2026-07-15] [IoT — Nettoyage RPi] : Anciens nœuds supprimés — `rpi-pkajch` (BirdNET-Pi) et RPi 5 Esneux (HA OS serre/maison). Seul RPi 5 Lupo (van) reste actif. `rpi-connexion.md` et `USER.md` mis à jour.
- [2026-07-15] [Modèle — DINOv2-bio] : Fichier `models/vit_reg4_so150m_p14_ls_dino-v2-bio-252px.pt` (510 MB) supprimé. Contexte préservé dans `TEAM_Inbox/2026-07-03_dobby_analyse-birder-dinov2-bio.md`. À retélécharger depuis HuggingFace `birder-project/vit_reg4_so150m_p14_ls_dino-v2-bio` si besoin (septembre+).

## Session 2026-07-14 — Carrefour spots vanlife + activation Dobby

- [2026-07-14] [TRAVELS — Carrefour spots vanlife] : Page HTML créée — `vanlife/carrefour-spots-vanlife.html` (547 lignes, 19 Ko). Consolide 24 liens (apps stationnement, planification voyage, par pays FR/IT/DE/BE, bases officielles réserves naturelles, outils PKA) en 6 sections. Checklist Cigogne intégrée. Dark mode responsive. Sources : `apps-roadtrip-lupo.md` + `methodologie-stationnement.md`.
- [2026-07-14] [Système — Activation Dobby] : Session démarrée. 31 membres actifs. 10 State files >7j (dont 1 CRITICAL — registre-achats.md 15j). IOT/Vanlife = P0 deadline 7 août. Samsung PRO Endurance 256GB + Reolink Argus MagiCam commandés 13/07.

## Session 2026-07-10/11 — Stabilisation Lupo RPi 5 : SD boot + double instance HA

- [2026-07-11] [IoT — Résolution double instance] : Le RPi 5 Lupo (HA OS 17.3 sur NVMe) et le Docker M5 (HA `localhost:8123`) provoquaient `duplicate_os_installation` → Supervisor unhealthy → add-ons bloqués. **Cause :** hostname par défaut `homeassistant` sur les deux instances + anciennes partitions HA OS sur NVMe détectées comme second OS. **Solution :** (1) hostname RPi changé en `lupo` dans Settings → System → Network, (2) `ha supervisor repair` exécuté via Terminal & SSH add-on pour régénérer le Machine ID, (3) Docker M5 conservé en `homeassistant`. Résultat : ✅ Healthy, coexistence stable, plus de conflit.
- [2026-07-10] [IoT — Échec boot NVMe natif] : Après la solution du 09/07 (boot NVMe confirmé à 22h), tentatives répétées de boot NVMe seul (sans SD). **Échec intermittent** : LED verte fixe = NVMe non détecté. **Diagnostic confirmé :** (1) les pogo pins du X1205 ne fournissent pas le courant de pointe nécessaire au boot NVMe (PCIe Gen3 + contrôleur SSD) → chute de tension sous 4.65V → PMIC coupe tout. Boot direct USB-C = OK. (2) La nappe PCIe est critique : contacts métalliques doivent être orientés vers l'intérieur (face au processeur), loquet noir bien verrouillé. (3) Le RPi 5 nécessite une carte SD présente pour initialiser le bus PCIe — sans SD, le NVMe n'est jamais détecté même si la SD est vide.
- [2026-07-10] [IoT — Solution retenue : Plan C] : **HA OS 17.3 sur SD 128 Go** (boot fiable), NVMe 256 Go en attente de wipe pour usage futur (Move Data Disk). La SD seule est stable — HA Community #716038 confirme cette approche comme fiable pour RPi 5. Le bug GitHub #4785 (HA OS 18.x + NVMe instable) impose de rester en 17.3.
- [2026-07-10] [IoT — Commande adaptateur USB-NVMe] : **UGREEN 10Gbps NVMe Enclosure** (réf `B0D53K7HK9`, ~25€) commandé pour wiper le NVMe Fanxiang 256 Go depuis le M5. Une fois wipe, le NVMe pourra être reconnecté au RPi et utilisé comme data disk via la fonction Move Data Disk de HA.
- [2026-07-10] [IoT — Configuration matérielle stable] : Stack final : RPi 5 + SD 128 Go (HA OS 17.3, hostname `lupo`) + X1205 (batteries 18650 en place pour UPS, mais alim directe USB-C sur le RPi pour éviter le problème pogo pins). NVMe + Shield PCIe déconnectés en attendant l'adaptateur USB. Boîtier X1201-C1 non encore monté (restera ouvert pour accès facile).
- [2026-07-10] [IoT — Expert externe] : Validation croisée avec un expert LLM externe. Points confirmés : orientation nappe PCIe, méthode d'isolation 3 étapes (SD seule → +NVMe → +HAT), paramètres EEPROM corrects (BOOT_ORDER=0xf416, PCIE_PROBE=1, PSU_MAX_CURRENT=5000), modèles LLM recommandés pour RPi 5 (Qwen 2.5 1.5B/3B, Gemma 3 1B, DeepSeek-Coder 1.3B).
- [2026-07-10] [Système — Session marathon] : Session de ~4h, 80+ échanges, diagnostic itératif hardware + software. Dobby a navigué entre le RPi (via SSH + API observer) et le Docker M5, avec wipe SD, reflash, et coordination des actions physiques de JC.

## Session 2026-07-09 — Analyse OBD/CAN bus Ford Transit Custom + intégration WiCAN Pro

- [2026-07-09] [IoT — Analyse OBD/CAN] : Analyse approfondie de l'apport des données OBD-II/CAN bus du Ford Transit Custom 170CV 4x4 (Westfalia Kelsey « Lupo »). Le véhicule expose deux bus CAN : HS-CAN (PCM 0x7E0, groupe motopropulseur) et MS-CAN (BCM 0x726, carrosserie). Le MS-CAN est critique — il fournit état portes ×6, pression pneus ×6, batterie SOC/courant/tension sans capteur physique.
- [2026-07-09] [IoT — Décision WiCAN Pro] : **WiCAN Pro retenu** (~82€, Crowd Supply/Mouser). Seul device compatible MS-CAN + HS-CAN avec PIDs Ford Transit prêts à l'emploi (repo `WiCAN-Ford-Transit`). WiCAN basic éliminé (pas de MS-CAN). DIY ESP32+CAN éliminé (effort de reverse engineering disproportionné). 17+ entités HA exposées.
- [2026-07-09] [IoT — Sommeil CAN bus] : Recherche intensive confirmée : le CAN bus Ford s'endort après 30-60 min contact OFF. Aucun hack fiable pour le maintenir actif 24/7 sans vider la batterie porteur (200-500mA → 4-5 jours d'autonomie). Le WiCAN Pro utilise un sleep mode <1mA + periodic wake configurable (5 min recommandé). **Les Aqara Zigbee restent obligatoires** pour la détection porte en temps réel en camping. Le CAN bus est un enrichisseur de données roulage + backup sécurité, pas un tueur de capteurs.
- [2026-07-09] [IoT — BOM impact] : TPMS Bluetooth supprimé (-20€, remplacé par BCM pneus ×6). BME280 extérieur supprimé (-5€, remplacé par PCM ambient air temp). WiCAN Pro ajouté (+82€). Delta net : +57€. Cumulé avec DS300 Tap (-57€) : **total optimisations = 0€ (neutre)**. 6 nouveaux scénarios créés : jauge carburant + range anxiety (P1), conso réelle par trajet (P1), diagnostic moteur DTC live (P1), surveillance turbo (P2), préchauffage Webasto intelligent (P2), alerte batterie porteur (P2). GPS u-blox rétrogradé P2→P3 (vitesse via CAN, position seule).
- [2026-07-09] [IoT — Fichiers mis à jour] : `SPEC-CAN-BUS.md` créé, `ADR-006-obd-can-wican-pro.md` créé, `BOM-VANLIFE.md` (v5 sections → 6), `scenarios-algorithmes-vanlife.md` (v1.0→v1.1, +section 7 CAN), `hardware-state.md`, `SPEC-DS300-TAP.md` (impact CAN). Commande WiCAN Pro ajoutée en Commande #2 prioritaire.

## Session 2026-07-09 — Diagnostic échec boot NVMe + correction guide assemblage

- [2026-07-09] [IoT — Diagnostic] : JC a tenté l'assemblage et l'installation HA OS sur le RPi 5 vanlife. **Échec complet** — « enormement de difficulté, j'ai du tout arreter ». Analyse post-mortem :
  - **Cause n°1 : bootloader NVMe non configuré.** Le guide `ASSEMBLAGE-RPi5-VANLIFE.md` indiquait de flasher HA OS directement sur le SSD et de booter, mais le RPi 5 ne boote PAS sur NVMe sans configuration préalable de l'EEPROM (`BOOT_ORDER=0xf416`, `PCIE_PROBE=1`, `dtparam=pciex1` dans config.txt).
  - **Cause n°2 : pogo pins X1205.** La FAQ Geekworm confirme que des standoffs mal serrés empêchent le contact pogo pins → pastilles RPi → pas d'alimentation.
  - **Cause n°3 : pas de câble USB-C PD e-mark.** Sans négociation Power Delivery 5A, le RPi 5 est en undervoltage chronique (`throttled=0x50000`).
  - **Cause n°4 : SSD Fanxiang.** Peut nécessiter `dtparam=pciex1_gen3` pour éviter les erreurs I/O.
  - **Tentative JC :** Dupont entre pin 6 (GND) et pin 8 (GPIO14/TXD) du GPIO — probablement pour forcer l'auto-power-on, mais la doc X1205 indique que cette fonction est gérée par une résistance soudée, pas par jumper GPIO.
- [2026-07-09] [IoT — Guide] : **Section 4 du guide d'assemblage entièrement réécrite** (298→500 lignes). Nouvelle procédure en 10 sous-étapes : microSD bootstrap → EEPROM update → BOOT_ORDER + PCIE_PROBE → dtparam=pciex1 + gen3 → PSU_MAX_CURRENT → vérification NVMe → flash HA OS → boot sans microSD. Checklist de vérification enrichie (pogo pins, EXT5V_V, throttle). Roadmap réorganisée en 3 phases.
- [2026-07-09] [IoT — Clarification Tailscale] : Tailscale utile uniquement quand le RPi a accès à internet. Sans dongle 4G → utile seulement sur Wi-Fi connu (maison, camping). Avec dongle 4G → game-changer 24/7. Positionné en Phase 1 étape 2 (après bootloader + HA OS).

## Session 2026-07-09 — Solution consolidée boot NVMe (analyse croisée équipe + web)

- [2026-07-09] [IoT — Erreur image HA OS] : **Forge 🔨 a identifié la cause racine probable.** Le postmortem indique que `haos_generic-aarch64-18.1.img` a été flashé, mais le guide spécifie `haos_rpi5-64-xx.img`. L'image `generic` est pour machines UEFI ARM64 (GRUB/systemd-boot) — le BCM2712 du RPi 5 cherche `start4.elf` sur la partition FAT, absent de l'image generic. Le hand-editing de `config.txt`/`cmdline.txt` ne servait à rien car aucun bootloader RPi n'était présent. La LED verte fixe initiale était le bootloader qui scannait sans trouver `start4.elf`.
- [2026-07-09] [IoT — Facteur aggravant X1205] : **Araignée 🕷️ confirme 80% probabilité d'alim insuffisante via pogo pins.** Le boot NVMe crée un appel de courant instantané (PCIe Gen3 + contrôleur SSD) supérieur au boot microSD. Si résistance de contact pogo pins > spec, chute de tension sous 4.65V → PMIC DA9091 coupe tout. Test discriminant : `vcgencmd get_throttled` sous stress `dd` NVMe.
- [2026-07-09] [IoT — Alerte externe GitHub #4785] : Bug **ouvert** sur HA OS 18.0/18.x + RPi 5 + NVMe hat → I/O errors en ~3 min, filesystem corrompu. Utilisateur a rollbacké vers 17.3 avec succès. **Non résolu au 9 juillet 2026.** Recommandation : utiliser HA OS **17.3** (pas 18.x) pour Lupo.
- [2026-07-09] [IoT — Plan d'action] : (1) Test `vcgencmd get_throttled` sous stress NVMe (5 min). (2) Si propre → flasher `haos_rpi5-64-17.3.img` sur NVMe. (3) Si throttling → bypass X1205 (alim directe USB-C). (4) Fallback : microSD + Move datadisk (Settings → Storage). **SOLUTION-BOOT-NVME-2026-07-09.md** réécrit avec analyse consolidée Dobby+Forge+Araignée+sources web.
- [2026-07-09] [IoT — Sources externes] : HA Community #716038 confirme Move datadisk fonctionnel (« data drive copied from SD to NVMe using Settings → Storage → Move Data Disk »). Reddit r/homeassistant idem. jbsoft.nl et martinrowan.co.uk documentent la procédure complète. Guide d'assemblage §4.8 était correct — l'erreur était au moment du téléchargement/flash.

## Session 2026-07-08 — Réception accus 18650 + état des lieux

- [2026-07-08] [IoT — Hardware] : **20× accus 18650 Flat 3400mAh CCC-5 SDIR18T** (rose) reçus. Destinés au Geekworm X1205 UPS HAT du RPi 5 vanlife. `hardware-state.md` mis à jour.
- [2026-07-08] [IoT — Hardware] : **Power Supply Adapter HS24A (24V)** + **sonde hydrostatique TL-136** + **Sonoff ZBMiniR2** + **5× Step-Down HW-133 3A 5V DC-DC (Tecnoiot)** + **3× ADS1115 HW-19S** reçus. Stock total ADS1115 : 6 (3 Heemol + 3 HW-19S). Stock ESP32-C3 Super Mini : 3 (Heemol). Détecteur niveau liquide : il ne manque plus que boost converter (MT3608) et chargeur TC4056 pour le proto banc (buck HW-133 et accus 18650 déjà en stock). `hardware-state.md` mis à jour.
- [2026-07-08] [IoT — Assemblage] : RPi 5 vanlife assemblé (RPi 5 + SSD NVMe + UPS HAT X1205 + accus 18650). Reste : mise en boîtier X1201-C1. `hardware-state.md` mis à jour.
- [2026-07-08] [IoT — Optimisation] : Analyse redondance signal capteurs vanlife. **Économie réelle : -1 capteur (-10€)**. JSN-SR04T van ×2 supprimés (→ DS300 Tap lit sondes CBE). SNZB-02D extérieur supprimé (→ BME280 P3). ⚠️ Correction : le SNZB-04P est un capteur contact uniquement (pas de T°). Les Aqara frigo/toit et SNZB-02D frigo sont conservés. Le 04P reste une option upgrade (tamper alert). Panier v4 : 27 items / 257€.
- [2026-07-08] [IoT — DS300 Tap] : **Sous-projet `iot-van/ds300-tap/` créé.** Recherche web confirmée : le CBE DS300 utilise un connecteur 16 broches (J9) avec signaux analogiques simples (pas de CAN/LIN). Pinout documenté par WomoNET. Le tap ESP32 + ADS1115 permet de lire tensions B1/B2, niveaux cuves eau, D+, 230V, état relais — sans modifier le câblage d'origine. Fichiers créés : `SPEC-DS300-TAP.md`, `esphome-ds300.yaml`. Scénarios mis à jour.
- [2026-07-08] [IoT — BOM] : **BOM maître `iot-van/BOM-VANLIFE.md` créée** — structurée par sous-projet : RPi 5 Hub (445€ reçus), DS300 Tap (15€), Capteurs Zigbee (276€ à commander), Victron P3 (210€ reporté), Divers (27€). Total projet : ~973€ dont ~446€ déjà payés. Panier Amazon v4 : 33 articles / 282€. Reste à payer P1 : ~317€.
- [2026-07-08] [IoT — Réorg] : **Réorganisation complète de `11_IOT/`.** Root : 14→6 entrées. `iot-van/` : 9 fichiers racine → 3 (`BOM-VANLIFE.md`, `scenarios-algorithmes-vanlife.md`, `ASSEMBLAGE-RPi5-VANLIFE.md`). Création de `docs/`, `briefs/`, `rpi-config/`, `specs/`, `archive/`, `assets/`. Chemins corrigés partout.

## Session 2026-07-07 — Correction protocole pka-session-start

- [2026-07-07] [Vetalyx — Clarification stratégique JC] : JC confirme que la note Depinois n'est PAS un ordre de modification des priorités actuelles. Les priorités restent inchangées. L'objectif est d'augmenter la réflexion stratégique et d'identifier d'autres MVP pour le futur, car Vetalyx sera à terme une plateforme de diagnostics vétérinaires sensu largo. Les briefs et la synthèse doivent être réinterprétés comme du travail d'enrichissement stratégique, pas comme un plan de pivot immédiat.

- [2026-07-07] [Vetalyx — Note cadrage Depinois] : Email d'Alain Depinois (AWDN Partners, 2026-06-25) analysé et comparé au corpus Vetalyx. Proposition de repositionner le MVP commercial sur les tests infectieux/vectoriels (panel Lyme/Anaplasma/Ehrlichia/Dirofilaria chien) + FeLV/FIV + biomarqueurs CRP/SAA, avec l'allergie comme option plus risquée. 4 scénarios évalués. Recommandation Dobby : scénario D (intégration sélective, négocier les 3 familles avec les chinois) avec option C si l'allergie EU n'est pas viable. Livrable : `TEAM_Inbox/2026-07-07_dobby_analyse-note-cadrage-vetalyx-depinois.md`. Source routée vers `JCH_Inbox/03_PROJECTS/08_VETALYX/strategy/`. Thread `thread-vetalyx.md` mis à jour.

- [2026-07-07] [Vetalyx — Synthèse décisionnelle] : Synthèse approfondie des points d'attention et de décision produite. 14 points de décision identifiés (stratégie, produit, fournisseur, réglementaire, financier, corporate, marque, scientifique, organisation, partenariat DIAHO, IP, etc.). 7 briefs créés et insérés dans `team.db` pour Furet+Milan, Renard, Clio, Bruno+Sigma, Hermine, Vega+Milan, Atlas. Recommandation Dobby : scénario C ajusté (P0 vectoriel chien + FeLV/FIV, P1 allergie différenciante). 7 questions ouvertes pour JCH. Livrable : `TEAM_Inbox/2026-07-07_dobby_synthese-points-decision-vetalyx-depinois.md`.

- [2026-07-07] [Vetalyx — Analyse croisée 4 spécialistes] : Dobby a mandaté Vasco, Hermine, Renard et Sigma pour analyser la proposition Depinois sous 4 angles (stratégique, réglementaire, contractuel, marché). 3 erreurs factuelles identifiées dans la proposition d'Alain : AFMPS ≠ plus simple, panels ≠ non-commoditisés, Dixun/DIAHO non mentionnés. Recommandation unanime : dual-track (allergologie P0 + infectieux P1), pas pivot. 3 décisions bloquantes en attente de JC (D1-D3). Livrable : `TEAM_Inbox/2026-07-07_dobby_analyse-cadrage-depinois-vetalyx.md`.

- [2026-07-07] [Système — Bootstrap GLM 5.2] : BOOTSTRAP.md créé (83 lignes, protocole Phase 2→5 condensé). `scripts/deepseek_chat.py` modifié pour charger BOOTSTRAP.md après MEMORY.md. GLM.md créé comme pointer dédié. `bin/dobby.sh` modifié pour exporter PKA_POINTER=GLM.md en mode glm5. Tous les modèles via deepseek_chat.py (GLM 5.2, DeepSeek API, Kimi, OpenRouter, Claude-OR, ChatGPT) bénéficient désormais du bootstrap complet.

- [2026-07-07] [Background Depinois] : Vérification web — Alain Depinois, vétérinaire de formation (confirmé JC), 132 connexions LinkedIn, AWDN&Partners fondée en 2010 (Havelange), classifiée « Other business services ». Aucune trace publique de publications, conférences ou présence dans l'industrie du diagnostic vétérinaire. Expertise marché non vérifiable — JC le qualifie de « compétent en connaissance, pertinence marché à vérifier ».

- [2026-07-07] [Vetalyx — Clarification JC] : La note Depinois est un **apport à la réflexion stratégique**, pas un ordre de pivot. Les priorités actuelles (WildNexus P0, IOT Van, NEXUS_ACOUSTIC) restent inchangées. Vision long terme : Vetalyx = plateforme de diagnostic vétérinaire *sensu largo*, intégrant à terme allergologie + infectieux + biomarqueurs. L'analyse produite reste valide mais son statut passe de « décision requise » à « réflexion long terme ».

- [2026-07-07] [Système — pka-session-start] : Skill `skills/pka-session-start/SKILL.md` réécrit pour s'aligner sur `docs/system/dobby-memory-bootstrap.md` v2. 6 corrections appliquées : (1) titre passé à « 5 phases » au lieu de « 4 phases », (2) retrait de `arbitrages-decisions.md` (archivé le 2026-06-23), (3) ajout de `wiki/index.md` en phase 2, (4) ajout de `PROTOCOLES/progress.md` en phase 3 avec règle anti-déduction d'artefacts, (5) ajout de `pka_retrieve.py --fts` en phase 4 pour recherche historique cross-session, (6) détection du modèle actif formalisée. Sauvegarde `SKILL.md.bak.20260707` créée.
- [2026-07-07] [Système — instructions-systeme.md] : Tableau des instructions mis à jour — description S4 enrichie (« Protocole démarrage 5 phases : identité, contexte, State, vérifications, activation ») et date de mise à jour ajoutée. Sauvegarde `instructions-systeme.md.bak.20260707` créée.
- [2026-07-07] [Système — State freshness] : `check_state_freshness.py` exécuté — 15/16 State OK, 1 WARNING (`docs/system/registre-achats.md` — 8 jours).

## Session 2026-07-03 — Analyse INTERSPECIES SONGS + Lucio Arese → Intégration NEXUS_ACOUSTIC

- [2026-07-03] [NEXUS_ACOUSTIC — TweetyBERT] : Document INTERSPECIES SONGS.md (627 lignes) analysé en profondeur. TweetyBERT (University of Oregon, Patterns/Cell Press, avril 2026) identifié comme découverte la plus actionnable pour PKA. Transformer self-supervised, parsing de syllabes sans labels, résolution 2.7ms. Open-source (GitHub/Zenodo). Pipeline complet xcapi→librosa→TweetyBERT→t-SNE→Markov documenté. Analyse livrée : `TEAM_Inbox/2026-07-03_dobby_analyse-interspecies-songs.md`.
- [2026-07-03] [NEXUS_ACOUSTIC — InsectSet459] : Dataset 26 298 fichiers, 226.6h, 459 espèces (310 Orthoptera + 149 Cicadidae), publié dans Nature Scientific Data (2026), disponible sur Zenodo. C'est le dataset de fine-tuning idéal pour TweetyBERT sur orthoptères.
- [2026-07-03] [NEXUS_ACOUSTIC — Lucio Arese] : Document Lucio Arese inspiration.md (261 lignes) analysé. Pont entre pipeline scientifique et visualisation 3D (TouchDesigner/SoundPlot). Dimension Z=temps validée comme avantage analytique réel. SoundPlot (arXiv 2601.12752) identifié comme alternative open-source à TouchDesigner. Schéma JSON standardisé PKA proposé par Forge. Livrable : `TEAM_Inbox/2026-07-03_dobby_analyse-lucio-arese.md`.
- [2026-07-03] [NEXUS_ACOUSTIC — Architecture cible] : Edge léger (ESP32 VAD + enregistrement) → RPi 5 BirdNET-Lite (classification) → M5 TweetyBERT (parsing/clustering). Musaraigne confirme : TweetyBERT sur RPi 5 = ❌ (transformer trop lourd, 4GB OOM), sur M5 = ✅ (GPU Apple Silicon).
- [2026-07-03] [NEXUS_ACOUSTIC — Roadmap] : P0 juillet = télécharger InsectSet459 + installer TweetyBERT sur M5 + adapter preprocessing orthoptères (fmin=5000). P1 août = fine-tuning + dashboard 3D. P2 septembre = pipeline automatisé + série WildLens « Sound Portraits ».
- [2026-07-03] [NEXUS_ACOUSTIC — WildLens] : Potentiel éditorial identifié — sculptures 3D de chants d'orthoptères comme contenu visuel différenciant. Série « Sound Portraits » proposée.
- [2026-07-03] [Validation web] : 15 recherches DuckDuckGo, 22 sources croisées. Confirmations : TweetyBERT peer-reviewed, InsectSet459 public, Lucio Arese artiste-chercheur confirmé (Seeing Birdsong, Nencki Institute), SoundPlot framework open-source, DolphinGemma forkable, ESP modèle généralisable 2028.
- [2026-07-03] [Système — Prompt INBOX] : Template `prompt-inbox-analysis.md` créé dans `docs/system/`. 7 phases standardisées (Discovery → Deep Read → Multi-Angle Analysis → Web Validation → Cross-Project Impact → Integration Proposals → Memory Capture). Réutilisable pour tout futur fichier INBOX. Supprime l'improvisation et garantit une analyse complète à chaque fois.
- [2026-07-03] [NEXUS_ACOUSTIC — BIRDER] : Modèle `birder-project/vit_reg4_so150m_p14_ls_dino-v2-bio` analysé. Encodeur ViT 133.6M params (DINOv2) entraîné sur 31M photos de biodiversité. ⚠️ Modèle VISUEL (photos RGB), PAS bioacoustique. Pertinent pour (1) classification automatique photos naturalistes JC (PHOTO_NATURE, 81% iNat2021) et (2) encodeur alternatif pour spectrogrammes InsectSet459. Framework `birder` open-source (GitLab), licence Apache 2.0. Livrable : `TEAM_Inbox/2026-07-03_dobby_analyse-birder-dinov2-bio.md`.
- [2026-07-03] [NEXUS_ACOUSTIC — Téléchargements] : InsectSet459 sur M5 — Train.zip (48 GB, MD5 ✅) + Validation.zip (15 GB, MD5 ✅) téléchargés. Test.zip (16 GB) en cours (2.3 MB/s, ~1h50 restant). Emplacement : `JCH_Inbox/03_PROJECTS/12_NEXUS_ACOUSTIC/datasets/InsectSet459/`.
- [2026-07-03] [WILDNEXUS — Correction hardware-state] : Commande Mouser #39492997 n'était PAS reçue — statut réel = BACKORDER. Bloqueur TPS62840DLCR (Buck TI) ETA 15 juillet. hardware-state.md corrigé (✅→⏳). MP1584 DC-DC ×5 reçus séparément. Panier Mouser restant ~279€ toujours à commander.
- [2026-07-03] [Hardware — Prototypage] : 5× MP1584 DC-DC Step Down 3A reçus. Ultra-Small, réglable, remplace LM2596. Alimentation projets WildNexus/IoT. Enregistré dans `hardware-state.md`.
- [2026-07-03] [Système — Threads Memory System] : Transcript YouTube Ev Chapman analysé via inbox-analysis (7 phases). Architecture PKA déjà supérieure (State/Log, team.db, 30+ skills, retro_digest.py). Gap identifié : pas de « living thread file » par projet. P0 exécuté : skill `pka-thread-file` créé (`skills/pka-thread-file/SKILL.md`), template `thread-file-template.md` déployé. 10/10 thread files créés. Système mémoire projet actif. Livrable : `TEAM_Inbox/2026-07-03_dobby_analyse-threads-memory-system.md`.

## Session 2026-07-04 — Concordance Lupo ↔ WildNexus

- [2026-07-04] [WILDNEXUS ↔ Lupo] : Concordance caméras van Lupo × WildNexus. Même socle technique (ESP32 + caméra extérieure + solaire + IP67 + HA). Lupo = variante surveillance humaine de WildNexus. 4 actions P0-P1 : MOSFET power-gating au lieu du relais, PIR EKMB dans boîtier ESP32, test ESPHome sur WN, gateway LoRa van. Recommandation : rattacher Lupo comme sous-projet WildNexus. Livrable : `TEAM_Inbox/2026-07-04_dobby_concordance-lupo-wildnexus.md`.

## Session 2026-07-02 — Restructuration ARTEON / WildLens / PHOTO_AI_JURY / PHOTO_NATURE

- [2026-07-02] [ARTEON — Restructuration] : Analyse complète des 3 projets photo (ARTEON, PHOTO_AI_JURY, PHOTO_NATURE). Constat : 3 couches d'un même système vivant en silos. WildLens enterré en sous-dossier malgré son rôle critique de tête du funnel. Option A validée par JC — WildLens promu service prioritaire sans extraction en projet autonome.
- [2026-07-02] [WildLens — Promotion] : INDEX dédié créé (`02_ARTEON/wildlens/INDEX.md`). Édition #1 materialisée depuis transcript ChatGPT (`editions/WildLens-2026-03-28.md`). 5 sections verrouillées : Lead Editorial, Behaviour & The Lens, Technique Spotlight, Competition Dissection, Field Assignment. Relance nécessaire — 0 édition depuis 3 mois.
- [2026-07-02] [ARTEON — INDEX] : INDEX mis à jour — WildLens remonté en première position. Roadmap étape 4 (charte) marquée ✅. 13 étapes, 5 ✅, 7 ⏳, 1 🔴 (relance WildLens).
- [2026-07-02] [PHOTO_AI_JURY — INDEX] : INDEX créé (manquait). Données clés : 58 analyses, 73.8/100 moyen, 81% acceptation JC. MCP LR partiellement installé (activation manquante). Cross-références vers ARTEON et PHOTO_NATURE.
- [2026-07-02] [PHOTO_NATURE — INDEX] : INDEX mis à jour avec section "Voir aussi" pointant vers ARTEON et PHOTO_AI_JURY. Cross-référence presets Argus (11 XMP ici ↔ 11 PDF dans PHOTO_AI_JURY).
- [2026-07-02] [Pilotage] : `etat-projets.md` mis à jour — ARTEON passe 🟢→🟡 (relance WildLens), WildLens ajouté en sous-ligne 2a. Diagramme des relations inter-projets photo ajouté en bas de fichier.
- [2026-07-02] [ARTEON — etat-projet] : `arteon-etat-projet.md` mis à jour — étape 4 charte marquée ✅, date mise à jour 02/07.

## Session 2026-07-01 — Réception SSD + Réorg hub OpenRouter

- [2026-07-01] [IoT — Hardware] : SSD Fanxiang NVMe 256GB reçu + **PV PI HAT reçu** (avance sur prévision 15/08). Le RPi 5 vanlife est complet : SSD + shield + boîtiers + PV PI HAT. Assemblage prêt à lancer. → [Guide d'assemblage](JCH_Inbox/03_PROJECTS/11_IOT/iot-van/ASSEMBLAGE-RPi5-VANLIFE.md) créé.
- [2026-07-01] [AI_IT_TOOLS — OpenRouter] : GLM 5.2 (`z-ai/glm-5.2`), Claude Sonnet 5 (`anthropic/claude-sonnet-5`), ChatGPT (`openai/gpt-chat-latest`) ajoutés comme lanceurs OpenRouter dans `dobby.sh` et le hub. Claude Code et Codex CLI retirés du hub (remplacés par OpenRouter).
- [2026-07-01] [AI_IT_TOOLS — Bootstrap] : `deepseek_chat.py` enrichi : ADAPTER-PROMPT.md et TEAM/dobby.md ajoutés au system prompt (6 fichiers, ~78K chars). PKA_PROVIDER renseigné pour chaque modèle OpenRouter.
- [2026-07-01] [IoT — Capteurs] : Document INBOX « détecteur niveau eau » analysé et structuré. → [SPEC-DETECTEUR-NIVEAU-HYDROSTATIQUE.md](JCH_Inbox/03_PROJECTS/11_IOT/_shared/detecteur-niveau-liquide/SPEC-DETECTEUR-NIVEAU-HYDROSTATIQUE.md). Solution TL-136 + ADS1115 + ESP32, BOM ~60-80€ par point, code ESPHome validé, use cases vanlife + serre documentés.
- [2026-07-01] [AI_IT_TOOLS — Hub] : Restructuration du hub avec menu latéral (sidebar 220px, ancres smooth-scroll) et lanceurs LLM remontés en première position.
- [2026-07-01] [AI_IT_TOOLS — Dashboard] : Correction du routage `/api/launch/` dans `dashboard_server.py` (accepte `/api/launch/*` et `/launch/*`). Ajout glm5, claude-or, chatgpt au dict MODELS.

## Session 2026-07-02 — Réception ADS1115 + ESP32-C3 Super Mini

- [2026-07-02] [IoT — Hardware] : **3× ADS1115 ADC Module** (Heemol, 9,21€) + **3× ESP32-C3 Super Mini** (Heemol, 15,98€) reçus. Composants pour le détecteur de niveau hydrostatique (projet `11_IOT`). `hardware-state.md` et `SPEC-DETECTEUR-NIVEAU-HYDROSTATIQUE.md` mis à jour (🔴 Commandé → ✅ REÇU).
- [2026-07-02] [IoT — Prochaine étape] : Reste à recevoir : sonde TL-136, alim 24V, buck/boost converters, chargeur TC4056, accus 18650. Assemblage proto banc dès que la sonde et l'alim sont là.
- [2026-07-02] [IoT — Zigbee] : **Aqara Light Sensor T1** (`GZCGQ11LM`, IEEE `0x54ef44100162b3de`) appairé avec succès. Renommé `Aqara_Lux`. Exposes : illuminance (lx), batterie (%), voltage, linkquality. Ajouté dans `hardware-state.md`.
- [2026-07-02] [Infra — Docker] : Docker Desktop configuré en démarrage automatique au login (`AutoStart: true` dans `settings-store.json`).
- [2026-07-02] [ARTEON — WildLens #2] : Article validé à 100%. Photo LrC to-112.jpg (couple + poussin fous de Bassan), français par défaut, images Unsplash sections ② et ③. `WildLens-2026-07-02-preview.html` prêt pour publication.

## Session 2026-06-30 — System check & deadline WildNexus

- [2026-06-30] [WildNexus — Décision JC] : Deadline test harness caméra reportée de 15 jours → 15 juillet 2026. OV5640×5 reçus, Mouser #39492997 reçu, hardware caméra disponible.
- [2026-06-30] [IoT — Hardware] : RPi 5 + SSD NVMe + boîtiers Geekworm X1201-C1 tous reçus (29/06). Assemblage vanlife à lancer. PV PI HAT en transit (livraison ~15/08).
- [2026-06-30] [IoT — Véhicule] : **Van acheté** — Westfalia Kelsey 2026, 170CV, 4x4, blanc. Remplace le Stylevan Equinox 4 précédemment envisagé. Le projet IoT vanlife a maintenant un véhicule réel.
- [2026-06-30] [Système — State freshness] : 5 fichiers procurement CRITICAL (>14j stale, jusqu'à 37j). `etat-projets.md` remis à jour (deadline 15/07, IoT hardware). Dernier system check : 21/06 (RED, 9 jours). `hardware-state.md` à jour (29/06).

---

## État équipe

- **31 membres actifs** (source : `team.db`) — 30 spécialistes + Dobby. Audit 2026-06-22 : Ariane fusionnée dans Forge (onboarding plateforme), Fourmi fusionnée dans Araignée (bench tech). Mésange #33 créée (Naturaliste Terrain & Bioacoustique).
- **Recrutement gelé** levé ponctuellement pour besoin opérationnel avéré — re-gelé après intégration.
- **Graphify onboardé** — attribué à Corbeau (#5). Outil de knowledge graph extraction (v0.4.29), doc `docs/system/graphify.md`.

---

## Session 2026-06-19 — Photo Keyworder

- **photo_keyworder.py** — Auto-tagging photos nature par vision model local (Ollama). 100% autonome, zéro API Google.
- **Taxonomie** : 62 catégories (faune 80+ espèces, flore 40+, comportements, saisons, lumières, compositions, habitats, techniques).
- **Modèle** : gemma4 (M5 local, ~18s/image) ou llama3.2-vision:11b (M1). Testé et fonctionnel.
- **Sortie** : IPTC + XMP + HierarchicalSubject → directement lisible par Lightroom (Metadata → Read from Files).
- **Cache** : évite de re-traiter les images déjà tagguées.
- Fichiers : `scripts/photo_keyworder.py`, `06_PHOTO_NATURE/keyword_taxonomy.json`, `keyword_prompt.md`, `keyword_cache.json`.
- Usage : `python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/ --m1 --dry-run`

---

## Session 2026-06-19 — Réorganisation WildNexus

- **Extraction NEXUS_ACOUSTIC** (projet #11) — tout le bioacoustique (100+ fichiers, projet « Faune Autour — Radar de Biodiversité Acoustique ») extrait de `06_COMPONENTS/BIOACOUSTIC/` → `03_PROJECTS/12_NEXUS_ACOUSTIC/`. Spécialistes : Clio, Chouette, Musaraigne.
- **Extraction FAUNE_AUTOUR** (projet #12) — code source PWA extrait de `06_COMPONENTS/FAUNE_AUTOUR_APP/` → `03_PROJECTS/FAUNE_AUTOUR/`. Projet gelé.
- **Renommage** `06_COMPONENTS` → `06_ADJACENT` — le nom « COMPONENTS » suggérait à tort des sous-composants du projet, alors que ce sont des projets adjacents.
- **Nettoyage** `08_TECH_NOTES` reclassé (bioacoustique → NEXUS_ACOUSTIC, hardware → 99_REFERENCES, veille → veille/). PPK2 CSV déplacés de `05_VISUALS` vers `03_ENERGIE_AUTONOMIE/mesures/`.
- **Création** `03_P0_ENGINEERING/99_REFERENCES/` pour ESP-DIVE, PPK2, datasheets, veille.
- Analyse complète dans `TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md`.
- Projets actifs : 10 → 12 (NEXUS_ACOUSTIC + FAUNE_AUTOUR extraits).

---

## Échecs récents

<!-- Dobby log automatiquement les échecs ici — Format : [YYYY-MM-DD] [Agent] : [Description] [Statut : résolu/ouvert] -->
- [2026-06-07] [M1] : M1 headless (100.73.212.110) régulièrement inaccessible — sleep/standby actif malgré `sleep 0`. Cause : `standby 1` + `hibernatemode 3` par défaut. Résolu par `sudo pmset -a standby 0 hibernatemode 0`. Vérifié : p2p direct, SSH, Ollama OK. [Statut : résolu]

---

## Décisions structurelles (juin 2026)

- [2026-06-23] [BirdNET — Intégration] : L'écosystème BirdNET (Cornell) est officiellement reconnu comme référence architecturale pour NEXUS_ACOUSTIC. Le pattern double canal mel spectrogram sera intégré au pipeline InsectNet. birdnet-stm32 et BirdNET-Tiny-Forge serviront de référence pour le déploiement TinyML sur ESP32-S3. geomodel (MIT) sera utilisé comme base pour un post-filtre spatial GBIF des détections InsectNet.
- [2026-06-04] [Optimisation] : MEMORY.md allégé — historique déplacé vers `wiki/archives/memory-history-2026-05.md`. Skills communautaires inutilisées retirées de `skills-lock.json`. Pointer files regénérés. System check auto-healing ajouté.
- [2026-06-04] [Pointer] : Tool pointers régénérés — 10 projets, 2 inbox. Permissions HA corrigées (0600).
- [2026-06-03] [Onboarding] : Graphify attribué à Corbeau par extension de responsabilités — pas de nouveau membre.
- [2026-06-05] [Auto-training] : `dobby_retro.py` réécrit — multi-source (DeepSeek TUI, Claude, composer_history), extraction locale patterns, provider OpenRouter. Tables `retro_patterns` + `retro_sessions` dans team.db.
- [2026-06-05] [Fine-tuning] : Pipeline LoRA via MLX — `dobby_train.py`. Modèle fine-tuné `Qwen2.5-7B-Instruct` + LoRA sur M1 (32GB RAM, 14.6GB peak). Ollama model `dobby-prompt` créé.
- [2026-06-05] [Infra] : Python 3.12.4 + MLX 0.31.2 installés sur M1 via pyenv. Cron 23h actif sur M1 pour rétro quotidienne. Launchd plist sur M5 (installer via `bin/install-dobby-retro.sh`).
- [2026-06-06] [HA] : iPad ajouté comme tableau de bord HA via Tailscale — `http://100.108.55.44:8123`
- [2026-06-06] [NotebookLM] : 5 notebooks préparés — WildNexus (25), Vetalyx (25), PhotoNature (25), Travels (25), PhotoAIJury (12). Correction budget WildNexus v0.3 (pivot AA). 7 livrables notebook_sources/.
- [2026-06-07] [Infra] : M1 — pmset corrigé (standby 0, hibernatemode 0). Maintenance session : permissions logs 0600, pointers regénérés, todo HTML resynchronisé. Modèles Ollama mis à jour : remplacement phi4 + mistral-nemo par gemma3:12b-it-qat (gain ~16 Go).
- [2026-06-07] [Domotique v1] : Première ébauche avec **N100 + HA OS** (Beelink S12 Pro). Budget vérifié ~387€. Plan dans `docs/system/station-domotique-plan.md`.
- [2026-06-06] [Onboarding] : Araignée #30 onboardée — IoT & Embedded Systems Specialist. Recrutement suite mandat Furet.
- [2026-06-07] [Domotique v2] : Pivot vers **RPi5 4GB + SSD USB** après analyse budget. Budget vérifié ~234-260€. Même coordonateur Zigbee (Sonoff ZBDongle-P). Plans disponibles : `docs/system/station-domotique-plan.md` (N100) et `docs/system/station-domotique-plan-rpi5.md` (RPi5).
- [2026-06-08] [Onboarding] : Fourmi #31 onboardée — Bench Technician Électronique & Protocoles. Recrutement suite gap opérationnel M-02 WildNexus. Profil : exécution protocoles, câblage, mesures PPK2, diagnostic 1er niveau.
- [2026-06-09] [Sécurité] : Secrets pka-decouvertes isolés dans `JCH_PRIVATE/decouvertes.env`. Token Telegram renouvelé. TokenMaskFilter + RotatingFileHandler sur collector.py. Log purgé (88K lignes → 0 token). `.gitignore` renforcé.
- [2026-06-09] [Convention] : Attribution modèle désormais documentée dans chaque script via champ `Model:` en docstring. Format : `Model: <modèle> (date, contexte)`. Objectif : affiner les choix de modèle par type de tâche.
- [2026-06-09] [Cleanup] : Artefacts NotebookLM supprimés — 6 × `NOTEBOOKLM_SOURCES.md` + 5 × `notebook_sources/` (~100 fichiers copies) éliminés des projets. Doublons, plus besoin.
- [2026-06-12] [Skills] : 25 skills SEO (claude-seo) installées depuis AgriciDaniel/claude-seo → `.claude/skills/seo*`. Trace #20 activé. Couverture : technique, contenu, schema, local, backlinks, ecommerce, GEO, programmatique.
- [2026-06-12] [Knowledge] : Glossaire IA 50 termes extrait de sAIpien (MIT Media Lab) → `wiki/AI-Tools/glossary-ai.md`. Cadre 6 piliers (Ideas, Data, Products, Experiences, Empowerment, Readiness).
- [2026-06-12] [Auto-apprentissage] : `pka_skill_generator.py` créé — boucle fermée retro_patterns → LLM → SKILL.md. Cron hebdo dimanche 22h via launchd.
- [2026-06-12] [Procurement] : Pipeline achat Mouser/DigiKey. Chaque ligne BOM → réf Mouser + DigiKey. Indispo → fallback auto, jamais de ligne vide. CSV prêts import. Fourmi exécute, Bruno valide budget. BOM v0.3 §11 = index canonique.
- [2026-06-18] [Procurement — Compétence autonome] : Session Arbor complète — 3 cycles de recherche exécutés. Agent `scripts/procurement/` étendu avec DigiKey Search v4, basket optimizer (seuils 50€ gratuité), validation MPN (score confiance ✅⚠️🔴), cache supply SQLite (team.db). Testé sur BOM WildNexus 11 composants : dual search 60s vs 2h manuel, facteur ~120×. Passe 2 : 100% cache, 0 appel API. Rapport dans `TEAM_Inbox/`. Farnell API confirmée (partner.element14.com — REST + SOAP, en attente de compte JCH). Octopart évalué : API payante (~$100-500/mois) non justifiée pour prototypage ponctuel. Alternatives chinoises sérieuses : LCSC (endpoint non documenté), TME (API XML documentée). Arbre Arbor dans `.arbor/research/procurement-electronique/`.
- [2026-06-18] [Pointer — Règle d'adresse] : Règle d'adresse ABSENTE des pointers AGENTS.md et DEEPSEEK.md — uniquement dans MEMORY.md et ADAPTER-PROMPT.md. Corrigé : ajoutée en #1 dans la section Behavioral rules (MANDATORY) des deux fichiers. Root cause : `generate_tool_pointers.py` n'incluait pas la règle d'adresse dans le template. À corriger côté générateur si les pointers sont regénérés.
- [2026-06-12] [Procurement — Prix réels] : ⚠️ PIR EKMB estimé 5€ → réel 22,30€ (×4.5). Règle : tout prix BOM vérifié sur site fournisseur avant présentation. Ne jamais estimer de mémoire. Écart >2× fausse les priorités CoG.
- [2026-06-19] [Honcho PKA] : Pivot asynchrone → synchrone. Dobby exécute Honcho en direct après chaque session significative (≥5 échanges, /save, décision). Insights stockés dans `user_model` (team.db), confiance ≥0.8 → proposition USER.md automatique. Design spec v0.2 : `docs/system/honcho-pka-design.md`.
- [2026-06-19] [Memory Nudge] : Pivot batch → synchrone. Dobby exécute Memory Nudge en direct toutes les ~10 réponses — extrait faits JC, décisions, patterns. Cohérent avec Honcho synchrone. Script `pka_memory_nudge.py` reste en fallback batch.
- [2026-06-19] [Skill Generator] : Ajout sources Honcho (`user_model`) et Memory Nudge (`dobby_feedback`) en priorité sur `retro_patterns`. Poids : Honcho ×3, Nudge ×2, retro ×1. Dry-run OK — les 3 top candidats sont maintenant des insights Honcho structurés au lieu de fragments bruités. En accumulation — point dans quelques semaines.
- [2026-06-19] [Gateway unifiée] : `pka_gateway.py` (480+ lignes) — point d'entrée unique multi-canal remplaçant les connecteurs fragmentés. 5 canaux actifs (local_inbox, dropbox_inbox, apple_notes, telegram, git_commits). Table `gateway_messages` dans team.db, state file `_local/gateway_state.json`, launchd plist `com.dobby.pka-gateway.plist`. Premier scan : 164 messages détectés.
- [2026-06-19] [Telegram — remise en route] : Bot out depuis le 19 juin. Diagnostic : clés API Anthropic + OpenAI périmées dans `.env` (différentes des clés centrales `~/.config/pka-jch/api_keys`). Bug Markdown entities : `parse_mode="Markdown"` causait `BadRequest` sur les réponses Claude. Corrigé : `.env` mis à jour depuis clés centrales, 5 parse_mode Markdown → None, conflit launchd résolu (ancien `com.pka.dobby.plist` désactivé, nouveau `com.dobby.telegram-bot.plist`). Bot actif, canal Telegram intégré dans gateway.
- [2026-06-12] [Skills — Analyse] : 59 skills audités, classés par fréquence (5 niveaux). 25 skills SEO = 42% du catalogue, <5% des activations. Cœur opérationnel = 15 skills.
- [2026-06-12] [Skills — Amélioration] : Top 12 skills analysés — 4 corrigés (session-start, file-versioning, obsidian-kg, wildnexus-adr), 4 shadowés (ingest, capture, brief, status), 2 créés (system-check, weekly-report). Décision : les skills locaux `skills/` prennent priorité sur les skills fondation du runtime. Politique de shadow pour toute amélioration future.
- [2026-06-12] [Pipeline ESP32] : Arduino CLI 1.5.1 + ESPHome 2026.5.3 installés sur M5. Core ESP32 3.3.9. En attente d'un ESP32 branché pour test blink. Pipeline prêt pour prototypage firmware WildNexus conversationnel.
- [2026-06-13] [InsectNet — Alpes] : Query Xeno-Canto API v3 → 132 espèces d'orthoptères dans l'arc alpin (box:44,5,48,13), 2 868 enregistrements. Nos 5 espèces V0.1 = 6.1% du potentiel. Inventaire complet dans `INSECTNET/02_DATASET/alpine-species-inventory.md`. Genres clés : Chorthippus (700+), Pholidoptera (260+), Anonconotus endémique (140+).
- [2026-06-13] [Qualité — Vérification] : Règle « Données chiffrées vérifiées » élargie en « Vérification avant affirmation » dans AGENTS.md + MEMORY.md. Registre `docs/system/sources-verite.md` créé — 40+ domaines avec source autoritaire et outil. Protocole 3 temps : fichier projet → outil externe → dire « non vérifié ».
- [2026-06-13] [Architecture — LLM Wiki] : Pattern Karpathy adopté. 3 couches formalisées dans `AGENTS.md` (Raw=JCH_Inbox/PRIVATE, Wiki=wiki/, Schema=AGENTS.md+skills). `wiki/index.md` réécrit — catalogue auto-maintenu. `wiki/log.md` formaté `## [DATE] op | description` — grep-parseable. Document fondateur archivé dans `wiki/Knowledge/AI-Tools/LLM Wiki — Karpathy pattern.md`.
- [2026-06-13] [InsectNet — xcapi] : Package `xenocanto-api` (xcapi 0.3.1) adopté → remplace 3 scripts de collecte par 1 commande. Wrapper `bin/xcapi` + `scripts/insectnet_xcapi_ingest.py` (enrichissement metadata). Scripts `insectnet_xc_metadata.py`, `insectnet_select_audio_candidates.py`, `insectnet_download_audio.py` marqués DEPRECATED. Pipeline segmentation/QC/split conservé. Venv dans `.venv/`. Document Xeno-Canto routé vers `INSECTNET/01_SOURCES/`.
- [2026-06-13] [WildNexus — NLM] : NotebookLM a interprété les 12 SOPs M-02 en PPTX 14 slides (`2026-06-13_NLM_SOP-M02-Metrology_Protocol.pptx`). Analyse Dobby : capture fidèle des seuils et workflow 6 phases, mais gaps critiques — code firmware absent, règles de sécurité incomplètes (SOP-03, SOP-10), lien ADR-010 R4 manquant, grilles GO/ORANGE/NO-GO absentes. Verdict : aide-mémoire visuel uniquement, pas un remplacement des SOPs Markdown. Routé vers `03_WILDNEXUS/05_VISUALS_DASHBOARDS/` avec PNG exemple SOP-01.
- [2026-06-13] [Système — Recovery] : Gap de 7 jours dans les daily notes (08→12 juin) comblé. 5 daily notes régénérées depuis retros + sybil-auto + system checks. Diagnostic : `com.dobby.retro.plist` est opérationnel. Vraie cause : Dobby n'a pas fait de `/save`.
- [2026-06-13] [HA — Zigbee] : Préparation intégration Sonoff AirGuard TH (SNZB-02DR2, Zigbee). Script `_local/install-zigbee-ha.sh` prêt + mode d'emploi `docs/manuels/sonoff-zigbee-ha-guide.md`. Reste à faire : acheter un Sonoff ZBDongle-E (~25€), le brancher, lancer le script, puis ZHA → appairage. Pas besoin de HACS pour ce capteur Zigbee.
- [2026-06-13] [Architecture IoT — Décision] : Architecture distribuée validée. 3 HA locaux autonomes — Belgique (M5 Docker), Italie (RPi 5 + HA OS), Van (RPi 5 + HA OS). Chaque site = ZBDongle-E. Supervision unifiée via iPhone (app HA multi-serveurs + Tailscale). Le van doit fonctionner offline (alarme portes, frigo). Pas de serveur central.
- [2026-06-14] [InsectNet — xcapi validé] : Clé API XC v3 testée, ingestion xcapi fonctionnelle. Cicada orni absent de XC — remplacé par **Conocephalus fuscus** (30 enregistrements, qualité A, licence CC BY-SA, 24 min → ~479 segments). Métadonnées enrichies dans `02_DATASET/conocephalus-fuscus-metadata.csv`.
- [2026-06-14] [ARTEON — Phase 0.3] : Évaluation JCH des rapports Argus — 16/58 analyses évaluées. Résultat : 81% d'acceptation (2👍 + 11👌), 19% de rejet (3👎). Points faibles : identification d'espèces ambiguës, scènes complexes. Prompt mis à jour dans `run_analysis.py` (+ règles géographiques, + règles scènes complexes). Dashboard dans `02_ARTEON/phase03-evaluation-argus.html`.
- [2026-06-15] [Backup] : Backup chiffré PKA → Dropbox (`scripts/backup_pka_to_dropbox.py`). AES-256-CBC via Keychain. team.db + JCH_PRIVATE chiffrés, MEMORY.md + docs/system/ en miroir. Launchd quotidien 08:15. Rotation 7j.
- [2026-06-15] [Sécurité] : Scanner prompt injection `pka_prompt_guard.py` déployé. Architecture airlock 3 niveaux : pré-traitement HTML/Unicode → détection patterns/heuristiques → scoring 0-100 + quarantaine. Pipelines inbox (ingest, Pie) intégrés. 5 familles d'attaques couvertes : zero-width binaire, Unicode tags, bidi override, homoglyphes, payload splitting. Recherche OWASP LLM01 + promptfoo + ctx-guard + cyberdesserts. Brief Pie (`TEAM_Inbox/2026-06-15_dobby_brief-pie_prompt-injection-security.md`).
- [2026-06-14] [InsectNet — M1] : Plan de migration du pipeline InsectNet (segmentation, spectrogrammes, training CNN) du M5 (16 Go) vers le M1 headless (32 Go, MLX 0.31.2, Python 3.12.4). Gains : RAM ×2, délestage M5, jobs longs 24/7 sans impacter le bureau. À exécuter plus tard — nécessite accès M1 au dépôt PKA (rsync ou partage réseau).
- [2026-06-20] [Kimi — Routing] : Kimi K2.7 basculé d'OpenRouter → API Moonshot directe (`api.moonshot.ai/v1` — `.cn` → `.ai` corrigé après 401). Clé `~/.config/pka-jch/kimi_key.txt`. Modèle `kimi-k2.7-code`. `KIMI.md` créé (pointer file dédié). `deepseek_chat.py` rendu générique via `PKA_POINTER` + `PKA_PROVIDER`. `dobby.sh` : case `kimi|kimik2|moonshot`, extrait du bloc OpenRouter ; détection auto `.venv/bin/python3` (évite conflit pydantic Python 3.13 système). `model_config.json` + `dobby-doctor.py` endpoint corrigés.
- [2026-06-20] [Siri — CarPlay] : Guide complet `docs/manuels/dobby-siri-carplay.md` — Raccourci iOS « Dobby » permettant de parler à Dobby via Siri + API Kimi en mains libres (voiture, CarPlay). Pipeline : dictée vocale → API Moonshot → réponse lue par Siri. ~$0.02/interaction.
- [2026-06-20] [Agent — Outils] : `deepseek_chat.py` upgadé en agent avec tool calling (OpenAI-compatible). 5 outils : `read_file`, `list_dir`, `grep_files`, `exec_shell`, `write_file`. Workspace isolé dans PKA_DIR. Tous les modèles (DeepSeek, Kimi, OpenRouter) bénéficient des outils automatiquement. Kimi K2.7 confirmé compatible tool calling natif.
- [2026-06-20] [Gateway — Intégration] : Gateway (`pka_gateway.py`) intégrée au protocole de démarrage Dobby. 128 messages historiques acquittés. À chaque « dobby », Dobby interroge `gateway_messages` pour les nouveaux messages depuis la dernière session. 5 canaux : Telegram, Dropbox, Apple Notes, inbox local, git commits. Piste d'audit complète.
- [2026-06-20] [P1 — Nettoyage] : 16 launchd zombies désactivés (→ `.disabled`), 22 MB de logs purgés. `.claude/skills/` supprimé (doublon de `.agents/skills/`). 3 venvs → 1 (`.venv` unique, 210 MB libérés). `requirements.txt` unifié racine. `pka_security_audit.py` exclut `node_modules`, `.venv`, `*.d.ts` — 12 faux positifs → 0. 8 `.DS_Store` + `.bak` supprimés.

---

## Suivi des modèles par script

| Script | Modèle | Date | Tâche |
|--------|--------|------|-------|
| `scripts/decouvertes-collector/collector.py` | unknown | ~2026-06-02 | Bot Telegram collecteur |
| `scripts/decouvertes-collector/analyzer.py` | unknown | ~2026-06-02 | Analyse lieux + fiches Obsidian |
| `scripts/decouvertes-collector/collector.py` (fix) | deepseek-v4 | 2026-06-09 | TokenMaskFilter, rotation logs, isolation secrets |
| `scripts/insectnet_xcapi_ingest.py` | deepseek-v4 | 2026-06-13 | Ingest Xeno-Canto via xcapi + enrichissement metadata |

---

## Session 2026-06-19 — Amélioration système Hermes → PKA

### Contexte
Analyse du transcript Hermes Agent (NousResearch, 197k★, v0.15.2) et recherche web (docs officielles, Hermes Atlas, Honcho, Dev.to « 5 layers of memory ») + 3 spécialistes (Forge, Corbeau, Furet). Objectif : extraire les patterns applicables à PKA.

### Décisions
- **Split SOUL.md / USER.md / MEMORY.md** — pattern Hermes soul/user/memory. Architecture mémoire 3 fichiers distincts.
- **Memory Nudge** — script `pka_memory_nudge.py` (225 lignes) pour extraction mémoire post-réponse (toutes les ~10 réponses ou /save)
- **Alerte compression contexte** — règle SOUL.md : Dobby alerte à 50% du context window
- **Skill system-improvement-ingest** — grille 6 axes pour tout document d'amélioration
- **Tableaux de pilotage (×3)** — etat-projets.md, matrice-modeles.md, decisions-pka.md
- **Design specs** — Honcho PKA (user modeling évolutif) + FTS5 sessions (recherche historique)
- **Instructions système consolidées** — 42 instructions dans un tableau unique

### Fichiers créés (10)
SOUL.md, USER.md, etat-projets.md, matrice-modeles.md, decisions-pka.md, instructions-systeme.md, roadmap-p2.md, pka_memory_nudge.py, honcho-pka-design.md, fts5-sessions-design.md

### Fichiers modifiés (10)
MEMORY.md, AGENTS.md, DEEPSEEK.md, GEMINI.md, QWEN.md, CLAUDE.md, ADAPTER-PROMPT.md, SOUL.md, outils-index.md, INDEX.md (04_PILOTAGE)

### Prochaines étapes
- ✅ P0 : Memory Nudge — testé et pivoté synchrone, règle dans SOUL.md
- ✅ P0 : Alerte contexte 50% — activée dans SOUL.md
- ✅ P1 : Honcho PKA — pivoté synchrone, 4 insights, USER.md mis à jour
- ✅ P1 : FTS5 — 6 sessions indexées, pka_retrieve.py --fts opérationnel
- ✅ P1 : Memory Nudge — pivoté synchrone, cohérent avec Honcho
- ✅ Clôture : /save exécuté le 2026-06-20 — daily note + log.md
- 🔧 P2.1 : Skill generator — amélioré (sources Honcho + Nudge), en accumulation
- ⏳ P2.2 : Gateway unifiée — audit connecteurs nécessaire

### Procurement potentiel
- [2026-06-19] [Bioacoustique] : Zoom F3 (220€) + LOM MikroUši Pro (180€) = setup bioacoustique ~400€ pour InsectNet. 32-bit float, 192 kHz, stéréo séparable. À envisager pour remplacer iPhone sur le terrain. Fiche : `TEAM_Inbox/2026-06-19_dobby_recherche-zoom-f3-micro-bioacoustique.md`

---

## Session 2026-06-14 — Wokwi + Test Harness Caméra

### Décisions
- **Wokwi adopté** pour smoke tests CI WildNexus P0. Wokwi CLI v0.26.1 installé sur M5.
- **Périmètre Wokwi** : logique firmware (GPIO, SPI/SD, deep sleep, WiFi). Hors scope : caméra OV5640, LoRa SX1262, mesures conso.
- **Test Harness Caméra** : approche découplée — lire images SD → inference → benchmark, sans attendre la caméra physique. Débloque ADR-010 R4.
- Brief Forge+Nova créé (`TEAM_Inbox/2026-06-14_dobby_brief-forge-nova_test-harness-camera.md`)

### Artefacts créés
- `03_P0_ENGINEERING/05_SIMULATION/wokwi/` — projet Wokwi complet (diagram.json, wokwi.toml, firmware smoke test)
- Simulation validée : BOOT → LED → SD → LOG → deep sleep → TEST PASSED
- Leçon critique : `diagram.json` doit connecter `$serialMonitor` pour capturer le output série

### Outils installés
- `wokwi-cli` v0.26.1 (`~/.wokwi/bin/wokwi-cli`, PATH via ~/.zshrc)
- Token WOKWI_CLI_TOKEN dans ~/.zshrc
- Dépendances : arduino-cli (ESP32-S3), idf-wokwi

### À retenir
- Wokwi = smoke test logique rapide, PAS un remplacement du banc PPK2+Fourmi
- Pour caméra et LoRa : aucun simulateur n'existe. Hardware obligatoire.
- Prochaine étape : Forge+Nova livrent le test harness caméra (deadline 21 juin)

### Décision caméra (2026-06-14)
- Camemake OV5640 rejeté (MOQ 10)
- Acheté : ESP32-CAM OV2640 (~10€) comme outil dév DVP
- Commandé en parallèle : OV5640 DVP M12 24-pin NoIR sur AliExpress (~30€, délai 15-25j)
- BOM v0.2c mis à jour

### Session 2026-06-16 — Redémarrage M5 + Docker restart policy
- Vérifié redémarrage HA après shutdown M5 : OK, reparti automatiquement.
- Corrigé : zigbee2mqtt et mosquitto n'avaient pas `--restart unless-stopped` → crash au shutdown (perte dongle USB → ASH_ERROR_TIMEOUTS).
- Appliqué `docker update --restart unless-stopped mosquitto zigbee2mqtt` → les 3 conteneurs (HA, mosquitto, z2m) repartent maintenant automatiquement.
- Dongle Sonoff ZBDongle-E sur `/dev/cu.usbserial-10`, capteur SNZB-02DR2 (Temphumid) opérationnel.
- ⚠️ **RPI — Projet IoT** : reproduire cette config sur le RPi. Tout conteneur Docker (HA, mosquitto, zigbee2mqtt, etc.) devra avoir `--restart unless-stopped`. Anticiper le même scénario : shutdown → dongle USB disparaît → conteneur perd le port série → sans restart policy, mort définitif. À intégrer dans la procédure de déploiement RPi.
- [2026-06-16] [WildNexus — BOM] : A19 (NULA DeepSleep ESP32-S3, ~25€, 7µA deep sleep) et A20 (Freenove Breakout nu, ~15€) ajoutés au WP02 v0.2c. Objectif : mesurer le vrai deep sleep ESP32-S3 sans overhead DevKit (AMS1117 + CP210x + LEDs = ~1 mA). Budget : +40€, réserve restante ~131€.
- [2026-06-16] [WildNexus — Production] : MCU recommandé = ESP32-S3-WROOM-1-N8R8 (~3.50-4.00 $/u en bulk, ~7-15 µA deep sleep). PCB : JLCPCB assembly pour prototypes (50-60 $ pour 5 PCB soudés). Fourmi QC. Décision JCH : attendre la fin des SOPs M-02 avant de lancer le PCB. A20 (Freenove) à supprimer — redondant avec NULA.
- [2026-06-16] [Permissions — Corrigé 17/06] : 22 fichiers `_local/` (HA DB, zigbee2mqtt logs/DB, zigbee-bridge.log, collector.log) → 0600. 66 faux positifs ignorés (node_modules/ tokenizers, .venv public certs).
- [2026-06-16] [Argus — MCP] : `lightroom-mcp` (github.com/Automaat/lightroom-mcp) et `photoshop-mcp` (github.com/alisaitteke/photoshop-mcp) découverts. Ces MCP servers permettent à un LLM de contrôler Lightroom Classic et Photoshop sans intervention humaine. Argus génère déjà des `lr_params` (JSON) dans `argus_critique.db` → le chaînon manquant est l'application automatique de ces paramètres dans LR via `set_develop_settings`. Roadmap détaillée dans `05_PHOTO_AI_JURY/roadmap-mcp-integration.md`.
- [2026-06-17] [InsectNet — Stratégie test ASAP] : Pipeline audio fonctionnel, dataset Conocephalus fuscus prêt (~479 segments). 3 découvertes DDG : **InsectSet459** (Nature, 26k fichiers, 459 espèces Orthoptères), **PULSE** (arXiv juin 2026, framework semi-supervisé), **BirdNET transfer learning pour insectes** (chirpkit, 37%→55%). Plan 3 phases : baseline BirdNET → fine-tuning → PULSE. Brief Clio pour évaluation scientifique. JCH va enregistrer des chants d'insectes en Italie (longues séquences WAV recommandées).
- [2026-06-17] [IoT RPi — Pré-déploiement] : Stratégie simulation/préparation pour le RPi. **PI-CI** (émulateur RPi5 Docker) pour tester la stack HA+Mosquitto+Zigbee2MQTT avant flashage SD. **QEMU ARM64 Docker** pour validation bare-metal. Briefs Forge (docker-compose ARM64 + test PI-CI + script install + van offline) et Chouette (assemblage hardware + migration capteur SNZB-02DR2 + spécification hardware van). Deadline 28 juin.
- [2026-06-17] [WildNexus — Simulation pré-réception] : Recherche DDG → 6 outils de simulation identifiés. **Cirkit Designer** (ESP32-S3 instruction-accurate, Rust/WASM, WiFi réel), **IoT Virtual Lab** (LoRaWAN), **QEMU ESP-IDF**, **CupCarbon** (Digital Twin), **Velxio** (SPICE open-source). Briefs Araignée (smoke test Cirkit + LoRaWAN simulé) et Forge (firmware MQTT + test harness caméra). Deadline 28 juin. Stratégie : tout ce qui peut être codé/testé sans hardware l'est maintenant.
- [2026-06-17] [Pointer Sync — script + DB corrigés] : `scripts/pka_pointer_sync.py` créé — détection automatique de dérive entre les 6 fichiers pointeurs et `team.db`. Trouvé : Fourmi (#31) absente de `team.db` → corrigé (INSERT). Araignée + Fourmi absentes du roster CLAUDE.md → ajoutées. Tous les compteurs (specialist count, team count, RÈGLE D'ADRESSE) synchronisés → 0 dérive. Le script s'exécute en `--fix` automatique.
- [2026-06-17] [Pointer Sync — CLAUDE.md corrigé] : 6 incohérences détectées et corrigées : (1) team count : 29 → 31 dans 2 endroits, (2) inbox count : 4 → 2, (3) tables DB manquantes ajoutées (dobby_feedback, retro_*, memory_log, email_senders, instincts), (4) doublon file_index supprimé, (5) RÈGLE D'ADRESSE absente du bloc canonique. Propagé vers AGENTS.md, GEMINI.md, DEEPSEEK.md, QWEN.md (30→31 membres, 4→2 inbox). Leçon : les fichiers pointeurs dérivent. Prochaine étape : `pka_pointer_sync.py`.
- [2026-06-17] [Conflict Checker] : `scripts/pka_conflict_checker.py` — détection de contradictions entre spécialistes inspirée de OctoChains ConflictChecker. Deux modes : heuristique (regex + Jaccard, local) et LLM (prompt matrix, via API). Détecte les conflits numériques (ratio >2x), recommandations opposées, et incohérences. Sortie structurée JSON avec sévérité (critical/high/moderate/minor). Testé sur cas réel : 3 conflits détectés entre rapports simulés (deep sleep ESP32, budget, recommandation d'achat).
- [2026-06-17] [Leçon — Mémoire transversale] : La règle d'adresse « commencer par JC » n'existait dans **aucun** fichier canonique (AGENTS.md, MEMORY.md, DEEPSEEK.md, ADAPTER-PROMPT.md). Elle était implicite, portée par les sessions Qwen/Claude mais jamais persistée. **Un système multi-modèles sans mémoire partagée perd les préférences utilisateur.** Corrigé : règle ajoutée dans AGENTS.md + MEMORY.md. Le pipeline `dobby_feedback → knowledge.type='procedure'` est précisément conçu pour éviter que ce scénario ne se reproduise. Prochaine étape : un « pointer sync » automatique qui propage les règles comportementales découvertes vers tous les fichiers pointeurs (AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md).
- [2026-06-17] [Memory Layer v2 — Procédural + Zettelkasten] : `pka_session_extract.py` étendu avec 2 nouvelles passes post-extraction : (1) **mémoire procédurale dynamique** — quand ≥3 feedbacks JCH partagent des mots-clés → génération automatique `knowledge.type='procedure'`, (2) **Zettelkasten linking** — similarité Jaccard entre nouvelles et anciennes entrées → `knowledge_links` automatiques. Inspiré de A-MEM (NeurIPS 2025), Red Hat « From context to dreams », Zylos.ai memory survey. Pipeline complet testé sur session active.
- [2026-06-17] [Memory Layer — Pipeline complet livré] : Architecture mémoire unifiée inspirée de Databricks « Memory Scaling » — spec dans `docs/system/pka-memory-layer.md`. **3 scripts créés et testés :** `pka_session_extract.py` (extraction post-session JSON → `knowledge` + `dobby_feedback` + `retro_patterns`), `pka_retrieve.py` (recherche unifiée multi-sources : team.db + graphify + file_index + MEMORY.md + wiki), `pka_generate_memory.py` (régénération MEMORY.md depuis team.db). Table `dobby_feedback` créée dans team.db. [[Corbeau]] promu Memory Curator (scoring, déduplication, détection obsolescence).
- [2026-06-17] [Purge système] : 34 session JSONs supprimés (20 MB), 46 `.DS_Store` éliminés, artifacts GitHub Actions (`build/`, `report-build-status/`) supprimés, 12 backups team.db mai-début juin supprimés (gardé 11 backups récents), 18 dossiers vides nettoyés, fichiers obsolètes (`MEMORY.md.bak`, `TTD_MASTER`, `.code-workspace`) supprimés. Routage : 3 PPK2 → WildNexus `06_COMPONENTS/PPK2/`, `argus_critique.db` → `05_PHOTO_AI_JURY/`, 16 fichiers WildNexus classés en sous-dossiers, 2 transcripts YouTube routés, Order Mouser #39492997 archivé. Inbox restante : `email_imports/` (1 audio) + `notes_apple/` (54 notes) — à traiter via ingest.
- [2026-06-19] [Architecture — Hermes] : Split SOUL.md / USER.md / MEMORY.md (pattern Hermes). Memory Nudge activé (extraction mémoire synchrone post-réponse). Alerte compression contexte 50% activée. Skill system-improvement-ingest créé (grille 6 axes). 3 tableaux de pilotage (etat-projets, matrice-modeles, decisions-pka). 42 instructions système consolidées dans instructions-systeme.md.
- [2026-06-19] [Honcho PKA + FTS5] : Table user_model + session_fts créées dans team.db. Scripts pka_honcho_analyze.py + pka_fts_index.py. Extension pka_retrieve.py --fts opérationnelle. 4 sessions indexées FTS5. Profil cognitif JC ajouté dans USER.md.
- [2026-06-19] [InsectNet — Pipeline] : 10 fichiers M4A iPhone → 1 441 segments WAV classifiés (Gryllus campestris, Tettigonia viridissima, Gryllus bimaculatus). Manifold 3D UMAP interactif. Arbor Loop densité acoustique (0.2–5 ind/ha). Recherche Lucio Arese (3D/4D sonogram). Recherche Zoom F3 + LOM MikroUši Pro (~400€).
- [2026-06-19] [WildNexus — Test Harness] : Dataset 51 images 224×224 extraites de Lightroom. Contact sheet HTML interactive. Deadline repoussée au 30 juin (attente IR Belgique). Note dropout voltage AMS1117 ajoutée à SOP-10.
- [2026-06-19] [Réorganisation — Projets] : NEXUS_ACOUSTIC (projet #11) + FAUNE_AUTOUR (projet #12) extraits de WildNexus. 06_COMPONENTS → 06_ADJACENT. Nettoyage 08_TECH_NOTES, PPK2, datasheets. Projets actifs : 10 → 12. Analyse complète dans TEAM_Inbox/2026-06-19_dobby_analyse-reorganisation-wildnexus.md.
- [2026-06-20] [Memory Nudge — Activé] : Première exécution live du Memory Nudge. Détection gap MEMORY.md (session 19 juin non capturée). Mode synchrone validé — les gaps mémoire sont détectés et comblés sans script externe.
- [2026-06-22] [Onboarding] : Musaraigne #32 onboardée — Edge AI & TinyML Specialist. Recrutement suite projet LEAFNET + besoins InsectNet.
- [2026-06-22] [IoT — Architecture] : Projet 11_IOT créé — 3 sous-projets : iot-van (RPi 5 12V DC-DC, HA autonome, Zigbee, Tailscale, prototype banc), iot-serre (RPi 5 Esneux, HA partagé, BOM 247€ prêt, 5 phases), iot-maison (même hub Esneux, ébauche long terme). Spécialistes : Araignée, Fourmi, Musaraigne.
- [2026-06-22] [LEAFNET — Création] : Sous-projet LEAFNET créé dans 12_NEXUS_ACOUSTIC. Concept WN-BIO v1.0 : nœud bioélectrique végétal ESP32-S3 + AD620ANZ. GO validé Forge. ~22€ proto banc. Phase P1 post-WildNexus P0 — nœud dédié séparé.
- [2026-06-22] [WildNexus P0 — État] : Phase M-02 banc. Option A (PPK2 + DevKit ESP32) prioritaire. Option B (proto terrain IP67) après M-02. Budget 1000€. Shortlist v0.2c active. MCU cible production : ESP32-S3-WROOM-1-N8R8.
- [2026-06-22] [Audit mémoire] : Transversalité vérifiée — gaps corrigés : session_count agrégation retro_patterns réparée (2595→721, upsert), retro_digest.py créé (inject 15 patterns/session), 3 skills IoT/LEAFNET créés (ids 35-37), MEMORY.md racine synchronisée, USER.md corrigé, ADAPTER-PROMPT.md mis à jour.
- [2026-06-23] [WildNexus — Matériel reçu] : 4× ESP32-CAM OV2640 (cartes sans module caméra) + 3× USB-C TTL Serial Adapter. Prototypage firmware caméra, debug ESP32. Registre mis à jour dans `07_PROCUREMENT_BOM/`.
- [2026-06-23] [IoT — Procurement] : PV PI (AutoEcology/Luke Ditria) commandé — 150 AUD (~90€). HAT solaire RPi : MPPT, LiFePO4 12V, 10A, RTC, watchdog. Livraison estimée mi-août 2026. Projets cibles : IoT van, IoT serre, WildNexus base, NEXUS_ACOUSTIC. Registre : `11_IOT/_shared/procurement-register.md`. Rappel team.db : 15 août 2026.
- [2026-06-23] [LEAFNET — Enrichissement] : Document `sonification.rtf` (Note Apple Notes JC) routé de INBOX → `LEAFNET/99_REFERENCES/`. Guide d'implémentation complet : XIAO ESP32-S3, ampli INA126/TLC2272, PPK2, ESP-NOW, code C++ production-ready (5 optimisations deep sleep), intégration MQTT→Home Assistant. Concordance LEAFNET v0.1 : AD623ANZ confirmé supérieur (CMRR 110 dB vs 94 dB). Scope LEAFNET enrichi (alternatives ampli, firmware ESP-NOW, intégration HA, PPK2 validation).
- [2026-06-23] [BirdNET — Analyse écosystème] : Analyse complète de l'écosystème BirdNET (Cornell + Chemnitz TU). **5 insights critiques :** (1) Architecture double canal mel spectrogram (0-3kHz + 500Hz-15kHz) directement transposable à InsectNet pour les orthoptères haute fréquence, (2) birdnet-stm32 comme architecture de référence TinyML pour ESP32-S3, (3) BirdNET-Tiny-Forge (Kedro, Apache 2.0) pour pipeline dataset FOMO, (4) geomodel (MIT) pour post-filtrage spatial GBIF, (5) ecoPi-rtf comme template dashboard bioacoustique. **9 recommandations** émises pour Clio, Chouette, Musaraigne, Forge, Araignée. Brief complet : `TEAM_Inbox/2026-06-23_dobby_analyse-birdnet-ecosysteme_integration-pka.md`. Modèles CC BY-NC-SA 4.0 — compatible recherche, à documenter pour dérivés.

- [2026-06-23][capture/episodic/P4] : Session 2026-06-23 : gap analysis mémoire+bootstrap exécuté, 5 corrections appliquées, pka_memory_capture.py créé

- [2026-06-23][capture/episodic/P4] : Session 2026-06-23 — Phase 2 mémoire : search_memory intégré dans SOUL.md, Memory Nudge temps réel via pka_memory_capture.py, check_state_freshness.py étendu à 19 fichiers (+procurement), outils-index.md + instructions-systeme.md mis à jour, 7 notes Apple routées vers projets (VETALYX, TRAVELS, NEXUS_ACOUSTIC, IOT)

- [2026-06-23][capture/episodic/P3] : Nettoyage WildNexus 2026-06-23 : 16 actions (2 vides, 3 temp, 6 déplacés, 30+ FAUNE_AUTOUR extraits, 3 ADR corrigés, _quarantine supprimé). Structure propre : PROTOCOLES/progress.md créé, VISUALS nettoyé, ADR-014 créé.

---

## Session 2026-06-24 — Outlook + OV5640

- [2026-06-24] [WildNexus — Matériel reçu] : 4× OV5640 DVP M12 reçus d'AliExpress. Total OV5640 = 5 (1× Camemake + 4× AliExpress). `hardware-state.md` mis à jour.
- [2026-06-24] [IT — Outlook] : Crash Outlook → restauration profil depuis `~/Library/Group Containers/UBF8T346G9.Office/`. Profil et données intacts mais entrées Keychain `Microsoft Office Identities Cache/Settings 2` disparues. Comptes recréés manuellement : jchytech ✅, Gmail ✅, Yahoo abandonné (timeout + mot de passe d'application). Leçon : les comptes sont dans la base Outlook + Keychain ; sans Keychain, impossible de les restaurer automatiquement.
- [2026-06-24] [AI_IT_TOOLS — Pattern 2 Mem0] : Distinction formelle mémoire session ↔ long-terme ajoutée à `SOUL.md` + `AGENTS.md`. Tableau 2 couches (Session/Contexte LLM vs Long-terme/team.db), règle « retrieval context window » en 3 étapes avant toute réponse impliquant projet/décision/état. Règle « jamais répondre de mémoire » renforcée.
- [2026-06-24] [AI_IT_TOOLS — Auto-extract v0.1] : Fonction `--auto-extract` ajoutée à `pka_memory_capture.py`. Extraction automatique de faits atomiques depuis transcripts de conversation via LLM. Primary: Gemma3 12B (Ollama M1), Fallback: DeepSeek V3 API. Prompt structuré {fact, category, importance}. 10 faits capturés en test réel (session 24 juin). Usage : `echo "conversation" | pka_memory_capture.py --auto-extract - [--dry-run]`. Limite ~6000 chars par extraction.
- [2026-06-24] [AI_IT_TOOLS — Veille Mem0] : Transcript tutoriel Mem0 analysé. Mem0 = couche mémoire agent IA avec extraction automatique de faits via LLM. **3 patterns cannibalisables pour PKA :** (1) Extraction automatique de faits atomiques depuis conversations — PKA pourrait l'ajouter à `pka_memory_capture.py` pour réduire la capture manuelle. (2) Distinction mémoire/historique opérationnalisée — PKA a déjà State/Log mais gagnerait à formaliser « retrieval context window » dans les prompts Dobby. (3) Vector DB interchangeable — PKA utilise FTS5, une couche vectorielle (Qdrant/Chroma) améliorerait la recherche sémantique cross-session. **Action différée** — à intégrer dans roadmap AI_IT_TOOLS si JC valide.

- [2026-07-01][capture/episodic/P4] : WildNexus — nettoyage projet complet : 14 fichiers mis à jour, ADR-014 renuméroté (conflit ADR-013), ADR-016 créé (firmware intégré P0 machine d'états), Start.md v0.3, budget v0.4 avec suivi achats réels (~758€ engagé/prévu / 1000€), MASTER_ARCHITECTURE marqué comme document de cadrage initial, usage policy alignée avec ADR-010 dual-license MIT+ETHICS.md, scope lock aligné micro stéréo (ADR-013), fiches produit corrigées (avertissements modèles IA, LoRaWAN non validé), agent mapping comblé, M-01 readiness clôturé, 10 inconsistances inter-fichiers corrigées

## Session 2026-07-05 — Implémentation boucle CoALA (Reconcile + Forget + Guard + Embed)

- [2026-07-05] [AI_IT_TOOLS — Memory Layer v0.2] : Analyse de 3 transcripts INBOX sur la mémoire des agents IA → framework CoALA (Princeton). 4 types identifiés : working (contexte), semantic (CLAUDE.md/AGENTS.md), procedural (skills/), episodic (MEMORY.md). Implémentation de 3 améliorations P0/P1/P2.
- [2026-07-05] [P0a — Auto-Reconcile] : `pka_memory_capture.py` v0.2 — ajout de `auto_reconcile()` : quand un fait contredit une entrée existante (même clé, valeur différente), supersede automatique si importance ≥ existante. Flag `--no-reconcile` pour désactiver.
- [2026-07-05] [P0b — Memory Prune] : Nouveau script `pka_memory_prune.py` — archive les entrées MEMORY.md > 90 jours vers `wiki/archives/memory-archive-YYYY-MM.md` avec résumé une ligne. Implémente le maillon « Forget » de CoALA. `--dry-run`, `--days N`, `--force`, `--json`.
- [2026-07-05] [P1a — Memory Guard] : `pka_memory_capture.py` — ajout de `guard_memory_write()` : scan pre-write de chaque fait contre 14 patterns d'injection (memory poisoning, role hijack, template injection, destructive commands). Niveaux : internal (bypass), external (warn≥20, block≥50), untrusted (block≥20).
- [2026-07-05] [P1b — Trust Levels] : Colonne `trust` ajoutée à `memory_capture` (internal/external/untrusted). Flag `--trust` pour capture manuelle, `--auto-trust` pour auto-extract (défaut: external). Faits untrusted exclus du routage vers knowledge/USER.md.
- [2026-07-05] [P2 — Semantic Retrieval] : `pka_retrieve.py` — ajout de `search_embedding()` via Ollama M1 (`nomic-embed-text`, fallback gemma3). Flag `--embed`/`--semantic`. Cosine similarity sur memory_capture + knowledge, seuil 0.5. Résultats mergés AVANT les résultats keyword.
- [2026-07-05] [outils-index.md] : Mis à jour avec les 3 nouveaux flags/scripts. Memory Pipeline documenté v0.2.
- [2026-07-05] [Tests] : Memory guard : 5/5 tests passés (clean=score 0, malicious=score 55 bloqué, internal bypass, untrusted bloqué). Prune dry-run : 4 entrées totales, 0 stales (90j), 3 stales (7j). Syntax check : 3/3 scripts OK.

## Session 2026-07-06 — Fiche technique Lupo + Correction Stylevan→Kelsey

- [2026-07-06] [TRAVELS — Lupo] : Van nommé « Lupo » 🐺 par JC. Fiche technique complète créée : `07_TRAVELS/van technique/achat-van/fiche-technique-lupo-kelsey.md`. Westfalia Kelsey 2026, Ford Transit Custom 2.0 EcoBlue 170ch, BVA8, 4×4 permanente, blanc, 5.45m, 3200kg PTAC. Équipement série + options documentés depuis catalogue UK RRP 2026.
- [2026-07-06] [Correction] : Base porteur corrigée dans tous les fichiers actifs : Ford Transit Custom (pas VW Crafter). Nom « Stylevan Equinox IV » remplacé par « Westfalia Kelsey 2026 / Lupo » dans INDEX.md, USER.md, securite-van-lupo.md.
- [2026-07-06] [Sécurité van] : Document stratégique `securite-van-lupo.md` créé — architecture 3 couches (capteurs Zigbee + verrouillage mécanique IMC + alarme Fencive), budget ~754€, plan P0→P3. Aucune serrure connectée compatible FAP européen.

## Session 2026-07-08 — Apps Roadtrip Lupo 🐺 + Recherche 6 pays

- [2026-07-08] [TRAVELS — Lupo] : Document `apps-roadtrip-lupo.md` créé dans `van technique/`. Synthèse des apps et plateformes pour roadtrip couvrant 🇫🇷 🇪🇸 🇮🇹 🇩🇪 🇧🇪 🇳🇱. 4 niveaux de priorité JC (sauvage → privé/fermier → camping isolé → camping classique).
- [2026-07-08] [Apps répertoriées] : park4night, iOverlander, Campspace, Campercontact, ACSI, Wanderlog, Windy, Cartes IGN, Organic Maps, AllTrails, Bivouacs Huttopia, France Passion, Allvan, Accueil Paysan, Bienvenue à la Ferme, España Discovery, Agricamper Italia, Natura Camping, CamperOnLine, Landvergnügen, Bauernhofcamping, stellplatz.info, Camperstop.com, VanSpot Finder.
- [2026-07-08] [Bivouacs Huttopia] : 1 000+ spots nature privatifs (15-30 €/nuit), visités et validés, réservables en ligne. 🇫🇷🇪🇸🇧🇪🇵🇹. Planificateur IA intégré.
- [2026-07-08] [Budget estimé] : ~210 €/an pour les abonnements (park4night Premium + ACSI + France Passion + Agricamper + España Discovery + Landvergnügen) + nuits à ~10-30 €.

## Session 2026-07-08 (suite) — Lupo Planner PWA

- [2026-07-08] [TRAVELS — Lupo Planner] : PWA « Lupo Planner 🐺 » créée dans `07_TRAVELS/lupo-planner/`. Carte unifiée des spots de bivouac, stockage local IndexedDB, filtrage par pays/type, roadtrips, import/export JSON, mode hors-ligne via service worker.
- Fichiers : `index.html` (754 lignes, tout-en-un), `manifest.json`, `sw.js`, `deploy.sh`
- Stack : vanilla HTML/CSS/JS, Leaflet.js (CDN), OpenStreetMap tuiles, IndexedDB, PWA installable
- Déploiement : `./deploy.sh dev` (localhost:8088), `./deploy.sh ha` (HA www/), `./deploy.sh rpi` (RPi http.server)
- 6 pays couverts 🇫🇷🇪🇸🇮🇹🇩🇪🇧🇪🇳🇱, 5 types de spots alignés sur priorités JC (sauvage → privé/ferme → camping isolé → camping → aire)

## Session 2026-07-08 (suite) — Commande Mouser #39492997 réceptionnée

- [2026-07-08] [WILDNEXUS — Hardware] : Commande Mouser #39492997 livrée complète avec 1 semaine d'avance (ETA initial 15/07). 11 références : LED IR 940nm×10, PIR EKMB 2µA×2, MEMS TDK×2, Buck TPS62840×5, Inductance 10µH×5, MOSFET SI2302×5, BME688×2, SHT31×2, Antenne LoRa×2, Dissipateur×4, Lot passifs CMS×1. 105,94€ + port.
- [2026-07-08] [WILDNEXUS — Statut] : Tous les composants actifs P0 sont maintenant reçus. Reste le panier Mouser #2 (~279€, 11 composants BOM). Prochaine étape : bench loop (SOPs WildNexus P0) avec les composants reçus.

## Session 2026-07-08 (suite) — Réorganisation P0 : IOT/Vanlife priorité absolue

- [2026-07-08] [PILOTAGE] : Réorganisation complète des projets. IOT/Vanlife promu **P0, deadline 7 août 2026** (arrivée Lupo). 6 projets gelés jusqu'à septembre : WILDNEXUS, ARTEON+WildLens, InsectNet, TRAVELS, VETALYX, NEXUS_ACOUSTIC. 3 projets P1 autonomes : PHOTO_NATURE, PHOTO_AI_JURY, AI_IT_TOOLS.
- [2026-07-08] [IOT/Vanlife — Reste à faire] : Mise en boîtier X1201-C1, silentblocs, coating, PV PI HAT, config HA finale, commander capteurs Zigbee, préparer installation Lupo.

- [2026-07-13][capture/episodic/P4] : SD RPi Lupo : Samsung PRO Endurance 256 Go commandée (89€). Reolink Argus MagiCam commandée. SSD NVMe Fanxiang 256 Go wipe effectué (ex-HA OS, maintenant HFS+). Décision : SD 256 Go seule (pas NVMe) pour fiabilité vanlife.

- [2026-07-13][capture/episodic/P3] : 3 nouveaux scripts intégrés (pattern Sanja Obsidian+AI) : pka_date_scanner.py (scan dates→follow_ups), pka_quick_capture.py (capture rapide inbox), pka_vault_maintenance.py étendu (dedup, broken links, orphans). SOUL.md et outils-index.md mis à jour.

- [2026-07-13][capture/episodic/P4] : Analyse Exosfer OBD Protect : antivol passif par permutation broches OBD. ⚠️ Incompatible avec dongle OBD permanent (WiCAN Pro). Commande WiCAN conditionnée à validation compatibilité.

- [2026-07-19][session/Dobby] : Password Mosquitto unifié Dobby2026!. Capteurs pression/altitude Esneux opérationnels dans HA (Sensor Logger HTTP→MQTT). Page assiette van autonome https://192.168.129.31:8843 (PWA, silhouette Lupo, hauteurs de cale par roue, Ford Transit Custom L2 3500×1740mm, calibration iPhone 17 Pro Max coque offset −1.6°). Noctua NF-A4x10 PWM 12V reçu pour RPi Lupo — connexion via adaptateur JST-SH + alim 12V séparée (pas compatible direct RPi 5). Ressources HA sauvegardées dans 11_IOT/_shared/. Tests réels assiette van prévus dans quelques jours.

- [2026-07-20][session/Dobby] : Page assiette van déployée sur https://aroundus.tech/lupo/assiette-van-leveling.html (Hostinger). Icône niveau à bulle (PNG 180×180). Règle YOLO ajoutée dans AGENTS.md pour tous les modèles. Analyse INBOX projet surveillance acoustique écurie : livrable TEAM_Inbox/2026-07-20_dobby_analyse-surveillance-acoustique-ecurie.md — synthèse 8 sections avec feuille de route 4 phases, briques WildNexus (SOP-13/14/15) + InsectNet (CNN 330K, F1 0.98), validation web via Savonia (projet jumeau Finlande). Source INBOX déplacée dans WildNexus/99_REFERENCES. Fichiers Revenu cadastral → JCH_PRIVATE/maman/. Images Lupo → 07_TRAVELS/vanlife/deco/.

- [2026-07-21][session/Dobby] : INBOX traité — 6 fichiers Revatis/Axovet → `08_VETALYX/partners/revatis/` (LETTER OF INTENT, Investor Brief, NDA, 2 présentations, dossier inbox). Revatis identifié comme partenaire potentiel de VETALYX. Facture → `07_TRAVELS/van technique/achats/`. Agricamper Italia 2026 → `07_TRAVELS/vanlife/destinations/`. INBOX vide ✅.

- [2026-10-18][session/Dobby] : [TRAVELS — Lupo / rétroviseur] Recherche démontage rétroviseur intérieur Ford Tourneo Custom 2026 (génération V710). Fiche atelier compilée : `docs/retroviseur-tourneo-custom-2026.md` (+ `.docx` / `.pdf` 4 pages) + 3 images de démontage du cache (`docs/retro-cache-cowl-1/2/3_*.png`, extraites d'une vidéo Ford Transit — même principe que V710). Décision finale : **ne pas démonter** (risque garantie Ford sur pare-brise/caméra ADAS) — nouveau rétroviseur attaché sur l'ancien avec **straps élastiques** (rasoir d'Occam, réversible, zéro risque garantie).

- [2026-10-19][session/Dobby] : [TRAVELS — Lupo / meuble-banquette] Projet meuble-banquette **clôturé en v5** : 3 modules à tiroir double-sens (coulisses **Chambrelan R28DD 500 mm**, 9,6 mm/côté, 85 kg/paire), hauteur tiroir 210 mm, charge 15 kg, couvercle HPL compact 12 mm dans cadre en L, traverse anti-rack, prises ovales 90×60, fonction table = rien. Livrables dans `07_TRAVELS/van technique/Meuble-banquette/` : spec `meuble-banquette-caisson-3-modules.md`, `meuble-banquette-bom-1-module.md` (BOM unitaire), `liste-coupes.xlsx`, `panneaux.xlsx/.csv`, 3 plans SVG — tous v5.

- [2026-10-19][session/Dobby] : [VOIX — à reprendre] Piste boucle locale Whisper+say **abandonnée** (latence, voix robotique, boucle micro/haut-parleur) — `scripts/voice_dobby.py` + `bin/dobby-dictate` supprimés. **Solution retenue : Gemini 3.1 Flash Live** (voix native, sans Whisper, ~200 ms). Client `scripts/gemini_voice.py` + launcher `bin/dobby-voice` (voix **Ursa**, français, system prompt « Dobby »). ⚠️ Correction API : `realtimeInput.mediaChunks` → `realtimeInput.audio` (vérifié : connexion + setup + audio acceptés, plus de 1007). Tâche VS Code « PKA: Dobby Voice (Gemini Live) » ajoutée (`.vscode/tasks.json`) + raccourci `Ctrl+Shift+V` (`.vscode/keybindings.json`). **Reste à faire :** le raccourci Ctrl+Shift+V ne s'est pas déclenché → tester la tâche via Cmd+Shift+P → « Run Task », recharger VS Code, sinon changer de touche (ex. Ctrl+Alt+V) ; conversation micro→audio pas encore validée de bout en bout. Lancement : `./bin/dobby-voice`.
