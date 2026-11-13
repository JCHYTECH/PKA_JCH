# WildNexus P0 — Processus de montage du prototype

Version révisée : 2026-11-05. Statut : projet repris (2026-11-11) ; processus de montage, non validation matérielle. Ce document ne remplace ni les datasheets, ni les SOP, ni une revue du schéma.

## 1. Règles de sécurité et de preuve

- Ne pas monter tous les sous-systèmes en même temps : les configurations actuelles présentent des conflits de GPIO à résoudre.
- Tous les pinouts historiques sont des propositions à vérifier, y compris ceux des ADR et du firmware. Ils ne sont pas un schéma final.
- Relever les références physiques des micros, du PIR, des caméras et du DevKit avant câblage. Les micros TDK en stock ne sont pas déclarés I2S sans datasheet confirmée.
- Ne pas combiner USB et alimentation externe sans schéma explicitement validé. Sortie PPK2 sur OFF avant toute modification.
- Pour le seul DevKit alimenté par le PPK2 en source meter, la procédure de référence utilise VOUT 5 V → broche 5 V et GND → GND. Ne pas appliquer 3,3 V sur cette broche.
- Couper l'alimentation en cas d'échauffement, polarité incertaine ou courant anormal ; investiguer plutôt que d'appliquer un seuil générique non validé.
- Un test hôte, un exemple de log ou une valeur illustrative ne compte pas comme réussite matérielle.

## 2. Étape 0 — Réconciliation avant montage

1. Inventorier le matériel physiquement présent et relever références, versions de cartes et connectiques.
2. Rapprocher les achats du stock et du budget ; aucune nouvelle commande sans décision JCH.
3. Vérifier le scope P0, `progress.md`, ADR-005/008/013/016 et les datasheets.
4. Produire une matrice des GPIO unique : fonction, carte, tension, bus, réveil possible, conflit et preuve.
5. Vérifier les niveaux logiques, tensions maximales, courants de démarrage et partages SPI/I2S/DVP.

Critère de sortie : matériel identifié, schéma et pinout revus, budget arbitré. Sans cela, rester sur les tests hôte.

## 3. Étape 1 — Socle firmware et mesure

Exécuter les phases D/E et les SOP-04/05 sur l'ESP32-S3 seul : réveils, retour au sommeil, journal d'erreurs et mesures PPK2. Les durées simulées ne représentent ni la caméra, ni l'IA, ni la radio réelles.

Consigner firmware, carte, câblage, acquisitions brutes et énergie en Wh. Ne pas calculer une autonomie à partir d'une batterie ou d'un courant supposé ; utiliser WP03 et ses scénarios complets.

Critère de sortie : cycles reproductibles sur la cible et acquisitions exploitables.

## 4. Étape 2 — Caméra et PIR séparément

### Caméra — SOP-08

Vérifier le brochage OV5640 contre la nappe, le module et le DevKit réellement utilisés. L'ancien exemple GPIO21/20/17/18, GPIO1/2 et GPIO4–11 n'est pas réutilisable sans validation des tensions, conflits et capacités de la carte.

Capturer de vraies images jour et nuit, mesurer les états, vérifier la mise en veille et tester les erreurs de nappe/capture. La qualité de l'optique IR et les pics d'éclairage sont mesurés séparément.

### PIR — SOP-09

Relever la référence EKMB physique ; les documents mentionnent EKMB1203111 et EKMB1303111. Vérifier alimentation, sortie et logique de réveil sur sa datasheet. Ne pas appliquer automatiquement une tension ou une résistance de pull-up d'un ancien exemple.

Tester réveil, fausses alertes et consommation sur la carte cible. Le partage avec un GPIO caméra doit être résolu avant intégration.

Critère de sortie : captures réelles et réveils PIR consignés sur matériel identifié.

## 5. Étape 3 — Audio réel

SOP-13 démarre uniquement après identification des deux micros et confirmation de leur interface. L'ancien exemple SPH0645 BCLK GPIO15, WS GPIO16, entrées GPIO7/6 est incompatible avec d'autres propositions ADR-016 et ne doit pas être câblé comme un schéma validé.

Après validation du bus :

