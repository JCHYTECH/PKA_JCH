HT-MT_TARGETING_STRATEGY.md

[[energy-intelligence]] [[prospection-industrielle]] [[ht-mt]]

Contexte

Le projet vise à identifier et qualifier des sociétés industrielles ou tertiaires à forte consommation énergétique afin de leur proposer des solutions destinées à optimiser et piloter leurs coûts énergétiques.

Le critère technique principal de ciblage est la présence probable ou certaine d’une cabine Haute Tension (HT) ou Moyenne Tension (MT), indicateur fort :

* de puissance électrique importante,
* de complexité énergétique,
* de potentiel d’optimisation,
* et de capacité d’investissement.

L’objectif n’est pas d’obtenir une liste officielle des cabines HT/MT, généralement non publique, mais de construire une base de données probabiliste fiable par croisement de multiples sources indirectes.

⸻

Objectifs du Projet

Objectif principal

Créer une base de données géographique et commerciale des entreprises ayant :

* une cabine HT/MT probable,
* une forte intensité énergétique,
* un potentiel commercial élevé.

Objectifs secondaires

* Détecter les consommateurs énergétiques importants.
* Identifier les entreprises sensibles à l’optimisation énergétique.
* Construire un système de scoring énergétique et commercial.
* Développer un pipeline OSINT automatisé.
* Prioriser les prospects à haute valeur.

⸻

Architecture Générale du Projet

Couche 1 — Géographie

Objectif :
Identifier les sites industriels et infrastructures électriques.

Technologies :

* [[PostgreSQL]] + PostGIS
* QGIS
* OpenStreetMap
* Orthophotos IGN

⸻

Couche 2 — Détection Électrique

Objectif :
Détecter les indices de présence HT/MT.

Sources :

* OSM
* Permis
* Documents ORES/RESA/Elia
* Orthophotos

⸻

Couche 3 — Intelligence Économique

Objectif :
Qualifier la capacité financière et énergétique.

Sources :

* BCE
* BNB
* Graydon
* Rapports ESG

⸻

Couche 4 — Intelligence Commerciale

Objectif :
Prioriser la prospection.

Résultat :
Scoring global.

⸻

Classification des Sources d’Information

⸻

CLASSE A — CERTITUDE TRÈS ÉLEVÉE

Valeur Informationnelle

90–100%

Ces sources indiquent quasi explicitement la présence d’une cabine HT/MT.

⸻

1. Permis mentionnant explicitement une cabine HT/MT

Mots-clés :

* cabine haute tension
* cabine moyenne tension
* poste transformation
* cellule MT
* transformateur 15 kV
* poste client

Sources :

* permis urbanisme
* permis unique
* enquêtes publiques
* commodo/incommodo

Indicateur :
CERTITUDE TRÈS ÉLEVÉE

⸻

2. Documents ORES / RESA / ELIA

Exemples :

* demande raccordement MT
* mise sous tension cabine client
* renforcement raccordement
* augmentation puissance > 56 kVA
* raccordement > 1 MVA

Indicateur :
CERTITUDE TRÈS ÉLEVÉE

⸻

3. Marchés publics techniques

Mots-clés :

* maintenance cabine HT
* remplacement transformateur
* tableau général HT
* cellule moyenne tension
* groupe électrogène industriel

Indicateur :
TRÈS ÉLEVÉ

⸻

4. Annonces immobilières industrielles

Mots-clés :

* cabine HT
* cabine privée
* puissance disponible
* transfo 630 kVA
* raccordement 15 kV

Indicateur :
TRÈS ÉLEVÉ

⸻

CLASSE B — PROBABILITÉ ÉLEVÉE

Valeur Informationnelle

70–90%

Ces indices corrèlent fortement avec une alimentation MT.

⸻

1. Installations photovoltaïques industrielles

Indicateurs :

* 250 kWc
* 500 kWc
* 1 MWc

Sources :

* permis PV
* certificats verts
* études d’incidence

⸻

