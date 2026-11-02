---
name: pka-weekly-report
description: Rapport hebdomadaire consolidé PKA — résumé équipe, projets, inbox, rétrospective. Déclencher sur "rapport hebdo", "weekly report", "bilan de la semaine".
---

# Skill — pka-weekly-report

## Déclencheurs
- "rapport hebdo"
- "weekly report"
- "bilan de la semaine"
- "résumé hebdomadaire"
- Automatique le dimanche (via cron `dobby_weekly_report.py`)

## Contexte système
- Script canonique : `/Users/jchavauxm5/PKA_JCH/scripts/dobby_weekly_report.py`
- Rétro complémentaire : `/Users/jchavauxm5/PKA_JCH/scripts/dobby_retro.py`
- Rapports stockés dans : `TEAM_Inbox/`

## Procédure

### 1. Collecter l'état
- Exécuter `dobby_weekly_report.py` pour le rapport consolidé
- Scanner `TEAM_Inbox/` pour les livrables de la semaine
- Vérifier `team.db` pour les tâches créées/complétées cette semaine

### 2. Structure du rapport

```
RAPPORT HEBDOMADAIRE PKA — Semaine XX (YYYY-MM-DD → YYYY-MM-DD)
═══════════════════════════════════════════════════════

ÉQUIPE
- Actifs : N membres
- Tâches créées : N
- Tâches complétées : N
- En attente : N

PROJETS
| Projet | Activité | Statut |
|--------|----------|--------|
| WILDNEXUS | N livrables | En cours |
| ... | ... | ... |

INBOX
- Fichiers traités : N
- En attente : N

RÉTROSPECTIVE
- Patterns détectés (via dobby_retro.py)
- Leçons de la semaine

PROCHAINE SEMAINE
- Priorités
- Deadlines
```

### 3. Sauvegarder
- Fichier : `TEAM_Inbox/YYYY-MM-DD_weekly-report_dobby.md`
- Ne pas écraser un rapport existant

## Règles
- Synthétique — 1 page max, pas de narration
- Toujours inclure la section "Prochaine semaine"
- Si `dobby_weekly_report.py` échoue → rapport manuel minimal
- Le rapport est un résumé, pas un journal — pointer vers les fichiers détaillés
