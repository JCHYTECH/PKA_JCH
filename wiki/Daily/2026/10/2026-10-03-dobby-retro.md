---
date: 2026-10-03
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1011
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-03

**Sessions analysées :** 2 | **Échanges :** 1011 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Sessions 2026-10-03 - Dobby PKA Audit

## Décisions prises

### Confirmées et documentées
- **IoT-Van revival** : Redémarrage du projet avec batterie Bluetti 100 V2 + chargeur 2 pour Lupo Bianco
- **Vetalyx - structure actionnariale** : Acceptation de la participation chinoise (DIaho) à 40% du capital sans opérateurs physiques chinois. Capital social : 10 000€. Validation juridique UCM Belgique en cours.
- **Meuble banquette** : Spécifications finalisées pour van Westfalia Kelsey (104×55×25cm, 3 tiroirs, trappe basculante 180°)
- **Priorité LLM Raspberry Pi 5** : Orientation vers SLM quantisés (Q4_K_M GGUF) via Ollama plutôt que LLM full-size

### Floues ou conditionnelles
- **Drafts → Validés** : Ordre donné sans cible de fichiers explicite
- **Recherche WICAN** : Demande rappel sur composant existant (nature du composant non clarifiée)
- **iPhone pressure pression** : Accès credentials et réseau cherché sans objectif déclaré

---

## Échecs ouverts / bloqueurs

### Critiques
1. **Raspberry Pi 5 bloqué en initialisation matérielle**
   - Phase de boot gelée au démarrage du HAT tiers-PSU
   - Impact : IoT-Van non fonctionnel
   - Action requise : Vérifier PSU_MAX_CURRENT=5000, diagnostic du HAT Geekworm

2. **Home Assistant - Conflit d'instance active**
   - Erreur : Deux instances détectées (clonage disque / restauration sauvegarde)
   - UUID dupliqué probable
   - Impact : HA ne démarre pas
   - Solution proposée non exécutée

3. **AppManager.install bloqué**
   - Message : "system is not healthy - duplicate_os_instal"
   - Cause racine inconnue (diagnostic incomplet)

### Modérés
4. **Credentials Google Keyword invalides**
   - Username/password ne fonctionnent pas
   - Origine : export/import mal géré
   - Contexte : Recherche de données (Umbria?)

5. **VanRoll test ne remonte plus de données**
   - Demande de diagnostic mais pas d'investigation systématique
   - Source de données inconnue

6. **Facteur 3 d'erreur détecté** 
   - Citation : "observe l'importance de ton erreur : un facteur 3. cela peut tuer une decision sur un projet"
   - Domaine : non spécifié (budget? capacité? timing?)
   - Aucune trace de correction

---

## Questions récurrentes (signe de lacune documentaire)

### Retours observés 2+ fois
- **"C'est quoi les states files?"** → Core HA/project config, jamais expliqué
- **"L(M) c'est quoi?"** → Notation technique non définie (Litres? Mode? Log?)
- **"Les 3 fiches needs_review"** → Dashboard/triage vague, pas de lien clair
- **"Avant/arrière (4 roues)"** → Spécification van, orientation manquante
- **"Pourquoi VanRoll ne donne plus de données?"** → Test failure, cause non documentée
- **"C'est quoi le ZH?"** → Acronyme jamais défini

### Questions structurelles non résolues
- **Procédure d'erreur "facteur 3"** : Aucun document root cause
- **Instruction non exécutée** : Qui valide? Qui trace?
- **Données Dante vides** : Exception ou bug système?

---

## Nouveaux patterns détectés

### Pattern 1 : Context-switching haute fréquence
- Passage Vetalyx (juridique Belgique) → IoT-Van (hardware) → WildNexus (audio sensor) en <10 messages
- **Impact** : Perte de momentum sur tasks incomplete (VanRoll diagnostic, HA fix)
- **Symptôme** : "on va faire des simulations et je te reviens" / "on va arrêter là"

