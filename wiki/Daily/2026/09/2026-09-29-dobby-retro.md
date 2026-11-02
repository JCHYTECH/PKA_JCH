---
date: 2026-09-29
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1067
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-29

**Sessions analysées :** 2 | **Échanges :** 1067 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS DU 2026-09-29

## Décisions prises

1. **Validation et mise à jour des fichiers** : Consensus sur la nécessité de valider et mettre à jour tous les fichiers pertinents, avec notification aux stakeholders.
2. **Approche conversationnelle** : Décision de poser des questions polies en priorité pour comprendre le contexte avant d'agir (plutôt que d'agir directement).
3. **Fiches finalisées** : Plusieurs fiches marquées comme "validées finalise".
4. **Standardisation matérielle IoT** : **Reste en 12V partout** pour faciliter la procurement et la logistique des projets IoT (Lupo, Vetalyx, etc.).
5. **Réveil du projet IoT-Van** : Décision de relancer le projet avec demande de résumé de l'état.
6. **Traitement par batch** : Les tâches seront traitées par lot de 10, avec traitement des "skip" en second.
7. **Travail sur les screenshots** : Focus sur l'analyse des screenshots dans `JCH_Inbox/sites`.

---

## Échecs ouverts / bloqueurs

### Critique
- **Raspberry Pi 5 bloqué à l'initialisation** : Le RPi reste suspendu au tout début de la phase d'initialisation matérielle. *Impact potentiel : critique pour le projet IoT-Van et Lupo.*
- **Erreur Home Assistant "duplicate_os_install"** : `AppManager.install` bloqué, système non-sain. Deux instances Home Assistant détectées sur le réseau/disque (conflit UUID post-restauration).
- **Facteur d'erreur "3x" mentionné** : JCH note que les erreurs dimensionnelles ou de configuration peuvent avoir un impact multiplicatif (3x) sur les décisions de projet.

### Matériel
- **Lupo/Ilupo** : Presque terminé, en attente de :
  - SD card "endurance" (remplacement)
  - Silent bloc sur RPi (isolation vibration)
- **Authentification échouée** : Identifiants (username/pass) venant d'une recherche keyword Google ne fonctionnent pas.
- **Erreur de connexion sécurisée** : "Secure connection to fail" (erreur SSL/TLS).

### Données / Documentation
- **Fiches vides** : Fiche Dante est vide. À clarifier : est-ce exceptionnel ou signe d'un bug systématique ?
- **Vanroll test ne donne plus de données** : Cause inconnue, à investiguer.

