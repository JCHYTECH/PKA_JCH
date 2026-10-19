---
date: 2026-08-18
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1089
modeles: <synthetic>, claude, deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-18

**Sessions analysées :** 3 | **Échanges :** 1089 | **Modèles :** <synthetic>, claude, deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA - SESSION 2026-08-18

## Décisions prises

1. **Modèles LLM sur RPi5** : Passer aux SLM (Small Language Models) quantisés Q4_K_M via Ollama pour l'optimisation de performance sur RPi5 8Go.
2. **Factorisation de la sphère de travail** : Arrêter la demande unitaire de fixation des éléments ; grouper en sphère pour simplifier les tests en conditions réelles "dans quelques jours".
3. **Niveau iOS** : Utiliser le niveau disponible natif sur iPhone (pas de requête externe).
4. **Lupo-RPi : gel du setup** : Retour à lupo-rpi pour figer la configuration matérielle (sauf SD endurance + silent-bloc RPi à installer).
5. **Vetalyx Belgique** : Intégration capitalistique chinoise (DIaho) à 40% sans rôle opérationnel ; déclaration actionnaire via UCM Belgique confirmée acceptable.
6. **Documentation manquante** : Créer fichier `.md` pour documenter les situations d'échec et les pistes testées.
7. **Reporting lupo-rpi** : Reporter au 31 août.

---

## Échecs ouverts / bloqueurs

### Critiques
- **RPi5 boot bloqué** : Raspberry Pi 5 reste figé lors de l'initialisation matérielle (phase early boot), cause indéterminée.
- **SQUASHFS superblock introuvable** : `ls /mnt/mount` → erreur `fsconfig()` sur nvme0n1p5 — le filesystem n'est pas reconnu. **Impact potentiel** : restauration HA OS partiellement échouée.
- **Conflit d'instance HA** : Détection d'une instance Home Assistant OS existante (UUID dupliqué ou sauvegarde non complètement restaurée) bloquant le démarrage complet.
- **SSH / Terminal RPi inaccessible** : Connexion établie puis fermée (`Broken pipe`), terminal RPI non disponible pour travail direct.

### Majeurs
- **Download interrupted** : Téléchargement de `haos_rpi5-64-18.1.img.xz` interrompu (timeout réseau, 6 MB / 347 MB). Retry en cours mais instabilité réseau détectée.
- **Ctrl+C non fonctionnel sur RPi** : Incapacité à interrompre les processus localement.
- **Ctrl+M n'affiche que "m"** : Shortcut clavier mal mappé/interprété (terminale ou locale ✗).
- **team.db inaccessible** : Base de données d'équipe en état inconsistent/locked (autre instance active ?).

### Secondaires
- **Whisper inopérant** : Pas de transcription audio ; diagnostic incomplet (VSCode vs CLI ?).
- **Vanroll test silencieux** : N'émet plus de données — cause non documentée.
- **404 réseau** : Endpoint manquant, contexte insuffisant.

---

## Questions récurrentes (signe de lacune documentaire)

1. **"C'est quoi le ZH ?"** *(posé 2x)* → Acronyme mal défini. Probablement "Zero Hour" ou "Zone Hack" ? **Action** : créer glossaire.
2. **"Pourquoi tu n'as pas accès au terminal RPi ?"** *(3 variations)* → Diagnostic de connectivité réseau incomplet. Pas de workflow clarifié pour remote SSH sur RPi dégradée.
3. **"team.db pourquoi inaccessible ?"** *(2x)* → Absence de procédure de recovery pour base verrouillée (autre instance HA en marche ?).
4. **"L(M) c'est quoi ?"** → Notation non expliquée (log level ? model capacity ?).
5. **"Pourquoi il boot ?"** → Formulation ambiguë. Intent : "Pourquoi ça démarre ?" ou "Pourquoi ça NE démarre pas ?" → Clarifier le rapport d'erreur.
6. **"State files c'est quoi ?"** → Contexte HA OS : fichiers de persistance non expliqués.
7. **"Whisper ne fonctionne pas"** *(3x contextes)* → Flottement entre VSCode, terminal, CLI Ollama. Pas d'arbre de debug clair.
8. **"Vanroll test pourquoi plus de données ?"** → Pas de logging centralisé pour audit.

**Diagnostic** : **Documentation PKA fragmentée**. Les termes métier, les acronymes internes, et les workflows de dépannage restent oraux. Risque de re-travail.

---

## Nouveaux patterns détectés

