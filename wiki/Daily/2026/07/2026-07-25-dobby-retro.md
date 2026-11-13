---
date: 2026-07-25
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1019
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-25

**Sessions analysées :** 2 | **Échanges :** 1019 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 🦉 RÉTROSPECTIVE PKA - 2026-07-25

## Décisions prises

1. **Arrêt du cycle de debugging actuel** → Documentation plutôt que poursuite infructueuse
   - Citation : *"on va arreter là. on tourne en rond, cree un fichier .md à mettre"*
   - **Impact** : Pivot vers documentation des états actuels

2. **Mémorisation des découvertes pour tests futurs** → Consolidation en mémoire longue
   - Citation : *"ok mets cela en memoire car on va faire des tests en reel dans quelques jours"*
   - **Impact** : Préparation d'une session de tests réels imminente

3. **Transfert vers modèle plus développé** → Escalade technique justifiée
   - Citation : *"rompt resumant probleme et situation, je vais te transferer sur un modele plus developper"*
   - **Impact** : Reconnaissance des limites du contexte actuel

4. **Retour au projet lupo-rpi pour stabilisation hardware** → Réaffectation de priorités
   - Citation : *"ok on va retourner a lupo-rpi pour essayer de figer son setup"*
   - **Impact** : Focus sur hardware endpoint stable avant IA

5. **Redémarrage isolé du lupo-rpi** → Validation expérimentale
   - Citation : *"on va reallume le lupo-rpi seul pour voir si tout redemarre comme"*
   - **Impact** : Test de résilience après précédents dysfonctionnements

6. **Configuration des modèles LLM via experts externes** → Sourcing de recommandations
   - Citation : *"ok j'ai interroge un expert qui me donne ceci comme commentaires # Configuration et Dépannage LLM sur Raspberry Pi 5"*
   - **Impact** : Intégration de bonnes pratiques (SLM, Ollama, Q4_K_M GGUF)

---

## Échecs ouverts / bloqueurs

### 🔴 **CRITIQUES (bloquent le développement)**

| Bloqueur | Description | État |
|----------|-------------|------|
| **Duplicate OS Install** | `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_instal` | ❌ Non résolu |
| **SQUASHFS Superblock Failure** | `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` | ❌ Corruption NVMe suspectée |
| **Ctrl+C inopérant sur RPi** | Impossibilité d'interrompter les processus SSH | ❌ Problème de session |
| **Conflit Home Assistant** | Deux instances HA détectées sur même réseau/disque (UUID conflictuels) | ❌ Restauration de sauvegarde corrompue |
| **terminal.db inaccessible** | Base de données verrouillée ou corrompue | ❌ Permissions/intégrité incertaines |

### 🟡 **MAJEURS (ralentissent itérations)**

| Bloqueur | Description | État |
|----------|-------------|------|
| **Credentials Google invalides** | Username/password issus de Google Keyword Research non fonctionnels | ⚠️ Mauvaise source identifiée |
| **Whisper non fonctionnel dans VSCode** | Module audio/transcrption bloqué | ⚠️ Dépendances manquantes |
| **Vanroll test sans données** | Requête data retourne vide | ⚠️ Endpoint ou payload incorrect |
| **404 réseau récurrent** | Connectivité instable entre M5/RPi/iPhone | ⚠️ Configuration Tailscale/DNS |
| **Téléchargement Home Assistant OS interrompu** | Timeout réseau pendant wget (6 GB) | ⚠️ Bande passante/stabilité ISP |

### 🟠 **SECONDAIRES (documentaires/clarifications)**

- Locale non configurée (LC_CTYPE=UTF-8 orpheline)
- HAT batterie Geekworm non fully intégré

---

## Questions récurrentes (signe de lacune documentaire)

### Pattern 1 : **Topologie réseau/adressage**
```
- "on avec les 4 roues un autre plus petit c'est quoi et ce serait bien de connaitre l'avant de l'arriere"
- "je vais choisir le niveau disponible dans l'iphone. peut on envoyer"
```
**⚠️ Diagnostic** : Absence de schéma réseau clair (M5 ↔ RPi ↔ iPhone). Les adresses IP ne sont pas documentées de manière accessible.

### Pattern 2 : **Terminologie/nomenclature**
```
- "ok, il indique L(M) c'est quoi ?"
```
**⚠️ Diagnostic** : Acronymes locaux (L(M), LUPO, VANROLL) jamais expliqués. Besoin d'un **glossaire du projet**.

