---
date: 2026-09-09
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1005
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-09-09

**Sessions analysées :** 2 | **Échanges :** 1005 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# 📋 RÉTROSPECTIVE SESSIONS 2026-09-09 - PKA JCH

## Décisions prises

1. **Allocation mémoire iPhone** → Validation de l'utilisation du niveau disponible sur l'appareil avec tests réels prévus dans quelques jours
2. **Documentation mémoire** → Stockage des configurations en attente de tests réels
3. **Validation fiches** → Passage des fiches du statut draft à validé
4. **Réorientation setup Lupo-RPI** → Retour sur la configuration pour la figer définitivement
5. **Traitement des screenshots** → Travail sur les visuels dans `inbox/sites`
6. **Procédure spots** → Création d'une procédure de fiches spots pour stockage/gestion
7. **Facteur forme** → Décision de ne PAS demander aux utilisateurs de fixer des éléments individuellement (approche sphérique/globale)
8. **Vetalyx Belgique** → Acceptation de 40% de capital pour société chinoise DIaho sans représentation opérationnelle/management physique

## Échecs ouverts / bloqueurs

### 🔴 **CRITIQUE : RPI5 complètement bloqué**
- **État** : Boot frozen à l'initialisation matérielle (Coulomb layer)
- **Symptômes** :
  - SSH inaccessible (connexions fermées : "Broken pipe")
  - Erreur `AppManager.install` : "system is not healthy - duplicate_os_install"
  - Terminal RPI inaccessible de manière persistante
  - Ctrl+C non fonctionnel sur RPI

### 🔴 **Problème SQUASHFS NVMe**
```
/mnt/mount: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5
```
- Le NVMe n'est pas correctement formaté ou image corrompue
- Bloque tout accès au système de fichiers

### 🔴 **Erreur Home Assistant OS - Instance dupliquée**
```
'AppManager.install' blocked - duplicate_os_install
```
- Détection d'une ancienne instance en arrière-plan ou UUID conflictuels
- Reste de restauration de sauvegarde non complètement supprimé

### 🔴 **Téléchargement image corrompue**
```
dd: failed to open 'haos_rpi5-15.1.img': No such file or directory
```
- Image HAOS non trouvée après téléchargement
- Erreurs de timeout durant DL : "Read error at byte 6059777/347121076 (Connection timed out)"
- Image XZ probablement incomplet

### 🟡 **Locale Debian invalide**
- `LC_CTYPE=UTF-8` / `LC_ALL` mal configurées
- Peut affecter la gestion des paquets

## Questions récurrentes (signe de lacune documentaire)

| Question | Occurrences | Enjeu |
|----------|-------------|-------|
| **Pourquoi tu n'as pas accès au terminal RPI ?** | 3x | Accès SSH complètement perdu, cause racine non établie |
| **Pourquoi il boot ?** | Implicite | État d'amorçage chaotique, pas de diagnostic structuré |
| **C'est quoi le ZH ?** | 2x | Terminologie non expliquée/documentée |
| **Quelle différence lupo/assiette vs esneux/iphone ?** | 1x | Modèle d'instances HA pas clarifié |
| **TTL 24h - comment l'utiliser en HTML ?** | 1x | Intégration de TTL dans interfaces pas documentée |
| **Vanroll test ne donne plus de données** | 1x | Débugage sans contexte, cause inconnue |
| **État files vs state files ?** | Confus | Terminologie SLM/HA mélangée |

**→ Lacune majeure** : Pas de glossaire/FAQ des acronymes (ZH, state files, TTL, etc.)

## Nouveaux patterns détectés

### 🔄 **Cycle de frustration sur Lupo-RPI**
- Session 1 : Tentative configuration NVMe
- Session 2 : Boot bloqué, SSH down
- Pattern : Chaque itération introduit un nouvel état bloquant sans roll-back clair
- **Cause probable** : Pas de snapshot/sauvegarde entre modifications critiques

### 🔄 **Spirale téléchargement/restauration**
1. Image DL avec timeout
2. DD échoue (fichier manquant ou corrompu)
3. Nouveau boot = nouvel échec
4. Restart du cycle sans diagnostic du DL

