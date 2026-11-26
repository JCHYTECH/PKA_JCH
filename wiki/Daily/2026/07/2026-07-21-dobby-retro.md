---
date: 2026-07-21
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 5
echanges: 1136
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-21

**Sessions analysées :** 5 | **Échanges :** 1136 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS JCH – 2026-07-21
## Décisions prises

1. **Redémarrage du Lupo-RPi en mode isolé** : Tentative de valider l'intégrité du setup matériel sans dépendances externes (validation 100% approuvée)
2. **Pivot vers projet Vetalyx** : Nouvelle commande d'une société chinoise → basculade prioritaire sur ce projet en parallèle
3. **Validation des configurations Aenova** : 8 sites industriels approuvés pour produits vétérinaires → mémorisation pour tests réels prévus dans quelques jours
4. **Utilisation du niveau iPhone disponible** : Décision de s'appuyer sur les capacités réseau/sensoriales de l'iPhone plutôt que de déployer de l'infrastructure custom
5. **Gel du setup Lupo-RPi** : Priorité donnée à la stabilisation hardware avant évolution logicielle

**Problème** : Ces décisions ne sont **pas tracées dans un registre centralisé**. Aucune source de vérité unique pour validation ultérieure.

---

## Échecs ouverts / bloqueurs

### Critiques
- **RPi 5 bloqué au boot** : Reste figé en phase d'initialisation matériel. Ctrl+C ne fonctionne pas → **perte de contrôle interactif**
- **Fichier image HAOS manquant** : `haos_rpi5-15.1.img` non trouvé → download échoué (404) → **image d'installation introuvable**
- **Whisper inopérant** : Dysfonctionnement détecté en VSCode → raison non documentée
- **Home Assistant duplicate_os_install** : Conflit détecté (instance dupliquée ou restauration de backup conflictuelle) → **bloque toute initialisation**
- **AppManager.install bloqué** : Erreur système "not healthy" → empêche installation/update

### Secondaires
- **Accès terminal RPi dénié** : Impossibilité d'interagir avec le terminal → debugging impossible
- **team.db inaccessible** : Base de données verrouillée ou corrompue
- **ctrl+M affiche M au lieu de mapper commande** : Problème de binding input (iOS/RPi)
- **SD Endurance + silent blocs** : Matériel identifié comme nécessaire mais **non installé**

**Impact global** : **Aucune progression hardware/logiciel sur Lupo-RPi depuis jours**. Le projet est gelé.

---

## Questions récurrentes (signe de lacune documentaire)

1. **"Pourquoi tu n'as pas accès au terminal RPi ?"** → Répétée 3x sans réponse documentée
2. **"Pourquoi cette erreur duplicate_os_install ?"** → Cause reste obscure (restauration ? clonage ? UUID ?)
3. **"Whisper ne fonctionne pas ; vérifie pourquoi"** → Pas de diagnostic systématique
4. **"Pourquoi il boot ?"** → Question mal formulée mais reflète confusion sur l'état du système
5. **"Comment faire en sorte que GM5.2 ait le même bootstrap ?"** → Absence de procédure standardisée

**Diagnostic** : JCH **répète les mêmes questions** car les réponses ne sont pas documentées dans un lieu accessible (wiki, playbook, README).

---

## Nouveaux patterns détectés

### 1. Mode "basket-weaving" documentaire
JCH alterne entre :
- Travail technique (Lupo-RPi, Whisper, Home Assistant)
- Recherche commerciale/pharma (Virbac, Aenova, hydrocortisone, CDMO)
- Spécifications hardware (Mouser BOM, composants électroniques)

**Aucun contexte de transition donné** → Difficile d'inférer la priorité réelle ou la relation inter-tâches.

### 2. Accès/permissions fragmenté
- Fichiers perdus ou inaccessibles (`team.db`, images HAOS)
- Credentials nécéssaires mais non synchronisés (`credentials-central.md` cité mais à quel endroit ?)
- Séparation home/travail (M5 macOS vs RPi Debian) sans pool d'état commun

### 3. Cycle de diagnostic court/incomplet
JCH identifie un problème → demande vérification → reçoit réponse partielle → pivote vers autre tâche sans clôture.
Exemple : Whisper → "vérifie pourquoi on est dans vscode" → silence → continue sur autre sujet.

