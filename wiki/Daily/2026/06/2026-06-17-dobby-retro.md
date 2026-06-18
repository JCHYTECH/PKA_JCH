---
date: 2026-06-17
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1125
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-17

**Sessions analysées :** 3 | **Échanges :** 1125 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective PKA — Sessions 2026-06-17

## Décisions prises

- **Retour au RPi comme plateforme centrale** : JCH a validé le choix RPi après vérification des coûts réels. Abandon du M1 comme routeur principal.
- **Passage sur DeepSeek-V4** : La clé Anthropic fonctionne mais JCH décide de basculer sur le M1 avec DeepSeek-V4 pour la session en cours.
- **Validation des paramètres** : Décision de valider les paramètres indiqués "du moment qu'on puisse ne c" — tronqué, mais semble être une validation sous condition de faisabilité.
- **Utilisation de HA + dongle Zigbee** : JCH a arrêté le M5 et validé l'utilisation de Home Assistant avec un dongle Zigbee comme hub central.
- **Cigogne comme planificateur** : Adoption de l'assistant "Cigogne 🦩" pour le voyage Baie de Somme, après validation de la fiche.
- **Standby sur plusieurs sujets** : "on va attendre" — décision de différer plusieurs actions non priorisées.

## Échecs ouverts / bloqueurs

- **Erreur d'exécution terminal** : `The terminal process failed to launch: Starting directory (cwd) "/Users/jchavauxm5/PK..."` — chemin tronqué, problème récurrent de lancement de terminal.
- **Erreur Telegram non gérée** : `"No error handlers are registered, logging exception."` sur `telegram.ext._updater` — erreur non rattrapée dans le collector de découvertes.
- **Échec de parsing modèle** : `m['name'] for m in d.get('models',[])` — ligne de commande invalide, erreur de syntaxe dans une requête Python one-liner.
- **Blocage VPN iPad** : Le VPN Tailscale est connecté mais ne fonctionne pas sur iPad — suspicion que l'appareil bloque le trafic.
- **Erreur d'importation Ollama** : Le modèle `gemma3:12b-it-qat` a un problème de parent model path (`/Users/pdevine/.ollama/models/...`) — path utilisateur incorrect.
- **WildNexus non résolu** : JCH demande de trouver des failles dans WildNexus, mais la demande n'a pas été satisfaite — échec ouvert sur l'audit de sécurité.

## Questions récurrentes (signe de lacune documentaire)

- **Pourquoi ne proposez-vous pas de mettre dans les dossiers projets respectifs ?** — posée 2 fois. Indique un manque de processus de classification documentaire.
- **Pourquoi les refs Mouser ne sont-elles pas disponibles sans chercher manuellement ?** — posée 2 fois. JCH attend un accès automatisé aux BOM Mouser. Il a dû faire une recherche manuelle.
- **"Comment faire pour que tu aies accès à Notes Apple ?"** — posée 2 fois. JCH utilise Notes comme base de connaissance, mais aucun pont n'existe.
- **"Pourquoi c'est exclusif Claude ?"** — posée 2 fois. JCH demande pourquoi DeepSeek-TUI (CodeWhale) est lié à Claude et pas à d'autres LLMs.
- **"Comment faire pour maintenir l'outil quand je perds mon M5 dans le van ?"** — posée 2 fois. Préoccupation de portabilité des outils entre machines mobiles.

## Nouveaux patterns détectés

- **Pattern "Approve one"** : JCH dit systématiquement "approuve one" pour les approbations — demande d'automatisation des approbations en une seule commande.
- **Pattern "Validation conditionnelle"** : JCH valide des paramètres "du moment qu'on puisse" — signature d'une validation sous réserve de faisabilité, jamais pleinement documentée.
- **Pattern "Cigogne planificateur"** : JCH a validé un assistant spécifique pour un voyage, mais ne l'a pas intégré dans le workflow standard — pattern d'adoption d'agents spécialisés.
- **Pattern "M5 → M1 → RPi loops"** : JCH change de machine en cours de session, désorientant l'assistant — demande une stabilisation de la plateforme cible.
- **Pattern "Erreur d'importation Ollama"** : Le modèle `gemma3` a un problème de path utilisateur sur M1 — signe que les modèles ne sont pas correctement isolés.

## Efficacités / inefficacités

### Efficacités
- **Décision rapide sur la plateforme** : JCH a validé le RPi comme routeur en moins de 3 échanges — bonne réactivité.
- **Adoption de Cigogne** : Le planificateur de voyage a été validé et adopté — outil opérationnel immédiat.
- **Tests Telegram fonctionnels** : Le bot Telegram a été testé avec succès (HTTP 409 mais logique métier OK).

