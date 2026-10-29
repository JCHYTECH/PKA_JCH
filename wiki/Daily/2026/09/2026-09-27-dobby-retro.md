---
date: 2026-09-27
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 5
echanges: 1169
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-27

**Sessions analysées :** 5 | **Échanges :** 1169 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Sessions 2026-09-27 | JCH & Assistants

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Traiter les skip après, batch de 10** | Optimisation de traitement de données | À implémenter |
| **Procédure de fiches spots pour parking** | Nouvelle procédure opérationnelle | Documentée |
| **Discussion avec Alain Bosseloir** | Validation externe requise | En attente |
| **Rester en 12V pour procurement** | Architecture électrique Lupo-RPI | Validée |
| **Tests en "real" dans quelques jours** | Passage simulation → production | Planifié |
| **Retour à Lupo-RPI pour figer setup** | Consolidation matérielle | En cours |
| **Tests en life après validation fiches** | Validation finales avant go-live | Programmé |

**Problème critique** : Aucune de ces décisions n'est centralisée dans un registre de décisions. Elles sont dispersées dans le transcript. **Recommandation : créer un fichier `DECISIONS_2026-09.md` dans `JCH_Inbox/04_PILOTAGE_STRATEGIQUE`**.

---

## Échecs ouverts / bloqueurs

### 🔴 Critiques (bloquent le déploiement)

1. **Authentification Google Keywords défaillante**
   - Username/password ne fonctionnent pas
   - Cause non identifiée
   - Impact : impossible de procéder aux tests planifiés

2. **Raspberry Pi 5 bloqué en initialisation matériel**
   - Reste au premier boot sans progression
   - Diagnostic incomplet : "cou[pée]" dans le transcript
   - Piste testée : configuration HAT PSU (PSU_MAX_CURRENT=5000)
   - Impact : Lupo-RPI non fonctionnel

3. **Erreur SQUASHFS sur NVMe**
   ```
   /mnt: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5
   ```
   - Suggère une corruption de partition ou mauvaise image flash
   - Non résolu

4. **Home Assistant - Instance dupliquée / UUID en conflit**
   - "Restauration récente : une ancienne instance tourne encore"
   - Deux disques possèdent les mêmes UUID
   - AppManager refusée (système non healthy)
   - Impact : supervision du projet impossible

### 🟡 Majeurs (dégradation performance)

5. **Erreur SSL/TLS - Secure connection failed**
   - Cause non identifiée
   - Impact sur tests réseau

6. **VanRoll test ne donne plus de données**
   - Régression inexpliquée
   - Diagnostic requis

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Implication |
|----------|-----------|-------------|
| "C'est quoi les state files ?" | 2x | Concepts Home Assistant/IoT **mal documentés** |
| "Pourquoi tu ne peux pas travailler en terminal RPI ?" | 2x | Procédure de diagnostic manquante |
| "C'est quoi le ZH ?" | 1x | Acronyme non défini dans la documentation |
| "L(M) c'est quoi ?" | 1x | Notation technique inexpliquée |
| "VanRoll test : pourquoi pas de données ?" | 1x | Absence de troubleshooting guide |
| "Dimensions meuble : pourquoi 25-26cm ?" | Récurrente | Rationnel de conception non documenté |
| "Comment gérer les procédures via nom de trigger ?" | 1x | Architecture de commande floue |
| "TTL 24h : comment utiliser en HTML ?" | 1x | Absence de cookbook technique |

**Analyse** : Ces questions révèlent que la documentation technique (CLAUDE.md, AGENTS.md) n'est **pas consultée** ou est **incomplète**. Les assistants (Dobby, Jade, DeepSeek) ne disposent pas d'une source unique de vérité pour :
- Architecture Home Assistant / IoT
- Conventions de nommage (ZH, L(M), etc.)
- Procédures RPI (terminal, debug, etc.)

---

## Nouveaux patterns détectés

### 1. **Multiplexage projet-infrastructure**
JCH alterne brutalement entre :
- 🏢 **VETALYX** (légal, captable, stratégie chinoise)
- 🚐 **TRAVELS/VAN** (meuble, banquette, dimensions mécaniques)
- 🤖 **LUPO-RPI** (IoT, Home Assistant, Raspberry Pi)
- 🛒 **WildNexus** (implicite, peu détaillé)