### 🔄 **Switcheroo entre outils**
- DeepSeek TUI pour logs
- Claude Code pour architecture
- Codex CLI pour exécution
- **Inefficacité** : Contexte fragmenté entre 3 interfaces, pas de continuité

### 🔄 **Documentation adhoc vs structure**
- Expert chinois consulté en externe
- Recommandations SLM/Ollama/Q4_K_M reçues mais pas intégrées au flux
- Vetalyx belgique (légal/fiscal) mélangé avec IoT/RPI

## Efficacités / inefficacités

### ✅ **Efficacités**
1. **Décision rapide** : D'oracle externe (expert LLM) → clarification immédiate modèles
2. **Validation fiches** : Processus documenté, transitionné proprement
3. **Compartimentage Vetalyx** : Séparation business/tech en cours, legality checked

### ❌ **Inefficacités**
1. **Pas de rollback plan** : RPI en état cassé = 0 possibilité de récupération sans réinstall complète
2. **Diagnostic ad-hoc** : Erreur SQUASHFS/AppManager = 3 heures d'exploration au lieu de 15 min avec checklist
3. **Split context** : Vetalyx belgique + Lupo-RPI + Vetalyx France dans même session
4. **Absence de DL verification** : Image XZ téléchargée sans checksum/integrity check
5. **Terminal RPI perdu** : Root cause jamais établie (réseau ? auth ? port ?) = 3 questions répétées
6. **Facteur forme sphere** : Décision prise sans formalisation de l'architecture (qui valide ?)

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 **État critique**
- **Lupo-RPI est DOWN** : SSH cassé, boot frozen, NVMe invalid
- **Prérequis immédiat** : Redémarrage complet du flash NVMe + réinstall HAOS 64-bit
- **Image à utiliser** : `haos_rpi5-64-18.1.img` (ou version 15.1 stable testée)

### 🧠 **Métadonnées importantes**
- **Expert LLM consulté** : Recommande SLM quantisés Q4_K_M via Ollama pour RPI 8Go
- **Modèles à tester** : Mistral 7B, Llama2 7B (GGUF quantisés)
- **Vetalyx Belgique** : 40% capital DIaho validé légalement (no operational presence required)
- **Fiches validées** : Prêtes à l'emploi, ne pas réouvrir

### 🧠 **Glossaire émergent** (À documenter)
- **ZH** : ?(à clarifier)
- **State files** : Fichiers d'état HA
- **TTL 24h** : Time-to-live intégration (usage HTML TBD)
- **Lupo/assiette vs esneux/iphone** : Instances HA distinctes
- **Vanroll test** : Suite de test (endpoint perdu ?)

### 🧠 **Procédures en attente d'automatisation**
1. **Fiches spots** : Procédure à encoder en CLI
2. **Screenshots inbox/sites** : Traitement batch nécessaire
3. **Procédure contrôle via Telegram vs inbox** : Orchestration multi-channel

## Recommandations

### 🚨 **P0 - Immédiat (avant session suivante)**
1. **Déclarer Lupo-RPI morte**
   - Créer fichier `.md` documentant l'état d'échec (diagnostic complet + pistes testées)
   - Planifier réinstall complet : extraction image → vérification SHA256 → DD → boot test
   - **Responsable** : JCH | **Timeline** : 2-3h

2. **Créer checklist post-crash RPI**
   - ✅ Télécharger image
   - ✅ Vérifier checksum
   - ✅ DD vers NVMe
   - ✅ SSH test
   - ✅ Locale reconfigure
   - Sans cette checklist, récurrence garantie

3. **Valider access SSH** dès boot
   - Avant toute autre opération, tester : `ssh jchavaux@lupo-rpi.local`
   - Si fail → diagnostic réseau avant poursuite

### 🔧 **P1 - Court terme (cette semaine)**
1. **Créer glossaire acronymes PKA**
   - Fichier `JCH_PRIVATE/PKA_GLOSSARY.md`
   - Entrées : ZH, state files, TTL, Assiette/Esneux, SLM, GGUF, Q4_K_M
   - Lier depuis chaque transcript

