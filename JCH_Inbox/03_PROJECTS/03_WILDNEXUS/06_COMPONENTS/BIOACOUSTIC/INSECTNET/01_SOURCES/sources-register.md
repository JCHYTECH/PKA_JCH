# InsectNet - Registre des sources V0.1

**Date :** 2026-05-24  
**Projet :** InsectNet PKA_JCH / WildNexus Bioacoustique  
**Statut :** registre initial  
**Source de cadrage :** `../00_SCOPE/insectnet-v0.1-scope.md`

## Objectif

Identifier les sources audio exploitables pour InsectNet V0.1, avec un statut clair sur :

- accessibilite ;
- automatisation ;
- qualite scientifique ;
- licences ;
- priorite de traitement ;
- blocages.

## Synthese de priorite

| Priorite | Source | Usage V0.1 | Statut |
|---:|---|---|---|
| 1 | [[Xeno-Canto]] | collecte automatisable principale si cle API disponible | API v3 a cle requise |
| 2 | ECOSoundSet | benchmark / validation Orthoptera-Cicadidae Europe | a localiser et verifier |
| 3 | InsectSet459 | dataset ML large, baseline possible | a localiser et verifier |
| 4 | BioAcoustica | validation scientifique, complements propres | a verifier |
| 5 | iNaturalist | enrichissement opportuniste | filtrage licence/qualite requis |
| 6 | Freesound / Pixabay / LaSonotheque | fonds sonores, demo, exemples negatifs | non primaire |

## 1. [[Xeno-Canto]]

URL :

```text
https://xeno-canto.org
```

Documentation API :

```text
https://xeno-canto.org/explore/api
```

### Statut API

L'endpoint historique API v2 n'est plus disponible :

```text
https://xeno-canto.org/api/2/recordings?query=Tettigonia%20viridissima
```

Retour observe le 2026-05-24 :

```json
{
  "error": "server_error",
  "message": "Xeno-canto API v2 is no longer available. Visit https://xeno-canto.org/explore/api for API v3 documentation."
}
```

API v3 :

```text
https://xeno-canto.org/api/3/recordings
```

Contraintes v3 observees dans la documentation :

- `query` obligatoire ;
- `key` obligatoire ;
- requetes par tags de recherche, pas par texte libre generique ;
- `per_page` optionnel, 50 a 500 ;
- cle disponible pour les comptes [[Xeno-Canto]] avec email verifie ;
- ne pas publier la cle dans un depot.

### Requete cible V0.1

Hypothese de requete a tester quand une cle API sera disponible :

```text
https://xeno-canto.org/api/3/recordings?query=gen:Tettigonia+sp:viridissima&key=<XC_API_KEY>&per_page=100
```

Alternative par pays apres validation taxonomique :

```text
https://xeno-canto.org/api/3/recordings?query=gen:Tettigonia+sp:viridissima+cnt:Belgium&key=<XC_API_KEY>&per_page=100
```

### Donnees attendues

Champs a mapper vers `metadata.csv` :

- identifiant XC ;
- genre/espece ;
- pays ;
- localisation ;
- latitude/longitude ;
- date ;
- auteur ;
- licence ;
- URL fichier ;
- duree ;
- qualite ;
- remarques.

### Decision

[[Xeno-Canto]] reste la source prioritaire, mais InsectNet V0.1 depend maintenant d'une etape explicite :

```text
obtenir une cle API Xeno-canto
```

Sans cle, on peut documenter et preparer le pipeline, mais pas lancer de collecte automatisee propre.

## 2. ECOSoundSet

Usage prevu :

- benchmark scientifique ;
- validation initiale Orthoptera / Cicadidae ;
- comparaison avec dataset InsectNet collecte.

Statut :

```text
a localiser, telecharger et verifier licence
```

Action requise :

- trouver page officielle ;
- confirmer licence ;
- identifier format ;
- verifier presence d'especes V0.1 ;
- noter train/test splits si disponibles.

## 3. InsectSet459

Usage prevu :

- baseline ML large ;
- verification de performances sur plusieurs especes ;
- source possible de segments deja nettoyes.

Statut :

```text
a localiser, telecharger et verifier licence
```

Action requise :

- trouver depot officiel ou papier associe ;
- confirmer les sources compilees ;
- verifier licence de redistribution ;
- verifier mapping taxonomique.

## 4. BioAcoustica

URL :

```text
https://bio.acousti.ca
```

Usage prevu :

- validation scientifique ;
- sons propres ;
- reference taxonomique.

Statut :

```text
a verifier
```

Action requise :

- verifier telechargement ;
- verifier metadonnees ;
- verifier licence par enregistrement ;
- confirmer couverture europeenne des especes V0.1.

## 5. iNaturalist

URL API :

```text
https://api.inaturalist.org/v1/observations
```

Usage prevu :

- enrichissement ;
- especes rares ;
- extension geographique.

Limites :

- qualite audio variable ;
- licences mixtes ;
- observations parfois non sonores ;
- besoin de filtrage fort.

Decision V0.1 :

```text
ne pas utiliser comme source primaire
```

## 6. Sources generalistes

Sources :

- Freesound ;
- Pixabay ;
- LaSonotheque.

Usage V0.1 :

- exemples negatifs ;
- bruit de fond ;
- demo ;
- tests de robustesse.

Decision :

```text
ne pas melanger aux sons scientifiques positifs avant le premier baseline
```

## Prochaine action

1. Obtenir ou creer une cle API [[Xeno-Canto]].
2. Tester `gen:Tettigonia sp:viridissima`.
3. Capturer un echantillon JSON.
4. Definir le mapping exact vers `metadata.csv`.
5. Creer `02_DATASET/metadata-schema.md`.

