---
date: 2026-08-10
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1034
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-08-10

**Sessions analysées :** 2 | **Échanges :** 1034 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Sessions 2026-08-10 – Dobby PKA Audit

## Décisions prises

- **Redémarrage isolé du Lupo-RPi** : Vérifier un redémarrage clean sans dépendances externes pour diagnostiquer l'état du système.
- **Arrêt temporaire des itérations stériles** : Décision de créer une documentation (.md) et de suspendre les tests répétitifs sur le RPi.
- **Validation et mise à jour des fichiers critiques** : Après tests, synchroniser tous les fichiers utiles et informer les membres.
- **Chiffrement du niveau iPhone disponible** : Évaluer l'envoi de données via le niveau d'encryptage natif iOS.
- **Transfert vers modèle plus robuste** : Basculer de deepseek-v4 vers une instance plus développée (non spécifiée).
- **Réception expert LLM** : Intégrer les recommandations d'un expert externe sur les SLM (Small Language Models) quantisés pour RPi5.
- **Gel du setup Lupo-RPi** : Figer la configuration actuelle en attente de tests réels dans quelques jours.
- **Report du Lupo au 31 août** : Décision de reprogrammer les tests critiques (délai accepté).
- **Investigation Vetalyx Belgique** : Confirmation que les actionnaires chinois (DIaho, 40%) n'ont pas besoin de déclaration opérationnelle spécifique selon UCM.

---

## Échecs ouverts / bloqueurs

### Critiques (production bloquée)

1. **Filesystem SQUASHFS manquant sur NVMe** 
   - `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5`
   - Impact : Impossible de booter le système complet, montage échoué.
   - Statut : **Ouvert** – Diagnostic en attente.

2. **Accès terminal RPi inaccessible**
   - La connexion SSH fonctionne mais le terminal ne répond pas comme attendu (ctrl+M, ctrl+C ineffectifs).
   - Impact : Impossibilité de debugger directement sur la machine.
   - Statut : **Ouvert** – Cause inconnue (environnement locale? SSH config?).

3. **Téléchargement Home Assistant OS échoué (404 + timeout)**
   - `HTTP 404 Not Found` + `Read error at byte 6059777 (Connection timed out)`
   - Fichier : `haos_rpi5-64-18.1.img.xz`
   - Tentative de réinstall Home Assistant – impossible de finir le flux.
   - Statut : **Ouvert** – Lien d'asset GitHub expiré ou réseau instable.

4. **Problème Whisper dans VSCode**
   - Module Whisper ne fonctionne pas, environnement unclear.
   - Statut : **Ouvert** – Diagnostic incomplet.

5. **Base de données team.db inaccessible**
   - Accès dénié ou fichier manquant.
   - Statut : **Ouvert** – Permissions? Chemin incorrect?

### Majeurs (fonctionnalité limitée)

6. **Vanroll test n'envoie plus de données**
   - `vanroll test` donne un résultat vide ou incorrect.
   - Régressiondepuis dernière session.
   - Statut : **Ouvert** – À vérifier après gel du setup.

7. **Locale non configurée sur RPi**
   - `LC_CTYPE=UTF-8, LC_ALL=` (vide) → warning système.
   - Impact mineur mais symptomatique d'un env. incomplet.
   - Fix : `sudo dpkg-reconfigure locales`.

8. **Instance Home Assistant en conflit**
   - Erreur détectée : "Une ancienne instance tourne en arrière-plan" après restauration de sauvegarde.
   - Possible UUID clash ou clonage de disque non nettoyé.
   - Statut : **Ouvert** – Nécessite investigation UUID + nettoyage.

---

## Questions récurrentes (signe de lacune documentaire)

### Tier 1 (très répétitif – **à documenter en priorité**)

- **"Pourquoi le RPi ne boot pas?"** (4 variantes détectées)
  - Lacune : Pas de "Boot Troubleshooting Flowchart" documenté.
  - À créer : `LUPO_BOOT_DIAGNOSIS.md` avec arbre de décision.

- **"Pourquoi pas d'accès au terminal RPi?"** (3 variantes)
  - Lacune : Pas de diagnostic SSH/locale/permissions documenté.
  - À créer : `RPI_TERMINAL_DEBUG.md`.

- **"Whisper ne fonctionne pas, c'est VSCode?"** 
  - Lacune : Dépendances Whisper + environnement VSCode jamais clarifié.
  - À créer : `WHISPER_SETUP.md`.

### Tier 2 (contexte manquant)

- **"C'est quoi L(M)?"** (notation technique non expliquée)
  - Probablement format de quantization GGUF (L = LoRA, M = Moyenne), jamais documenté en contexte JCH.

