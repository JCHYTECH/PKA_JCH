---
date: 2026-07-09
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 6
echanges: 1566
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-09

**Sessions analysées :** 6 | **Échanges :** 1566 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSION 2026-07-09 — PKA DOBBY

## Décisions prises

1. **Migration vers OpenRouter pour Kimi** : validation de passage exclusif via OpenRouter pour les requêtes Kimi (vérification d'accès en cours)
2. **Report délai projets IR/Belgique** : reprogrammé au 30 juin (dates incohérentes dans les logs)
3. **Nettoyage fichiers système** : suppression `.bak-*`, vidage `.DS_Store` (8 instances), validation des `session_*.json`
4. **Transfert vers modèle avancé** : rupture sur problème détecté, escalade vers DeepSeek v4-pro
5. **Validation et mise à jour fichiers** : décision de valider et synchroniser tous les fichiers utiles (détails flous)
6. **Passage au projet Vetalyx** : déploiement pour société chinoise (contexte manquant)

**⚠️ CRITIQUE** : 3 décisions sur 6 sont **sous-documentées**. Les termes "on va", "on valide" sans ownership clair ni dates.

---

## Échecs ouverts / bloqueurs

### Bloqueurs critiques
- **Accès RPi bloqué** (répété 3x minimum)
  - `ctrl+c` ne fonctionne pas sur RPI
  - SSH timeout sur `lupo-rpi.local`
  - Accès terminal RPi non disponible depuis VS Code
  - Symptôme : `client_loop: send disconnect: Broken pipe`

- **Montage SQUASHFS échoué**
  - `/mnt: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5`
  - Tentative d'écriture image HAOS bloquée : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory`

- **Zigbee NCP reset échoué**
  - `NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT`
  - Impossible de créer nouveau réseau Zigbee

- **Whisper non fonctionnel**
  - Raison : "vérifie pourquoi on est dans vscode" (pas investigué)
  - État : NOT_ANALYZED

- **Téléchargement fichier 404**
  - `HTTP request sent, awaiting response... 404 Not Found` sur haos_rpi5-15.1.img.xz
  - Ressource manquante ou URL expirée

- **"Tout est bloqué"** (déclaration JCH sans détail spécifique)

### Symptômes d'infrastructure
- Working set fragmenté : accès inconsistant à `/Users/jchavauxm5/PKA_JCH`
- Historique Git volumineux (1,92 Go pack, binaires suspects)
- Health-check système en RED (faux positifs massifs documentés)

---

## Questions récurrentes (signe de lacune documentaire)

### T1. Accès RPi (répété 4+ fois)
```
- "pourquoi tu n'as pas accès au terminal rpi ?"
- "en attendant pourquoi tu ne peux pas travailler dans le terminal RPI ?"
- "pourquoi il boot ?"
```
**Interprétation** : Problème de connectivité RPi NON RÉSOLU, JCH revient dessus constamment.  
**Cause probable** : Pas de diagnostic root cause, solution vague ("attendre"), absence de workaround.

### T2. Configuration VS Code / OpenRouter (questions terminales)
```
- "explique moi comment utiliser openrouter dans l'interface de vs code et comment choisir un modele"
- "ca c'est la commande terminal c'est quoi la commande quand je suis dans un terminal vscode; c'est la meme ?"
```
**Interprétation** : JCH confond commandes terminal Bash ↔ VS Code CLI, manque de doc claire.  
**Cause** : Configuration OpenRouter dans VS Code n'est pas documentée (probablement).

### T3. Vocabulaire technique non défini (4x)
```
- "c'est quoi le X1201-C1 c'est celui ou on peut connecter le ssd ?"
- "c'est quoi harness"
- "memory nudge c'est quoi ?"
- "pourquoi ais je aussi (.env) en debut de path ?"
```
**Interprétation** : Références internes (hardware, patterns) jamais expliquées ou versionnées.  
**Cause** : Manque de **GLOSSAIRE** ou **HARDWARE_REFERENCE.md**.

### T4. Workflow logique (récurrent)
```
- "comment faire en sorte que tu puisses faire les recherches necessaires en entrant dans les si[...] de travail plus logique et pro"
```
**Interprétation** : JCH cherche à structurer le workflow assistant ↔ outils, pas de standard établi.

---

## Nouveaux patterns détectés

### Pattern 1 : "Attendre" comme décision par défaut
- `"on va attendre"` (3 instances minimum)
- `"report el delai au 30 juin"` (contradiction temporelle avec date de session)
- **Implication** : Blockers non escaladés, pas de plan B activé.

### Pattern 2 : Fragmentation multi-contexte
- **Projets parallèles actifs** : Vetalyx (Chine) + WildNexus (van) + Home Assistant + pharmaceutical (Virbac/Cortavance)
- **Outils changent dans le même échange** : Composer → DeepSeek → Claude → Kimi
- **Implication** : Context switching coûteux, perte de continuité mémoire.

### Pattern 3 : Mélange données opérationnelles ↔ historiques
- Extraits Virbac/pharmaceutique mélangés à logs RPi
- Factures Mouser (composants) dans transcript système
- **Implication** : Pas de séparation INPUT/OUTPUT, risque de hallucination documentaire.

### Pattern 4 : Escalade vers modèles plus puissants sans résolution
- "rompt résumant problème et situation, je vais te transférer sur un modèle plus développé"
- Aucune trace de débriefing final vers le modèle escaladé
- **Implication** : Perte de contexte, re-learning inutile.

### Pattern 5 : Nommage machine incohérent
- `RPi` (23x) / `rpi` (177x) / `Raspberry Pi` (36x) / `RPI` (23x) / `raspberrypi` (8x)
- `M5` (127x) / `m5` (12x) / `M1` (22x)
- **Implication** : Recherche mémoire compromise, parsing fragmenté.

---

## Efficacités / inefficacités

### ✅ Efficacités détectées
1. **Détection rapide de problèmes** : JCH identifie blockers vite (Zigbee fail, mount fail)
2. **Escalade modèle** : Décision de passer à v4-pro sur détection problème
3. **Nettoyage proactif** : Cleanup fichiers système planifié (.bak, .DS_Store)
4. **Utilisation multi-outils** : Mix DeepSeek + Claude + Kimi permet breadth (si coordonné)

### ❌ Inefficacités critiques
1. **Diagnostic incomplet** → pas de RCA (Root Cause Analysis)
   - Whisper failure : cause inconnue
   - RPi access : tout bloqué, 0 workaround
   - Zigbee reset : error code documenté, solution zéro

2. **Décisions floues sans ownership**
   - "on va" = qui ? deadline ? checkpoint ?
   - "mets à jour tous les fichiers utiles" = lesquels ? format ? review gate ?

3. **Context dilution**
   - 1566 échanges sur 6 sessions = 261 msg/session
   - Working set mal défini (fichiers "N/A", références HTML)
   - Memory continuit pas validée entre outils

4. **Absence de retry loops**
   - Blockers = "attendre" ou escalade
   - Zéro tentative de contournement documentée

5. **Ratio signal/bruit dans transcript**
   - Virbac pharmacie mélangée à logs RPi
   - Factures Mouser dans buffer système
   - → Indicateur de pollution mémoire à long terme

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Urgences non résolues
```
🔴 [BLOQUEUR] RPi connectivity down
   - SSH timeout on lupo-rpi.local
   - ctrl+c broken
   - Workaround needed: SSH key rotation? Network restart? DNS check?
   
🔴 [BLOQUEUR] HAOS image download 404
   - Fetch failed: haos_rpi5-15.1.img.xz
   - Need: alternative mirror or version rollback
   
🔴 [BLOQUEUR] Zigbee NCP reset with ACK timeout
   - Last error: NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT
   - Next: Check firmware, reset power sequence
   
🟡 [MEDIUM] Whisper integration broken in VS Code
   - Symptom noted, root cause not investigated
   - May be PATH/plugin issue
```

### État projet WildNexus (VAN)
- RPi5 assembly documentation exists: `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/ASSEMBLAGE-RPi5-VANLIFE.md`
- Hardware bill ongoing (Mouser backorders detected)
- Integration blocked on Zigbee network

### Nomenclature à standardiser
| Entité | Formes détectées | Recommandé |
|--------|------------------|-----------|
| Raspberry Pi | RPi, rpi, RPI, Raspberry Pi, raspberrypi | `rpi5` ou `lupo-rpi` (hostname) |
| MacBook | M5, m5, M1 | `jchavauxm5` (hostname) ou `m5-mac` |
| Model names | deepseek-v4, deepseek-v4-pro, claude, kimi | Utiliser versioning semver strict |

### Configurations oubliées/partielles
- **OpenRouter VS Code** : mode d'emploi manquant, config .env ambiguë
- **Terminal vs Code terminal** : commandes différentes, pas documentées
- **Harness** : référence technique non définie
- **Memory nudge** : pattern inconnu
- **X1201-C1 connector** : hardware reference flou

---

## Recommandations

### 🎯 IMMÉDIAT (avant session suivante)

1. **Diagnostic root cause RPi**
   ```
   [ ] Ping lupo-rpi.local (DNS alive ?)
   [ ] ssh -vvv test (log détaillé)
   [ ] Check /etc/hosts ou Tailscale routing
   [ ] Try SSH key rotation
   [ ] If no progress: fallback serial console
   ```
   → **Owner** : JCH ou Dobby (décider)
   → **Deadline** : 2026-07-10 EOD
   → **Exit criteria** : Shell accès OU documented workaround

2. **Résoudre HAOS image 404**
   ```
   [ ] Check Home Assistant mirror status
   [ ] Try alternative: download via RPI

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 50
- Résolus automatiquement : 5
- Résolus manuellement : 0
- Encore ouverts : 45
- **Taux : 10.0%**

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

- [Decision] : validation de passage exclusif via OpenRouter pour les requêtes Kimi (vérification d'accès en cours)
- [Decision] : reprogrammé au 30 juin (dates incohérentes dans les logs)
- [Decision] : suppression `.bak-*`, vidage `.DS_Store` (8 instances), validation des `session_*.json`
- [Decision] : rupture sur problème détecté, escalade vers DeepSeek v4-pro
- [Decision] : décision de valider et synchroniser tous les fichiers utiles (détails flous)
- [Decision] : déploiement pour société chinoise (contexte manquant)
- [Decision] : 3 décisions sur 6 sont **sous-documentées**. Les termes "on va", "on valide" sans ownership clair ni dates.
- [Decision] Migration vers OpenRouter pour Kimi** : validation de passage exclusif via OpenRouter pour les requêtes Kimi (vérification d'accès en cours)
- [Decision] Report délai projets IR/Belgique** : reprogrammé au 30 juin (dates incohérentes dans les logs)
- [Decision] Nettoyage fichiers système** : suppression `.bak-*`, vidage `.DS_Store` (8 instances), validation des `session_*.json`
- [Decision] Transfert vers modèle avancé** : rupture sur problème détecté, escalade vers DeepSeek v4-pro
- [Decision] Validation et mise à jour fichiers** : décision de valider et synchroniser tous les fichiers utiles (détails flous)
- [Decision] Passage au projet Vetalyx** : déploiement pour société chinoise (contexte manquant)
- [Failure] Accès RPi bloqué** (répété 3x minimum)
- [Failure] `ctrl+c` ne fonctionne pas sur RPI
- [Failure] SSH timeout sur `lupo-rpi.local`
- [Failure] Accès terminal RPi non disponible depuis VS Code
- [Failure] Symptôme : `client_loop: send disconnect: Broken pipe`
- [Failure] Montage SQUASHFS échoué
- [Failure] `/mnt: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5`
- [Failure] Tentative d'écriture image HAOS bloquée : `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory`
- [Failure] Zigbee NCP reset échoué
- [Failure] `NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT`
- [Failure] Impossible de créer nouveau réseau Zigbee
- [Failure] Whisper non fonctionnel
- [Failure] Raison : "vérifie pourquoi on est dans vscode" (pas investigué)
- [Failure] Téléchargement fichier 404
- [Failure] `HTTP request sent, awaiting response... 404 Not Found` sur haos_rpi5-15.1.img.xz
- [Failure] Ressource manquante ou URL expirée
- [Failure] "Tout est bloqué"** (déclaration JCH sans détail spécifique)

### Fréquence des patterns (14 jours)
- **Decision** : 8 jours, 34 occurrences
- **Question** : 8 jours, 26 occurrences
- **Failure** : 7 jours, 40 occurrences
- **Recurring question** : 6 jours, 19 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 30
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**245** recommandations au total — **245** ouvertes — **0** en cours — **0** terminées

⚠️ 183 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 208
- **Forge** : 30
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=241] (2026-07-09) **Dobby** : Diagnostic root cause RPi
- [id=242] (2026-07-09) **Dobby** : : JCH ou Dobby (décider)
- [id=243] (2026-07-09) **Dobby** : : 2026-07-10 EOD
- [id=244] (2026-07-09) **Dobby** : : Shell accès OU documented workaround
- [id=245] (2026-07-09) **Dobby** : Résoudre HAOS image 404

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **4 alerte(s) budget détectée(s)**

- OpenRouter   🔴 $0.2 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $0.2**
