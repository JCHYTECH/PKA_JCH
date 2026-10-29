---
date: 2026-09-26
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1084
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-26

**Sessions analysées :** 2 | **Échanges :** 1084 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSION 2026-09-26 | Dobby PKA

## Décisions prises

| Décision | Contexte | État |
|----------|----------|------|
| **Traiter les skips par batch de 10** | Optimisation du workflow de traitement | Actée |
| **Travailler sur screenshots inbox/sites** | Analyse de contenu visuel en attente | En cours |
| **Facteur form = sphère sans fixation unitaire** | Conception mécanique : pas de demande client sur fixations individuelles | Validée |
| **Sélection niveau dispo iPhone** | Configuration réseau / batterie pour remote pilotage | À confirmer |
| **Redémarrage lupo-rpi solo** | Diagnostic de stabilité système après instabilité détectée | À exécuter |
| **Procédure fiches spots pour stationnement** | Workflow de gestion des emplacements (Vetalyx) | En attente de formalisation |
| **Test en live avant finalisation** | Fiches validées → tests réels quelques jours après | Planifié |
| **Discussion partenaire Alain Bosseloir** | Point stratégique Vetalyx Belgique | En attente |

---

## Échecs ouverts / bloqueurs

### 🔴 CRITIQUE
- **RPi 5 bloqué en phase init matériel** : Système reste figé au démarrage, impossible de progresser vers OS. Suspect : conflit SQUASHFS sur nvme0n1p5 (`fsconfig() failed`).
- **Erreur duplicate_os_install + AppManager.install blocked** : Deux instances Home Assistant détectées → conflits UUID/réseau. Indique restauration sauvegarde non nettoyée ou disque cloné.
- **Connexion SSL/TLS fail** : Erreur 404 combinée à secure connection fail → certificats ou endpoint misconfigurés.

### 🟡 MOYEN
- **LUPO hardware quasi complet** : Manquent = SD endurance + silent bloc RPi. Blocage mineur.
- **Terminal RPI inaccessible** : Question récurrente → SSH fonctionne (logs montrent login réussi) mais capacité exec limitée en local. À clarifier.
- **Vanroll test ne retourne plus de données** : Cause non identifiée, correction demandée mais pas de diagnostic.

### 🟠 INFORMATION MANQUANTE
- **ZH** : Référence non documentée (acronyme inconnu).
- **Différence lupo/assiette vs esneux/iphone** : Instance HA différente ? Architecture sous-jacente floue.
- **État files confusion** : Terme "states files" mentionné mais contexte Home Assistant pas clair.

---

## Questions récurrentes (lacune documentaire)

| Question | Occurrence | Implication |
|----------|-----------|------------|
| **Comment garder en mémoire procedures lancées via nom/alias ?** | 2x | Besoin CLI standardisée + documentation procédures |
| **Pourquoi tu ne peux pas travailler terminal RPI ?** | 2x | Permissions ? SSH config ? GPU/resources ? **À documenter urgently** |
| **L(M) c'est quoi ?** | 1x | Notation/sigle métier non défini |
| **4 roues vs petit, avant vs arrière ?** | 1x | Nomenclature mécanique LUPO manquante |
| **Pourquoi vanroll test ne donne plus de données ?** | 1x | Debug incomplet, cause racine pas trouvée |
| **TTL 24h + utilisation HTML fluide ?** | 1x | Intégration cache/token pas documentée |
| **Pourquoi fiche Dante est vide ?** | 1x | Défaut structurel ou incident ponctuel ? **Audit requis** |

---

## Nouveaux patterns détectés

### 🔄 Patterns de travail
1. **Debugging par cascade d'outils** : SSH → grep_files → exec_shell → read_file → list_dir. Efficace mais traces fragmentées.
2. **Décisions verbales sans formalisation** : "on va faire...", "on va tester..." → pas d'issue/ticket créé. **Traçabilité faible.**
3. **Mélange contextes** : IoT (RPi/HA), mécanique (LUPO), juridique (Vetalyx Belgique), opérations (fiches spots) dans même session → context switching coûteux.
4. **Consultation d'experts externe** : Patterns sains (avis UCM Belgique, expert LLM Ollama). À valoriser mais formaliser référence.

