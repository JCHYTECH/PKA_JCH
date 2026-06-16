---
date: 2026-06-14
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1177
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-14

**Sessions analysées :** 4 | **Échanges :** 1177 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective de session : 2026-06-14

## Décisions prises
- **Utilisation de NotebookLM pour les rapports** : JCH décide d'utiliser NotebookLM pour générer les rapports des projets WildNexus, IoT et Travels. Décision non documentée ailleurs que dans ce transcript.
- **Achat du ventilateur actif** : JCH valide l'achat du ventilateur actif (officiel) sans préciser le modèle exact ni le budget alloué. Décision prise en cours de session, sans lien vers une spécification technique.
- **Élimination des fichiers NotebookLM** : JCH ordonne de supprimer les fichiers `notebooklm_ources` et `notebooklm_sources.md` dans les répertoires. Décision prise sans vérification préalable de leur usage par d'autres outils.
- **Validation des paramètres** : JCH valide "les paramètres indiqués du moment qu'on puisse ne c" (phrase tronquée). Décision floue, non documentée dans un fichier de configuration.
- **Matching des besoins capteurs IoT van** : Décision prise de matcher les besoins de capteurs IoT avec les besoins du van, sans validation des spécifications techniques des capteurs.

## Échecs ouverts / bloqueurs
- **Bloqueur console** : Un assistant reste bloqué côté console (message "c'est toujours bloqué cote console"). Cause non identifiée, le transcript ne montre pas de résolution.
- **Échec installation VPN Tailscale sur iPad** : JCH ne parvient pas à installer le VPN sur son iPad (Tailscale connecté mais ne fonctionne pas). Bloqueur ouvert, pas de solution proposée.
- **Échec démarrage de Dobby** : Le LaunchAgent `com.dobby.retro.plist` échoue avec `Launchctl bootstrap` : "Input/output error". Pas de résolution, le service Dobby ne démarre pas.
- **Erreur API Telegram** : L'API Telegram renvoie une erreur 409 (Confict) pour le bot `decouvertes-collector`. Aucun gestionnaire d'erreur n'est enregistré. Exception non traitée.
- **Échec de parsing de port distant** : Le script `ssh` échoue avec "Failed to parse remote port from server output". Pas de résolution.
- **Échec de régénération de fichier** : Un fichier n'a pas été régénéré, JCH demande de "vérifier d'abord pourquoi il n'a pas été regeneré". Pas d'action corrective.

## Questions récurrentes (signe de lacune documentaire)
- **"pourquoi en 2 tu parles de usb-A, le mac a des usb-c"** : Incohérence entre les recommandations (USB-A) et le matériel réel (USB-C). Signe que les spécifications techniques du Mac ne sont pas documentées dans le projet.
- **"c'est quoi la peur pour toi ?"** : Question philosophique récurrente, non résolue. Signe d'un manque de documentation sur l'état émotionnel et les blocages psychologiques de JCH.
- **"pourquoi c'est exclusif claude ?"** : Question sur l'exclusivité de l'outil Claude. Réponse non fournie dans le transcript.
- **"fichiers en ordre d'intérêt et explique pourquoi"** : Demande récurrente de tri des fichiers. Indique un manque de documentation sur l'ordre de priorité des fichiers.
- **"vérifie d'abord pourquoi il n'a pas été regeneré"** : Demande de vérification de la non-régénération d'un fichier. Aucune procédure documentée pour la régénération.

## Nouveaux patterns détectés
- **Pattern "Décision en session unique"** : JCH prend des décisions (achat, validation) sans les documenter dans des fichiers de configuration ou des tickets. Les décisions sont perdues entre les sessions.
- **Pattern "Erreur non traitée"** : Les erreurs API (Telegram 409, SSH, LaunchCtl) sont levées mais non corrigées dans la session. Aucun gestionnaire d'erreur n'est enregistré avant la production.
- **Pattern "Question philosophique non résolue"** : Les questions sur l'émotion ("peur") sont posées mais non documentées. Aucune réponse n'est fournie.
- **Pattern "Validation sans vérification"** : JCH valide des paramètres sans vérifier leur exactitude technique (ex : "pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs").
- **Pattern "Outillage multiple non synchronisé"** : Utilisation de DeepSeek, Claude, Codex, sans synchronisation des résultats. Les sessions sont parallèles mais non coordonnées.

