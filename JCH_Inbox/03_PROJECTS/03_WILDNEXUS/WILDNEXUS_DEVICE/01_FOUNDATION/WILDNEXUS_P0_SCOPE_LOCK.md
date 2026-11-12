# WildNexus — Verrou de périmètre P0

**Version :** v0.5
**Date :** 2026-11-05
**Statut :** Pré-go opérationnel  
**Owner :** [[Dobby]]  

## 1. Objet

Ce document verrouille le périmètre P0 pour éviter que les composants déjà documentés mais non critiques ne diluent l'exécution du premier prototype.

Le principe est simple : P0 doit prouver un nœud caméra autonome crédible et sa chaîne d'alerte de bout en bout, pas toute la plateforme WildNexus finale. Une gateway minimale de développement est nécessaire à cette preuve ; la STATION commerciale autonome reste en P1.

## 2. P0 engagé

P0 couvre uniquement :

- un nœud caméra autonome ;
- capture image exploitable de jour et de nuit ;
- capture audio locale courte via micro stéréo MEMS (2× SPH0645LM4H-B) ;
  - **clip WAV 3s toutes les 60 min** (stocké SD, format WAV PCM 16-bit 16 kHz stéréo — ADR-017) ;
  - **features spectrales FFT 1024 toutes les 15 min** (10 descripteurs, transmises LoRa — ADR-014/016) ;
- détection événementielle (PIR) ;
- filtre embarqué animal / non-animal, avec détection humaine distincte pour la confidentialité ;
- transmission LPWAN événementielle de métadonnées ou alerte + features spectrales, reçue et décodée par une gateway de développement P0 ;
- stockage local (images + clips audio + sidecars JSON) ;
- configuration terrain simple ;
- cible d'autonomie de 60 jours sur batterie seule au profil de référence, à valider par mesures PPK2 puis EVT 30 jours avec extrapolation documentée ;
- boîtier terrain avec cible IP67, à confirmer par le protocole d'étanchéité ;
- documentation suffisante pour compiler, flasher et reproduire le socle.

> **Mise à jour v0.4 (2026-07-05) :** Précision des deux cycles audio (FFT 15 min + clip 60 min) suite à l'audit ADR-016/014/017. Le scope est inchangé sur le fond — capture audio locale P0, analyse/classification d'espèces P1. Mais la machine d'états firmware (ADR-016) intègre désormais explicitement le cycle audio timer-triggered pour que les micros ne restent pas muets.

## 3. Hors P0 explicite

Ces éléments sont hors P0, sauf contrainte d'interface minimale :

| Sujet | Statut | Raison |
|---|---|---|
| Reconnaissance bioacoustique / BirdNET | P1 deferred | Le micro stéréo est P0 pour capture locale + features spectrales, mais la classification d'espèces reste hors P0 |
| Faune Autour PWA | Projet adjacent ou P2 | Application utile, mais non requise pour prototype caméra P0 |
| Reconnaissance espèce fine | P1 | P0 se limite au filtre animal / non-animal |
| Reconnaissance individuelle | P1/P2 | Valeur forte mais dépend d'un corpus et de modèles plus avancés |
| STATION commerciale autonome | P1 | Seule une gateway minimale de banc est nécessaire au P0 pour décoder les alertes et prouver la chaîne radio |
| Réseau public de stations | P2 | Requiert gouvernance, sécurité, communauté et exploitation de données |
| Bioacoustique multi-taxons | P2 | Complexité scientifique et DSP non nécessaire au premier jalon |
| Cloud scientifique complet | P2 | Ne doit pas précéder la preuve terrain |
| App native iOS/Android | Hors scope | PWA ou interface web suffisante pour les besoins initiaux |
| Monitoring audio continu 24/7 | P1 | P0 = clips programmés (3s/60min) + FFT (15min). P1 = monitoring continu pour NEXUS_ACOUSTIC |
| Upload audio via LoRa | Hors scope | Clips WAV trop gros pour LoRa. Récupération Wi-Fi (Mode C) ou SD physique. Notification existence clip via flag LoRa. |

## 4. Interfaces à préserver en P0

P0 ne développe pas les modules P1/P2, mais doit éviter de les bloquer :

