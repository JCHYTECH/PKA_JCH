---
date: 2026-07-19
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1147
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-19

**Sessions analysées :** 2 | **Échanges :** 1147 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSION 2026-07-19 - Dobby PKA Analysis

## ⚠️ AVERTISSEMENT PRÉALABLE

Les données reçues sont **fortement dégradées et fragmentées**. Le transcript contient :
- Du bruit massif (contenu pharmaceutique non-pertinent sur Virbac/hydrocortisone)
- Des extraits de configuration sans contexte complet
- Des listes de composants électroniques isolées
- Des fragments d'erreurs système sans trace d'exécution cohérente

**Cette rétrospective s'appuie sur les patterns détectés localement, en compensant l'absence de transcript lisible.**

---

## Décisions prises

### Confirmées
1. **Redémarrage Lupo-RPi en mode minimal** : Test de bootstrap avec une SD d'endurance + silent blocs (amortissement vibrations)
2. **Transfert de contexte vers modèle plus développé** : Passage d'un assistant light vers configuration plus puissante (mention DeepSeek v4-pro)
3. **Gel temporaire du setup Lupo** : "Mets cela en mémoire, on fera des tests réels dans quelques jours"
4. **Validation à 100%** d'une configuration iphone (probablement niveau disponible/pression)
5. **Migration/déplacement de fichiers** : Vérification de l'endroit définitif

### Mal documentées
- La sélection du "niveau disponible" iPhone : quel paramètre ? quelle plage ?
- Les "tests en réel" annoncés : quelle date exacte ? quels KPIs ?
- Le modèle transféré : quelle architecture LLM pour RPi 5 ?

---

## Échecs ouverts / bloqueurs

### CRITIQUES
| Bloqueur | Symptôme | État | Priorité |
|----------|----------|------|----------|
| **Système de fichiers NVME** | `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` | Bloqué en lecture | 🔴 CRITIQUE |
| **Timeout Zigbee/NCP** | `ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` (2x mentionné) | Instable | 🔴 CRITIQUE |
| **Accès terminal RPi manquant** | "Pourquoi tu n'as pas accès au terminal rpi ?" (non résolu) | Bloqué | 🔴 CRITIQUE |
| **Ctrl+C non fonctionnel sur RPi** | Processus zombies impossibles à tuer | Bloquer | 🟠 MAJEUR |
| **Conflit instance HA** | UUID dupliqué / restoration mauvaise (mention en notes) | Conflit réseau | 🟠 MAJEUR |

### SECONDAIRES
- Whisper non fonctionnel en VSCode
- Base de données `team.db` inaccessible ("pourquoi ?")
- Téléchargement HAOS échoué (404 Not Found sur `.xz`)
- Identifiants Google (username/pass) invalides

---

## Questions récurrentes (signe de lacune documentaire)

### Haute fréquence (signe d'absence de doc claire)
1. **"Pourquoi on boot ? / pourquoi il boot ?"** ← Absence de flowchart de séquence d'amorçage RPi5
2. **"Pourquoi tu n'as pas accès au terminal RPi ?"** (x2) ← Lacune : schéma réseau + droits SSH non documentés
3. **"Pourquoi cette erreur (UUID/instance) ?"** (x2) ← Absence de guide troubleshooting Home Assistant
4. **"Comment faire en sorte que GM 5.2 ait le même bootstrap ?"** ← Manque : procédure de synchronisation bootstrap inter-devices

### Symptôme structural
- Les mêmes problèmes sont posés 2-3 fois sans réponse définitive
- Aucune référence à un document de dépannage existant
- Pattern : "rompt resumzant probleme et situation" → transfert à un modèle plus développé

---

## Nouveaux patterns détectés

### 1. **Cycle itératif non-convergent ("on tourne en rond")**
```
Problème → Test → Erreur → "mets cela en mémoire" → Pause → Test différent
```
Aucun point de terminaison clair pour les issues. Décision finale : créer `.md` documentant l'état.

### 2. **Dépendance à la relance de modèles**
- DeepSeek v4 → DeepSeek v4-pro (contexte insuffisant → escalade)
- Implique : fragmentation de l'état entre modèles
- Risque : perte de contexte à chaque transfert

