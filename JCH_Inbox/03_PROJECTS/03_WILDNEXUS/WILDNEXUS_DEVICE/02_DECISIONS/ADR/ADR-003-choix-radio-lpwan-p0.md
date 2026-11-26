# ADR-003 — Choix radio / LPWAN P0

Date initiale : 2026-05-18. Révision : 2026-11-05. Statut : architecture acceptée ; validation radio ouverte. Owners : Forge + Chouette. Jalon : M-01/M-02.

## Contexte

P0 doit transmettre des alertes, métadonnées et états techniques depuis un nœud vers une gateway locale. Les images et clips audio restent sur support local : le débit LoRa et les contraintes réglementaires ne permettent pas d'en faire un transport de médias.

Le contrat binaire est défini par ADR-014 : uplink fixe de 48 octets, downlink de 16 octets. Les portées, consommations, temps d'air et débits indiqués dans d'anciens documents sont des hypothèses à calculer et mesurer, pas des caractéristiques du prototype.

## Décision

### P0 : LoRa EU868 point à point uniquement

Retenir LoRa EU868 bidirectionnel point à point, sans LoRaWAN/TTN ni abonnement cellulaire en P0. Le module cible est RAK3172/SX1262, sous réserve de confirmation de son interface, de sa disponibilité, de sa documentation et du contenu du panier. Murata Type 1SJ reste une alternative à évaluer, non un remplacement déjà validé.

L'ESP32-S3 n'implémente qu'une interface radio P0. Le mapping SPI/UART/GPIO et la bibliothèque sont confirmés contre le module réel avant câblage ; les exemples historiques de GPIO ne sont pas un schéma approuvé.

Flux :

- uplink nœud → gateway : événement caméra ou spectral, horodatage, identifiant et données techniques ADR-014 ;
- downlink gateway → nœud : commande de 16 octets ADR-014 ;
- aucun média dans ces paquets ; une demande de fichier utilise un transport local distinct validé.

La stratégie initiale est SF7 avec adaptation seulement après mesures de liaison. Les cibles de portée en forêt et les volumes à SF7–SF12 doivent être établis par configuration radio, calcul de temps d'air et essais SOP-07. Le respect des limites réglementaires applicables — dont les contraintes de duty cycle selon le canal — prime sur la file d'attente logicielle.

### Gateway minimale P0

La gateway de développement est indispensable à la preuve WP05 : second contrôleur/module LoRa, réception, décodage caméra/spectral, journal persistant et remontée des erreurs. Son coût et ses composants sont réconciliés dans le BOM avant achat.

La STATION avec Raspberry Pi, dashboard et services commerciaux est une vision P1. Elle n'est pas nécessaire pour démontrer le contrat radio minimal, mais l'absence de STATION ne dispense pas de la gateway P0.

### P1 : LTE-M à la demande

Une option SIM7080G/LTE-M est conservée comme vision P1 pour récupérer un média à la demande. Elle n'est ni montée ni engagée en P0. Sa couverture, son offre SIM, sa consommation et son intégration seront réévaluées au moment de cette évolution. Aucune affirmation d'impact négligeable sur l'autonomie de 60 jours n'est retenue sans mesure du système complet.

## Alternatives

| Option | Statut | Motif |
|---|---|---|
| LoRa EU868 P2P seul | Retenu P0 | Simplicité, alertes compactes, pas de dépendance cellulaire |
| LoRa + LTE-M à la demande | P1 | Médias à distance, mais seconde radio et consommation/complexité supplémentaires |
| LoRaWAN/TTN | Écarté P0 | Dépendance et stack non nécessaires à la preuve initiale |
| NB-IoT/LTE-M seul | Écarté P0 | Couverture/débit au prix d'une autre architecture énergie/service |
| Mesh LoRa | Écarté P0 | Collisions, relayage, consommation et complexité |
| Wi-Fi seul | Transport local possible, pas radio terrain P0 | Portée et infrastructure différentes |

## Conséquences

- WP02/WP05 ne prévoient qu'une radio LoRa en P0 ; l'empreinte LTE-M n'est pas une obligation matérielle.
- WP04 implémente le contrat ADR-014 et les états d'erreur, pas le transfert de médias.
- Le codec testé sur hôte ne prouve pas la transmission. Une gateway réelle doit recevoir et journaliser les paquets.
- Le budget WP03 inclut réveil radio, TX/RX, attente, pertes et retransmissions ; aucune portée ou autonomie n'est déduite d'une datasheet seule.
- Le scénario 96 paquets spectraux/jour + événements caméra + retries est testé pour le temps d'air et la réglementation applicable.
- La revue réglementaire du module, de l'antenne et de la puissance est requise avant terrain et avant toute industrialisation.

## Critères de validation M-02

| Test | Preuve attendue |
|---|---|
| Uplink caméra et spectral | Octets reçus et décodés par la gateway, journal conservé |
| Downlink | Commande de 16 octets reçue et interprétée ; délai mesuré sur configuration documentée |
| Liaison terrain | RSSI/SNR/pertes mesurés à distances et environnements définis ; aucune distance minimale présumée |
| Charge radio | Calculs de temps d'air et essais du scénario spectral + caméra + retries |
| Erreurs | Perte, timeout, retry, file pleine et retour au sommeil vérifiés |
| Montage final | Antenne/boîtier mesurés ; puissance et conformité revues |

## Sources à revérifier à la reprise

Datasheets Semtech SX1262 et du module retenu, documentation RadioLib/ESP-IDF effectivement utilisée, textes ETSI et règles belges/européennes applicables à la configuration. Les liens historiques restent dans les versions antérieures de cette ADR ; ils ne remplacent pas la vérification des versions et limites courantes.

## Révision

Réviser si la couverture ou le volume radio ne satisfait pas le besoin, si le module/interface change, si la gateway minimale ne suffit pas à la preuve ou si la réglementation impose une autre configuration. Le passage à LTE-M ou LoRaWAN constitue une décision P1 séparée.