2. Bornes HPC / Recharge Poids Lourds

Indicateurs :

* Ionity
* Tesla Supercharger
* Electra
* Fastned

Probabilité :
ÉLEVÉE

⸻

3. Industrie lourde ou continue

Secteurs :

* agroalimentaire
* métallurgie
* froid industriel
* chimie
* data centers
* logistique automatisée

⸻

4. Présence groupe électrogène industriel

Signaux :

* UPS
* redondance électrique
* continuité activité

⸻

5. Sites Seveso

Sources :

* plans d’urgence
* rapports sécurité
* documentation publique

⸻

CLASSE C — INDICES MOYENS

Valeur Informationnelle

40–70%

Indices indirects nécessitant croisement.

⸻

1. Taille importante des bâtiments

Indicateurs :

* 10 000 m²
* entrepôts
* production

Sources :

* orthophotos
* cadastre
* OSM

⸻

2. Zonings industriels

Indices :

* puissance disponible
* alimentation 15 kV
* proximité poste source

⸻

3. Immobilisations corporelles élevées

Source :

* BNB

Corrélation :
machines énergivores.

⸻

4. Activité 24/7

Indices :

* éclairage nocturne satellite
* trafic logistique
* froid continu

⸻

5. Taxes industrielles communales

Indices :

* force motrice
* matériel industriel
* outillage

⸻

CLASSE D — INDICES FAIBLES MAIS UTILES

Valeur Informationnelle

10–40%

Utiles uniquement dans un système de scoring multi-source.

⸻

1. Rapports ESG

Indices :

* ISO 50001
* réduction CO₂
* stratégie énergétique

⸻

2. Recrutement spécialisé

Postes :

* energy manager
* facility manager
* responsable maintenance

⸻

3. Communication marketing

Mots-clés :

* transition énergétique
* optimisation énergétique
* smart factory

⸻

4. Études immobilières ou logistiques

Indices :

* chambres froides
* automatisation
* HVAC massif

⸻

Système de Scoring Recommandé

Indice	Score
Cabine HT explicite	+50
Demande raccordement MT	+40
>1 MVA	+60
PV >1 MW	+40
Industrie lourde	+30
Groupe électrogène	+25
Site Seveso	+30
Immobilisations élevées	+20
Zoning industriel	+15
Activité 24/7	+15

⸻

Pipeline Technique

Étape 1 — Base Géographique

Créer :

* [[PostgreSQL]]
* PostGIS

Importer :

* OSM
* zonings
* orthophotos

⸻

Étape 2 — Scraping Documentaire

Technologies :

* [[Python]]
* BeautifulSoup
* Scrapy
* OCR PDF

Objectif :
extraire :

* noms entreprises
* adresses
* puissance
* tension
* indices techniques

⸻

Étape 3 — Géocodage

Transformer :

* adresses
* permis
* documents

en :

* coordonnées GPS.

⸻

Étape 4 — Scoring

Créer :

* HT_MT_probability_score

Classes :

* 0–40 : faible
* 40–60 : possible
* 60–80 : probable
* 80–100 : quasi certain

⸻

Étape 5 — Interface de Prospection

Fonctions :

* carte interactive
* filtres
* exports CRM
* suivi commercial

Technologies :

* QGIS
* Metabase
* Superset
* Leaflet

⸻

Compétences Nécessaires

* GIS / QGIS
* [[PostgreSQL]]/PostGIS
* [[Python]] scraping
* OCR PDF
* OSINT
* Analyse énergétique
* Data engineering léger

⸻

Vision Long Terme

Le projet peut évoluer vers :

* plateforme d’intelligence énergétique territoriale,
* scoring automatisé,
* surveillance continue des nouveaux raccordements,
* détection automatique des investissements énergétiques,
* IA satellite de détection des cabines,
* outil de prospection prédictive.

L’objectif final n’est pas simplement de détecter des cabines HT/MT.

L’objectif final est de construire une cartographie dynamique des entreprises énergétiquement stratégiques.