### 3. **Bruit massif dans les inputs**
- Contenu non-pertinent (Virbac, hydrocortisone) mélangé à configuration technique
- Hypothesis : copy-paste depuis navigateur sans filtrage, ou contamination de historique
- Impact : inefficacité cognitive, dilution du signal

### 4. **Matériel en convergence lente**
- Lupo "terminé côté hardware" SAUF SD endurance + silent blocs (tâches restantes peu claires)
- M5 + RPi5 : configuration multi-agent, bootstrap non synchronisé
- 4 roues vs autre plus petit : **pas même d'accord sur la morphologie du système**

### 5. **Authentification + réseau fragile**
- Identifiants Google non valides
- MQTT unclear (mention "mqTT" sans contexte)
- Créds dans fichiers locaux (`.storage/core.config_entries`, `credentials-central.md`)

---

## Efficacités / inefficacités

### ✅ EFFICACITÉS OBSERVÉES
1. **Escalade intelligente** : Transfer vers modèle plus puissant quand contexte sature
2. **Décision rapide de freeze** : "On arrête là" → création de doc de synthèse
3. **Tri des tâches matérielles** : Identification claire (SD, silent blocs, HAT)
4. **Utilisation multi-outil** : DeepSeek TUI + Claude Code + Codex CLI (diversité acceptable)

### 🔴 INEFFICACITÉS CRITIQUES
1. **Pas de source unique de vérité (SSOT) pour l'état système**
   - Fichiers dispersés : `AGENTS.md`, `.storage/`, `TEAM_Inbox/`, `wiki/`
   - Aucune mention d'un "Status Board" centralisé
   
2. **Questions récurrentes non loggées**
   - "Pourquoi tu n'as pas accès ?" demandé 2x → pas de FAQ ou troubleshooting doc
   
3. **Bruit d'entrée masqué (contamination du transcript)**
   - ~20% du contenu est off-topic (pharmaceutique)
   - Pas de filtrage/validation avant ingestion PKA
   
4. **Cycle non-convergent**
   - Durée session : inconnue, mais multiple échanges sur mêmes blockers
   - Métrique : aucune
   
5. **Manque de **parity between M5 & RPi5**
   - "Comment faire en sorte que GM 5.2 ait le même bootstrap ?" → réponse absente
   - Implique : deux systèmes divergent en configuration

6. **Absence de timeline définie**
   - "Tests en réel dans quelques jours" → pas de date, pas de checklist

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### BLOQUEURS À RÉSOUDRE EN PRIORITÉ
- [ ] **Accès SSH/terminal RPi5** : Debugging root cause (réseau ? firewall ? clé SSH ?)
- [ ] **Superblock NVME manquant** : Vérifier partition map, relancer fdisk, restaurer image HAOS
- [ ] **Timeout Zigbee** : Analyser logs Home Assistant (`home-assistant.log`), vérifier débit série NCP
- [ ] **Ctrl+C paralysé** : Processus zombie → `pkill -9` ou restart daemon

### CONFIGURATION CRITIQUE
```yaml
Systems:
  Lupo-RPi5:
    CPU: ARM (8GB)
    Storage: NVME (config broken)
    Batterie: Geekworm HAT (à valider)
    Tâches restantes: SD endurance + silent blocs
    
  M5 (MacBook?):
    DeepSeek TUI active
    Bootstrap: ≠ RPi5 (gap documenté)
    
  Zigbee/MQTT:
    NCP reset errors recurring
    State: unstable
```

### DOCUMENTATION À CRÉER (IMMÉDIATEMENT)
1. **Flowchart d'amorçage** (boot sequence RPi5 + Home Assistant)
2. **Troubleshooting guide** (UUID conflicts, SSH access, NVME mount)
3. **Bootstrap parity checklist** (M5 ↔ RPi5 synchronisation)
4. **Architecture réseau diagram** (M5 → RPi5 → Zigbee/MQTT → HA)
5. **Status Board** : État actuel de Lupo, deadlines pour tests réels

### CONTRATS D'INTERFACE
- **Entre modèles** : Contexte JSON standardisé lors de transfert (évitera escalades inutiles)
- **Avec PKA** : Valider inputs AVANT ingestion (filtrer bruit pharmaceutique)
- **Avec matériel** : Checklist matériel signé avant "freeze"

---

## Recommandations

### 🎯 COURT TERME (Avant prochaine session)

