  

MAPS GOOGLE . j'ai enregistre sur mon google maps plusieurs endroits en diverses categories, j'aimerais organiser ces enregistrements via par exemple excell car il y a plusieurs facons de les classer par mono classe ou par classe croisée. comment faire pour avoir ce type de fichier qui soit toujours à jour avec maps

09:47

# Synchroniser les lieux sauvegardés Google Maps avec un fichier Excel

Il y a deux problèmes distincts ici : **extraire** les données, puis **les garder à jour**. Soyons clairs sur ce qui est faisable et ce qui ne l'est pas.

## Extraction initiale : Google Takeout

Google Maps n'offre pas d'export direct de vos listes de lieux sauvegardés vers un tableur. La méthode standard :

1. Aller sur **takeout.google.com**
2. Décocher tout, puis cocher uniquement **"Saved" (Enregistrés)** sous la section Maps
3. Lancer l'export — vous recevrez un fichier GeoJSON ou CSV contenant vos lieux sauvegardés avec leurs coordonnées, noms, et les listes auxquelles ils appartiennent

À partir de là, on peut structurer un Excel avec les colonnes pertinentes (nom, adresse, catégorie Google, vos propres tags croisés, coordonnées, etc.).

## Le problème de la synchronisation automatique

Voici où il faut être honnête : **il n'existe pas de méthode native pour garder un fichier Excel automatiquement synchronisé avec vos listes Google Maps.** Google ne fournit pas d'API publique pour accéder aux listes de lieux sauvegardés d'un utilisateur. L'API Google Maps/Places sert à chercher des lieux, pas à lire _vos_ listes personnelles.

Les options réalistes sont :

- **Manuelle périodique** : refaire un Takeout de temps en temps et réimporter. Fastidieux mais fiable.
- **Google Sheets + ajout manuel** : basculer vers un Google Sheet comme source de vérité _à la place de_ (ou en parallèle de) Google Maps. Vous y ajoutez vos lieux avec votre propre système de classification croisée, et c'est toujours à jour par définition.
- **My Maps (Google)** : créer une carte personnalisée dans Google My Maps, qui permet l'export/import CSV et offre des calques (layers) qui fonctionnent un peu comme des classes. Mais la classification croisée multi-critères reste limitée.

## Ce que je peux faire concrètement

Si vous faites un export Takeout et me transmettez le fichier, je peux vous construire un Excel structuré avec un système de classification croisée (colonnes de tags multiples, filtres, tableaux croisés dynamiques). Ça résout le problème de l'organisation — mais pas celui de la synchro temps réel, qui n'a pas de solution propre à ce jour.

Quelle direction vous intéresse ?

est ce que excle est la solution idéale ou peux tu proposer une alternative plus elegante et fluide ?

09:48

La question est légitime. Excel _fonctionne_, mais ce n'est pas forcément l'outil le plus adapté pour ce cas d'usage. Analysons ce dont vous avez réellement besoin :

- Des lieux avec coordonnées géographiques
- Une classification multi-critères (mono-classe ET croisée)
- De la fluidité à l'ajout et à la consultation
- Idéalement, un lien visuel avec une carte

Voici les alternatives, par ordre de pertinence :

## Notion