- **"On a 4 roues et un plus petit, c'est quoi?"** 
  - Contexte matériel vague, probablement projet robotique non documenté.

- **"Pourquoi team.db est inaccessible?"** (répété 2x)
  - Pas de guide permissions/chemin pour les DBs partagées en équipe.

- **"State files, c'est quoi?"** (Home Assistant)
  - Concept HA non expliqué pour novices.

---

## Nouveaux patterns détectés

### Pattern 1 : **Cycle Test → Blocage → Pivot Inexpliqué**
- Session suit un pattern : teste X → bloqueur non résolu → "on va faire une doc" → report date.
- Cause probable : Manque de stratégie d'escalade / diagnostic exhaustif avant pivot.
- Exemple : Lupo-RPi → report au 31 août sans root cause analysis finalisée.

### Pattern 2 : **Multiplexing outil non coordonné**
- DeepSeek, Claude, Composer History, Shell exec, File read mixés sans ordre clair.
- Résultat : Contexte fragmenté, commands exécutées sans validation préalable.
- À régulariser : Séquence stricte de diagnostic avant action.

### Pattern 3 : **Documentation réactive, pas proactive**
- Les décisions "on va créer un .md" apparaissent **après** les blocages, pas avant.
- Exemple : Protocole LLM reçu d'expert, pas intégré en MEMORY.md avant test.

### Pattern 4 : **Contexte métier non séparé de contexte technique**
- Vetalyx Belgique (actionnariat chinois, UCM) mixé avec debug RPi.
- Sessions manquent de séparation clear : stratégie vs ops vs infra.

---

## Efficacités / inefficacités

### ❌ Inefficacités critiques

| Inefficacité | Impact | Preuve |
|---|---|---|
| **Téléchargements non validés** | Perte 6h+ sur `haos_rpi5.img.xz` corrompu/expiré | Retry loop visible, 404 persistant |
| **SSH terminal limité** | Diagnostic RPi réduit à 50% de capacité | ctrl+M, ctrl+C ne répondent pas |
| **Pas de log centralisé** | Même question posée 3-4x par session | "pourquoi boot?" répété 4 fois |
| **Setup RPi non gelé** | Changements non documentés, dérives config | vanroll test régresse, locale non défini |
| **Escalade ad-hoc** | Chaque blocage → nouveau pivot sans escalade structurée | Expert LLM consulté tard, conseils pas intégrés |

### ✅ Efficacités conservées

| Efficacité | Valeur | Preuve |
|---|---|---|
| **Consultation d'experts** | Validation externe rapide | Réponse UCM reçue, expert LLM engagé |
| **Isolation test** | Décision de reboot isolé Lupo-RPi pertinente | Diagnostic root cause avant next iteration |
| **Tool multiplexing** | Rapidité d'exploration (grep, exec, read en cascade) | 1034 messages/2 sessions = pace soutenu |
| **Decision documentation** | Même partielle, crée une trace | Décisions listées malgré chaos de transcript |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🔴 Dépendances critiques en attente

1. **Lupo-RPi boot diagnosis** (report 31 août)
   - État: SQUASHFS manquant, SSH limité, locale non défini
   - Pré-requis avant next tests: Redémarrage isolé + vérification UUID/FS
   - Responsable: À assigner (JCH/Renard/autre?)

2. **Home Assistant OS restore conflict**
   - UUID clash détecté → nécessite nettoyage avant réinstance
   - Fichier asset GitHub `haos_rpi5-64-18.1.img.xz` à re-vérifier (lien expiré?)

3. **Whisper + team.db**
   - Deux régression fonctionnelles non diagnostiquées
   - Impact utilisateur unclear, à investiguer avant production

### 📋 Documentation à créer (délai: avant 31 août)

- [ ] `LUPO_BOOT_DIAGNOSIS.md` – Flowchart boot + SSH troubleshooting
- [ ] `RPI_TERMINAL_DEBUG.md` – Locale, ctrl keys, terminal responsiveness
- [ ] `WHISPER_SETUP.md` – Dépendances, VSCode config, test path
- [ ] `VETALYX_LLM_SETUP.md` – Intégrer conseils expert (SLM quantized, Ollama Q4_K_M)
- [ ] `HA_RESTORE_CHECKLIST.md` – UUID cleanup, asset validation, network isolation
- [ ] `TEAM_DB_ACCESS.md` – Permissions, chemins, sync protocol

### 🧠 Contexte métier à préserver

- **Vetalyx Belgique** : Actionnaires chinois (DIaho 40%) NON déclarables opérationnellement selon UCM → validé ✅
- **Camping sauvage + IoT privé** : Use case prioritaire pour Vetalyx (fermes, endroits exceptionnels)
- **Lupo-RPi** : Testbed pour cette use case, tests réels prévus après 31 août