### 4. Mobilité réseau chaotique
Flux IPv4 changeant (iPhone → M5 → RPi) avec des commandes réseau éparpillées :
```
grep_files("192\\.168\\.|M5.*IP")
ipconfig getifaddr en0/en1
find / -iname "mosquitto.conf"
```
→ Indice que **la topologie réseau n'est pas cartographiée**

---

## Efficacités / inefficacités

### ⚡ Efficacités
- **Utilisation multi-outils intelligente** : Claude Code + DeepSeek TUI + Codex CLI pour paralléliser (57x Claude, 11x DeepSeek)
- **Mémorisation explicite** : "mets cela en mémoire car tests en réel dans quelques jours" → conscient de la limite cognitive
- **Pivotage pragmatique** : Face au blocage RPi, bascule vers Vetalyx plutôt que rumination stérile
- **Recherche d'expertise** : Appel à expert externe pour recommandations LLM/RPi (bon réflexe)

### 🔴 Inefficacités critiques
- **Pas de ticket/issue tracker** : 1136 échanges sans trace structurée → tout en mémoire ou transcript chaos
- **Image manquante non tracée** : Pourquoi HAOS 404 ? Qui devait la downloader ? Quand ?
- **Boot loop sans termination** : RPi figé → 0 tentative de hard reset/JTAG/console série documentée
- **Duplication de contexte** : Même info pharma / même questions RPi parsemées dans 5 sessions sans consolidation
- **Locale non configurée** : Avertissement LC_CTYPE=UTF-8 → jamais corrigé mais rencontré 5x

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### État critique du matériel
```
Lupo-RPi :
  ├─ Hardware : 95% complet (manque : SD Endurance, silent blocs, validation boot)
  ├─ Logiciel : BLOQUÉ (Home Assistant duplicate_os_install, Whisper KO, terminal inaccessible)
  ├─ Dernière session opérationnelle : 2026-07-09
  └─ Action requise : Hard reset + console série pour diagnostiquer boot loop

M5 macOS :
  ├─ IP config fragmentée (en0/en1 à mapper)
  ├─ Credentials en local (`credentials-central.md`) → à vérifier accessibilité
  └─ Bootstrap GM5.2 → procédure standardisée manquante
```

### Projets en attente
```
WildNexus : mentions 18x, besoin de clarification (objectif ? status ? deadline ?)
Vetalyx : PRIORITÉ MONTANTE (société chinoise, tests réels en "quelques jours")
Aenova : 8 sites certifiés → à exploiter pour Vetalyx/pharma vétérinaire
```

### Dépendances non résolues
- **HAOS image** : Où la trouver ? Mirror officiel ? Checksum ?
- **Mosquitto config** : Trouvée avec find mais pas intégrée au plan de dépannage
- **Whisper debug** : Cause VSCode TBD
- **duplicate_os_install** : À investiguer (grep logs, vérifier UUID disques)

---

## Recommandations

### 🎯 Immédiat (24-48h)
1. **Créer un registre de décisions** (Decision Log) pour chaque projet
   - Format : Date | Projet | Décision | Responsable | Deadline validation
   - Stocker dans `JCH_Inbox/00_INBOX/_DECISIONS.md`

2. **Débloquer Lupo-RPi via console série**
   - Procédure : JTAG ou câble USB série pour voir output boot
   - Si stuck → reflash HAOS depuis machine tierce (PC Linux + balena Etcher)
   - Tester locale Debian EN_US.UTF-8 immédiatement

3. **Classifier les tâches par projet**
   - Ségréguer Pharma/Vetalyx | IoT/Lupo-RPi | Réseau/M5
   - Chaque projet = folder dédié + README explicite

### 📋 Court terme (1 semaine)
4. **Créer ticket tracker minimaliste**
   - Au minimum : fichier YAML ou JSON par projet listant blockers + status
   - Lier à decision log

5. **Documenter FAQ Lupo-RPi**
   - "Pourquoi pas d'accès terminal ?" → Créer playbook SSH/locale/permissions
   - "Comment booter proprement ?" → Flowchart graphique

6. **Valider topologie réseau**
   - Cartographier : iPhone ↔ M5 ↔ Lupo-RPi (IPs, credentials, Tailscale status)
   - Output : schéma + fichier `network-topology.md`

### 🏗️ Moyen terme (2-3 semaines)
7. **Centraliser credentials et configurations**
   - `credentials-central.md` → audit d'accessibilité depuis chaque machine
   - Utiliser Tailscale pour seamless access ou secrets manager

8. **Standardiser bootstrap pour G5.2/M5**
   - Procédure écrite, testée, versionnée (v0.1, v0.2...)
   - Template réutilisable

