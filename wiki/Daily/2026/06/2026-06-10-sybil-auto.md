```yaml
---
date: 2026-06-10
archiviste: Sybil
type: journal_automatique
---
```

# Journal — 10 juin 2026

## Graphify : cycle de production complet

La journée s'est structurée autour d'une exécution complète du pipeline Graphify. L'ensemble du répertoire `graphify-out/` a été régénéré :

- **Extraction sémantique** : trois batches traités (`semantic_batch1.json`, `semantic_batch2.json`, `semantic_batch3.json`) et consolidation dans `semantic_extraction.json`
- **Construction du graphe** : génération de `graph.json` avec sauvegarde préalable (`graph.json.bak`, `graph.json.pre-fullrun`)
- **Logs de production** : captures multiples du flux d'exécution (`fullrun.log`, `fullrun_stdout.log`, `fullrun_nohup.log`, `batch_progress.log`, `batch_progress_stdout.log`)
- **Métadonnées** : mise à jour du manifest, des labels internes (`.graphify_labels.json`) et de la racine (`graphify_root`)
- **Rapport généré** : `GRAPH_REPORT.md` produit en fin de cycle

## Synchronisation Dropbox et suivi

La surveillance des changements Dropbox a enregistré de l'activité :

- **Journal des modifications** : `dropbox_vetalyx_changes.log` mis à jour
- **Snapshot de l'état** : `dropbox_vetalyx_snapshot.json` capturé dans tmp/
- **Rapport d'entrée** : `2026-06-10_corbeau_graphify-update_dobby.md` créé dans TEAM_Inbox

Le service de suivi (`dropbox-watch.log`) et le script de lancement (`_run_graphify.py`) ont été exécutés.

## Bases de données et état TEAM

Les fichiers de coordination d'équipe ont été modifiés :

- `TEAM/team.db` : mise à jour
- `TEAM/araignee.md` et `TEAM/trace.md` : modifications de suivi
- Archive de recherche consultée : `2026-05-01_research-seo-specialist_furet.md`

## Infrastructure locale

- **Home Assistant** : base de données `home-assistant_v2.db` avec fichiers WAL et SHM actualisés
- **Services** : fichier de configuration plist Dropbox-Inbox-Watch (`com.dobby.dropbox-inbox-watch.plist`) présent
- **Sauvegarde** : log de backup PKA M1 enregistré (`backup_pka_m1.log`)
- **Autostart** : exécution Plane notifiée (`plane-autostart.log`)

## Résumé

Journée d'exécution stable du pipeline principal avec synchronisation des données d'équipe et maintien de l'infrastructure locale.