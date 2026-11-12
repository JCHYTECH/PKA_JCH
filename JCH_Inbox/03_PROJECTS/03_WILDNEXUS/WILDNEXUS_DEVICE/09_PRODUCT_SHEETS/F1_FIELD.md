# F1 — WildNexus FIELD

> Nœud caméra autonome · configuration cible P0
> Fiche technique de développement — mise à jour 2026-11-05
> Statut : prototype non commercialisé ; aucune performance terrain n'est certifiée par cette fiche

## 1. Positionnement

Le FIELD est le nœud d'observation WildNexus en cours de prototypage. Sa cible est de capturer des images jour/nuit et de courts clips audio, de filtrer les événements localement, de conserver les médias sur microSD et d'émettre des alertes de métadonnées vers une gateway LoRa.

Le fonctionnement sur carte SD ne nécessite pas de gateway. Les alertes à distance, elles, exigent une gateway compatible dès le premier déploiement connecté. Le P0 utilise une gateway minimale de développement ; la STATION commerciale autonome reste en P1.

Le produit n'est pas encore validé de bout en bout. Les éléments ci-dessous décrivent donc une architecture et des critères de réussite, non des caractéristiques acquises.

**Persona cible à valider :** naturaliste amateur, association locale, propriétaire de terrain naturel.

## 2. Configuration cible et preuves attendues

| Catégorie | Configuration ou cible P0 | État de validation |
|-----------|---------------------------|--------------------|
| MCU | ESP32-S3 avec au moins 8 MB PSRAM ; DevKit N16R8 sur le banc | Choix candidat confirmé sous réserve des gates ADR-001 ; module produit final non figé |
| Caméra | OV5640 DVP 5 MP, monture M12, optique NoIR et lentille IR-corrigée à sélectionner | Matériel reçu ; capture et optique à valider par SOP-08/CAM-02 |
| Détection | PIR Panasonic EKMB ; référence EKMB1203111 ou EKMB1303111 à rapprocher du matériel réel | Capture et portée non validées |
| IR nocturne | 4× LED 940 nm, pilotage pulsé | Câblage, courant, portée et effet sur la faune à tester |
| Audio | 2× MEMS en stéréo, WAV PCM 16 bits 16 kHz | Contrat logiciel testé sur hôte ; interface des micros TDK reçus à confirmer avant SOP-13 |
| Stockage | microSD 128 GB minimum ; images, clips WAV et sidecars JSON | Écriture, coupure et capacité réelle à valider par SOP-06 |
| Radio | LoRa EU868 P2P, module RAK3172/SX1262 prévu | Module non commandé au dernier état connu ; SOP-07 bloquée |
| Gateway P0 | Second ESP32-S3 + SX1262, réception, décodage ADR-014 et journal local | À construire et tester avec le nœud |
| Énergie | Pack 8× AA 4S2P et TPS62840 envisagés, sortie 3,3 V | SOP-10 suspendue ; tension maximale du pack, limite 6,5 V du régulateur et câblage à valider avant alimentation |
| Autonomie | Cible 60 jours au profil de référence WP03 | Non démontrée ; mesures de tous les cycles puis EVT 30 jours requises |
| Boîtier | Hammond 1555 modifié, cible IP67 | Conception à valider ; une modification ne vaut pas certification IP67 |
| IA | Alerte animal/non-animal ; détection humaine distincte ; modèle choisi par benchmark | Aucun modèle P0 validé ; latence cible inférieure à 2 s et recalls ADR-010 à mesurer |
| Configuration | BLE ou Wi-Fi local, Wi-Fi désactivé hors configuration/maintenance | SOP-12 à exécuter |
| Mise à jour | Câble en P0 ; OTA signée éventuellement en P1 | Pas d'OTA promise dans le P0 |

Les portées radio, distances de détection, durées de rétention et performances d'autonomie seront publiées uniquement avec leur protocole et leurs mesures.

## 3. Architecture de communication P0

```
FIELD ── métadonnées LoRa ──→ Gateway de développement ──→ journal / dashboard local
FIELD ←─ commandes LoRa validées ─ Gateway

Médias sur microSD
  └── extraction physique, ou Wi-Fi local de maintenance à valider
```

- Les paquets caméra et spectraux de 48 octets sont définis par ADR-014 ; ce contrat est testé sur hôte, pas encore sur une liaison radio réelle.
- Les images et les clips audio ne transitent jamais dans les paquets LoRa.
- Les commandes `upload_image` et `upload_audio_clip` sont des demandes de transfert sur un transport distinct ; elles ne prouvent pas que ce transport est implémenté.
- Le LTE-M/SIM7080G est une option P1, hors du prototype P0.
- La réception, le décodage et la journalisation par la gateway sont un livrable P0 à part entière, rattaché à WP05.