1. **Créer un fichier `.md` de synthèse immédiatement**
   ```
   TEAM_Inbox/2026-07-19_dobby_etat-lupo-blockers.md
   ```
   Contenant :
   - État exact du NVME (output de `fdisk -l`)
   - Logs complets Home Assistant (dernière erreur Zigbee)
   - Trace complète d'accès SSH (ou blocage exact)
   - Checklist matériel signé

2. **Nettoyer le PKA d'entrée**
   - Implémenter filtrage : rejeter inputs contenant `<X% de mots clés non-tech>`
   - Valider qu'aucun contenu pharmaceutique ne rentre dans le repo PKA

3. **Tester accès RPi5 seul**
   ```bash
   ssh -v pi@<IP-RPi5> 2>&1 | tee ssh-debug.log
   ```
   Partager output brut à l'assistant suivant.

4. **Figer la date des "tests réels"**
   - Donner une date exacte
   - Définir 3 KPIs mesurables (uptime, latency Zigbee, CPU load)

### 📋 MOYEN TERME (1-2 semaines)

5. **Créer une Status Board centralisée**
   ```
   wiki/LUPO_STATUS.md
   - Dernière modification : auto-update depuis PKA
   - Sections : Hardware | Software | Network | Blockers | ETA fixes
   ```

6. **Implémenter "Bootstrap Sync Check"**
   - Script : compare M5 config avec RPi5 config
   - Output : JSON diff, blockers sur parity gaps
   - À exécuter avant chaque session

7. **Documenter l'architecture Zigbee/MQTT**
   -

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 46
- Résolus automatiquement : 8
- Résolus manuellement : 0
- Encore ouverts : 38
- **Taux : 17.4%**

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

- [Decision] : Test de bootstrap avec une SD d'endurance + silent blocs (amortissement vibrations)
- [Decision] : Passage d'un assistant light vers configuration plus puissante (mention DeepSeek v4-pro)
- [Decision] : "Mets cela en mémoire, on fera des tests réels dans quelques jours
- [Decision] d'une configuration iphone (probablement niveau disponible/pression)
- [Decision] : Vérification de l'endroit définitif
- [Decision] Redémarrage Lupo-RPi en mode minimal** : Test de bootstrap avec une SD d'endurance + silent blocs (amortissement vibrations)
- [Decision] Transfert de contexte vers modèle plus développé** : Passage d'un assistant light vers configuration plus puissante (mention DeepSeek v4-pro)
- [Decision] Gel temporaire du setup Lupo** : "Mets cela en mémoire, on fera des tests réels dans quelques jours
- [Decision] Validation à 100%** d'une configuration iphone (probablement niveau disponible/pression)
- [Decision] Migration/déplacement de fichiers** : Vérification de l'endroit définitif
- [Failure] | `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` | Bloqué en lecture | 🔴 CRITIQUE |
- [Failure] | `ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` (2x mentionné) | Instable | 🔴 CRITIQUE |
- [Failure] | "Pourquoi tu n'as pas accès au terminal rpi ?" (non résolu) | Bloqué | 🔴 CRITIQUE |
- [Failure] | Processus zombies impossibles à tuer | Bloquer | 🟠 MAJEUR |
- [Failure] | UUID dupliqué / restoration mauvaise (mention en notes) | Conflit réseau | 🟠 MAJEUR |

### Fréquence des patterns (14 jours)
- **Failure** : 9 jours, 57 occurrences
- **Decision** : 8 jours, 36 occurrences
- **Question** : 8 jours, 21 occurrences
- **Recurring question** : 7 jours, 21 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 15
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**314** recommandations au total — **314** ouvertes — **0** en cours — **0** terminées

⚠️ 253 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 272
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 4

### Plus récentes ouvertes

- [id=303] (2026-07-19) **Dobby** : Créer un fichier `.md` de synthèse immédiatement
- [id=304] (2026-07-19) **Dobby** : État exact du NVME (output de `fdisk -l`)
- [id=305] (2026-07-19) **Dobby** : Logs complets Home Assistant (dernière erreur Zigbee)
- [id=306] (2026-07-19) **Dobby** : Trace complète d'accès SSH (ou blocage exact)
- [id=307] (2026-07-19) **Dobby** : Checklist matériel signé

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $18.8 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $18.8**
