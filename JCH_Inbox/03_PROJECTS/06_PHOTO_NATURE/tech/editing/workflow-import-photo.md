---
date: 2026-04-18
source: note
domain: photo/photo-flow
project:
tags:
  - workflow
  - import
  - SSD
  - session
  - Canon
  - type/project
  - status/active
status: raw
---
# Workflow Import Photo

[[Equipment_JCH]]

## Vue d'ensemble

Carte SD (EOS\_DIGITAL)

    ↓

SSD TERRAIN

    ├── Sessions/nom-session/BRUTE/       ← copie 1, verrouillée (lecture seule)

    └── Sessions/nom-session/NETTOYAGE/   ← copie 2, espace de travail culling

---

## Convention de nommage des sessions

pays-lieu\_DD-MM-YYYY

ex : Belgique-Forêt-de-Soignes\_18-04-2026

---

## Prérequis

- SSD externe nommé **TERRAIN** branché en USB-C  
- Carte SD Canon nommée **EOS\_DIGITAL** insérée  
- Script `import_session.sh` installé dans `~/Scripts/`  
- Shortcut **Import Session Photo** créé dans Shortcuts.app

---

## Procédure de lancement

1. Brancher le SSD TERRAIN  
2. Insérer la carte SD EOS\_DIGITAL  
3. Lancer le Shortcut **Import Session Photo**  
4. Saisir le nom de session au format `pays-lieu_DD-MM-YYYY`  
5. Attendre la notification de fin

---

## Ce que le script fait automatiquement

1. Vérifie la présence de EOS\_DIGITAL et TERRAIN — arrêt avec notification d'erreur si absent  
2. Crée la structure de dossiers `BRUTE/` et `NETTOYAGE/`  
3. Copie la carte SD vers `BRUTE/` avec vérification checksum (rsync)  
4. Verrouille `BRUTE/` en lecture seule (`chmod 444`)  
5. Copie `BRUTE/` vers `NETTOYAGE/` avec vérification checksum  
6. Envoie une notification avec le nombre de fichiers importés

---

## Emplacement du script

\~/Scripts/import\_session.sh

Installation initiale (une seule fois) :

mkdir \~/Scripts

\# déposer import\_session.sh dans ce dossier

chmod \+x \~/Scripts/import\_session.sh

---

## Règles de travail

| Dossier | Règle |
| :---- | :---- |
| BRUTE | Ne jamais modifier — lecture seule — source de vérité |
| NETTOYAGE | Espace de culling — suppressions autorisées |

- Logiciel de catalogue maître : **Lightroom** (ou DXO PhotoLab)  
- Les autres logiciels (Luminar Neo, Topaz, Photoshop) utilisés en sortie destructive uniquement  
- Les sidecars XMP restent liés au logiciel maître

---

## Prochaine étape (à développer)

Script de transfert **TERRAIN → NAS** à la base, avec création du dossier `FINI/` et archivage froid.  
