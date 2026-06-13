---
date: 2026-06-12
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 7
echanges: 1359
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-12

**Sessions analysées :** 7 | **Échanges :** 1359 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective des sessions — 2026-06-12

## Décisions prises

| Décision | Contexte |
|---|---|
| Éliminer les dossiers `notebooklm_ources` et `md` | JCH demande explicitement de vérifier où ils se trouvent et de les supprimer. Pas de justification partagée. |
| Valider les paramètres capteurs IoT van avec les besoins | Décision prise lors d’une session de matching entre capteurs disponibles et besoins van. Non tracée dans un ADR. |
| Reporter la génération du rapport (attente) | L’utilisateur dit « non on va attendre » sans préciser le déclencheur. |
| Utiliser NotebookLM pour créer les rapports WildNexus, IoT et Travels | Décision d’outillage : JCH demande de mettre à jour la documentation associée. |
| Faire le point sur la caméra WildNexus | Session dédiée : résumé de challenge, évaluation de l’Arducam IMX500. |
| Ne pas optimiser une performance de 3% | JCH : « une amélioration de 3% cela ne vaut pas la peine » — principe de pragmatisme posé. |
| Profils Débutant/Confirmé avec budgets 3 750€ / 5 800€ | Données utilisées pour un projet (probablement IoT Van). Non documenté formellement. |

**Problème** : Aucune décision n’est enregistrée dans `02_DECISIONS/ADR`. Elles restent dispersées dans les échanges.

---

## Échecs ouverts / bloqueurs

1. **Crash du script de check graph Ollama**  
   - Traceback : `File ".../scripts/decouvertes-collector/venv/lib/python3.13/site-packages/anthropic/...`  
   - JCH : « on a crashe dans le dernier boulot : check graphy complet utilisant ol[lamma] »  
   - Cause : non déterminée. Pas de reprise documentée.

2. **Échec de lancement du cron `com.dobby.retro.plist`**  
   - `Load failed: 5: Input/output error`  
   - Solution proposée (`launchctl bootstrap`) non exécutée. Toujours bloqué.

3. **Erreur de parsing de port distant**  
   - `[16:24:26.399] Failed to parse remote port from server output`  
   - Connexion bloquée entre outils (DeepSeek TUI / Codex CLI ?). Pas de résolution.

4. **Problème d’accès fichiers / quotes**  
   - JCH : « `quote> cquote> c'est quoi ces quote et pourquoi l'acces fichihers impossible` »  
   - Probablement un artéfact de terminal (copier-coller cassé). Non résolu.

5. **Arducam IMX500 non intégrée**  
   - JCH trouve le module mais ne confirme pas son utilisation. Aucune décision d’achat ou d’intégration.

---

## Questions récurrentes (signe de lacune documentaire)

- « Comment faire pour que cette instruction ne soit jamais oubliée quel que soit le modèle ? »  
  → Absence de mécanisme de persistance des consignes entre outils (Claude Code, DeepSeek TUI, Codex CLI).

- « Pourquoi maintenant tu as les ref Mouser et avant pas m’obligeant à chercher manuellement ? »  
  → Incohérence dans la fourniture de références composants. Pas de processus standard pour les BOM.

- « C’est quoi ces quote et pourquoi l’accès fichiers impossible ? »  
  → Symptôme d’un problème d’encodage ou de doublon de quotes dans les prompts. Non documenté dans `docs/troubleshooting`.

- « Pourquoi en 2 tu parles de USB-A, le Mac a des USB-C ? »  
  → Connaissance du matériel non partagée dans `CLAUDE.md` / `AGENTS.md`. Chaque assistant doit deviner.

- « Continue, je ne vois pas de Qwen 3.7 et c’est quoi l’icône avant ? »  
  → Interface utilisateur non homogène entre outils. Manque d’un guide UI commun.

---

## Nouveaux patterns détectés

1. **Utilisation de NotebookLM comme générateur de rapports**  
   JCH délègue la synthèse de plusieurs projets à NotebookLM plutôt qu’à un assistant. Cela montre une perte de confiance dans la capacité des LLM à produire des rapports consolidés.

