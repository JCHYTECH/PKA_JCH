# 09_PRODUCT_SHEETS — Fiches produit WildNexus

> Créées le 2026-06-19 ; revue de cohérence P0 le 2026-11-05.
> Les fiches P1/P2 décrivent une vision, pas des produits développés ou validés.

## 1. Gamme documentaire

| # | Fiche | Produit | Phase | Tarification |
|---|-------|---------|-------|--------------|
| F1 | [F1_FIELD.md](F1_FIELD.md) | WildNexus FIELD | Prototype P0 | À définir après BOM et coût complet |
| F2 | [F2_FIELD_PLUS.md](F2_FIELD_PLUS.md) | WildNexus FIELD+ | Vision P1 | Non validée |
| S1 | [S1_STATION.md](S1_STATION.md) | WildNexus STATION | Vision P1 | Non validée |
| S2 | [S2_STATION_PLUS.md](S2_STATION_PLUS.md) | WildNexus STATION+ | Vision P1+ | Non validée |
| A1 | [A1_NEXUS_ACOUSTIC.md](A1_NEXUS_ACOUSTIC.md) | Nexus Acoustic | Vision P1 / projet associé | Non validée |

Les prix historiques des fiches P1/P2 ne constituent pas des offres. Pour le FIELD, JCH a explicitement retiré le prix 149–179 € et la marge de 40 % le 2026-11-05.

## 2. P0 et gateway

Le FIELD pourra enregistrer seul sur SD. Pour recevoir des alertes LoRa, une gateway compatible doit exister dès le départ :

```
FIELD seul → captures + extraction SD
FIELD + gateway P0 → alertes, métadonnées et journal local
FIELD + STATION P1 → administration et dashboard autonomes envisagés
```

La gateway minimale de développement appartient au P0. La STATION commerciale décrite dans S1 reste en P1 ; ses 50 nœuds, fonctions de dashboard, prix et BOM ne sont pas validés.

## 3. Principes partagés — intentions, pas certifications

- **Firmware MIT + politique éthique :** direction actée le 2026-11-05. `ETHICS.md` ne restreint pas automatiquement les permissions MIT en aval ; hardware, documentation, modèles, données et marque ont des règles à préciser.
- **Local-first :** pas de cloud obligatoire dans la cible P0, médias sur SD, métadonnées LoRa et exports locaux.
- **Formats documentés :** JSON/WAV et cible Camtrap-DP ; leur compatibilité réelle se prouve sur des fichiers produits par le nœud.
- **LoRa EU868 P2P :** pas de réseau public requis dans l'architecture cible ; gateway, temps d'air, couverture et conformité restent à valider.
- **Payload 48 octets :** contrat ADR-014 testé sur hôte, pas preuve de portée ou de livraison.
- **Confidentialité par conception :** détection humaine locale, suppression ou floutage selon ADR-010, SD chiffrée au terrain et procédure d'accès. La conformité RGPD n'est pas acquise tant que les mesures, la base légale et les procédures ne sont pas validées.
- **Aucun média par LoRa :** images et clips restent sur SD ou utilisent un transport distinct validé.

## 4. État des fonctionnalités au 2026-11-05

| Fonctionnalité | Fiche | État réel |
|----------------|-------|-----------|
| Capture OV5640 jour/nuit | F1 | Matériel reçu ; SOP-08/CAM-02 à exécuter |
| IA animal/non-animal et humaine | F1 | Modèle non validé ; dataset et benchmark ADR-010 requis |
| Audio stéréo et WAV | F1 | Contrats et tests hôte ; interface des micros reçus et capture réelle à confirmer |
| Alerte LoRa de bout en bout | F1 + gateway P0 | Codec hôte ; radio, parser et journal à valider |
| Autonomie 60 jours | F1 | Cible WP03 non démontrée |
| Boîtier IP67 | F1 | Cible de conception non testée |
| STATION commerciale | S1 | Vision P1, non développée comme produit P0 |
| IA espèces, BirdNET-Lite, InsectNet-CNN, AmphibianNet | F2/S2/A1 | Fonctions P1/P2 ou projets associés ; aucune capacité n'est transférée automatiquement au P0 |
| LTE-M et transfert de médias à distance | F1/S1 | Option P1 ; extraction SD ou Wi-Fi local à valider en P0 |

Les fiches P1/P2 n'ont pas fait l'objet de la même revue technique que F1. Elles ne doivent pas servir de source d'état ou de preuve commerciale sans une revue dédiée.

## 5. Références

- [Scope lock P0 v0.5](WILDNEXUS_P0_SCOPE_LOCK.md)
- [Index des ADR](WILDNEXUS_ADR_INDEX.md)
- [État des protocoles](JCH_Inbox/03_PROJECTS/03_WILDNEXUS/WILDNEXUS_DEVICE/03_P0_ENGINEERING/PROTOCOLES/progress.md)
- [Budget P0](WILDNEXUS_P0_BUDGET_RANGE.md)
- [BOM et procurement](../03_P0_ENGINEERING/07_PROCUREMENT_BOM/)
- [Usage matrix](wildnexus-usage-matrix.md)
- [Vision initiale](MASTER_ARCHITECTURE_WN.md), document de cadrage historique

---

*Révision 2026-11-05 : tarification FIELD retirée, gateway P0 distinguée de la STATION P1, MIT/éthique clarifiés et performances non prouvées requalifiées.*
