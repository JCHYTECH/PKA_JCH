---
date: 2026-06-13
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 5
echanges: 1125
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-13

**Sessions analysées :** 5 | **Échanges :** 1125 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective de Session — 2026-06-13

## Décisions prises

1. **NotebookLM pour les rapports wildnexus, iot et travels**  
   Décidé d’utiliser NotebookLM pour créer les rapports de ces trois projets. **Mais** la décision a été prise sans valider l’accessibilité des données sources ni le workflow de génération.

2. **Retour au choix RPi**  
   Validé après vérification des coûts réels. Question : les coûts ont-ils été réellement vérifiés ou juste supposés ? Le transcript ne montre pas de consultation de devis.

3. **Priorisation A/B/C**  
   “le A on va attendre, le B on fait et le C processer” — décision claire mais non documentée dans un fichier quelconque (ex: PRIORITIES.md ou BOARD.md).

4. **Nettoyage des dossiers notebooklm_sources et .md**  
   “on va les éliminer. vérifie où ils sont” — décision de purge prise sans vérification préalable de l’impact sur les projets.

## Échecs ouverts / bloqueurs

1. **Erreur SSH persistante**  
   ```  
   debug1: Server host key: ssh-ed25519 SHA256:...  
   Using connect timeout of 17 seconds  
   ```  
   Connexion échouée (timeout/refus). **Problème non résolu**, aucune action corrective documentée.

2. **Erreur Telegram Bot — 409 Conflict**  
   L’updater Telegram retourne 409 Conflict (conflit de session). Le bot est probablement déjà actif ailleurs. **Bloquant** pour le collector de découvertes. Aucune solution proposée.

3. **Erreur MCP Plane Server**  
   `failed to connect` — pas de détail, pas de diagnostic. L’agent MCP plane est hors ligne.

4. **Déploiement du cron Dobby**  
   `Bootstrap failed: 5: Input/output error` — le cron/launchd de la rétrospective automatique ne démarre pas. Cause : permissions ou fichier plist corrompu.

5. **Recherche infructueuse Arducam IMX500**  
   “j’ai trouvé ceci Arducam IMX500 AI Camera Module for ESP32-P4... c’est de ça” — pas de validation que le composant est compatible avec le besoin réel.

## Questions récurrentes (signe de lacune documentaire)

1. **“Pourquoi en 2 tu parles de USB-A, le Mac a des USB-C ?”**  
   Posé **au moins 2 fois**. Signe que les spécifications hardware de la machine (M1/M5) ne sont pas documentées dans AGENTS.md ou MEMORY.md.

2. **“C’est quoi ces `quote>` et pourquoi l’accès fichiers impossible ?”**  
   Posé **au moins 3 fois**. L’utilisateur ne comprend pas le formatage des citations dans le transcript, et le problème d’accès aux fichiers n’est jamais résolu.

3. **“Pourquoi ne proposes-tu pas de les mettre dans les dossiers projets respectifs ?”**  
   Signe que la structure de répertoire (PKA_JCH/projets/X) n’est pas respectée par les assistants.

4. **“Comment installer HACS / HA / DeepSeek-TUI / Qwen via OpenRouter ?”**  
   Récurrent — montre qu’il manque un guide d’installation centralisé pour les outils courants (HACS, Home Assistant, DeepSeek-TUI, Ollama, OpenRouter).

5. **“Vérifie d’abord pourquoi il n’a pas été regénéré”**  
   Posé plusieurs fois pour différents scripts/crons. L’utilisateur doit systématiquement rappeler de diagnostiquer avant d’exécuter.

## Nouveaux patterns détectés

1. **Demande de “description de fonction exhaustive”**  
   L’utilisateur fournit une description de poste pour “Araignée” et “Chouette” (agents). Nouveau besoin : définir les rôles des agents avec des job descriptions formelles.

2. **Vérification des coûts avant décision**  
   L’utilisateur insiste sur la validation des coûts réels (ex: RPi) avant de prendre une décision. Signe que les décisions précédentes étaient prises sans cette validation.

3. **Passage forcé à Codex CLI / Claude Code**  
   L’utilisateur répond “ok” quand on lui propose de basculer sur un outil avec accès shell. Accepte de perdre le contrôle direct du terminal — signe de confiance mais aussi de dépendance.

4. **Questions sur les icônes dans le terminal**  
   “c’est quoi l’icône avant ?” — l’utilisateur découvre les icônes de modèles dans les listes (DeepSeek vs Qwen). Besoin de légende/guide visuel.

## Efficacités / inefficacités

✅ **Efficacités**
- Décision de publication avec “mets à jour maintenant sinon on va l’oublier” — prise rapide, évite la procrastination.
- Utilisation de NotebookLM pour les rapports — bon choix d’outil si bien configuré.
- Demande de vérification des coûts avant décision — prudent.

