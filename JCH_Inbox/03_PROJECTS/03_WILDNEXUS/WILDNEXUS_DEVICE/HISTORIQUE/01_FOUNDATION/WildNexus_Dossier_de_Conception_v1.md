# WildNexus – Dossier de conception
_Date : 16 juillet 2026_

# 1. Vision

WildNexus est une plateforme autonome de surveillance écologique destinée à détecter des signaux faibles dans les milieux naturels avant qu'ils ne deviennent des événements critiques.

L'objectif n'est pas uniquement de détecter un incendie ou un orage, mais d'évaluer **l'état de santé global d'un écosystème**.

## Objectifs

- Surveillance de la biodiversité
- Surveillance du risque incendie
- Surveillance du stress hydrique
- Détection des orages
- Acquisition de données scientifiques

# 2. Principe général

Chaque station comporte :

- ESP32
- Microphones (audible + éventuellement ultrasons)
- Capteurs météo
- Capteurs VOC
- Détecteur d'éclairs
- Communication LoRa/Wi-Fi

Les données sont fusionnées localement puis transmises à un serveur IA.

# 3. Module "Éléphant"

Inspiré de la capacité supposée des éléphants à percevoir des orages lointains.

Composants :

- AS3935
- antenne adaptée
- ESP32

Fonctions :

- détection des éclairs
- estimation de distance
- historique
- corrélation avec météo

# 4. Module acoustique

Détection :

- oiseaux
- insectes
- mammifères
- pluie
- vent
- feu
- activité humaine

Bases de données à exploiter :

- FSD50K
- ESC-50
- AudioSet
- jeux de données ouverts complémentaires

Objectif futur :

Créer une base mondiale spécialisée des sons d'incendie.

# 5. Module incendie

Fusion de plusieurs indices :

- activité acoustique
- température
- humidité
- vitesse du vent
- VOC
- CO
- particules fines
- proximité d'orages

L'IA produit un indice de risque.

# 6. Module stress hydrique

Concept très innovant.

Hypothèse :

Les arbres en stress émettent des ultrasons de cavitation dans le xylème.

Pistes :

- microphones ultrasons
- capteurs piézo
- traitement IA

Applications :

- sécheresse
- dépérissement
- estimation indirecte du risque incendie

# 7. Architecture

## Niveau 1

ESP32

Fonctions :

- acquisition
- filtrage
- compression
- pré-analyse

## Niveau 2

Serveur IA (Mac mini / NAS / Raspberry Pi 5)

Fonctions :

- modèles IA
- apprentissage
- fusion des capteurs
- tableau de bord

# 8. Communications

Priorité :

- LoRa
- Wi-Fi
- 4G uniquement lorsque nécessaire

# 9. Capteurs envisagés

- AS3935
- BME688
- capteur CO
- capteur PM2.5
- micro MEMS
- micro ultrason
- GPS (option)

# 10. Originalité scientifique

WildNexus ne détecte pas uniquement des événements.

Il estime un état écologique :

- biodiversité
- sécheresse
- stress des arbres
- risque incendie
- activité météorologique

# 11. Feuille de route

Phase 1
- Station acoustique

Phase 2
- Détecteur Éléphant

Phase 3
- VOC

Phase 4
- Fusion IA

Phase 5
- Cavitation

Phase 6
- Réseau collaboratif

# 12. Questions ouvertes

- meilleure technologie ultrason
- disponibilité de bases incendie
- choix du modèle IA embarqué
- consommation énergétique
- validation scientifique

# Conclusion

WildNexus pourrait évoluer d'un simple système de suivi de biodiversité vers une plateforme complète de surveillance de la santé des écosystèmes, capable de détecter des signaux faibles grâce à la fusion de capteurs physiques, chimiques, biologiques et acoustiques.
