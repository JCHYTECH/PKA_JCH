---
date: 2026-07-05
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1039
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-07-05

**Sessions analysées :** 2 | **Échanges :** 1039 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE SESSIONS 2026-07-05 - PKA & PROJETS CRITIQUES

## Décisions prises

### Validées
- **Achat composants** : Rejet MOQ Meramake (10u), pivot vers EPS pour M0
- **Délai de livraison** : Report au 30 juin (images/vidéo IR en Belgique)
- **Sauvegarde projet plantes** : Confirmée et documentée
- **Déplacement matériel** : Validation de relocalisation physique (vérification accès dossier `/Users/jchavauxm5/` pending)
- **MQTT** : Décision en attente ("je choisis quel mqtt ?") → **À formaliser**
- **Tests ESP32** : Démarrage imédiat avec accès chemin utilisateur confirmé
- **Rappel système** : À intégrer dans reminders (domaine flou)
- **Partenariat pharma** : Aenova (8 sites industriels vétérinaires) — contexte Vetalyx non clarifié

### Non finalisées (ambigu, reportées ou abandonnées)
- Sélection MQTT (aucun modèle choisi)
- Clarification X1201-C1 et connexion SSD
- Stratégie d'accès Apple Notes depuis outils IA

---

## Échecs ouverts / bloqueurs

### Matériel / Électronique
1. **Camera 1005005710463218** : État inconnu, pas de suivi visible
2. **API crash** : "upstream connect error or disconnect/reset before head" → **Pas diagnostiqué**
3. **OV5640 + ESP32-S3** : Pinout incompatibilité identifiée (ancien brochage ESP32-CAM ≠ OV5640 24-pin) → Nécessite recâblage ou module compatible

### Logiciels / Intégrations
4. **OpenRouter launcher** : Fonction dysfonctionnelle (crash après clic) → À déboguer
5. **Zigbee network creation** : `NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT` → Problème déterministe non résolu
6. **Git pack bloat** : 1,92 Go historique binaire → À nettoyer (rebase, purge)
7. **Health-check PKA** : RED status, faux positifs massifs → Métrique non fiable
8. **Traceback non capturé complet** : Fichier `/Users/jchavauxm5/PKA_JCH/s...` → Truncué, impossible diagnostic

### Accès / Contexte
9. **Accès Apple Notes** : JCH utilise Apple Notes, zéro intégration API visible → Bloque recherche contexte
10. **Yahoo API 404** : "on laisse yahoo" → Contournement au lieu de résolution

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Récurrence | Diagnostic |
|----------|-----------|-----------|
| "Comment tu accèdes à Apple Notes ?" | 2x+ | **Absence doc intégration externe** |
| "Comment faire recherches logiques et pro ?" | 2x+ | **Méthodologie PKA non documentée publiquement** |
| "C'est quoi harness ?" | 3x+ | **Terme technique vague, contexte WildNexus/WildMesh absent** |
| "Memory nudge c'est quoi ?" | 2x+ | **Feature interne Dobby non expliquée** |
| "Pourquoi (.env) au début du path ?" | 2x+ | **Convention shell/venv mal enseignée** |
| "Terminal vs VSCode terminal — c'est la même commande ?" | 2x+ | **Confusion PATH/env, zsh vs bash** |
| "C'est quoi X1201-C1 ?" | 2x+ | **Nomenclature matériel sans référence** |
| "OpenRouter dans VSCode + choix modèle ?" | 2x+ | **Doc config manquante pour Claude Code/Codex CLI** |

**→ Root cause** : Pas de **glossaire PKA** (harness, memory nudge, X1201-C1), pas de **guide intégration outils** (OpenRouter, Apple Notes), pas de **documentation shell** (env vars, terminals).

---

## Nouveaux patterns détectés

### Multimodalité chaotique
- JCH mixe **3 outils** : DeepSeek TUI, Claude Code, Codex CLI
- **0 coordination explicite** entre eux (ex: qui sauvegarde où ?)
- Décisions vocales → transcription textuelle → implémentation → **zéro audit trail**