### Pattern 3 : **Accès terminal RPi**
```
- "en attendant pourquoi tu ne peux pas travailler dans le terminal RPI ?"
- "pourquoi tu n'as pas acces au terminal rpi ?"
- "pourquoi il boot ?"
```
**⚠️ Diagnostic** : Confusion persistante entre accès SSH, sessions interrompues, et problèmes d'authentification. **Processus de diagnostic standardisé manquant**.

### Pattern 4 : **Synchronisation modèles/versions**
```
- "j'utilise aussi gm 5.2 comment faire en sorte qu'il ait le meme bootstrap ?"
- "whisper ne fonctionne pas ; vérifie pourquoi on est dans vscode"
```
**⚠️ Diagnostic** : Déploiement fragmenté (versions hétérogènes). Besoin d'une **matrice de compatibilité**.

### Pattern 5 : **États de base de données**
```
- "team.db pourquoi inacessible ?"
```
**⚠️ Diagnostic** : Absence de procédure de vérification d'intégrité DB. Monitoring des fichiers critiques inexistant.

---

## Nouveaux patterns détectés

### 1️⃣ **Cycle de debugging divergent**
**Observation** : Alternance entre 3 contextes distincts sans convergence :
- Configuration LLM/Ollama sur RPi
- Dépannage Home Assistant (duplicate instances)
- Problèmes réseau M5/iPhone/RPi

**Cause racine probable** : Pas de matrice de priorités. Chaque problème est traité indépendamment sans dépendances documentées.

### 2️⃣ **Sourcing de solutions via experts externes en direct**
**Observation** : JCH consulte des experts externes (configuration LLM) au lieu de documenter patterns internaliser les solutions.

**Efficacité** : ⚠️ Moyen terme bon, long terme risqué (fragmentation des sources).

### 3️⃣ **Passage de context entre modèles implicite**
**Observation** : *"rompt resumant probleme et situation, je vais te transferer sur un modele plus developper"*

**Impact** : Pertes documentées de continuité logique. Chaque model doit re-bootstrapper le contexte.

### 4️⃣ **Hardware comme variable critique sous-estimée**
**Observation** : Chaque problème logiciel remonte finalement à configuration hardware (NVMe corruption, alimentation RPi, localisation Debian).

**Pattern** : Test logiciel sans isolation hardware → faux négatifs systématiques.

---

## Efficacités / inefficacités

### ✅ **EFFICACITÉS**

| Pratique | Évidence | Score |
|----------|----------|-------|
| **Isolation des tests (lupo-rpi seul)** | Permet de distinguer problèmes réseau vs. locaux | ⭐⭐⭐⭐⭐ |
| **Pivot vers documentation rapide** | Arrêt du cycle infructueux → fichier .md | ⭐⭐⭐⭐ |
| **Consultation d'experts externes** | Intégration rapide de bonnes pratiques (SLM/Ollama) | ⭐⭐⭐⭐ |
| **Mémorisation pour tests futurs** | Prépare état connu pour prochaine session | ⭐⭐⭐⭐ |
| **Grep/shell pour diag réseau** | JCH utilise outils appropriés (grep patterns IP, find mosquitto.conf) | ⭐⭐⭐⭐ |

### ❌ **INEFFICACITÉS**

| Anti-pattern | Coût | Score |
|--------------|------|-------|
| **Absence de matrice dépendances** | Même problème debuggé 3x → contextes différents | ⭐⭐⭐⭐⭐ |
| **Questions récurrentes = doc manquante** | Réponses données verbalement, jamais consolidées | ⭐⭐⭐⭐⭐ |
| **Transferts de context implicites** | "Je vais te transférer" → perte continuité logique | ⭐⭐⭐⭐ |
| **Pas de checklist avant redémarrage** | Redémarrage isolé du RPi = test ad-hoc, non reproductible | ⭐⭐⭐⭐ |
| **Hardware diagnostics manuels** | `fsconfig() failed` découvert par hasard, pas proactif | ⭐⭐⭐ |
| **Credentials mal sourcées** | Google Keyword Research ≠ API keys → gaspillage temps | ⭐⭐⭐ |
| **Fichiers fragmentés** | Extraits de transcript montrent imports depuis Mouser/GitHub éparpillés | ⭐⭐⭐ |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🎯 **État critique du système**

