---
date: 2026-07-29
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1025
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-29

**Sessions analysées :** 2 | **Échanges :** 1025 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Sessions 2026-07-29 : Wildnexus & Infrastructure RPi

## 🎯 Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Pivot vers modèle plus robuste** | Problèmes de stabilité détectés, transfert du problème à un LLM plus puissant | Validée |
| **Figer le setup lupo-rpi** | Arrêt des itérations infinies, besoin de stabilisation urgente | En cours |
| **Redémarrage isolé lupo-rpi** | Validation du comportement sans dépendances externes | Planifiée |
| **Validation et mise à jour documentaire** | Synchronisation de tous les fichiers utiles + information des membres | Débutée |
| **Tests en conditions réelles** | Mémorisation pour exécution dans "quelques jours" | À planifier |
| **Ne pas forcer la saisie manuelle des facteurs de forme** | Architecture sphérique : pas d'ajout unitaire, approche par ensemble | Acceptée |

**Problème critique** : Les décisions sont **verbales et partielles**. Aucune décision n'a de document de suivi ou de date butoir claire.

---

## 🚨 Échecs ouverts / Bloqueurs

### Critiques (blocage immédiat)
1. **Home Assistant OS : Duplicate Instance Error**
   - Erreur : `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_instal`
   - Cause probable : Résidu d'ancienne installation ou UUID conflictuel
   - **Impact** : RPi5 inutilisable, HA ne peut pas s'initialiser
   - **Action requise** : Wipe complet du NVMe + réinstall propre

2. **Accès au terminal RPi bloqué**
   - SSH fonctionne par intermittence, connexion fermée inopinément
   - `Broken pipe` → instabilité réseau ou PSU insuffisante
   - **Impact** : Impossibilité de diagnostiquer en direct

3. **Téléchargement HAOS interrompu**
   - `dd: failed to open 'haos_rpi5-15.1.img': No such file or directory`
   - `Read error at byte 6059777/347121076 (Connection timed out)`
   - Fichier source manquant ou timeout réseau long
   - **Impact** : Cycle de tentatives sans fin

### Majeurs (fonctionnement dégradé)
4. **Whisper non fonctionnel**
   - Status inconnu, exécution bloquée dans vscode
   - Pas de diagnostic fourni
   - **Impact** : Voix non disponible

5. **SQUASHFS superblock error**
   - `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5`
   - Indique partition corrompue ou mauvais format
   - **Impact** : RPI ne démarre pas

6. **Ctrl+C non fonctionnel sur RPi**
   - Procédures d'arrêt d'urgence compromises
   - **Impact** : Risque de corruption à chaque intervention

7. **Alimentation insuffisante suspecte**
   - HAT Geekworm + RPi5 8Go + SSD NVMe : configuration gourmande
   - PSU_MAX_CURRENT=5000 noté mais validé ?
   - Symptôme : démarrages partiels, freezes, réinitialisation inopinée

### Mineurs (documentation / clarification)
8. **team.db inaccessible** – Cause non diagnostiquée
9. **Vanroll test ne retourne plus de données** – Régression silencieuse

---

## ❓ Questions récurrentes (lacunes documentaires)

| Question | Occurrences | Signification |
|----------|-------------|---------------|
| "Pourquoi ça boot ?" | 1× explicite, multiples implicites | Manque de documentation de la séquence de démarrage |
| "Quelle est la différence entre lupo/assiette et esneux/iphone ?" | 1× | **Absence totale de doc d'architecture instances** |
| "C'est l'instance HA ?" | Implicite répétée | Confusion des rôles (Ollama vs HA vs autres services) |
| "Gm 5.2 : comment avoir le même bootstrap ?" | 1× | Procédure d'harmonisation manquante |
| "Pourquoi pas d'accès terminal RPi ?" | 1× | Troubleshooting SSH absent |
| "L(M) c'est quoi ?" | 1× | Notation non définie |
| "Pourquoi vanroll test ne donne plus de données ?" | 1× | Monitoring / validation silencieux absent |

**Verdict** : **3 domaines critiques de documentation manquante** :
- Architecture instances (Wildnexus, HA, Ollama)
- Procédures de bootstrap et harmonisation
- Diagnostics SSH et réseau

---

## 🔍 Nouveaux patterns détectés

### Pattern 1 : "Pivot stratégique par fatigue"
```
Symptôme: Après N tentatives infructueuses → "on va transférer sur un modèle plus puissant"
Fréquence: Détecté lors de la transition vers DeepSeek pro
Risque: Dilution du contexte, perte de trace des troubleshooting tentés
```

### Pattern 2 : "Mémoire verbale sans trace"
```
Symptôme: "mets cela en mémoire car on va faire des tests en reel"
Contexte: Pas de fichier, pas de ticket, pas de dated
Résultat: Amnésie projet à la prochaine session
```

### Pattern 3 : "Commande CLI exploratoire → impasse**
```
Symptôme: Nombreux exec_shell() sans action de résolution
Exemple: grep sur credentials-central, find mosquitto.conf, ipconfig getifaddr
Résultat: Données collectées mais non triées / analysées
```

### Pattern 4 : "Hardware list (Mouser) sans intégration"
```
Symptôme: Affichage de composants achetés (microphones, IR emitters, inductors)
Absence: Allocation à un sous-projet, date de livraison, plan d'intégration
Risque: Stock fantôme
```