### Questions non résolues bloquant les décisions
- Différence entre `lupo/assiette` et `esneux/iphone` (quelle est l'instance HA exacte ?)
- C'est quoi les "3 fiches needs_review" ?
- C'est quoi les "states files" ?

---

## Questions récurrentes (signe de lacune documentaire)

**CRITIQUE : répétitions massives indiquant une absence de documentation centralisée ou accessible.**

1. **"c'est quoi les 3 fiches needs_review"** → Pas de liste documentée des fiches requérant une review.
2. **"lupo reporté au 31 aout. c'est quoi les states files ?"** → Concept technique non expliqué.
3. **"c'est quoi le ZH"** → Acronyme non défini.
4. **"Pourquoi 25-26 cm pour la hauteur du tiroir ?"** → Logique de conception pas documentée (JCH explique : "pour laisser le meuble en place même quand la banquette passager est sortie").
5. **"4 roues vs petit, lequel avant/arrière ?"** → Spécifications matériel Lupo manquantes.
6. **"TTL 24h. Comment utiliser cela avec fluidité dans du HTML ?"** → Pas de pattern d'usage documenté.
7. **"Pourquoi Dante fiche est vide ?"** → Investigation ad-hoc du même problème d'intégrité de données.
8. **"Pourquoi vanroll test ne donne plus de données ?"** → Même question cyclique.
9. **"L(M) c'est quoi ?"** → Notation/convention non expliquée.

**Diagnostic : Le PKA manque d'un glossaire centralisé, d'une FAQ technique et d'une documentation d'architecture.**

---

## Nouveaux patterns détectés

1. **Mode multi-projet chaotique** : JCH bascule entre :
   - Projets IoT (Raspberry Pi, Home Assistant, Lupo, Ilupo, Vetalyx)
   - Projets VanLife (meuble banquette 104×55×25 cm, Westfalia Kelsey)
   - Projets commerciaux (Vetalyx Belgium, capital chinois 40% via DIaho)
   - Recherche/exploration (Ombrie, lieux exotiques)
   
   → Pas de contexte de switching explicite. Les assistants doivent inférer le projet actif.

2. **Utilisation intensive du "working set"** : JCH utilise systématiquement des directives de "working set" pour limiter le contexte :
   - `/Users/jchavauxm5/PKA_JCH`
   - Priorité : `JCH_Inbox`, `JCH_PRIVATE`, `TEAM`, fichiers clés `AGENTS.md`, `CLAUDE.md`
   
   → Pattern sain mais nécessite une documentation à jour.

3. **Questions polies comme filtre** : JCH explicite : "d'abord on va leur poser des questions polies pour comprendre" avant d'exécuter.
   → Approche conversationnelle > action directe.

4. **Décisions d'arrêt et documentation** : "on va arreter là. on tourne en rond, cree un fichier .md à mettre" 
   → Reconnaissance proactive des boucles infinies → création de documentation.

5. **Vérifications de cohérence PKA** : Demande explicite : "fais une analyse du pka-jch pour verifier que tout est cohérent en terme de positionnement dans les directory, presence de doublons".
   → Besoin récurrent d'audit de structure.

---

## Efficacités / inefficacités

### ✅ Efficacités observées
1. **Utilisation des outils CLI** : Grep, exec_shell, read_file pour diagnostiquer rapidement (ex : recherche de `mosquitto.conf`, credentials).
2. **Standardisation matérielle** : Décision "rester en 12V partout" réduit la complexité de procurement.
3. **Batch processing** : Traiter par lots de 10 élimine l'overload.
4. **Reconnaissance des boucles** : JCH arrête les discussions circulaires et crée de la documentation.

### ❌ Inefficacités critiques
1. **Questions répétées ad nauseam** : 9+ questions sans réponse écrite, posées à chaque session.
2. **Pas de FAQ/Glossaire** : Chaque question = relecture du contexte complet.
3. **États ambigus** : "Lupo reporté au 31 aout" → état flou, date passée (on est en 2026-09), pas de clarté.
4. **Erreurs non documentées** : Erreur Home Assistant "duplicate_os_install" → expliquée dans le transcript mais pas créé de runbook de résolution.
5. **Switching de projet sans structure** : VanLife ↔ IoT ↔ Vetalyx sans arborescence claire.
6. **Fiches vides/incohérentes** : Dante fiche vide, vanroll test "ne donne plus de données" (regression ?).

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Architecture / Working Set
- **Workspace racine** : `/Users/jchavauxm5/PKA_JCH`
- **Fichiers clés** : `AGENTS.md`, `CLAUDE.md` (vérifier à chaque session)
- **Répertoires prioritaires** :
  - `JCH_Inbox/00_INBOX` (inbox)
  - `JCH_Inbox/03_PROJECTS/07_TRAVELS/van` (VanLife)
  - `JCH_Inbox/03_PROJECTS/11_IOT` (IoT)
  - `JCH_PRIVATE/credentials-central.md` (credentials)
  - `PHOTO/analyses`, `places.json` (géolocalisation/voyage)

### Projets actifs (état au 2026-09-29)
| Projet | État | Bloqueur |
|--------|------|----------|
| **Lupo (Ilupo)** | 95% HW | SD endurance + silent bloc RPi 5 |
| **Vetalyx (BE)** | Legal review | Capital chinois 40% (DIaho) – déclaration obligatoire ? |
| **IoT-Van** | Réactivation | RPi 5 bloqué initialisation + Home Assistant duplicate_os_install |
| **VanLife Meuble** | Design | 104×55×25cm, 3 tiroirs, trappe 180° |
| **Ombrie (Travel)** | Recherche | Lieux exotiques/peu visités à identifier |

### Concepts/Terms à clarifier et documenter
- **States files** (Home Assistant)
- **ZH** (acronyme non-défini)
- **3 fiches needs_review** (list à établir)
- **L(M)** notation (convention dimensionnelle ?)
- **Fiches Dante** (pourquoi vide ?)
- **Vanroll test** (regression ou feature stop ?)

### Valeurs / Standards
- **Standardisation** : Tout en **12V** pour IoT
- **Procurement** : Batch de 10 tâches
- **Approche** : Questions polies → Compréhension → Action
- **Arrêt** : Stopper les boucles infinies et documenter

### Erreurs à tracker
1. Home Assistant : erreur `duplicate_os_install` (post-restauration, UUID conflit)
2. Authentification : credentials Google Keyword-based ne fonctionnent pas
3. SSL/TLS : "Secure connection to fail"
4. Raspberry Pi 5 : initialisation bloquée phase matériel

---

## Recommandations

### 🔴 URGENT (Impact immédiat)

1. **Créer un FAQ/Glossaire centralisé** (`PKA_JCH/docs/FAQ.md`) :
   - Définir : States files, ZH, L(M), fiches needs_review, Dante context
   - Poser une fois, répondre une fois, partager toujours
   
2. **Résoudre RPi 5 initialisation** :
   - Documenter l'erreur exacte (serial output, logs)
   - Test : autre SD card, autre alimentation, autre HAT
   - Créer runbook : `JCH_Inbox/03_PROJECTS/11_IOT/RPi5_init_troubleshooting.md`

3. **Résoudre Home Assistant duplicate_os_install** :
   - Lister toutes les instances HA sur le réseau (scan réseau complet)
   - Cloner/backup conflictuel : quel disque, quelle date ?
   - Créer runbook : `JCH_Inbox/03_PROJECTS/11_IOT/HA_duplicate_recovery.md`

4. **Clarifier état Lupo/

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 28
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 26
- **Taux : 7.1%**

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

- [Decision] : Consensus sur la nécessité de valider et mettre à jour tous les fichiers pertinents, avec notification aux stakeholders.
- [Decision] : Décision de poser des questions polies en priorité pour comprendre le contexte avant d'agir (plutôt que d'agir directement).
- [Decision] : Plusieurs fiches marquées comme "validées finalise".
- [Decision] : **Reste en 12V partout** pour faciliter la procurement et la logistique des projets IoT (Lupo, Vetalyx, etc.).
- [Decision] : Décision de relancer le projet avec demande de résumé de l'état.
- [Decision] : Les tâches seront traitées par lot de 10, avec traitement des "skip" en second.
- [Decision] : Focus sur l'analyse des screenshots dans `JCH_Inbox/sites`.
- [Decision] Validation et mise à jour des fichiers** : Consensus sur la nécessité de valider et mettre à jour tous les fichiers pertinents, avec notification aux 
- [Decision] Approche conversationnelle** : Décision de poser des questions polies en priorité pour comprendre le contexte avant d'agir (plutôt que d'agir directem
- [Decision] Fiches finalisées** : Plusieurs fiches marquées comme "validées finalise".
- [Decision] Standardisation matérielle IoT** : **Reste en 12V partout** pour faciliter la procurement et la logistique des projets IoT (Lupo, Vetalyx, etc.).
- [Decision] Réveil du projet IoT-Van** : Décision de relancer le projet avec demande de résumé de l'état.
- [Decision] Traitement par batch** : Les tâches seront traitées par lot de 10, avec traitement des "skip" en second.
- [Decision] Travail sur les screenshots** : Focus sur l'analyse des screenshots dans `JCH_Inbox/sites`.
- [Failure] Raspberry Pi 5 bloqué à l'initialisation** : Le RPi reste suspendu au tout début de la phase d'initialisation matérielle. *Impact potentiel : critique
- [Failure] Erreur Home Assistant "duplicate_os_install"** : `AppManager.install` bloqué, système non-sain. Deux instances Home Assistant détectées sur le réseau/
- [Failure] Facteur d'erreur "3x" mentionné** : JCH note que les erreurs dimensionnelles ou de configuration peuvent avoir un impact multiplicatif (3x) sur les dé

### Fréquence des patterns (14 jours)
- **Failure** : 4 jours, 14 occurrences
- **Recurring question** : 4 jours, 14 occurrences
- **Question** : 3 jours, 16 occurrences
- **Decision** : 2 jours, 24 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 17
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**440** recommandations au total — **440** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 395
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=429] (2026-09-29) **Dobby** : Créer un FAQ/Glossaire centralisé** (`PKA_JCH/docs/FAQ.md`) :
- [id=430] (2026-09-29) **Dobby** : Définir : States files, ZH, L(M), fiches needs_review, Dante context
- [id=431] (2026-09-29) **Dobby** : Poser une fois, répondre une fois, partager toujours
- [id=432] (2026-09-29) **Dobby** : Résoudre RPi 5 initialisation** :
- [id=433] (2026-09-29) **Dobby** : Documenter l'erreur exacte (serial output, logs)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