### Pharmacie + IoT : fusion incongruente
- Vetalyx (corticoïdes vétérinaires, GMP, CDMO) **VS** WildNexus (capteurs OV5640, Zigbee, ESP32)
- **Même contexte PKA** (18 Go, 12 projets) → Aucune séparation domaine métier visible
- Indicateur : Aenova (pharma) et MEMS microphones dans même transcript

### "Validation sans confirmation"
- "validé oui" → aucun critère, aucun signataire
- "on va essayer à partir d'ici" → essai lancé sans baseline, sans success criteria
- "bon ca marche pas" → absence post-mortem

### Reminders comme pansement
- "mets dans les reminders de me le pro..." → **fragment, incomplet**
- Symptôme : JCH délègue mémoire à Dobby sans architecture (Dobby peut-il vraiment rappeler ?)

---

## Efficacités / inefficacités

### ❌ Inefficacités critiques

| Inefficacité | Impact | Fréquence |
|---|---|---|
| **Décisions sans specs** ("validé oui", "quel mqtt") | 3+ semaines de blocage si implémentation commence | Systématique |
| **Zéro doc glossaire** | Questions identiques x3+ par session | Systématique |
| **Crash tools non post-mortems** (API crash, openrouter, zigbee) | Perte contexte debug, répétition risque | Tous les bloqueurs |
| **Accès notes Apple impossible** | JCH doit re-contextualize à chaque session | À chaque démarrage |
| **Git 1,92 Go bloat** | CI/CD lent, clone réseau lent, DevOps debt | Passif mais croissant |
| **Health-check faux positifs** | Dashboard inutilisable, zéro confiance PKA | Daily noise |
| **Pharma + IoT dans même namespace** | Conf coulée, query ambigue (X1201-C1 hardware? pharma ref?) | Chaque projet |

### ✅ Efficacités à garder

| Efficacité | Bénéfice |
|---|---|
| **Dobby comme orchestrateur mémoire** | Historique structuré, patterns tracés |
| **Multi-modèle (deepseek + claude)** | Redondance expertise (une API crash = other backups) |
| **Accès chemin utilisateur préservé** | Continuité tests (esp32, M0, M1, M5, RPI) |
| **Pharma research intégrée** | Contexte GMP/CDMO (Virbac, Aenova) accessibles à la demande |

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Domaine Pharmacie (Vetalyx track)
- **Lead fabricant** : Virbac S.A. (Carros, France) → Cortavance®, Easotic®
- **Partenaire CDMO envisagé** : Aenova (8 sites vétérinaires EU-GMP approuvés)
- **Composant clé** : Hydrocortisone aceponate corticoïde puissant → Exigences Highly Potent APIs en suspension liquide
- **Fournisseur composants détecté** : Mouser (MMICT5848 microphone I2S, VSLB3940 IR 940nm, EKMB1203111 motion sensor)

### Domaine IoT/Électronique (WildNexus track)
- **Camera module problématique** : OV5640 24-pin + ESP32-S3 → **Pinout incompatibilité critique** (ancien ESP32-CAM brochage ≠ OV5640)
- **Zigbee blocker persistent** : NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT → À debugger (ACK timeout = TX/RX range, capacitor, ou firmware)
- **Décision MQTT suspendue** : Modèle non spécifié
- **Images/vidéo IR Belgique** : En attente, délai au 30 juin

### Infrastructure PKA
- **Taille critique** : 18 Go, 12 projets actifs, 32 membres DB (+Dobby)
- **Processus runtime** : dashboard, telegram-bot, gateway, docker (4 processus)
- **Santé** : RED health-check (faux positifs) → À recalibrer
- **Techdebt** : Git 1,92 Go binaire → À nettoyer (rebase, push --force-with-lease)

### Outils & accès
- **OpenRouter** : Launcher dysfonctionnel → À déboguer (VSCode integration)
- **Apple Notes** : JCH préfère notes natives → Aucune intégration API visible (blocage critique pour contexte JCH)
- **Paths actifs** : `/Users/jchavauxm5/` confirmé accessible
- **Modèles utilisés** : deepseek-v4, deepseek-v4-pro

---

## Recommandations

### 🔴 URGENT (semaine 1)