### Inefficacités
- **Perte de contexte machine** : JCH alterne entre M1, M5, RPi sans informer l'assistant — chaque changement nécessite une re-découverte.
- **Error handlers non installés** : Le collector de découvertes n'a pas de gestion d'erreur → crash non récupéré.
- **Choix de modèle non documenté** : JCH passe de Anthropic à DeepSeek-V4 sans raison explicite dans le transcript — non traçable.
- **Validation sous condition** : "du moment qu'on puisse ne c" est une validation partielle, jamais finalisée → risque de reprise.
- **Demande non satisfaite** : "Trouve des failles dans WildNexus" n'a pas abouti → consomme du temps sans résultat.

## Ce qu'il faut garder en mémoire pour les prochaines sessions

1. **Plateforme cible** : Le RPi est maintenant la plateforme centrale validée pour le routeur. Ne pas proposer M1/M5 sauf si JCH le demande.
2. **Clé API** : La clé Anthropic fonctionne, mais JCH préfère DeepSeek-V4 sur M1. Stocker les deux configurations.
3. **BOM Mouser** : JCH veut un accès automatisé aux listes Mouser sans chercher manuellement. Implémenter un endpoint MCP pour Mouser BOM.
4. **Notes Apple** : JCH veut que les assistants aient accès aux Notes Apple — demander une API ou un export automatique.
5. **Error handlers** : Le collector de découvertes Telegram doit avoir des `error handlers` installés. Problème déjà connu.
6. **Portabilité** : Quand JCH perd son M5, il veut maintenir l'outil — prévoir un script de synchronisation entre M5 et M1.
7. **Machine switch** : JCH change de machine sans prévenir — ajouter une commande `/switch` dans le protocole.

## Recommandations

**Immédiates :**
1. **Installer les error handlers** sur le collector Telegram — l'erreur `No error handlers are registered` est critique et bloque le déploiement.
2. **Corriger le path Ollama** : Le modèle `gemma3` pointe vers `/Users/pdevine` — supprimer et re-télécharger en local.
3. **Finaliser la validation RPi** : Documenter dans `MEMORY.md` que le RPi est la plateforme cible validée, avec coûts réels.

**Court terme :**
4. **Automatiser les BOM Mouser** : Créer un endpoint MCP `mouser-bom` qui prend une liste de refs et retourne les prix/disponibilités sans recherche manuelle.
5. **Accès Notes Apple** : Créer un pont MCP vers Notes via AppleScript ou API — JCH le demande deux fois.
6. **Simplifier les approbations** : Ajouter une commande `approve all` pour éviter de dire "approve one" à chaque fois.
7. **WildNexus** : Terminer l'audit de failles — échec ouvert. Planifier une session de 30 min.

**Moyen terme :**
8. **Stabiliser le M5** : Si JCH utilise le M5 dans le van, prévoir une sauvegarde automatique vers M1 — la peur de "perdre l'outil" est récurrente.
9. **Documenter les décisions** : Toutes les validations sous condition sont des décisions à 80 % — ajouter une étape de confirmation explicite dans le workflow.
10. **Standardiser les agents** : Cigogne planificateur a été adopté — le pattern "adoption d'agent spécialisé" doit être documenté pour éviter la fragmentation.

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 418
- Résolus automatiquement : 136
- Résolus manuellement : 0
- Encore ouverts : 282
- **Taux : 32.5%**

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

- [Decision] M0 EPS** : Achat du composant fourni par EPS (moq=10 chez meramake rejeté)
- [Decision] Stratégie A/B/C** : A=attendre, B=faire, C=processer (triage par priorité)
- [Decision] Changement clé Telegram** : Nouvelle clé en cours de déploiement (conflit HTTP 409 détecté)
- [Decision] Achat officiel + ventilateur actif** : Commande approuvée pour M5
- [Decision] Travel PKA Découvertes** : Activation du flux `travels/pka/decouvertes` pour collecte de messages
- [Decision] Retour au RPi comme plateforme centrale** : JCH a validé le choix RPi après vérification des coûts réels. Abandon du M1 comme routeur principal.
- [Decision] Passage sur DeepSeek-V4** : La clé Anthropic fonctionne mais JCH décide de basculer sur le M1 avec DeepSeek-V4 pour la session en cours.
- [Decision] Validation des paramètres** : Décision de valider les paramètres indiqués "du moment qu'on puisse ne c" — tronqué, mais semble être une validation sou
- [Decision] Utilisation de HA + dongle Zigbee** : JCH a arrêté le M5 et validé l'utilisation de Home Assistant avec un dongle Zigbee comme hub central.
- [Decision] Cigogne comme planificateur** : Adoption de l'assistant "Cigogne 🦩" pour le voyage Baie de Somme, après validation de la fiche.
- [Decision] Standby sur plusieurs sujets** : "on va attendre" — décision de différer plusieurs actions non priorisées.
- [Failure] Erreur : `HTTP/1.1 409 Conflict` sur getUpdates
- [Failure] Cause : Probablement ancienne clé + nouvelle clé = sessions en conflit
- [Failure] Impact** : Collecteur découvertes ne récupère plus les messages
- [Failure] Action requise** : Vérifier déploiement nouvelle clé, redémarrer service
- [Failure] VPN Tailscale connecté ✓ mais app ne se lance pas
- [Failure] Suspect : Problem de cwd ou chemins réseau
- [Failure] Bloquant** : Portabilité M5 sur iPad compromise
- [Failure] `Starting directory (cwd) "/Users/jchavauxm5/PK..."` → process launch failed
- [Failure] Impact** : Impossible lancer containers depuis terminal
- [Failure] Lié à** : Structure de paths fragile dans config
- [Failure] Telegram Bot 409 Conflict
- [Failure] iPad Installation Failure
- [Failure] Docker / Terminal cwd Crash
- [Failure] Erreur d'exécution terminal** : `The terminal process failed to launch: Starting directory (cwd) "/Users/jchavauxm5/PK..."` — chemin tronqué, problème
- [Failure] Erreur Telegram non gérée** : `"No error handlers are registered, logging exception."` sur `telegram.ext._updater` — erreur non rattrapée dans le coll
- [Failure] Échec de parsing modèle** : `m['name'] for m in d.get('models',[])` — ligne de commande invalide, erreur de syntaxe dans une requête Python one-liner.
- [Failure] Blocage VPN iPad** : Le VPN Tailscale est connecté mais ne fonctionne pas sur iPad — suspicion que l'appareil bloque le trafic.
- [Failure] Erreur d'importation Ollama** : Le modèle `gemma3:12b-it-qat` a un problème de parent model path (`/Users/pdevine/.ollama/models/...`) — path utilisat
- [Failure] WildNexus non résolu** : JCH demande de trouver des failles dans WildNexus, mais la demande n'a pas été satisfaite — échec ouvert sur l'audit de sécur

