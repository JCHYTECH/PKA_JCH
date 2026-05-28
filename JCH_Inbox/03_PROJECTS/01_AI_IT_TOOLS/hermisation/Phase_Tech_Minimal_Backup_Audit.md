# Phase Technique Minimale — Étape 2 Backup TEAM DB

Date : 2026-05-28
Statut : validé

## 1. Objectif

Stabiliser la sauvegarde de `TEAM/team.db`, vérifier le log, confirmer les permissions et documenter une procédure de restauration.

Mandat limité :

- pas de modification Obsidian ;
- pas de nouvelle infrastructure ;
- pas de suppression de backups ;
- pas de restauration réelle sans validation humaine.

## 2. État backup

| Élément | Résultat |
|---|---|
| Base active | `TEAM/team.db` |
| Taille base active | `1732608` octets |
| Permissions base active | `0600` |
| Dossier backups | `TEAM/backups/` |
| Permissions dossier backups | `0755` |
| Log cron | `TEAM/backups/backup.log` |
| Permissions log | `0600` |
| Dernier backup testé | `TEAM/backups/team_2026-05-28_2157.db` |
| Permissions backup testé | `0600` |
| Intégrité base active | `ok` |
| Intégrité backup testé | `ok` |

## 3. Planification

Le backup quotidien est actif dans le crontab :

```cron
0 8 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/jchavauxm5/PKA_JCH/scripts/backup_team_db.py >> /Users/jchavauxm5/PKA_JCH/TEAM/backups/backup.log 2>&1
```

`email_digest.py` n'est pas présent dans le crontab.

## 4. Durcissement appliqué

Fichier modifié :

- `scripts/backup_team_db.py`

Changements :

- vérification explicite de l'existence de `TEAM/team.db`;
- création du dossier `TEAM/backups`;
- application de permissions contrôlées ;
- backup via SQLite Online Backup API ;
- `chmod 600` sur le backup produit ;
- `PRAGMA integrity_check` sur le backup produit ;
- suppression du fichier produit si l'intégrité échoue ;
- sortie log enrichie avec taille, mode et nombre de fichiers purgés.

## 5. Test de restauration à blanc

La restauration a été répétée sans toucher à `TEAM/team.db`.

Fichier test :

```text
tmp/restore_rehearsal/team_restored_test.db
```

Résultat :

- copie du backup OK ;
- permissions `0600` ;
- `PRAGMA integrity_check` retourne `ok` ;
- tables SQLite lisibles.
- copie temporaire supprimée après validation.

## 6. Procédure

Procédure opérationnelle :

- [[TEAM/RESTORE_TEAM_DB]]

Règle :

Une restauration réelle exige validation humaine explicite, arrêt ou suspension des writers, copie de sécurité `team_before_restore_*`, puis audit sécurité.

## 7. Risques résiduels

| Risque | Gravité | Décision |
|---|---|---|
| Backups seulement locaux | Moyenne | À traiter dans une étape sauvegarde hors machine. |
| Restauration automatisée dangereuse | Élevée | Interdite sans validation humaine. |
| Writers concurrents pendant restauration | Élevée | Arrêter ou suspendre Dobby/scripts avant restauration réelle. |

## 8. Verdict

L'étape 2 est validée.

Étape suivante exécutée :

- [[RUNBOOK_PKA_MACBOOK]]

Prochaine étape recommandée :

> Préparer le commit propre Phase 1 + phase technique minimale.
