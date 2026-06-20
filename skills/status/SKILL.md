---
name: status
description: Tableau de bord des livrables en attente par membre PKA — vue d'ensemble de l'équipe. Version PKA améliorée (shadow du skill fondation) avec détection des tâches bloquées.
---

# /status — Tableau de bord équipe

Affiche l'état des tâches en attente dans `team.db` par membre.

> **Version PKA** — détection automatique des tâches bloquées (>7 jours).

## Usage

```
/status           # vue complète de tous les membres
/status Forge     # vue d'un membre spécifique
/status pending   # uniquement les tâches en attente
```

## Étapes d'exécution

### 1. Requêter team.db

```sql
-- Toutes les tâches en attente ou en cours
SELECT to_name, subject, status, created_at
FROM inbox
WHERE direction = 'JCH→TEAM'
  AND status IN ('pending', 'in_progress')
ORDER BY to_name, created_at;
```

Si un membre spécifique est précisé, ajouter `AND to_name = '<membre>'`.

### 2. Détecter les tâches bloquées

Pour chaque tâche `pending` :
- Si `created_at` > 7 jours → marquer `⚠️ bloqué`
- Afficher le nombre de jours depuis création

### 3. Afficher le tableau de bord

```
STATUS ÉQUIPE — YYYY-MM-DD HH:MM
════════════════════════════════

🦦 Forge         2 tâches
  · [pending]    Intégrer Pie dans pipeline digest
  · [in_progress] Page arteon.be/legal

🦊 Renard        1 tâche
  · [pending]    Vérifier CGU avant publication ⚠️ 12 jours

🦚 Vega          1 tâche
  · [pending]    Wireframes arteon.be

════════════════════════════════
Total : 4 tâches · 3 membres actifs · 1 bloquée
```

### 4. Extraire priority et deadline des briefs

Pour chaque tâche, scanner le `body` (texte du brief) pour extraire :
- `PRIORITY : high` / `medium` / `low` → afficher avec code couleur implicite
- `DEADLINE : YYYY-MM-DD` → si dépassée, marquer `⏰ deadline dépassée`

### 5. Signaler les blocages

Si des tâches bloquées existent → les lister en fin de rapport avec suggestion d'action :
```
⚠️ TÂCHES BLOQUÉES (>7 jours)
  · Renard — "Vérifier CGU avant publication" (12 jours) → relancer ou réévaluer priorité
```

## Règles

- Lecture seule — ne jamais modifier team.db pendant /status
- Si aucune tâche en attente → afficher "Équipe à jour ✓"
- Une tâche `pending` depuis >7 jours = bloquée → toujours le signaler

## Skills liés

- **`brief`** — Pour créer les tâches qui apparaissent dans ce tableau de bord. Les champs PRIORITY et DEADLINE des briefs sont lus par `status`.
