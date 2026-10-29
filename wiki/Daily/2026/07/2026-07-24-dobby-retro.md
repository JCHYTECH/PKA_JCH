---
date: 2026-07-24
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1124
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-24

**Sessions analysées :** 2 | **Échanges :** 1124 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSION 2026-07-24 - PKA JCH

## Décisions prises

1. **Arrêt de la boucle infinie sur le form factor** : Abandon de la demande utilisateur pour fixer les sphères une à une. Décision de chercher une approche batch.
2. **Pivot vers iPhone** : Choix d'utiliser le niveau disponible sur iPhone au lieu de dépendre d'une API externe.
3. **Réinitialisation du Lupo-RPI** : Décision de relancer le système seul pour vérifier un redémarrage propre.
4. **Transfert vers modèle plus développé** : Escalade vers un modèle LLM supérieur pour résoudre des problèmes complexes.
5. **Gel du setup Lupo-RPI** : Décision de figer la configuration avant tests réels "dans quelques jours".
6. **Documentation d'erreur** : Création d'un fichier `.md` pour documenter la situation actuelle et les pistes testées.

---

## Échecs ouverts / bloqueurs

### Critiques

| Bloqueur | Symptôme | Impact |
|----------|----------|--------|
| **Santé système HA** | `AppManager.install` bloqué - `duplicate_os_install` détecté | Impossible d'installer des extensions, dépôt bloqué |
| **Téléchargement d'image HS** | 404 Not Found sur `haos_rpi5-64-18.1.img.xz` (GitHub release asset) | Impossible de flasher une nouvelle image HA OS |
| **Raspberry Pi 5 gelé** | Reste bloqué à l'initialisation matérielle (couche HAT) | Système inutilisable, aucun accès au shell |
| **Instance HA dupliquée** | Restauration de sauvegarde + clonage = 2 instances avec mêmes UUID | Erreur "duplicate_os_install", supervision impossible |

### Sérieux

- **Accès terminal RPI perdu** : SSH fonctionne sporadiquement (`Broken pipe`, `Connection timed out`)
- **team.db inaccessible** : Base de données verrouillée ou corrompue
- **Whisper ne fonctionne pas** : Non-fonctionnement dans VSCode (cause non diagnostiquée)
- **PSU insuffisant** : HAT tiers demande 5000mA, alimentation actuelle insuffisante
- **Download timeout réseau** : Retry multiples sur teléchargement 347MB (vitesse 5.85 KB/s)

### Mineurs

- **Ctrl+M dans éditeur** : Affiche `m` au lieu d'exécuter macro
- **L(M) dans logs** : Notation inconnue, jamais explicitée
- **Accès RPI via iPhone** : Configuration réseau IP non documentée

---

## Questions récurrentes (lacunes documentaires)

| Question | Apparus | Diagnostic |
|----------|---------|-----------|
| *Pourquoi tu n'as pas accès au terminal RPI ?* | 3x | **Critique** : Aucun runbook de reconnexion SSH, pas de monitoring de santé |
| *team.db pourquoi inaccessible ?* | 2x | **Critique** : Pas de diagnostic de processus verrouillant, pas de backup strategy |
| *Whisper ne fonctionne pas ; vérifie pourquoi on est dans vscode* | 2x | **Sérieux** : Confusion entre problème d'env Python et config VSCode |
| *Pourquoi il boot ?* | 2x | **Urgent** : Loop infini entre reboot et initialisation, no error logs captured |
| *Quelle est la différence entre lupo/assiette et esneux/iphone ?* | 1x | **Sérieux** : Architecture d'instances HA jamais documentée (est-ce une même instance ? deux instances ?) |
| *Comment faire en sorte qu'il ait le même bootstrap ?* | 1x | **Grave** : Pas de procédure d'init standardisée, chaque machine est un flocon unique |
| *L(M) c'est quoi ?* | 3x | **Mineure** : Notation technique jamais définie |

**Constat** : Les questions posées 2-3 fois ne demandent PAS de clarification immédiate. Elles indiquent une **mémoire insuffisante entre sessions** ou une **documentation absente**.

---

## Nouveaux patterns détectés

