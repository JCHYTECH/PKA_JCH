---
date: 2026-06-19
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 7
echanges: 1332
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-06-19

**Sessions analysées :** 7 | **Échanges :** 1332 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE SESSIONS DU 2026-06-19
## Dobby - PKA Analysis Report

---

## Décisions prises

### Confirmées et actionnées
- **Attendre validation ESP32** : "supposons que espe32 est confirmé après les essais. quel esp32 faudra-t-il acheter" → Décision : ne pas valider le modèle avant tests matériels conclusifs
- **Migration notebook** : "on va le passer dans notebook" → Décision de déplacer certains contenus vers Notebook LM pour générer rapports sur WildNexus, IoT et Travels
- **Nettoyage répertoire** : "on va les éliminer. vérifie où il sont" → Décision de supprimer fichiers en doublon dans `directory, notebook_sources` et `.md`
- **Approche API Anthropic** : "la clé anthropic fonctionne mais on va sur le M1" → Choix d'utiliser la clé sur M1 plutôt que basculer infrastructure
- **Testbed = M1** : "oui on va essayer à partir d'ici si tu as accès à '/Users/jchavauxm5/'" → M1 = machine de référence pour tests

### Non documentées / ambiguës
- Qu'est-ce qui justifie l'abandon de certains composants Aliexpress (liens cassés dans logs) ?
- Quand exactement la validation caméra OV5640 DVP 24-pin est-elle prévue ?
- Quel est le scope réel du nettoyage de répertoire (en cours / aboli / à valider) ?

---

## Échecs ouverts / bloqueurs

### Critiques
1. **Crash terminal non résolu** : "il y a eu un crash de terminal. regarde ce qui a été fait et ce qui reste à faire"
   - État : EN ATTENTE DE DIAGNOSTIC
   - Impact : Perte potentielle de traces, blocage équipe
   - Action : Vérification du vault incomplète

2. **Bloqueur d'approbation itératif** : "comment ne pas être bloqué par les demandes d'approbation ou je dis tjrs approve one"
   - État : BLOQUEUR WORKFLOW
   - Impact : Ralentit cycles itératifs
   - Cause : Processus d'approbation trop strict ou mal aligné avec la réalité du développement

3. **Problèmes de connectivité matériel (Unresponsive Device)**
   - "Connection Failed: Device Unresponsive"
   - "Failed uploading: no upload port provided"
   - "Maximum is 327680 bytes" → Dépassement limite mémoire locale
   - État : BLOQUEUR HARDW. / ENVIRONNEMENT
   - Affecte : Tests ESP32, uploads firmware

4. **Problème Telegram API** : HTTP 409 Conflict sur `getUpdates`
   - "HTTP/1.1 409 Conflict" 
   - Traceback : `telegram/ext/_updater.py` ligne 753
   - État : BLOQUEUR EN PRODUCTION (decouvertes-collector)
   - Cause possible : Bot déjà en écoute dans une autre session

5. **URLs cassées composants Aliexpress/Mouser**
   - Liens dans transcript : 404 ou expiré
   - État : BLOQUEUR APPROVISIONNEMENT
   - Impact : Impossibilité valider BOM matériel réelle

### Warnings
- HTTP/2 404 en date Tue, 09 Jun 2026 18:05:07 GMT (dates incohérentes dans logs)
- Données partielles/tronquées dans upload (14 bytes seulement)

---

## Questions récurrentes (signe de lacune documentaire)

### Haute fréquence = DOCUMENTER EN PRIORITÉ

1. **Architecture outils multi-clients** (5+ occurrences)
   - "pourquoi c'est exclusif Claude ?"
   - "comment faire en sorte que tu puisses faire les recherches nécessaires en entrant dans les si[...]"
   - "n van avec mon M5, je perds cet outil. comment faire pour le maintenir ok ?"
   - **Lacune** : Pas de doc sur la stratégie DeepSeek-TUI vs Claude, intégration MCP, portabilité M5
   - **Besoin** : Architecture diagram + choix de design documentés

