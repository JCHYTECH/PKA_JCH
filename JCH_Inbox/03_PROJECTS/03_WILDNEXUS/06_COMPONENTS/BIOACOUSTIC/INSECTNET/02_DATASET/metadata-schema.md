# InsectNet - Metadata Schema V0.1

**Date :** 2026-05-24  
**Source initiale validee :** Xeno-canto API v3  
**Espece test :** `Tettigonia viridissima`  
**Statut :** schema initial

## Objectif

Definir le format `metadata.csv` utilise pour construire le dataset InsectNet V0.1.

Le schema doit conserver :

- la tracabilite de chaque son ;
- la licence ;
- la qualite ;
- le contexte geographique ;
- les filtres utiles pour entrainement ;
- les informations techniques audio.

## Colonnes obligatoires

| Colonne | Type | Source Xeno-canto | Description |
|---|---|---|---|
| `recording_id` | string | `id` | Identifiant source stable |
| `source` | string | constant | Source, ex. `xeno-canto` |
| `source_url` | string | `url` | Page source |
| `download_url` | string | `file` | URL de telechargement |
| `file_name` | string | `file-name` | Nom fichier source |
| `local_path` | string | derive | Chemin local apres telechargement |
| `genus` | string | `gen` | Genre |
| `species` | string | `sp` | Espece |
| `species_latin` | string | `gen` + `sp` | Nom latin complet |
| `species_common_en` | string | `en` | Nom anglais si disponible |
| `group` | string | `grp` | Groupe Xeno-canto, ex. `grasshoppers` |
| `country` | string | `cnt` | Pays |
| `location` | string | `loc` | Localite |
| `latitude` | float/null | `lat` | Latitude |
| `longitude` | float/null | `lon` | Longitude |
| `altitude_m` | int/null | `alt` | Altitude |
| `date_recorded` | date/null | `date` | Date d'enregistrement |
| `time_recorded` | string/null | `time` | Heure |
| `uploaded_date` | date/null | `uploaded` | Date upload |
| `recordist` | string | `rec` | Auteur |
| `license_url` | string | `lic` | Licence |
| `quality` | string | `q` | Qualite Xeno-canto |
| `sound_type` | string | `type` | Type sonore |
| `sex` | string/null | `sex` | Sexe |
| `life_stage` | string/null | `stage` | Stade |
| `method` | string/null | `method` | Field/studio/etc. |
| `animal_seen` | string/null | `animal-seen` | Animal vu |
| `playback_used` | string/null | `playback-used` | Playback utilise |
| `temperature_c` | float/null | `temp` | Temperature |
| `device` | string/null | `dvc` | Enregistreur |
| `microphone` | string/null | `mic` | Microphone |
| `sample_rate_hz` | int/null | `smp` | Frequence d'echantillonnage |
| `duration_text` | string | `length` | Duree source, ex. `0:30` |
| `duration_s` | float | derived | Duree en secondes |
| `remarks` | string/null | `rmk` | Remarques |
| `quality_flag` | enum | derived | `ok`, `review`, `reject` |
| `split` | enum/null | assigned | `train`, `val`, `test` |
| `notes` | string/null | manual | Notes internes InsectNet |

## Colonnes recommandees plus tard

| Colonne | Description |
|---|---|
| `license_class` | `open`, `non_commercial`, `no_derivatives`, `unknown` |
| `usable_for_training` | booleen derive de la licence et du quality_flag |
| `usable_for_public_release` | booleen derive de la licence |
| `segment_count` | nombre de segments generes |
| `spectrogram_path` | chemin vers les spectrogrammes |
| `embedding_path` | chemin vers embeddings si utilises |
| `geo_region` | Belgique, France, Europe Ouest, etc. |
| `frequency_band_hint` | plage frequentielle utile si connue |

## Regles de filtrage V0.1

Filtre minimal recommande :

```text
quality in A,B
playback_used != yes
license_url known
download_url present
sample_rate_hz present
```

Filtre scientifique strict :

```text
quality == A
method == field recording
playback_used == no
animal_seen == yes
license_class in open, non_commercial
```

Filtre licence conservateur pour entrainement redistribuable :

```text
license_class == open
```

## Decision V0.1

Conserver tous les enregistrements dans `metadata.csv`, mais ne pas tout utiliser pour entrainement.

Le champ `quality_flag` et les champs de licence decident de l'usage :

- `ok` : utilisable dans le premier dataset ;
- `review` : a verifier manuellement ;
- `reject` : conserve en trace mais exclu.