### Pattern 5 : "Locale misconfiguration bruit de fond"
```
Symptôme: Avertissements LC_CTYPE=UTF-8 sur RPi
Trivialité: Facilement réglable
Risque: Masque problèmes réels, pollue troubleshooting
```

---

## 📊 Efficacités / Inefficacités

### ✅ Efficacités

| Point | Justification |
|-------|---------------|
| **Escalade vers expert** | Consultation d'un expert LLM → recommandations SLM (Ollama Q4_K_M) reçues rapidement |
| **Multiples outils coordonnés** | DeepSeek + Claude + Codex CLI : bonne division du travail |
| **Verbosité contextuelle** | JCH explique l'environnement complet (RPi5 8Go, NVMe, Geekworm HAT) |
| **Tentatives de diagnostics matériels** | Recherche de la cause profonde (PSU, locale, UUID, partition) |

### ❌ Inefficacités

| Point | Impact | Sévérité |
|-------|--------|----------|
| **Pas de matrix RACI** | Dobby vs JCH vs expert : rôles flous | **Haute** |
| **Zéro docs écrits pendant session** | Décisions verbales, logs non structurés | **Critique** |
| **Téléchargement HAOS non atomique** | 347 Mo, timeout → relance manuelle | **Moyenne** |
| **Pas de rollback plan** | Si RPi5 crash → wipe total, pas de snapshot | **Haute** |
| **Contrôle d'état absent** | Pas de health-check entre tentatives | **Moyenne** |
| **Questions répétées** | Même diagnostic lancé 3-4× dans la session | **Moyenne** |
| **Outils CLI sans parsing** | Shell output → copié-collé, pas de struct data | **Moyenne** |

---

## 💾 Ce qu'il faut garder en mémoire pour les prochaines sessions

### Priorité 1 : État critique

```markdown
## RPi5 Lupo-Status [UNSTABLE - 2026-07-29]

**Current Issue:** Duplicate HA OS instance + SQUASHFS superblock error
**Last Action:** SSH intermittent, download timeout on haos_rpi5-15.1.img
**Hardware:** RPi5 8GB + NVMe SSD + Geekworm HAT (PSU capacity TBD)
**Next Action:** Full NVMe wipe + clean HAOS 18.1 install + isolated reboot test

**Questions Suspendues:**
- PSU adequacy: verify 5A capacity under full load (SSD + HAT + RPi5)
- Whisper status in vscode: TBD
- team.db access: root cause unknown
```

### Priorité 2 : Architecture non documentée

```markdown
## Instance Architecture (MANQUE DIAGRAM)

**Instances identifiées :**
- lupo-rpi : Home Assistant OS (RPi5 8GB + NVMe)
- esneux/iphone : ? (conflit non clarifié)
- assiette : ? (mention sans contexte)

**Rôles flous :**
- Ollama placement (local RPi? Central?)
- Wildnexus integration point (HA addon? Docker?)
- M5 / gm 5.2 relationship

**À clarifier en prochaine session**
```

### Priorité 3 : Décisions suspendues

```markdown
## Décisions à Valider

1. [ ] **Facteur de forme sphérique** : approche non-unitaire, validation architecture?
2. [ ] **Tests réels** : date butoir + environnement de test + critères de succès?
3. [ ] **Vanroll test** : régression silencieuse, à investiguer en priorité
4. [ ] **Bootstrap gm 5.2** : procédure d'harmonisation avec gm 5.x
```

### Priorité 4 : Composants en attente

```markdown
## Hardware En Stock (Status Mouser 2026-07)

- MEMS Microphones (I2S Digital) × 3, Backorder
- IR Emitters 940nm × 10, Backorder  
- PIR Sensors × 2, Backorder
- TPS62840DLC buck converter × ?, Backorder

**À-faire :** Allocation à Wildnexus sous-projet + date livraison estimée
```

---

## 📋 Recommandations

### 🔴 **IMMÉDIAT (avant prochaine session)**

1. **Sauvegarder l'état RPi5 complet**
   ```bash
   # Snapshot logique du NVMe avant wipe
   sudo blkid  # Documenter UUIDs
   sudo lsblk -o NAME,SIZE,TYPE,MOUNTPOINT > /tmp/blockdevices.log
   ```
   → Fichier : `JCH_Inbox/03_PROJECTS/11_IOT/lupo-rpi/2026-07-29_preWipe_state.log`

2. **Créer

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

*Aucun nouveau pattern découvert par le LLM aujourd'hui.*

### Fréquence des patterns (14 jours)
- **Decision** : 7 jours, 24 occurrences
- **Question** : 5 jours, 16 occurrences
- **Failure** : 4 jours, 30 occurrences
- **Recurring question** : 2 jours, 11 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 0
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**357** recommandations au total — **357** ouvertes — **0** en cours — **0** terminées

⚠️ 329 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 314
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=346] (2026-07-24) **Dobby** : Créer runbook SSH diagnostique** (MANQUANT)
- [id=347] (2026-07-24) **Dobby** : Vérifier santé RPI: ping lupo-rpi.local
- [id=348] (2026-07-24) **Dobby** : Si timeout: SSH via iphone bridge (procédure?)
- [id=349] (2026-07-24) **Furet** : Si toujours down: snapshot écran boot (HDMI) → analyse crash
- [id=350] (2026-07-24) **Dobby** : Dernier recours: wipe+reflash image (avec mirror URL)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
