# InsectNet - Dataset Summary: Tettigonia viridissima

**Date :** 2026-05-24  
**Source :** Xeno-canto API v3  
**Fichier :** `metadata.csv`  
**Statut :** espece pilote validee

## Resultat global

```text
Total recordings: 631
Usable for internal training: 506
Usable for strict public release: 392
Review/reject candidate: 125
```

## Qualite

| Qualite Xeno-canto | Nombre |
|---|---:|
| A | 61 |
| B | 475 |
| C | 64 |
| D | 31 |

| Flag InsectNet | Nombre |
|---|---:|
| ok | 535 |
| review | 96 |

## Licences

| Classe licence | Nombre | Usage recommande |
|---|---:|---|
| open | 448 | entrainement + release possible selon attribution |
| non_commercial | 148 | exploration interne, prudence publication |
| no_derivatives | 35 | exclure par defaut de l'entrainement |

## Contexte d'enregistrement

| Champ | Valeur | Nombre |
|---|---|---:|
| method | field recording | 591 |
| method | studio recording | 40 |
| playback_used | no | 626 |
| playback_used | unknown | 4 |
| playback_used | yes | 1 |
| animal_seen | yes | 490 |
| animal_seen | no | 120 |
| animal_seen | unknown | 21 |

## Pays principaux

| Pays | Nombre |
|---|---:|
| Netherlands | 249 |
| France | 105 |
| Spain | 73 |
| Greece | 67 |
| Italy | 44 |
| Germany | 26 |
| Russian Federation | 20 |
| Sweden | 14 |
| Albania | 13 |
| Belgium | 1 |

## Frequences d'echantillonnage

| Sample rate Hz | Nombre |
|---:|---:|
| 384000 | 196 |
| 256000 | 170 |
| 44100 | 93 |
| 192000 | 59 |
| 96000 | 51 |
| 48000 | 29 |

## Lecture scientifique et technique

Le corpus est particulierement interessant pour InsectNet car une grande partie des enregistrements est en sample rate eleve.

Cela confirme que la bioacoustique insectes ne doit pas etre traitee exactement comme BirdNET oiseaux :

- beaucoup d'information utile peut se trouver haut en frequence ;
- les choix micro et sample rate terrain seront structurants ;
- les downsampling agressifs peuvent detruire le signal.

## Decision

`Tettigonia viridissima` est retenue comme premiere espece pilote V0.1.

Avant tout telechargement audio massif, collecter les metadonnees des autres especes V0.1 pour comparer :

- volume disponible ;
- licences ;
- qualite ;
- geographie ;
- sample rates ;
- proportion terrain/studio.