**Impact** : contexte switching élevé, risque d'erreurs multiplicatif par 3 mentionné ("observe l'importance de ton erreur : un facteur 3").

### 2. **Diagnostic sans documentation des résultats**
Chaque blocage entraîne une investigation ad-hoc :
- Grep sur fichiers config
- Exec shell commands
- Lecture de credentials
- Mais **zéro rapport d'analyse produit**

JCH demande explicitement : "expliques la situation et l'échec actuel ainsi que les pistes testées" → **cela n'est jamais formalisé dans un fichier**.

### 3. **Dépendance non-technique (juridique, partenaire)**
- Décision Vetalyx + DIAHO + approche chinoise = validation externe (UCM Belgique)
- Décision Lupo-RPI = "discussion avec Alain Bosseloir"

**Problème** : ces dépendances ne sont **pas suivies dans un sprint board**. On ne sait pas quel est le statut de la réponse UCM ou si Alain a répondu.

### 4. **Simulation → Real Gap**
- "On va faire des simulations et je te reviens" 
- "On va tester en life et je te reviens"

**Risque** : les conditions de test réel (RF, métérologie, réseau) ne sont pas préfigurées. Les bloqueurs RPI + HA vont impacter le go-live.

---

## Efficacités / inefficacités

### ✅ Efficacités
1. **Multi-outils intégrés** : DeepSeek TUI + Claude Code + Codex CLI fonctionnent en tandem
2. **Dobby + Jade** : archivage et memory management fonctionnels (53 mentions Dobby)
3. **Extractions rapides** : grep, exec_shell, read_file lancés sans friction
4. **Validation rapide** : fiches spots validées, décisions prises sans blocage processus

### ❌ Inefficacités
1. **Pas de registre centralisé de décisions** → rediscussions
2. **Pas de rapport de diagnostic** → investigations répétées des mêmes erreurs
3. **Documentation technique dispersée** → questions récurrentes non résolues
4. **Pas de sprint board** → dépendances externes (Alain, UCM) non suivies
5. **Pas de post-mortem des erreurs** → "facteur 3 d'erreur" accepté sans amélioration systémique
6. **Terminal RPI bloqué** → diagnostic local impossible, dépendance en ligne sur DeepSeek/Claude

**Coût estimé** : ~30-40% de temps perdu à rediscuter ou chercher contexte.

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Bloqueurs critiques
- **RPI 5 stuck au boot** : valider que PSU_MAX_CURRENT=5000 + image flash sans corruption
- **Google Keywords auth** : obtenir credentials valides ou alternative
- **SQUASHFS error** : réimager l'NVMe avec checksums
- **Home Assistant UUID** : purger l'ancienne instance (cloner proprement)

### 📌 Architectural
- **Lupo-RPI = 12V seulement** : procurement figé à cet standard
- **Vetalyx = Belgique + DIAHO 40%** : structure légale finalisée, attendre réponse UCM + Alain
- **Van meuble = 25-26cm** : permet fermeture passager, dimensions critiques

### 🛠️ Procédures à documenter
1. **State files** (Home Assistant)
2. **ZH, L(M)** : notation technique
3. **Terminal RPI : troubleshooting checklist**
4. **VanRoll : diagnostic data pipeline**
5. **TTL 24h → HTML button** : cookbook

### 📊 Dépendances externes
- Alain Bosseloir : validation Lupo-RPI setup (statut : ?)
- UCM Belgique : avis structure VETALYX + DIAHO (statut : ?)
- Tests "real" : dans quelques jours → nécessite RPI + HA opérationnels

---

## Recommandations

### Immédiat (cette semaine)

1. **Créer registre de décisions**
   ```
   JCH_Inbox/04_PILOTAGE_STRATEGIQUE/DECISIONS_2026-09.md
   Format : | Décision | Date | Responsable | Statut | Deadline |
   ```

2. **Créer rapport de diagnostic RPI**
   ```
   JCH_PRIVATE/RPI5_DIAGNOSTICS_2026-09-27.md
   - Symptôme : stuck boot
   - Pistes testées : [PSU_MAX_CURRENT, ...]
   - Étapes suivantes : [checksums, réimage, ...]
   ```

