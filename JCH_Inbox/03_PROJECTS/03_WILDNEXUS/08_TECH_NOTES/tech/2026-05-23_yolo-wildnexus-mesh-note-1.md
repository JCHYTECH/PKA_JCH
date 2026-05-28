# YOLO WildNexus 1

## Réseaux Mesh pour le projet WildMesh

Le réseau mesh radio est particulièrement pertinent pour un projet de monitoring écologique distribué comme WildMesh.

Chaque nœud du réseau peut :
- émettre,
- recevoir,
- relayer les informations des autres nœuds.

Cela permet de créer une architecture autonome adaptée :
- aux forêts,
- aux réserves naturelles,
- aux zones sans infrastructure réseau,
- aux grands espaces.

## Architecture recommandée

### Niveau capteurs
- Microphones
- Caméras
- Température
- Humidité
- Luminosité
- Détection mouvement

### Niveau IA locale
- [[BirdNET]]
- YOLO
- Analyse embarquée

### Niveau Mesh
Transmission uniquement :
- événements,
- scores IA,
- télémétrie,
- alertes,
- état batterie,
- coordonnées GPS.

Pas de :
- vidéo HD,
- audio continu brut.

## Technologie la plus adaptée

### [[LoRa]] Mesh

Technologies possibles :
- Meshtastic
- SX1262
- Heltec V3
- LilyGo T-Beam

Avantages :
- très basse consommation,
- excellente portée,
- compatible solaire,
- robuste en forêt.

## Architecture hybride recommandée

- [[ESP32-S3]] toujours actif
- [[Raspberry Pi]] réveillé uniquement si nécessaire
- [[BirdNET]] et YOLO localement
- [[LoRa]] Mesh pour communication
- Wi-Fi local pour maintenance et téléchargement

## Vision du projet

WildMesh peut évoluer vers :
- un réseau écologique intelligent,
- une cartographie distribuée de la biodiversité,
- une corrélation multi-capteurs,
- une surveillance autonome longue durée.
