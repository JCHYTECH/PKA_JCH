# ADR-013 — Format données et protocole transmission (payload LoRa)

**Date :** 2026-06-12  
**Statut :** proposé  
**Owner PKA :** [[Forge]] + [[Chouette]]  
**Agent WildNexus :** `wildnexus-rf-propagation` + `wildnexus-firmware-ulp`  
**Jalon :** M-02 — Prototype banc  

## Contexte

ADR-003 a défini le choix radio (LoRa EU868 P2P SX1262) et esquissé un format de paquet uplink « ~50 octets ». Ce format n'a jamais été spécifié formellement, ce qui bloque :
- l'implémentation firmware du codec paquet ;
- le parser côté gateway/station de base ;
- l'interopérabilité entre le nœud caméra et le dashboard PKA.

Le canal LoRa impose des contraintes fortes : duty cycle EU868 1%, SF7 → ~50 octets utiles par paquet, transmission événementielle uniquement (pas d'image). Le format doit être compact, extensible et auto-descriptif.

## Décision proposée

### 1. Structure du paquet uplink (nœud → base)

Paquet binaire compact, longueur fixe **48 octets** (padding à 48 si nécessaire), organisé en sections :

| Offset | Taille | Champ | Type | Description |
|--------|--------|-------|------|-------------|
| 0 | 1 | Version | u8 | Version du protocole (0x01 = v1) |
| 1 | 1 | Flags | u8 | Bitfield : bit0=ack_request, bit1=low_battery, bit2=sd_full, bit3=ia_failed, bits4-7=reserved |
| 2 | 4 | Node ID | u32 | Identifiant unique du nœud (dérivé MAC ou provisionné) |
| 6 | 4 | Timestamp | u32 | Unix timestamp UTC de l'événement |
| 10 | 1 | Event type | u8 | 0x01=motion, 0x02=schedule, 0x03=test, 0x04=diagnostic |
| 11 | 1 | IA score | u8 | Score de confiance animal 0–100 (0=pas d'inférence, 255=erreur IA) |
| 12 | 1 | IA class | u8 | Classe prédite : 0=non-animal, 1=mammifère, 2=oiseau, 3=humain, 4=indéterminé, 255=N/A |
| 13 | 2 | Battery mV | u16 | Tension batterie en mV (ex: 5800 = 5.8V pour 8×AA) |
| 15 | 2 | Storage count | u16 | Nombre d'images sur microSD |
| 17 | 1 | Temperature | i8 | Température interne boîtier en °C (offset −40) |
| 18 | 2 | Uptime | u16 | Uptime depuis dernier boot en heures |
| 20 | 4 | Image hash | u32 | 4 premiers octets du SHA-256 de l'image associée (pour requête downlink) |
| 24 | 8 | Reserved | — | Réservé pour extensions futures (padding zéro) |
| 32 | 4 | RSSI (node) | i32 | Dernier RSSI mesuré par le nœud (downlink précédent) ou 0 |
| 36 | 4 | SNR (node) | i32 | Dernier SNR mesuré par le nœud ou 0 |
| 40 | 2 | Frame counter | u16 | Compteur incrémental, remet à 0 après reboot |
| 42 | 2 | CRC-16 | u16 | CCITT CRC-16 sur octets 0–41 |
| 44 | 4 | Padding | — | Zéro — alignement 48 octets |

**Taille totale : 48 octets** — compatible SF7 (~50 octets utiles max), laisse 2 octets de marge pour l'en-tête RadioLib.

### 2. Paquet downlink (base → nœud)

Paquet compact **16 octets**, émis uniquement sur commande utilisateur :

| Offset | Taille | Champ | Type | Description |
|--------|--------|-------|------|-------------|
| 0 | 1 | Version | u8 | Version protocole (0x01) |
| 1 | 1 | Command | u8 | 0x01=upload_image, 0x02=ping, 0x03=config_update, 0x04=reboot |
| 2 | 4 | Target timestamp | u32 | Timestamp de l'image ciblée (pour upload_image) |
| 6 | 4 | Target hash | u32 | 4 premiers octets SHA-256 image (confirmation) |
| 10 | 2 | Parameter | u16 | Paramètre dépendant de la commande |
| 12 | 2 | CRC-16 | u16 | CCITT CRC-16 sur octets 0–11 |
| 14 | 2 | Padding | — | Zéro — alignement 16 octets |

### 3. Règles de transmission

- **SF7 par défaut** — portée ~500 m–1 km en forêt, duty cycle confortable.
- **SF12 fallback** — automatique si pas d'ACK downlink dans les 60s (3 tentatives max).
- **Duty cycle** : respect strict EU868 1%. Le firmware doit espacer les TX selon la formule `Toff = Tair × 99` (SF7: ~5s, SF12: ~100s). Une file d'attente FIFO de 16 événements maximum permet de lisser les rafales.
- **ACK optionnel** : flag `ack_request` à 1 si le nœud attend une confirmation. La base répond en downlink dans la fenêtre RX1 (1s après TX).

### 4. Extensibilité

- Le champ `Version` (offset 0) permet de faire évoluer le format sans casser la rétrocompatibilité.
- Les 8 octets `Reserved` (offset 24–31) sont disponibles pour de futurs champs (GPS, humidité, compteur PIR).
- L'ajout de capteurs (via ADR-008) utilisera ces octets réservés ou justifiera un bump de version.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| Format binaire compact (48 octets) | Déterministe, faible temps d'air, parseur simple | Peu lisible sans outil | **Retenu** |
| JSON texte | Lisible, auto-descriptif | 100–200 octets minimum → SF10 obligatoire → duty cycle ×4 | Rejeté — impact autonomie |
| Protobuf | Compact, schéma | Dépendance bibliothèque, complexité firmware ESP32 | P1 si besoin complexité |
| Pas de format formel | Rapidité proto | Non interopérable, dette technique | Rejeté |

## Conséquences

- Le firmware WP03 doit implémenter le codec binaire (encode uplink, decode downlink).
- Le parser gateway (Python) doit décoder les paquets et les pousser vers le dashboard PKA.
- Le dashboard doit afficher les champs en clair (node ID, IA score, batterie, etc.).
- Le `Frame counter` permet de détecter les paquets manquants (duty cycle saturation, collision).

## Sources

- ADR-003 (choix radio LPWAN)
- ETSI EN 300 220 — duty cycle EU868
- RadioLib SX1262 packet format

## Prochaine action

1. [[Forge]] implémente le codec firmware (C, ESP-IDF)
2. [[Chouette]] valide le format sur le terrain simulé (banc M-02)
3. Intégration dashboard PKA après validation M-02
