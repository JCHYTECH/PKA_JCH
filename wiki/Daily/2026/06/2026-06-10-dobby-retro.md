---
date: 2026-06-10
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 6
echanges: 1218
modeles: codex-cli, deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-10

**Sessions analysées :** 6 | **Échanges :** 1218 | **Modèles :** codex-cli, deepseek-v4, deepseek-v4-pro

---

## Décisions prises

- **Pause de travail** : "je vais dormir on reprend demain" – décision explicite de suspendre la session.
- **Utilisation de NotebookLM pour les rapports** : "les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer les rapports."
- **Suppression de répertoires** : "n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont" – décision de nettoyer des dossiers inutiles.
- **Achat matériel** : "je vais acheter l'officiel et aussi le ventilateur actif. pour celu" – engagement sur un achat.
- **Retour au choix Raspberry Pi** : "oui on va donc retourner au choix RPI. tu as verifier les couts reels" – abandon d’une autre direction pour revenir au RPI avec vérification des coûts.
- **Mise à jour d’un MacBook M1 écran cassé** : tentative de mise à jour malgré le matériel dégradé.
- **Travail sur travels/pka decouvertes** : "on va maintenant dans travels/ pka decouvertes" – focus sur un sous-projet spécifique.

## Échecs ouverts / bloqueurs

- **Échec SSH récurrent** : `Host key verification failed` et `ssh, pid=24786 ... debug1: Server host key` – le client SSH refuse la connexion, probablement à cause d’une clé inconnue ou changée.
- **Crash non résolu** : "on a crashe dans le dernier boulot : check graphy complet utilisant ol" – pas de mention de correction.
- **Build pages échoué** : `build	pages build and deployment / buildFailed in 25 seconds` – échec rapide, cause non documentée.
- **Erreur LaunchAgent** : `/LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output error` – problème de configuration du service Dobby.
- **Connexion console bloquée** : "B mais c'est toujours bloqué cote console" – service en attente.
- **Interface réseau inactive** : `media: none` sur `anpi0` – problème de connectivité physique ou virtuelle.

## Questions récurrentes (signe de lacune documentaire)

1. **Pourquoi l’assistant propose des solutions erronées et les explore longtemps ?**
   - "pourquoi on se ballade depuis des minutes sur une mauvaise solution que tu proposes ?"
2. **Pourquoi les instructions ne sont pas mémorisées entre modèles ?**
   - "comment faire pour que cette instruction ne soit jamais oubliée quelquesoit le modele ?"
3. **Pourquoi le choix du modèle est flou / pourquoi Claude semble privilégié ?**
   - "pourquoi modele clude ne premiere attention ?", "pourquoi c'est eclusif claude ?"
4. **Accès aux fichiers impossible – pourquoi des quotes apparaissent ?**
   - "c'est quoi ces quote et pourquoi l'acces fichihers impossible" (posé deux fois)
5. **Comment exposer un HTML en dehors du réseau local ?**
   - "comment faire en sorte que l'html s'ouvre chez quelqu'un d'autres hors reseau jch ?"

Ces questions montrent un **manque de documentation sur le fonctionnement multi-outils** (DeepSeek, Claude, Codex CLI) et sur les bonnes pratiques de partage de fichiers.

## Nouveaux patterns détectés

- **Utilisation de NotebookLM comme outil de génération de rapports** pour les projets WildNexus, IoT et Travels.
- **Tentatives de mise à jour de machines dégradées** (MacBook M1 écran cassé) – pattern risqué car aucune mention de sauvegarde ou précaution.
- **Vérification systématique des coûts** lors de décisions matérielles ("tu as verifier les couts reels") – signe d’une conscience budgétaire.
- **Questions de frustration répétées** ("pourquoi tu ne le fais pas") – peut indiquer un désalignement des attentes entre l’utilisateur et l’assistant.

## Efficacités / inefficacités

### Efficacités
- Décision rapide d’utiliser NotebookLM pour éviter la rédaction manuelle des rapports.
- Nettoyage de fichiers inutiles (suppression des dossiers `notebooklm_ources` et `md`).
- Retour sur une solution testée (RPI) avec vérification des coûts.

