---
date: 2026-06-09
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 8
echanges: 1355
modeles: deepseek-v4, deepseek-v4-flash, deepseek-v4-pro
---

# Rétrospective — 2026-06-09

**Sessions analysées :** 8 | **Échanges :** 1355 | **Modèles :** deepseek-v4, deepseek-v4-flash, deepseek-v4-pro

---

## Décisions prises
- **Validation des paramètres** : "on va valider les parametres indiqués du moment qu'on puisse ne c" – décision partielle, nécessite clarification.
- **Matching besoins IoT van** : "on va matcher les besoins de capteurs iot van avec les besoins de" – décision de convergence entre capteurs et besoins utilisateur.
- **Suppression de dossiers** : "les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer les rapports. mets à jour l" – élimination des répertoires `notebooklm_ources` et `.md`.
- **Utilisation de Notebook LM** : choix d'outil pour la génération de rapports.
- **Mise à jour MacBook M1** : "on va essayer de mettre à jour un macbook m1 dont l'écran est cas" – intervention sur un M1 avec écran cassé.
- **Gestion RPI** : "on va s'occuper du RPI. on a eu un orage et le rpi s'est arret" – redémarrage et stabilisation après coupure.
- **Workflow découvertes** : "on va maintenant dans travels/ pka decouvertes" – organisation des logs dans `pka-decouvertes/logs`.
- **Browser externe** : question sur l'ouverture de HTML en dehors de VS Code – non tranchée.

## Échecs ouverts / bloqueurs
- **Problèmes SSH récurrents** : "Host key verification failed", "Failed to parse remote port from server output", "Exec error". Empêche la connexion aux machines distantes (M1, RPI).
- **OAuth / Keychain** : "OAuth error: Failed to save API key to macOS Keychain". Bloque l'authentification à certains services (OpenRouter ?).
- **Terminal** : "The terminal process failed to launch (Starting directory ...)". Problème de configuration de l'environnement de travail (PKA_JCH).
- **Gestion des fichiers en attente** : "d'attent garde fichiers ne inbox equipe bloquée et en cours. en attente validation et rejetes non retriate". Processus de validation non fluide, fichiers en suspens.
- **Erreurs génériques** : "ca marche pas" sans diagnostic – plusieurs occurrences indiquent un manque de suivi systématique.
- **Modèle non priorisé** : "pourquoi modele clude ne premiere attention ?" – frustration sur l'ordre de sélection des modèles.

## Questions récurrentes (signe de lacune documentaire)
- **Maintien d'outil sur M5** : "n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?" – besoin de documentation sur la persistance des outils embarqués.
- **Définitions basiques** : "duckduckgo c'est quoi ?", "c'est quoi ext4fuse". Lacune dans la connaissance des outils système.
- **Exécution automatique des tâches** : "pourquoi tu ne le fais pas", "comment faire pour que cette instruction ne soit jamais oubliée quelquesoit le modele ?". Demande de scripts autonomes et de garde-fous.
- **Partage HTML** : "comment faire en sorte que l'html s'ouvre chez quelqu'un d'autres hors reseau jch ?". Manque de documentation sur le déploiement réseau.
- **Affichage des modèles** : "continue, je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?". Problème de visualisation de la liste des modèles.

## Nouveaux patterns détectés
- **Multi-modèles simultanés** : utilisation de `deepseek-v4`, `deepseek-v4-flash`, `deepseek-v4-pro` dans une même journée. Risque d'incohérence si les instructions ne sont pas unifiées.
- **Collecte de données via Telegram** : `scripts/decouvertes-collector/collector.py` et `analyzer.py` avec utilisation de bots Telegram. Nouveau pipeline non documenté dans les fichiers centraux.
- **Dépendance à Tailscale** : mentionné comme outil de connexion réseau, mais pas de procédure de secours.
- **Cycle "attente validation et rejetes"** : pattern récurrent de fichiers bloqués dans `TEAM_Inbox` sans suivi.

## Efficacités / inefficacités
**Efficacités :**
- Utilisation de Notebook LM pour créer des rapports structurés (ex: itinéraire Baie de Somme).
- Tentative d’automatisation avec des scripts Python (collector, analyzer) – bonne direction.
- Passage à des modèles plus rapides (`deepseek-v4-flash`) pour les itérations rapides.

