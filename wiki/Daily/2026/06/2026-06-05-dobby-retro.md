---
date: 2026-06-05
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 98
echanges: 4456
modeles: <synthetic>, claude, claude-sonnet-4-6, codex-cli, deepseek-v4, deepseek-v4-flash, deepseek-v4-pro
---

# Rétrospective — 2026-06-05

**Sessions analysées :** 98 | **Échanges :** 4456 | **Modèles :** <synthetic>, claude, claude-sonnet-4-6, codex-cli, deepseek-v4, deepseek-v4-flash, deepseek-v4-pro

---

## Décisions prises

- **Langue de travail** : "on va garder le français sans introduire l'anglais" – décision de rester en français pour toute la communication.
- **Couleurs des modèles** : "on va utiliser des couleurs différentes pour chaque modèle" – pour améliorer la lisibilité dans les interfaces.
- **Test RPI BirdNet avec carte SIM** : validation de l'approche mobile pour la bioacoustique terrain.
- **Utilisation du working set** : répété systématiquement dans les meta-turns de DeepSeek et Codex – décision implicite de focaliser les assistants sur un ensemble de fichiers prioritaire.
- **Choix de l’imagerie WildNexus** : un prompt "camera-imaging" a été fourni et validé comme base pour la rédaction (extrait codex).
- **Déploiement de script et cron** : accepté via Codex CLI pour automatiser une tâche sur RPi.

## Échecs ouverts / bloqueurs

- **Throttling RPi** : temp=51.6°C, throttled=0x50000 – problème thermique non résolu, peut impacter les tests terrain.
- **Échec SSH** : `Host key verification failed` empêche la connexion à 192.168.129.16 – nécessaire pour accéder au RPi.
- **Erreur SSL certificat** : `[SSL: CERTIFICATE_VERIFY_FAILED]` bloque les appels AI – impacte l’utilisation d’OpenRouter et autres APIs.
- **Build GitHub Pages** : échec en 25 secondes – cause inconnue, pourrait être lié à la configuration du dépôt.
- **Locale perl** : `Setting locale failed` sur RPi – plantage possible des scripts Perl liés à BirdNET.
- **"ca marche pas"** : réponse à une tentative non documentée – manque de traçabilité de l’action échouée.
- **Accès bloqué JCH-PKA** : procédure de validation Google non terminée – bloque potentiellement l’utilisation de certains services.

## Questions récurrentes (signe de lacune documentaire)

1. **"c'est quoi ces quote et pourquoi l'accès fichiers impossible"** – posée 3 fois avec des variantes. Les `quote>` dans les meta-turns ne sont pas expliqués.
2. **"pourquoi modele claude ne première attention ?"** – question sur l’ordre de priorité des modèles, signe d’un besoin de documentation sur le routage.
3. **"comment faire pour que cette instruction ne soit jamais oubliée quelque soit le modele ?"** – demande de persistance des instructions à travers les sessions et outils.
4. **"verifie d'abord pourquoi il n'a pas été regeneré"** – demande récurrente sur l’absence de régénération d’un fichier.
5. **"comment faire en sorte que l'html s'ouvre chez quelqu'un d'autres hors reseau jch ?"** – question sur l’exposition publique d’une page, liée à Tailscale/réseau.
6. **"c'est quoi ext4fuse"** / **"duckduckgo c'est quoi ?"** – questions basiques qui pourraient être documentées dans un glossaire.

## Nouveaux patterns détectés

- **Meta-turn working set** : presque chaque échange avec DeepSeek/Codex commence par le même bloc `<turn_meta>` listant les fichiers actifs. Ce pattern de focalisation est systématique mais génère une redondance.
- **Multi-modèle en parallèle** : utilisation simultanée de DeepSeek (analyse/rédaction), Claude (Code dans Cursor), et Codex CLI (shell) – nécessite une coordination entre eux.
- **Problèmes de connectivité récurrents** : SSH, SSL, build – chaque session semble rencontrer au moins un blocage réseau.
- **Questions sans réponse** : plusieurs questions récurrentes n’ont pas de réponse dans le transcript (ex: quote, persistance des instructions) – signe que les assistants ne savent pas ou ne peuvent pas répondre.
- **Usage de "focus on working set" comme instruction passe-partout** mais sans véritable suivi – les assistants récitent le bloc sans forcément y adhérer (ex: DeepSeek répondant à des questions hors working set).

## Efficacités / inefficacités

