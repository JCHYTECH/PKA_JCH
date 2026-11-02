# Restauration TEAM/team.db

Date : 2026-05-28
Statut : procédure validée par test à blanc

## Objectif

Restaurer `TEAM/team.db` depuis une sauvegarde `TEAM/backups/team_*.db` sans perte accidentelle.

Cette procédure est manuelle par défaut. Elle ne doit pas être automatisée sans validation humaine.

## Sauvegarde actuelle

Le backup est planifié par cron :

```cron
0 8 * * * /Library/Frameworks/Python.framework/Versions/3.13/bin/python3 /Users/jchavauxm5/PKA_JCH/scripts/backup_team_db.py >> /Users/jchavauxm5/PKA_JCH/TEAM/backups/backup.log 2>&1
```

Le script :

- crée un snapshot [[SQLite]] cohérent via l'API [[SQLite]] Online Backup ;
- écrit dans `TEAM/backups/team_YYYY-MM-DD_HHMM.db` ;
- applique `chmod 600` au fichier généré ;
- vérifie `PRAGMA integrity_check`;
- conserve environ 30 jours de backups selon l'âge fichier.

## Vérifier les backups

Lister les derniers backups :

```sh
ls -lt TEAM/backups/team_*.db | head
```

Vérifier les permissions :

```sh
stat -f '%Lp %N' TEAM/team.db TEAM/backups/team_*.db
```

Vérifier l'intégrité d'un backup :

```sh
sqlite3 TEAM/backups/team_YYYY-MM-DD_HHMM.db 'PRAGMA integrity_check;'
```

Le résultat attendu est :

```text
ok
```

## Test de restauration sans risque

Cette étape restaure dans `tmp/restore_rehearsal/` uniquement.

```sh
mkdir -p tmp/restore_rehearsal
cp TEAM/backups/team_YYYY-MM-DD_HHMM.db tmp/restore_rehearsal/team_restored_test.db
chmod 600 tmp/restore_rehearsal/team_restored_test.db
sqlite3 tmp/restore_rehearsal/team_restored_test.db 'PRAGMA integrity_check;'
sqlite3 tmp/restore_rehearsal/team_restored_test.db '.tables'
```

Ne pas passer à la restauration réelle si l'intégrité n'est pas `ok`.

## Restauration réelle

Préconditions :

- [[Dobby]] et les scripts pouvant écrire dans `TEAM/team.db` sont arrêtés ou suspendus.
- Un backup récent a été vérifié avec `PRAGMA integrity_check`.
- JCH valide explicitement l'écrasement de `TEAM/team.db`.

Procédure :

```sh
cd /Users/jchavauxm5/PKA_JCH
cp TEAM/team.db TEAM/backups/team_before_restore_$(date +%Y-%m-%d_%H%M).db
chmod 600 TEAM/backups/team_before_restore_*.db
cp TEAM/backups/team_YYYY-MM-DD_HHMM.db TEAM/team.db
chmod 600 TEAM/team.db
sqlite3 TEAM/team.db 'PRAGMA integrity_check;'
```

Après restauration :

```sh
python3 scripts/pka_security_audit.py
```

## Test validé le 2026-05-28

Backup testé :

```text
TEAM/backups/team_2026-05-28_2157.db
```

Résultats :

- backup créé avec taille `1732608` octets ;
- mode `0600`;
- intégrité backup : `ok`;
- copie de restauration à blanc : `tmp/restore_rehearsal/team_restored_test.db`;
- intégrité copie restaurée : `ok`;
- tables [[SQLite]] visibles.
- copie temporaire supprimée après validation pour éviter une base sensible en double.

## Limites

- Cette procédure protège `TEAM/team.db`, pas l'ensemble du vault Markdown.
- Les backups sont locaux. Une stratégie hors machine reste à formaliser séparément.
- Le dossier `tmp/restore_rehearsal/` est une zone de test, pas une sauvegarde officielle. Les copies de test doivent être supprimées après validation.