C'est probablement le meilleur candidat. Une base de données Notion permet de créer des propriétés multi-select (vos classifications croisées), de basculer entre vue tableau, vue galerie, vue kanban par catégorie, et d'appliquer des filtres croisés instantanément. Vous pouvez y coller un lien Google Maps par entrée. Le défaut : pas de vue carte intégrée native (il existe des extensions tierces, mais c'est bancal).

## Airtable

Similaire à Notion côté base de données, mais avec un avantage concret : **Airtable a une vue carte native**. Vous entrez des adresses ou coordonnées, et vos lieux s'affichent sur une carte, filtrables par vos catégories croisées. C'est probablement le compromis le plus fluide entre tableur, base de données relationnelle, et visualisation cartographique. Version gratuite suffisante pour un usage personnel.

## Google Sheets + Google My Maps

Approche "tout Google" : un Sheet comme base de données, lié à une carte My Maps. L'avantage est que My Maps peut importer directement depuis un Sheet. Le défaut : My Maps est assez rigide sur la classification (un calque = une catégorie), donc la dimension croisée reste dans le Sheet uniquement.

## Ce que je déconseille

Excel en local. Fichier figé, pas de vue carte, pas de filtrage dynamique agréable, pas de collaboration, pas de lien vivant avec quoi que ce soit. Ça fait le travail, mais c'est l'option la moins fluide de toutes.

## Mon avis

Si la visualisation cartographique compte : **Airtable**. Si c'est surtout la classification croisée et la flexibilité des vues qui comptent : **Notion**. Les deux sont gratuits pour cet usage.

Vous voulez que je vous prépare un template de structure (colonnes, catégories, relations) pour l'un ou l'autre ?

de airtable et notion , lequel est le plus user friendly avec courbe d'apprentissage rapide. Toi avec cowork vois tu un ajout de solutions ?

09:50

## Airtable vs Notion : courbe d'apprentissage

**Airtable est plus accessible.** L'interface ressemble à un tableur — quiconque a utilisé Excel s'y retrouve immédiatement. On ajoute des colonnes, on change leur type (texte, multi-select, URL, coordonnées), on crée des vues filtrées. La vue carte est là en deux clics. Notion est plus puissant à terme, mais son modèle "page dans page dans base de données" déroute souvent au début. Pour votre cas d'usage (une base de lieux avec classification croisée + carte), Airtable est le choix direct.

## Cowork — ce que ça peut apporter

Vous posez la bonne question. Cowork ([[Claude]] sur le bureau) peut intervenir sur la dimension fichiers et automatisation locale, mais il faut être précis sur ce qu'il fait et ne fait pas :

- **Il peut** : manipuler des fichiers locaux, transformer des exports (Takeout GeoJSON/CSV), restructurer des données, générer des fichiers d'import formatés pour Airtable ou Notion
- **Il ne peut pas** : se connecter directement à votre compte Airtable ou Google Maps pour synchroniser en temps réel, ni surveiller des changements automatiquement

Concrètement, un workflow réaliste avec Cowork serait :

1. Vous faites un Takeout Google Maps (manuel, quelques clics)
2. Vous passez le fichier à Cowork/[[Claude]]
3. [[Claude]] nettoie, restructure, applique votre grille de classification, et produit un CSV prêt à importer dans Airtable
4. Vous importez dans Airtable (drag & drop)

Ça réduit le travail de reformatage à zéro, mais ça ne supprime pas l'étape manuelle du Takeout.

## La vraie question en amont

Avant de choisir l'outil, il faudrait définir votre **grille de classification**. Quels types de critères croisés avez-vous en tête ? (type de lieu × saison × accessibilité × intérêt photo × pays/région... ?) La structure conditionne le choix du template. Si vous me décrivez vos catégories, je peux vous préparer la structure Airtable.

![1775980480696_image.png](https://claude.ai/api/10b39125-655b-4464-9f51-7278444c0323/files/019d80af-8a6d-7488-9a4a-765cd064b332/preview)

09:54

Bon, c'est un début de structure. Quelques observations avant d'aller plus loin :

## Ce qui fonctionne

- **CLASSES** et **ENVIRONNEMENT** sont vos deux axes de classification croisée — un lieu peut être à la fois "Réserve Naturelle" + "Site photo", et se trouver en "forêt" + "ruisseau". C'est exactement le cas d'usage multi-select d'Airtable.
- PAYS, COORDONNÉES GPS, ADRESSE : données factuelles, récupérables en partie depuis le Takeout.

## Ce qui manque ou mérite réflexion

**Des colonnes supplémentaires à envisager :**

- **Nom du lieu** — ça paraît évident mais ce n'est pas dans votre grille
- **Saison idéale** (multi-select : printemps, été, automne, hiver) — pertinent pour la photo wildlife
- **Espèces observées / cibles** — vous êtes photographe animalier, c'est un critère de recherche naturel
- **Statut** (visité / à visiter / à revisiter)
- **Notes / conditions d'accès** (parking, marche, autorisation requise…)
- **Lien Google Maps** — URL directe pour y naviguer depuis Airtable
- **Photos de repérage** — Airtable permet des pièces jointes par ligne

**Sur CLASSES** : "À visiter" n'est pas du même registre que "Réserve Naturelle" ou "Paysage". Les trois premiers décrivent la _nature_ du lieu, le dernier décrit votre _intention_. Ça pourrait être une colonne séparée (Statut) pour éviter de mélanger les axes.

**Sur ENVIRONNEMENT** : la liste est un bon départ. Côtes/littoral, zones humides/marais, urbain — à ajouter selon vos besoins ?

Précisez-moi ce que vous voulez garder, ajouter ou modifier, et je vous construis le template Airtable (un CSV d'import structuré avec les bons types de colonnes).

observations tres bonnes integrent les

09:55

Entendu. Je prépare le template. Avant de le construire, deux choix à faire :

Vous le voulez sous quelle forme ? Un fichier CSV prêt à importer dans Airtable, ou d'abord un visuel de la structure complète pour valider avant de produire le fichier ?

Et deuxième point : voulez-vous que je pré-remplisse quelques lignes d'exemple avec des lieux fictifs pour que la structure soit immédiatement lisible à l'import, ou vous préférez un template vide avec uniquement les en-têtes et les options de multi-select documentées à part ?

visuel d'abord

09:56

Voici la structure complète pour votre base de lieux. Chaque colonne indique son type Airtable entre parenthèses.

Quelques points à valider avant que je produise le CSV d'import :

**Région** — j'ai ajouté cette colonne séparée de Pays. Utile pour filtrer "tous les spots en Wallonie" ou "tous en Toscane" sans passer par l'adresse complète. Pertinent ou superflu dans votre cas ?

**Espèces cibles** — c'est le champ qui rend la base réellement utile pour la photo wildlife. Un filtre croisé "Environnement = Étang + Espèce = Martin-pêcheur + Saison = Printemps" vous donne instantanément vos spots. Voulez-vous pré-remplir une liste d'espèces, ou les ajouter au fil de l'eau ?

**Colonnes manquantes ?** — si d'autres critères de tri vous viennent (distance depuis Bruxelles, niveau de fréquentation, qualité de lumière…), c'est le moment de les intégrer.

region ok bonne idée pour les especes on va les ajouter au fur et à mesure qu'on les a photographié à l'endroit colonne en plus : si c'est un endroit avec horaire d'entrée, les indiquer si c'est un lieu géré (exemple reserve) il y a peut etre un site web. Si oui l'integrer

10:02

Deux colonnes ajoutées :

- **Horaires d'accès** (Single line text) — pour les lieux avec restrictions horaires (réserves, parcs fermés la nuit, etc.). Vide si accès libre.
- **Site web** (URL) — site du gestionnaire quand il existe.

La structure est finalisée. Vous voulez le CSV d'import Airtable maintenant, ou il reste des ajustements ?

Go

10:03

Viewed a file, ran a command, read a file

Viewed a file, ran a command, read a file

Le fichier contient 15 colonnes et 3 lignes d'exemple pour que Airtable détecte correctement les types de champs à l'import.

**Pour l'import dans Airtable :**

1. Créer une nouvelle base → "Import data" → glisser le CSV
2. Airtable va créer les colonnes automatiquement en "Single line text"
3. Convertir manuellement les colonnes suivantes en leur bon type : Classe → Multi-select, Environnement → Multi-select, Pays → Single select, Espèces observées → Multi-select, Saison idéale → Multi-select, Statut → Single select, Lien Google Maps → URL, Site web → URL
4. Supprimer les 3 lignes d'exemple une fois les types configurés
5. Activer la vue "Map" sur le champ Adresse ou Coordonnées GPS

Les valeurs multi-select séparées par des virgules dans le CSV seront reconnues par Airtable comme des tags distincts une fois le champ converti.

Lieux airtable import

Table · CSV 

comment on defini multiselect

10:15

Dans Airtable, une fois le CSV importé :

1. Cliquer sur l'en-tête de la colonne (par exemple "Classe")
2. Cliquer sur "Customize field type"
3. Dans le menu déroulant du type, choisir **"Multiple select"**
4. Airtable va automatiquement créer les options à partir des valeurs déjà présentes dans les cellules
5. Confirmer

À faire pour chaque colonne concernée : Classe, Environnement, Espèces observées, Saison idéale.

Pour Pays et Statut, même démarche mais choisir **"Single select"** (une seule valeur possible par ligne).

Pour Lien Google Maps et Site web, choisir **"URL"** — ça rendra les liens cliquables directement depuis la fiche.

5 comment on fait

10:17

Pour activer la vue carte dans Airtable :

1. En haut à gauche, à côté de "Grid view", cliquer sur **"+"** (ajouter une vue)
2. Choisir **"Map"**
3. Airtable demande quel champ utiliser pour géolocaliser — sélectionner **"Adresse"** ou **"Coordonnées GPS"**
4. Les lieux apparaissent comme des marqueurs sur la carte

Si vous utilisez le champ Coordonnées GPS, le format doit être `latitude, longitude` (ex : `50.7735, 4.4181`) — c'est déjà le cas dans le CSV.

À noter : la vue Map est disponible dans le plan gratuit d'Airtable, mais limitée à 100 enregistrements par vue. Au-delà, il faut un plan payant.

ok done

10:19

La base est en place. À partir de maintenant, le workflow est simple : vous ajoutez vos lieux directement dans Airtable, vous taguez les multi-selects au fur et à mesure, et les filtres croisés font le reste.

Si à un moment vous faites un Takeout Google Maps pour récupérer vos lieux déjà sauvegardés en masse, passez-moi le fichier — je le reformate pour import direct dans votre base existante.

pour ton info airtable n'est gratuit que 14 jours. donc ce n'est pas gratuit. Je prefere les solutions gratuites

10:20

Effectivement, je me suis trompé sur ce point. La politique de tarification a dû changer depuis mes données — ou j'avais une information incorrecte. Bien noté.

Alternatives réellement gratuites qui couvrent le même besoin :

**Notion** — gratuit pour usage personnel, sans limite de temps. Bases de données avec multi-select, filtres croisés, vues tableau/kanban/galerie. Pas de vue carte native, mais le lien Google Maps reste cliquable depuis chaque fiche. Le CSV que je vous ai fourni est importable directement dans une base Notion (Import → CSV).

**Google Sheets** — gratuit, vous y êtes déjà dans l'écosystème Google. Moins élégant qu'Airtable pour le multi-select (il faut utiliser la validation de données avec des listes), mais fonctionnel. Filtres croisés via les filtres natifs ou tableaux croisés dynamiques. Couplable avec Google My Maps pour la vue carte.

**NocoDB** — clone open source d'Airtable, gratuit. Multi-select, vues multiples, vue carte incluse. Hébergeable en ligne gratuitement via leur cloud. C'est probablement le remplacement le plus direct d'Airtable sans les contraintes de prix.

Lequel vous tente ? Le CSV est compatible avec les trois — seule la conversion des types de colonnes diffère légèrement.

on va essayer nocoDB

10:21

Searched the web

Searched the web

Un point important à mentionner : le plan gratuit de NocoDB cloud est limité à 1 000 enregistrements par workspace [NocoDB](https://nocodb.com/pricing). Pour votre usage (une base de lieux personnels), ça devrait largement suffire.

Cependant, NocoDB permet aussi de self-hoster la version open source gratuitement sans limite de données [Softr](https://www.softr.io/blog/baserow-vs-nocodb) — mais ça demande un serveur, ce qui n'est pas forcément ce que vous cherchez.

**Pour démarrer sur NocoDB cloud :**

1. Aller sur **nocodb.com**
2. Cliquer "Start For Free" en haut à droite
3. S'inscrire avec Google ou email
4. Créer un nouveau workspace → nouvelle base → importer le CSV

**Pour l'import du CSV et la configuration des champs :** la logique est quasi identique à Airtable. Après import, cliquer sur l'en-tête de chaque colonne → changer le type de champ vers Multi-select, Single select, ou URL selon le cas.

**Point à vérifier :** NocoDB propose les vues Grid, Kanban, Gallery et Form. La vue Map n'est pas garantie dans le plan gratuit — il faudra vérifier une fois connecté. Si elle n'est pas disponible, le lien Google Maps cliquable dans chaque fiche reste la solution de repli.

Vous y êtes ?

oui mais je vois que les liens google maps ne fonctionne pas

10:26

Les liens dans le CSV sont au format `https://maps.google.com/?q=50.7735+4.4181` — il est possible que NocoDB ne les reconnaisse pas comme URL cliquables si le champ n'est pas configuré en type URL.

Deux choses à vérifier :

1. **Le type du champ** — dans NocoDB, cliquer sur l'en-tête de la colonne "Lien Google Maps" → vérifier qu'il est bien défini comme type **URL** (et non "Single line text"). Si c'est du texte brut, les liens ne seront pas cliquables.
2. **Le format du lien** — si le problème persiste même en type URL, le format avec `+` peut poser problème. Essayez de remplacer un lien manuellement par ce format : `https://www.google.com/maps/search/?api=1&query=50.7735,4.4181` (virgule au lieu du +, et URL plus standard). Si ça fonctionne, je vous régénère le CSV avec les liens corrigés.

Quel est le comportement exact ? Le lien n'est pas cliquable, ou il s'ouvre mais n'affiche pas le bon endroit ?

1 ok

10:27

Donc le problème était le type de champ. Une fois passé en URL, les liens sont cliquables et fonctionnent ?

oui

10:27

Bien. La base est opérationnelle. Pensez à convertir aussi la colonne "Site web" en type URL si ce n'est pas déjà fait — même logique.

Vous pouvez supprimer les 3 lignes d'exemple et commencer à remplir avec vos vrais lieux. Pour le peuplement initial depuis Google Maps, le Takeout reste disponible si vous voulez importer en masse plutôt qu'à la main.

takeout low ?

10:28

Je suppose que vous demandez comment faire le Takeout Google Maps. Voici les étapes :

1. Aller sur **takeout.google.com**
2. Cliquer "Tout désélectionner"
3. Descendre jusqu'à **"Enregistrés"** (ou "Saved" en anglais) — c'est la section Google Maps — et cocher uniquement celle-là
4. Cliquer "Étape suivante"
5. Choisir le format d'export (laisser par défaut) et cliquer "Créer un export"
6. Google prépare le fichier (quelques minutes) et vous envoie un lien de téléchargement par email

Vous recevrez un fichier ZIP contenant vos lieux sauvegardés en format GeoJSON. Passez-le-moi ensuite — je le convertirai en CSV compatible avec votre structure NocoDB, colonnes pré-remplies (nom, coordonnées, adresse, lien Google Maps).

Les champs comme Classe, Environnement, Espèces, etc. resteront vides — c'est du classement manuel que vous seul pouvez faire.

### takeout-20260412T083053Z-3-001.zip

zip

10:34

Ran 8 commands

Ran 8 commands

644 lieux extraits. Un point important avant l'import :

**Le plan gratuit NocoDB cloud est limité à 1 000 enregistrements** — vous êtes à 644, ça passe.

Voici ce que le fichier contient :

- **455 lieux** avec le pays pré-rempli (déduit du nom de la liste Google Maps : Espagne 157, Italie 74, France 70, Allemagne 47, etc.)
- **176 lieux** avec une classe pré-remplie (Arbres remarquables 84, Réserve naturelle 40, Circuit 34…)
- **189 lieux** sans pays — ce sont ceux des listes thématiques (Arbres remarquables, Réserves naturelles…) qui couvrent plusieurs pays. Le pays sera à compléter manuellement.
- Les colonnes Environnement, Espèces, Saison, Horaires, Site web sont vides — à remplir au fil du temps.

Ran a command, read a file

Ran a command, read a file

Après import dans NocoDB, pensez à reconvertir les types de colonnes comme précédemment (Multi-select pour Classe, Environnement, Espèces, Saison — Single select pour Pays et Statut — URL pour Lien Google Maps et Site web).

Nocodb import

Table · CSV 

comment importer ?

10:38

Dans NocoDB :

1. Ouvrir votre base existante (celle où vous aviez importé le premier CSV)
2. Supprimer les 3 lignes d'exemple si ce n'est pas déjà fait
3. Plutôt que d'ajouter à la table existante, le plus simple est de **créer une nouvelle base** : cliquer sur **"+"** à côté de "Tables" → **"Import from CSV"** → glisser le fichier `nocodb_import.csv`
4. NocoDB va afficher un aperçu des colonnes détectées — vérifier que tout semble correct puis confirmer

Si vous préférez garder votre base existante avec les types de colonnes déjà configurés, l'autre option est :

1. Ouvrir la table existante
2. Cliquer sur **"..."** (menu en haut à droite de la table) → chercher une option d'import/ajout de lignes depuis CSV
3. Si cette option n'existe pas, il sera plus rapide de repartir d'une nouvelle table avec le gros CSV

Dans les deux cas, il faudra reconfigurer les types de colonnes après import. Vu que vous avez 644 lignes, ça vaut le coup de repartir proprement sur une nouvelle table avec ce fichier complet.

ok fini

10:44

La base est en place avec vos 644 lieux. Le gros du travail maintenant est le classement progressif : compléter les pays manquants sur les listes thématiques, taguer les environnements, ajouter les espèces au fur et à mesure de vos sorties.

Si à un moment vous refaites un Takeout pour récupérer de nouveaux lieux ajoutés dans Google Maps, repassez-moi le fichier — je ferai le diff avec l'existant pour n'ajouter que les nouvelles entrées sans doublons.

Convertis le texte de ce chat en un fichier Markdown propre, avec des titres pour chaque message et des blocs de code formatés.

10:46

Avant de lancer ça — ce chat est assez long avec beaucoup d'échanges techniques. Vous voulez :

1. **L'intégralité du chat** (chaque message JC + chaque réponse [[Claude]], verbatim) — ça fera un document conséquent
2. **Une synthèse structurée** du parcours et des décisions prises (plus utile comme référence future, plus court)

Lequel ?

synthese

10:46

Created a file, read a file

Created a file, read a file

Le document couvre les décisions prises, la structure retenue, le process d'import, et les étapes de configuration NocoDB. Utilisable comme référence si vous devez reconfigurer ou refaire un import plus tard.

Synthese base lieux

Document · MD 

  

[Claude is AI and can make mistakes. Please double-check responses.](https://support.anthropic.com/en/articles/8525154-claude-is-providing-incorrect-or-misleading-responses-what-s-going-on)

## Synthese base lieux · MD

Copy

# Base de lieux sauvegardés — Google Maps → NocoDB

## Objectif

Organiser les lieux sauvegardés dans Google Maps en une base de données structurée, avec classification croisée (multi-critères) et consultation fluide.

---

## Choix de l'outil

### Options évaluées

|Outil|Avantages|Inconvénients|Verdict|
|---|---|---|---|
|Excel|Familier|Figé, pas de vue carte, pas de filtrage dynamique|Écarté|
|Airtable|Vue carte native, multi-select, UX fluide|Gratuit 14 jours seulement|Écarté (payant)|
|Notion|Gratuit, bases de données flexibles|Pas de vue carte native|Candidat|
|NocoDB|Open source, clone Airtable, gratuit (cloud limité à 1 000 lignes)|Vue carte à vérifier|**Retenu**|

### Plateforme retenue : NocoDB cloud (nocodb.com)

- Plan gratuit : jusqu'à 1 000 enregistrements par workspace
- Version self-hosted disponible sans limite si besoin futur

---

## Structure de la base

|Colonne|Type NocoDB|Valeurs / usage|
|---|---|---|
|Nom du lieu|Single line text|Nom principal|
|Classe|**Multi-select**|Réserve naturelle, Site photo, Paysage, Arbres remarquables, Circuit, Jardins, Adresse favorite|
|Environnement|**Multi-select**|Forêt, Étang, Plaine, Montagne, Ruisseau, Côte, Marais|
|Pays|Single select|Belgique, France, Italie, Espagne, Allemagne…|
|Région|Single line text|Wallonie, Toscane, Andalousie…|
|Adresse|Single line text|Adresse complète|
|Coordonnées GPS|Single line text|Format : `50.7735, 4.4181`|
|Lien Google Maps|**URL**|Lien cliquable vers le lieu|
|Espèces observées|**Multi-select**|À remplir au fil des sorties photo|
|Saison idéale|**Multi-select**|Printemps, Été, Automne, Hiver|
|Statut|Single select|À visiter, Visité, À revisiter|
|Horaires d'accès|Single line text|Pour les lieux avec restrictions horaires|
|Conditions d'accès|Long text|Parking, marche, autorisation…|
|Site web|**URL**|Site du gestionnaire (réserve, parc…)|

### Notes de conception

- **Classe vs Statut** : séparés volontairement. Classe décrit la nature du lieu, Statut décrit l'intention.
- **Multi-select** = un lieu peut avoir plusieurs valeurs (ex : Réserve naturelle + Site photo, ou Forêt + Ruisseau).
- **Espèces** : ajoutées progressivement après observation sur le terrain, pas pré-remplies.

---

## Import des données

### Source : Google Takeout

1. Aller sur `takeout.google.com`
2. Tout désélectionner → cocher uniquement **"Enregistrés"** (section Maps)
3. Créer l'export → télécharger le ZIP reçu par email

### Conversion

Le fichier Takeout contient un CSV par liste Google Maps (BELGIQUE.csv, RESERVES NATURELLES.csv, etc.). Un script de conversion a fusionné les 24 fichiers en un seul CSV compatible NocoDB :

- **644 lieux** exportés (dédupliqués par URL)
- **455** avec pays pré-rempli (déduit du nom de la liste)
- **176** avec classe pré-remplie
- **189** sans pays (listes thématiques multi-pays — à compléter manuellement)
- Colonnes Environnement, Espèces, Saison, Horaires, Site web : vides, à remplir progressivement

### Import dans NocoDB

1. Créer une nouvelle table → "Import from CSV" → glisser le fichier
2. Reconfigurer les types de colonnes après import :
    - Multi-select : Classe, Environnement, Espèces observées, Saison idéale
    - Single select : Pays, Statut
    - URL : Lien Google Maps, Site web

---

## Configuration NocoDB

### Vue carte

1. Cliquer **"+"** à côté de "Grid view" → choisir **"Map"**
2. Sélectionner le champ Adresse ou Coordonnées GPS
3. Les lieux apparaissent comme marqueurs

### Types de champs

Pour convertir un champ : cliquer sur l'en-tête de colonne → "Customize field type" → choisir le type souhaité. Airtable/NocoDB crée automatiquement les options multi-select à partir des valeurs existantes.

---

## Maintenance future

- **Nouveaux lieux** : ajouter directement dans NocoDB, ou refaire un Takeout et passer le fichier à [[Claude]] pour un diff sans doublons
- **Classification** : remplir Environnement, Espèces, Saison au fil des sorties terrain
- **Limite** : 1 000 lignes en gratuit cloud (644 actuellement, marge de 356)