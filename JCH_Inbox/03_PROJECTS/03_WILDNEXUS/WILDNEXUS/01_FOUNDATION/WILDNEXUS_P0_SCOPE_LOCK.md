# WildNexus — Verrou de périmètre P0

**Version :** v0.4  
**Date :** 2026-07-05  
**Statut :** Pré-go opérationnel  
**Owner :** [[Dobby]]  

## 1. Objet

Ce document verrouille le périmètre P0 pour éviter que les composants déjà documentés mais non critiques ne diluent l'exécution du premier prototype.

Le principe est simple : P0 doit prouver un nœud caméra autonome crédible, pas toute la plateforme WildNexus finale.

## 2. P0 engagé

P0 couvre uniquement :

- un nœud caméra autonome ;
- capture image exploitable de jour et de nuit ;
- capture audio locale courte via micro stéréo MEMS (2× SPH0645LM4H-B) ;
  - **clip WAV 3s toutes les 60 min** (stocké SD, format WAV PCM 16-bit 16 kHz stéréo — ADR-017) ;
  - **features spectrales FFT 1024 toutes les 15 min** (10 descripteurs, transmises LoRa — ADR-014/016) ;
- détection événementielle (PIR) ;
- filtre embarqué animal / non-animal ;
- transmission LPWAN événementielle de métadonnées ou alerte + features spectrales ;
- stockage local (images + clips audio + sidecars JSON) ;
- configuration terrain simple ;
- autonomie minimale de 60 jours batterie seule, validée par EVT 30 jours avec extrapolation ;
- boîtier terrain IP67 ;
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
- **format WAV compatible BirdNET/InsectSet459/TweetyBERT** (ADR-017) ;
- **features spectrales transmissibles via LoRa** (ADR-014 type 0x05) ;
- **cycle audio timer-triggered coexistant avec cycle PIR** (ADR-016) ;
- upgrade path micro ICS-43434 pin-compatible (ADR-013) ;
- upgrade path sample rate 16→48 kHz sans changement de format (ADR-017) ;
- carte SD 128 GB minimum pour anticiper monitoring continu P1 (ADR-017 §6) ;
- volume réservé PCB pour RTC externe DS3231 (ADR-018 backlog).

## 5. Relation avec les composants existants

### NEXUS_ACOUSTIC (projet extrait)

Le répertoire bioacoustique a été extrait vers le projet autonome `NEXUS_ACOUSTIC`. Le P0 intègre :
- 2 micros MEMS stéréo (ADR-013)
- enregistrement de clips WAV courts programmés (ADR-016/017)
- features spectrales transmises LoRa (ADR-014 type 0x05)

Le P0 ne crée pas de tâche bloquante pour NEXUS_ACOUSTIC sur la classification d'espèces, BirdNET, DSP avancé ou analyse scientifique. Les clips WAV P0 sont néanmoins **compatibles d'emblée** avec les pipelines InsectNet et NEXUS_ACOUSTIC (format WAV 16 kHz 16-bit stéréo + sidecar JSON).

### InsectNet (projet extrait)

Les clips WAV P0 de WildNexus peuvent alimenter directement le pipeline InsectNet (classification orthoptères) après extraction SD. Le format WAV 16 kHz est compatible InsectSet459 (resample si nécessaire). Les features spectrales LoRa donnent une vue temps réel de l'activité acoustique du site.

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

Le `go` opérationnel porte sur WP01 à WP06 tels que cadrés dans le document fondateur, avec les exclusions explicites ci-dessus.

---

*Mis à jour v0.4 le 2026-07-05 — précision cycles audio (ADR-016/014/017), interfaces préservées élargies, compatibilité InsectNet/NEXUS_ACOUSTIC explicite.*
