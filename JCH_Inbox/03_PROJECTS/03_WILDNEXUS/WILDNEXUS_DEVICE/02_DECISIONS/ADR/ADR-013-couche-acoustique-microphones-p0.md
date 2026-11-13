# ADR-013 — Couche acoustique : microphones et monitoring sonore

**Statut :** accepté comme architecture cible ; validation matérielle ouverte
**Date :** 2026-06-19  
**Dernière mise à jour :** 2026-11-05
**Décideur :** Dobby + JCH
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Portée :** capture stéréo P0 ; pistes P1 non engagées

## Contexte

WildNexus vise à compléter les images par des clips audio locaux et des descripteurs spectraux. Le P0 ne fait ni classification d'espèce ni traduction animale.

Le schéma initial retenait deux Knowles SPH0645LM4H-B. Le stock et le générateur de BOM mentionnent aussi des micros TDK reçus. Leur référence exacte, leur interface et leur compatibilité avec le pinout doivent être vérifiées avant SOP-13 : la présence d'un boîtier MEMS ne prouve pas une interface I2S.

## Décision

### 1. Architecture P0

- Deux micros MEMS pour une capture stéréo locale et une redondance fonctionnelle.
- Clip WAV PCM 16 bits, 16 kHz, stéréo, 3 secondes toutes les 60 minutes.
- Dix descripteurs FFT toutes les 15 minutes, avec transmission LoRa prévue par ADR-014.
- Récupération des clips par SD ou transport local distinct ; jamais dans la payload LoRa.
- Aucune classification bioacoustique d'espèce dans le P0.

Le SPH0645LM4H-B reste la référence de conception historique. Le composant définitif du prototype ne sera confirmé qu'après rapprochement du stock, de la datasheet et du schéma. Les valeurs de sensibilité, bruit et consommation seront reprises de la datasheet du composant effectivement retenu, pas héritées d'un autre modèle.

### 2. Limite de bande

À 16 kHz d'échantillonnage, la bande numérique utile est inférieure à 8 kHz. La réponse analogique annoncée d'un micro jusqu'à 10 ou 20 kHz ne supprime pas cette limite.

| Usage envisagé | Conséquence P0 |
|----------------|----------------|
| Sons avec énergie utile sous 8 kHz | Candidats à un essai de captabilité réelle |
| Espèces dont une partie du répertoire dépasse 8 kHz | Couverture partielle possible, à documenter par espèce |
| Sauterelles haute fréquence et chauves-souris | Non couverts par la configuration 16 kHz ; autre chaîne d'acquisition nécessaire |

Aucune distance de détection, marge de bruit ou précision angulaire n'est validée sans protocole terrain, niveau source, environnement et calibration.

### 3. Ce que les deux micros peuvent et ne peuvent pas promettre

La stéréo vise une différence gauche/droite et une redondance. Une localisation azimutale chiffrée exigerait une acquisition simultanée, une baseline mesurée, une calibration de phase/gain et un traitement adapté. Elle n'est pas un livrable P0.

Le P0 ne promet ni triangulation fine inter-nœuds, ni comptage d'individus, ni résolution angulaire. Ces fonctions exigeraient une architecture de synchronisation et de localisation distincte, notamment ADR-018, et des essais scientifiques.

### 4. Upgrade P1 éventuel

L'ICS-43434 peut être étudié en P1, sans présumer qu'il est pin-compatible avec le SPH0645LM4H-B. Son interface ne suffit pas à couvrir les ultrasons : le micro, le filtrage, l'horloge, le débit I2S, la fréquence d'échantillonnage, le stockage et les pipelines doivent être dimensionnés ensemble.

Toute hausse à 48 kHz triple le volume PCM par rapport à 16 kHz à format identique. Elle ne couvre toujours pas les chauves-souris et ne devient pas un engagement P0.

## Conséquences

### BOM et boîtier

- Le BOM distingue le micro cible du micro réellement reçu ; toute substitution exige une revue électrique et acoustique.
- Les membranes et ouvertures acoustiques sont à prototyper. Leur présence ne garantit pas le maintien de la cible IP67.
- Le coût des micros, membranes, joints et modifications de boîtier doit figurer dans le BOM consolidé.

### Firmware et données

- L'acquisition stéréo et l'horodatage commun sont validés par SOP-13 ; le code I2S seul ne suffit pas.
- Les tests FFT/WAV sur hôte doivent être reproduits sur des données et des fichiers produits par le nœud.
- Un clip de 3 s à 16 kHz, 16 bits, stéréo contient **192 000 octets audio**, soit environ **4,61 MB de WAV pour 24 clips/jour**, hors sidecars JSON.
- Les 10 descripteurs occupent 20 octets une fois quantifiés en `u16` dans ADR-014 ; 40 octets correspondent seulement à leur représentation flottante interne éventuelle.
- À 96 cycles FFT/jour, les paquets de 48 octets représentent au maximum 4 608 octets de payload applicative/jour/nœud, avant overhead radio, retransmissions et contraintes de temps d'air.
- Aucune position GPS n'est transmise dans ADR-014. La position de déploiement, si nécessaire, est enregistrée côté gateway avec une base légale et une protection adaptées.

### Réseau et analyse

La gateway agrège les événements effectivement reçus et leurs horodatages. À 10 nœuds et 96 cycles/jour pendant 30 jours, elle pourrait recevoir 28 800 enregistrements spectraux, chacun portant 10 descripteurs, si toutes les transmissions réussissent. Ce volume est un scénario de capacité, pas une mesure ni une preuve de scientificité.

## Alternatives considérées

| Alternative | Décision |
|-------------|----------|
| Micro analogique + ADC externe | Écarté en P0 pour limiter la complexité ; réévaluation si le stock numérique est incompatible |
| Un seul micro | Ne répond pas à la cible stéréo/redondance |
| Trois à quatre micros | Hors P0 : câblage, boîtier, énergie et traitement supplémentaires |
| Analyse d'espèce embarquée | Hors P0 ; pipelines en aval après extraction |
| Mesure de direction ou triangulation | Recherche ultérieure après calibration et synchronisation, pas une conséquence automatique de la stéréo |

## Validation requise

| Test | Critère |
|------|---------|
| Référence et datasheet | Composant physique identifié, interface et niveaux électriques compatibles |
| Capture SOP-13 | Deux canaux réels, sans échange ni saturation anormale |
| Fichiers du nœud | WAV/sidecars conformes à ADR-017, relus après extraction SD |
| Compatibilité aval | Au moins un clip réel traité par chaque pipeline cible ou adaptation documentée |
| Couverture taxons | Liste d'espèces et bandes cibles avant toute affirmation scientifique |
| Consommation | Mesure PPK2 intégrée à WP03/SOP-18 |
| Boîtier | Essais acoustiques et d'étanchéité après modification |

## Références

- ADR-014 — transport des descripteurs spectraux
- ADR-016 — cycles firmware
- ADR-017 — format WAV et sidecars
- ADR-018 à rédiger — synchronisation temporelle
- SOP-13 à SOP-18 — preuves acoustiques
- Stock et BOM actifs — références physiques à rapprocher

---

*Révision 2026-11-05 : micros reçus non présumés I2S, limites de 16 kHz explicites, précisions de localisation non prouvées retirées, volumes stéréo corrigés et validation matérielle ajoutée.*
