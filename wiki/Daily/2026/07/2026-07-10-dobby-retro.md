---
date: 2026-07-10
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1250
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-10

**Sessions analysées :** 4 | **Échanges :** 1250 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-07-10 | Dobby PKA System

## Décisions prises

1. **Migration vers modèle plus puissant** : Transfert décidé vers un modèle de développement supérieur (détails du modèle cible non spécifiés → *défaut de documentation*)
2. **Validation complète PKA** : "validé à 100%" après mise à jour fichiers utiles et notification équipe (statut : OK)
3. **Intégration projet Vetalyx** : Acceptation demande société chinoise, intégration au portefeuille projets
4. **Déplacement ressources plantes** : Décision de déplacer données vers localisation définitive
5. **Passage en mode manuel** : Abandon procédure automatisée pour opération de fichiers (cause : non documentée)
6. **Abandon URL Yahoo** : Décision de laisser tomber endpoint 404 (absence de raison justifiée)

**Problème critique** : 6 décisions sur 6 manquent de **contexte de raison** ou **détails d'implémentation**. Aucune trace de "pourquoi" — juste des "quoi".

---

## Échecs ouverts / bloqueurs

### **CRITIQUES (system-blocking)**

1. **RPI terminal inaccessible** 
   - Ctrl+C non fonctionnel sur RPi
   - Impossibilité de travailler dans terminal RPI (demande répétée 3x)
   - Statut : **NON RÉSOLU**
   - Impact : Bloque accès à 165 mentions d'activités RPi dans le système

2. **Montage système de fichiers échoué**
   ```
   ls /mnt/mount: fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5
   ```
   - **Blocage complet** : "tout est bloqué"
   - Cause : Superblock SQUASHFS manquant ou corrompu
   - Workaround : Déplacement manuel en cours
   - Statut : **CRITIQUE**

3. **Accès DB team.db**
   - Fichier inaccessible (mentionné 2x)
   - Statut : **NON RÉSOLU**

### **MAJEURS (service-impacting)**

4. **Crash Outlook** 
   - "Outlook s'est crashé" → remise en place en cours
   - Impact : Communication équipe affectée

5. **Erreurs HTTP 404 multiples**
   - Endpoints morts (Yahoo, fichiers .xz)
   - Pas de fallback configuré

6. **Whisper (STT) dysfonctionnel**
   - "Whisper ne fonctionne pas dans VS Code"
   - Debugging en cours, statut flou

7. **Problèmes locale/encoding Debian**
   ```
   LC_CTYPE=UTF-8 LC_ALL=
   ```
   - Avertissement reconfiguration locales nécessaire
   - Peut affecter gestion paquets

### **MINEURS (work-in-progress)**

8. **Déplacement fichiers plantes** : Vérification manuelle requise
9. **Gestion multi-modèles OpenRouter** : Workflow pas clarifié
10. **Composant X1201-C1** : Spécification de connecteur SSD floue

---

## Questions récurrentes (signe de lacune documentaire)

### **Hautement répétitives (4+ occurrences)**

| Question | Occurrences | Implication |
|----------|------------|-------------|
| "Pourquoi n'as pas accès au terminal RPi ?" | 3 | **Documentation manquante sur accès RPi** |
| "Comment utiliser OpenRouter dans VS Code + choix modèle ?" | 2+ variantes | **Workflow OpenRouter non documenté** |
| "C'est la même commande en terminal VS Code vs natif ?" | 2+ | **Confusion shell VS Code vs natif** |

### **Concepts non expliqués (définitions manquantes)**

1. **"Memory nudge"** — Mentionné 2x sans définition. *Est-ce une feature Dobby ? Un pattern mémoire ?*
2. **"(.env) en début de path"** — Pourquoi `.env` ? Gestionnaire de secrets ou charge de session ?
3. **"X1201-C1"** — Numéro de composant sans datasheet ou lien contexte
4. **"GM 5.2"** — Outil/framework non présenté

### **Problèmes d'accès répétitifs**

- "Pourquoi team.db inaccessible ?"
- "Pourquoi RPi boot ?" 
- "Pourquoi Whisper ne fonctionne pas ?"

**Root cause** : **Pas de runbook de diagnostic** pour ces trois composantes.

---

## Nouveaux patterns détectés