**Inefficacités :**
- **Manque de documentation des décisions** : les décisions sont souvent tronquées ou implicites, ce qui oblige à les redécouvrir.
- **Problèmes SSH non résolus** : les erreurs se répètent sans qu’une solution durable ne soit mise en place.
- **Dépendance excessive à l’intervention manuelle** : JCH doit souvent copier-coller des commandes ou approuver des actions (ex: "approve one").
- **Gestion des clés API** : échec OAuth récurrent, pas de procédure de récupération documentée.
- **Absence de logs centralisés** : les sessions sont multiples (DeepSeek TUI, Claude Code, Codex CLI) mais pas de vue d’ensemble.

## Ce qu'il faut garder en mémoire pour les prochaines sessions
- **Centraliser les commandes** : préférer l’exécution directe par les assistants (Claude Code, Codex CLI) plutôt que du copier-coller.
- **Documenter les échecs** : chaque "ca marche pas" doit être suivi d’un diagnostic et d’une résolution écrite.
- **Unifier les modèles** : définir une priorité claire des modèles (ex: Qwen 3.7 en local, deepseek-v4 en cloud) et la figer dans AGENTS.md.
- **Résoudre les problèmes SSH** : mettre en place une configuration SSH persistante avec clé, ou utiliser Tailscale comme solution de repli documentée.
- **Automatiser la validation des fichiers** : créer un workflow clair pour les fichiers en attente dans `TEAM_Inbox` (ex: script de tri auto).
- **Conserver les logs** : toutes les sessions doivent être sauvegardées dans `wiki/sessions/` avec un résumé.

## Recommandations
1. **Créer un guide de dépannage** (dans `wiki/troubleshooting.md`) pour les erreurs SSH, OAuth, et lancement de terminal.
2. **Standardiser l’exécution des tâches** : ajouter une section dans `AGENTS.md` qui impose aux assistants d’exécuter les commandes directement (pas de copier-coller).
3. **Mettre en place un processus d’approbation unique** : remplacer les "approve one" par une règle globale "approuver automatiquement les actions non destructives".
4. **Documenter les outils système** : ajouter des entrées dans `docs/system/outils-index.md` pour DuckDuckGo, ext4fuse, Tailscale, OpenRouter.
5. **Réviser la gestion des fichiers en attente** : implémenter un script de notification et d’archivage automatique pour les fichiers non traités.
6. **Unifier les modèles** : spécifier un ordre de sélection (ex: priorité au modèle local si disponible) et le rendre non modifiable par les assistants.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 301
- Résolus automatiquement : 144
- Résolus manuellement : 0
- Encore ouverts : 157
- **Taux : 47.8%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 169.4
- Échanges/session début fenêtre : 74.4
- Tendance globale : 127.7%
- Tendance 3j-3j : 173.3%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] B = faire immédiatement
- [Decision] C = processer (mettre en queue)
- [Decision] Contexte* : Priorisation des travaux multi-outils sur M1/M5
- [Decision] Décision : continuer sur M1 plutôt que de basculer ailleurs
- [Decision] État : la clé fonctionne mais a nécessité une reconfiguration
- [Decision] Le RPI s'est arrêté suite à une perturbation électrique
- [Decision] Procédure de redémarrage lancée
- [Decision] Détectée : un nouveau message Telegram reçu
- [Decision] Action : changement de clé de sécurité décidé
- [Decision] Élimination de fichiers non essentiels : `notebook_sources/`, fichiers `.md` orphelins
- [Decision] Vérification de leur localisation requise avant suppression
- [Decision] Question pratique soulevée : comment ouvrir un browser externe à VS Code ?
- [Decision] Décision implicite* : solution n'a pas été documentée dans le transcript
- [Decision] Stratégie d'approche ABC sur les tâches
- [Decision] Migration clé API Anthropic
- [Decision] Récupération du RPI après orage
- [Decision] Changement de clé Telegram
- [Decision] Nettoyage du répertoire travels/
- [Decision] Navigation web depuis VS Code
- [Decision] Validation des paramètres** : "on va valider les parametres indiqués du moment qu'on puisse ne c" – décision partielle, nécessite clarification.
- [Decision] Matching besoins IoT van** : "on va matcher les besoins de capteurs iot van avec les besoins de" – décision de convergence entre capteurs et besoins u
- [Decision] Suppression de dossiers** : "les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer les rapports. mets à jour l" – élimination
- [Decision] Utilisation de Notebook LM** : choix d'outil pour la génération de rapports.
- [Decision] Mise à jour MacBook M1** : "on va essayer de mettre à jour un macbook m1 dont l'écran est cas" – intervention sur un M1 avec écran cassé.
- [Decision] Gestion RPI** : "on va s'occuper du RPI. on a eu un orage et le rpi s'est arret" – redémarrage et stabilisation après coupure.
- [Decision] Workflow découvertes** : "on va maintenant dans travels/ pka decouvertes" – organisation des logs dans `pka-decouvertes/logs`.
- [Decision] Browser externe** : question sur l'ouverture de HTML en dehors de VS Code – non tranchée.
- [Failure] Symptôme : "B mais c'est toujours bloqué côté console
- [Failure] Répété 2 fois → signale un problème non résolu
- [Failure] Impact** : bloque l'avancement du projet B
- [Failure] À investiguer** : logs de console, état du venv, variables d'environnement
- [Failure] Erreur : "failed to load page
- [Failure] Contexte : probablement lié à la navigation web externe VS Code
- [Failure] Status** : non diagnostic poussé
- [Failure] `perl: warning: Setting locale failed. LANG=...`
- [Failure] Affect : scripts Perl ou dépendances indirectes
- [Failure] Contour** : n'a pas bloqué l'exécution mais pourrait causer des issues futures
- [Failure] Logs montrent : `done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelins`
- [Failure] Interprétation : cron n'a rien exécuté ou retour anormal
- [Failure] À vérifier** : crontab `-l`, permissions, chemins absolus
- [Failure] Erreur : `c'est quoi ces quote et pourquoi l'accès fichiers impossible`
- [Failure] Symptôme : quoting issue dans chemins avec espaces ou caractères spéciaux
- [Failure] Affect** : scripts Python/Shell générant des paths
- [Failure] Blocker console persistant sur projet B
- [Failure] Chargement de page en échec
- [Failure] Warnings de locale Perl
- [Failure] Déploiement cron incomplet
- [Failure] Accès fichiers impossible (quotes mal échappées)
- [Failure] Problèmes SSH récurrents** : "Host key verification failed", "Failed to parse remote port from server output", "Exec error". Empêche la connexion aux 
- [Failure] OAuth / Keychain** : "OAuth error: Failed to save API key to macOS Keychain". Bloque l'authentification à certains services (OpenRouter ?).
- [Failure] Terminal** : "The terminal process failed to launch (Starting directory ...)". Problème de configuration de l'environnement de travail (PKA_JCH).
- [Failure] Gestion des fichiers en attente** : "d'attent garde fichiers ne inbox equipe bloquée et en cours. en attente validation et rejetes non retriate". Proc
- [Failure] Erreurs génériques** : "ca marche pas" sans diagnostic – plusieurs occurrences indiquent un manque de suivi systématique.
- [Failure] Modèle non priorisé** : "pourquoi modele clude ne premiere attention ?" – frustration sur l'ordre de sélection des modèles.

