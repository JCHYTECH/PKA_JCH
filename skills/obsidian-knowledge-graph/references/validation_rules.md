# Regles de validation - Obsidian Knowledge Graph

## Interdits par defaut

Ne jamais wikilinker automatiquement :

- `Claude`
- `ChatGPT`
- `Python`
- `Apple`
- `Pi`

Ces termes restent en file de revue tant que JCH n'a pas donne une decision canonique.

## Cibles canoniques

Agents :

- dossier canonique : `TEAM/`
- `Heron` et `Héron` doivent etre traites comme alias possibles ; demander validation avant fusion.

Projets :

- dossier canonique : `JCH_Inbox/03_PROJECTS/<projet>/`
- les `INDEX.md` projet restent les points d'entree humains.

Technologies :

- lier seulement les termes presents dans le dictionnaire genere ;
- preferer les formes specifiques : `Raspberry Pi 5` plutot que `Pi`.

## Zones a eviter

Ne pas proposer de remplacement dans :

- blocs de code Markdown ;
- spans inline entre backticks ;
- liens Obsidian deja existants `[[...]]` ;
- fichiers racine de configuration ou pointeurs systeme, sauf demande explicite.

## Workflow de modification reelle

Toute modification reelle doit etre precedee par :

1. un dry-run limite ;
2. une validation JCH ;
3. une verification du diff ;
4. les tests pertinents ;
5. un commit dedie.