3. **Créer sprint board (notion/obsidian)**
   - Tâches techniques (RPI, HA, VanRoll)
   - Tâches de dépendance (UCM, Alain, Google Auth)
   - Jalons : go-live date, tests real

4. **Documenter terminologie**
   ```
   wiki/GLOSSAIRE_TECHNIQUE.md
   - State files
   - ZH (Zone Helper ?)
   - L(M) (notation ?)
   ```

### Court terme (semaine prochaine)

5. **Créer checklist de diagnostic terminal RPI**
   ```
   docs/RPI_TERMINAL_TROUBLESHOOTING.md
   - Vérifier partition SQUASHFS
   - Checker logs systemd
   - Valider HAT PSU
   ```

6. **Planifier tests "real"**
   - Conditions pré-requises : RPI boot ✓, HA healthy ✓, Google auth ✓
   - Scénarios : [RF, latence, reliability]
   - Captation résultats automatisée

7. **Post-mortem error "facteur 3"**
   - Identifier quel error a eu impact 3x
   - Implémenter validation de checkpoint avant/après
   - (N'acceptez jamais un "facteur 3" sans rootcause)

### Long terme (avant go-live)

8. **Automation pipeline**
   - Registre décisions → notifications DeepSeek/Dobby
   - Dépendances externes → reminders (Alain, UCM)
   - Post-tests → rapport automatisé

9. **Memory système**
   ```
   Dobby : maintenir DECISIONS_2026-09.md + GLOSSAIRE
   Jade : archiver chaque rapport diagnostic
   DeepSeek : consulter DECISIONS avant

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 26
- Résolus automatiquement : 1
- Résolus manuellement : 0
- Encore ouverts : 25
- **Taux : 3.8%**

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

- [Decision] | Optimisation de traitement de données | À implémenter |
- [Decision] | Nouvelle procédure opérationnelle | Documentée |
- [Decision] | Validation externe requise | En attente |
- [Decision] | Architecture électrique Lupo-RPI | Validée |
- [Decision] | Passage simulation → production | Planifié |
- [Decision] | Consolidation matérielle | En cours |
- [Decision] | Validation finales avant go-live | Programmé |
- [Decision] : Aucune de ces décisions n'est centralisée dans un registre de décisions. Elles sont dispersées dans le transcript. **Recommandation : créer un fichi
- [Failure] Username/password ne fonctionnent pas
- [Failure] Cause non identifiée
- [Failure] Impact : impossible de procéder aux tests planifiés
- [Failure] Reste au premier boot sans progression
- [Failure] Diagnostic incomplet : "cou[pée]" dans le transcript
- [Failure] Piste testée : configuration HAT PSU (PSU_MAX_CURRENT=5000)
- [Failure] Impact : Lupo-RPI non fonctionnel
- [Failure] Suggère une corruption de partition ou mauvaise image flash
- [Failure] Instance dupliquée / UUID en conflit
- [Failure] Restauration récente : une ancienne instance tourne encore
- [Failure] Deux disques possèdent les mêmes UUID
- [Failure] AppManager refusée (système non healthy)
- [Failure] Impact : supervision du projet impossible
- [Failure] Authentification Google Keywords défaillante
- [Failure] Raspberry Pi 5 bloqué en initialisation matériel
- [Failure] Erreur SQUASHFS sur NVMe
- [Failure] Home Assistant - Instance dupliquée / UUID en conflit

### Fréquence des patterns (14 jours)
- **Failure** : 3 jours, 14 occurrences
- **Recurring question** : 3 jours, 12 occurrences
- **Decision** : 2 jours, 22 occurrences
- **Question** : 2 jours, 14 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 25
- Jours d'observation : 4
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**428** recommandations au total — **428** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 383
- **Forge** : 33
- **Furet** : 6
- **Corbeau** : 5
- **Sybil** : 1

### Plus récentes ouvertes

- [id=417] (2026-09-27) **Dobby** : Créer registre de décisions
- [id=418] (2026-09-27) **Sybil** : Créer rapport de diagnostic RPI
- [id=419] (2026-09-27) **Dobby** : Symptôme : stuck boot
- [id=420] (2026-09-27) **Dobby** : Pistes testées : [PSU_MAX_CURRENT, ...
- [id=421] (2026-09-27) **Dobby** : Étapes suivantes : [checksums, réimage, ...

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