1. Initialiser les micros séparément puis en stéréo selon le montage réellement possible.
2. Produire un clip WAV PCM 16 kHz/16 bits/stéréo de trois secondes.
3. Vérifier 192 000 octets de données audio, en-tête, sidecar et horodatage.
4. Exécuter SOP-14/15 sur les fichiers issus du nœud, y compris mixdown si un pipeline l'exige.
5. Exécuter SOP-17 pour les conflits PIR/timer et SOP-18 pour l'énergie.

Critère de sortie : fichiers réels lisibles, pipelines testés et coexistence démontrée. Aucune localisation acoustique n'est présumée.

## 6. Étape 4 — Stockage microSD

Après réception d'une carte adaptée et validation du module/niveau logique, exécuter SOP-06. Le brochage SPI historique GPIO39–42 est à réconcilier avec la matrice GPIO et `wn_config.h`.

Vérifier création de `DCIM/`, `AUDIO/`, `LOGS/` et `CONFIG/`, écriture/relecture, fichiers partiels, SD pleine, retrait et endurance. La carte cible est 128 GB ; le système de fichiers et le partitionnement sont choisis selon les outils réellement supportés, pas par une commande de formatage générique.

Critère de sortie : campagne d'écriture/relecture sans corruption et pipelines alimentés depuis cette carte.

## 7. Étape 5 — Alimentation AA : SUSPENDUE

SOP-10 est suspendue. Ne pas réaliser l'ancien montage 6×AA, buck 3,3 V puis entrée 5 V. Ne pas assembler de pack 4S2P L91 à cette étape.

Avant toute reprise :

- choisir et documenter le nombre de cellules, la chimie L91 Li-FeS2 et la configuration du pack ;
- vérifier la tension maximale du pack, la plage d'entrée recommandée du TPS62840 et tout autre régulateur ;
- dimensionner pics caméra/IR/SD/radio, rendement, protections et câblage ;
- faire revoir le schéma complet et définir un premier essai limité et mesuré ;
- consigner la levée formelle de la suspension dans ADR-005, SOP-10 et `progress.md`.

Aucun critère de rendement ou d'autonomie n'est déclaré atteint avant ces mesures.

## 8. Étape 6 — Radio et gateway

La radio n'est pas commandée à ce stade documentaire ; le contenu et le prix du panier doivent être revalidés et l'achat autorisé. Ne pas suivre les anciens pinouts RAK3172/SPI sans confirmer le module, son interface et son alimentation.

Après réception :

1. Exécuter SOP-07 avec antenne adaptée connectée avant émission et cadre réglementaire documenté.
2. Tester paquets caméra et spectraux, ACK, perte, retries, files et reprise.
3. Livrer la gateway P0 : réception, décodage ADR-014, journal et erreurs.
4. Mesurer le scénario 96 paquets spectraux/jour + caméra + retries ; ne pas reprendre les anciens temps d'air comme des mesures.

Critère de sortie : chaîne nœud → gateway démontrée et énergie intégrée à WP03.

## 9. Étape 7 — IA puis intégration

Après caméra réelle et dataset, appliquer SOP-11 : comparer les modèles sur images jour/nuit, mesurer rappel humain/animal, fausses alertes, latence, mémoire et Wh. Le code factice historique n'est pas un résultat.

Intégrer progressivement caméra, PIR, audio, SD, IA et radio selon la matrice GPIO validée. Exécuter les critères ADR-016 et la matrice du scope lock avant de préparer boîtier/EVT. Les 37/37 tests hôte historiques restent une preuve logicielle séparée.

## 10. Check-list de reprise

- [ ] Inventaire, factures, budget et autorisation réconciliés.
- [ ] Micros/PIR/cartes identifiés ; datasheets et matrice GPIO validés.
- [ ] Phases D/E et caméra/PIR mesurés sur cible.
- [ ] Audio/WAV/JSON/pipelines et coexistence validés.
- [ ] SD et récupération sur erreurs validées.
- [ ] SOP-10 formellement débloquée avant tout essai AA.
- [ ] Radio achetée après arbitrage ; gateway fonctionnelle.
- [ ] Modèle IA choisi par benchmark ; cycle complet mesuré en Wh.
- [ ] Aucun passage au terrain sans ADR-018, sécurité/RGPD et boîtier validés.