2. **Demande de classement de fichiers par ordre d’intérêt**  
   « fichiers en ordre d’interet et explique pourquoi » → besoin de priorisation automatique, pas encore satisfait.

3. **Transfert de commandes entre outils**  
   JCH demande à Forge de préparer un bloc de commandes pour Cursor/Codex CLI. C’est redondant : un seul outil pourrait exécuter directement.

4. **Questionnement philosophique hors contexte**  
   « c’est quoi la peur pour toi ? » → dérive attentionnelle. Risque de dilution des sessions.

5. **Besoin de déploiement cron avec script shell**  
   Tentative de mise en place d’un `com.dobby.retro.plist` mais échoué. Pattern : l’utilisateur veut automatiser sans maîtriser `launchctl`.

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Pragmatisme sur les gains faibles** : JCH refuse d’investir du temps pour 3% de perf.
- **Utilisation de Mouser BOM** : bonne pratique pour les achats de composants.
- **NotebookLM pour les rapports** : évite de surcharger les LLM avec des contextes longs.

### ❌ Inefficacités
- **Multiplex outil coûteux** : alterner entre DeepSeek TUI, Claude Code, Codex CLI génère des incohérences (ref Mouser, comportement UI). Perte de temps à recadrer.
- **Questions redondantes non résolues** : le problème des « quotes » revient 3 fois sans solution.
- **Crash non investigué** : le check graph Ollama a planté, personne n’a analysé le stacktrace après coup.
- **Absence d’ADR** : les décisions importantes (élimination de dossiers, validation capteurs, profils budgets) ne sont pas tracées.
- **Documentation insuffisante sur la persistance des instructions** : JCH doit répéter ses demandes.

---

## Ce qu’il faut garder en mémoire pour les prochaines sessions

- **Les dossiers `notebooklm_ources` et `md` doivent être supprimés.** Attention à leur localisation exacte.
- **Cron planifié pour Dobby Retro** : `com.dobby.retro.plist` doit être corrigé via `launchctl bootstrap` et testé.
- **Caméra WildNexus** : évaluer l’Arducam IMX500, décider achat ou non.
- **Instructions persistantes** : définir un mécanisme (fichier `CONSIGNES.md` ou section spéciale dans `AGENTS.md`) pour que chaque assistant les lise au démarrage.
- **Pas d’optimisation sous 5%** : principe « 3% ne vaut pas la peine » à étendre à 5%.
- **Check graph Ollama** :

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 300
- Résolus automatiquement : 65
- Résolus manuellement : 0
- Encore ouverts : 235
- **Taux : 21.7%**

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

