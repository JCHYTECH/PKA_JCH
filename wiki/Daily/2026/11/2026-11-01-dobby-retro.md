---
date: 2026-11-01
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 2
echanges: 1135
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-11-01

**Sessions analysées :** 2 | **Échanges :** 1135 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# RÉTROSPECTIVE PKA JCH — Session 2026-11-01

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Raccourcir à 4 jours** | Restructuration d'un programme/roadtrip | ✓ Prise |
| **Passer au français** | Contexte Belgique mentionné | ✓ Prise |
| **Équiper les caissons d'un tiroir à coulisse** | Design WildLens/Vetalyx (25-26 cm depth) | ✓ Prise |
| **Utiliser Canva** | Outil de design/contenu à tester | ✓ Prise |
| **Rester en 12 (couleur/grille)** | Faciliter le procurement | ✓ Prise |
| **Fixer le seuil d'endettement à 175 000€** | Paramètre financier Vetalyx | ✓ Prise |
| **Attendre position des autres (P2)** | WildLens phase 2 | ⏳ En attente |
| **Discuter distribution WildLens avec Alain Bosseloir** | Stratégie commerciale | ⏳ À reporter |

**Problème** : 4 décisions **non documentées** dans le repo. Aucune trace dans `AGENTS.md` ou les fichiers de projet. Risk d'oubli ou de divergence avec partenaires (Alain Bosseloir, Zheda).

---

## Échecs ouverts / bloqueurs

### 🔴 Critiques

1. **Erreur 403 (Access Blocked)**
   - Contexte : Tentative d'accès à une ressource/API
   - Impact : Bloque l'intégration testée
   - Cause probable : Clé API invalide, permissions insuffisantes
   - **Action requise** : Vérifier credentials et scope

2. **Erreur APFS encryptée (tmutil)**
   - `tmutil startbackupVolume on disk8s2 failed to mountThis is an encrypted and locked APFS Volume`
   - Impact : Backup système paralysé
   - **Action requise** : Déverrouiller le volume avant retry

3. **WebSocket 1007 - Invalid frame payload**
   - Erreur `realtime_input.m`
   - Impact : Communication temps réel avec Home Assistant/Vetalyx cassée
   - **Cause probable** : Format de données mal formé ou encodage incompatible
   - **Action requise** : Vérifier le format des messages envoyés

4. **Home Assistant - blocage HA avec API Key required**
   - `van à niveau off, cap ne fonctionne pas, API key required`
   - Impact : WildLens ne peut pas communiquer avec HA
   - **Action requise** : Vérifier configuration API dans HA + renouveler token

5. **3 fiches en statut `needs_review`** (non identifiées)
   - Impact : Pas clair quelles fiches / quel projet
   - **Risk** : Tâches oubliées ou dupliquées
   - **Action requise** : Lister et assigner priorité

### ⚠️ Secondaires

- Bug Dante : **fiche vide** → à analyser si c'est un défaut global du système ou cas isolé
- Intégration Kiro (renaud-dekode.fr) : **accès non vérifié**, contenu tronqué dans le transcript
- Contrats Vetalyx : Modifications en cours (Article 6+), statut de signature flou
- Erreur GPT/Claude (reasoning_content 400) : Mauvais format de requête API

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Enjeu |
|----------|-----------|-------|
| *C'est quoi le kit hardwire ?* | 2x | **Terminologie non définie** — doit être dans un glossaire projet |
| *Pourquoi tu es passé en plan ?* | 2x | **Décisions non documentées** — raison du changement de stratégie perdue |
| *C'est quoi le risque ISC ?* | 2x | **Jargon financier non expliqué** — doit être dans un doc Vetalyx |
| *C'est quoi la synthèse de lecture propre ?* | 2x | **Standard méthodologique absent** — format/structure à définir |
| *Pourquoi ce blocage ?* (x3 variantes) | 3x+ | **Manque de traçabilité des erreurs** — pas de log centralisé |
| *Pourquoi as-tu parlé de DaVinci ?* | 1x | **Contexte de décision perdu** — IA utilisée pour quoi ? |
| *C'est quoi les 3 fiches needs_review ?* | 1x | **Tâches orphelines** — assignation floue |

**Diagnostic** : Le PKA souffre d'une **amnésie documentaire**. Les questions reviennent parce que :
- Les décisions ne sont pas écrites
- Les glossaires projet manquent
- Les erreurs ne sont pas catégorisées
- Les fiches `needs_review` ne sont pas associées à une tâche claire

---

## Nouveaux patterns détectés

