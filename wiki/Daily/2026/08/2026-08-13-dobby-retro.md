---
date: 2026-08-13
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1021
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-13

**Sessions analysées :** 2 | **Échanges :** 1021 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Session 2026-08-13 - PKA JCH

## Décisions prises

- **Validation et mise à jour des fichiers utiles** : JCH a décidé de valider et mettre à jour tous les fichiers pertinents du système, avec documentation complète.
- **Mise en mémoire système** : Les décisions actuelles sont archivées pour tests réels prévus dans quelques jours.
- **Redémarrage du Lupo-RPi en isolation** : Décision de tester le redémarrage du Lupo-RPi seul pour vérifier la restauration complète.
- **Facteur forme sphérique validé** : Abandon de la fixation manuelle unitaire ; validation d'une approche en facteur forme sphérique pour déploiement.
- **Abandon de boucle d'itération** : "On va arrêter là, on tourne en rond" → création d'un fichier `.md` de synthèse imposée.
- **Utilisation de l'iPhone comme référence de niveau** : Utilisation du niveau disponible nativement sur iPhone pour étalonnage.
- **Reportage Lupo au 31 août** : Tâche reportée officiellement.

## Échecs ouverts / bloqueurs

### Critiques (blocage immédiat)
- **Raspberry Pi 5 bloqué en initialisation matérielle** : Le RPi reste suspendu au tout début du boot, phase matérielle non dépassée.
- **Erreur `AppManager.install` - Système non sain** : `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_instal` → impossibilité d'installer des packages. Cause présumée : ancienne instance HA active en arrière-plan (conflit UUID ou clonage de disque).
- **Whisper non fonctionnel** : Dysfonctionnement dans l'environnement VS Code, raison non identifiée à ce jour.
- **Fichier d'image manquant** : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory` → tentative de flashage échouée.
- **Accès `team.db` inaccessible** : Base de données critique non accessible, raison non documentée.

### Erreurs de téléchargement/connexion
- **Erreur SSL 404** : Connexion sécurisée échouée lors de téléchargement d'image Home Assistant OS.
- **Timeout réseau** : `Read error at byte 6059777/347121076 (Connection timed out)` → téléchargement interrompu, retry échoué.
- **Credentials Google invalides** : Identifiants et mots de passe issus de Google Keywords ne fonctionnent pas (source : ?).

### Incompréhensions techniques
- **"L(M) c'est quoi ?"** : Format de quantification GGUF mentionné (Q4_K_M) — absence de clarification sur notation.
- **États des fichiers de configuration** : "Lupo reporté au 31 août. C'est quoi les states files ?" → confusion sur la distinction entre fichiers d'état et de configuration.

## Questions récurrentes (signe de lacune documentaire)

| Question | Occurrences | Implication |
|----------|-------------|------------|
| "Pourquoi `team.db` est inaccessible ?" | 2+ | Absence de documentation d'accès/permissions |
| "Whisper ne fonctionne pas ; pourquoi on est dans VS Code ?" | 2+ | Configuration VS Code non documentée pour audio |
| "Pourquoi pas d'accès terminal RPi ?" | 2+ | Configuration SSH/réseau instable ou oubliée |
| "Pourquoi il boot ?" | 2+ | Comportement non déterministe du RPi5 |
| "Quelle différence Lupo/Assiette vs Esneux/iPhone ?" | 1+ | Absence de schéma d'architecture/instances |
| "C'est quoi les states files ?" | 1+ | Terminologie HA non clarifiée |
| "Vanroll test ne donne plus de données — pourquoi ?" | 1+ | Suite de test régression sans documentation de baseline |

**Signal fort** : Les trois premières questions tournent sur **accès/permissions, configuration outils, connexion réseau**. Absence manifeste de documentation d'infrastructure.

## Nouveaux patterns détectés

1. **Itération infructueuse** : JCH entre en boucle diagnostic sans avancer → nécessité de "casser la boucle" par création de fichier `.md`. Pattern : approche par essai-erreur plutôt que par hypothèse/test structuré.

2. **Conflit d'instances HA non résolu** : L'erreur `duplicate_os_install` revient ; suggestion d'expert reçue (restauration/clonage/UUID dupliqué) mais JCH ne documente pas la décision de résolution.