| Efficacités | Inefficacités |
|-------------|---------------|
| Working set bien défini pour chaque session | Répétition des mêmes problèmes techniques sans correction pérenne |
| Protocole terrain 24h RPI BirdNet documenté et testé | Questions récurrentes non documentées (locale, quotes, certificats) |
| Utilisation complémentaire des outils (DeepSeek pour analyse, Claude pour code, Codex pour shell) | Manque de synchronisation entre modèles : une instruction donnée à l’un n’est pas connue des autres |
| Progression sur WildNexus (imagerie, bioacoustique, voyages) | **Temps perdu à redemander la même chose** ("vérifie d'abord pourquoi...") |

## Ce qu’il faut garder en mémoire pour les prochaines sessions

- **Résoudre les bloqueurs critiques avant de commencer** : SSH, SSL, locale perl sur le RPi.
- **Documenter les motifs récurrents** (quote, persistance, exposition HTML) dans un fichier FAQ ou dans CLAUDE.md.
- **Le RPI BirdNet avec carte SIM est fonctionnel** – prioriser les tests terrain maintenant.
- **WildNexus est le projet central** – garder les fichiers bioacoustique et caméra dans le working set.
- **Les instructions doivent être stockées de façon persistante** (MEMORY.md, CLAUDE.md) pour être relues par tous les modèles.

## Recommandations

1. **Créer un fichier `FAQ_TECH.md`** dans le dossier `wiki/` listant les solutions aux problèmes connus : quote dans les meta-turns, résolution des certificats SSL, locale Perl sur RPi, commandes SSH fiables.
2. **Ajouter une section "Instructions permanentes"** dans `CLAUDE.md` et `AGENTS.md` avec les règles que tous les modèles doivent suivre (ex: "ne pas introduire d’anglais", "vérifier avant de régénérer").
3. **Automatiser la vérification de connectivité** au début de chaque session (script `bin/check-connectivity.sh` testant SSH, SSL, build GitHub Pages).
4. **Centraliser le working set dynamique** : au lieu de répéter le bloc meta-turn manuellement, créer un fichier `WORKING_SET.md` que les assistants lisent automatiquement, et le maintenir via une commande dédiée.
5. **Mettre en place un suivi des échecs** : chaque bloqueur non résolu doit être enregistré dans `JCH_Inbox/00_INBOX/blockers.md` avec date, étape tentée, et solution éventuelle.
6. **Former un "assistant de session"** (peut-être Dobby) qui lance une checklist initiale avant toute interaction : vérifie les connexions, rappelle les instructions persistantes, et signale les problèmes ouverts.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 181
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 181
- **Taux : 0.0%**

