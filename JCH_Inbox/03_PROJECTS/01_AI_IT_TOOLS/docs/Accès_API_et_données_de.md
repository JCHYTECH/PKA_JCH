# Accès API et données de biodiversité

**Created:** 2026-04-09  
**Updated:** 2026-04-09  
**Messages:** 6

---

## Human
*2026-04-09 07:09*

voici reponse

Dear Jean-Claude Havaux,
Thank you for your interest in our API.
We publish our open biodiversity data via GBIF (Global Biodiversity Information Facility), which offers free and well-documented API access. You can find more information and access the data here: 👉 https://observation.org/pages/gbif
Our internal API is currently intended for use in our own applications and for business partners involved in funded projects. While we appreciate the broad interest, we are unable to offer general external access at this time.
If you are requesting access as part of a partnership or a funded project, please include details about the project, its objectives, and any relevant partners or funding sources. We will review such requests on a case-by-case basis.


Kind regards, Nicoliene from Observation.org
Observation.org is available to everyone for free 💌 Donate and support Observation.org

---

## Assistant
*2026-04-09 07:09*

JC, voici ce que je retiens de cette réponse d'Observation.org :

En résumé, leur API interne n'est pas ouverte au public — elle est réservée à leurs propres applications et à des partenaires dans le cadre de projets financés. Par contre, ils redirigent vers **GBIF** pour accéder aux données de biodiversité via une API gratuite et bien documentée.

Ils laissent toutefois une porte ouverte : si tu présentes ta demande dans le cadre d'un **partenariat ou projet financé**, avec objectifs et partenaires clairement décrits, ils examineront au cas par cas.

**Deux pistes concrètes :**

1. **Explorer l'API GBIF** — elle est gratuite et couvre un énorme volume de données d'observation. Pour tes besoins en photographie wildlife (repérage d'espèces, localisation, saisonnalité), ça peut déjà être très utile. Tu veux que je regarde ce que GBIF propose exactement via leur API ?

2. **Reformuler ta demande** en mettant en avant un projet structuré (par exemple lié à JCHYTECH, à la conservation, ou à un projet photo-scientifique) pour tenter d'obtenir l'accès à leur API interne.

Tu veux qu'on creuse l'une de ces pistes ?

---

## Human
*2026-04-09 07:10*

1

---

## Assistant
*2026-04-09 07:10*

Je vais explorer ce que l'API GBIF propose concrètement.
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Voici un tour d'horizon complet de ce que GBIF peut t'offrir, JC.

## L'API GBIF — ce qu'elle couvre

L'API est organisée en plusieurs sections : **Species** (recherche et identification d'espèces), **Occurrence** (observations géoréférencées indexées par GBIF), **Registry** (datasets, organisations) et **Maps** (cartographie).

### Ce qui est directement utile pour la photo wildlife :

**1. Recherche d'espèces par nom**
Tu peux interroger l'API avec un nom scientifique ou vernaculaire et obtenir la clé taxonomique (taxonKey) correspondante. Par exemple, `https://api.gbif.org/v1/species/match?name=Passer domesticus` retourne un identifiant unique (usageKey) pour le moineau domestique, utilisable ensuite dans toutes les autres requêtes.

**2. Recherche d'observations par zone géographique**
L'API Occurrence permet de filtrer par coordonnées GPS, pays, année, altitude, et bien d'autres paramètres. On peut chercher par latitude/longitude, par pays, par collecteur, par dataset, et combiner tous ces filtres.

**3. Accès aux médias (photos)**
Les résultats d'occurrence incluent souvent des liens vers des photos associées aux observations — paramètre `mediatype` dans la recherche.

**4. Téléchargements massifs**
Les téléchargements sont disponibles en trois formats principaux : Simple, Darwin Core Archive et Species List, accessibles via le site web, l'API, ou via les bibliothèques rgbif (R) et pygbif (Python).

**5. Client Python : pygbif**
pygbif est un package Python qui encapsule l'API GBIF pour accéder aux métadonnées, noms d'espèces et occurrences directement depuis Python. C'est probablement la voie la plus pratique pour toi sur macOS.

### Exemples concrets d'usage pour toi :

- **"Quelles espèces d'oiseaux ont été observées dans un rayon de 20 km autour de mon terrain ?"** → Requête Occurrence avec coordonnées + filtre taxonKey sur les oiseaux (Aves, taxonKey 212)
- **"À quelle saison le martin-pêcheur est-il le plus observé en Belgique ?"** → Requête par espèce + pays BE + filtre par mois
- **"Quelles espèces rares sont signalées dans la forêt de Soignes ?"** → Requête par polygone WKT + filtre sur le statut de conservation

### Bonus belge
Une équipe belge a d'ailleurs développé **GBIF Alert**, un système open-source de notifications qui alerte automatiquement quand de nouvelles observations d'espèces ciblées apparaissent dans GBIF — ça pourrait être très utile pour suivre les espèces autour de ton terrain.

### Limites à noter
- L'API de recherche est paginée (max 300 résultats par page, jusqu'à 100 000 en profondeur)
- Les requêtes trop nombreuses ou rapides peuvent être limitées (erreur HTTP 429)
- Pas de données temps réel — il y a un décalage entre l'observation et l'indexation dans GBIF

---

Tu veux que je te prépare un petit script Python prêt à l'emploi avec pygbif pour chercher les observations autour de tes coordonnées ? Ou que je te fasse un résumé en .md / .docx ?

---

## Human
*2026-04-09 07:11*

python

---

## Assistant
*2026-04-09 07:13*

Je vais te préparer un script Python avec pygbif. Laisse-moi d'abord vérifier les coordonnées approximatives de ton terrain pour centrer la recherche.

Avant de créer le fichier, tu préfères le recevoir en **.md** ou **.docx** ? (Le script Python `.py` sera créé dans tous les cas, la question porte sur la documentation d'accompagnement éventuelle.)

En attendant, je lance la création du script :
```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```


```
This block is not supported on your current device yet.
```

Voilà ton script **GBIF Wildlife Scout** ! Voici comment le lancer sur ton Mac :

**Installation des dépendances :**
```bash
pip install pygbif tabulate
```

**Trois modes d'utilisation :**

1. **Mode interactif** (le plus simple) : `python gbif_wildlife_scout.py` → menu avec choix oiseaux, mammifères, recherche par espèce, saisonnalité, export CSV

2. **Ligne de commande directe** :
   - `python gbif_wildlife_scout.py --group birds --lat 50.45 --lon 4.35 --radius 20`
   - `python gbif_wildlife_scout.py --species "Alcedo atthis" --radius 30`
   - `python gbif_wildlife_scout.py --group mammals --csv export_mammiferes.csv`

3. **Les coordonnées par défaut** sont centrées sur la Belgique (50.45°N, 4.35°E). Tu peux les modifier dans le script (lignes `DEFAULT_LAT` / `DEFAULT_LON`) ou les changer en mode interactif ou via `--lat` / `--lon`.

**Ce que le script te donne :** tableau des espèces triées par fréquence d'observation, mois pics d'observation (saisonnalité), nombre de photos disponibles, dernière date d'observation, et export CSV complet. Pas besoin de clé API pour la recherche — seuls les téléchargements massifs nécessitent un compte GBIF gratuit.

---