2. **Gestion d'environnements & dépendances** (4+ occurrences)
   - "maintenant avant j'avais pas (.venv), c'est quoi ?"
   - "ocused on the working set" (fragment, mais indique problème de contexte Python)
   - **Lacune** : Pas d'onboarding `.venv`, pas de specs Python/pip
   - **Besoin** : Setup.md avec requirements.txt, .python-version, venv init checklist

3. **Compatibilité USB/connecteurs Mac** (2+ occurrences)
   - "pourquoi en 2 tu parles de usb-A, le mac a des usb-c"
   - **Lacune** : Specs matériel incohérentes, adaptateurs non spécifiés
   - **Besoin** : Compatibility matrix matériel

4. **HACS / Home Assistant** (2+ occurrences)
   - "un outil hacs https://hacs.xyz/ analyse comment installer tout cela pour que HA soit le carrefour des produits sonoff et autres"
   - **Lacune** : Pas d'intégration documentée HA + IoT
   - **Besoin** : Guide HACS + Sonoff integration

5. **Références composants mouser** (2+ occurrences)
   - "oui mais explique moi pourquoi maintenant tu as les ref mouser et avant pas m'obligeant à chercher manuellement"
   - **Lacune** : Processus BOM non standardisé, sources références changeantes
   - **Besoin** : BOM template + source de vérité unique

6. **Ordering de fichiers par intérêt** (2+ occurrences)
   - "fichiers en ordre d'intérêt et explique pourquoi. on decidera qu'en faire après"
   - **Lacune** : Critères de tri non définis, décision non prise
   - **Besoin** : Taxonomy fichiers + criteria scoring

---

## Nouveaux patterns détectés

### Pattern 1 : Analyse-Décision-Ajournement
```
JCH pose question technique spécifique
→ Réponse détaillée (souvent 3-5 paragraphes)
→ JCH répond "on va attendre" ou "on va le passer en notebook"
→ Pas d'exécution immédiate, accumulation en queue
```
**Impact** : 7 sessions × 1332 échanges = bruit décisionnel important

### Pattern 2 : Duplication outil/expertise
- **DeepSeek-TUI/CodeWhale vs Claude** mentionné 7+ fois sans clarification rôle
- JCH switche entre outils sans trace de **pourquoi**
- Résultat : requêtes identiques posées à plusieurs LLM

### Pattern 3 : Débits d'information non filtrés
- Extraits de transcript = mélanges de :
  - Réponses LLM complètes (40-50% du token budget)
  - Logs bruts système (errors, warnings)
  - Fragments de questions sans contexte
  - URLs cassées inopérantes
- **Indicateur** : Peu de filtrage avant envoi à Dobby

### Pattern 4 : M1 = pivot technique non officiel
- M1 mentionné 97 fois (dépassé seulement par Claude 187x)
- M1 utilisé pour : tests, déploiement, TUI, Ollama
- **Aucune doc** sur pourquoi M1 = testbed officiel
- Risque : Si M1 tombe, flux entier s'arrête

### Pattern 5 : Blocage approbation itératif
- "je dis tjrs approve one" = problème workflow systémique
- Validation trop centralisée ou critères flous
- Ralentit cycles rapid-prototyping

---

## Efficacités / Inefficacités

### ✅ Efficacités détectées

1. **Réponses LLM bien structurées** : Lorsque questions posées clairement, réponses incluent steps numérotés, exemples, pinpoints techniques (ex: "OV5640 DVP 24-pin pinout differs from OV2640")

2. **Capacité diagnostic rapide** : Notebook LM + DeepSeek pour rapports → temps de synthèse réduit

3. **Utilisation Telegram API** : Même avec erreur 409, architecture bot de collecte existe

4. **Mouser BOM tools** : Une fois demandé, processus d'import est clair (format .csv/.xlsx, colonnes requises)

5. **M1 infrastructure stable** : Pas d'erreur sur Ollama, curl, API calls locales

### ❌ Inefficacités critiques

