# Protocole Arbor Loop — pas à pas

> Ce fichier est le **mode d'emploi exécutable** de la skill `arbor-research`.
> Dobby le suit séquentiellement à chaque cycle de recherche.

---

## Phase 0 — Initialisation

### 0.1 Charger le contexte

- [ ] Lire l'arbre existant : `.arbor/research/<project>/tree.json`
- [ ] Si pas d'arbre : créer avec `idea-tree-template.md`
- [ ] Identifier le trunk actuel (nœud `merged` le plus profond, ou ROOT)
- [ ] Lire les insights de tous les nœuds `done`, `merged`, `pruned`

### 0.2 Vérifier la convergence

Avant de lancer un nouveau cycle, vérifier :

- [ ] **Convergence dure** : les `N` derniers cycles ont-ils tous donné Δscore < seuil ?
- [ ] **Budget** : nombre de cycles exécutés < max_cycles ?
- [ ] **Convergence sémantique** : les 3 dernières hypothèses sont-elles des variantes mineures d'hypothèses déjà testées ?

Si convergence détectée → **arrêter et rapporter**. Ne pas forcer un cycle supplémentaire.

### 0.3 Déterminer le type de cycle

- **Cycle 1** (pas d'hypothèses pending) → OBSERVE + IDEATE + DECIDE + EXECUTE
- **Cycle N** (résultat reçu) → OBSERVE + DECIDE (merge/prune) + si trunk changé → IDEATE + DECIDE + EXECUTE
- **Reprise** (nœud `needs_retry`) → EXECUTE uniquement (relancer le même nœud)

---

## Phase 1 — OBSERVE

### 1.1 Collecter les données

- [ ] Lire le résultat brut du dernier EXECUTE (sortie du spécialiste)
- [ ] Lire les logs/métriques pertinents
- [ ] Comparer au score baseline (trunk actuel)

### 1.2 Analyse des échecs (si applicable)

Si le dernier résultat est un échec ou une non-amélioration :

- [ ] Lister **au moins 3 cas d'échec concrets** avec IDs, logs, ou références
- [ ] Pour chaque cas, identifier **pourquoi** le système actuel échoue
- [ ] **NE PAS** proposer de solution à ce stade

### 1.3 First-Principles Probe (obligatoire)

Répondre aux 4 questions dans le reasoning trace de Dobby. Chaque réponse doit citer des preuves concrètes.

**Q1. Bottleneck CLASS — quelle est la classe de bottleneck dominante ?**

Raisonner depuis l'essence mathématique/algorithmique de la tâche. Classifier :
- Mauvaise représentation
- Mauvais raisonnement
- Mauvaise condition d'arrêt
- Mauvaise métrique
- Mauvais espace d'action
- Mauvaise attribution de crédit

Citer ≥2 cas concrets comme preuve.

**Q2. Hidden Assumption — sur quoi le trunk s'appuie-t-il silencieusement ?**

Nommer une hypothèse porteuse qui, si elle était levée, débloquerait de nouvelles stratégies.

Exemples par domaine :
- Hardware : « le régulateur doit être intégré au PCB principal »
- ML : « le modèle doit tourner en continu »
- SEO : « le contenu doit cibler un mot-clé principal par page »

**Q3. Analogy — quel problème formellement similaire a déjà été résolu ailleurs ?**

Nommer un domaine ou une approche qui attaque une structure de problème similaire, même si le domaine est différent.

Exemples :
- « La planification de trajectoire en robotique → ordonnancement des événements caméra »
- « La compression de modèle NLP → compression de modèle TinyML »
- « Le A/B testing web → expérimentation hardware »

**Q4. Why the gap persists — pourquoi une solution évidente n'a-t-elle pas déjà été trouvée ?**

Est-ce :
- Une connaissance manquante (le champ ignore une méthode d'un autre domaine) ?
- Une contrainte non remise en question (on a toujours fait comme ça) ?
- Une difficulté technique réelle (le problème est fondamentalement dur) ?

### 1.4 Synthèse OBSERVE

Produire un bloc synthèse :
```
BOTTLENECK : [classe] — [résumé 1 phrase]
HIDDEN ASSUMPTION : [hypothèse porteuse à challenger]
ANALOGY SOURCE : [domaine analogue]
GAP REASON : [pourquoi pas déjà résolu]
```

---

## Phase 2 — IDEATE

### 2.1 Génération d'hypothèses

Pour chaque hypothèse candidate, remplir les 5 champs :

**1. Assumption challenged** — quelle hypothèse de Q2 cette idée attaque-t-elle ?
Si « aucune — elle ajoute juste quelque chose par-dessus » → ❌ (engineering, pas recherche)

**2. Mechanism class** — choisir parmi :
- `algorithm/method`
- `data-representation`
- `search/retrieval`
- `planning/control`
- `verification/feedback`
- `training/data`
- `orchestration`
- `hardware/component` (extension PKA)
- `firmware/configuration` (extension PKA)

**3. Mechanism + Hypothesis chain** — format canonique :
> Nous pensons que **[MÉCANISME]** aide parce que **[CAUSALITÉ]**,
> et nous saurons que ça marche si **[OBSERVABLE]**.

**4. Orthogonality vs siblings** — pour chaque sibling existant, nommer l'axe de différence.
« À peu près différent » → ❌

**5. Conflicts with prior insight** — lister tout insight élagué que cette hypothèse semble contredire.
Si conflit : expliquer en 1 phrase le contre-argument. Si aucun : « none — nouvel axe ».

### 2.2 Filtre anti-pseudo-idées

Pour chaque candidat, vérifier :

- [ ] Le changement peut-il s'exprimer comme un seul paramètre ? → ❌ kill
- [ ] Est-ce « plus de X » (retries, contexte, modèle plus gros) ? → ❌ kill
- [ ] L'hypothèse décrit-elle un objectif au lieu d'un mécanisme ? → ❌ rewrite
- [ ] Recouvre-t-elle un nœud déjà `pruned` sans contre-argument ? → ❌ kill
- [ ] Peut-on pointer vers la question du Probe Block qui l'a motivée ? → si non ❌ kill

### 2.3 Priorisation

Classer les hypothèses survivantes par :
1. Upside potentiel (haute priorité)
2. Coût estimé (basse priorité si élevé)
3. Diversité d'axe vs nœuds existants (haute priorité si orthogonal)

**Règle :** 1 hypothèse sharp > 5 variantes faibles. Si aucune ne survit au filtre, retourner à OBSERVE.

---

## Phase 3 — DECIDE

### 3.1 Sélection

- [ ] Choisir la meilleure hypothèse selon la priorisation 2.3
- [ ] Si plusieurs sont équivalentes, choisir la plus orthogonale aux nœuds existants
- [ ] Vérifier qu'elle ne répète pas un nœud `pruned` sans contre-argument explicite

### 3.2 Préparer le contrat d'évaluation

Définir avant d'exécuter :

```
HYPOTHÈSE   : [texte canonique]
EXECUTOR    : [spécialiste PKA]
MÉTRIQUE    : [quoi mesurer, comment]
BUDGET      : [max cycles, max temps]
SEUIL MERGE : [Δ minimum pour considérer un succès, ex: +5%]
PROTECTIONS : [fichiers/données à ne pas modifier]
```

### 3.3 Créer le nœud

- [ ] Ajouter le nœud à l'arbre avec `status: pending`
- [ ] Sauvegarder `tree.json` et `TREE.md`

---

## Phase 4 — EXECUTE

### 4.1 Déléguer

- [ ] Formuler le brief au spécialiste : hypothèse + contrat d'évaluation + budget
- [ ] Le brief doit contenir le **mécanisme à tester**, pas juste l'objectif
- [ ] Le spécialiste doit savoir exactement quoi mesurer et quel seuil viser

### 4.2 Monitorer (optionnel)

Si le run est long :
- [ ] Passer le nœud en `status: running`
- [ ] Checkpoint intermédiaire si supporté

### 4.3 Recevoir le résultat

- [ ] Le spécialiste rapporte : score brut, logs, artefacts, statut d'évaluation
- [ ] Dobby **ne retouche pas** le résultat — il l'interprète

---

## Phase 5 — INTEGRATE (retour à OBSERVE)

### 5.1 Classifier le résultat

| Issue | eval_status | Action |
|---|---|---|
| Test exécuté, score mesuré | `scored` | → DECIDE merge/prune |
| Test non exécutable (bug, setup) | `failed_to_run` | → `needs_retry` ou `pruned` |
| Test sauté (hypothèse invalide) | `skipped` | → `pruned` avec raison |

### 5.2 Merge ou Prune ?

**MERGE si :**
- Score > trunk ET Δ > seuil_merge
- L'amélioration est confirmée (pas de fluctuation)
- L'insight est généralisable

**PRUNE si :**
- Score ≤ trunk
- L'hypothèse est invalidée par les données
- Le coût du test était prohibitif pour le résultat

**NEEDS_RETRY si :**
- Échec technique (pas conceptuel)
- Bug corrigeable
- Setup incorrect

### 5.3 Enregistrer l'insight

Quel que soit le résultat, enregistrer un insight :
- Ce qui a été appris
- Pourquoi ça a marché/échoué
- Ce que les prochains nœuds devraient savoir

### 5.4 Propager

- [ ] Remonter l'insight au parent
- [ ] Marquer les siblings incompatibles comme `pruned`
- [ ] Mettre à jour `tree.json` et `TREE.md`
- [ ] Retourner en Phase 0

---

## Commandes utiles

```bash
# Créer un nouvel arbre
mkdir -p .arbor/research/<project>/sessions

# Visualiser l'arbre
cat .arbor/research/<project>/TREE.md

# Lister les nœuds pending
grep -A2 '"status": "pending"' .arbor/research/<project>/tree.json

# Compter les cycles
grep -c '"status": "done"' .arbor/research/<project>/tree.json
```

---

## Anti-patterns à éviter

| Anti-pattern | Pourquoi c'est dangereux | Correction |
|---|---|---|
| **Sauter OBSERVE** | Propose des solutions à un problème mal compris | Forcer la First-Principles Probe avant toute hypothèse |
| **Tweaks déguisés en hypothèses** | « Essayons avec un timeout plus long » n'est pas une hypothèse | Exiger un mécanisme nommé |
| **Merge sans contre-test** | Accepter un résultat sans vérifier qu'il n'est pas un artefact | Exiger confirmation sur données held-out |
| **Ignorer les nœuds pruned** | Retester la même idée sans contre-argument | Vérifier l'historique des pruned avant chaque IDEATE |
| **Dobby fait l'Executor** | Dobby n'a pas les outils/spécialisation pour exécuter | Toujours déléguer au spécialiste |
| **Trop d'hypothèses par cycle** | Dilue le budget, ralentit la convergence | Max 3 hypothèses par cycle IDEATE, 1 exécutée |
