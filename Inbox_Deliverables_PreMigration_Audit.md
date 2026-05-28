# Inbox Deliverables — Audit Pré-Migration

Date : 2026-05-28
Statut : lecture seule, aucune migration appliquée

## 1. Objectif

Auditer la table `inbox` de `TEAM/team.db` avant d'appliquer le mandat `PROMPT_DOBBY_INBOX.md`.

Mandat de prudence :

- backup avant observation ;
- aucune modification de schéma ;
- aucun `ALTER TABLE` ;
- aucun changement dashboard ;
- aucune modification des 235 entrées existantes.

## 2. Backup et intégrité

Backup créé avant audit :

```text
TEAM/backups/team_2026-05-28_2329.db
```

Résultat :

- taille : `1736704` octets ;
- mode : `0600` ;
- `PRAGMA integrity_check` sur `TEAM/team.db` : `ok`.

## 3. Schéma actuel `inbox`

Colonnes actuelles :

| Colonne | Type | Contraintes |
|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT |
| `direction` | TEXT | NOT NULL, `CHECK(direction IN ('JCH→TEAM', 'TEAM→JCH'))` |
| `from_name` | TEXT | NOT NULL |
| `to_name` | TEXT | NOT NULL |
| `subject` | TEXT | NOT NULL |
| `body` | TEXT |  |
| `status` | TEXT | NOT NULL DEFAULT `pending`, `CHECK(status IN ('pending', 'in_progress', 'done', 'cancelled'))` |
| `created_at` | TEXT | NOT NULL DEFAULT `datetime('now')` |
| `closed_at` | TEXT |  |
| `file_path` | TEXT |  |

Index existant :

```text
idx_inbox_direction_status ON inbox(direction, status)
```

## 4. État des entrées

Total :

```text
235 entrées
```

Répartition par statut :

| Statut | Nombre | Plus ancien | Plus récent |
|---|---:|---|---|
| `cancelled` | 224 | 2026-05-01 12:59:04 | 2026-05-10 12:00:27 |
| `done` | 2 | 2026-05-18 18:02:03 | 2026-05-18 20:28:49 |
| `pending` | 9 | 2026-05-01 12:59:28 | 2026-05-18 19:57:03 |

Répartition direction/statut :

| Direction | Statut | Nombre |
|---|---|---:|
| `JCH→TEAM` | `cancelled` | 224 |
| `JCH→TEAM` | `done` | 2 |
| `JCH→TEAM` | `pending` | 9 |

Constat :

- aucune entrée `TEAM→JCH` pour l'instant ;
- la direction `TEAM→JCH` est déjà autorisée par le schéma ;
- il y a 9 `pending`, pas 6.

## 5. Pending actuels

| ID | Spécialiste | Sujet | Créé | Fichier |
|---:|---|---|---|---|
| 20 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 12:59:28 |  |
| 83 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:00:50 |  |
| 128 | Renard | `[EMAIL] Re: contrat type` | 2026-05-01 13:02:58 |  |
| 147 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | 2026-05-01 13:03:05 |  |
| 214 | Vasco | `[EMAIL] These are not quizzes. They are diagnostic tools.` | 2026-05-02 18:00:14 |  |
| 228 | Renard | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | 2026-05-09 07:00:19 |  |
| 232 | Chouette | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/ADR-002-choix-camera-ir-p0.md` |
| 233 | Forge | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/2026-05-18_product-review-meshnology-n35.md` |
| 234 | Milan | `WildNexus — scan fabricants produit intégré P0` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/2026-05-18_market-scan-integrated-p0-products.md` |

## 6. Compatibilité avec `PROMPT_DOBBY_INBOX.md`

Le mandat propose d'ajouter :

- `deliverable_path`;
- `delivered_at`;
- `validated_at`;
- `validated_by`;
- `rejection_reason`.

Ces colonnes n'existent pas actuellement et peuvent être ajoutées.

Mais le mandat demande aussi de nouveaux statuts :

- `delivered`;
- `validated`;
- `rejected`.

Le schéma actuel impose :

```sql
CHECK(status IN ('pending', 'in_progress', 'done', 'cancelled'))
```

Conclusion :

Un simple `ALTER TABLE ADD COLUMN` ne suffit pas. Pour autoriser les nouveaux statuts, SQLite nécessite une migration contrôlée par reconstruction de table :

1. `BEGIN IMMEDIATE`;
2. créer `inbox_new` avec le nouveau `CHECK`;
3. copier toutes les lignes existantes ;
4. recréer l'index ;
5. vérifier les compteurs ;
6. renommer ;
7. `PRAGMA integrity_check`;
8. `COMMIT`.

## 7. Décision recommandée avant migration

Ne pas appliquer encore la migration.

À valider avec JCH :

1. conserver le statut historique `done` ou le transformer en `delivered` ;
2. traiter les 9 `pending` anciens : maintenir, `cancelled`, ou convertir selon livrable existant ;
3. accepter une reconstruction SQLite de la table `inbox`, pas seulement des `ALTER TABLE`;
4. reporter le dashboard après migration et rapport post-migration.

## 8. Script préparé

Script créé :

```text
scripts/migrate_inbox_deliverables.py
```

Comportement :

- par défaut, dry-run sur une copie temporaire dans `tmp/inbox_migration/` ;
- aucune modification de `TEAM/team.db` sans option `--apply` ;
- avec `--apply`, création d'un backup frais avant migration ;
- reconstruction transactionnelle de `inbox` pour modifier le `CHECK(status...)` ;
- ajout des colonnes livrables ;
- conservation de `done` pour compatibilité historique ;
- vérification compteurs et `PRAGMA integrity_check`.

Dry-run validé le 2026-05-28 :

```text
Dry-run database copy: tmp/inbox_migration/team_inbox_migration_dry_run_2026-05-28_233330.db
Rows preserved: 235
Status counts preserved: {'cancelled': 224, 'done': 2, 'pending': 9}
New columns present: ['deliverable_path', 'delivered_at', 'validated_at', 'validated_by', 'rejection_reason']
Integrity: ok
Dry-run complete; source TEAM/team.db unchanged
```

Vérification source :

- `TEAM/team.db` ne contient pas encore les nouvelles colonnes ;
- migration non appliquée.
- copie temporaire dry-run supprimée après validation.

## 9. Prochaine étape

Relire le script, valider explicitement avec JCH, puis exécuter :

```sh
python3 scripts/migrate_inbox_deliverables.py --apply
```

Après application :

1. vérifier intégrité ;
2. produire le rapport post-migration des `pending` ;
3. committer séparément ;
4. reporter le dashboard à une validation ultérieure.
