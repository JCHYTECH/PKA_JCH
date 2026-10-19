```yaml
---
date: 2026-10-08
tags:
  - infrastructure
  - système
  - automatisation
---
```

# Journal du 8 octobre 2026

## Infrastructure système

La journée s'est concentrée sur l'activité des systèmes d'automatisation et de surveillance. L'infrastructure locale a connu une intense période de traitement et de logging.

### Base de données équipe

La base de données TEAM a été modifiée, avec mise à jour des fichiers associés (`.db-wal`, `.db-shm`, `.db`). Ces modifications suggèrent des opérations transactionnelles courantes.

### Passerelle et pont Zigbee

L'état de la passerelle a été actualisé via `gateway_state.json`. Le bridge Zigbee a produit des traces (`zigbee-bridge.out`) et généré plusieurs fichiers de log horodatés :
- 2026-10-08.19-56-27
- 2026-10-08.19-56-54
- 2026-10-08.19-57-21
- 2026-10-08.19-58-42

Ces multiples redémarrages ou reconnexions indiquent une activité importante ou des réinitialisations du service.

## Systèmes de surveillance et tâches planifiées

Intense activité des watchs et des tâches d'arrière-plan :

**Surveillance spécialisée :**
- Surveillance des prix Bluetti (`bluetti_price_watch`)
- Surveillance de la boîte de réception (`inbox-watch`)
- Surveillance des hôtes PKA (`pka-host-watch`, `pka-watch-host`)
- Surveillance générale PKA (`pka-watch`) avec gestion des délais (`pka-watch-deadline`)
- Surveillance de la fraîcheur des données (`pka-watch-freshness`)
- Surveillance spécifique Bluetti (`pka-watch-bluetti`)

**Tâches de maintenance :**
- Sauvegarde (`pka-backup`)
- Nettoyage (`pka-cleanup`)
- Traitement graphique (`graphify`)
- Remplissage Overpass (`overpass-backfill`)

Tous ces processus ont généré des logs (`.log`, `.out`, `.err`), attestant d'une exécution active tout au long de la journée.

### Logs launchd

Un fichier `pka-watch.launchd.log` a été enregistré, confirmant que les tâches sont orchestrées par le scheduler système.