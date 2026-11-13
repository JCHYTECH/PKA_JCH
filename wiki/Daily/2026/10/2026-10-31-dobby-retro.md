---
date: 2026-10-31
type: retrospective
author: Dobby
tags: [retro, meta, auto-analyse, apprentissage]
sessions: 4
echanges: 1067
modeles: deepseek-v4, deepseek-v4-pro
---

# Rétrospective — 2026-10-31

**Sessions analysées :** 4 | **Échanges :** 1067 | **Modèles :** deepseek-v4, deepseek-v4-pro

---

# Rétrospective Session 2026-10-31 — PKA de JCH

## Décisions prises

| Décision | Contexte | Statut |
|----------|----------|--------|
| **Traiter les skips après, batch de 10** | Optimisation du traitement de données | Initiée |
| **Rester au niveau 1** (avec escalade conditionnelle) | Architecture de système, avec révision si nécessaire | À valider |
| **Faire des simulations, retour ultérieur** | WildNexus ou projet similaire | En attente de résultats |
| **Équiper les caissons de tiroirs avec coulisses** | Vanlife (Lupo Bianco) — meuble 104×55×25cm, 3 tiroirs | Design en cours |
| **Convertir les drafts en validés** (Vetalyx) | Gestion documentaire | En cours |
| **Poser des questions polies avant d'agir** | Collecte d'info préalable | Pattern établi |
| **Organiser un roadtrip** (travels) | Planification vanlife | Initiée |
| **Tester en live après validation** | Cycle de déploiement standard | À planifier |
| **Retirer l'alimentation du M1 pour le déplacer** | Infrastructure physique | Prévue (sans rush) |
| **Rester en 12V partout** | Vanlife — simplification procurement | Décision architecturale |

### Observation critique
Les décisions sont **fragmentées sur 4 axes majeurs** (WildNexus, Vetalyx, Vanlife, secondhand-selling) sans trace de dépendances inter-projets. Risque de dérive prioritaire.

---

## Échecs ouverts / bloqueurs

### Critiques (blocage immédiat)
- **API Error 1007** : `realtime_input.m` — frame payload data invalide (DeepSeek)
- **HA van niveau OFF** : CAP ne fonctionne pas + "API key required" en cascade
- **tmutil backup échoué** : Encrypted APFS Volume sur disk8s2 — nécessite unlock avant mount
- **Erreur 403** : Access blocked (origine non identifiée dans transcript)

### Importants (impact fonctionnel)
- **Bug HA non vérifié** : Dobby n'a pas encore confirmé la nature du problème
- **3 fiches needs_review** : Identité et raison inconnues (Vetalyx ?)
- **Fiche vide de Dante** : Diagnostic requis — incident ou correction globale nécessaire ?
- **Warn Invalid request (400)** : `reasoning_content` manquant ou malformé dans appel API

### Ouverts (sans urgence immédiate)
- **Raison de l'arrêt d'une procédure** : À réactiver mais cause inconnue
- **Demande ASIX AX88179B** : Apparaît comme device manquant (RPI ?) — non documenté

### Pattern dangéreux
Les erreurs techniques sont notées mais **rarement fermées** — accumulation de dettes diagnostiques.

---

## Questions récurrentes (signe de lacune documentaire)

| Question | Fréquence | Implication |
|----------|-----------|------------|
| **"Comment mémoriser les procédures et les lancer par nom ?"** | 2+ | Absence de registre de procédures — Dobby ne dispose pas d'index exécutable |
| **"Comment utiliser TTL 24h avec fluidité ?"** | 2+ | Concept de cache/session mal intégré dans le workflow — pas de pattern établi |
| **"Qu'est-ce que les 3 fiches needs_review ?"** | Récurrente | Métadonnées non documentées — risque de pertes d'information |
| **"Pourquoi cette fiche est vide ?"** | Récurrente | Absence de schéma de validation / complétude |
| **"C'est quoi le risque ISC à 175k€ d'endettement ?"** | 2+ | Définitions métier (ISC = ?) non externalisées — dépend de mémoire individuelle |
| **"C'est quoi le kit hardwire ?"** | Récurrente | Terminologie interne non documentée |
| **"Pourquoi Dobby ne s'appuie pas sur les experts ?"** | 1, mais fondamentale | Absence de cadre pour délégation / escalade vers spécialistes |

