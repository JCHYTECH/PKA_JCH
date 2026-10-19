---
date: 2026-09-24
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1032
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-24

**Sessions analysées :** 2 | **Échanges :** 1032 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 📋 Rétrospective Sessions 2026-09-24 | PKA JCH

**Période** : 2 sessions | 1032 échanges | Outils : DeepSeek v4, Claude, DeepSeek TUI  
**Entités principales** : Vetalyx (49x), RPi/M5 (97x), Dobby/Jade (65x)

---

## ⚡ Décisions prises

### Décisions claires et exécutables
1. **Infrastructure RPi** : Redémarrage isolé du `lupo-rpi` pour vérifier la stabilité post-initialisation
2. **Traitement des données** : Batch de 10 + traitement des skip en second pass
3. **Workflow de validation** : Drafts → Validés (d'abord) avant publication
4. **Approche relationnelle** : Questions polies préalables avant intervention corrective
5. **Vetalyx/Diaho** : Décision prise de consulter UCM Belgique sur la déclaration d'actionnaires chinois (40% capital)
6. **Test en live** : Tests hardware suivis de feedback avant poursuite

### Décisions *flou* ou incomplètes
- "Wican search" : terme non clarifié, contexte absent → **à documenter**
- "Niveau disponible iPhone" : quelle sélection exactement ? quel système ?
- Arrêt de la discussion avec instruction "créer .md" → **le fichier a-t-il été créé ?**
- Reprise du projet Vetalyx post-31 août : scope exact du redémarrage ? → **clarification nécessaire**

---

## ⛔ Échecs ouverts / Bloqueurs

### Bloqueurs matériels (RPi 5 - CRITIQUE)
| Problème | Impact | Status |
|----------|--------|--------|
| **Boot incomplet** | RPi 5 bloquée lors de l'init hardware (phase CPU thermals) | 🔴 OUVERT |
| **HAT PSU config** | `PSU_MAX_CURRENT=5000` non reconnu (ou mauvais format) | 🟡 PARTIEL |
| **Montage NVMe** | `fsconfig() failed: Can't find SQUASHFS superblock on nvme0n1p5` | 🔴 OUVERT |
| **SSH/terminal** | `Ctrl+C` non fonctionnel sur RPi / connexion instable | 🟡 DIAGNOSTIC INCOMPLET |
| **Locale settings** | `LC_CTYPE=UTF-8 LC_ALL=` non configuré (warning Debian) | 🟢 MINEUR |

### Bloqueurs logiciels
- **Authentification M5** : Credentials Google ne fonctionnent pas → origine inconnue
- **Sécurité HTTPS** : Erreur "secure connection ro fail" sur endpoint non identifié → **à logger**
- **404 sur ressource** : Endpoint spécifique cassé → **à tracker par URL**
- **Vanroll test** : Arrêt de la production de données (raison inexplorée)
- **Fiches vides (Dante)** : Analyse du pourquoi en attente → défaut localisé ou systémique ?

### Bloqueurs organisationnels
- **Conflits d'instance HA** : Deux instances Home Assistant détectées (une en arrière-plan après restauration)
- **Documentation Telegram/Inbox** : Double flux d'infos → perte de contexte procédures
- **Redondance de questions** : Même 7+ questions en boucle = documentation inexistante

---

## 🔄 Questions récurrentes (lacunes documentaires)

### Patterns critiques (7+ répétitions)
```
1. "Pourquoi il boot ?" 
   → Diagnostic incomplet des phases d'initialisation RPi
   → BESOIN : arbre de décision boot RPi 5 + logs standardisés

2. "Pourquoi vanroll test ne donne plus de données ?"
   → Pas de schema de dépendances vanroll (sources, API, timeouts)
   → BESOIN : diagnostique procédure vanroll + checklist état

3. "C'est quoi le ZH ?"
   → Acronyme métier non défini
   → BESOIN : glossaire PKA JCH obligatoire

4. "L(M) c'est quoi ?"
   → Notation probabiliste/LLM non explicitée
   → BESOIN : notation standard doc + exemples

5. "States files ?" 
   → Home Assistant internals mal expliqués
   → BESOIN : HA architecture overview pour PKA

6. "Avant/Arrière des 4 roues ?" 
   → Contexte auto/mécanique absent
   → BESOIN : specs véhicule ou schéma physique

7. "Comment garder procédures en mémoire + lancer par nom ?"
   → Absence de registry procédure persistant
   → BESOIN : système d'indexation Dobby pour procedures
```

---

## 🎯 Nouveaux patterns détectés

### Pattern 1 : Décisions sans trace écrite
- JCH décide rapidement en verbal → pas de ticket/MD → Dobby/Jade redécouvrent
- **Exemple** : "on va arreter là" → fichier .md jamais créé ? → pas de confirmation
- **Impact** : Perte de context entre sessions

### Pattern 2 : Diagnostic incomplet en parallèle
- 3+ hypothèses testées simultanément sur RPi sans documenter l'ordre logique
- `fsconfig() error` + `boot hang` + `SSH fail` mélangés → impossible isoler la cause racine
- **Impact** : Temps perdu, escalade confusion

### Pattern 3 : Contexte métier absent
- Vetalyx/Diaho : questions légales/finance mélangées avec IOT/RPi
- Terminology (ZH, L(M), "wican") utilisée sans définition
- **Impact** : Dobby/Jade doivent deviner l'intent

### Pattern 4 : Procédures orales vs écrites
- "Rappelle-moi si on avait aussi..." → attente que Dobby maintienne mémoire orale
- Double flux Inbox + Telegram sans sync
- **Impact** : Perte d'infos, pas de playbook répétable

### Pattern 5 : Scope creep silencieux
- Vetalyx + RPi Hardware + Home Assistant + Recherche Ombrie en parallèle
- Pas de priorité explicite → alternance rapide entre domaines
- **Impact** : Fragmentation cognitive, fin de session "on tourne en rond"

---

## 📊 Efficacités / Inefficacités

### ✅ Ce qui fonctionne bien
1. **Rapidité de décision** : JCH décide vite (batch de 10, test en live immédiat)
2. **Utilisation multi-outils** : DeepSeek TUI + Claude + shell exploitée efficacement
3. **Feedback itératif** : "bon travail → teste en live → reviens" crée boucle courte
4. **Consultation d'experts** : Recours à expertise externe (UCM, expert LLM Raspberry Pi)
5. **Escalade structurée** : Sphinx → Q&A → Fiches → Validation (workflow clair)

### ❌ Ce qui ralentit / bloque
1. **Zéro documentation de décision** : Aucun ADR (Architecture Decision Record) trouvé
   - Impact : Questions identiques chaque session
   - Coût : ~15% du temps de session

2. **Diagnostic en étoile sans pivot** : Plusieurs axes explorés → pas de tronc commun
   - Exemple : RPi (boot/mount/auth) explorés sans ordre causal
   - Coût : Perte de 20-30 min par session

3. **Absence de glossaire/schéma métier** 
   - ZH, L(M), wican, states files → termes fantômes
   - Coût : Clarifications répétées

4. **Double flux d'infos** : Inbox + Telegram = perte de procédures
   - Coût : Redécouverte de context

5. **Pas de playbook runbook** : "Comment lancer procédure par nom ?" → pas de registry
   - Coût : Dobby/Jade doivent inventer à chaque fois

6. **Facteur 3 sur erreurs observé** : JCH note "une erreur peut tuer une décision"
   - Pas de validation croisée pré-décision
   - Coût : Risque projet élevé

---

## 🧠 Ce qu'il faut garder en mémoire pour les prochaines sessions

### État des systèmes
- **RPi 5 (lupo-rpi)** : 🔴 BLOQUÉE à boot (phase init hardware, fsconfig mount fail)
  - À essayer : Reflash NVMe, reconfigurer HAT PSU, update firmware
  - Logs en attente de collecte standardisée
  
- **M5 (iPhone/assiette)** : 🟡 Running mais credential issue Google (source inconnue)
  - Config permanente en place (lupo/assiette vs esneux/iphone = instance HA différente)

- **Home Assistant** : ⚠️ Conflit instance (restauration récente = 2 copies actives)
  - À résoudre : UUID/hostname duplication

### Projets en cours
| Projet | Phase | Blocker | Ownership |
|--------|-------|---------|-----------|
| **Vetalyx** | Restructuration capital (+ Diaho 40%) | Clarification legal UCM | JCH |
| **Vetalyx** | Traduction statuts SRL | Doc reçue de Jade | JCH/Jade |
| **RPi5 LLM** | Specs modèles (SLM Q4_K_M GGUF via Ollama) | Hardware boot | JCH/Dobby |
| **Ombrie search** | Recherche sites exceptionnels | Recherche en attente | JCH |
| **Vanroll** | Test data collection | Production stopped | Jade/JCH |

### Procédures critiques à clarifier
1. "Wican search" → définition + scope
2. "Niveau disponible iPhone" → quelle sélection/API
3. "ZH" → acronyme métier
4. "L(M)" → notation probabiliste explicitée
5. "States files HA" → internals HA pour PKA
6. Diagnostic boot RPi → arbre décision + logs
7. Vanroll restart → checklist état

### Patterns à changer dès la prochaine session
- ✅ **Créer ADR (Architecture Decision Record)** pour chaque décision non triviale
- ✅ **Documenter immédiatement** les définitions de termes (ZH, L(M), etc.)
- ✅ **Établir runbook registry** avec index par nom + procédure
- ✅ **Centraliser flux Telegram + Inbox** → single source of truth pour procedures
- ✅ **Formaliser diagnostic RPi** → checklist + ordre causal (pas étoile)

---

## 🎯 Recommandations

### 🔴 URGENCE 1 : Déblocage RPi (cette semaine)
```markdown
1. Collecte de logs standardisée :
   - dmesg | grep -i squash/mount/fsconfig
   - journalctl -u home-assistant -50 (logs init)
   - /proc/version + HAT firmware version
   
2. Diagnostic or

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 24
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 24
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
- **Decision** : 1 jours, 18 occurrences
- **Failure** : 1 jours, 14 occurrences
- **Question** : 1 jours, 13 occurrences
- **Recurring question** : 1 jours, 10 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 0
- Jours d'observation : 1
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**410** recommandations au total — **410** ouvertes — **0** en cours — **0** terminées

⚠️ 410 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 367
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=398] (2026-09-09) **Dobby** : Immédiat (avant session suivante)
- [id=399] (2026-09-09) **Dobby** : Déclarer Lupo-RPI morte
- [id=400] (2026-09-09) **Dobby** : Créer fichier `.md` documentant l'état d'échec (diagnostic complet + pistes test
- [id=401] (2026-09-09) **Dobby** : Planifier réinstall complet : extraction image → vérification SHA256 → DD → boot
- [id=402] (2026-09-09) **Dobby** : Responsable** : JCH | **Timeline** : 2-3h

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