## 4. Estimation de composants — configuration listée, pas BOM de production

Les montants historiques ci-dessous ne sont ni un devis fournisseur ni un coût de production validé. Ils servent uniquement à conserver la traçabilité de la configuration initiale.

| Composant | Qté | Estimation historique | Total |
|-----------|-----|----------------------:|------:|
| ESP32-S3-WROOM-1-N8R8 | 1 | 4,00 € | 4,00 € |
| OV5640 DVP + lentille M12 basique | 1 | 8,00 € | 8,00 € |
| PIR EKMB, référence à confirmer | 1 | 18,00 € | 18,00 € |
| LED IR VSLB3940 | 4 | 0,37 € | 1,48 € |
| MEMS cible SPH0645LM4H-B, sous réserve du matériel réel | 2 | 3,00 € | 6,00 € |
| RAK3172 | 1 | 8,00 € | 8,00 € |
| TPS62840 + inducteur + passifs | 1 | 3,00 € | 3,00 € |
| Holders AA Keystone 2463 | 2 | 3,00 € | 6,00 € |
| PCB + assemblage, hypothèse non chiffrée par devis | 1 | 10,00 € | 10,00 € |
| Hammond 1555 modifié | 1 | 15,00 € | 15,00 € |
| microSD 128 GB | 1 | 15,00 € | 15,00 € |
| Câbles, joints, visserie | 1 | 5,00 € | 5,00 € |
| **Somme arithmétique de cette liste** | | | **99,48 €** |

Cette somme n'inclut pas notamment la lentille IR-corrigée de qualité, la gateway, l'assemblage et les tests réels, la certification, la logistique, la TVA, la garantie, le support ni les éventuels écarts entre composants cibles et composants reçus. Elle ne permet donc pas de calculer une marge.

**Décision JCH du 2026-11-05 :** le prix 149–179 € et la marge de 40 % sont retirés provisoirement. Le prix sera rétabli seulement après un BOM consolidé et un modèle de coût complet.

Le budget d'ingénierie P0 est suivi séparément dans `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md`.

## 5. Contenu commercial

Aucun contenu de boîte, garantie, niveau de service ou abonnement n'est figé tant que le prototype et le modèle économique ne sont pas validés.

Points d'architecture déjà actés :

- piles non intégrées à l'estimation de composants ;
- gateway nécessaire pour les alertes LoRa, mais non nécessaire à l'enregistrement local sur SD ;
- pas de cloud obligatoire pour la cible P0 ;
- pas d'abonnement cellulaire en P0 puisque le LTE-M est en P1 ;
- licence du firmware : MIT, accompagnée d'une politique éthique `ETHICS.md` ; les licences du hardware, de la documentation, des modèles et des données restent à préciser.

## 6. Intentions de différenciation

| Axe | Intention WildNexus | Preuve à produire |
|-----|---------------------|-------------------|
| Ouverture | Firmware MIT et formats documentés | Publication, notices tierces et politique éthique relues |
| Local-first | Médias sur SD, alertes sans cloud obligatoire | Essai complet nœud + gateway |
| IA locale | Filtrage sur le nœud, modèle remplaçable après benchmark | Latence, recall jour/nuit et consommation mesurés |
| Audio | Capture stéréo et descripteurs spectraux | Clips réels du nœud et compatibilité des pipelines |
| Données | JSON, WAV et cible Camtrap-DP | Exports réels et validation de schéma |
| Extensibilité | Interfaces documentées sans élargir le P0 | Revue des broches, de l'alimentation et du boîtier |

Ces intentions ne constituent pas encore une comparaison de performance ou de prix avec les pièges photographiques commerciaux.

## 7. Chemin d'adoption envisagé

```
FIELD seul → captures et récupération SD
FIELD + gateway compatible → alertes et métadonnées locales
Plusieurs FIELD + gateway → couverture multi-nœuds à tester
STATION P1 → dashboard et administration autonomes, si validés
```

La STATION ne peut plus être présentée comme un achat ultérieur obligatoire pour recevoir des alertes : une gateway doit exister dès le premier usage connecté.

---

*Références : ADR-001 (MCU), ADR-002 (caméra/IR), ADR-003 (radio), ADR-004 (stockage), ADR-005 (énergie), ADR-006 (boîtier), ADR-007 (détection), ADR-010 (confidentialité/licence), ADR-013 (audio), ADR-014 (payload), ADR-016 (cycles firmware), ADR-017 (fichiers audio). Preuves : SOP-06 à SOP-18 et matrice du scope lock v0.5.*