## Efficacités / inefficacités
- **Efficacité** : La demande de résumé ("ok bon nom") avec description de fonction est bien structurée (Missions principales → tâches). Le format est réutilisable.
- **Inefficacité majeure** : Le temps passé à débattre d'une mauvaise solution ("pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu proposes ?") avant de la rejeter. Temps perdu sans documenter la solution rejetée.
- **Inefficacité** : Le poste "m1@MBP-de-M1" exécute `curl` sur localhost pour vérifier les modèles. La commande est exécutée mais le résultat (JSON) n'est pas exploité pour la prise de décision.
- **Efficacité** : La liste d'achat Mouser (BOM) est préparée avec des instructions claires (format xls, xlsx, csv). Le processus est documenté.

## Ce qu'il faut garder en mémoire pour les prochaines sessions
- **Documenter chaque échec** : L'API Telegram 409, le DDOS de Tailscale, les erreurs SSH et LaunchCtl doivent être documentés dans un fichier `errors.md`. Ne pas repartir de zéro.
- **Fixer les décisions** : Les décisions d'achat (ventilateur, capteurs) doivent être enregistrées dans un fichier `BUDGET.md` avec les montants et les modèles.
- **Synchroniser les assistants** : Noter que les sessions DeepSeek, Claude et Codex ne sont pas synchronisées. Prévoir un canal de synchronisation (ex : fichier `LOG_SESSIONS.md`).
- **Répondre aux questions récurrentes** : Les questions sur l'USB-A vs USB-C, la peur, l'exclusivité doivent être traitées une fois pour toutes dans le wiki.
- **Vérifier les fichiers avant suppression** : Avant de supprimer `notebooklm_ources`, vérifier qu'ils ne sont pas utilisés par d'autres outils.

## Recommandations
1. **Créer un fichier `errors.md`** : Dans le répertoire `PKA_JCH/errors`, lister toutes les erreurs (Telegram, SSH, Tailscale, launchctl) avec leurs causes et solutions documentées.
2. **Utiliser un système de tickets** : Les décisions d'achat (ventilateur, capteurs) doivent être converties en tickets (ex : dans `GH_ISSUES.md` ou `TICKETS.md`).
3. **Déployer un gestionnaire d'erreur** : Avant de lancer un nouveau script, ajouter un gestionnaire d'erreur global (`ERROR_HANDLER.py`) dans le projet.
4. **Documenter le matériel** : Dans `HARDWARE.md`, lister les machines (M1, M5, iPad) avec leurs spécifications USB (type, ports) pour éviter les incohérences.
5. **Ajouter un fichier `PHILOSOPHIE.md`** : Documenter les réponses aux questions philosophiques (peur, exclusivité) pour qu'elles ne reviennent pas.
6. **Automatiser la vérification des modèles** : Le script `curl` sur localhost (modèles Ollama) doit être intégré dans un `healthcheck.sh` automatisé.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 360
- Résolus automatiquement : 94
- Résolus manuellement : 0
- Encore ouverts : 266
- **Taux : 26.1%**

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

