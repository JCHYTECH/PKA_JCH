# WILDNEXUS P0 Engineering — Index

Ce dossier regroupe les documents d'ingénierie du prototype P0 par domaine technique.

## Structure

- `01_ARCHITECTURE_SYSTEME/` — architecture SAT / master / cloud, décisions de cadrage système.
- `02_HARDWARE_SATELLITE/` — cartes, capteurs, boîtier, encombrement, matrices hardware.
- `03_ENERGIE_AUTONOMIE/` — batteries, autonomie, alimentation, modèles de consommation.
- `04_CONNECTIVITE_MESH_LORA_LTE/` — radio, LoRa, LTE, modules de communication.
- `05_SIMULATION/` — simulation Wokwi, test harness caméra, datasets de test.
- `07_PROCUREMENT_BOM/` — achats, shortlist, politique de procurement, risques fournisseurs.
- `08_BUDGET_MODELES/` — budgets, coûts, modèles financiers P0.
- `09_BENCHMARKS_PRODUITS/` — scans marché, produits comparables, analyses de composants.
- `99_REFERENCES/` — ESP-DIVE, PPK2, datasheets, veille technologique.
- `99_TEMPLATES_REGISTERS/` — templates, registres transversaux, supports de suivi.
- `PROTOCOLES/` — SOPs M-02, progress tracker, protocoles de mesure.

## Règle de classement

Un fichier est classé selon son usage principal, pas seulement selon son sujet apparent. Exemple : une note BirdWeather peut mentionner capteurs et cloud, mais reste dans `09_BENCHMARKS_PRODUITS/` si son rôle est de documenter un produit comparable.

Les fichiers analysés depuis `JCH_Inbox/00_INBOX/` doivent être déplacés, pas copiés.