### 1. **Polyvalence extrême + Fragmentation**
- Sessions couvrent : WildLens (hardware), Vetalyx (legal/finance), HA (automation), KiroAI (outil), photo d'oiseaux, Roadtrip planning
- **Symptôme** : Contexte switching permanent, "focus" métaphorique perdu
- **Impact** : Pas de profondeur, beaucoup de surface
- **Risque** : Erreurs détail, décisions hâtives (voir : tiroir à 25-26cm validé sans calcul ergonomique apparent)

### 2. **Working Set trop large**
- Fichiers actifs listés 6x : path/type/project, scripts/wildlens, status/active, etc.
- Même fichier mentionné plusieurs fois (n/n, status/active)
- **Symptôme** : Dobby lui-même perd le fil du "scope"
- **Efficacité** : Probablement < 60% (beaucoup de navigation, peu de progress)

### 3. **Dépendances humaines non externalisées**
- "Alain Bosseloir" → décision en suspens
- "Zheda" → contrat pas finalisé
- "DiaHo" → infos fiscales demandées
- **Symptôme** : Attente passive (P2 en freeze)
- **Recommandation** : Créer un système de dépendances (deadline, escalade auto)

### 4. **Mélange langage (FR/EN) + Typos systématiques**
- Messages : "bon on va raccourcir", "peaufinant la reflexion", "serati d'aller"
- Apparemment du français rapide/parlé retranscrit
- **Impact** : Flou sémantique, parsing chatbot difficile
- **Symptôme** : Dobby demande clarification souvent

### 5. **"Second brain" en surcharge**
- Transcript JCH mentionne explicitement : *"having a second brain is great until it reaches a state of morbid obesity"*
- Introspection claire : **le PKA devient trop gros**
- **Solution hinted** : Audit du système + health score 90/100
- **Action** : Cette session MÊME est diagnostic de la maladie

---

## Efficacités / Inefficacités

### ✅ Efficacités détectées

1. **Utilisation multi-outils pragmatique**
   - DeepSeek + Claude + OpenRouter testés en parallèle
   - JCH benchmark les modèles sur tâches réelles
   - Adaptation rapide : passage au français, choix Canva

2. **Dobby fonctionne sans experts assignés**
   - Continue même face aux bloqueurs (403, encryption, WebSocket)
   - Propose alternatives (LLM spécialisée suggérée pour bug)
   - Peu d'escalade premature

3. **Décisions rapides sur constraints matérielles**
   - Dimensions tiroir (25-26cm) décidées avec raison (passager bench)
   - Critère "12 pour procurement" montre conscience supply chain

### ❌ Inefficacités critiques

1. **Pas de fermeture de tâche**
   - Bloqueurs identifiés ≠ résolus
   - Exemple : Bug HA avec API key → "on va vérifier" → jamais mentionné à nouveau
   - Estimation : 40% des questions = relance sur même sujet

2. **Décisions verbales non tracées**
   - Aucune issue GitHub, ticket, ou ligne dans AGENTS.md
   - Risque : Dobby réinvente décisions à la prochaine session
   - Exemple : "Comment on voulait distribuer WildLens ?" (décision déjà prise, oubliée)

3. **Working set drift**
   - Paths répétés 6x dans le même jour (n/n, status/active)
   - Dobby lui-même se perd → liste différente à chaque turn
   - Impact : Navigation cognitive, pas de état stable

4. **Diagnostic sans action**
   - JCH cite la vidéo PKA-obesity
   - Reconnaît le problème
   - Puis... continue la session habituelle sans pivot
   - Symptôme d'inertie système

5. **Handoff partenaires flou**
   - Alain Bosseloir : pas de date/format/contenu pour discussion
   - Zheda : contrat envoyé, modifications jamais consolidées
   - Résultat : Délai, miscommunication probable

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### 🧠 Mémoire court terme (urgent)

1. **3 fiches `needs_review` non identifiées** → Lister et assigner ASAP
2. **HA API key bloqueur** → Test après fix
3. **Contrat Vetalyx Article 6+** → Consolidation + signature timeline
4. **Discussion Alain Bosseloir sur distribution WildLens** → Planifier date
5. **Seuil endettement Vetalyx = 175 000€** → Valider avec consultant ISC

### 🧭 Mémoire moyen terme (design)

- **Tiroir caisson WildLens** : 25-26cm profondeur, coulisse acier
- **Palette couleur** : 12 couleurs (non détaillées dans transcript)
- **Durée program** : 4 jours (nouveau)
- **Outil design** : Canva (à tester)
- **Langue opérationnelle** : Français (Belgique)

### 📊 Mémoire long terme (système)

