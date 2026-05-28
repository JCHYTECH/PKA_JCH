# Inbox Deliverables — Rapport Post-Migration

Date : 2026-05-28
Statut : migration appliquée, vérifiée et triage partiel effectué

## 1. Résumé

La migration `inbox` demandée par `PROMPT_DOBBY_INBOX.md` a été appliquée à `TEAM/team.db`.

Objectif atteint :

- ajout du suivi livrable ;
- prise en charge des statuts `delivered`, `validated`, `rejected` ;
- conservation des 235 entrées existantes ;
- aucune conversion automatique des anciens statuts ;
- aucune modification dashboard dans cette étape.
- triage WildNexus appliqué sur les entrées `232-234`.

## 2. Sauvegarde

Backup automatique créé juste avant migration :

```text
TEAM/backups/team_2026-05-28_2335.db
```

Permissions :

```text
0600
```

## 3. Schéma après migration

Colonnes ajoutées :

| Colonne | Rôle |
|---|---|
| `deliverable_path` | Chemin du livrable produit dans `TEAM_Inbox/` ou autre dossier validé |
| `delivered_at` | Date/heure de livraison au statut `delivered` |
| `validated_at` | Date/heure de validation ou rejet JCH |
| `validated_by` | Validateur, défaut `JCH` |
| `rejection_reason` | Motif obligatoire en pratique si statut `rejected` |

Statuts autorisés après migration :

```text
pending, in_progress, done, delivered, validated, rejected, cancelled
```

Note :

- `done` est conservé pour compatibilité historique.
- Les nouveaux workflows doivent utiliser `delivered` puis `validated` ou `rejected`.

## 4. Vérifications

| Vérification | Résultat |
|---|---|
| Backup pré-application | `TEAM/backups/team_2026-05-28_2335.db` |
| Lignes avant/après | `235` conservées |
| Compteurs statuts | inchangés |
| Intégrité SQLite | `ok` |
| Permissions `TEAM/team.db` | `0600` |
| Test temporaire `TEAM→JCH` + `delivered` | OK, supprimé dans la même transaction |

Répartition post-migration :

| Statut | Nombre |
|---|---:|
| `cancelled` | 224 |
| `delivered` | 2 |
| `done` | 2 |
| `pending` | 6 |
| `validated` | 1 |

## 5. Pending à traiter

| ID | Spécialiste | Sujet | Statut | Créé | Fichier |
|---:|---|---|---|---|---|
| 20 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 12:59:28 |  |
| 83 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:00:50 |  |
| 128 | Renard | `[EMAIL] Re: contrat type` | `pending` | 2026-05-01 13:02:58 |  |
| 147 | Vasco | `[EMAIL] Commandé : « Moi, ce que j'aime, c'est... » et 1 articles supplémentaires` | `pending` | 2026-05-01 13:03:05 |  |
| 214 | Vasco | `[EMAIL] These are not quizzes. They are diagnostic tools.` | `pending` | 2026-05-02 18:00:14 |  |
| 228 | Renard | `[EMAIL] Jean-Claude, tatouage Thaïlandais, Tatouage Japonaise et plus d'idées à explorer` | `pending` | 2026-05-09 07:00:19 |  |
| 232 | Chouette | `WildNexus — déterminer longueur d'onde LED IR non visible/non perturbante faune` | `validated` | 2026-05-18 18:52:08 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/ADR-002-choix-camera-ir-p0.md` |
| 233 | Forge | `WildNexus — revue Meshnology N35 ESP32 LoRa V3/V4` | `delivered` | 2026-05-18 19:53:20 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/2026-05-18_product-review-meshnology-n35.md` |
| 234 | Milan | `WildNexus — scan fabricants produit intégré P0` | `delivered` | 2026-05-18 19:57:03 | `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/2026-05-18_market-scan-integrated-p0-products.md` |

## 6. Règle opérationnelle Dobby

À partir de cette migration :

1. À l'envoi d'un mandat spécialiste : créer ou maintenir une entrée `inbox` direction `JCH→TEAM`, statut `in_progress`.
2. À la livraison : passer l'entrée en `delivered`, renseigner `deliverable_path` et `delivered_at`.
3. À la validation JCH : passer en `validated`, renseigner `validated_at`, `validated_by`.
4. En cas de rejet : passer en `rejected`, renseigner `validated_at`, `validated_by`, `rejection_reason`.

## 7. Décisions restantes

À valider avant nettoyage des anciens `pending` :

| Sujet | Décision attendue |
|---|---|
| 6 vieux pending email sans fichier | Maintenir, annuler, ou rechercher livrable correspondant |
| 3 pending WildNexus avec fichier | Déjà triés : `232` validé, `233-234` livrés |
| Dashboard | Mettre à jour seulement après validation JCH |

## 8. Prochaine étape

Commit séparé recommandé avec :

- `TEAM/team.db`;
- `scripts/migrate_inbox_deliverables.py`;
- `Inbox_Deliverables_PreMigration_Audit.md`;
- `Inbox_Deliverables_PostMigration_Report.md`.

Ne pas inclure les backups SQLite.
