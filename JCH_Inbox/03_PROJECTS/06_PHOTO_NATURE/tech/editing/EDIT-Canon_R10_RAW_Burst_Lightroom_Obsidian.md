---
tags:
  - type/project
  - status/active
---
# Canon R10 — RAW Burst et Lightroom

[[IMAGE EDIT]]

## Question de départ
Comment ouvrir dans Lightroom les fichiers issus du mode **RAW Burst** du **Canon R10** ?

## Conclusion courte
Les fichiers **RAW normaux (.CR3)** du Canon R10 peuvent être importés directement dans Lightroom, à condition d’utiliser une version compatible.

Les fichiers issus du **mode RAW Burst** ne sont **pas pris en charge directement** par Lightroom.  
Il faut d’abord les ouvrir dans **Canon Digital Photo Professional (DPP)**, puis **extraire les images utiles** en fichiers individuels avant de les importer dans Lightroom.

---

## Points essentiels

### 1. Différence entre RAW normal et RAW Burst
- **RAW normal** : import direct possible dans Lightroom.
- **RAW Burst** : le boîtier enregistre une **séquence entière dans un seul fichier CR3 “roll”**.
- Lightroom ne sait pas exploiter directement ce type de fichier “roll”.

### 2. Solution correcte
Passer par **Canon DPP** pour :
- ouvrir le fichier RAW Burst,
- visualiser les images contenues dans la séquence,
- extraire une ou plusieurs images,
- sauvegarder les vues choisies en fichiers individuels,
- importer ensuite ces fichiers dans Lightroom.

---

## Réponse sur le batch dans DPP

### Oui, mais avec limite
Dans **DPP**, le **RAW Burst Image Tool** permet de travailler **par lot à l’intérieur d’un seul roll** :
- extraire une image unique,
- extraire une plage d’images,
- sauvegarder séparément toutes les images d’une plage.

### Limite importante
Il ne semble pas y avoir de véritable traitement **batch global sur plusieurs fichiers RAW Burst simultanément**.  
Le traitement est surtout prévu **roll par roll**.

---

## Workflow recommandé sur Mac

### Organisation des dossiers
Créer un dossier principal, par exemple :

`Photos/2026-04-18_R10_RAWBurst/`

Avec trois sous-dossiers :
- `01_Rolls`
- `02_Extracted_CR3`
- `03_Rejected`

### Procédure
1. Copier tous les fichiers RAW Burst d’origine dans `01_Rolls`.
2. Ouvrir ce dossier dans **Canon DPP**.
3. Repérer les rolls intéressants.
4. Ouvrir un roll utile.
5. Lancer **Tools > [[Start]] RAW Burst Image Tool**.
6. Parcourir rapidement la séquence.
7. Définir le début et la fin de la plage intéressante.
8. Utiliser **Save a Range of Images Separately**.
9. Enregistrer les fichiers extraits dans `02_Extracted_CR3`.
10. Importer `02_Extracted_CR3` dans Lightroom.

---

## Conseil pratique
Le plus efficace n’est pas d’extraire immédiatement une seule image “parfaite”, mais plutôt :
- extraire une **courte plage utile** autour du meilleur moment,
- faire ensuite la sélection finale dans Lightroom.

Exemple :
- garder 5 à 12 vues autour du moment fort,
- comparer ensuite netteté, attitude, regard, ailes, posture, etc. dans Lightroom.

---

## Méthode de tri conseillée
- **Roll sans intérêt** : ne pas ouvrir ou classer en rejet.
- **Roll potentiellement bon** : ouvrir dans DPP.
- **Dans le roll** : extraire uniquement une plage serrée.
- **Dans Lightroom** : faire le tri qualitatif final et le développement.

---

## Conclusion finale
Le meilleur flux de travail est :

**RAW Burst Canon R10 → DPP → extraction des images utiles en CR3 individuels → import dans Lightroom**

DPP sert d’outil d’ouverture et d’extraction.  
Lightroom sert au tri fin, à l’édition et à l’archivage.