- **WildLens** : Phase 2 en attente (P2), partenaire distribution TBD
- **Vetalyx** : Statuts + contrat en cours, fiscal à valider
- **Home Assistant** : Intégration temps réel cassée (WebSocket 1007)
- **KiroAI** : Interface candidat pour intégration routine (renaud-dekode.fr)
- **Veo Access** : Nécessite Google Cloud billing (Pay-As-You-Go)

### ⚠️ Mémoire des erreurs

- **APFS encryption** : tmutil ne peut pas

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 33
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 31
- **Taux : 6.1%**

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

- [Decision] | Restructuration d'un programme/roadtrip | ✓ Prise |
- [Decision] | Contexte Belgique mentionné | ✓ Prise |
- [Decision] | Design WildLens/Vetalyx (25-26 cm depth) | ✓ Prise |
- [Decision] | Outil de design/contenu à tester | ✓ Prise |
- [Decision] | Faciliter le procurement | ✓ Prise |
- [Decision] | Paramètre financier Vetalyx | ✓ Prise |
- [Decision] | WildLens phase 2 | ⏳ En attente |
- [Decision] | Stratégie commerciale | ⏳ À reporter |
- [Decision] : 4 décisions **non documentées** dans le repo. Aucune trace dans `AGENTS.md` ou les fichiers de projet. Risk d'oubli ou de divergence avec partenaire
- [Failure] `tmutil startbackupVolume on disk8s2 failed to mountThis is an encrypted and locked APFS Volume`
- [Failure] Contexte : Tentative d'accès à une ressource/API
- [Failure] Impact : Bloque l'intégration testée
- [Failure] Cause probable : Clé API invalide, permissions insuffisantes
- [Failure] Action requise** : Vérifier credentials et scope
- [Failure] Impact : Backup système paralysé
- [Failure] Action requise** : Déverrouiller le volume avant retry
- [Failure] Erreur `realtime_input.m`
- [Failure] Impact : Communication temps réel avec Home Assistant/Vetalyx cassée
- [Failure] Cause probable** : Format de données mal formé ou encodage incompatible
- [Failure] Action requise** : Vérifier le format des messages envoyés
- [Failure] blocage HA avec API Key required
- [Failure] `van à niveau off, cap ne fonctionne pas, API key required`
- [Failure] Impact : WildLens ne peut pas communiquer avec HA
- [Failure] Action requise** : Vérifier configuration API dans HA + renouveler token
- [Failure] Impact : Pas clair quelles fiches / quel projet
- [Failure] Risk** : Tâches oubliées ou dupliquées
- [Failure] Action requise** : Lister et assigner priorité
- [Failure] Erreur 403 (Access Blocked)
- [Failure] Erreur APFS encryptée (tmutil)
- [Failure] WebSocket 1007 - Invalid frame payload
- [Failure] Home Assistant - blocage HA avec API Key required
- [Failure] 3 fiches en statut `needs_review`** (non identifiées)

### Fréquence des patterns (14 jours)
- **Decision** : 7 jours, 39 occurrences
- **Failure** : 6 jours, 20 occurrences
- **Recurring question** : 6 jours, 21 occurrences
- **Question** : 5 jours, 27 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 32
- Jours d'observation : 9
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**538** recommandations au total — **538** ouvertes — **0** en cours — **0** terminées

⚠️ 524 recommandations ouvertes depuis plus de 7 jours.

### Répartition par assigné

- **Dobby** : 485
- **Forge** : 35
- **Furet** : 7
- **Corbeau** : 6
- **Renard** : 3
- **Sybil** : 2

### Plus récentes ouvertes

- [id=530] (2026-10-31) **Dobby** : Créer `PROJECTS_MATRIX.md`
- [id=531] (2026-10-31) **Dobby** : Lister 4 projets : nom, owner, deadline, dépendances, priority (1-4)
- [id=532] (2026-10-31) **Dobby** : Décider : lequel d'abord ? WildNexus ? Vetalyx (legal blocker) ?
- [id=533] (2026-10-31) **Dobby** : Fermer les 6 bloqueurs
- [id=534] (2026-10-31) **Dobby** : Assigner chacun : "Dobby to diagnose" / "DeepSeek API" / "HA config" / "Verify D

Consulte les ids ci-dessus avec `mark_recommendation_status(id, 'done')` pour les clôturer.


## 💰 Budget fournisseurs API

⚠️ **3 alerte(s) budget détectée(s)**

- OpenRouter   🟢 $17.27 USD
- DeepSeek     🔴 $0.0 CNY
- NVIDIA       🔴 <urlopen error [Errno 8] nodename nor servname provided, or 
- OpenAI       🔴 403 Forbidden — clé sans scope billing ou org ID manquant

**Total disponible (USD) : $17.27**