3. **Téléchargements instables** : Trois échecs réseau (SSL, 404, timeout) sur une même image — absence de stratégie de retry/cache/checksum documentée.

4. **Consultation d'experts externes** : JCH interroge "un expert" sur config LLM/RPi5 → information reçue (SLM + Ollama + Q4_K_M GGUF) mais pas intégrée dans PKA.

5. **Mélange contexte technique + stratégique** : Même session couvre RPi5 boot, Home Assistant, Whisper, et structuration VETALYX Belgique avec actionnaires chinois (UCM legal) → pas de séparation domaine → fatigue cognitive.

6. **Facteur d'erreur critique ignoré** : "Observer l'importance de ton erreur : un facteur 3. Cela peut tuer une décision sur un projet" → JCH reconnaît l'enjeu mais ne crée pas de process de validation. Exemple : image 64-bit vs résolution finale → non clarifié.

## Efficacités / inefficacités

### ❌ Inefficacités détectées
- **Diagnostic sans logging** : Erreurs SSH, boot RPi, accès réseau diagnostiqués verbalement ; aucun fichier de log structuré n'est extrait ou analysé.
- **Outils non synchronisés** : Claude Code, DeepSeek TUI, Codex CLI utilisés → aucune état partagé → redécouverte des mêmes problèmes.
- **Questions répétées non pré-répondues** : "Pourquoi `team.db` inaccessible ?" posée 2+ fois → absence de FAQ/runbook.
- **Décisions verbales non timestampées** : "On va essayer", "Fais le 1", "Ça va redémarrer comme" → flou sur ordre des actions.
- **Expert consulté, mais info perdue** : Recommandations SLM/Ollama/Q4_K_M reçues, pas d'action ensuite ni d'archivage structured dans PKA.

### ✅ Efficacités conservées
- **Escalade rapide à expert** : JCH reconnaît blocage et cherche avis externe → bon signal.
- **Arrêt de boucle intentionnel** : "On tourne en rond, créer un fichier `.md`" → capacité d'auto-correction.
- **Entités bien tracées localement** : Dobby détecte 95 mentions RPi, 39 mentions Dobby → couverture de sujet bon.
- **Multi-outils orchestrés** : Passage Claude → DeepSeek sans perte apparente → orchestration fonctionnelle.

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Blocages ouverts (action requise)
1. **RPi5 boot suspendu** — Diagnostic : vérifier phase matérielle (LED, UART serial), pas seulement SSH.
2. **Conflit HA `duplicate_os_install`** — Résolution : identifier UUID de l'ancienne instance via `blkid` avant réinstall ; ou forcer purge disque (`wipefs -a`).
3. **`team.db` inaccessible** — Vérifier : permissions, chemin absolu, instance HA active, ou lockfile stale.
4. **Téléchargement image instable** — Action : utiliser mirror/cache local, valider checksum SHA256, ou télécharger via curl avec retry (`--retry 5`).

### 📋 Décisions à formaliser
- **Format sphérique validé** : documenter dans `VETALYX/hardware/design.md`.
- **Lupo reporté 31 août** : ajouter dépendances (states files clarification, silent bloc, SD endurance).
- **Niveau iPhone utilisé** : enregistrer procédure de mesure (photo angle, GPS localisation).
- **SLM + Ollama sur RPi5 8Go** : créer `setup_llm_rpi5.sh` et tester Q4_K_M quantization.

### 🧠 Améliorations PKA requises
- **FAQ "Accès infrastructure"** : template pour SSH, team.db, HA instance config.
- **Diagramme d'architecture** : Lupo-RPi vs Esneux-iPhone vs assiette vs instances HA (distinct ou shared ?).
- **Glossaire HA** : states files, AppManager, UUID, duplicate_os_instal.
- **Log structure** : chaque test RPi → fichier `rpi_boot_log_YYYYMMDD.txt` avec timestamps.
- **Checklist téléchargement** : image → sha256, extraction, validation, avant flashage.