### Pattern 2 : Requête non spécifiée → digging aveugle
- "Pression iPhone" → 6 tools lancés (grep, ipconfig, credentials, docker-compose) sans objectif déclaré
- "Recherche Umbria" → Query vague sans contexte
- **Inefficacité** : 40% de travail d'assistant sans convergence

### Pattern 3 : Décisions avec condition implicite
- "Je vais installer la batterie Bluetti" (pas commande, pas timeline, pas vérification stock)
- "On va attendre la position des autres" (qui? deadline?)
- **Risque** : Dépendances cachées

### Pattern 4 : Diagnostic partial = abandon
- HA error analysée → cause posée → "verifie le bug HA" → silence
- AppManager blocked → hypothèse system health → pas de follow-up
- **Perte d'information** : Hypothèses diagnostiques jamais validées

---

## Efficacités / Inefficacités

### ✅ Efficacités observées
1. **Specification granulaire (meuble banquette)** : Dimensions, matériaux, mécanismes très clairs → BOM actionnable
2. **Escalade juridique appropriée** : Question complexe Vetalyx → expert UCM → décision informée
3. **Orientation technologique justifiée** : Consultation expert RPi5/LLM → recommandation SLM cohérente
4. **Richesse d'entités** : Multi-domaines (hardware, juridique, logiciel, design) gérés en parallèle

### ❌ Inefficacités observées
1. **Outils lancés sans convergence** : grep_files, ipconfig, credentials lues sans lien causal → ~15 min perdues
2. **Diagnostics abandonnés** : 3 erreurs système non résolues (RPi5, HA, AppManager)
3. **Terminologie interne non documentée** : "states files", "L(M)", "ZH", "needs_review" → questions répétées
4. **Décisions sans validation** : "Je vais choisir le niveau iPhone" → pas de test avant engagement
5. **Questions polies avant agir** : "D'abord on va leur poser des questions polies" → délai non quantifié

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Projets en vol
1. **IoT-Van (BLOQUER)** 
   - RPi5 gelé en boot → diagnostic HAT/PSU obligatoire avant nouvelle tentative
   - Bluetti 100 V2 : achat non confirmé, timeline ?
   - WICAN : composant non identifié, rappel attendu

2. **Vetalyx Belgique**
   - Décision actionnariale : ✅ structurée (DIaho 40%, capital 10k€)
   - Étape suivante : Dépôt légal? Timing?

3. **Home Assistant**
   - Conflit UUID dual-instance → nettoyage disque requis avant restart
   - Procédure de clonage imprécise → documenter next time

4. **WildNexus Audio Sensor**
   - Pivot vers captation sonore minimaliste (pre-Phase B)
   - Cas d'usage : surveillance biotope (armes à feu, tronçonneuse, flamme)
   - Status : Concept only

5. **VanRoll test**
   - Ne remonte plus de données → source inconnue, diagnostic pending
   - Impact sur quel produit?

### Terminologie non documentée
```
- states files → Créer glossaire_homeassistant.md
- L(M) → Notation technique, domaine?
- ZH → Acronyme réseau?
- needs_review (fiches) → Triage system?
- WICAN → Composant IoT? Marque?
- Facteur 3 d'erreur → Raprocher contexte exact
```

### Dépendances bloquantes
- Diagnose RPi5 hardware → condition sine qua non IoT-Van
- Clarify WICAN → condition rappel assistant
- VanRoll root cause → impact produit ?

---

## Recommandations

### R1 : Créer template "Décision" obligatoire
**Problème** : Décisions avec conditions implicites ("on va attendre", "je vais essayer")
```markdown
# Décision: [Titre]
- **Qui** : 
- **Quoi** : [Action précise]
- **Condition/Deadline** : 
- **Dépendances** : 
- **Validé par** :
- **Trace** : lien fichier/issue
```

### R2 : Fermer les diagnostics avant context-switch
**Règle** : Si tu as >1 hypothèse diagnostique, **valide ou documente chacune** avant de switch
- RPi5 boot hang → rédige mini-rapport {cause_hypothèse, test_fait, résultat}
- HA dual-instance → ajoute step-by-step fix ou "parké en attente de [ressource]"

