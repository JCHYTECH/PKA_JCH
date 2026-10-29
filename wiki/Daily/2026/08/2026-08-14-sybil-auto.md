```yaml
---
date: 2026-08-14
tags: [infrastructure, systèmes, logs]
---
```

# 14 août 2026

## Infrastructure réseau et passerelle

La passerelle locale a connu une période d'activité soutenue. L'état de la configuration réseau a été enregistré dans `gateway_state.json`. Le pont Zigbee a généré plusieurs cycles de redémarrage ou de reconnexion entre 19h55 et 19h59, produisant dix fichiers journaux distincts sur cette plage horaire.

## Système Zigbee

Le service Zigbee2MQTT a enregistré une succession rapide de journaux entre 19h55:42 et 19h59:45. Cette densité de fichiers — dix entrées en moins de quatre minutes — suggère soit une boucle de redémarrage, soit une haute fréquence d'événements captés par le système de domicatique.

## Services et observabilité

Plusieurs services ont laissé des traces :
- **pka-watch** : activité enregistrée dans les logs de surveillance et dans le journal launchd
- **whisper-server** : génération de logs de sortie standard et d'erreurs
- **inbox-watch** : mise à jour de l'état de surveillance dans `_local/state/`

## Projet Pka-découvertes

Le système de collecte du projet de voyages "pka-découvertes" a effectué une rotation de ses fichiers journaux : `collector.log` et son archive `collector.log.1` ont été mises à jour.

## Équipes et base de données

La base de données partagée `TEAM/team.db` a connu des modifications, enregistrées dans les fichiers d'écriture anticipée (`-wal`) et de mémoire partagée (`-shm`), indiquant une activité transactionnelle.