- [Decision] : JCH décide de basculer les découvertes dans ce dossier au lieu de garder une structure disperse
- [Decision] : Décision de valider les paramètres en place sans action immédiate (mode observation)
- [Decision] : JCH valide l'achat de composants officiels + ventilateur actif pour WildNexus P0
- [Decision] : Écarter les améliorations de performance < 3% (ROI insuffisant)
- [Decision] : Ranger les fichiers par ordre d'intérêt dans les dossiers projets respectifs plutôt qu'en vrac
- [Decision] Migration vers `travels/pka-decouvertes`** : JCH décide de basculer les découvertes dans ce dossier au lieu de garder une structure disperse
- [Decision] Attente sur validation paramètres WildNexus** : Décision de valider les paramètres en place sans action immédiate (mode observation)
- [Decision] Achat équipement de monitoring** : JCH valide l'achat de composants officiels + ventilateur actif pour WildNexus P0
- [Decision] Seuil d'optimisation défini** : Écarter les améliorations de performance < 3% (ROI insuffisant)
- [Decision] Stratégie de priorisation fichiers** : Ranger les fichiers par ordre d'intérêt dans les dossiers projets respectifs plutôt qu'en vrac
- [Decision] Utilisation de NotebookLM pour les rapports** : JCH décide d'utiliser NotebookLM pour générer les rapports des projets WildNexus, IoT et Travels. Déci
- [Decision] Achat du ventilateur actif** : JCH valide l'achat du ventilateur actif (officiel) sans préciser le modèle exact ni le budget alloué. Décision prise en
- [Decision] Élimination des fichiers NotebookLM** : JCH ordonne de supprimer les fichiers `notebooklm_ources` et `notebooklm_sources.md` dans les répertoires. Déc
- [Decision] Validation des paramètres** : JCH valide "les paramètres indiqués du moment qu'on puisse ne c" (phrase tronquée). Décision floue, non documentée dans 
- [Decision] Matching des besoins capteurs IoT van** : Décision prise de matcher les besoins de capteurs IoT avec les besoins du van, sans validation des spécifica
- [Failure] Bloqueur console** : Un assistant reste bloqué côté console (message "c'est toujours bloqué cote console"). Cause non identifiée, le transcript ne mon
- [Failure] Échec installation VPN Tailscale sur iPad** : JCH ne parvient pas à installer le VPN sur son iPad (Tailscale connecté mais ne fonctionne pas). Bloqueu
- [Failure] Échec démarrage de Dobby** : Le LaunchAgent `com.dobby.retro.plist` échoue avec `Launchctl bootstrap` : "Input/output error". Pas de résolution, le se
- [Failure] Erreur API Telegram** : L'API Telegram renvoie une erreur 409 (Confict) pour le bot `decouvertes-collector`. Aucun gestionnaire d'erreur n'est enregis
- [Failure] Échec de parsing de port distant** : Le script `ssh` échoue avec "Failed to parse remote port from server output". Pas de résolution.
- [Failure] Échec de régénération de fichier** : Un fichier n'a pas été régénéré, JCH demande de "vérifier d'abord pourquoi il n'a pas été regeneré". Pas d'action

### Fréquence des patterns (14 jours)
- **Decision** : 8 jours, 393 occurrences
- **Failure** : 8 jours, 401 occurrences
- **Question** : 8 jours, 353 occurrences
- **Recurring question** : 8 jours, 200 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (8x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Question] (8x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (8x) verifie d'abord pourquoi il n'a pas été regeneré
- [Decision] (7x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (7x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Failure] (7x) /LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running
- [Failure] (7x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Failure] (7x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (7x) done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelinsjchav
- [Failure] (7x) failed to connect
- [Question] (7x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (7x) pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo
- [Question] (7x) quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible
- [Question] (7x) ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces
- [Recurring question] (7x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI**
- [ ] Documenter : **ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?**
- [ ] Documenter : **verifie d'abord pourquoi il n'a pas été regeneré**
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **foramnce par exemple de 3% cela ne vaut pas la peine**
- [ ] Documenter : **/LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running**
- [ ] Documenter : **What's next:    Debug this container error with Gordon → docker ai "help me fix **
- [ ] Documenter : **chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error**
- [ ] Documenter : **done: 0 traités, 0 skip, 0 en cours, 0 échecs, 0 purgés, 0 orphelinsjchav**
- [ ] Documenter : **failed to connect**
- [ ] Documenter : **ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode**
- [ ] Documenter : **pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu propo**
- [ ] Documenter : **quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible**
- [ ] Documenter : **ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces**
- [ ] Documenter : **ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 21
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**102** recommandations au total — **102** ouvertes — **0** en cours — **0** terminées

⚠️ 22 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 82
- **Forge** : 16
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=97] (2026-06-14) **Dobby** : Créer un fichier `errors.md`** : Dans le répertoire `PKA_JCH/errors`, lister tou
- [id=98] (2026-06-14) **Dobby** : Utiliser un système de tickets** : Les décisions d'achat (ventilateur, capteurs)
- [id=99] (2026-06-14) **Forge** : Déployer un gestionnaire d'erreur** : Avant de lancer un nouveau script, ajouter
- [id=100] (2026-06-14) **Dobby** : Documenter le matériel** : Dans `HARDWARE.md`, lister les machines (M1, M5, iPad
- [id=101] (2026-06-14) **Dobby** : Ajouter un fichier `PHILOSOPHIE.md`** : Documenter les réponses aux questions ph

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.99 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.99**