### Évolution du volume (tendance)
- 📉 Direction : down
- Échanges/session récent : 45.4
- Échanges/session début fenêtre : 74.4
- Tendance globale : -38.9%
- Tendance 3j-3j : -38.9%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Utilisation du working set** : JCH a décidé de rester dans le working set pour toutes les sessions.
- [Decision] Pause nocturne** : « je vais dormir on reprend demain » → décision saine.
- [Decision] Réorientation sur vanlife : JCH change de priorité vers les capteurs maison.
- [Decision] Validation procurement** : approvisionnement validé après vérification.
- [Decision] Diagnostic d’un souci réseau sur le RPi (throttled, interface down) et validation du diagnostic par JCH.
- [Decision] Abandon du déploiement automatique d’un script d’analyse sur le RPi via Forge : JCH opte pour un copier-coller manuel ou un basculement vers Codex CLI
- [Decision] Validation du template de création de fichier : nouvelle règle de nommage (`nom du fich`).
- [Decision] Poursuite des tests RPi après orage (arrêt inopiné du RPi).
- [Decision] Report des opérations RPi au lendemain : « je vais dormir on reprend demain ».
- [Decision] Confirmation partielle du procurement : JCH demande validation, pas de réponse explicite immédiate.
- [Decision] Validation du protocole RPi BirdNet mobile** : JCH valide le test terrain avec carte SIM fonctionnel. Le protocole est individualisé pour validation a
- [Decision] Nom de code « Arteon »** : Adopté pour identifier le duo de collaborateurs chinois. Décision prise sans documentation formelle dans les fichiers du wo
- [Decision] Automatisation validée** : Un processus d’automatisation a été confirmé (non précisé). Niveau 2 (validation humaine requise) vs Niveau 3 (interdit san
- [Decision] Analyse différée** : JCH reporte l’analyse d’un élément (« j’analyserai cela après ») – décision de priorisation non enregistrée.
- [Decision] Langue de travail** : "on va garder le français sans introduire l'anglais" – décision de rester en français pour toute la communication.
- [Decision] Couleurs des modèles** : "on va utiliser des couleurs différentes pour chaque modèle" – pour améliorer la lisibilité dans les interfaces.
- [Decision] Test RPI BirdNet avec carte SIM** : validation de l'approche mobile pour la bioacoustique terrain.
- [Decision] Utilisation du working set** : répété systématiquement dans les meta-turns de DeepSeek et Codex – décision implicite de focaliser les assistants sur u
- [Decision] Choix de l’imagerie WildNexus** : un prompt "camera-imaging" a été fourni et validé comme base pour la rédaction (extrait codex).
- [Decision] Déploiement de script et cron** : accepté via Codex CLI pour automatiser une tâche sur RPi.
- [Failure] Host key verification failed** : échec SSH entre M5 et M1.
- [Failure] birdnet.service introuvable** : le service systemd ne se lance pas.
- [Failure] OAuth Keychain** : erreur de sauvegarde de clé API dans le trousseau macOS.
- [Failure] - **birdnet.service introuvable** : le service systemd ne se lance pas.
- [Failure] RPi BirdNET arrêté après orage** : plantage suspecté dû à la foudre ou à une coupure réseau. Le diagnostic montre `throttled=0x50000` (indicateur de t
- [Failure] Échecs de connexion SSH répétés** : `Host key verification failed.` et messages `failed to connect`. Le terminal local (M5) parvient à accéder au RPi,
- [Failure] Erreur locale sur Mac JCH** : `perl: warning: Setting locale failed.` — indique une config locale incomplète.
- [Failure] Service birdnet.service introuvable** : `Failed to stop birdnet.service: Unit birdnet.service not loaded.` — le service n’est pas présent au moment de
- [Failure] Pages GitHub build échoué** : `build	pages build and deployment / build Failed in 25 seconds` — problème de déploiement automatique non résolu.
- [Failure] Accès bloqué à JCH-PKA** : JCH-PKA n’a pas terminé la procédure de validation de Google (selon le message d’erreur).
- [Failure] Print dans VS Code ne fonctionne pas** : Bloqueur répété, non résolu dans la session.
- [Failure] BirdNET Pi : modem détecté mais pas d’interface wwan/opérateur** : `lsusb` montre le modem ZTE/Huawei, mais `ip addr` et `nmcli` ne montrent aucune in
- [Failure] Build GitHub Pages échoué en 25 secondes** : `annotations for pages build and deployment / build` – échec rapide, cause non documentée.
- [Failure] Erreur OAuth / Keychain macOS** : Échec de sauvegarde de la clé API dans le trousseau (`OAuth error: Failed to save API key to macOS Keychain`).
- [Failure] Erreur DeepSeek TUI : `Error: Failed to parse config file`** : Fichier de configuration `/Users/jchavauxm5/.deepseek/config` mal formé ou inexistant.
- [Failure] Throttling RPi (0x50000)** : Température 48.8°C, throttling détecté, non adressé.
- [Failure] Throttling RPi** : temp=51.6°C, throttled=0x50000 – problème thermique non résolu, peut impacter les tests terrain.
- [Failure] Échec SSH** : `Host key verification failed` empêche la connexion à 192.168.129.16 – nécessaire pour accéder au RPi.
- [Failure] Erreur SSL certificat** : `[SSL: CERTIFICATE_VERIFY_FAILED]` bloque les appels AI – impacte l’utilisation d’OpenRouter et autres APIs.
- [Failure] Build GitHub Pages** : échec en 25 secondes – cause inconnue, pourrait être lié à la configuration du dépôt.
- [Failure] Locale perl** : `Setting locale failed` sur RPi – plantage possible des scripts Perl liés à BirdNET.
- [Failure] "ca marche pas"** : réponse à une tentative non documentée – manque de traçabilité de l’action échouée.
- [Failure] Accès bloqué JCH-PKA** : procédure de validation Google non terminée – bloque potentiellement l’utilisation de certains services.

### Fréquence des patterns (14 jours)
- **Decision** : 1 jours, 121 occurrences
- **Failure** : 1 jours, 121 occurrences
- **Question** : 1 jours, 121 occurrences
- **Recurring question** : 1 jours, 60 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 43
- Jours d'observation : 1
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**13** recommandations au total — **13** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 8
- **Forge** : 4
- **Corbeau** : 1

### Plus récentes ouvertes

- [id=1] (2026-06-05) **Forge** : Créer un fichier `TROUBLESHOOTING.md`** dans le working set pour les erreurs réc
- [id=2] (2026-06-05) **Dobby** : Mettre en place des guardrails de bout en bout** : avant de changer de modèle/ou
- [id=3] (2026-06-05) **Dobby** : Standardiser le feed-forward de contexte** : quand JCH donne un YAML skill ou un
- [id=4] (2026-06-05) **Forge** : Installer un outil CPU/memory monitor sur le RPi** : `htop` ou `top` en tête, et
- [id=5] (2026-06-05) **Forge** : Documenter le « protocole Arteon »** : écrire une fiche dans `TEAM/` ou `JCH_Inb

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.
