# InsectNet - Dataset Build Log

## 2026-05-24 - [[Xeno-Canto]] metadata page 1

**Commande :**

```bash
XC_API_KEY=<secret> python3 scripts/insectnet_xc_metadata.py --limit-pages 1 --per-page 100
```

**Secret handling :**

- La cle API [[Xeno-Canto]] a ete fournie en memoire uniquement.
- Elle n'a pas ete ecrite dans les fichiers PKA.

**Sortie :**

```text
Wrote 100 rows to .../INSECTNET/02_DATASET/metadata.csv
```

**Fichier produit :**

```text
INSECTNET/02_DATASET/metadata.csv
```

**Comptage par parser CSV :**

```text
rows: 100
```

Note : `wc -l` retourne plus de lignes car certains champs texte contiennent des retours ligne cites dans le CSV.

**Synthese des 100 premieres lignes :**

```text
quality_flag:
  ok     : 69
  review : 31

license_class:
  non_commercial : 51
  open           : 34
  no_derivatives : 15

usable_for_training:
  yes : 56
  no  : 44

usable_for_public_release:
  yes : 16
  no  : 84
```

**Pays les plus presents dans cet echantillon :**

```text
Spain              : 32
France             : 27
Italy              : 14
Greece             : 11
Russian Federation : 10
Germany            : 3
```

## Interpretation

Le corpus `Tettigonia viridissima` est suffisamment riche pour demarrer InsectNet V0.1.

Points importants :

- Le volume brut est bon : 631 enregistrements disponibles d'apres l'API.
- La qualite est exploitable : 69/100 lignes page 1 passent en `ok`.
- La redistribution publique sera plus limitee que l'entrainement : seulement 16/100 lignes page 1 sont `open` et `ok`.
- Les licences `non_commercial` peuvent etre utiles pour exploration interne, mais a traiter avec prudence pour toute publication.
- Les licences `no_derivatives` sont exclues de l'entrainement par defaut.

## Prochaine etape

1. Collecter toutes les pages metadata pour `Tettigonia viridissima`.
2. Creer un resume statistique complet.
3. Repeter sur les autres especes V0.1.
4. Seulement ensuite telecharger un petit sous-ensemble audio sous licences compatibles.

## 2026-05-24 - [[Xeno-Canto]] metadata complete

**Commande :**

```bash
XC_API_KEY=<secret> python3 scripts/insectnet_xc_metadata.py --per-page 100
```

**Sortie :**

```text
Wrote 631 rows to .../INSECTNET/02_DATASET/metadata.csv
```

**Comptage par parser CSV :**

```text
rows: 631
```

**Synthese complete `Tettigonia viridissima` :**

```text
quality_flag:
  ok     : 535
  review : 96

license_class:
  open           : 448
  non_commercial : 148
  no_derivatives : 35

quality:
  B : 475
  C : 64
  A : 61
  D : 31

usable_for_training:
  yes : 506
  no  : 125

usable_for_public_release:
  yes : 392
  no  : 239

method:
  field recording  : 591
  studio recording : 40

playback_used:
  no      : 626
  unknown : 4
  yes     : 1

animal_seen:
  yes     : 490
  no      : 120
  unknown : 21
```

**Pays principaux :**

```text
Netherlands        : 249
France             : 105
Spain              : 73
Greece             : 67
Italy              : 44
Germany            : 26
Russian Federation : 20
Sweden             : 14
Albania            : 13
Belgium            : 1
```

**Frequences d'echantillonnage principales :**

```text
384000 : 196
256000 : 170
44100  : 93
192000 : 59
96000  : 51
48000  : 29
```

**Interpretation :**

`Tettigonia viridissima` est validee comme espece pilote InsectNet V0.1.

Le volume est suffisant pour :

- creer un premier dataset ;
- entrainer une baseline ;
- tester differents filtres licence/qualite ;
- evaluer l'impact de sample rates eleves, importants pour insectes.

**Decision :**

Passer a la collecte metadata des autres especes V0.1 avant de telecharger l'audio.

## 2026-05-24 - Collecte metadata multi-especes V0.1

Collectes [[Xeno-Canto]] API v3 terminees pour les especes candidates.

Resultats :

```text
Tettigonia viridissima       : 631
Gryllus campestris           : 367
Pholidoptera griseoaptera    : 1417
Leptophyes punctatissima     : 353
Metrioptera roeselii strict  : 0
Roeseliana roeselii          : 268
Cicada orni                  : 0
```

Correction :

```text
Metrioptera roeselii -> utiliser Roeseliana roeselii dans Xeno-canto.
```

Decision :

```text
InsectNet V0.1 Xeno-canto = 5 especes exploitables.
Cicada orni est gardee pour recherche source alternative.
```

Resume detaille :

```text
v0.1-species-metadata-comparison.md
```
