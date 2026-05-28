# Document Unique de Projet : Faune Autour - Radar de Biodiversité Acoustique

**Version :** 1.0 (Consolidée)
**Date :** 15 Mai 2026
**Préparé par :** Analyse IA (à valider par JC)
**Référence :** Fusion des documents `Faune_Autour_Acoustic_Project_Report.md` et `faune_autour_report_UI.md`

---

## 1. Résumé Exécutif (Décisionnel)

- **Le Problème :** L'application Faune Autour actuelle est une PWA statique qui ne fait que « deviner » les espèces (données GBIF). Elle ne capte pas la réalité du terrain.
- **La Solution :** Créer un **système de détection acoustique** (station + plateforme) qui prouve ce qui est vraiment présent, en commençant par les oiseaux.
- **Le Choix Stratégique (Primordial) :** On **ne réécrit pas** l'application existante. On la **transforme** en un client riche (frontend) qui communique avec une **nouvelle API backend** robuste. La PWA actuelle devient l'interface du nouveau système.
- **Le Premier Jalon (Indépassable) :** Dans 6 mois, une station fixe (jardin de JC) envoie des détections d'oiseaux à un serveur, et le dashboard (amélioration de la PWA actuelle) les affiche. *C'est tout. C'est le seul objectif.*
- **Valeur Clé :** Passer de « quelles espèces sont théoriquement possibles ? » à « quelles espèces sont réellement actives maintenant ? ».

---

## 2. Décision Fondamentale : Point de Départ Unique

> **Décision :** Le projet part de l'**existant** (la PWA statique du Fichier 2) et le **transforme**. On ne reconstruit pas de zéro.

- **Conséquence :** Le développeur frontend ne réécrit pas la carte et la liste. Il les enrichit pour qu'elles appellent la nouvelle API.
- **Conséquence :** Le développeur backend construit une API qui est **compatible** avec le format de données attendu par la PWA actuelle, tout en y ajoutant les nouvelles fonctionnalités (détections, scoring).
- **Règle de gestion :** Toute tâche qui suggère de « refaire » l'interface utilisateur existante est **bloquée** et doit être justifiée.

---

## 3. Périmètre Strict (MoSCoW) - Priorité "Fermée"

Cette section est un contrat. Tout ajout non listé ici est **hors périmètre** jusqu'à la prochaine revue de phase.

### Must Have (Pour le jalon des 6 mois - *Le système est utilisable*)

- **F-MVP-01 :** La station RPi (fixe, secteur, Wi-Fi) exécute BirdNET-Go 24h/24.
- **F-MVP-02 :** Le RPi stocke les détections localement ([[SQLite]]) et les envoie au serveur dès que le réseau est disponible.
- **F-MVP-03 :** L'API backend reçoit, stocke ([[PostgreSQL]] + PostGIS) et expose les détections.
- **F-MVP-04 :** Le dashboard (PWA enrichie) affiche la carte avec la position de la station, une liste des dernières détections avec le score de confiance, et une timeline.
- **NF-MVP-01 :** Fiabilité : le système redémarre automatiquement après une coupure.
- **NF-MVP-02 :** Données Audio : AUCUN fichier audio brut n'est envoyé au serveur par défaut (seulement les métadonnées).

### Should Have (Pour la Phase 2 - *Le système devient intéressant*)

- **F-P2-01 :** Connexion à l'API eBird pour une meilleure fraîcheur des données "attendues" (oiseaux uniquement).
- **F-P2-02 :** Introduction d'un statut de validation « Unverified » / « Verified » (manuel, par JC pour l'instant).
- **F-P2-03 :** Une page simple "Comparaison" : espèces détectées vs espèces eBird à cet endroit.
- **NF-P2-01 :** Scalabilité : Le backend doit pouvoir gérer 10 stations simultanément sans ralentissement.

### Could Have (Future / Hors périmètre pour l'instant)

- Intégration GBIF / iNaturalist.
- Validation experte automatisée.
- Version batterie / 4G / solaire.
- Multi-taxon (bats, amphibiens).
- Fonction "Photographe".

### Won't Have (Ce qu'on ne fera PAS)

- Développer une application native iOS/Android (la PWA suffit).
- Entraîner un modèle IA personnalisé (on utilise [[BirdNET]] tel quel).
- Créer un réseau public de stations avant la validation scientifique.

---

## 4. Architecture Technique (Simple & Claire)