### 🎯 Utilisation outils
- **DeepSeek** : 3 occurrences, primarily context retrieval + repo exploration.
- **Claude** : 26 occurrences → outil principal pour synthèse/decisions.
- **Docker** : 5x, setup infrastructure (mosquitto, HA, Ollama).
- **Entité dominante** : RPi (74x) >> M5 (28x) → projet RPi critique.

---

## Efficacités / inefficacités

### ✅ EFFICACES
- **Expert external consultation** : Input qualifié sur Ollama/SLM Raspberry Pi 5.
- **Batch processing décision** : Skip par 10 = réduction overhead vs un par un.
- **Diagnostic SSH multi-layer** : Logs montrent progression structurée (auth → kernel → filesystem).

### ❌ INEFFICACES
- **Manque formalisation décisions** : "ok on va..." vs créer issue/ticket. Risque oubli/dérives.
- **Terminal RPI blocage non résolu** : Question posée 2x sans réponse actionnelle → frustration accumulée.
- **Fiche Dante vide** : Pas de root cause analysis systématique. Décision "c'est exceptionnel" prise sans audit.
- **Notation métier non standardisée** : L(M), ZH, "assiette", sans glossaire → compréhension fragile.
- **Mélange contextes IoT/juridique/mécanique** : Coût cognitif élevé. Priorisation opérationnelle floue.

---

## Ce qu'il faut garder en mémoire pour prochaines sessions

### 🧠 TECHNIQUEMENT
1. **RPi 5 state** : Bloqué init matériel. SQUASHFS corruption suspect sur nvme0n1p5. À corriger avant tests "en live".
2. **Home Assistant conflict** : UUID/duplicate_os_install → nettoyer ancienne instance, valider sauvegarde propre.
3. **LLM sur RPi** : Expert recommande SLM quantisés (Q4_K_M GGUF) via Ollama pour fluidité.
4. **Lupo-rpi hardware** : ~95% complet. SD endurance + silent bloc = étapes finales.
5. **Credentials centralisées** : credentials-central.md existe → utiliser pour mosquitto/HA setup.

### 📋 PROCÉDURELLEMENT
1. **Procedures via alias** : Besoin CLI nommée (ex: `lupo-test-boot`, `vetalyx-fiche-spots`). À formater.
2. **Terminal RPI access** : Clarifier constraints (SSH ok, exec local non?). Documenter workaround.
3. **Fiches spots workflow** : Formalisé en procédure écrits avant tests réels.
4. **Fiche Dante audit** : Vérifier si défaut global ou ponctuel avant rollout.

### 🤝 ORGANISATIONNELLEMENT
1. **Partenaire Alain Bosseloir** : Point stratégique Vetalyx Belgique → suivi à noter.
2. **Diaho Chinese capital** : 40% capital, UCM Belgique avis reçu → impact juridique clarifier avant actions.
3. **Dates clés** : Lupo "31 août" (reporté?), tests live "quelques jours" (baseline = 2026-09-30?).

---

## Recommandations

### 🔴 IMMÉDIAT (< 24h)
1. **Diagnostic RPi 5 SQUASHFS** : SSH → `fsck.squashfs /mnt`, identifier corruption. Backup/restore SD si nécessaire.
2. **Nettoyer Home Assistant UUID conflict** : SSH → vérifier `/etc/machine-id`, restaurer sauvegarde propre OU réinstaller OS.
3. **Débloquer terminal RPI** : Documenter exact constraint (permissions? GPU memory? SSH tunnel required?). Fournir workaround.

