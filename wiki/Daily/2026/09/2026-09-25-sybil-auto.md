```yaml
---
date: 2026-09-25
type: journal
---
```

# Vendredi 25 septembre 2026

## Infrastructure & Monitoring

Activité soutenue sur l'infrastructure locale. Nombreuses rotations de logs sur les services de surveillance :

- **PKA Watch** : cycles de vérification de fraîcheur et de deadline, logs accumulés (freshness.out, deadline.out, watch.log)
- **PKA Backup** : exécution de sauvegarde (logs horodatés)
- **PKA Cleanup** : tâche de nettoyage complétée
- **Graphify** : traitement de données graphique
- **Overpass Backfill** : opération de synchronisation avec Overpass (traces d'erreurs détectées)

État du système courant enregistré dans `gateway_state.json`.

## Connectivité & Domotique

Activité intensive sur la passerelle Zigbee. Plusieurs démarrages/redémarrages du bridge Zigbee2MQTT détectés entre 19h55 et 20h00, avec génération de 10 fichiers de log distincts. Pas d'indication de dysfonctionnement critique — suite normale de cycles de reconnexion.

Watchlist inbox synchronisée (`inbox-watch.json`).

## Équipe & Données Partagées

Mise à jour de la base de données équipe (`TEAM/team.db-wal`).

## Projets Actifs

Deux fichiers de travail modifiés dans le projet **VETALYX** (réf: 08_VETALYX) :
- Draft email pour la Chine (Dobby)
- Email de suivi avec pack Chine, datés du 31 mai 2026

Documents stockés dans la livraison d'étape.