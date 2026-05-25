# InsectNet - Test Xeno-canto API v3

**Date :** 2026-05-24  
**Espece cible :** `Tettigonia viridissima`  
**Objectif :** verifier l'acces API avant construction du pipeline dataset.

## Test effectue

Commande testee :

```bash
curl --silent --show-error 'https://xeno-canto.org/api/2/recordings?query=Tettigonia%20viridissima'
```

Retour :

```json
{
  "error": "server_error",
  "message": "Xeno-canto API v2 is no longer available. Visit https://xeno-canto.org/explore/api for API v3 documentation."
}
```

## Conclusion

La note source du 2026-05-23 mentionne l'API v2. Cette information est maintenant obsolete.

La collecte InsectNet doit utiliser :

```text
https://xeno-canto.org/api/3/recordings
```

## Contraintes API v3

D'apres la documentation Xeno-canto API v3 :

- `query` est obligatoire ;
- `key` est obligatoire ;
- les requetes doivent utiliser les tags de recherche Xeno-canto ;
- `per_page` est optionnel ;
- l'API exige une cle liee a un compte Xeno-canto avec email verifie ;
- la cle ne doit pas etre publiee dans un depot.

## Requete cible a tester avec cle

```bash
curl --silent --show-error 'https://xeno-canto.org/api/3/recordings?query=gen:Tettigonia+sp:viridissima&key=<XC_API_KEY>&per_page=100'
```

Variante geographique :

```bash
curl --silent --show-error 'https://xeno-canto.org/api/3/recordings?query=gen:Tettigonia+sp:viridissima+cnt:Belgium&key=<XC_API_KEY>&per_page=100'
```

## Secret handling

Ne pas ecrire `<XC_API_KEY>` dans les fichiers PKA.

Options propres :

- variable d'environnement locale `XC_API_KEY` ;
- fichier `.env` ignore par git ;
- gestionnaire de mots de passe externe.

## Etat

```text
Cle API fournie par JCH et testee en memoire uniquement le 2026-05-24.
```

## Test API v3 reussi

Requete testee :

```text
gen:Tettigonia sp:viridissima
```

Resultat global :

```text
numRecordings : 631
numSpecies    : 1
numPages      : 13
per_page      : 50
```

Exemples de resultats observes :

| XC id | Pays | Qualite | Licence | Format | Sample rate | Remarque |
|---|---|---|---|---|---:|---|
| 1095466 | Spain | A | CC BY-SA 4.0 | WAV | 384000 | field recording, male adult, calling song |
| 1086751 | Germany | A | CC BY-NC-ND 4.0 | WAV | 300000 | studio recording, playback used |
| 1060773 | France | A | CC0 1.0 | WAV | 44100 | field recording, parabolic mic |

Champs confirmes dans la reponse :

- `id`
- `gen`
- `sp`
- `grp`
- `en`
- `rec`
- `cnt`
- `loc`
- `lat`
- `lon`
- `alt`
- `type`
- `sex`
- `stage`
- `method`
- `url`
- `file`
- `file-name`
- `lic`
- `q`
- `length`
- `time`
- `date`
- `uploaded`
- `animal-seen`
- `playback-used`
- `temp`
- `dvc`
- `mic`
- `smp`

## Implications InsectNet

Xeno-canto est confirme comme source exploitable pour la V0.1.

Points d'attention :

- Les licences sont heterogenes : CC0, CC BY-SA, CC BY-NC-ND, etc.
- Certains enregistrements sont en studio, d'autres en terrain.
- Certains utilisent playback, ce qui doit etre marque.
- Les frequences d'echantillonnage varient fortement : 44.1 kHz a 384 kHz observe.
- La qualite `A` existe en quantite suffisante pour demarrer.

Decision :

```text
Le pipeline doit filtrer explicitement par licence, qualite, methode, playback, pays et sample_rate.
```
