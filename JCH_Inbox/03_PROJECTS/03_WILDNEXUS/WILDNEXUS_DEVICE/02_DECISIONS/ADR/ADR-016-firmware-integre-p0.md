# ADR-016 — Firmware intégré P0 : double cycle caméra et audio

Date initiale : 2026-06-30. Révision : 2026-11-05. Statut : architecture acceptée ; validation matérielle ouverte. Owner : Forge. Jalon : M-02.

## 1. Contexte et état de preuve

P0 exige deux cycles : un cycle caméra déclenché par PIR et un cycle audio déclenché par minuterie. L'ADR définit leur orchestration, pas une validation du matériel.

Le projet `firmware/` et les modules de codec, machine d'états, audio et métadonnées existent. Les 37/37 tests consignés en juillet sont des tests sur ordinateur hôte, avec mocks. Ils ne prouvent ni les périphériques ESP32-S3, ni la capture caméra/I2S, ni l'IA, ni la radio, ni la consommation, ni la robustesse du système intégré.

Les phrases antérieures affirmant que les firmwares individuels avaient validé chaque composant sont retirées. Les résultats réels et les protocoles restants sont suivis dans `03_P0_ENGINEERING/PROTOCOLES/progress.md`.

## 2. Décision d'architecture

### 2.1 Projet modulaire ESP-IDF

Conserver un projet ESP-IDF modulaire et testable sur hôte : orchestration, configuration, caméra, énergie, stockage, radio, PIR, IA, audio, provisioning et codecs. Les tests hôte restent utiles pour la logique, les erreurs et les contrats binaires ; chaque fonction possède aussi un critère matériel explicite.

Les fichiers `firmware/main/wn_config.h` et les modules associés décrivent l'implémentation courante. Ils ne constituent pas un schéma électrique approuvé. Tout GPIO, partage SPI/I2S et mode de réveil doit être vérifié contre le DevKit, les références physiques et les datasheets avant câblage.

### 2.2 Cycle caméra déclenché par PIR

Séquence cible :

```text
SLEEP → WAKE → CAPTURE → AI_FILTER
                            ├─ humain : suppression ou floutage irréversible avant conservation ; pas d'alerte animale
                            ├─ animal admissible : STORE_MEDIA → TX_METADATA → SLEEP
                            ├─ non-animal : LOG_ONLY ou rétention documentée → SLEEP
                            └─ échec : LOG_ERROR/IA_FAILED, politique de conservation sûre → SLEEP
```

Règles :

- LoRa ne transporte que les métadonnées ADR-014 ; aucune image ne quitte le nœud par ce canal.
- La conservation suit ADR-010. Le filtre humain peut produire des faux négatifs : chiffrement, durée maximale et droit d'accès restent nécessaires.
- En cas d'échec IA ou de conservation, aucun média non évalué n'est exposé par un transport externe. Le comportement local retenu doit privilégier la confidentialité et être testé.
- Les seuils d'IA sont des paramètres à calibrer après benchmark ; les valeurs présentes dans le code ne sont pas des performances validées.
- Les erreurs SD ne doivent pas provoquer de rafale radio. Les files et retransmissions respectent ADR-014 et le budget énergie.

### 2.3 Cycle audio déclenché par minuterie

Deux échéances initiales sont conservées comme configuration de prototype :

- descripteurs spectraux toutes les 15 minutes, avec acquisition courte, calcul, stockage JSON et paquet spectral ADR-014 ;
- clip WAV stéréo de trois secondes toutes les 60 minutes, à 16 kHz/16 bits, avec sidecar JSON.

```text
SLEEP → AUDIO_WAKE → AUDIO_ACQUIRE → AUDIO_PROCESS → AUDIO_STORE
                                                       ├─ FFT : TX_METADATA → SLEEP
                                                       └─ CLIP : SLEEP, sans transfert du WAV par LoRa
```

Le clip contient 192 000 octets de données PCM, hors en-tête et sidecar. La fréquence d'échantillonnage impose une bande analysable inférieure à 8 kHz. La compatibilité avec les pipelines est à tester sur fichiers réels.

Les volumes et les besoins radio réels sont mesurés avant de figer la cadence définitive. Un flag `audio_clip_ready` peut signaler un clip ; le fichier emprunte seulement un transport local validé.

### 2.4 Concurrence et reprises

La caméra est prioritaire sur l'audio programmé. Une interruption ne doit jamais laisser un WAV/JSON corrompu ou une ressource matérielle indisponible.