### Fréquence des patterns (14 jours)
- **Decision** : 11 jours, 513 occurrences
- **Failure** : 11 jours, 521 occurrences
- **Question** : 11 jours, 429 occurrences
- **Recurring question** : 11 jours, 258 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (10x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Failure] (10x) What's next:    Debug this container error with Gordon → docker ai "help me fix 
- [Decision] (9x) dernier point, on va matcher les besoins de capteurs iot van avec les besoins de
- [Decision] (9x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Decision] (9x) foramnce par exemple de 3% cela ne vaut pas la peine
- [Decision] (9x) je vais acheter l'officiel et aussi le ventilateur actif. pour celu
- [Decision] (9x) le A on va ttendre, le B on fait et le C processer
- [Decision] (9x) lement la clé anthropic fonctionne mais on va sur le M1
- [Decision] (9x) les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l
- [Decision] (9x) n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont
- [Decision] (9x) on va maintenant dans travels/ pka decouvertes. si j'envoie un me
- [Decision] (9x) on va valider les parametres indiqués du moment qu'on puisse ne c
- [Decision] (9x) oui on va donc retourner au choix RPI. tu as verifier les couts reels
- [Decision] (9x) our ce lieu directement ou doit il etre validé
- [Decision] (9x) tu sais comment on va sur un browser externe à vs code ?

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **What's next:    Debug this container error with Gordon → docker ai "help me fix **
- [ ] Documenter : **dernier point, on va matcher les besoins de capteurs iot van avec les besoins de**
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **foramnce par exemple de 3% cela ne vaut pas la peine**
- [ ] Documenter : **je vais acheter l'officiel et aussi le ventilateur actif. pour celu**
- [ ] Documenter : **le A on va ttendre, le B on fait et le C processer**
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**
- [ ] Documenter : **les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l**
- [ ] Documenter : **n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont**
- [ ] Documenter : **on va maintenant dans travels/ pka decouvertes. si j'envoie un me**
- [ ] Documenter : **on va valider les parametres indiqués du moment qu'on puisse ne c**
- [ ] Documenter : **oui on va donc retourner au choix RPI. tu as verifier les couts reels**
- [ ] Documenter : **our ce lieu directement ou doit il etre validé**
- [ ] Documenter : **tu sais comment on va sur un browser externe à vs code ?**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 30
- Jours d'observation : 11
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**152** recommandations au total — **152** ouvertes — **0** en cours — **0** terminées

⚠️ 37 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 124
- **Forge** : 24
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=140] (2026-06-17) **Dobby** : Telegram Bot Recovery** : Debug 409 Conflict avec nouvelle clé. Check `/getUpdat
- [id=141] (2026-06-17) **Dobby** : iPad Tailscale Debug** : SSH into M1 from iPad to confirm network path working. 
- [id=142] (2026-06-17) **Dobby** : A/B/C Triage Formalize** : Write decision-matrix in MEMORY.md with 3 examples fr
- [id=143] (2026-06-17) **Forge** : 1. **Installer les error handlers** sur le collector Telegram — l'erreur `No err
- [id=144] (2026-06-17) **Dobby** : Corriger le path Ollama** : Le modèle `gemma3` pointe vers `/Users/pdevine` — su

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.96 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.96**