### 🔧 Setup gelé à honorer

```
Lupo-RPi config actuelle (as of 2026-08-10):
- RPi5 8Go
- NVMe SSD (nvme0n1p5 – SQUASHFS issue)
- Geekworm HAT batterie (PSU_MAX_CURRENT=5000)
- Home Assistant OS 18.1 (incomplete, restore pending)
- Locale: undefined (fix: dpkg-reconfigure locales)
- SSH: Fonctionnel mais terminal limité
- Status: FROZEN pending reboot test + expert LLM integration
```

---

## Recommandations

### 1.

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

### Nouveaux patterns découverts aujourd'hui
*(identifiés par le LLM, non détectés par l'extraction locale)*

- [Decision] Redémarrage isolé du Lupo-RPi** : Vérifier un redémarrage clean sans dépendances externes pour diagnostiquer l'état du système.
- [Decision] Arrêt temporaire des itérations stériles** : Décision de créer une documentation (.md) et de suspendre les tests répétitifs sur le RPi.
- [Decision] Validation et mise à jour des fichiers critiques** : Après tests, synchroniser tous les fichiers utiles et informer les membres.
- [Decision] Chiffrement du niveau iPhone disponible** : Évaluer l'envoi de données via le niveau d'encryptage natif iOS.
- [Decision] Transfert vers modèle plus robuste** : Basculer de deepseek-v4 vers une instance plus développée (non spécifiée).
- [Decision] Réception expert LLM** : Intégrer les recommandations d'un expert externe sur les SLM (Small Language Models) quantisés pour RPi5.
- [Decision] Gel du setup Lupo-RPi** : Figer la configuration actuelle en attente de tests réels dans quelques jours.
- [Decision] Report du Lupo au 31 août** : Décision de reprogrammer les tests critiques (délai accepté).
- [Decision] Investigation Vetalyx Belgique** : Confirmation que les actionnaires chinois (DIaho, 40%) n'ont pas besoin de déclaration opérationnelle spécifique se
- [Failure] `fsconfig() failed: Can't find a SQUASHFS superblock on nvme0n1p5`
- [Failure] Impact : Impossible de booter le système complet, montage échoué.
- [Failure] Statut : **Ouvert** – Diagnostic en attente.
- [Failure] La connexion SSH fonctionne mais le terminal ne répond pas comme attendu (ctrl+M, ctrl+C ineffectifs).
- [Failure] Impact : Impossibilité de debugger directement sur la machine.
- [Failure] Statut : **Ouvert** – Cause inconnue (environnement locale? SSH config?).
- [Failure] `HTTP 404 Not Found` + `Read error at byte 6059777 (Connection timed out)`
- [Failure] Fichier : `haos_rpi5-64-18.1.img.xz`
- [Failure] Tentative de réinstall Home Assistant – impossible de finir le flux.
- [Failure] Statut : **Ouvert** – Lien d'asset GitHub expiré ou réseau instable.
- [Failure] Module Whisper ne fonctionne pas, environnement unclear.
- [Failure] Statut : **Ouvert** – Diagnostic incomplet.
- [Failure] Accès dénié ou fichier manquant.
- [Failure] Statut : **Ouvert** – Permissions? Chemin incorrect?
- [Failure] Filesystem SQUASHFS manquant sur NVMe
- [Failure] Accès terminal RPi inaccessible
- [Failure] Téléchargement Home Assistant OS échoué (404 + timeout)
- [Failure] Problème Whisper dans VSCode
- [Failure] Base de données team.db inaccessible

### Fréquence des patterns (14 jours)
- **Failure** : 2 jours, 19 occurrences
- **Question** : 2 jours, 14 occurrences
- **Recurring question** : 2 jours, 11 occurrences
- **Decision** : 1 jours, 11 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 28
- Jours d'observation : 3
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**365** recommandations au total — **365** ouvertes — **0** en cours — **0** terminées

⚠️ 357 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 322
- **Forge** : 33
- **Corbeau** : 5
- **Furet** : 5

### Plus récentes ouvertes

- [id=358] (2026-08-07) **Dobby** : Snapshot diagnostic RPI 5** :
- [id=359] (2026-08-07) **Dobby** : Tester serial console** :
- [id=360] (2026-08-07) **Dobby** : Brancher UART USB sur MAC
- [id=361] (2026-08-07) **Dobby** : Capturer early boot logs lors du hang
- [id=362] (2026-08-07) **Dobby** : → Fournira raison du boot bloqué

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.48 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.48**
