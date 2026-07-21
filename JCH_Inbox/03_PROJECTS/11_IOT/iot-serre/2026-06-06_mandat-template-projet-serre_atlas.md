# Mandat [[Atlas]] — Structure projet & Template PKA

**Demandeur :** [[Dobby]] 🦉
**Date :** 2026-06-06
**Urgence :** Normale
**Projet source :** `11_IOT/iot-home/` — Serre connectee
**Projets futurs :** Tous projets PKA

## Contexte

JCH souhaite deux livrables :

### Livrable A — Template projet PKA generique

Inspire de la structure WildNexus, mais genericise pour tout projet PKA.

Proposition de base (a challenger par toi) :

```
PROJET_XX/
  00_GOUVERNANCE/        Pilotage, roles, mapping equipe
  01_FONDATION/          Document fondateur, scope, exit conditions
  02_DECISIONS/          ADR et decisions architecturales
  03_WP/                 Work packages par phase (WP01, WP02...)
  04_LIVRABLES/          Outputs finaux (specs, exports, validations)
  05_RESSOURCES/         Donnees, visuels, schemas, templates
  06_COMPOSANTS/         Sous-projets adjacents ou futurs
  INDEX.md               Vue d ensemble du projet
```

**Contraintes :**
- Applicable a tous les projets (ARTEON, VETALYX, IOT, FUTURE_INVEST...)
- Trop de dossiers tue le dossier — si un projet n a pas besoin d un niveau, il ne le cree pas
- Structure plate (pas plus de 2 niveaux)
- Compatible Obsidian (wikilinks [[...]], tags)

### Livrable B — Document de developpement Serre IoT

Appliquer le template au projet serre, avec :

| Sujet | Contenu source |
|-------|---------------|
| Contexte | Maison Rue des Renards, Esneux — 800 m, lotissement |
| Serre | 3 x 4 m (12 m), eau pluie (tonneau 225L), solaire si possible |
| Arrosage | Parkside PBSS1 A1 12V, pompe + electrovanne, 2 capteurs humidite sol |
| Ventilation | Fenetres existantes + ventilateur 12V ajout |
| Station meteo | Ecowitt (T, H, vent, pluie, pression) — prioritaire |
| Camera | ESP32-CAM timelapse croissance |
| Controleur | ESP32 via ESPHome, Zigbee prefere |
| Dashboard | Home Assistant (existant sur Mac M5) |
| Alimentation | Solaire 20W ou filaire 12V (si < 15m maison) |
| Logique HA | Seuils humidite sol → arrosage. Station meteo → skip si pluie/vent. Temp → ventilateur |
| References web | 5 projets GitHub identifies (voir [[INDEX]].md) |
| Budget | ~259 EUR (BOM detaille dans [[INDEX]].md) |
| Priorite | Serre d abord, maison en P2 |

## Livrable attendu

1. **Template projet PKA** (fichier `JCH_Inbox/90_TEMPLATES/PROJECT-TEMPLATE.md`)
2. **Fondation Serre IoT** appliquant le template (dans `11_IOT/iot-home/`)

## Referent technique

[[Araignee]] pour la partie capteurs/firmware/ESPHome.
Le projet serre est deja documente dans `11_IOT/iot-home/INDEX.md`.

---

## Sources

- `11_IOT/iot-home/INDEX.md` — contenu actuel du projet serre
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/` — structure a inspirer
- `JCH_Inbox/03_PROJECTS/07_TRAVELS/INDEX.md` — structure projet existante
- Meme structure que WildNexus, mais plus legere
