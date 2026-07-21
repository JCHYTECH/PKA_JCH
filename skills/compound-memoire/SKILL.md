# Skill — compound-memoire

## Déclencheur
- « compound mémoire », « erreur → règle », « apprends de cette erreur »
- Automatique après chaque correction de JC à Dobby
- Automatique après chaque échec de loop (score < seuil)

---

## Concept

Inspiré du pattern Cherny (Claude Code) : *"Every single time Claude makes a mistake, I tell it to write it to CLAUDE.md, or make a skill. If you can do this, then Claude can just run forever."*

Transposé à PKA : **chaque correction de JC → règle durable dans SOUL.md ou un skill.**

---

## Workflow (3 étapes)

### 1. DÉTECTION — Quand capturer ?

| Trigger | Délai | Exemple |
|---------|-------|---------|
| JC corrige Dobby explicitement | Immédiat | « Non Dobby, tu aurais dû vérifier X avant » |
| Une loop échoue (score < seuil) | Après 2 échecs consécutifs | forge-loop → score 3/5 deux fois de suite |
| Dobby se corrige lui-même | Immédiat | « Je me suis trompé, la bonne réponse est Y » |
| Incohérence State vs MEMORY | Immédiat | State file contredit MEMORY.md |

### 2. EXTRACTION — Quelle règle ?

Pour chaque erreur, Dobby :
1. Identifie la **cause racine** (pas le symptôme)
2. Formule une **règle actionable** (format SOUL.md : « Dobby doit toujours… »)
3. Détermine la **cible** : SOUL.md (règle comportementale) ou skill (règle procédurale)
4. Calcule la **confiance** : erreur unique (0.3) → pattern récurrent (0.7) → pattern confirmé par JC (0.9)

### 3. APPLICATION — Où écrire ?

| Cible | Quand | Format |
|-------|-------|--------|
| `SOUL.md` — section « Règles de comportement » | Règle transversale, tous modèles | `### Règle X — [titre]` + description + justification |
| `MEMORY.md` — section « Patterns récurrents » | Pattern observé ≥ 3 occurrences | `- [Pattern] [date] : description` |
| Skill existant — mise à jour | Règle procédurale spécifique | Ajout dans la section appropriée du SKILL.md |
| `USER.md` — section « À retenir » | Préférence JC confirmée | Ajout dans la liste « À retenir » |

---

## Seuil de confiance

| Confiance | Action |
|-----------|--------|
| < 0.5 | Logger dans `MEMORY.md` (section Patterns), ne pas proposer |
| 0.5 – 0.79 | Logger + proposer à JC si pattern récurrent (≥ 3 occurrences) |
| ≥ 0.8 | Proposer immédiatement à JC : « JC, j'ai détecté ce pattern. Veux-tu que j'ajoute cette règle à SOUL.md ? » |

---

## Implémentation

### Script `bin/pka-compound`

```bash
bin/pka-compound --extract     # Analyse les dernières corrections JC → propose règles
bin/pka-compound --apply <id>  # Applique une règle proposée
bin/pka-compound --list        # Liste les règles en attente
bin/pka-compound --help
```

Lit les sessions récentes depuis `TEAM_Inbox/` et `MEMORY.md`, détecte les patterns de correction, et propose des règles.

### Intégration avec les loops

Après chaque échec de loop (score < seuil) :
1. La loop log l'échec avec la cause
2. `pka-compound --extract` analyse l'échec
3. Si pattern détecté → proposition de règle

---

## Exemple concret

**Erreur :** Dobby oublie de vérifier `hardware-state.md` avant d'affirmer un statut matériel.

**Détection :** JC corrige 3 fois en 2 semaines.

**Règle proposée (SOUL.md) :**
```
### Règle 7 — Vérifier hardware-state.md avant toute affirmation matérielle
Avant d'affirmer qu'un composant est reçu, commandé, ou en attente, Dobby doit TOUJOURS
lire `hardware-state.md` (State, pas MEMORY.md). Si contradictoire → privilégier State.
```

**Cible :** SOUL.md (règle comportementale transversale)

**Confiance :** 0.85 (3 occurrences, JC a explicitement corrigé)

---

## Voir aussi
- [[TEAM_Inbox/2026-07-17_dobby_analyse-loop-engineering-completive]]
- [[Boris Cherny]] — compound mémoire Claude Code
- [[SOUL.md]] — cible des règles comportementales