### 1. **"Ça tourne en rond" = Point d'arrêt signalé**
Quand JCH dit "on va arrêter là, on tourne en rond", il **demande une documentation**, pas juste une pause. 
- Action manquante : générer `.md` d'état avant pivot
- Risque : perte de contexte à la session suivante

### 2. **Confusion multi-instance (lupo-rpi vs M5 vs iPhone)**
- Entité "rpi" : 95 mentions (RPi 5, but also generic references)
- Entité "M5" : 76 mentions (Raspberry Pi ou autre ?)
- Entité "iPhone" : Unclear role (iPhone 6 controller? M5 via iPhone interface?)
- **Pas de schéma réseau clair**

### 3. **Escalade par changement de modèle LLM**
Quand claude refuse/bloque (Whisper, terminal), la stratégie = "je vais te transférer sur un modèle plus développer"
- Efficace à court terme
- **Problème** : absence de diagnostic root-cause, accumulation de brouillon téchnique

### 4. **Fetiche matériel non documenté**
- HAT Geekworm (batterie) : insuffisant en puissance
- Microphones I2S + IR emitters (Mouser) : jamais expliqué pourquoi (WildNexus audio capture ?)
- **Aucun BOM validé**, achat par bricolage

### 5. **Délais vagues ("dans quelques jours")**
"on va faire des tests en reel dans quelques jours" → aucune date, aucun checklist
- Risque : oubli, incompletion, débordement sur session suivante

---

## Efficacités / inefficacités

### ❌ Inefficacités graves

| Inefficacité | Fréquence | Coût |
|--------------|-----------|------|
| **SSH/terminal down** → bascule Claude tools → retry SSH | Récurrent | Perte 20-30 min/session |
| **Whisper failure non diagnostiquée** → essai VSCode → essai CLI → escalade modèle | 2x | Perte 15 min + confusion |
| **Download timeout sur 347MB image** | 1x | Perte 10+ min, aucun mirror alternatif |
| **Ctrl+M hotkey cassée** | 1x | Friction à chaque test |
| **UUID duplicate → réinstall nécessaire** | Bloquant | Perte 1-2h +données |

### ✅ Efficacités observées

| Point fort | Evidence |
|-----------|----------|
| **Escalade rapide vers experts** | "j'ai interrogé un expert qui me donne ceci" → input external immédiat |
| **Pivot pragmatique** | iPhone niveau = solution rapidement acceptée vs perfectionniste |
| **Consultation docs pendant session** | Grep/recherche patterns, credentials récupérées en contexte |
| **Demande de documentation explicite** | "crée un fichier .md à mettre" = autoconscience de lacune |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 CRITIQUE - État des systèmes

```markdown
## Lupo-RPI (Raspberry Pi 5 + Geekworm HAT)
- STATUS: **BLOQUÉ** - gelé au boot, initialisation matériel incomplète
- DERNIÈRE TENTATIVE: 2026-07-24, restart seul = pas testé/résultat inconnu
- ACCESS: SSH intermittent (Broken pipe)
- PROBLÈME RACINE: Probable duplicate_os_install (uuid), image HA OS téléchargement 404
- PROCHAINE ACTION: Flasher nouvelle image (mirror requis) OU wipe+réinstall propre
- PSU: **INSUFFISANT** (HAT réclame 5A, source?/capacity?)

## Home Assistant OS
- ERREUR: "AppManager.install blocked - duplicate_os_install - système pas sain"
- CAUSE: Ancienne instance + restauration sauvegarde OU deux disques clonés
- IMPACT: Impossibilité ajouter extensions
- SOLUTION POSSIBLE: reset device ID + restauration propre sauvegarde

## Accès par Iphone/M5
- CONFIG RÉSEAU: **NON DOCUMENTÉE** (IP, ports, SSH proxy?)
- DISTINCTION lupo/assiette vs esneux/iphone = **JAMAIS EXPLICITÉE**
- Est-ce deux instances HA distinctes ou une seule avec deux frontends?
```

### 🟡 IMPORTANT - Questions suspendues

1. **L(M) notation** = Quelle unité? (L = inductance, M = millidécade?)
2. **team.db lock** = Quel processus l'accapare? Diagnostique manquante: `lsof | grep team.db`
3. **Whisper sur M5** = Python env correct? pip install --upgrade? ou VSCode Python path cassé?
4. **Bootstrap GM 5.2** = Procédure standardisée à créer (ansible playbook? script init?)
5. **Horaire tests réels** = **Date précise requise** pour planning matériel

