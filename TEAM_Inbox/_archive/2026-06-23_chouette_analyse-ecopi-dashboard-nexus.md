# ecoPi-RTF — Analyse pour Dashboard NEXUS_ACOUSTIC

> **Date :** 2026-06-23  
> **Source :** https://github.com/birdnet-team/ecopi-rtf  
> **Auteur :** Dobby 🦉 → Chouette 🦉 (implémentation)  
> **Statut :** Analyse — prêt pour prototypage

---

## Résumé

ecoPi-RTF est un dashboard Dash (Plotly) qui visualise en temps réel les données collectées par des enregistreurs acoustiques ecoPi. Il affiche les détections d'espèces, les spectrogrammes, et les tendances temporelles.

## Architecture technique

| Composant | Techno | Pertinence PKA |
|-----------|--------|----------------|
| Frontend | Dash (Plotly) | Même stack que nos dashboards existants |
| Backend | Python Flask (via Dash) | Compatible scripts/ PKA |
| Cache | Route `/cache` + cron 30min | Pattern à réutiliser |
| Déploiement | Gunicorn + Nginx | Compatible RPi 5 |
| Config | YAML par projet | Pattern multi-site intéressant |
| API externe | OekoFor API (données audio) | Remplacer par notre propre API |
| Météo | OpenWeatherMap API | Contexte environnemental enrichissant |

## Structure du projet

```
ecopi-rtf/
├── app.py              # Point d'entrée Dash
├── configs/            # YAML par projet (SWAMP, AMiC...)
│   └── swamp_config.yaml
├── assets/             # CSS, images
├── requirements.txt
└── .env                # API_TOKEN, OWM_API_KEY
```

## Patterns réutilisables

### 1. Configuration multi-projet par YAML

```yaml
# Pattern: un fichier YAML par site de monitoring
project_name: "NEXUS_ACOUSTIC"
species_list: "data/species_tilff.csv"
detections_db: "data/detections.db"
map_center: [50.55, 5.58]  # Tilff
timezone: "Europe/Brussels"
```

### 2. Route de cache avec cron

```python
@app.callback(...)
def cache_route():
    # Régénère les données agrégées toutes les 30 min
    pass
```
Pattern directement applicable pour pré-calculer les stats de détection InsectNet.

### 3. Visualisations standard

- **Timeline des détections** — espèce × temps
- **Spectrogramme interactif** — zoom, sélection temporelle
- **Carte de présence** — heatmap géographique
- **Top espèces** — bar chart temps réel
- **Météo contextuelle** — overlay conditions environnementales

## Plan d'adaptation NEXUS_ACOUSTIC

### Phase 1 — Clone et adaptation (juillet)

1. Cloner ecoPi-rtf → `NEXUS_ACOUSTIC/dashboard/`
2. Remplacer OekoFor API → notre API de détections InsectNet
3. Adapter les visualisations aux données orthoptères
4. Ajouter le manifold UMAP 3D existant (déjà fait le 19 juin)

### Phase 2 — Déploiement RPi 5

5. Déployer sur le RPi 5 (même machine que BirdNET-Go)
6. Configurer Gunicorn + Nginx
7. Accès via Tailscale (déjà en place)

### Phase 3 — Enrichissement

8. Intégrer données météo (OpenWeatherMap gratuit)
9. Ajouter post-filtre geomodel insectes (si proto Clio validé)
10. Export CSV/JSON pour analyse externe

## Stack technique recommandée

```text
Dash + Plotly       → Frontend interactif (déjà maîtrisé)
Flask-Caching       → Cache des requêtes lourdes
SQLite              → Stockage détections (déjà dans Faune Autour)
Gunicorn            → Production WSGI
Tailscale           → Accès distant (déjà en place)
```

## Effort estimé

| Phase | Tâches | Effort |
|-------|--------|--------|
| 1. Clone + adaptation | Fork, remplacer API, adapter vues | 2-3 jours |
| 2. Déploiement | Config Gunicorn/Nginx, test RPi | 1 jour |
| 3. Enrichissement | Météo, geomodel, exports | 2-3 jours |

---

*À valider par Chouette — le dashboard ecoPi est un bon point de départ mais l'adaptation aux insectes nécessite de repenser les visualisations spectrales (fréquences plus hautes, patterns temporels différents des oiseaux).*