```markdown
## LuPo-RPi (2026-07-25)
- **Hardware** : RPi 5 (8GB) + NVMe (SQUASHFS corruption suspectée) + HAT batterie Geekworm
- **OS Bloquant** : Home Assistant OS - Duplicate instance error (UUID conflict)
  - Cause : Restauration de sauvegarde + instance antérieure non supprimée
  - Symptôme : 'AppManager.install' blocked - system not healthy
- **Réseau** : Instabilité Tailscale M5 ↔ RPi ↔ iPhone (4xx errors)
- **Terminal SSH** : Sessions fermées brutalement (Ctrl+C non-responsive)
- **Données** : team.db inaccessible, vanroll test sans réponse

## Prochains tests réels prévus
- Redémarrage isolé RPi (validation résilience)
- Contrôle NVMe (fsck/badblocks)
- Recréation Home Assistant OS from scratch (non-restauration)
- Test SLM via Ollama (Q4_K_M GGUF, recommandation expert)
```

### 📚 **Glossaire projet (à compléter)**
```
- LUPO : Raspberry Pi 5 endpoint (nom robot/machine?)
- M5 : Machine cliente (Mac?) - adresse réseau 192

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 32
- Résolus automatiquement : 3
- Résolus manuellement : 0
- Encore ouverts : 29
- **Taux : 9.4%**

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

- [Decision] → Documentation plutôt que poursuite infructueuse
- [Decision] Citation : *"on va arreter là. on tourne en rond, cree un fichier .md à mettre"
- [Decision] Impact** : Pivot vers documentation des états actuels
- [Decision] → Consolidation en mémoire longue
- [Decision] Citation : *"ok mets cela en memoire car on va faire des tests en reel dans quelques jours"
- [Decision] Impact** : Préparation d'une session de tests réels imminente
- [Decision] → Escalade technique justifiée
- [Decision] Citation : *"rompt resumant probleme et situation, je vais te transferer sur un modele plus developper"
- [Decision] Impact** : Reconnaissance des limites du contexte actuel
- [Decision] → Réaffectation de priorités
- [Decision] Citation : *"ok on va retourner a lupo-rpi pour essayer de figer son setup"
- [Decision] Impact** : Focus sur hardware endpoint stable avant IA
- [Decision] → Validation expérimentale
- [Decision] Citation : *"on va reallume le lupo-rpi seul pour voir si tout redemarre comme"
- [Decision] Impact** : Test de résilience après précédents dysfonctionnements
- [Decision] → Sourcing de recommandations
- [Decision] Citation : *"ok j'ai interroge un expert qui me donne ceci comme commentaires # Configuration et Dépannage LLM sur Raspberry Pi 5"
- [Decision] Impact** : Intégration de bonnes pratiques (SLM, Ollama, Q4_K_M GGUF)
- [Decision] Arrêt du cycle de debugging actuel** → Documentation plutôt que poursuite infructueuse
- [Decision] Mémorisation des découvertes pour tests futurs** → Consolidation en mémoire longue
- [Decision] Transfert vers modèle plus développé** → Escalade technique justifiée
- [Decision] Retour au projet lupo-rpi pour stabilisation hardware** → Réaffectation de priorités
- [Decision] Redémarrage isolé du lupo-rpi** → Validation expérimentale
- [Decision] Configuration des modèles LLM via experts externes** → Sourcing de recommandations
- [Failure] | `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5` | Bloqué en lecture | 🔴 CRITIQUE |
- [Failure] | Bloqueur | Description | État |
- [Failure] | `'AppManager.install' blocked from execution, system is not healthy - duplicate_os_instal` | ❌ Non résolu |
- [Failure] | Impossibilité d'interrompter les processus SSH | ❌ Problème de session |
- [Failure] | Deux instances HA détectées sur même réseau/disque (UUID conflictuels) | ❌ Restauration de sauvegarde corrompue |
- [Failure] | Base de données verrouillée ou corrompue | ❌ Permissions/intégrité incertaines |

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 28 occurrences
- **Question** : 7 jours, 19 occurrences
- **Failure** : 6 jours, 36 occurrences
- **Recurring question** : 4 jours, 15 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 30
- Jours d'observation : 10
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**357** recommandations au total — **357** ouvertes — **0** en cours — **0** terminées

⚠️ 302 recommandations ouvertes depuis plus de 7 jours.

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
