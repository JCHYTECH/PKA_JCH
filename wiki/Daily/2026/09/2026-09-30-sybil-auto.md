```yaml
---
date: 2026-09-30
archiviste: Sybil
type: journal-automatique
---
```

# 30 septembre 2026

## Activité juridique — Vetalyx

La journée a porté essentiellement sur la matérialisation du cadre juridique du projet Vetalyx. Quatre documents ont été produits ou finalisés :

- **Pacte d'actionnaires v1** : soumis aux partenaires pour validation
- **Validation du fond juridique** : mémo de Dobby analysant la structure proposée
- **Convention du bloc fondateurs v1** : document cadre des engagements mutuels
- **Synthèse de lecture** : consolidation des points critiques et recommandations

Ces documents marquent le passage de la phase de cadrage à celle de formalisation contractuelle. L'implication de Dobby (briefing et validation) signale une relecture externe de la structure.

## Infrastructure système

Plusieurs cycles de reconnexion et synchronisation ont été enregistrés sur l'écosystème domotique et serveurs locaux :

- **Zigbee2MQTT** : 10 séquences de log entre 19h56 et 20h00, suggérant des redémarrages ou réinitialisations de pont radio
- **Services locaux** : activité normale sur gateway, watchdog PKA, backfill Overpass, serveur Whisper (logs stdOut/stdErr)
- **Base de données TEAM** : modifications enregistrées (team.db + fichiers temporaires WAL/SHM)

L'état global de l'infrastructure a été consolidé dans `gateway_state.json` et les métriques d'inbox-watch révisées.

## Extraction statuts

Un fichier temporaire contenant un extrait des statuts (référence 2209) a été traité, probablement en support des démarches juridiques Vetalyx.

## Collecte données — Travels

Un cycle de collecte de logs sur le volet PKA-découvertes (projet Travels) a été complété.