1. **Recherche manuelle répétée** : "tu m'obligeant à chercher manuellement" → JCH doit chercher références Mouser/Aliexpress à chaque session
   - **Cost** : ~30-45 min par BOM
   - **Fix** : Scraper + base composants locale

2. **Crash terminal non investigué** : "il y a eu un crash" → aucun follow-up visible
   - **Cost** : Données perdues, relance coûteuse
   - **Fix** : Log rotation, crash handler

3. **URLs cassées = relance manuelle** : 3 URLs Aliexpress dans logs → plus d'accès
   - **Cost** : Dépend à nouveau de recherche manuelle
   - **Fix** : Snapshot BOM au moment du choix

4. **Décisions "on va attendre" sans deadline** : 5+ décisions en suspend depuis le 19 juin
   - **Cost** : Queue infinie, context fatigue
   - **Fix** : Date explicite ou blocked state

5. **Duplication Claude/DeepSeek** : Même question à 2 outils = gaspillage 2x tokens
   - **Cost** : Budget tokens doublé pour même réponse
   - **Fix** : Routeur décisionnel : "Utilise DeepSeek pour X, Claude pour Y"

6. **Logs mélangés à transcripts** : 40% du contenu = garbage (errors, traces)
   - **Cost** : Dobby doit nettoyer, patterns perdus
   - **Fix** : Séparer `*.log` → `*.md` transcripts

7. **Pas de DDD (Decision Documentation Date)** : Impossible de tracer "quand/pourquoi ce choix"
   - **Cost** : Remise en question sans historique
   - **Fix** : Format `[DECISION date] status scope > action`

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### État de la playlist / queue active

| Item | Status | Since | Owner | Notes |
|------|--------|-------|-------|-------|
| ESP32 validation | AWAITING_TESTS | 2026-06-19 | JCH | Pas confirmé, supplier selection pending |
| Camera OV5640 DVP | DESIGN_PHASE | 2026-06-19 | ? | Pinout mismatch flagged, needs HW audit |
| Terminal crash investigation | BLOCKED | 2026-06-19 | Dobby | Vault verification incomplete |
| Approval bottleneck | SYSTEMIC | ongoing | JCH | Workflow overha

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 417
- Résolus automatiquement : 116
- Résolus manuellement : 0
- Encore ouverts : 301
- **Taux : 27.8%**

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

