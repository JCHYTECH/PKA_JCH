```yaml
date: 2026-06-20
tags: [maintenance, infrastructure, automation]
```

# Journée du 20 juin 2026

## Infrastructure et scripts de lancement

Révision systématique des scripts d'invocation d'IA dans `bin/`. Mise à jour des lanceurs pour :
- OpenRouter (KIMI)
- Qwen3
- Gemma4
- DeepSeek (standard et R1)
- Gemini
- Claude
- Codex

Ajustement du script `dobby.sh` et du diagnostic `dobby-doctor`. Intégration d'un script de montage datasets M1 (`m1-datasets-mount.sh`).

## Gestion de bases de données et équipe

Modifications répétées sur le fichier `TEAM/team.db` et ses fichiers de transaction (`.db-wal`, `.db-shm`). Indique une activité soutenue d'accès/modification à la base données collaborative.

## Systèmes locaux et intégrations

Déploiement ou maintenance de plusieurs services :
- **Homeassistant** : mise à jour de la base `v2.db` (trace de transaction `.db-wal`)
- **Zigbee Bridge** : nouvelle sortie de log
- **Gateway** : génération d'état et sorties de journal
- **Plane** : log d'autostart mis à jour
- **Dropbox** : exécution de backup

## Gestion des données personnelles

Export de notes Apple vers fichier local. Backup du répertoire PKA sur M1. Activité de boucle de surveillance (watcher) avec génération d'erreurs enregistrées.

## Documentation et mémoire

Mises à jour du fichier `MEMORY.md` et des logs wiki (`wiki/log.md`, `wiki/index.md`). Enregistrement d'une session utilisateur (timestamp `20260620_214640`). Révision du profil `KIMI.md`.

## Synthèse

Journée d'administration système dense. Consolidation des outils de lancement, maintenance de l'infrastructure distribuée (HA, IoT, backup), et mise à jour des systèmes de mémoire et documentation.