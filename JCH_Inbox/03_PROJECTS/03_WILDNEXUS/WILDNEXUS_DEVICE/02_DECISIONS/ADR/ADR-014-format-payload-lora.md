# ADR-014 — Format données et protocole transmission (payload LoRa)

**Date :** 2026-06-12  
**Dernière mise à jour :** 2026-11-05 — Alignement stéréo, quantification firmware et preuves radio
**Statut :** accepté  
**Owner PKA :** [[Forge]] + [[Chouette]]  
**Agent WildNexus :** `wildnexus-rf-propagation` + `wildnexus-firmware-ulp`  
**Jalon :** M-02 — Prototype banc  

## Contexte

ADR-003 a défini le choix radio (LoRa EU868 P2P SX1262) et esquissé un format de paquet uplink « ~50 octets ». Ce format n'a jamais été spécifié formellement, ce qui bloque :
- l'implémentation firmware du codec paquet ;
- le parser côté gateway/station de base ;
- l'interopérabilité entre le nœud caméra et le dashboard PKA.

Le canal LoRa impose des contraintes fortes de temps d'air et de réglementation selon la configuration et le canal. La transmission est événementielle, sans image ni audio. Le format doit être compact, extensible et versionné ; le temps d'air réel sera calculé puis mesuré pour la configuration retenue.

### Gap identifié le 2026-07-05

Le payload original ne couvrait que les événements caméra (motion, schedule, test, diagnostic). ADR-013 prévoit la transmission de **features spectrales** via LoRa, mais aucun format n'était défini pour les encoder. Les clips WAV stéréo de 3 s contiennent **192 000 octets de données PCM** et sont hors de portée LoRa — récupération par Wi-Fi local ou SD physique, deux procédures restant à démontrer de bout en bout.

**Correctif :** ajout d'un type d'événement `0x05=spectral` et d'un format de payload spectral dédié, réutilisant la même structure 48 octets pour compatibilité parser.

## Décision

Le format est accepté comme contrat d'interface. Son acceptation ne prouve ni la portée radio ni la chaîne de bout en bout : celles-ci exigent SOP-07 et un parser de gateway P0.

### 1. Structure du paquet uplink — Événements caméra (Event type 0x01–0x04)

Paquet binaire compact, longueur fixe **48 octets** (padding à 48 si nécessaire), organisé en sections :

