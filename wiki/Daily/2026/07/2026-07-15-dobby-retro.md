---
date: 2026-07-15
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1047
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-15

**Sessions analysées :** 2 | **Échanges :** 1047 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-07-15 — PKA de JCH

## Décisions prises

### Validated & Locked
- **Migration OpenRouter** : Arrêt de Claude Code et Codex CLI. Passage exclusif à OpenRouter pour éviter les coûts API répétitifs.
- **Retour à Lupo-RPI** : Gel du setup RPI pour stabilisation (après cascades d'erreurs matérielles).
- **Transfert sur modèle plus robuste** : Escalade vers DeepSeek V4-Pro quand la résolution de problème dépasse le contexte courant.
- **Setup Vetalyx** : Nouvelle société chinoise intégrée au pipeline. Validation 100% du système pharmaceutique (hydrocortisone aceponate).
- **Validation du travail plantes** : Tous les fichiers sauvegardés et archivés.

### En attente / Conditionnelles
- "On va attendre" (contexte non explicité) — **signale une décision suspendue sans justification documentée**.
- Passage vers Kimi via OpenRouter (vérification de faisabilité en cours).

---

## Échecs ouverts / Bloqueurs

### Critiques (non résolvables ce jour)
| Bloqueur | Symptôme | Status |
|----------|----------|--------|
| **AppManager.install crash** | `system is not healthy - duplicate_os_install` | OUVERT |
| **MQTT timeout** | `NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` | OUVERT — RPI réseau instable |
| **FS SQUASHFS** | `fsconfig() failed: Can't find superblock on nvme0n1p5` | OUVERT — corruption possible SSD |
| **Upstream connect error** | Disconnect/reset avant réception headers (Docker/gateway) | OUVERT |
| **Home Assistant duplication** | Confllit UUID/instance active détectée | OUVERT — requiert restart propre |

### Palliés par workaround manuel
- **Whisper non-fonctionnel en VSCode** → Passage en terminal natif RPI (non idéal).
- **team.db inaccessible** → Accès direct Postgres (contournement, pas solution).
- **Erreur 6683** → Pas d'identifiant trouvé dans la session (documentation manquante).

### Matériel en attente
- Composants Mouser backordés (MEMS mics, inducteurs, capteurs) — livraison non prévue.
- Incertitude X1201-C1 : "C'est celui où on peut connecter le SSD ?" reste sans réponse définitive.

---

## Questions récurrentes (signe de lacune documentaire)

### Le problème central : **VSCode vs Terminal RPI**

Posée **4 fois** en variantes :
- "Ca c'est la commande terminal, c'est quoi la commande quand je suis dans un terminal VSCode?"
- "Pourquoi tu n'as pas accès au terminal RPI?"
- "En attendant pourquoi tu ne peux pas travailler dans le terminal RPI?"
- "Whisper ne fonctionne pas; vérifie pourquoi on est dans VSCode"

**Root cause** : Pas de doc explicite sur l'architecture SSH/Terminal RPI. JCH mélange :
- Terminal *local* M5 (avec env vars incorrects)
- Remote RPI via Tailscale (connexion instable)
- VSCode Remote SSH (avec mauvaise config locale .env)

**Action urgente** : Créer diagram + checklist "Before running any command, you are in : [ ] Local M5 [ ] RPI via SSH [ ] Docker container [ ] VSCode terminal"

### OpenRouter + VSCode integration
Posée **2 fois** :
- "Explique-moi comment utiliser OpenRouter dans l'interface de VS Code et comment choisir un modèle?"
- "Pourquoi j'ai aussi (.env) en début de path?"

**Root cause** : Pas de guide unifié "OpenRouter + VSCode Remote SSH". JCH confond variables d'env shell vs VSCode settings.

### Whisper troubleshooting
Posée **2 fois** avec contextes différents (une fois VSCode, une fois dans quelle config?). Pas de logs complets fournis.

---

## Nouveaux patterns détectés

### 1. **Decision Fatigue avec Escalade Modèle**
Pattern : "Ca marche pas → Je vais le faire manuellement" apparaît **3x**.
- Indique que JCH *abandonne* le debug d'outils pour solutions manuelles quand temps > effort.
- Les escalades vers DeepSeek V4-Pro sont correctes mais arrivent *après* perte de 30+ min.

### 2. **Mixing Domains in Single Session**
- Pharma (Virbac, hydrocortisone) + RPI setup + VSCode SSH + MQTT + Home Assistant.
- Cognitive load très élevé. Les erreurs 6683, UUID duplicates ne sont jamais debuggées à fond (context switching).

### 3. **Stateless Bloquers**
- Erreur "404 on laisse yahoo" → abandonnée sans trace.
- "Pourquoi tu n'as pas accès au terminal RPI?" → Jamais clarifié : est-ce réseau? Perm? Config?

### 4. **Hardware as Unknown**
- X1201-C1 connector schema → Question posée, pas de réponse. Dobby a *accepté* l'incertitude.
- SSD NVMe vs HAT Geekworm compatibility — expert fourni une guidance mais implém pas tracée.

---

## Efficacités / Inefficacités

### ❌ Très inefficace
| Domaine | Problème | Impact |
|---------|----------|--------|
| **Debugging RPI** | Erreurs matérielles (SQUASHFS, timeout MQTT) sans logs systématiques | 45+ min perdues |
| **Context switching** | Pharma ↔ RPI ↔ VSCode ↔ Docker en même session | Erreurs de compilation mentale |
| **Undocumented decisions** | "On va attendre" sans trace de pourquoi/quand | Blocage futur = redémarrage chaud |
| **Terminal clarity** | 4 questions sur SSH vs local vs VSCode terminal | Besoin de doc visuelle |
| **Escalade modèles** | Passer à DeepSeek *après* avoir spammé Dobby 10 min | Wastes tokens inutilement |

### ✅ Efficace
| Domaine | Pattern | Bénéfice |
|---------|---------|----------|
| **Validation pharma** | Expert + KMI 2.5 analysis + Virbac research = 100% confidence | Décision lock rapide |
| **OpenRouter pivot** | Abandon API coûteux pour flux unifié = coût ↓, contrôle ↑ | Smart cost move |
| **Dobby escalade** | Quand manual override → "OK je le fais manu" = clarity | Évite infinite loop |
| **File archiving** | "Tous ce travail sur les plantes → Validé et sauvegardé" | Pas de perte |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 BLOCKERS NON RÉSOLUS (reporter)
1. **RPI Filesystem Corruption** : `nvme0n1p5 SQUASHFS superblock` — requiert `fsck` ou reclone SSD
2. **AppManager duplicate_os_install** : Requiert Hard Reset ou reinstall OS propre
3. **MQTT timeout cascade** : Vérifier Tailscale MTU, MQTT broker config, power management RPI
4. **Home Assistant UUID conflict** : Cleaner shutdown + UUID reset avant restart
5. **Whisper in VSCode** : Vérifier `export PYTHONPATH` dans `.env` et rechecker Ollama status

### 🟡 DECISIONS EN ATTENTE
- "On va attendre" → **Clarifier QUOI et JUSQU'À QUAND**
- Kimi 2.5 via OpenRouter → Vérifier rate limits avant production
- X1201-C1 connector → Demander schéma exact à fournisseur

### 📚 DOCUMENTATION CRITIQUE À CRÉER
1. **"VSCode SSH Terminal vs Local Terminal" Cheatsheet**
   - Inclure: env vars différentes, PATH precedence, où exécuter quoi
   - Diagrams : M5 local → RPI remote vs Docker container

2. **"OpenRouter + VSCode Remote SSH Setup"**
   - `.env` precedence rules
   - Model selection via CLI vs API vs UI

3. **"Whisper on RPI5 Troubleshooting Guide"**
   - Ollama status check
   - Memory bottlenecks (8GB) vs model size
   - Audio input permission check

4. **"RPI Hardware Health Dashboard"**
   - Script de health check : FS, MQTT, network, thermal
   - Runbook pour chaque error code (MQTT timeout, SQUASHFS, etc.)

### 💾 MEMORY SNAPSHOTS À SAUVEGARDER
- **Vetalyx pharma config** : Supplier (Virbac), CDMO process, regulatory (EU-GMP)
- **RPI5 LLM stack** : Ollama + Q4_K_M quantization + recommended models (phi-2, mistral-7b-q4)
- **OpenRouter API keys + rate limits** : Pour KMI 2.5 et DeepSeek V4-Pro
- **Team DB** : 32 membres + 12 projects (4 actifs, 4 en cours, 4 en veille)

---

## Recommandations

### Immédiat (avant prochaine session)
1. **RPI Triage** : Créer script diagnostic systématique
   ```bash
   # Checker: FS health, MQTT connectivity, Tailscale route, thermal
   # Output: color-coded report avec actions recommandées
   ```

2. **Documentation triad creation**
   - VSCode SSH guide (1h)
   - OpenRouter cheatsheet (30 min)
   - Whisper troubleshooting (1h)
   - → Stock dans `/PKA_JCH/docs/` et lier dans Dobby memory

3. **Décision "On va attendre"** → Tracer explicitement
   - Créer issue : "DECISION_SUSPENDED_[date]_[raison]_[deadline]"
   - Ajouter dans `sessions.log` : raison + condition de reprise

### Court terme (cette semaine)
1. **RPI filesystem recovery**
   - Option A : `fsck -y /dev/nvme0n1p5` (non-destructif)
   - Option B : Reclone depuis sauvegarde + re-apply configs
   - Documenter la procédure choisie pour réplication future

2. **Home Assistant UUID cleanup**
   - Stop instance, edit `/config/uuid`, restart
   - Test détection doublons avant réimport sauvegarde

3. **Whisper + VSCode** : Validation simple
   - Vérifier `python -c "import whisper; print(whisper.__version__)"`
   - Vérifier Ollama active + model loaded
   - Tester via CLI *avant* VSCode integration

4. **OpenRouter pivot finalization**
   - Tester Kimi 2.5 sur 1 use case réel (ex: Vetalyx doc review)
   - Confirmer rate limits suffisants
   - Mettre à jour `.env` global

### Moyen terme (2-4 semaines)
1. **Refactor PKA memory system**

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 55
- Résolus automatiquement : 13
- Résolus manuellement : 0
- Encore ouverts : 42
- **Taux : 23.6%**

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

- [Decision] Migration OpenRouter** : Arrêt de Claude Code et Codex CLI. Passage exclusif à OpenRouter pour éviter les coûts API répétitifs.
- [Decision] Retour à Lupo-RPI** : Gel du setup RPI pour stabilisation (après cascades d'erreurs matérielles).
- [Decision] Transfert sur modèle plus robuste** : Escalade vers DeepSeek V4-Pro quand la résolution de problème dépasse le contexte courant.
- [Decision] Setup Vetalyx** : Nouvelle société chinoise intégrée au pipeline. Validation 100% du système pharmaceutique (hydrocortisone aceponate).
- [Decision] Validation du travail plantes** : Tous les fichiers sauvegardés et archivés.

### Fréquence des patterns (14 jours)
- **Decision** : 8 jours, 32 occurrences
- **Failure** : 8 jours, 53 occurrences
- **Question** : 8 jours, 23 occurrences
- **Recurring question** : 6 jours, 20 occurrences

### Patterns confirmés (3+ jours d'apparition)
*(assez fréquents pour mériter une action documentaire)*

- [Failure] (3x) édente, échecs d'outils (ex: "L'API X a crashé hier avec l'erreur Y"), statuts d

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 5
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**274** recommandations au total — **274** ouvertes — **0** en cours — **0** terminées

⚠️ 240 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 235
- **Forge** : 32
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=266] (2026-07-15) **Forge** : RPI Triage** : Créer script diagnostic systématique
- [id=267] (2026-07-15) **Dobby** : Documentation triad creation
- [id=268] (2026-07-15) **Dobby** : VSCode SSH guide (1h)
- [id=269] (2026-07-15) **Dobby** : OpenRouter cheatsheet (30 min)
- [id=270] (2026-07-15) **Dobby** : Whisper troubleshooting (1h)

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $24.85 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $24.85**