### **1. Fragmentation de contexte multi-projet**
- **Home Assistant** : 22+ mentions (42 variantes + dérivés)
- **Wildnexus** : 14 mentions
- **Vetalyx** (nouveau) : 1 mention → **intégration chaotique possible**
- **Projet Plantes** : fichiers en déplacement
- **Camping/fermes privées** : mention priorité non-tech (signal de dérive scope ?)

**Signal** : Trop de contextes parallèles. Dobby doit tracker 4+ projets simultanément sans frontière claire.

### **2. Oscillation outil Claude vs DeepSeek**
```
- CLAUDE mentions : 116x
- deepseek-v4 / deepseek-v4-pro : utilisés en session
```
**Hypothèse** : Basculage dynamique selon tâche. Pas de règle de routage explicite → inefficacité.

### **3. Transfert fichiers binaires volumineux**
- Git pack : 1,92 Go (historique binaire lourd)
- Composants électroniques (images Mouser, fichiers photos Canon EOS R10)
- Ressources plantes en déplacement

**Signal** : Gestionnaire versioning pas adapté aux assets volumineux.

### **4. Dépendances matérielles critiques non documentées**
```
Mentionnées dans ordre :
- RPi (165x) + M5 (89x) + RPI (21x) + M1 (20x)
- Accès réseau (lupo-rpi.local)
- Montage NVMe : nvme0n1p5
```
**Signal** : Topology infra complexe. Pas de schéma unique.

### **5. Détournement scope "camping/fermes"**
> "priorité: camping sauvage dans endroits exceptionnel, utilisation installation chez privé notamment les fermi"

**Alerte** : Contexte non-tech glissé dans logs système. Collision projet ?

---

## Efficacités / inefficacités

### **INEFFICACITÉS** 🔴

| Inefficacité | Preuve | Coût estimé |
|--------------|--------|------------|
| **Workaround manuel vs automatisé** | "Non ça marche pas. Je vais le faire manuellement" (2x) | +30 min/occurrence |
| **Pas de diagnostic systématique** | Questions "pourquoi" = 7/50 sans réponse directe | Frustration, blocage |
| **Répétition documentation** | 4 questions récurrentes = 4 explications duplicatas | -2h/semaine |
| **Accès RPI bloqué mais non triagé** | Ctrl+C ne fonctionne, mais pourquoi ? (non investigué) | **Bloque 165 références** |
| **Débordement scope** | Camping + fermes + pharma + electronics + plantes | Perte focus contextuelle |
| **Montage FS en cascade** | Erreur SQUASHFS → workaround manuel → "tout est bloqué" | Cascade de dépendances |
| **404 ignorées au lieu de resolver** | "On laisse Yahoo" au lieu de redirect/fallback | Dette technique |

### **EFFICACITÉS** ✅

| Efficacité | Preuve | Gain |
|-----------|--------|------|
| **Escalade rapide vers modèle supérieur** | Décision prise + exécution valide | Pas de thrashing |
| **Équipe DB stable** | 32 membres, 31 spécialistes + Dobby | Support parallelizable |
| **Sauvegarde complète** | "Sauvegarde le. Tous ce travail sur les plantes" validé | Prévention data loss |
| **OpenRouter intégration active** | 18 mentions, utilisé en session | Multi-model routing fonctionnel |
| **Reconnaissance image** | Photo Canon R10 → Dobby identification automatique | Asset tracking OK |
| **Dépôt git stable** | 1,92 Go organisé malgré historique lourd | Versioning maîtrisé |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### **CRITIQUES À MÉMORISER**

1. **RPI access = blocker** : Terminal inaccessible. Ctrl+C non-responsive. **Action requise avant prochaine session RPi.**
2. **SQUASHFS superblock missing** : nvme0n1p5 monté sur /mnt. **Ne pas redémarrer RPI jusqu'à diagnostic.**
3. **Team.db inaccessible** : Statut DB inconnu. Check permissions + disk space avant accès.
4. **OpenRouter model selection** : Workflow pas clair pour utilisateur → **documenté obligatoire**.

### **PATTERNS STABLES**

- **Claude vs DeepSeek** : Routage par tâche ; conserver flexibilité.
- **Équipe Dobby** : 56+ interactions = asset critique. Sauvegardes à jour.
- **Multi-projet** : 12 actifs ; risque fragmentation. Tracker par UUID/tag.

### **À NE PAS RÉPÉTER**

- Accepter décision ("validé") sans documenter le **pourquoi**.
- Basculer en "mode manuel" sans enregistrer l'échec automatisé.
- Laisser erreurs 404 trainer sans fallback.
- Laisser questions sans définitions (memory nudge, X1201-C1, GM 5.2).

