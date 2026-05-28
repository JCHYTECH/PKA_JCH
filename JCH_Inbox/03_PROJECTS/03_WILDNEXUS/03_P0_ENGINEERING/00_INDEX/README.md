# WILDNEXUS P0 Engineering — Index

Ce dossier regroupe les documents d'ingenierie du prototype P0 par domaine technique.

## Structure

- `01_ARCHITECTURE_SYSTEME/` — architecture SAT / master / cloud, decisions de cadrage systeme.
- `02_HARDWARE_SATELLITE/` — cartes, capteurs, boitier, encombrement, matrices hardware.
- `03_ENERGIE_AUTONOMIE/` — batteries, autonomie, alimentation, modeles de consommation.
- 
- `05_IA_EDGE_CLOUD/` — repartition IA locale/cloud, vision, audio, inference.
- `07_PROCUREMENT_BOM/` — achats, shortlist, politique de procurement, risques fournisseurs.
- `08_BUDGET_MODELES/` — budgets, couts, modeles financiers P0.
- `09_BENCHMARKS_PRODUITS/` — scans marche, produits comparables, analyses de composants.
- `99_TEMPLATES_REGISTERS/` — templates, registres transversaux, supports de suivi.

## Regle de classement

Un fichier est classe selon son usage principal, pas seulement selon son sujet apparent. Exemple : une note BirdWeather peut mentionner capteurs et cloud, mais reste dans `09_BENCHMARKS_PRODUITS/` si son role est de documenter un produit comparable.

Les fichiers analyses depuis `JCH_Inbox/00_INBOX/` doivent etre deplaces, pas copies.