### 📌 Contexte stratégique retenu
- **VETALYX Belgique** : capital 10k€, actionnaire chinois DIaho 40%, pas de personnel chinois opérationnel, déclaration requise probablement (UCM avis incomplet dans transcript).
- **Camping sauvage / installations privées** : cas d'usage clé pour wildnexus/IOT (fermes...).
- **M5 référence** : confiance in M5 (34 mentions) pour tests de validation.

## Recommandations

### Priorité 1 (cette semaine)
1. **Créer runbook RPi5 boot diagnostique** : UART serial output, vérifier alim stable (multimètre), logs kernel avec `dmesg`, pas juste SSH.
2. **Résoudre `duplicate_os_install` définitivement** : tester `wipefs -a /dev/sdX` avant réinstall HA OS 18.1, valider UUID unique post-boot.
3. **Documenter `team.db` accès** : path exact, permissions, instance HA responsable, failover strategy.
4. **Arrêter consultation experts sans archivage** : si expert donne advice (SLM/Q4_K_M/Ollama), créer issue GitHub ou fichier `.md` directement, **pas d'info perdue**.

### Priorité 2 (avant 31 août)
1. **Créer `architecture.md`** : schéma clair instances HA, réseau (192.168.x.x ?), Tailscale, MQTT/Mosquitto, rôles M5 vs RPi vs iPhone.
2. **Standardiser test logging** : chaque tentative boot/install → fichier structuré (JSON ou Markdown table) avec timestamp, erreur exacte, command exacte.
3. **Automation téléchargement** : script bash avec retry, checksum, extraction — plus de "failed to open .img".
4. **Tester SLM sur RPi5** : une fois boot stable, exécuter setup

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 30
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 30
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

- [Decision] Validation et mise à jour des fichiers utiles** : JCH a décidé de valider et mettre à jour tous les fichiers pertinents du système, avec documentation
- [Decision] Mise en mémoire système** : Les décisions actuelles sont archivées pour tests réels prévus dans quelques jours.
- [Decision] Redémarrage du Lupo-RPi en isolation** : Décision de tester le redémarrage du Lupo-RPi seul pour vérifier la restauration complète.
- [Decision] Facteur forme sphérique validé** : Abandon de la fixation manuelle unitaire ; validation d'une approche en facteur forme sphérique pour déploiement.
- [Decision] Abandon de boucle d'itération** : "On va arrêter là, on tourne en rond" → création d'un fichier `.md` de synthèse imposée.
- [Decision] Utilisation de l'iPhone comme référence de niveau** : Utilisation du niveau disponible nativement sur iPhone pour étalonnage.
- [Decision] Reportage Lupo au 31 août** : Tâche reportée officiellement.
- [Failure] Raspberry Pi 5 bloqué en initialisation matérielle** : Le RPi reste suspendu au tout début du boot, phase matérielle non dépassée.
- [Failure] Erreur `AppManager.install` - Système non sain** : `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_instal` → imposs
- [Failure] Whisper non fonctionnel** : Dysfonctionnement dans l'environnement VS Code, raison non identifiée à ce jour.
- [Failure] Fichier d'image manquant** : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory` → tentative de flashage échouée.
- [Failure] Accès `team.db` inaccessible** : Base de données critique non accessible, raison non documentée.

### Fréquence des patterns (14 jours)
- **Recurring question** : 3 jours, 12 occurrences
- **Question** : 2 jours, 14 occurrences
- **Decision** : 1 jours, 11 occurrences
- **Failure** : 1 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 12
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**369** recommandations au total — **369** ouvertes — **0** en cours — **0** terminées

⚠️ 357 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 326
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=366] (2026-08-13) **Dobby** : Créer runbook RPi5 boot diagnostique** : UART serial output, vérifier alim stabl
- [id=367] (2026-08-13) **Dobby** : Résoudre `duplicate_os_install` définitivement** : tester `wipefs -a /dev/sdX` a
- [id=368] (2026-08-13) **Dobby** : Documenter `team.db` accès** : path exact, permissions, instance HA responsable,
- [id=369] (2026-08-13) **Dobby** : Arrêter consultation experts sans archivage** : si expert donne advice (SLM/Q4_K
- [id=358] (2026-08-07) **Dobby** : Snapshot diagnostic RPI 5** :

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
