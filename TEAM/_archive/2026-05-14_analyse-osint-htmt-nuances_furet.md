# RAPPORT DE RECHERCHE — FAISABILITÉ OSINT HT/MT
**Auteur :** [[Furet]] 🦡 (via [[Dobby]] 🦉)
**Projet :** 04_NUANCES
**Date :** 2026-05-14

## Executive Summary
L'analyse de faisabilité confirme que la construction d'une base de données probabiliste de "Certitude Élevée" est techniquement possible en croisant trois flux de données majeurs en Wallonie. Le levier le plus puissant identifié est le **Permis Unique (Classe 2)** pour les transformateurs ≥ 1 500 kVA, qui fait l'objet de publications légales systématiques.

---

## 1. Analyse des Sources Classe A (Certitude 90-100%)

### 1.1 Permis d'Environnement et Permis Uniques
**Faisabilité : ÉLEVÉE**
- **Règle :** Toute cabine avec transformateur ≥ 100 kVA est une installation classée.
- **Classe 3 (100 - 1500 kVA) :** Simple déclaration. Moins de traces publiques numériques.
- **Classe 2 (≥ 1500 kVA) :** Nécessite un **Permis Unique** avec **Enquête Publique**.
- **Extraction :** Les avis d'enquête publique sont publiés sur les sites communaux et le portail de la Wallonie (environnement.wallonie.be). Ils contiennent : nom de l'entreprise, adresse, puissance du transformateur et nature des travaux.
- **Difficulté :** Moyenne (nécessite un scraper ciblant les mots-clés "rubrique 40.10.01.01.02").

### 1.2 Marchés Publics (Maintenance et RGIE)
**Faisabilité : TRÈS ÉLEVÉE**
- **Règle :** Le RGIE (Articles 267/268) impose des visites trimestrielles obligatoires pour les installations HT.
- **Signal :** Les pouvoirs publics (communes, hôpitaux, intercommunales, écoles) publient des marchés de "Maintenance préventive et curative des cabines HT".
- **Source :** BDA (Bulletin des Adjudications) et e-Procurement.
- **Difficulté :** Faible. Les données sont structurées et les CPV (Common Procurement Vocabulary) facilitent le filtrage.

---

## 2. Analyse des Sources Classe B (Probabilité 70-90%)

### 2.1 WalOnMap et Cartographie Continue (PICC)
- **Outil :** Le Géoportail de la Wallonie.
- **Indice :** La couche topographique PICC permet de repérer des structures de type "bâtiment technique" non résidentiel sur des sites industriels.
- **Croisement :** Superposer la couche PICC avec les données de la BCE (Banque Carrefour des Entreprises) pour identifier le propriétaire du site.

### 2.2 Données GRD (ORES / RESA)
- **Accès :** Les listes de clients MT ne sont pas publiques.
- **Signal Indirect :** Le portail Open Data Wallonie-Bruxelles (ODWB) publie des consommations agrégées par secteur et zone. Utile pour identifier des "hotspots" industriels à prospecter physiquement ou via orthophotos.

---

## 3. Recommandations pour le PoC (Proof of Concept)

Je recommande à **[[Forge]] 🦦** de concentrer le PoC sur deux axes prioritaires :

1.  **Scraper e-Procurement** : Extraire tous les attributaires et demandeurs de marchés de maintenance HT sur les 24 derniers mois en Belgique. C'est la source la plus "propre" et structurée.
2.  **Monitor d'Enquêtes Publiques** : Développer un script qui surveille les occurrences de "rubrique 40.10.01" sur les plateformes de publication légale wallonnes.

## Conclusion
Le pipeline OSINT est viable. La structuration des données publiques belges, bien que fragmentée par commune, offre des points d'ancrage légaux (permis uniques et RGIE) qui permettent de contourner l'absence de liste officielle des GRD.

*Transmis à [[Corbeau]] pour archivage et à [[Forge]] pour évaluation technique.*