### 🔵 À VALIDER

- Mouser BOM partiellement commandé (backorders) → statut actualisé?
- HAT Geekworm batteries : capacité vs consommation M5 + éléctronique?
- WildNexus/WildLens scope = capture audio (Whisper) + vision (IR?)

---

## Recommandations

### Immédiat (avant prochaine session)

1. **Créer runbook SSH diagnostique** (MANQUANT)
   ```markdown
   ## Reconnexion Lupo-RPI
   1. Vérifier santé RPI: ping lupo-rpi.local
   2. Si timeout: SSH via iphone bridge (procédure?)
   3. Si toujours down: snapshot écran boot (HDMI) → analyse crash
   4. Dernier recours: wipe+reflash image (avec mirror URL)
   ```

2. **Générer schéma réseau en ASCII** (URGENT)
   ```
   [Iphone / M5] --ssh--> [Lupo-RPI:22] --mqtt--> [Mosquitto]
                          [HA-OS:8123]
   Est-ce juste? Où rentre iPhone? Où est esneux?
   ```

3. **Documenter toutes les 404 avec mirrors**
   - Image HA OS : URL primaire + URL backup github/archive.org
   - Ollama models : endpoint avec timeout config

4. **Créer `.md` "État ouvert" à la fin CHAQUE session** (clé)
   ```markdown
   # Session fin 2026-07-24
   ## Bloqueurs ouverts
   - Lupo-RPI frozen at boot [ASSIGNÉ: TBD, DATE: 2026-07-XX]
   - team.db inaccessible [ASSIGNÉ: TBD, DATE: 2026-07-XX]
   ## Délais/

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

- [Decision] : Abandon de la demande utilisateur pour fixer les sphères une à une. Décision de chercher une approche batch.
- [Decision] : Choix d'utiliser le niveau disponible sur iPhone au lieu de dépendre d'une API externe.
- [Decision] : Décision de relancer le système seul pour vérifier un redémarrage propre.
- [Decision] : Escalade vers un modèle LLM supérieur pour résoudre des problèmes complexes.
- [Decision] : Décision de figer la configuration avant tests réels "dans quelques jours".
- [Decision] : Création d'un fichier `.md` pour documenter la situation actuelle et les pistes testées.
- [Decision] Arrêt de la boucle infinie sur le form factor** : Abandon de la demande utilisateur pour fixer les sphères une à une. Décision de chercher une approch
- [Decision] Pivot vers iPhone** : Choix d'utiliser le niveau disponible sur iPhone au lieu de dépendre d'une API externe.
- [Decision] Réinitialisation du Lupo-RPI** : Décision de relancer le système seul pour vérifier un redémarrage propre.
- [Decision] Transfert vers modèle plus développé** : Escalade vers un modèle LLM supérieur pour résoudre des problèmes complexes.
- [Decision] Gel du setup Lupo-RPI** : Décision de figer la configuration avant tests réels "dans quelques jours".
- [Decision] Documentation d'erreur** : Création d'un fichier `.md` pour documenter la situation actuelle et les pistes testées.
- [Failure] | `AppManager.install` bloqué - `duplicate_os_install` détecté | Impossible d'installer des extensions, dépôt bloqué |
- [Failure] | 404 Not Found sur `haos_rpi5-64-18.1.img.xz` (GitHub release asset) | Impossible de flasher une nouvelle image HA OS |
- [Failure] | Reste bloqué à l'initialisation matérielle (couche HAT) | Système inutilisable, aucun accès au shell |
- [Failure] | Restauration de sauvegarde + clonage = 2 instances avec mêmes UUID | Erreur "duplicate_os_install", supervision impossible |

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 28 occurrences
- **Failure** : 6 jours, 36 occurrences
- **Question** : 6 jours, 19 occurrences
- **Recurring question** : 4 jours, 15 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 16
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**357** recommandations au total — **357** ouvertes — **0** en cours — **0** terminées

⚠️ 292 recommandations ouvertes depuis plus de 7 jours.

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