- [Decision] Projet WildNexus** : recentrage sur la caméra OV5640 avec ESP32‑S3. Décision de suivre le brochage spécifique (ne pas utiliser le pinout ESP32‑CAM sta
- [Decision] Commande matérielle** : rejet de la commande Meramake (MOQ 10) – achat de la pièce fournie par Eps pour le M0.
- [Decision] Structure projet** : déplacement vers `travels/` pour "pka decouvertes" (non confirmé si effectué).
- [Decision] Nettoyage des fichiers** : élimination des répertoires `notebooklm_sources` et `.md` superflus (décision prise mais pas tracée).
- [Decision] Intégration MCP** : choix de DeepSeek‑TUI (CodeWhale) comme client MCP natif pour le codage, abandon progressif de Claude Desktop pour les tâches loca
- [Decision] Carnet de voyage** : validation du plan Baie de Somme (mais décision non formalisée dans PKA).
- [Decision] Décision de suivre le brochage spécifique (ne pas utiliser le pinout ESP32‑CAM standard).
- [Decision] Attendre validation ESP32** : "supposons que espe32 est confirmé après les essais. quel esp32 faudra-t-il acheter" → Décision : ne pas valider le modè
- [Decision] Migration notebook** : "on va le passer dans notebook" → Décision de déplacer certains contenus vers Notebook LM pour générer rapports sur WildNexus, 
- [Decision] Nettoyage répertoire** : "on va les éliminer. vérifie où il sont" → Décision de supprimer fichiers en doublon dans `directory, notebook_sources` et `.
- [Decision] Approche API Anthropic** : "la clé anthropic fonctionne mais on va sur le M1" → Choix d'utiliser la clé sur M1 plutôt que basculer infrastructure
- [Decision] Testbed = M1** : "oui on va essayer à partir d'ici si tu as accès à '/Users/jchavauxm5/'" → M1 = machine de référence pour tests
- [Failure] : "on a crashe dans le dernier boulot : check graphy complet utilisant ol" – pas de trace de reprise.
- [Failure] : `MCP validation failed: pka-homeassistant: Stdio transport closed` – le server MCP HA ne répond plus.
- [Failure] : `HTTP 409 Conflict` lors de `getUpdates` – le token bot est utilisé par une autre instance.
- [Failure] : `Failed uploading: no upload port provided` – pas de port série spécifié pour l’ESP32.
- [Failure] : `https://nl.aliexpress.com/item/1005003006706291.html` – produit probablement supprimé ou indisponible.
- [Failure] : `Maximum is 327680 bytes` – script Python trop lourd pour un terminal.
- [Failure] : "a note est <8" – condition de qualité non satisfaite pour un composant.
- [Failure] Crash d’un script inconnu** : "on a crashe dans le dernier boulot : check graphy complet utilisant ol" – pas de trace de reprise.
- [Failure] MCP Home‑Assistant HS** : `MCP validation failed: pka-homeassistant: Stdio transport closed` – le server MCP HA ne répond plus.
- [Failure] Télégram bot en conflit** : `HTTP 409 Conflict` lors de `getUpdates` – le token bot est utilisé par une autre instance.
- [Failure] Upload Arduino échoué** : `Failed uploading: no upload port provided` – pas de port série spécifié pour l’ESP32.
- [Failure] Lien AliExpress cassé** : `https://nl.aliexpress.com/item/1005003006706291.html` – produit probablement supprimé ou indisponible.
- [Failure] Problème de mémoire** : `Maximum is 327680 bytes` – script Python trop lourd pour un terminal.
- [Failure] Validation bloquée** : "a note est <8" – condition de qualité non satisfaite pour un composant.
- [Failure] : "il y a eu un crash de terminal. regarde ce qui a été fait et ce qui reste à faire
- [Failure] État : EN ATTENTE DE DIAGNOSTIC
- [Failure] Impact : Perte potentielle de traces, blocage équipe
- [Failure] Action : Vérification du vault incomplète
- [Failure] : "comment ne pas être bloqué par les demandes d'approbation ou je dis tjrs approve one
- [Failure] État : BLOQUEUR WORKFLOW
- [Failure] Impact : Ralentit cycles itératifs
- [Failure] Cause : Processus d'approbation trop strict ou mal aligné avec la réalité du développement
- [Failure] "Connection Failed: Device Unresponsive
- [Failure] Maximum is 327680 bytes" → Dépassement limite mémoire locale
- [Failure] État : BLOQUEUR HARDW. / ENVIRONNEMENT
- [Failure] Affecte : Tests ESP32, uploads firmware
- [Failure] : HTTP 409 Conflict sur `getUpdates`
- [Failure] HTTP/1.1 409 Conflict
- [Failure] Traceback : `telegram/ext/_updater.py` ligne 753
- [Failure] État : BLOQUEUR EN PRODUCTION (decouvertes-collector)
- [Failure] Cause possible : Bot déjà en écoute dans une autre session
- [Failure] Liens dans transcript : 404 ou expiré
- [Failure] État : BLOQUEUR APPROVISIONNEMENT
- [Failure] Impact : Impossibilité valider BOM matériel réelle
- [Failure] Crash terminal non résolu** : "il y a eu un crash de terminal. regarde ce qui a été fait et ce qui reste à faire
- [Failure] Bloqueur d'approbation itératif** : "comment ne pas être bloqué par les demandes d'approbation ou je dis tjrs approve one
- [Failure] Problèmes de connectivité matériel (Unresponsive Device)
- [Failure] Problème Telegram API** : HTTP 409 Conflict sur `getUpdates`
- [Failure] URLs cassées composants Aliexpress/Mouser

### Fréquence des patterns (14 jours)
- **Decision** : 12 jours, 472 occurrences
- **Failure** : 12 jours, 480 occurrences
- **Question** : 12 jours, 361 occurrences
- **Recurring question** : 12 jours, 237 occurrences
- **Blocker** : 1 jours, 1 occurrences
- **Conflict detected** : 1 jours, 3 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Decision] (11x) ent il y a un nouveau message telegrma. je vais changer la cle
- [Decision] (11x) lement la clé anthropic fonctionne mais on va sur le M1
- [Decision] (11x) les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l
- [Decision] (11x) n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont
- [Decision] (11x) on va maintenant dans travels/ pka decouvertes. si j'envoie un me
- [Decision] (11x) our ce lieu directement ou doit il etre validé
- [Failure] (11x) error handlers are registered, logging exception.Traceback (most recent call las
- [Question] (11x) n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?
- [Question] (11x) pourquoi en 2 tu parles de usb-A , le mac a des usb-c
- [Question] (11x) pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.
- [Decision] (10x) Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution
- [Decision] (10x) a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta
- [Decision] (10x) dernier point, on va matcher les besoins de capteurs iot van avec les besoins de
- [Decision] (10x) je vais acheter l'officiel et aussi le ventilateur actif. pour celu
- [Decision] (10x) on va valider les parametres indiqués du moment qu'on puisse ne c

### 📝 Suggestions de documentation automatique
- [ ] Documenter : **ent il y a un nouveau message telegrma. je vais changer la cle**
- [ ] Documenter : **lement la clé anthropic fonctionne mais on va sur le M1**
- [ ] Documenter : **les projets wildnexus, iot et travels. je vais utiliser notebook lm pour creer l**
- [ ] Documenter : **n directory ,otebooklm_ources et le md. on va les eliminer. vérifie ou il sont**
- [ ] Documenter : **on va maintenant dans travels/ pka decouvertes. si j'envoie un me**
- [ ] Documenter : **our ce lieu directement ou doit il etre validé**
- [ ] Documenter : **error handlers are registered, logging exception.Traceback (most recent call las**
- [ ] Documenter : **n van avec mon M5, je perds cet outil . comment faire pour le maintenir ok ?**
- [ ] Documenter : **pourquoi en 2 tu parles de usb-A , le mac a des usb-c**
- [ ] Documenter : **pourquoi ne propose tu pas de les mettre dans les dossiers projets respectifs.**
- [ ] Documenter : **Profil DébutantEnviron 3 750 €🚀 Profil Confirmé / SeniorEnviron 5 800 €Évolution**
- [ ] Documenter : **a note est <8.Bonjour ! Ici Cigogne 🦩, ton Vanlife Travel Planner. J'ai passé ta**
- [ ] Documenter : **dernier point, on va matcher les besoins de capteurs iot van avec les besoins de**
- [ ] Documenter : **je vais acheter l'officiel et aussi le ventilateur actif. pour celu**
- [ ] Documenter : **on va valider les parametres indiqués du moment qu'on puisse ne c**

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 51
- Jours d'observation : 12
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**159** recommandations au total — **159** ouvertes — **0** en cours — **0** terminées

⚠️ 74 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 129
- **Forge** : 26
- **Corbeau** : 2
- **Furet** : 2

### Plus récentes ouvertes

- [id=153] (2026-06-19) **Dobby** : Créer un document "Décisions PKA"** : y reporter chaque décision (projet, matéri
- [id=154] (2026-06-19) **Dobby** : Installer un glossaire** : fichier `glossary.md` dans `PKA_JCH/docs/` avec défin
- [id=155] (2026-06-19) **Dobby** : Corriger le serveur MCP HA** : vérifier la configuration du `stdio_transport`, r
- [id=156] (2026-06-19) **Forge** : Reprendre le script planté** : identifier le script via les logs (rechercher "ch
- [id=157] (2026-06-19) **Forge** : Uniformiser les commandes Arduino** : ajouter un alias ou un script dans `~/bin/

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🟡 $9.95 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $9.95**