### Inefficacités
- **Exploration prolongée d’une mauvaise solution** – perte de temps sans refus précoce de l’assistant.
- **Échecs SSH non résolus** qui bloquent l’accès à des machines distantes.
- **Build pages échoué sans analyse** – pas de diagnostic ni de correction dans le transcript.
- **Erreur de lancement de Dobby** (LaunchAgent) – non corrigée, pourrait impacter les rétrospectives futures.
- **Questions récurrentes sans réponse définitive** – la documentation existante (s’il y en a) n’est pas utilisée ou est insuffisante.

## Ce qu’il faut garder en mémoire pour les prochaines sessions

1. **Le problème SSH avec les machines M1 et RPI** – la clé de l’hôte a changé ou n’est pas acceptée. Prévoir un nettoyage du `known_hosts` ou une régénération de clé.
2. **La configuration LaunchAgent de Dobby est invalide** – `com.dobby.retro.plist` ne charge pas. Corriger avant la prochaine rétrospective automatique.
3. **Les instructions multi-modèles ne persistent pas** – il faut un mémo centralisé (README dans `PKA_JCH/_docs` par exemple) qui précise le comportement attendu de chaque outil.
4. **Le build pages échoue** – vérifier les workflows GitHub Actions ou le déploiement statique.
5. **NotebookLM pour les rapports** – conserver le pattern mais documenter le processus (dossier source, format, destination).
6. **Les questions "pourquoi" récurrentes** – rédiger une FAQ courte pour y répondre directement.

## Recommandations

1. **Résoudre les échecs SSH** : exécuter `ssh-keygen -R 192.168.129.16` sur le Mac M1 et vérifier les permissions du serveur.
2. **Corriger le LaunchAgent** : éditer le plist, puis `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.dobby.retro.plist`.
3. **Documenter le workflow multi-modèle** : créer un `WORKFLOW.md` qui explique quand utiliser DeepSeek, Claude, Codex CLI, et comment les instructions sont transmises (ou non). Inclure les bonnes pratiques pour éviter les explorations inutiles.
4. **Analyser l’échec du build pages** : examiner les logs dans GitHub Pages ou l’outil de déploiement pour identifier l’erreur.
5. **Mettre en place un mémo partagé** : un fichier `_shared/INSTRUCTIONS.md` dans le dépôt PKA que tous les assistants lisent en début de session (via une instruction système).
6. **Réduire le temps d’exploration** : demander explicitement à l’assistant de signaler rapidement si une solution est douteuse et de proposer un plan B.
7. **Prévoir un temps de documentation** lors des prochaines sessions : dédier 10 minutes à répondre aux questions récurrentes et mettre à jour la base documentaire.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 361
- Résolus automatiquement : 151
- Résolus manuellement : 0
- Encore ouverts : 210
- **Taux : 41.8%**

### Évolution du volume (tendance)
- 📈 Direction : up
- Échanges/session récent : 203.0
- Échanges/session début fenêtre : 74.4
- Tendance globale : 172.8%
- Tendance 3j-3j : 134.0%

### Taux d'application implicite
- Aucune question identifiée il y a 7 jours


