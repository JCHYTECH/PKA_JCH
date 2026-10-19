```yaml
---
date: 2026-10-03
tags: [infrastructure, automation, domotique, voyages]
---
```

# Mercredi 3 octobre 2026

## Surveillance énergétique Bluetti

Activité importante autour du système de surveillance des prix Bluetti. Le script `pka-watch-bluetti` a été modifié, tout comme le script d'installation du service launchd associé (`install-bluetti-price-watch-launchd.sh`). La configuration a été déployée via une nouvelle tâche planifiée (`com.dobty.pka-watch-bluetti.plist`).

L'état du service a été enregistré dans `_local/state/bluetti_price_watch.json`. Les logs montrent une activité continue avec plusieurs rotations : `bluetti_price_watch.log` contient les traces du monitoring en cours.

## Passerelle Zigbee et domotique

Activité soutenue sur le pont Zigbee2MQTT avec dix rotations de logs générées entre 19h55 et 19h59 (résolution à la minute et demi). Cela suggère un redémarrage répété ou un dépannage du service. L'état de la passerelle a été actualisé dans `_local/gateway_state.json`.

## Projet électrification camping-car

Documentation mise à jour dans le projet de voyage : le fichier `installation-bluetti-elite100v2-charger2-lupo.md` (section électricité, van technique) a reçu des modifications. Ce fichier trace probablement les spécifications et progrès de l'installation d'une batterie Bluetti Elite 100V2 avec chargeur dans le véhicule.

## Base de données partagée

La base de données d'équipe (`TEAM/team.db`) a enregistré des modifications (fichiers `.wal` et `.shm` mis à jour), indiquant une activité de synchronisation ou de transaction en cours.

## Collecte de données et logs

Le service de collecte (`pka-decouvertes`) a généré plusieurs rotations de logs. Le fichier `collector.log` et sa sauvegarde `.1` montrent une activité de fond régulière. Les autres services système (`overpass-backfill`, `whisper-server`, `pka-watch`) sont également actifs avec leurs traces respectives.

## État général

L'infrastructure locale fonctionne en continu : base de données, domotique, surveillance énergétique et collecte de données opérationnelles.