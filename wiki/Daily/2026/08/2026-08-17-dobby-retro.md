---
date: 2026-08-17
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 3
echanges: 1043
modeles: <synthetic>, claude, deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-17

**Sessions analysées :** 3 | **Échanges :** 1043 | **Modèles :** <synthetic>, claude, deepseek-v4, deepseek-v4-pro

---

# Rétrospective des Sessions du 2026-08-17
## Dobby's PKA Analysis - JCH Multi-Tool Sessions

---

## Décisions prises

1. **Relancer lupo-rpi isolément** pour diagnostiquer les redémarrages → validation en mémoire avant tests réels (quelques jours plus tard)
2. **Transférer sur un modèle plus développé** pour les problèmes complexes (rupture de contexte détectée)
3. **Geler la configuration lupo-rpi** → retour au setup hardware après phase de diagnostic
4. **Valider et mettre à jour tous les fichiers utiles** → informer les acteurs (decision incomplète : pas de destinataires spécifiés)
5. **Archiver en .md** → arrêter la boucle infinie identifiée
6. **Changer la topologie lupo** : passer d'un facteur forme sphère à une solution sans fixation manuelle unitaire (impact UX/déploiement)
7. **Vetalyx (Belgique)** : accepter investissement chinois 40% via DIaho sans opérateurs/managers physiques chinois ; capital = 10k€ (déclaration statut actionnaire à confirmer auprès UCM)
8. **Modèles LLM sur RPi5** : utiliser SLM quantisés Q4_K_M via Ollama (décision issue d'expert externe)

**⚠️ PROBLÈME : Plusieurs décisions sont partielles, non documentées avec contexte clair, pas de date d'exécution définie.**

---

## Échecs ouverts / bloqueurs

### Hardware / Infrastructure
- **RPi5 bloqué au boot initial** : stuck in hardware initialization phase → pas de progression observable
- **RPi inaccessible via terminal** : SSH intermittent, connexions fermées abruptement (`Broken pipe`)
- **Problème CTRL+C sur RPi** : les signaux ne passent pas → debugging impossible sans escalade
- **SQUASHFS superblock error** (`/mnt: fsconfig() failed`) → nvme0n1p5 corrompu ou mal flashé
- **AppManager.install bloqué** : "system is not healthy - duplicate_os_instal" → détecte plusieurs instances HA actives sur même disque/réseau
- **Whisper (STT) ne fonctionne pas en VSCode** → cause inconnue, non diagnoticisée
- **team.db inaccessible** → requête jamais complétée, cause non identifiée
- **HTTP 404 sur haos_rpi5 image** : téléchargement interrompu à 6.05 MB / 347 MB → retry loop visible mais jamais résolu
- **Locale configuration invalide** (`LC_CTYPE=UTF-8`, `LC_ALL=`) sur Debian → peut bloquer gestion paquets

### Processus
- **Lupo reporté au 31 août** : Hardware quasi terminé (SD endurance + silent blocs manquants) mais logiciel en impasse
- **Responsabilité floue** : qui corrige quoi ? (Dobby ? Assistant IA ? JCH directement ?)

---

## Questions récurrentes (signe de lacune documentaire)

### Top 5 redondances
1. **"Pourquoi tu n'as pas accès au terminal RPi ?"** (×3)
   - **Signification** : Problème réseau SSH non résolu, diagnostic incomplet
   - **Lacune doc** : Pas de checklist SSH (clés, DNS, firewall, locale)

2. **"Pourquoi il boot ?" / "Pourquoi ne boot pas ?"** (×2)
   - **Signification** : Confusion sur état du boot process, absence de logs structurés
   - **Lacune doc** : Pas de séquence boot documentée (UEFI → kernel → systemd stages)

3. **"Vanroll test ne donne plus de données"** (×2)
   - **Signification** : Regression silencieuse, pas de baseline de monitoring
   - **Lacune doc** : Pas de test cases formalisés ni d'alertes

4. **"Qu'est-ce que c'est ?" (L(M), states files, iphone/assiette vs instance HA)** (×4)
   - **Signification** : Métier / nommage non standardisé, acronymes non définis
   - **Lacune doc** : Glossaire manquant + architecture HA non cartographiée

5. **"team.db pourquoi inaccessible ?"** (×2)
   - **Signification** : Pas de diagnostic root cause, question abandonnée
   - **Lacune doc** : Pas de schema d'accès DB, audit logs manquants

---

## Nouveaux patterns détectés

### Pattern 1 : Rebonds "en attendant"
```
en attendant pourquoi tu ne peux pas travailler dans le terminal RPI ?
```
→ **Signal** : Blocker non résolu + pivot sur tâche de remplissage → **décision non prioritisée**

### Pattern 2 : Transferts de contexte rupturés
```
rompt resumzant problem et situation, je vais te transferer sur un modele plus developper
```
→ **Signal** : Contexts switch violent, pas de handoff document → pertes d'info en cascade

### Pattern 3 : Mélange stratégique / tactique
- Session démarre sur RPi5 debug
- Switch brutal vers vetalyx (capital, actionnaires chinois)
- Retour à LLM configs
→ **Signal** : Pas de separation des domaines, charge cognitive explosante

### Pattern 4 : Questions sans follow-up
- 1043 échanges sur 3 sessions
- Questions posées mais réponses non enregistrées
→ **Signal** : Cycle question → action implicite → pas de closed-loop

### Pattern 5 : Accent sur "ce qu'on va essayer"
- "oui on va essayer" (×multiple)
- Pas de critères de succès explicites
→ **Signal** : Experimentation non structurée, pas d'hypothèses écrites

---

## Efficacités / inefficacités

### ✅ Efficacités
1. **Diagnostic exploratoire rapide** : JCH interroge experts externes (→ recommandations SLM/Ollama) = bonne pratique
2. **Utilisation d'outils variés** : Shell exec, grep_files, read_file → polyvalence
3. **Archivage conscient** : Décision d'arrêter les boucles + créer fichier .md

### ❌ Inefficacités (critiques)

| Inefficacité | Impact | Cause | Solution |
|---|---|---|---|
| **SSH intermittent jamais triagé** | RPi5 inaccessible = 40% des tâches bloquées | Pas de diagnostic TCP/DNS/firewall | Créer runbook SSH (check hostname, keys, route, netstat) |
| **Téléchargement HAOS échoué × sessions** | Build impossible, redémarrages coûteux | Retry sans analyse réseau | Mirror local ou script de validation checksum |
| **Questions posées 2-3× par session** | Perte ∼100 tokens/cycle | Pas de FAQ vivante | Wiki searchable synchronisé |
| **Whisper non-fonctionnel oublié** | STT inutile, regret tacite | Pas de escalade ou accept/reject | Décider : fixer ou archiver en "known-issue" |
| **team.db bloqueur non explorée** | Données inaccessibles | Pas d'audit trail DB | SQL logs + permission check systematic |
| **Contexte strategy/tactic mélangé** | OKR dilués, focus fragmenté | Pas de session structure | Segmenter : strategy meetings ≠ ops sprints |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 📌 État des projets
- **lupo-rpi** : Hardware 90% (SD endurance + silent blocs pending), Firmware bloqué (boot loop, SSH down, SQUASHFS error), reporté 31-08
- **vetalyx (BE)** : Structure actionnariat validée (DIaho 40%), capital 10k€, statut déclaration à confirmer UCM
- **wildnexus / Home Assistant cluster** : Plagued by duplicate instance detection, needs inventory consolidation
- **Raspberry Pi 5 (8 Go)** : Recommandation = Ollama + Q4_K_M SLM, à appliquer

### 🔧 Blockers persistants
1. SSH/network access RPi = CRITICAL PATH BLOCKER
2. HAOS image integrity (checksum validation missing)
3. Whisper STT abandoned state (accept/reject decision needed)
4. team.db inaccessible (permission or corruption?)
5. Locale warnings on Debian (may affect Docker, Ollama)

### 📚 Lacunes documentaires majeures
- [ ] SSH troubleshooting checklist (RPi5 specific)
- [ ] LLM model matrix (which SLM for which hardware?)
- [ ] HA instance inventory + duplicate detection procedure
- [ ] PKA glossary (L(M), states files, iphone/assiette context)
- [ ] vetalyx legal/structure (shareholder registry, cap table)
- [ ] Vanroll test spec (baseline data, alert thresholds)

### 🎯 Patterns to adopt
1. **Decision logging** : Every "on va essayer" → write hypothesis + success criteria
2. **Handoff discipline** : If transferring to different model → explicit context export
3. **Closed-loop Q&A** : Questions recorded → responses logged → FAQ synced
4. **Hardware state machine** : Boot stages documented (power → UEFI → kernel → systemd → app)

---

## Recommandations

### 🔴 **Immediate (48h)**
1. **RPi5 SSH audit**
   - Verify hostname resolution (`ping lupo-rpi.local`)
   - Check SSH key permissions (`ls -la ~/.ssh`)
   - Test SSH from different network (rule out local firewall)
   - **Owner**: JCH or dedicated ops; **Deliverable**: SSH works or decision to reimage
   
2. **Triage Whisper + team.db**
   - Decide: Fix whisper or close as "not-viable-in-vscode"?
   - Check team.db: DB running? Permissions? File corruption?
   - **Owner**: Dobby diagnostic; **Deliverable**: Root cause or wontfix decision

3. **HAOS image validation**
   - Add checksum verification before flashing
   - Create local mirror to avoid timeout retries
   - **Owner**: JCH; **Deliverable**: Reproducible flashing procedure

### 🟠 **Short-term (1-2 weeks)**
4. **Create PKA glossary + FAQ**
   - Define: L(M), states files, iphone/assiette, instance HA topology
   - Document Vanroll test spec + baseline
   - **Owner**: Dobby or JCH; **Deliverable**: Wiki page (searchable)

5. **Hardware state machine for RPi5**
   - Map boot sequence with timeouts + logs per stage
   - **Owner**: JCH; **Deliverable**: Markdown + linked logs

6. **Decision log format**
   - Template: [Decision ID] | Date | Context | Hypothesis | Acceptance Criteria | Owner | Status
   - Retrofit last 3 sessions
   - **Owner**: Dobby; **Deliverable**: decisions.md file

7. **Vetalyx legal close-out**
   - Confirm UCM response on Chinese shareholder declaration requirement
   - Document final cap table
   - **Owner**: JCH; **Deliverable**: Signed legal doc

### 🟡

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 28
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 28
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

- [Decision] pour diagnostiquer les redémarrages → validation en mémoire avant tests réels (quelques jours plus tard)
- [Decision] pour les problèmes complexes (rupture de contexte détectée)
- [Decision] → retour au setup hardware après phase de diagnostic
- [Decision] → informer les acteurs (decision incomplète : pas de destinataires spécifiés)
- [Decision] → arrêter la boucle infinie identifiée
- [Decision] : passer d'un facteur forme sphère à une solution sans fixation manuelle unitaire (impact UX/déploiement)
- [Decision] : accepter investissement chinois 40% via DIaho sans opérateurs/managers physiques chinois ; capital = 10k€ (déclaration statut actionnaire à confirme
- [Decision] : utiliser SLM quantisés Q4_K_M via Ollama (décision issue d'expert externe)
- [Decision] Relancer lupo-rpi isolément** pour diagnostiquer les redémarrages → validation en mémoire avant tests réels (quelques jours plus tard)
- [Decision] Transférer sur un modèle plus développé** pour les problèmes complexes (rupture de contexte détectée)
- [Decision] Geler la configuration lupo-rpi** → retour au setup hardware après phase de diagnostic
- [Decision] Valider et mettre à jour tous les fichiers utiles** → informer les acteurs (decision incomplète : pas de destinataires spécifiés)
- [Decision] Archiver en .md** → arrêter la boucle infinie identifiée
- [Decision] Changer la topologie lupo** : passer d'un facteur forme sphère à une solution sans fixation manuelle unitaire (impact UX/déploiement)
- [Decision] Vetalyx (Belgique)** : accepter investissement chinois 40% via DIaho sans opérateurs/managers physiques chinois ; capital = 10k€ (déclaration statut a
- [Decision] Modèles LLM sur RPi5** : utiliser SLM quantisés Q4_K_M via Ollama (décision issue d'expert externe)
- [Failure] RPi5 bloqué au boot initial** : stuck in hardware initialization phase → pas de progression observable
- [Failure] RPi inaccessible via terminal** : SSH intermittent, connexions fermées abruptement (`Broken pipe`)
- [Failure] Problème CTRL+C sur RPi** : les signaux ne passent pas → debugging impossible sans escalade
- [Failure] SQUASHFS superblock error** (`/mnt: fsconfig() failed`) → nvme0n1p5 corrompu ou mal flashé
- [Failure] AppManager.install bloqué** : "system is not healthy - duplicate_os_instal" → détecte plusieurs instances HA actives sur même disque/réseau
- [Failure] Whisper (STT) ne fonctionne pas en VSCode** → cause inconnue, non diagnoticisée
- [Failure] team.db inaccessible** → requête jamais complétée, cause non identifiée
- [Failure] HTTP 404 sur haos_rpi5 image** : téléchargement interrompu à 6.05 MB / 347 MB → retry loop visible mais jamais résolu
- [Failure] Locale configuration invalide** (`LC_CTYPE=UTF-8`, `LC_ALL=`) sur Debian → peut bloquer gestion paquets

### Fréquence des patterns (14 jours)
- **Recurring question** : 3 jours, 12 occurrences
- **Question** : 2 jours, 14 occurrences
- **Decision** : 1 jours, 11 occurrences
- **Failure** : 1 jours, 18 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 25
- Jours d'observation : 4
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**382** recommandations au total — **382** ouvertes — **0** en cours — **0** terminées

⚠️ 365 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 339
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=370] (2026-08-17) **Dobby** : 1. **RPi5 SSH audit
- [id=371] (2026-08-17) **Dobby** : Verify hostname resolution (`ping lupo-rpi.local`)
- [id=372] (2026-08-17) **Dobby** : Check SSH key permissions (`ls -la ~/.ssh`)
- [id=373] (2026-08-17) **Dobby** : Test SSH from different network (rule out local firewall)
- [id=374] (2026-08-17) **Dobby** : Owner**: JCH or dedicated ops; **Deliverable**: SSH works or decision to reimage

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