### Fréquence des patterns (14 jours)
- **Decision** : 3 jours, 201 occurrences
- **Failure** : 3 jours, 201 occurrences
- **Question** : 3 jours, 189 occurrences
- **Recurring question** : 3 jours, 100 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (3x) en cours de test et seuls les testeurs approuvés par le développeur y ont accès.
- [Decision] (3x) je vais dormir on reprend demain
- [Decision] (3x) ok maintenant on va essayer de mettre à jour un macbook m1 dont l'écran est cas
- [Decision] (3x) ok maintenant on va s'occuper du RPI. on a eu un orage et le rpi s'est arret su
- [Failure] (3x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Failure] (3x) ca marche pas
- [Failure] (3x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (3x) d strict checking.Host key verification failed.jchavauxm5@mac ~ %
- [Failure] (3x) done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelinsjchav
- [Failure] (3x) générer du TypeScript/Vanilla CSS ou debugger tes scripts Python.   * Pour l'Ana
- [Failure] (3x) ive)# Usage: cron 0 3 * * *set -euo pipefail# === Config (chemins absolus pour c
- [Failure] (3x) perl: warning: Setting locale failed.perl: warning: Please check that your local
- [Question] (3x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (3x) c'est quoi ext4fuse
- [Question] (3x) duckduckgo c'est quoi ?

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 54
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**37** recommandations au total — **37** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 24
- **Forge** : 9
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=23] (2026-06-09) **Dobby** : Débugger le blocker console sur B
- [id=24] (2026-06-09) **Dobby** : Commandes de diagnostic : `python3 -m venv --help`, `pip list`, test import mini
- [id=25] (2026-06-09) **Forge** : Logs attendus : `scripts/decouvertes-collector/venv/lib/python3.13/...`
- [id=26] (2026-06-09) **Dobby** : Durée estimée : 10 min
- [id=27] (2026-06-09) **Dobby** : Documenter l'instruction système pour tous les modèles

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**
