# InsectNet PKA_JCH - Cadrage V0.1

**Date :** 2026-05-24  
**Projet parent :** WildNexus / Bioacoustique  
**Statut :** cadrage initial  
**Owner orchestration :** Dobby  
**Specialistes mobilises :** Furet, Clio, Forge, Chouette, Nova  
**Source de depart :** `../2026-05-23_insect-sound-sources-europe.md`

## 1. Intention

InsectNet PKA_JCH vise a creer un module de reconnaissance acoustique des insectes europeens, d'abord comme preuve de faisabilite scientifique et technique, puis comme brique future de WildNexus.

Le projet ne cherche pas a remplacer BirdNET. Il s'en inspire pour l'architecture :

- analyse par fenetres audio ;
- classification taxonomique ;
- score de confiance ;
- filtrage geographique ;
- historique local ;
- integration terrain sur Raspberry Pi ou base WildNexus.

## 2. Principe de cadrage V0.1

V0.1 doit rester volontairement etroit :

```text
5-6 especes europeennes sonores
dataset propre
pipeline reproductible
classification baseline
validation mesurable
```

La V0.1 n'a pas pour objectif de reconnaitre tous les insectes, ni de fonctionner en temps reel sur le terrain des le depart.

## 3. Especes prioritaires V0.1

Liste initiale issue de la note source :

1. `Tettigonia viridissima`
2. `Gryllus campestris`
3. `Pholidoptera griseoaptera`
4. `Leptophyes punctatissima`
5. `Metrioptera roeselii`
6. `Cicada orni`

Critere de choix :

- sons distinctifs ;
- presence europeenne ;
- disponibilite probable de donnees audio ;
- interet naturaliste pour WildNexus ;
- couverture suffisante dans les sources ouvertes.

## 4. Sources de donnees

### Priorite 1 - collecte automatisable

- Xeno-canto : API publique, metadonnees riches, GPS, licences, telechargement automatisable.

### Priorite 2 - validation scientifique et benchmark

- ECOSoundSet : dataset europeen Orthoptera / Cicadidae, annote, utile pour validation.
- InsectSet459 : dataset large, deja compile, utile pour baseline ML.
- BioAcoustica : source scientifique specialisee insectes.

### Priorite 3 - enrichissement controle

- iNaturalist : volume et geolocalisation, mais qualite et licences variables.
- Freesound / Pixabay / LaSonotheque : utiles surtout pour bruit de fond, demo, pretraining ou exemples negatifs, pas comme source scientifique primaire.

## 5. Schema de metadonnees minimal

Chaque enregistrement doit produire une ligne dans `metadata.csv` avec :

| Champ | Description |
|---|---|
| `recording_id` | identifiant source stable |
| `source` | xeno-canto, ecosoundset, bioacoustica, inaturalist, etc. |
| `species_latin` | nom latin |
| `species_common` | nom commun si disponible |
| `country` | pays |
| `latitude` | latitude si disponible |
| `longitude` | longitude si disponible |
| `date_recorded` | date de prise de son |
| `author` | auteur ou deposant |
| `license` | licence exacte |
| `download_url` | URL du fichier audio |
| `local_path` | chemin local apres telechargement |
| `sample_rate` | frequence d'echantillonnage |
| `duration_s` | duree en secondes |
| `quality_flag` | ok, review, reject |
| `notes` | remarques libres |

## 6. Pipeline technique cible

Pipeline V0.1 :

```text
source audio
-> telechargement
-> metadata.csv
-> controle licence
-> controle qualite manuel leger
-> segmentation 1-3 s
-> spectrogrammes
-> baseline classifier
-> evaluation
-> rapport de resultats
```

La segmentation cible des fenetres courtes, car les insectes produisent souvent des motifs repetitifs dont la signature est visible sur spectrogramme.

## 7. Baseline modele

Deux pistes acceptables pour V0.1 :

### Baseline A - CNN spectrogrammes

Approche simple :

- convertir segments audio en spectrogrammes ;
- entrainer un CNN leger ;
- evaluer par espece.

Avantage : lisible, rapide a prototyper, compatible avec une evolution embarquee.

### Baseline B - embeddings audio

Approche plus proche des systemes modernes :

- extraire des representations audio ;
- entrainer un classifieur leger dessus.

Avantage : peut mieux generaliser, mais depend davantage des outils choisis.

Decision V0.1 recommandee : commencer par **Baseline A**, puis comparer a B si les donnees sont suffisantes.

## 8. Integration BirdNET / BirdNET-Pi

BirdNET-Pi reste le socle oiseaux actuel du Raspberry Pi. InsectNet V0.1 doit d'abord exister comme module separe.

Architecture cible a terme :

```text
RPI / micro
-> flux audio
-> BirdNET-Pi pour oiseaux
-> InsectNet pour insectes
-> historique local WildNexus
-> filtrage geographique
-> export ou dashboard commun
```

Regle : ne pas casser BirdNET-Pi pour tester InsectNet.

## 9. Hors scope V0.1

Sont explicitement hors scope :

- reconnaissance de tous les insectes europeens ;
- temps reel terrain obligatoire ;
- integration directe dans BirdNET-Pi ;
- app iPhone dediee ;
- cloud public ;
- modele embarque ultra-low-power ;
- achat de materiel specifique avant validation du dataset ;
- entrainement d'un modele massif.

## 10. Critères de succes V0.1

V0.1 est reussie si :

- au moins 5 especes prioritaires disposent d'un corpus exploitable ;
- les licences sont documentees ;
- le pipeline de telechargement et metadata est reproductible ;
- les segments audio et spectrogrammes sont generes ;
- un premier classifieur produit une matrice de confusion ;
- les faux positifs majeurs sont identifies ;
- un rapport indique si InsectNet merite un passage V0.2.

## 11. Risques

| Risque | Impact | Mitigation |
|---|---:|---|
| Licences incompatibles | eleve | filtrer et documenter avant entrainement |
| Peu de sons propres par espece | eleve | reduire la liste V0.1 ou enrichir par source scientifique |
| Confusion entre especes proches | moyen | commencer avec especes acoustiquement distinctes |
| Bruit environnemental | moyen | qualite_flag et exemples negatifs |
| Sur-ingenierie precoce | eleve | garder V0.1 dataset + baseline uniquement |
| Integration RPI prematuree | moyen | module separe avant terrain |

## 12. Livrables V0.1

Livrables minimaux :

```text
INSECTNET/
  00_SCOPE/
    insectnet-v0.1-scope.md
  01_SOURCES/
    sources-register.md
    licenses.md
  02_DATASET/
    metadata-schema.md
    metadata.csv
    dataset-build-log.md
  03_PIPELINE/
    segmentation-notes.md
    spectrogram-notes.md
  04_MODELS/
    baseline-results.md
  05_FIELD/
    rpi-field-test-protocol.md
```

## 13. Prochaine etape recommandee

Creer le registre de sources V0.1 :

```text
INSECTNET/01_SOURCES/sources-register.md
```

Puis tester Xeno-canto sur une seule espece :

```text
Tettigonia viridissima
```

Objectif du premier test :

- confirmer l'API ;
- recuperer metadata ;
- verifier licence ;
- telecharger quelques fichiers ;
- evaluer qualite et frequences utiles.