| Situation | Règle cible à tester |
|---|---|
| PIR pendant l'audio | Terminer ou abandonner proprement l'étape atomique, fermer les fichiers, libérer I2S/SD puis exécuter la caméra ; replanifier l'audio |
| Timer audio pendant la caméra | Mettre l'audio en attente, sans acquisition concurrente non validée |
| PIR et timer simultanés | Priorité caméra |
| FFT et clip simultanés | Sérialiser ; l'ordre initial privilégie le FFT court, sans créer de famine du clip |
| Reset/brunout/SD pleine | État récupérable au boot, fichiers partiels identifiés, erreur journalisée |

La simultanéité réelle des périphériques n'est pas présumée : DMA, RAM, bus et SD sont vérifiés avant d'autoriser tout parallélisme.

### 2.5 Paramètres et interfaces

Les constantes de pins, cadences, seuils, niveaux de batterie et radio du firmware sont une proposition d'implémentation. Elles doivent être réconciliées avec :

- ADR-005 et le schéma d'alimentation validé ;
- ADR-013 et l'interface réelle des micros ;
- ADR-014 pour le contrat radio ;
- ADR-017 pour les fichiers ;
- le pinout du DevKit et le processus de montage révisé.

Le contrat spectral v1 quantifie les fréquences sur 0–16000, conformément à `WN_FREQ_QUANT_MAX`. Cela ne modifie pas la bande physique <8 kHz à 16 kHz d'échantillonnage.

## 3. Énergie

Les anciennes estimations d'environ 1,4 mAh/jour pour l'audio et de 5–8 mAh/jour pour la caméra sont supprimées comme base de décision : elles ne reposent pas sur des mesures du système retenu.

Chaque état est mesuré au PPK2 selon WP03 : veille, réveil, caméra, IA, IR, I2S, FFT, écriture SD, LoRa, attente ACK et retransmissions. Le modèle en Wh inclut conversion, froid et scénarios 10/30/72 événements/jour. Un courant de deep sleep isolé, même inférieur à 1 mA, ne prouve pas la cible de 60 jours.

## 4. Alternatives

| Option | Décision |
|---|---|
| ESP-IDF modulaire avec tests hôte et matériels | Retenu |
| Sketch Arduino monolithique | Rejeté pour l'intégration P0 |
| Attendre la validation de chaque module avant de tester la logique intégrée | Rejeté : les mocks permettent déjà de tester les transitions, sans les confondre avec le matériel |
| Thread audio parallèle permanent | Non retenu en veille profonde ; toute concurrence active doit être prouvée sûre |
| Audio uniquement sur PIR | Rejeté : il ne fournit pas les captures programmées requises |

## 5. Conséquences et travaux

- Maintenir les tests hôte et ajouter les validations sur cible aux mêmes contrats.
- Tester le codec sur hôte, puis son transport réel nœud → gateway ; un roundtrip local ne suffit pas.
- Exécuter SOP-13/14/15/17/18 sur l'audio réel après confirmation des micros.
- Exécuter CAM-03/SOP-11 avec le modèle choisi par benchmark, sans imposer MobileNet-SSD ou FOMO.
- Implémenter et vérifier la gateway minimale P0 : réception, décodage caméra/spectral, journal et erreurs.
- Rédiger ADR-018 avant de revendiquer une synchronisation image/audio ou une horodatation terrain fiable.
- Ne pas réactiver SOP-10 ni appliquer les exemples de GPIO sans revue matérielle.

## 6. Critères de validation matérielle

| Test | Critère minimal, à compléter par les SOP |
|---|---|
| Cycle caméra intégré | 100 cycles sur cible sans crash ni fichier corrompu ; comportements humain/animal/échec vérifiés |
| Cycle spectral | 50 cycles sur cible ; JSON valide et paquets effectivement reçus par la gateway |
| Cycle clip | 20 cycles sur cible ; WAV PCM 16 kHz/16 bits/stéréo/3 s lisible et sidecar cohérent |
| Conflits PIR/audio/timer | Reprise propre, ressources libérées, pas de perte silencieuse |
| Codec caméra et spectral | Roundtrip hôte puis décodage des octets reçus par la gateway |
| Contraintes radio | Temps d'air calculé pour le matériel/configuration, scénario 96 spectraux + caméra + retries testé |
| Filtre humain | Seuils ADR-010 mesurés jour/nuit ; faux négatifs traités par sécurité du support |
| Énergie | Mesures par état et cycle complet intégrées au gate WP03 ; pas de seuil de sommeil utilisé seul |
| Pipelines | Fichiers produits par le nœud lus par les pipelines cibles |

Le statut « accepté » porte sur l'architecture. Il ne sera pas interprété comme une acceptation du prototype matériel.

## 7. Révision

Réviser si les ressources RAM/DMA/bus imposent une autre orchestration, si le modèle IA requiert un autre MCU, si les micros réels changent l'interface, si le volume radio dépasse le cadre réglementaire ou si les mesures WP03 invalident les cadences.
