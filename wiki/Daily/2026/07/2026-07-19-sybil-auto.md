```yaml
---
date: 2026-07-19
tags: [infrastructure, automation, mqtt, zigbee, surveillance]
---
```

# 19 juillet 2026

## Surveillance et alertes

Un nouvel élément a été enregistré dans l'inbox de suivi : `forge_watch-inbox-alert.md`. Le système de surveillance des modifications de fichiers continue de fonctionner.

## Infrastructure domotique

### Zigbee et MQTT

L'activité s'est concentrée sur la couche de communication domotique. Le bridge Zigbee a enregistré plusieurs cycles de redémarrage ou de reconnexion entre 19h55 et 19h59 :
- Neuf fichiers journaux générés en moins de cinq minutes
- La base de données Zigbee a été modifiée, ainsi que sa configuration YAML
- Les états du gateway et du bridge Zigbee ont été synchronisés

La passerelle MQTT (Mosquitto) a reçu une mise à jour de configuration et des ajustements d'authentification (fichier passwd).

## Système local et services

### Logs et monitoring

- Le watchdog d'inbox (`inbox-watch.json`) a enregistré des changements d'état
- Les services en arrière-plan (whisper-server, pka-watch) ont généré des entrées journalières
- Le dashboard a produit un log de lancement

### État du système

L'état global enregistré dans `gateway_state.json` a été mis à jour, reflétant probablement les variations d'état observées du côté Zigbee/MQTT.

## Environnement de développement

La base de données d'équipe (TEAM/team.db et ses fichiers de verrouillage WAL/SHM) a enregistré des modifications. Des dépendances Python, notamment Paho MQTT 2.1.0, ont reçu une attention particulière, probablement dans le cadre d'une maintenance ou mise à jour de l'environnement virtuel.

La configuration des sous-agents dans `.deepseek/` a également été synchronisée.