- [Decision] : "on va attendre" / "non on va le passer dans notebook
- [Decision] Décision de reporter l'action sur la caméra pour en faire d'abord le point
- [Decision] : "on va valider les parametres indiqués du moment qu'on puisse ne c[ensuite]
- [Decision] Approche minimaliste : valider juste ce qui permet de continuer
- [Decision] : achat "de l'officiel et aussi le ventilateur actif
- [Decision] Montage matériel confirmé mais contexte imprécis
- [Decision] Utilisation de **Codex CLI** ou **Claude Code** pour déploiements shell (plutôt que copy-paste)
- [Decision] DeepSeek-TUI (CodeWhale) intégré comme client/serveur MCP natif
- [Decision] Ollama comme runtime local
- [Decision] Attendre avant d'intégrer la caméra WildNexus** : "on va attendre" / "non on va le passer dans notebook
- [Decision] Validation paramètres en mode passif** : "on va valider les parametres indiqués du moment qu'on puisse ne c[ensuite]
- [Decision] Matériel informatique acquis** : achat "de l'officiel et aussi le ventilateur actif
- [Decision] Architecture CLI confirmée** :
- [Decision] : Aucune décision n’est enregistrée dans `02_DECISIONS/ADR`. Elles restent dispersées dans les échanges.
- [Failure] Gestion de clés API compromise** : "il y a un nouveau message telegram. je vais changer la cle
- [Failure] Clé potentiellement exposée, rotation manuelle en cours
- [Failure] ⚠️ Pas de processus automatisé de rotation, pas de vault clarifié
- [Failure] Accès fichiers bloqué (VPN + iPad)** : "veux l'installer sur mon ipad mais cela ne fonctionne pas. le vpn est connect (tailscale) et je soupconne que 
- [Failure] Installation Arduino CLI sur iPad échouée
- [Failure] Suspect : conflit Tailscale ou restriction DNS
- [Failure] Statut** : non résolu
- [Failure] Traceback : `File ".../scripts/decouvertes-collector/venv/lib/python3.13/site-packages/anthropic/...`
- [Failure] JCH : « on a crashe dans le dernier boulot : check graphy complet utilisant ol[lamma] »
- [Failure] Cause : non déterminée. Pas de reprise documentée.
- [Failure] `Load failed: 5: Input/output error`
- [Failure] Solution proposée (`launchctl bootstrap`) non exécutée. Toujours bloqué.
- [Failure] `[16:24:26.399] Failed to parse remote port from server output`
- [Failure] Connexion bloquée entre outils (DeepSeek TUI / Codex CLI ?). Pas de résolution.
- [Failure] JCH : « `quote> cquote> c'est quoi ces quote et pourquoi l'acces fichihers impossible` »
- [Failure] Probablement un artéfact de terminal (copier-coller cassé). Non résolu.
- [Failure] JCH trouve le module mais ne confirme pas son utilisation. Aucune décision d’achat ou d’intégration.
- [Failure] Crash du script de check graph Ollama
- [Failure] Échec de lancement du cron `com.dobby.retro.plist`
- [Failure] Erreur de parsing de port distant
- [Failure] Problème d’accès fichiers / quotes
- [Failure] Arducam IMX500 non intégrée

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 313 occurrences
- **Failure** : 6 jours, 321 occurrences
- **Question** : 6 jours, 289 occurrences
- **Recurring question** : 6 jours, 160 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (6x) OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI
- [Question] (6x) ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode
- [Question] (6x) e ce soit toi qui envoie les commandes. comment faire pour que cette instruction
- [Question] (6x) ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez qu
- [Question] (6x) ontinue , je ne vois pas de Qwen 3.7 et c'est quoi l'icone avant ?
- [Question] (6x) quote> cquote>  c'est quoi ces quote et pourquoi l'acces fichihers impossible
- [Question] (6x) ravaillerquote> ?       quote> cquote>  c'est quoi ces quote et pourquoi l'acces
- [Question] (6x) verifie d'abord pourquoi il n'a pas été regeneré
- [Decision] (5x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (5x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Failure] (5x) /LaunchAgents/com.dobby.retro.plistLoad failed: 5: Input/output errorTry running
- [Failure] (5x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Failure] (5x) build	pages build and deployment / buildFailed in 25 secondsannotations for page
- [Failure] (5x) chAgents/com.dobby.retro.plistBootstrap failed: 5: Input/output error
- [Failure] (5x) d strict checking.Host key verification failed.jchavauxm5@mac ~ %

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **OAuth error: Failed to save API key to macOS Keychain (security: SecKeychainI**
- [ ] Documenter : **ax via openrouter. et j'aimerais savoir comment lancer qwen a partir du vscode**
- [ ] Documenter : **e ce soit toi qui envoie les commandes. comment faire pour que cette instruction**
- [ ] Documenter : **ok parfait. derniere questions comment faire en sorte que l'html s'ouvre chez qu**
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
- [ ] Documenter : **d strict checking.Host key verification failed.jchavauxm5@mac ~ %**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 36
- Jours d'observation : 6
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**81** recommandations au total — **81** ouvertes — **0** en cours — **0** terminées

### Répartition par assigné

- **Dobby** : 65
- **Forge** : 12
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=75] (2026-06-12) **Dobby** : 1. **Diagnostic iPad + Tailscale
- [id=76] (2026-06-12) **Dobby** : SSH into iPad via Tailscale → tester `curl localhost:11434` (Ollama)
- [id=77] (2026-06-12) **Dobby** : Vérifier DNS settings Tailscale
- [id=78] (2026-06-12) **Dobby** : Créer ticket diagnostic complet avant prochaine session
- [id=79] (2026-06-12) **Dobby** : Bloquer fichiers équipe

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.0 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.0**