### R3 : Glossaire technique pour PKA
**Créer** : `docs/terminologie-interne.md` avec entrées :
- states files (HA)
- ZH / L(M) / WICAN / needs_review
- Mise à jour hebdo après sessions

### R4 : "Objectives Board" au démarrage de session
**Avant de lancer outils** : 3 questions
1. Quel est mon objectif principal aujourd'hui?
2. Y a-t-il des bloqueurs en attente (RPi5? HA? Credentials)?
3. Quel est mon time-box par domaine?

### R5 : Tracer les "on va arrêter là, on tourne en rond"
**Problème** : 3 abandons observés sans raison documentée
**Solution** : Tag `[PARKED]` avec raison = {attente_info, manque_resources, diminishing_returns, depends_on_X}

### R6 : Requête ≠ Outil-launching
**Avant** `grep_files()`, `exec_shell()`, `read_file()`, demander à haute voix :
- Qu'est-ce que je cherche exactement?
- Où je m'attends à trouver ça?
- Comment je valide si j'ai la bonne réponse?

---

## Synthèse critique

**Santé du PKA** : ⚠️ **Modérée**
- ✅ Multi-domaines actifs, décisions structurelles prises
- ❌ 3 bloqueurs matériels/sys non résolus
- ❌ Terminologie interne fragmentée
- ❌ Context-switching rapide + diagnostics incomplets = tech debt

**Prochaine étape prioritaire** : Déboguer RPi5 boot hang (IoT-Van dépend de ça) OU créer `/docs/terminologie-interne.md` (all projects) ?

**Recommandation Dobby** : Faire les deux cette semaine — 1h RPi5 debug (méthodique), 1h glossaire (gain répétabilité long-terme).

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 30
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 6.7%**

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

- [Decision] IoT-Van revival** : Redémarrage du projet avec batterie Bluetti 100 V2 + chargeur 2 pour Lupo Bianco
- [Decision] Vetalyx - structure actionnariale** : Acceptation de la participation chinoise (DIaho) à 40% du capital sans opérateurs physiques chinois. Capital soc
- [Decision] Meuble banquette** : Spécifications finalisées pour van Westfalia Kelsey (104×55×25cm, 3 tiroirs, trappe basculante 180°)
- [Decision] Priorité LLM Raspberry Pi 5** : Orientation vers SLM quantisés (Q4_K_M GGUF) via Ollama plutôt que LLM full-size
- [Failure] Phase de boot gelée au démarrage du HAT tiers-PSU
- [Failure] Impact : IoT-Van non fonctionnel
- [Failure] Action requise : Vérifier PSU_MAX_CURRENT=5000, diagnostic du HAT Geekworm
- [Failure] Conflit d'instance active
- [Failure] Erreur : Deux instances détectées (clonage disque / restauration sauvegarde)
- [Failure] UUID dupliqué probable
- [Failure] Impact : HA ne démarre pas
- [Failure] Solution proposée non exécutée
- [Failure] Message : "system is not healthy - duplicate_os_instal
- [Failure] Cause racine inconnue (diagnostic incomplet)
- [Failure] Raspberry Pi 5 bloqué en initialisation matérielle
- [Failure] Home Assistant - Conflit d'instance active
- [Failure] AppManager.install bloqué

### Fréquence des patterns (14 jours)
- **Failure** : 6 jours, 18 occurrences
- **Recurring question** : 6 jours, 16 occurrences
- **Decision** : 5 jours, 29 occurrences
- **Question** : 5 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 17
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**460** recommandations au total — **460** ouvertes — **0** en cours — **0** terminées

⚠️ 413 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 415
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=456] (2026-10-03) **Dobby** : : Décisions avec conditions implicites ("on va attendre", "je vais essayer")
- [id=457] (2026-10-03) **Dobby** : Quoi** : [Action précise
- [id=458] (2026-10-03) **Dobby** : Condition/Deadline** :
- [id=459] (2026-10-03) **Dobby** : Dépendances** :
- [id=460] (2026-10-03) **Dobby** : Trace** : lien fichier/issue

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