### Racine commune
**Pas de wiki/glossaire/procedure manifesto** — chaque question est un diagnostic symptomatique d'une lacune d'architecture informationnelle.

---

## Nouveaux patterns détectés

### 1. **Mode "Second Brain Audit"**
JCH questionne explicitement la santé de son PKA (référence vidéo sur "morbid obesity" d'une second brain). Signal : besoin de **nettoyage / archivage / consolidation**.

### 2. **Expansion non-linéaire de scope**
En une session : WildNexus (tech) → Vetalyx (legal/fiscal) → Vanlife (fabrication) → Secondhand-selling (e-commerce). Aucune hiérarchie. Risque de **context-switching destructeur**.

### 3. **Décisions sans "Why documented"**
Ex. : "rester en 12V" — c'est juste, mais pourquoi ? (procurement, compatibilité RPI, autonomie ?) → À tracer une fois.

### 4. **Integration exploration (KIRO)**
Évaluation d'une interface IA externe (renaud-dekode/KIRO) pour "améliorer la routine de travail". Signe : frustration sur l'outillage actuel ou besoin de centralisation.

### 5. **Spatial reasoning + fabrication**
Vanlife : dimensions précises (104×55×25), glissières, trappe 180°. Pattern nouveau : JCH codifie ses besoins physiques en specs techniques → signal pour futur **CAD/BOM automation**.

---

## Efficacités / inefficacités

### ✅ Efficacités
- **Batch thinking** : Décision de traiter les skip en batch de 10 (+ simulations) = approche raisonnable d'optimisation
- **Questionnement préalable** : Poser des questions polies avant d'agir = friction intentionnelle, bon pattern
- **Multi-tool orchestration** : DeepSeek TUI + Claude Code + Codex CLI sont utilisés en parallèle sans friction apparente
- **Rapid ideation** : Passage Vetalyx → Vanlife → Secondhand en même session = mind ouverte, créative

### ❌ Inefficacités
- **No audit trail for decisions** : Aucune des décisions n'a de "decided on [date], rationale: [text], owner: [agent]"
- **Bug accumulation** : Au moins 6 bloqueurs non fermés depuis plusieurs sessions (API 1007, HA cap, tmutil, 403, needs_review, Dante)
- **Recurring Q&A** : Même question posée 2–3× = perte de ~30 min cumulée par question non documentée
- **No project sequencing** : 4 projets actifs, aucun ordre de dépendance ou priorité explicite
- **Context pollution** : Fragments de texte cassés, URLs incomplètes, citations mal copiées dans le transcript → parsing difficulty
- **Dobby working solo** : "pourquoi Dobby travaille sans s'appuyer sur les experts ?" → signal que délégation n'est pas claire

---

## Ce qu'il faut garder en mémoire pour les prochaines sessions

### Architecture PKA
1. **Vous êtes en mode audit** de la seconde brain (voir vidéo) → priorité : santé/consolidation avant nouvelle expansion
2. **4 projets majeurs en parallèle** (WildNexus, Vetalyx, Vanlife, Secondhand) → NÉCESSITE une matrice priorité/dépendances
3. **Dobby est l'orchestrateur central** mais pas le gardien du contexte métier → besoins d'escalade vers experts à formaliser

### Dettes techniques / informations
- **API Error 1007** (DeepSeek realtime_input) : À diagnostiquer + fermer
- **HA van OFF + CAP down** : Config issue ou bug ? À tester en isolation
- **3 fiches needs_review + fiche Dante vide** : Pattern systémique ? Vérifier schéma de validation
- **ASIX AX88179B** : Appareil inconnu, à documenter (RPI peripheral ?)

### Terminologie interne à externaliser
- ISC (debt threshold metric) = ?
- Kit hardwire = ?
- needs_review (status) = ?
- Vetalyx fiscal year fix (Art. 23) + directors (Art. 33) = BLOCKER légal avant publication

### Workflow patterns à mémoriser
- **TTL 24h caching** : Comment ? HTML button trigger ? Event-driven ? À spécifier
- **Procedure registry** : JCH veut invoquer procédures par nom (ex: "run secondhand-listing"). Créer `PROCEDURES.md` avec index exécutable
- **Secondhand-selling loop** : Inbox → price scraping (Belgium geo) → draft listing → site recommendation → response tracking (incomplete, à finaliser)

### Machine/infra state
- **M1** : Alimentation à retirer/déplacer (pas urgent, sans rush)
- **RPI** : Actif mais statut détaillé flou (M5, M4 aussi mentionnés ?)
- **Lupo Bianco** : Meuble banquette 104×55×25 avec 3 tiroirs + trappe → prêt pour CAD/prototype

---

## Recommandations

### 🔴 Urgent (< 7 jours)
1. **Créer `PROJECTS_MATRIX.md`**
   - Lister 4 projets : nom, owner, deadline, dépendances, priority (1-4)
   - Décider : lequel d'abord ? WildNexus ? Vetalyx (legal blocker) ?
   
2. **Fermer les 6 bloqueurs**
   - Assigner chacun : "Dobby to diagnose" / "DeepSeek API" / "HA config" / "Verify Dante schema"
   - Target: 3 days, update BLOCKERS.md après chaque diagnostic

3. **Créer `TERMINOLOGY.md`** (glossaire interne)
   - ISC, hardwire, needs_review, directors, TTL usage, etc.
   - Empêcher prochaines "c'est quoi [X] ?" recurses

### 🟠 Important (< 30 jours)
4. **Formaliser escalade Dobby → Experts**
   - Document: "Quand appeler qui ?" (fiscal → JCH, tech → ?, vanlife → ?)
   - Répondre à "pourquoi Dobby ne s'appuie pas sur les experts" → intentionnel ou oubli ?

5. **Créer `PROCEDURES.md`** (index exécutable)
   - Template : `[procedure-name]` → description → invocation (CLI / function / manual)
   - Exemple : "secondhand-listing" → steps 1-6 avec API calls / parsing / draft

6. **Évaluer KIRO integration**
   - Essai sur use-case light (ex: secondhand metadata extraction)
   - Décider : remplace quoi ? Complète ? Archive actuelle ?

7. **Documenter Vanlife specs**
   - Meuble 104×55×25, 3 

## 📊 Métriques d'efficacité

### Taux de résolution (7 jours glissants)
- Patterns détectés : 30
- Résolus automatiquement : 2
- Résolus manuellement : 0
- Encore ouverts : 28
- **Taux : 6.7%**

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

- [Decision] | Optimisation du traitement de données | Initiée |
- [Decision] (avec escalade conditionnelle) | Architecture de système, avec révision si nécessaire | À valider |
- [Decision] | WildNexus ou projet similaire | En attente de résultats |
- [Decision] | Vanlife (Lupo Bianco) — meuble 104×55×25cm, 3 tiroirs | Design en cours |
- [Decision] (Vetalyx) | Gestion documentaire | En cours |
- [Decision] | Collecte d'info préalable | Pattern établi |
- [Decision] (travels) | Planification vanlife | Initiée |
- [Decision] | Cycle de déploiement standard | À planifier |
- [Decision] | Infrastructure physique | Prévue (sans rush) |
- [Decision] | Vanlife — simplification procurement | Décision architecturale |
- [Failure] API Error 1007** : `realtime_input.m` — frame payload data invalide (DeepSeek)
- [Failure] HA van niveau OFF** : CAP ne fonctionne pas + "API key required" en cascade
- [Failure] tmutil backup échoué** : Encrypted APFS Volume sur disk8s2 — nécessite unlock avant mount
- [Failure] Erreur 403** : Access blocked (origine non identifiée dans transcript)

### Fréquence des patterns (14 jours)
- **Decision** : 6 jours, 33 occurrences
- **Failure** : 5 jours, 18 occurrences
- **Recurring question** : 5 jours, 19 occurrences
- **Question** : 4 jours, 24 occurrences

### Bilan apprentissage
- Nouveaux patterns appris aujourd'hui : 14
- Jours d'observation : 8
- L'extraction locale reste fixe ; le LLM découvre ce que les regex ne voient pas.


## ✅ État des recommandations

**538** recommandations au total — **538** ouvertes — **0** en cours — **0** terminées

⚠️ 519 recommandations ouvertes depuis plus de 7 jours.

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
