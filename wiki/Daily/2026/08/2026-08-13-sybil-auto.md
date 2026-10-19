```yaml
date: 2026-08-13
type: journal
tags: [infra, design, voyage]
```

## Activité système et surveillance

La journée a été marquée par une intense activité des services de monitoring et d'infrastructure locale.

La base de données TEAM a enregistré plusieurs cycles d'écriture (team.db, team.db-wal, team.db-shm), indiquant une synchronisation active des données d'équipe.

Le service `zigbee2mqtt` a connu une séquence de redémarrages répétés entre 19h55 et 19h59, avec dix cycles de log distinct générés. Cette instabilité suggère une tentative de stabilisation de la couche domotique, possiblement liée à des reconnexions d'appareils ou à une recherche de configuration optimale.

Le service `pka-watch` a fonctionné continuellement, avec logs de freshness, deadline et launchd enregistrés. Le serveur Whisper a également produit des logs d'erreur et de sortie.

La passerelle (gateway_state.json) et le système de veille Inbox ont été mis à jour.

## Alerte et triage

Un événement TEAM_Inbox a été capturé dans le fichier `2026-08-13_forge_watch-inbox-alert.md`, signalant une nouvelle entrée détectée par le système de surveillance des messages d'équipe.

## Travail créatif - Design

Trois fichiers relatifs au projet de sticker "Lupo G" ont été créés ou modifiés en inbox :
- sticker lupo G view.png et .psd (asset de visionnage)
- sticker lupo G step 1 to svg.psd (étape 1 de vectorisation)
- sticker lupo G step 2 to svg.png (étape 2 de vectorisation)

Le projet progresse dans sa phase de conversion vers format vectoriel.

## Travail de projet - Voyages et exploration

Un fichier de coordonnées géographiques a été intégré au projet pka-decouvertes : `lieux_google_maps.csv`. Cet enrichissement complète les références spatiales du projet de découverte.