### Patterns de décision
- **Décisions reportées à tests réels** : JCH prend des décisions avec validation "dans quelques jours" mais sans jalons explicites. Risque de dérive temporelle.
- **Escalade vers experts externes** : Consultation d'experts LLM/RPi avant tests → bon signal d'apprentissage, mais pas de feedback loop documenté.

### Patterns d'inefficacité
- **"On tourne en rond"** explicite : Session reconnue comme boucle infinie → arrêt et création fichier `.md` de débriefing.
- **Switching de contexte élevé** : VetalyX Belgique (stratégie capitalistique) → RPi5 (hardware) → Whisper (audio) → Home Assistant (infra) en ~1h. Pas de batching par domaine.
- **Absence de DRI (Directly Responsible Individual)** : Questions "pourquoi" sans owner clair → réponses flottantes (Dobby, Jade, Renard non assignés).

### Patterns technologiques
- **Network instability bottleneck** : Téléchargements interrompus, SSH timeouts, réseau local fragile. Pas de mesh network ou failover documenté.
- **Dual-boot / multi-instance confusion** : Conflits Home Assistant OS (UUID dupliqué). Suggest: versioning et backup isolation.
- **SLM vs LLM trade-off reconnu** : Passage de gros modèles à quantisés = acknow du constraint RPi (8 Go), mais pas encore benchmarké localement.

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Rapid escalation to expert** : Consultation rapide d'expert LLM → recommandations structurées (Q4_K_M GGUF, Ollama) en < 30 min.
- **Multi-tool orchestration** : DeepSeek TUI + Claude Code + Codex CLI utilisés en parallèle = flex adaptatif selon contexte.
- **Self-awareness of loop** : JCH reconnaît explicitement "on tourne en rond" et décide d'arrêter → discipline d'arrêt bon.
- **Business-tech separation attempt** : VetalyX Belgique traité en parallèle avec lupo-rpi (pas d'entrelacement).

### ❌ Inefficacités
- **Offline diagnosis impossible** : RPi bloquée au boot → pas d'accès à logs / telemetry → aveuglement diagnostique.
- **Redundant troubleshooting** : SSH timeouts, puis retry identique sans variation (wget avec --timeout ?).
- **No async task queue** : Tests "dans quelques jours" sans caldrier, assignation ou reminder system.
- **Acronym soup** : ZH, L(M), state files, SLM — chaque terme re-demandé × 2-3 → coût cognitif répété.
- **Locale warning ignorée** : Debian `LC_CTYPE=UTF-8` misconfigured sur RPi, symptôme d'setup incomplet, pas escaladé.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### État critique
1. **Lupo-RPi en impasse** : RPi5 stuck early boot + SQUASHFS error = likely image corruption ou mauvais burn. **Action prochaine** : re-flash HAos 18.1 depuis macOS (vérifier checksum).
2. **Home Assistant instance conflict** : UUID dupliqué ou sauvegarde fantôme active. **Prérequis avant reboot** : `avahi-browse -a` + netstat pour identifier instances concurrentes.
3. **Network instability** : Wget timeouts sur download image → considérer mirror local ou USB transfer.

### Domaines de travail
- **VetalyX Belgique** : Actionnariat chinois (DIaho 40%) documenté auprès UCM ✓. Pas de blocage légal mais **à formaliser juridiquement avant tranche capitalistique**.
- **Whisper non-fonctionnel** : Audio transcription cassée (contexte VSCode/CLI unclear). **Diagnostic manquant** : vérifie model download, GPU/CPU allocation.
- **Vanroll test silencieux** : Dernier log timestamp ? Process crashed ou network disconnect ?

### Glossaire manquant
Créer fichier `JCH_Inbox/00_GLOSSAIRE.md` avec :
- **ZH** : (?) — à clarifier
- **L(M)** : (?) — notation modèle ?
- **SLM** : Small Language Model (quantisé)
- **State files** : Persistance HA (config.yaml snapshots)
- **DRI** : Directly Responsible Individual
- **Q4_K_M** : GGUF quantization format

---

## Recommandations

### 🔴 Urgent (avant 31 août)
1. **Re-flash lupo-rpi** :
   - Télécharger `haos_rpi5-64-18.1.img.xz` complet (mirror ou USB).
   - Brûler sur SD avec `balena-etcher` + vérification checksum.
   - Brancher RPi5 seule (pas d'autres périphériques) et log les premier 5 min de boot sur HDMI.
   - Documenter first error → ouvrir issue.

2. **Killer questions à clarifier** :
   - ZH = ? (demander définition formelle).
   - L(M) = ? (contexte modèle ou log level).
   - Whisper failure = VSCode plugin ou CLI Ollama ?
   - Vanroll test = checksum données ou network disconnect ?

3. **Créer PKA living document** :
   ```
   JCH_Inbox/00_PKA_LIVING.md
   - Session date & attendees
   - Decisions & owners
   - Blockers & deadlines
   - Glossary (updatable)
   - Next sync date
   ```

### 🟡 Court-terme (1-2 semaines)
4. **Assign DRI par domaine** :
   - **Hardware (lupo-rpi)** : Dobby (orchestration), Renard (RPi expert ?)
   - **HA OS** : Jade (config) ?
   - **Whisper/Audio** : Bruno (TTS specialist ?)
   - **Business (Vetalyx)** : JCH (CEO) + Vasco (legal ?)

5. **Setup resilience** :
   - Backup HA OS config avant reboot (snapshot à `/mnt/backup`).
   - Multi-instance detection script : `avahi-browse -a | grep "Home Assistant"`.
   - Network resilience : test `--timeout 30` sur wget, considérer rsync local.

6. **Automation** : Créer Makefile ou shell script pour :
   ```bash
   make lupo-diagnosis  # Collecte logs + state

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 29
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 29
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

- [Decision] : Passer aux SLM (Small Language Models) quantisés Q4_K_M via Ollama pour l'optimisation de performance sur RPi5 8Go.
- [Decision] : Arrêter la demande unitaire de fixation des éléments ; grouper en sphère pour simplifier les tests en conditions réelles "dans quelques jours".
- [Decision] : Utiliser le niveau disponible natif sur iPhone (pas de requête externe).
- [Decision] : Retour à lupo-rpi pour figer la configuration matérielle (sauf SD endurance + silent-bloc RPi à installer).
- [Decision] : Intégration capitalistique chinoise (DIaho) à 40% sans rôle opérationnel ; déclaration actionnaire via UCM Belgique confirmée acceptable.
- [Decision] : Créer fichier `.md` pour documenter les situations d'échec et les pistes testées.
- [Decision] : Reporter au 31 août.
- [Decision] Modèles LLM sur RPi5** : Passer aux SLM (Small Language Models) quantisés Q4_K_M via Ollama pour l'optimisation de performance sur RPi5 8Go.
- [Decision] Factorisation de la sphère de travail** : Arrêter la demande unitaire de fixation des éléments ; grouper en sphère pour simplifier les tests en condit
- [Decision] Niveau iOS** : Utiliser le niveau disponible natif sur iPhone (pas de requête externe).
- [Decision] Lupo-RPi : gel du setup** : Retour à lupo-rpi pour figer la configuration matérielle (sauf SD endurance + silent-bloc RPi à installer).
- [Decision] Vetalyx Belgique** : Intégration capitalistique chinoise (DIaho) à 40% sans rôle opérationnel ; déclaration actionnaire via UCM Belgique confirmée acc
- [Decision] Documentation manquante** : Créer fichier `.md` pour documenter les situations d'échec et les pistes testées.
- [Decision] Reporting lupo-rpi** : Reporter au 31 août.
- [Failure] RPi5 boot bloqué** : Raspberry Pi 5 reste figé lors de l'initialisation matérielle (phase early boot), cause indéterminée.
- [Failure] SQUASHFS superblock introuvable** : `ls /mnt/mount` → erreur `fsconfig()` sur nvme0n1p5 — le filesystem n'est pas reconnu. **Impact potentiel** : rest
- [Failure] Conflit d'instance HA** : Détection d'une instance Home Assistant OS existante (UUID dupliqué ou sauvegarde non complètement restaurée) bloquant le dé
- [Failure] SSH / Terminal RPi inaccessible** : Connexion établie puis fermée (`Broken pipe`), terminal RPI non disponible pour travail direct.

### Fréquence des patterns (14 jours)
- **Recurring question** : 4 jours, 13 occurrences
- **Question** : 3 jours, 16 occurrences
- **Decision** : 1 jours, 11 occurrences
- **Failure** : 1 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 18
- Jours d'observation : 5
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**397** recommandations au total — **397** ouvertes — **0** en cours — **0** terminées

⚠️ 365 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 354
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=383] (2026-08-18) **Dobby** : Re-flash lupo-rpi** :
- [id=384] (2026-08-18) **Dobby** : Télécharger `haos_rpi5-64-18.1.img.xz` complet (mirror ou USB).
- [id=385] (2026-08-18) **Dobby** : Brûler sur SD avec `balena-etcher` + vérification checksum.
- [id=386] (2026-08-18) **Dobby** : Brancher RPi5 seule (pas d'autres périphériques) et log les premier 5 min de boo
- [id=387] (2026-08-18) **Dobby** : Documenter first error → ouvrir issue.

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