### **CONTEXTE SCOPE**

- **Projets actifs** : Home Assistant (42), Wildnexus (14), Vetalyx (1 ← NOUVEAU), Plantes (1), Camping/Fermes (?)
- **Machines de base** : RPi (primary), M5 (secondary), M1 Mac (dev)
- **Outils fixes** : Claude (principal), DeepSeek (fallback/analyse), Docker (infra)

---

## Recommandations

### **🔴 IMMÉDIAT (< 24h)**

1. **Diagnostiquer RPI terminal access**
   - SSH fonctionne (logs montrent connexion réussie)
   - Ctrl+C dysfonctionnel → PTY issue ? Signal handling ?
   - **Action** : Tester `stty`, `script`, PTY allocation
   - **Owner** : Infrastructure

2. **Réparer SQUASHFS mount**
   ```bash
   fsck.squashfs /dev/nvme0n1p5  # ou vérifier intégrité image
   mount -o ro /dev/nvme0n1p5 /mnt  # test lecture seule
   ```
   - **Owner** : Infrastructure / JCH

3. **Checker team.db intégrité**

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 57
- Résolus automatiquement : 5
- Résolus manuellement : 0
- Encore ouverts : 52
- **Taux : 8.8%**

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

- [Decision] : Transfert décidé vers un modèle de développement supérieur (détails du modèle cible non spécifiés → *défaut de documentation*)
- [Decision] : "validé à 100%" après mise à jour fichiers utiles et notification équipe (statut : OK)
- [Decision] : Acceptation demande société chinoise, intégration au portefeuille projets
- [Decision] : Décision de déplacer données vers localisation définitive
- [Decision] : Abandon procédure automatisée pour opération de fichiers (cause : non documentée)
- [Decision] : Décision de laisser tomber endpoint 404 (absence de raison justifiée)
- [Decision] : 6 décisions sur 6 manquent de **contexte de raison** ou **détails d'implémentation**. Aucune trace de "pourquoi" — juste des "quoi".
- [Decision] Migration vers modèle plus puissant** : Transfert décidé vers un modèle de développement supérieur (détails du modèle cible non spécifiés → *défaut de
- [Decision] Validation complète PKA** : "validé à 100%" après mise à jour fichiers utiles et notification équipe (statut : OK)
- [Decision] Intégration projet Vetalyx** : Acceptation demande société chinoise, intégration au portefeuille projets
- [Decision] Déplacement ressources plantes** : Décision de déplacer données vers localisation définitive
- [Decision] Passage en mode manuel** : Abandon procédure automatisée pour opération de fichiers (cause : non documentée)
- [Decision] Abandon URL Yahoo** : Décision de laisser tomber endpoint 404 (absence de raison justifiée)
- [Failure] 1. **RPI terminal inaccessible
- [Failure] Ctrl+C non fonctionnel sur RPi
- [Failure] Impossibilité de travailler dans terminal RPI (demande répétée 3x)
- [Failure] Statut : **NON RÉSOLU
- [Failure] Impact : Bloque accès à 165 mentions d'activités RPi dans le système
- [Failure] Blocage complet** : "tout est bloqué
- [Failure] Cause : Superblock SQUASHFS manquant ou corrompu
- [Failure] Workaround : Déplacement manuel en cours
- [Failure] Fichier inaccessible (mentionné 2x)
- [Failure] RPI terminal inaccessible
- [Failure] Montage système de fichiers échoué

### Fréquence des patterns (14 jours)
- **Decision** : 9 jours, 34 occurrences
- **Question** : 9 jours, 26 occurrences
- **Failure** : 8 jours, 42 occurrences
- **Recurring question** : 7 jours, 24 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 24
- Jours d'observation : 11
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**253** recommandations au total — **253** ouvertes — **0** en cours — **0** terminées

⚠️ 191 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 215
- **Forge** : 31
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=246] (2026-07-10) **Dobby** : 1. **Diagnostiquer RPI terminal access
- [id=247] (2026-07-10) **Dobby** : SSH fonctionne (logs montrent connexion réussie)
- [id=248] (2026-07-10) **Dobby** : Ctrl+C dysfonctionnel → PTY issue ? Signal handling ?
- [id=249] (2026-07-10) **Forge** : Action** : Tester `stty`, `script`, PTY allocation
- [id=250] (2026-07-10) **Dobby** : Owner** : Infrastructure

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $24.94 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $24.94**
