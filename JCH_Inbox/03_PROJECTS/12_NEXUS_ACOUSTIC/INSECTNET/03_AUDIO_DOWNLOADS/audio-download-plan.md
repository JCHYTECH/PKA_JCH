# InsectNet - Plan de telechargement audio minimal V0.1

**Date :** 2026-05-24  
**Statut :** manifeste pret, audio non telecharge  
**Manifeste :** `audio-download-manifest.csv`

## Objectif

Telecharger un premier lot reduit et propre pour tester le pipeline audio InsectNet sans aspirer tout Xeno-canto.

## Lot selectionne

```text
5 especes
20 sons par espece
100 candidats au total
```

Especes :

1. `Tettigonia viridissima`
2. `Gryllus campestris`
3. `Pholidoptera griseoaptera`
4. `Leptophyes punctatissima`
5. `Roeseliana roeselii`

## Filtres appliques

Chaque candidat respecte :

```text
quality_flag = ok
usable_for_public_release = yes
playback_used = no
method = field recording
license_class = open
quality = A ou B
sample_rate_hz >= 44100
duration_s > 0
download_url present
```

## Resultat du manifeste

```text
Total candidats : 100

Par espece :
  Tettigonia viridissima    : 20
  Gryllus campestris        : 20
  Pholidoptera griseoaptera : 20
  Leptophyes punctatissima  : 20
  Roeseliana roeselii       : 20

Qualite :
  A : 25
  B : 75

Sample rates :
  384000 : 86
  96000  : 12
  44100  : 2
```

## Lecture

Le lot est volontairement strict :

- licences ouvertes ;
- terrain uniquement ;
- pas de playback ;
- haute frequence preservee ;
- taille compatible avec ecoute/verification manuelle.

## Attention

Le choix par score favorise fortement les sample rates eleves. Cela est utile pour insectes, mais peut concentrer les sons chez quelques recordists ou pays.

Avant entrainement, verifier :

- diversite des auteurs ;
- diversite geographique ;
- presence de bruit parasite ;
- durees trop longues a segmenter ;
- homogenisation des niveaux audio.

## Prochaine etape

Creer le script de telechargement audio depuis `audio-download-manifest.csv`.

Regles :

- ne telecharger que les 100 candidats ;
- ranger par espece ;
- conserver les noms XC ;
- ne pas modifier les originaux ;
- produire un `download-log.csv`.

## Telechargement effectue

**Date :** 2026-05-24  
**Script :** `scripts/insectnet_download_audio.py`  
**Log :** `download-log.csv`

Resultat :

```text
Processed 100 rows: downloaded=100
```

Verification :

```text
downloaded files : 100
partial files    : 0
total size       : 1.1G
total bytes      : 1155049892
```

Repartition :

```text
Tettigonia viridissima    : 20
Gryllus campestris        : 20
Pholidoptera griseoaptera : 20
Leptophyes punctatissima  : 20
Roeseliana roeselii       : 20
```

Etat :

```text
Lot audio V0.1 minimal telecharge avec succes.
```