| Offset | Taille | Champ | Type | Description |
|--------|--------|-------|------|-------------|
| 0 | 1 | Version | u8 | Version du protocole (0x01 = v1) |
| 1 | 1 | Flags | u8 | Bitfield : bit0=ack_request, bit1=low_battery, bit2=sd_full, bit3=ia_failed, **bit4=audio_clip_ready**, bits5-7=reserved |
| 2 | 4 | Node ID | u32 | Identifiant unique du nœud (dérivé MAC ou provisionné) |
| 6 | 4 | Timestamp | u32 | Unix timestamp UTC de l'événement |
| 10 | 1 | Event type | u8 | 0x01=motion, 0x02=schedule, 0x03=test, 0x04=diagnostic, **0x05=spectral** |
| 11 | 1 | IA score | u8 | Score de confiance animal 0–100 (0=pas d'inférence, 255=erreur IA) |
| 12 | 1 | IA class | u8 | 0=non-animal, 1=mammifère, 2=oiseau, 3=humain, 4=indéterminé, 255=N/A. En P0, seule la décision d'alerte animal / non-animal est exigée ; les classes larges sont facultatives et ne constituent pas une identification d'espèce. Humain ne déclenche jamais d'alerte animale. |
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

**Taille totale : 48 octets** — taille fixe du contrat applicatif. La capacité et le temps d'air dépendent des paramètres PHY réels ; ils sont vérifiés par calcul et SOP-07 plutôt que par une ancienne limite indicative de 50 octets.

### 2. Structure du paquet uplink — Features spectrales (Event type 0x05)

Quand le cycle audio FFT (ADR-016, timer 15 min) complète une acquisition, le nœud transmet un paquet spectral. Même taille (48 octets) pour compatibilité parser, mais champs redéfinis :

| Offset | Taille | Champ | Type | Description |
|--------|--------|-------|------|-------------|
| 0 | 1 | Version | u8 | Version du protocole (0x01 = v1) |
| 1 | 1 | Flags | u8 | bit4=audio_clip_ready (si clip 60min disponible), bits0-3,5-7=reserved |
| 2 | 4 | Node ID | u32 | Identifiant unique du nœud |
| 6 | 4 | Timestamp | u32 | Unix timestamp UTC du segment spectral |
| 10 | 1 | Event type | u8 | 0x05 = spectral |
| 11 | 1 | Audio channels | u8 | Nombre de canaux audio actifs (1=mono, 2=stéréo) |
| 12 | 2 | Audio features 1 | u16 | Spectral centroid (Hz, quantifié 0-16000 → 0-65535) |
| 14 | 2 | Audio features 2 | u16 | Spectral rolloff (Hz, quantifié) |
| 16 | 2 | Audio features 3 | u16 | Spectral bandwidth (Hz, quantifié) |
| 18 | 2 | Audio features 4 | u16 | Spectral flatness (0-65535 → 0.0-1.0) |
| 20 | 2 | Audio features 5 | u16 | RMS amplitude (0-65535 → 0.0-1.0) |
| 22 | 2 | Audio features 6 | u16 | Zero crossing rate (Hz, quantifié) |
| 24 | 2 | Audio features 7 | u16 | Spectral entropy (0-65535 → 0.0-1.0) |
| 26 | 2 | Audio features 8 | u16 | Peak frequency (Hz, quantifié 0-16000 → 0-65535 comme les autres fréquences v1) |
| 28 | 2 | Audio features 9 | u16 | Spectral skewness (signed, offset 32768) |
| 30 | 2 | Audio features 10 | u16 | Spectral kurtosis (quantifié) |
| 32 | 2 | Audio clip count | u16 | Nombre de clips WAV stockés sur SD |
| 34 | 2 | Battery mV | u16 | Tension batterie en mV |
| 36 | 1 | Temperature | i8 | Température interne boîtier (°C, offset −40) |
| 37 | 1 | Mic status | u8 | bit0=mic_L_ok, bit1=mic_R_ok, bits2-7=reserved |
| 38 | 2 | Reserved | — | Zéro |
| 40 | 2 | Frame counter | u16 | Compteur incrémental |
| 42 | 2 | CRC-16 | u16 | CCITT CRC-16 sur octets 0–41 |
| 44 | 4 | Padding | — | Zéro — alignement 48 octets |

**Taille totale : 48 octets** — identique au payload caméra.

**10 descripteurs spectraux** (alignés avec ADR-013 §Impact firmware) :
1. Spectral centroid — centre de gravité du spectre
2. Spectral rolloff — fréquence sous laquelle 85% de l'énergie est contenue
3. Spectral bandwidth — largeur du spectre
4. Spectral flatness — mesure de bruit vs tonalité (0=tonal, 1=bruit blanc)
5. RMS amplitude — niveau sonore global
6. Zero crossing rate — indicateur de fréquence dominante
7. Spectral entropy — complexité/distribution du spectre
8. Peak frequency — fréquence de plus haute énergie
9. Spectral skewness — asymétrie du spectre
10. Spectral kurtosis — aplatissement du spectre

**Quantification v1 :** les valeurs flottantes sont quantifiées en u16 (16-bit). Conformément à `firmware/main/wn_config.h` (`WN_FREQ_QUANT_MAX 16000`), centroid, rolloff, bandwidth, zero crossing rate et peak frequency utilisent tous la plage 0–16000. Cette plage de quantification ne change pas la bande physique analysable, inférieure à 8 kHz à 16 kHz d'échantillonnage. Une optimisation future à 0–8000 exigerait un changement de version, du firmware et des tests ; elle n'est pas appliquée silencieusement. Les autres échelles suivent le codec v1 et ses tests. La classification fine se fait éventuellement côté pipelines avec les clips, après validation de compatibilité.

### 3. Paquet downlink (base → nœud)

Paquet compact **16 octets**, émis uniquement sur commande utilisateur :

| Offset | Taille | Champ | Type | Description |
|--------|--------|-------|------|-------------|
| 0 | 1 | Version | u8 | Version protocole (0x01) |
| 1 | 1 | Command | u8 | 0x01=upload_image, 0x02=ping, 0x03=config_update, 0x04=reboot, **0x05=upload_audio_clip**, **0x06=set_audio_schedule** |
| 2 | 4 | Target timestamp | u32 | Timestamp de l'image/clip ciblé |
| 6 | 4 | Target hash | u32 | 4 premiers octets SHA-256 du fichier ciblé |
| 10 | 2 | Parameter | u16 | Paramètre dépendant de la commande (ex: intervalle FFT pour set_audio_schedule en minutes) |
| 12 | 2 | CRC-16 | u16 | CCITT CRC-16 sur octets 0–11 |
| 14 | 2 | Padding | — | Zéro — alignement 16 octets |

**Précision de transport :** `0x01=upload_image` et `0x05=upload_audio_clip` sont des demandes transmises par LoRa, mais les fichiers eux-mêmes empruntent uniquement un transport distinct validé (Wi-Fi local ou option cellulaire P1), jamais la payload LoRa.

**Nouvelles commandes :**
- `0x05=upload_audio_clip` — déclenche l'upload d'un clip WAV via Wi-Fi (Mode C gateway locale, pas via LoRa)
- `0x06=set_audio_schedule` — met à jour les intervalles FFT et clip (Parameter = minutes)

### 4. Règles de transmission

- **SF7 par défaut** — hypothèse de départ ; la portée en forêt est une cible à mesurer avec SOP-07, pas une caractéristique garantie.
- **SF12 fallback** — automatique si pas d'ACK downlink dans les 60s (3 tentatives max).
- **Contraintes radio** : appliquer les limites de duty cycle et les règles du canal retenu. Lorsque la limite est 1 %, le firmware calcule `Toff = Tair × 99` à partir du temps d'air réel de chaque configuration ; les anciennes valeurs SF7/SF12 n'étaient que des estimations non vérifiées. Une file FIFO de 16 événements maximum lisse les rafales sans autoriser un dépassement.
- **ACK optionnel** : flag `ack_request` à 1 si le nœud attend une confirmation. La base répond en downlink dans la fenêtre RX1 (1s après TX).
- **Priorité caméra > spectral** : si la queue FIFO est pleine, les paquets spectraux sont les premiers éliminés (l'événement animal est plus urgent que le segment spectral programmé).
- **Flag audio_clip_ready** (bit4) : le nœud set ce bit dans chaque paquet (caméra ou spectral) quand un nouveau clip WAV 60min est disponible sur SD. La base peut alors décider de demander l'upload via downlink 0x05.

### 5. Extensibilité

- Le champ `Version` (offset 0) permet de faire évoluer le format sans casser la rétrocompatibilité.
- Les 8 octets `Reserved` du payload caméra (offset 24–31) restent disponibles pour de futurs champs (GPS, humidité, compteur PIR).
- L'ajout de capteurs (via ADR-008) utilisera ces octets réservés ou justifiera un bump de version.
- Le format spectral peut évoluer (bump version) si plus de 10 features sont nécessaires.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| Format binaire compact (48 octets) | Déterministe, faible temps d'air, parseur simple | Peu lisible sans outil | **Retenu** |
| JSON texte | Lisible, auto-descriptif | 100–200 octets minimum → SF10 obligatoire → duty cycle ×4 | Rejeté — impact autonomie |
| Protobuf | Compact, schéma | Dépendance bibliothèque, complexité firmware ESP32 | P1 si besoin complexité |
| Pas de format formel | Rapidité proto | Non interopérable, dette technique | Rejeté |
| Payload spectral séparé >48 octets | Plus de features, plus de précision | Dépasse SF7, impose SF9+, duty cycle ×3 | Rejeté — 10 features suffisent pour détection d'événement |
| Pas de transmission spectrale LoRa | Simplicité maximale | Aucune remontée acoustique temps réel — la base ne sait pas qu'il y a activité acoustique | Rejeté — perd la valeur de WildNexus comme capteur multi-modal |

## Conséquences

- Le codec binaire caméra + spectral existe avec des tests hôte ; cela ne valide ni le matériel ni la radio.
- La gateway P0 doit recevoir, décoder et journaliser les paquets selon `Event type`, puis gérer les erreurs. Son implémentation et son routage restent à démontrer de bout en bout.
- Le dashboard doit afficher les champs en clair (node ID, IA score, batterie, etc. pour caméra ; features spectrales + peak frequency pour spectral).
- Le `Frame counter` permet de détecter les paquets manquants (duty cycle saturation, collision).
- Les clips WAV ne transitent jamais par LoRa — récupération Wi-Fi (Mode C) ou SD physique uniquement.

## Sources

- ADR-003 (choix radio LPWAN)
- ADR-013 (couche acoustique — features spectrales 40 bytes/segment)
- ADR-016 (firmware intégré — cycle audio timer-triggered)
- ETSI EN 300 220 — duty cycle EU868
- RadioLib SX1262 packet format

## Prochaine action

1. Conserver les tests hôte et vérifier la quantification 0–16000 pour les cinq descripteurs de fréquence.
2. Exécuter SOP-07 sur matériel identifié, calculer les temps d'air et tester 96 paquets spectraux/jour + caméra + retries.
3. Démontrer la gateway P0 avec réception, décodage multi-type, journal et erreurs avant tout dashboard.

---

*Révisé le 2026-11-05 : clip stéréo corrigé à 192 000 octets, quantification v1 alignée sur le firmware, temps d'air et chaîne radio renvoyés aux preuves SOP-07/WP05.*