9. **Paralléliser Vetalyx études pharma**
   - Compiler recherche Virbac + Aenova en document synthétique
   - Mapper : API active → CDMO certifiés EU-GMP → coût/délai

### 🔍 Méthodologie
- **Stop les pivotages non documentés** : avant de changer de projet, 2min de notes
- **Timeboxing** : Lupo-RPi 2h max/session, puis pivot si bloqué
- **Weekly sync** : 15min pour consolider patterns, décisions, blockers

---

## Notes finales

**Diagnostic** : JCH opère en mode **"multi-contexte non-persistent"**. Chaque session réinvente la roue car le précédent apprentissage n'est pas stocké structurellement. 1136 échanges sans système de capitalisierung = **perte d'efficacité quadratique**.

**Symptôme clé** : Les mêmes questions reviennent (terminal RPi, whisper, erreur duplicate) parce qu'il n'existe pas d'artefact durable (ticket, wiki, playbook) pour les résoudre une fois pour toutes.

**Urgence** : Lupo-RPi bloqué depuis 12j. Vetalyx accélère. **Il faut débloquer le hardware ASAP ou pivoter définitivement sur Vetalyx/pharma.** Choix stratégique à documenter explic

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 39
- Résolus automatiquement : 11
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 28.2%**

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

- [Decision] : Tentative de valider l'intégrité du setup matériel sans dépendances externes (validation 100% approuvée)
- [Decision] : Nouvelle commande d'une société chinoise → basculade prioritaire sur ce projet en parallèle
- [Decision] : 8 sites industriels approuvés pour produits vétérinaires → mémorisation pour tests réels prévus dans quelques jours
- [Decision] : Décision de s'appuyer sur les capacités réseau/sensoriales de l'iPhone plutôt que de déployer de l'infrastructure custom
- [Decision] : Priorité donnée à la stabilisation hardware avant évolution logicielle
- [Decision] : Ces décisions ne sont **pas tracées dans un registre centralisé**. Aucune source de vérité unique pour validation ultérieure.
- [Decision] Redémarrage du Lupo-RPi en mode isolé** : Tentative de valider l'intégrité du setup matériel sans dépendances externes (validation 100% approuvée)
- [Decision] Pivot vers projet Vetalyx** : Nouvelle commande d'une société chinoise → basculade prioritaire sur ce projet en parallèle
- [Decision] Validation des configurations Aenova** : 8 sites industriels approuvés pour produits vétérinaires → mémorisation pour tests réels prévus dans quelques
- [Decision] Utilisation du niveau iPhone disponible** : Décision de s'appuyer sur les capacités réseau/sensoriales de l'iPhone plutôt que de déployer de l'infrast
- [Decision] Gel du setup Lupo-RPi** : Priorité donnée à la stabilisation hardware avant évolution logicielle
- [Failure] RPi 5 bloqué au boot** : Reste figé en phase d'initialisation matériel. Ctrl+C ne fonctionne pas → **perte de contrôle interactif
- [Failure] Fichier image HAOS manquant** : `haos_rpi5-15.1.img` non trouvé → download échoué (404) → **image d'installation introuvable
- [Failure] Whisper inopérant** : Dysfonctionnement détecté en VSCode → raison non documentée
- [Failure] Home Assistant duplicate_os_install** : Conflit détecté (instance dupliquée ou restauration de backup conflictuelle) → **bloque toute initialisation
- [Failure] AppManager.install bloqué** : Erreur système "not healthy" → empêche installation/update

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 36 occurrences
- **Failure** : 9 jours, 54 occurrences
- **Question** : 7 jours, 20 occurrences
- **Recurring question** : 6 jours, 20 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**329** recommandations au total — **329** ouvertes — **0** en cours — **0** terminées

⚠️ 265 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 287
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 4

### Plus récentes ouvertes

- [id=320] (2026-07-21) **Dobby** : Créer un registre de décisions** (Decision Log) pour chaque projet
- [id=321] (2026-07-21) **Dobby** : Format : Date | Projet | Décision | Responsable | Deadline validation
- [id=322] (2026-07-21) **Dobby** : Stocker dans `JCH_Inbox/00_INBOX/_DECISIONS.md`
- [id=323] (2026-07-21) **Dobby** : Débloquer Lupo-RPi via console série
- [id=324] (2026-07-21) **Dobby** : Procédure : JTAG ou câble USB série pour voir output boot

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