- port ou bus d'extension capteur documenté (ADR-008) ;
- schéma de métadonnées extensible (Camtrap-DP pour images — ADR-016, JSON sidecar pour audio — ADR-017) ;
- horodatage et géolocalisation propres — ⚠️ synchronisation temporelle à spécifier (ADR-018 backlog) ;
- séparation claire entre capture, détection, stockage et transmission (ADR-016 machine d'états modulaire) ;
- possibilité future d'ajouter événement acoustique ou environnemental sans refonte complète ;
- **format WAV prévu pour validation dans BirdNET/InsectSet459/TweetyBERT** (ADR-017), sans prétendre à une compatibilité avant essai ;
- **features spectrales destinées à LoRa** (ADR-014 type 0x05), sous réserve de SOP-07 et de la gateway ;
- **cycle audio timer-triggered coexistant avec cycle PIR** (ADR-016), à vérifier sur matériel ;
- éventuel upgrade micro ICS-43434 en P1, dont le brochage, l'électronique et le couple micro/fréquence d'échantillonnage doivent être vérifiés (ADR-013) ;
- possibilité de faire évoluer le WAV de 16 à 48 kHz, avec recalcul des volumes et compatibilités (ADR-017) ;
- carte SD 128 GB minimum pour anticiper monitoring continu P1 (ADR-017 §6) ;
- volume réservé PCB pour RTC externe DS3231 (ADR-018 backlog).

## 5. Relation avec les composants existants

### NEXUS_ACOUSTIC (projet extrait)

Le répertoire bioacoustique a été extrait vers le projet autonome `NEXUS_ACOUSTIC`. Le P0 intègre :
- 2 micros MEMS stéréo (ADR-013), dont l'interface réelle reste à confirmer sur le matériel reçu ;
- enregistrement programmé de clips WAV courts (ADR-016/017) ;
- features spectrales destinées à LoRa (ADR-014 type 0x05).

Le P0 ne crée pas de tâche bloquante pour NEXUS_ACOUSTIC sur la classification d'espèces, BirdNET, DSP avancé ou analyse scientifique. Le format WAV 16 kHz 16-bit stéréo + sidecar JSON est conçu pour alimenter InsectNet et NEXUS_ACOUSTIC après extraction, mais chaque pipeline doit encore traiter avec succès un clip réellement produit par le nœud.

### InsectNet (projet extrait)

Les clips WAV P0 pourront alimenter InsectNet après extraction SD, resampling ou mixdown si le pipeline l'exige. La couverture des espèces et la fréquence d'échantillonnage doivent être validées avant toute promesse multi-taxons. Les features spectrales LoRa sont une cible de remontée d'activité, pas une capacité radio déjà démontrée.

### FAUNE_AUTOUR (projet extrait)

Faune Autour est un projet adjacent à forte synergie. Il peut devenir une interface ou une extension WildNexus en P2, mais n'est pas un livrable P0. Son évolution ne doit pas bloquer le prototype caméra.

## 6. Critère anti-scope-creep

Toute proposition ajoutant une capacité P1/P2 à P0 doit répondre à trois questions :

1. Cette capacité est-elle nécessaire pour prouver le nœud caméra autonome ?
2. Son absence rend-elle M-03 invalide ?
3. Peut-elle être remplacée par une interface ou une hypothèse documentée ?

Si les réponses ne justifient pas clairement l'inclusion, la capacité reste hors P0.

## 7. Décision actuelle

Statut recommandé : P0 strict.

Le `go` opérationnel porte sur WP01 à WP06 tels que cadrés dans le document fondateur, avec les exclusions explicites ci-dessus. Les caractéristiques non mesurées sont des cibles de conception, jamais des performances acquises.

## 8. Matrice minimale exigence → preuve

Cette matrice détermine la clôture réelle du P0. Un test algorithmique sur ordinateur hôte ne vaut pas validation matérielle ou terrain.

| Exigence | Preuve minimale | État au 2026-11-05 |
|---|---|---|
| Capture image jour/nuit | SOP-08 + CAM-02 sur OV5640, puis essai IR | À exécuter |
| Capture audio réelle | SOP-13 sur micros + SOP-14/15 sur fichiers produits par le nœud | Tests host seulement ; interface des micros reçus à confirmer |
| Filtre animal / non-animal et humain | SOP-11 + benchmark jour/nuit ADR-010 sur ESP32-S3 | Bloqué ; modèle non entraîné |
| Alerte de bout en bout | SOP-07 + gateway P0 : réception, décodage caméra/spectral et journal | Bloqué par le module radio |
| Stockage local fiable | SOP-06 + cycles écriture/coupure sur carte 128 GB | À exécuter |
| Autonomie cible 60 jours | WP03 + SOP-18 : tous les cycles, pertes et scénarios jour/nuit ; EVT 30 jours ensuite | Non démontrée |
| Confidentialité et sécurité | Réserves ADR-010, règles de conservation et procédure droit d'accès | En cours de spécification |
| Boîtier et terrain | WP06 : étanchéité, fixation et EVT | À exécuter |

Le chemin de preuve minimal est : détection → image/audio → stockage → filtre → gateway → mesure d'énergie. Aucune fonction P1/P2 ne doit être ajoutée pour combler un échec de ce chemin.

---

*Mis à jour v0.5 le 2026-11-05 — gateway de développement P0 distinguée de la STATION P1, performances non mesurées requalifiées en cibles, matrice exigence → preuve ajoutée.*