2. **Intégrer recommandations expert LLM**
   - Encoder dans `03_PROJECTS/11_IOT/LUPO_RPI_SETUP.md`
   - Modèles testés + benchmarks
   - Ollama install procedure

3. **Documenter Vetalyx split**
   - Fichier distinct pour Vetalyx Belgique (capital structure)
   - Fichier distinct pour Vetalyx France (tech/IoT)
   - Éviter croising contexts

4. **Snapshot RPI state post-recovery**
   - Une fois Lupo-RPI relancé : **prendre image de sauvegarde**
   - Stocker sur NAS avec timestamp
   - Permet rollback sans réinstall

### 🏗️ **P2 - Moyen terme**
1. **Formaliser facteur forme sphere**
   - Doc architecture : pourquoi pas fixture individuelle
   - Validation: qui signe off ? (JCH ? expert external ?)
   - User acceptance criteria

2. **Automatiser procédure spots**
   - Script CLI : `dobby spots validate [directory]`
   - Lier à Telegram + inbox async
   - Memory encoder pour réutilisation

3. **Centraliser multi-tool context**
   - Au lieu de 3 sessions parallèles (DeepSeek/Claude/Codex)
   - Implémenter **session persistence** avec PKA file
   - Accès unique point (e.g., PKA Web dashboard)

4. **Mettre en place DL verification automatis**
   - Checksum validation post-DL avant DD
   - Fallback à mirror alternatif si corruption
   - Log pour audit

### 🎯 **P3 - Validation post-fix**
- Tests réels iPhone dans quelques jours : **documenter résultats**
- Vanroll test debugging : isoler endpoint, reproduire locally
- TTL 24h integration HTML :

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 27
- Résolus automatiquement : 0
- Résolus manuellement : 0
- Encore ouverts : 27
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

- [Decision] → Validation de l'utilisation du niveau disponible sur l'appareil avec tests réels prévus dans quelques jours
- [Decision] → Stockage des configurations en attente de tests réels
- [Decision] → Passage des fiches du statut draft à validé
- [Decision] → Retour sur la configuration pour la figer définitivement
- [Decision] → Travail sur les visuels dans `inbox/sites`
- [Decision] → Création d'une procédure de fiches spots pour stockage/gestion
- [Decision] → Décision de ne PAS demander aux utilisateurs de fixer des éléments individuellement (approche sphérique/globale)
- [Decision] → Acceptation de 40% de capital pour société chinoise DIaho sans représentation opérationnelle/management physique
- [Decision] Allocation mémoire iPhone** → Validation de l'utilisation du niveau disponible sur l'appareil avec tests réels prévus dans quelques jours
- [Decision] Documentation mémoire** → Stockage des configurations en attente de tests réels
- [Decision] Validation fiches** → Passage des fiches du statut draft à validé
- [Decision] Réorientation setup Lupo-RPI** → Retour sur la configuration pour la figer définitivement
- [Decision] Traitement des screenshots** → Travail sur les visuels dans `inbox/sites`
- [Decision] Procédure spots** → Création d'une procédure de fiches spots pour stockage/gestion
- [Decision] Facteur forme** → Décision de ne PAS demander aux utilisateurs de fixer des éléments individuellement (approche sphérique/globale)
- [Decision] Vetalyx Belgique** → Acceptation de 40% de capital pour société chinoise DIaho sans représentation opérationnelle/management physique
- [Failure] État** : Boot frozen à l'initialisation matérielle (Coulomb layer)
- [Failure] SSH inaccessible (connexions fermées : "Broken pipe")
- [Failure] Erreur `AppManager.install` : "system is not healthy - duplicate_os_install
- [Failure] Terminal RPI inaccessible de manière persistante
- [Failure] Ctrl+C non fonctionnel sur RPI

### Fréquence des patterns (14 jours)
- **Decision** : 2 jours, 19 occurrences
- **Failure** : 2 jours, 18 occurrences
- **Question** : 2 jours, 15 occurrences
- **Recurring question** : 2 jours, 12 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 21
- Jours d'observation : 2
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**410** recommandations au total — **410** ouvertes — **0** en cours — **0** terminées

⚠️ 397 recommandations ouvertes depuis plus de 7 jours.

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
