# ADR-006 — Boîtier IP67 P0

**Date :** 2026-06-06
**Statut :** accepté — 2026-06-06 (contraintes validées par analyse NotebookLM)
**Owner PKA :** [[Castor]] + [[Forge]]
**Jalon :** M-02 Prototype banc

## Contexte

Le nœud satellite P0 doit être déployé en milieu forestier exposé aux intempéries, fixé sur des supports d'arbre variables. Le boîtier doit protéger l'électronique, garantir l'étanchéité long terme, et permettre la maintenance terrain (remplacement piles AA, accès carte microSD).

## Contraintes non-négociables

| Paramètre | Valeur |
|---|---|
| Dimensions cibles | 150 × 100 × 60 mm |
| Volume interne minimum | 2 holders 4×AA (~15×57×57 mm chacun) + PCB + module LoRa + caméra |
| Étanchéité | IP67 (immersion 1m / 30 min) |
| Température opérationnelle | -10 °C à +45 °C |
| Fixation | Dos concave pour supports ronds de 10 à 40 cm de diamètre |
| Accès maintenance | Trappe ou face amovible sans outil ou vis quart de tour |
| Fenêtre optique | Ouverture caméra + IR LEDs avec protection transparente anti-buée |

## Décision

**Boîtier [[commercial]] modifié (type Hammond 1555) retenu pour le P0.**

L'impression 3D PETG est écartée pour le P0 : garantir l'étanchéité IP67 sur le long terme avec des assemblages imprimés est trop aléatoire sans accès à une imprimante industrielle ou à un processus de post-traitement contrôlé. Hammond ou équivalent ABS/PC offre une robustesse mécanique et des joints préformés conformes IP67 dès le catalogue.

La conception sur mesure (moulage, alu usiné) est réservée aux versions série P1+.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Boîtier Hammond 1555 (ABS) | IP67 certifié, disponible, modificable à la perceuse, prix ~15 € | Volume interne à vérifier, fixation arbre à adapter | **Retenu P0** |
| Impression 3D PETG | Sur-mesure, coût matière faible, itération rapide | Étanchéité IP67 non garantie long terme, UV dégradation | Rejeté P0 — option prototypage interne |
| Boîtier alu usiné | Robustesse max, IP68 possible, dissipation thermique | Coût élevé, délai, non adapté au volume P0 | Réservé P1+ série |
| Boîtier PVC électrique | Économique, disponible | Non certifié IP67, fixation arbre absente | Rejeté |

## Conséquences

- WP02 hardware doit valider le volume interne avec le modèle Hammond sélectionné avant commande PCB.
- Le dos du boîtier doit intégrer un système de sangle ou de vis M4 pour fixation sur tronc — à concevoir en impression 3D comme accessoire séparé.
- Prévoir un joint torique de rechange dans le kit de maintenance terrain.
- Le boîtier doit réserver un point de fixation mécanique optionnel pour panneau solaire futur (P1) sans perçage supplémentaire.

## Critère de révision

Réviser si :
- L'encombrement réel du PCB + holders AA dépasse les dimensions internes du Hammond retenu ;
- Les tests IP67 terrain (immersion, pluie prolongée) révèlent des infiltrations ;
- Le passage en série P1 justifie un moulage dédié.

## Voir aussi

- [[ADR-001-choix-mcu-p0]] — dimensions PCB dépendent du MCU
- [[ADR-002-choix-camera-ir-p0]] — fenêtre optique à adapter selon module caméra
- [[ADR-005-energie-autonomie-p0]] — holders 8×AA = contrainte volume principale