❌ **Inefficacités**
- **Balade sur une mauvaise solution** : “pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu proposes ?” — l’assistant propose sans valider le besoin réel de l’utilisateur.
- **Erreurs non diagnostiquées** : SSH, Telegram, MCP, cron — toutes ouvertes, aucune n’a été résolue dans la session.
- **Questions répétées** : les mêmes questions reviennent car les réponses ne sont pas mémorisées (pas de mise à jour de MEMORY.md ou AGENTS.md).
- **Décisions non enregistrées** : rien n’est écrit dans un fichier de décision. Tout est perdu au prochain changement de contexte.

## Ce qu’il faut garder en mémoire pour les prochaines sessions

1. **Structure critique pour les réponses** :
   - Toujours partir du besoin réel de l’utilisateur, pas d’une solution prédéfinie.
   - Quand l’utilisateur dit “vérifie d’abord”, faire un diagnostic avant d’exécuter.

2. **Documentation manquante à créer** :
   - Un guide d’installation des outils (HACS, DeepSeek-TUI, HA, OpenRouter, Qwen, Ollama).
   - Un BOARD.md ou PRIORITIES.md listant les tâches A/B/C validées.
   - Les spécifications hardware des machines (M1/M5) — notamment USB-C vs USB-A.

3. **Erreurs en cours** (à reprendre en priorité) :
   - Telegram Bot 409 Conflict — tuer l’autre instance ou changer de token.
   - SSH timeout — vérifier Tailscale et la connectivité.
   - MCP Plane Server — redémarrer et capturer le log.
   - Cron Dobby — réparer la plist (input/output error).

4. **Décisions non implémentées** :
   - Nettoyage des dossiers notebooklm_sources/.md — ne pas supprimer sans backup.
   - Retour au RPi — confirmer le devis réel.

## Recommandations

1. **Installer un fichier DECISIONS.md**  
   Chaque décision (même rapide) doit être écrite dans un fichier daté. Sinon, elle est perdue dans le flux.

2. **Corriger les erreurs bloquantes avant toute nouvelle tâche**  
   Telegram bot et SSH sont bloquants pour le flux de travail. Priorité 1.

3. **Créer un guide “Premiers pas” pour les assistants**  
   Inclure : structure des dossiers Projets, spécifications hardware, liste des outils installés, comment poser une question efficace (sans tourner autour).

4. **Réduire le nombre de modèles / outils**  
   L’utilisateur jongle entre DeepSeek (TUI + chat), Claude (Code, Desktop), Codex CLI, Ollama, OpenRouter. Trop de contexte différent → erreurs et lenteur. Limiter à 2 max pour la session.

5. **Ajouter un hook de diagnostic automatique**  
   Avant toute exécution, l’assistant doit exécuter `check_status.sh` (ou équivalent) pour vérifier que SSH, Telegram, MCP, cron sont OK. Si pas OK → stop et réparation.

6. **Documenter la procédure de purge**  
   Avant de supprimer des dossiers (notebooklm_sources), archiver dans un dossier `_archived/` et tester pendant 7 jours.

---