### 🟡 COURT TERME (3-5 jours)
1. **Créer issue tracker** pour each décision verbale. Format minimal : titre + contexte + décision + deadline.
2. **Standardiser notation métier** : Glossaire (L(M), ZH, assiette, etc.) + insérer dans AGENTS.md ou wiki.
3. **Audit fiche Dante** : Script pour vérifier toutes fiches, detector pattern vide. Root cause (permission? template?) + fix global.
4. **Formaliser procédure fiches spots** : Flowchart + checklist + test case avant live.

### 🟢 MOYEN TERME (1-2 semaines)
1. **Context separation** : Dédier sessions par domaine (IoT tech, juridique, mécanique). Réduire cognitive load.
2. **CLI procedures** : Créer namespace (ex: `jch-lupo-*`, `jch-vetalyx-*`). Documenter en bin/ avec help texte.
3. **Rapport expert Ollama** : Intégrer recommandations dans AGENTS.md sous "RPi5_LLM_config".
4. **Suivi partenaire** : Calendar + tracker Alain Bosseloir meeting, Diaho capital decisions.

### 🔵 STRUCTUREL
1. **PKA maintenance** : Session replay = fragments. Intégrer phase "synthesis + formalization" en fin chaque session.
2. **Dobby tuning** : Extraire mieux patterns "question non résolue = recurre 2x". Automatiser escalade.
3. **Credentials hygiene** : Audit mosquitto/HA access. Revoke duplicates, générer tokens frais (TTL 24h mention is clue).

---

**Signature** : Dobby PKA | 2026-09-26 | Scan 2 sessions, 1084 échanges.  
**Prochaine review** : 2026-09-30 (post-tests LUPO live).

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 26
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 26
- **Taux : 0.0%**

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

- [Decision] | Optimisation du workflow de traitement | Actée |
- [Decision] | Analyse de contenu visuel en attente | En cours |
- [Decision] | Conception mécanique : pas de demande client sur fixations individuelles | Validée |
- [Decision] | Configuration réseau / batterie pour remote pilotage | À confirmer |
- [Decision] | Diagnostic de stabilité système après instabilité détectée | À exécuter |
- [Decision] | Workflow de gestion des emplacements (Vetalyx) | En attente de formalisation |
- [Decision] | Fiches validées → tests réels quelques jours après | Planifié |
- [Decision] | Point stratégique Vetalyx Belgique | En attente |
- [Failure] RPi 5 bloqué en phase init matériel** : Système reste figé au démarrage, impossible de progresser vers OS. Suspect : conflit SQUASHFS sur nvme0n1p5 (`
- [Failure] Erreur duplicate_os_install + AppManager.install blocked** : Deux instances Home Assistant détectées → conflits UUID/réseau. Indique restauration sauv
- [Failure] Connexion SSL/TLS fail** : Erreur 404 combinée à secure connection fail → certificats ou endpoint misconfigurés.

### Fréquence des patterns (14 jours)
- **Recurring question** : 3 jours, 12 occurrences
- **Failure** : 2 jours, 14 occurrences
- **Question** : 2 jours, 14 occurrences
- **Decision** : 1 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 11
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**416** recommandations au total — **416** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 372
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5

### Plus récentes ouvertes

- [id=414] (2026-09-26) **Dobby** : Diagnostic RPi 5 SQUASHFS** : SSH → `fsck.squashfs /mnt`, identifier corruption.
- [id=415] (2026-09-26) **Dobby** : Nettoyer Home Assistant UUID conflict** : SSH → vérifier `/etc/machine-id`, rest
- [id=416] (2026-09-26) **Dobby** : Débloquer terminal RPI** : Documenter exact constraint (permissions? GPU memory?
- [id=411] (2026-09-25) **Furet** : Créer diagnostic.md** (template) pour capturer les outputs `exec_shell` + analys
- [id=412] (2026-09-25) **Dobby** : Fix NVMe Lupo** : Reproduire erreur SQUASHFS, tenter mount avec options alternat

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