1. **Créer glossaire PKA obligatoire** (Markdown, versionné Git)
   - Termes : harness, memory nudge, X1201-C1, meramake MOQ, EPS (M0), etc.
   - Cible : zéro répétition question dans session suivante
   - Propriétaire : Dobby (auto-update)

2. **Formaliser MQTT choice** → JCH doit confirmer modèle ou critiquer options
   - Proposer 3 modèles (ex: Mosquitto MQTT5, Aedes, HiveMQ) + matrice critères
   - Decision deadline : avant prochaine session IoT

3. **Post-mortem Zigbee timeout** (NcpResetCode.ERROR_EXCEEDED_MAXIMUM_ACK_TIMEOUT_COUNT)
   - Reproduire erreur isolée
   - Vérifier TX power, capacitors, antenna, firmware version Zigbee coordinator
   - Documenter root cause + workaround

4. **Déboguer OpenRouter launcher**
   - Reproduire crash dans VSCode Claude extension
   - Capturer full stacktrace (ta version tronquée est inutile)
   - Test fallback DeepSeek TUI

5. **Intégrer Apple Notes** (ou alternative synchrone)
   - Option A : script iCloud Notes → PostgreSQL (JSONb)
   - Option B : JCH migrée Obsidian + git sync (meilleur audit)
   - Option C : webhook Apple Notes → Slack (perte richesse média)
   - Deadline : décider option avant J+3

### 🟡 IMPORTANT (semaine 1-2)

6. **Nettoyer Git pack

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 41
- Résolus automatiquement : 5
- Résolus manuellement : 0
- Encore ouverts : 36
- **Taux : 12.2%**

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

- [Decision] Achat composants** : Rejet MOQ Meramake (10u), pivot vers EPS pour M0
- [Decision] Délai de livraison** : Report au 30 juin (images/vidéo IR en Belgique)
- [Decision] Sauvegarde projet plantes** : Confirmée et documentée
- [Decision] Déplacement matériel** : Validation de relocalisation physique (vérification accès dossier `/Users/jchavauxm5/` pending)
- [Decision] MQTT** : Décision en attente ("je choisis quel mqtt ?") → **À formaliser
- [Decision] Tests ESP32** : Démarrage imédiat avec accès chemin utilisateur confirmé
- [Decision] Rappel système** : À intégrer dans reminders (domaine flou)
- [Decision] Partenariat pharma** : Aenova (8 sites industriels vétérinaires) — contexte Vetalyx non clarifié
- [Failure] : État inconnu, pas de suivi visible
- [Failure] : "upstream connect error or disconnect/reset before head" → **Pas diagnostiqué
- [Failure] : Pinout incompatibilité identifiée (ancien brochage ESP32-CAM ≠ OV5640 24-pin) → Nécessite recâblage ou module compatible
- [Failure] Camera 1005005710463218** : État inconnu, pas de suivi visible
- [Failure] API crash** : "upstream connect error or disconnect/reset before head" → **Pas diagnostiqué
- [Failure] OV5640 + ESP32-S3** : Pinout incompatibilité identifiée (ancien brochage ESP32-CAM ≠ OV5640 24-pin) → Nécessite recâblage ou module compatible

### Fréquence des patterns (14 jours)
- **Decision** : 7 jours, 38 occurrences
- **Question** : 7 jours, 18 occurrences
- **Failure** : 6 jours, 36 occurrences
- **Recurring question** : 5 jours, 17 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 14
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**234** recommandations au total — **234** ouvertes — **0** en cours — **0** terminées

⚠️ 172 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 198
- **Forge** : 29
- **Corbeau** : 4
- **Furet** : 3

### Plus récentes ouvertes

- [id=215] (2026-07-05) **Dobby** : Créer glossaire PKA obligatoire** (Markdown, versionné Git)
- [id=216] (2026-07-05) **Dobby** : Termes : harness, memory nudge, X1201-C1, meramake MOQ, EPS (M0), etc.
- [id=217] (2026-07-05) **Dobby** : Cible : zéro répétition question dans session suivante
- [id=218] (2026-07-05) **Dobby** : Propriétaire : Dobby (auto-update)
- [id=219] (2026-07-05) **Dobby** : Formaliser MQTT choice** → JCH doit confirmer modèle ou critiquer options

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $10.55 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $10.55**