## 🧠 Auto-apprentissage

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] : Adoption du modèle A/B/C
- [Decision] B = faire immédiatement
- [Decision] C = traiter en arrière-plan
- [Decision] Impact* : clarification des priorités, mais pas encore documentée formellement
- [Decision] : Migration vers `travels/pka/decouvertes`
- [Decision] Centralisation des données de voyage (Baie de Somme, CoFe d'Opale, juin 2026)
- [Decision] Validation des paramètres requise avant traitement
- [Decision] : Achat officiel + ventilateur actif pour van
- [Decision] Décision prise sans documentation des spécifications techniques
- [Decision] Pas de lien établi avec la fiche IoT M5 existante
- [Decision] : Préférence assumée pour Claude/CodeX
- [Decision] Décision non explicite mais récurrente (56x mentions Claude vs alternatives)
- [Decision] Crée une dépendance organisationnelle non documentée
- [Decision] Stratégie de triage des tâches** : Adoption du modèle A/B/C
- [Decision] Architecture travels/ PKA** : Migration vers `travels/pka/decouvertes`
- [Decision] Matériel acquis** : Achat officiel + ventilateur actif pour van
- [Decision] Routage des commandes** : Préférence assumée pour Claude/CodeX
- [Decision] Pause de travail** : "je vais dormir on reprend demain" – décision explicite de suspendre la session.
- [Decision] Utilisation de NotebookLM pour les rapports** : "les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer les rapports.
- [Decision] Suppression de répertoires** : "n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont" – décision de nettoyer des dossiers in
- [Decision] Achat matériel** : "je vais acheter l'officiel et aussi le ventilateur actif. pour celu" – engagement sur un achat.
- [Decision] Retour au choix Raspberry Pi** : "oui on va donc retourner au choix RPI. tu as verifier les couts reels" – abandon d’une autre direction pour revenir 
- [Decision] Mise à jour d’un MacBook M1 écran cassé** : tentative de mise à jour malgré le matériel dégradé.
- [Decision] Travail sur travels/pka decouvertes** : "on va maintenant dans travels/ pka decouvertes" – focus sur un sous-projet spécifique.
- [Failure] Pages deployment failure** (25 secondes) : erreur d'accès généralisée
- [Failure] Keychain OAuth** : `Failed to save API key to macOS Keychain (security: SecKeychainI...)`
- [Failure] LaunchAgent boot failure** : `/LaunchAgents/com.dobby.retro.plist` → "Load failed: 5: Input/output error
- [Failure] Docker port mapping** : `Failed to parse remote port from server output [16:24:26.399]`
- [Failure] Échec SSH récurrent** : `Host key verification failed` et `ssh, pid=24786 ... debug1: Server host key` – le client SSH refuse la connexion, probableme
- [Failure] Crash non résolu** : "on a crashe dans le dernier boulot : check graphy complet utilisant ol" – pas de mention de correction.
- [Failure] Build pages échoué** : `build	pages build and deployment / buildFailed in 25 seconds` – échec rapide, cause non documentée.
- [Failure] Erreur LaunchAgent** : `/LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output error` – problème de configuration du service Dobby.
- [Failure] Connexion console bloquée** : "B mais c'est toujours bloqué cote console" – service en attente.
- [Failure] Interface réseau inactive** : `media: none` sur `anpi0` – problème de connectivité physique ou virtuelle.

### Fréquence des patterns (14 jours)
- **Decision** : 4 jours, 241 occurrences
- **Failure** : 4 jours, 241 occurrences
- **Question** : 4 jours, 221 occurrences
- **Recurring question** : 4 jours, 120 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (4x) je vais dormir on reprend demain
- [Decision] (4x) ok maintenant on va essayer de mettre à jour un macbook m1 dont l'écran est cas
- [Failure] (4x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Failure] (4x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (4x) d strict checking.Host key verification failed.jchavauxm5@mac ~ %
- [Failure] (4x) générer du TypeScript/Vanilla CSS ou debugger tes scripts Python.   * Pour l'Ana
- [Failure] (4x) perl: warning: Setting locale failed.perl: warning: Please check that your local
- [Question] (4x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (4x) e ce soit toi qui envoie les commandes. comment faire pour que cette instruction
- [Question] (4x) ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez qu
- [Question] (4x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (4x) pourquoi modele clude ne premiere attention ?
- [Question] (4x) pourquoi tu ne le fais pas
- [Question] (4x) quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible
- [Question] (4x) ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 34
- Jours d'observation : 4
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**56** recommandations au total — **56** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 41
- **Forge** : 11
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=38] (2026-06-10) **Dobby** : Créer `TOOL_SELECTION_MATRIX.md`
- [id=39] (2026-06-10) **Dobby** : Tableau : tâche × outil optimal × raison
- [id=40] (2026-06-10) **Dobby** : Exemple : "IoT config" → ESPHome CLI / "Raisonnement complexe" → DeepSeek-v4-pro
- [id=41] (2026-06-10) **Dobby** : Intégrer en prompt system pour TOUS les modèles
- [id=42] (2026-06-10) **Dobby** : Fixer "Pourquoi c'est exclusif Claude ?"

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**