*Généré par Dobby* 🦉 — 2026-06-13

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 300
- Résolus automatiquement : 59
- Résolus manuellement : 0
- Encore ouverts : 241
- **Taux : 19.7%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 194.1
- Échanges/session début fenêtre : 74.4
- Tendance globale : 160.9%
- Tendance 3j-3j : 443.5%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] DeepSeek-TUI/CodeWhale confirmé comme client MCP natif + serveur MCP pour extension des capacités d'agent
- [Decision] Claude Code et Codex CLI réservés aux déploiements avec accès shell complet
- [Decision] M1 comme machine de développement primaire, M5 en mode production/portabilité
- [Decision] A : attendre (risque faible, pas urgent)
- [Decision] B : faire immédiatement (valider les paramètres, lancer)
- [Decision] C : traiter en processing (batch, automation)
- [Decision] Application directe sur la caméra WildNexus et paramètres Home Assistant
- [Decision] Clé API Anthropic : fonctionnelle sur M1
- [Decision] Ventilateur actif + officiel : ajoutés au panier
- [Decision] Références Mouser importées (rupture documentaire comblée : avant = recherche manuelle, maintenant = import automatisé)
- [Decision] `travels/pka_decouvertes` : focus principal
- [Decision] WildNexus : caméra IoT (challenges réseau à adresser)
- [Decision] Home Assistant : intégration HACS pour centralisation Sonoff + autres
- [Decision] Architecture multi-outils stabilisée
- [Decision] Stratégie de priorisation triple (A/B/C)
- [Decision] Projets de travail définis
- [Decision] Décidé d’utiliser NotebookLM pour créer les rapports de ces trois projets. **Mais** la décision a été prise sans valider l’accessibilité des données s
- [Decision] Validé après vérification des coûts réels. Question : les coûts ont-ils été réellement vérifiés ou juste supposés ? Le transcript ne montre pas de con
- [Decision] “le A on va attendre, le B on fait et le C processer” — décision claire mais non documentée dans un fichier quelconque (ex: PRIORITIES.md ou BOARD.md)
- [Decision] “on va les éliminer. vérifie où ils sont” — décision de purge prise sans vérification préalable de l’impact sur les projets.
- [Decision] NotebookLM pour les rapports wildnexus, iot et travels
- [Decision] Nettoyage des dossiers notebooklm_sources et .md
- [Failure] Annotation manquante pour les logs détaillés
- [Failure] Déploiement GitHub Pages bloqué, solution non documentée
- [Failure] Connect timeout 17s relevé mais pas d'action de remédiation
- [Failure] Lien entre local-server-2 et architecture Cloud flou
- [Failure] `/getUpdates` retourne erreur sans handler d'erreur enregistré
- [Failure] Traceback complet dans `decouvertes-collector/venv`
- [Failure] Bloque la collecte de données en temps réel
- [Failure] "Starting directory (cwd) /Users/jchavauxm5/..." — chemins manquants ou mal résolus
- [Failure] Blocage de l'exécution VSCode/Cursor sur M1
- [Failure] Pages build & deployment : failure en 25s
- [Failure] SSH timeout lors de déploiement
- [Failure] Telegram Bot API — 409 Conflict
- [Failure] Terminal launch failure
- [Failure] L’updater Telegram retourne 409 Conflict (conflit de session). Le bot est probablement déjà actif ailleurs. **Bloquant** pour le collector de découver
- [Failure] `failed to connect` — pas de détail, pas de diagnostic. L’agent MCP plane est hors ligne.
- [Failure] `Bootstrap failed: 5: Input/output error` — le cron/launchd de la rétrospective automatique ne démarre pas. Cause : permissions ou fichier plist corro
- [Failure] “j’ai trouvé ceci Arducam IMX500 AI Camera Module for ESP32-P4... c’est de ça” — pas de validation que le composant est compatible avec le besoin réel
- [Failure] Erreur SSH persistante
- [Failure] Erreur Telegram Bot — 409 Conflict
- [Failure] Erreur MCP Plane Server
- [Failure] Déploiement du cron Dobby
- [Failure] Recherche infructueuse Arducam IMX500

### Fréquence des patterns (14 jours)
- **Decision** : 7 jours, 353 occurrences
- **Failure** : 7 jours, 361 occurrences
- **Question** : 7 jours, 321 occurrences
- **Recurring question** : 7 jours, 180 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (7x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Question] (7x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (7x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (7x) quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible
- [Question] (7x) ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces
- [Question] (7x) verifie d'abord pourquoi il n'a pas été regeneré
- [Decision] (6x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (6x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Failure] (6x) /LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running
- [Failure] (6x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Failure] (6x) build	pages build and deployment / buildFailed in 25 secondsannotations for page
- [Failure] (6x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (6x) done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelinsjchav
- [Failure] (6x) failed to connect
- [Question] (6x) e ce soit toi qui envoie les commandes. comment faire pour que cette instruction

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI**
- [ ] Documenter : **ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode**
- [ ] Documenter : **ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?**
- [ ] Documenter : **quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible**
- [ ] Documenter : **ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces**
- [ ] Documenter : **verifie d'abord pourquoi il n'a pas été regeneré**
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **foramnce par exemple de 3% cela ne vaut pas la peine**
- [ ] Documenter : **/LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running**
- [ ] Documenter : **What's next:    Debug this container error with Gordon → docker ai "help me fix **
- [ ] Documenter : **build	pages build and deployment / buildFailed in 25 secondsannotations for page**
- [ ] Documenter : **chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error**
- [ ] Documenter : **done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelinsjchav**
- [ ] Documenter : **failed to connect**
- [ ] Documenter : **e ce soit toi qui envoie les commandes. comment faire pour que cette instruction**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 44
- Jours d'observation : 7
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**96** recommandations au total — **96** ouvertes — **0** en cours — **0** terminées

⚠️ 13 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 78
- **Forge** : 14
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=82] (2026-06-13) **Forge** : Créer `VANLIFE.md`** : guide déploiement offline-first, M5 sync strategy, Tailsc
- [id=83] (2026-06-13) **Dobby** : Citation : "n van avec mon M5, je perds cet outil
- [id=84] (2026-06-13) **Dobby** : Fixer Telegram Bot
- [id=85] (2026-06-13) **Dobby** : Diagnose: `curl https://api.telegram.org/bot{TOKEN}/getMe`
- [id=86] (2026-06-13) **Dobby** : Implémenter handler d'erreur systématique

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**
