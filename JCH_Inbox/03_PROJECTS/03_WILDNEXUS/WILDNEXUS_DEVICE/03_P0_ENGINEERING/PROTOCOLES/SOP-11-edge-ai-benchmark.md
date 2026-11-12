# SOP-11 — Benchmark comparatif Edge AI sur ESP32-S3

Version 2.0 — 2026-11-05. Statut : procédure prête à préparer, non exécutée sur le matériel cible. Projet : WildNexus P0 / M-02.

## 1. Objectif

Comparer au moins deux modèles compatibles avec la cible — par exemple FOMO, MobileNet-SSD ou un équivalent quantisé — puis mesurer le modèle retenu sur ESP32-S3. Le choix ne se fait pas sur le nom du modèle ni sur un exemple de documentation.

Le benchmark traite ADR-010 R4/R5 et CAM-03 : rappel humain, qualité de détection animale, fausses alertes, latence, mémoire et énergie. Une latence inférieure à 100 ms n'est pas un objectif acquis ; le critère ADR-010 actuel est inférieur à 2 s par frame, sauf révision documentée.

## 2. Prérequis bloquants

- [ ] SOP-08 exécutée : la caméra OV5640 produit de vraies images sur la cible.
- [ ] Dataset daté, versionné et séparé en jeux d'entraînement, validation et test.
- [ ] Images réelles jour/nuit IR, avec animaux, humains, végétation et scènes vides représentatives du site.
- [ ] Annotations relues ; classes `animal`, `humain` et `non-animal/autre` définies sans ambiguïté.
- [ ] Au moins deux modèles exportés avec leur version, leurs poids, leurs licences et leur configuration de prétraitement.
- [ ] Environnement ESP-IDF et runtime TensorFlow Lite Micro/Edge Impulse effectivement utilisé par le firmware, versions consignées.
- [ ] PPK2 et DevKit identifiés ; alimentation externe vérifiée. Pour le DevKit en source meter, PPK2 VOUT 5 V → broche 5 V et GND → GND selon la procédure validée. Ne pas transposer ce câblage à un autre montage.
- [ ] SOP-10 non utilisée comme raccourci : elle reste suspendue pour l'alimentation par pack AA.

Si le dataset ou un modèle exécutable manque, ne pas exécuter le benchmark et ne pas produire de résultat de substitution.

## 3. Protocole commun

Utiliser exactement le même jeu de test et les mêmes règles de décision pour tous les modèles. Consigner :

- identifiant du modèle, source, licence, hash du fichier et quantification ;
- dimensions, type et ordre des données d'entrée, normalisation et transformation couleur ;
- dimensions, type et signification de chaque sortie ;
- opérateurs requis, taille du modèle, tensor arena réellement allouée et RAM/PSRAM disponible ;
- fréquence MCU, version ESP-IDF/runtime, options de compilation et carte ;
- nombre d'images, répartition jour/nuit et classes, seuils de décision.

Ne pas présumer une entrée VGA 640×480×3, une sortie float, une classe à l'index 1 ou une arena de 512 KB. Lire ces propriétés depuis le modèle et le code effectivement compilés.

## 4. Vérifier le code de benchmark

L'ancien exemple `wn_edge_bench` inclus dans cette SOP était un template : il remplissait l'entrée avec `(i % 255)` et lisait `output->data.f` sans connaître le modèle. Sa prétendue sortie « 847,3 ms » était illustrative et n'est pas une mesure.

Avant toute exécution :

1. Remplacer les données factices par des images réelles et le prétraitement du modèle.
2. Vérifier le type quantifié de l'entrée et des sorties ; appliquer les paramètres de déquantification si nécessaires.
3. Vérifier le mapping des classes et les règles humain/animal/non-animal.
4. Dimensionner la tensor arena à partir de l'allocation réelle et enregistrer les échecs OOM.
5. Mesurer `Invoke()` avec `esp_timer_get_time()`, en distinguant si nécessaire prétraitement, inférence et post-traitement.
6. Effectuer des cycles de chauffe puis un nombre défini de répétitions ; rapporter médiane, p95, minimum et maximum.
7. Sauvegarder les prédictions et journaux bruts avec le hash du firmware et du modèle.

Un test sur données synthétiques peut vérifier la plomberie, mais il doit être marqué `SMOKE_ONLY` et exclu des métriques de détection et des affirmations de performance.

## 5. Qualité de détection

Pour chaque modèle et chaque sous-ensemble jour/nuit :

- calculer matrice de confusion, rappel et précision pour humain et animal ;
- compter séparément les humains non détectés, les animaux manqués et les fausses alertes animales sur végétation/scènes vides ;
- conserver les erreurs pour revue visuelle, sans publier d'images de personnes ;
- vérifier les seuils ADR-010 : rappel humain >90 % à 5 m le jour, >80 % à 5 m en IR nocturne, faux positifs humains sur faune <5 % ;
- documenter taille de l'échantillon et intervalle d'incertitude ; ne pas transformer un petit échantillon en garantie.

Le contrat d'alerte reste binaire animal/non-animal. Une éventuelle classification large ou d'espèce est hors exigence P0.

## 6. Mesure matérielle et énergie

1. Flasher le firmware de benchmark effectivement versionné sur le DevKit.
2. Débrancher l'USB avant l'alimentation externe si le montage validé l'exige ; ne jamais combiner deux sources sans schéma vérifié.
3. PPK2 éteint, connecter VOUT 5 V à la broche 5 V du DevKit et GND à GND ; vérifier polarité et configuration avant activation.
4. Acquérir veille, prétraitement, inférence, post-traitement, écriture SD et retour au sommeil.
5. Répéter sur un échantillon représentatif ; inclure les échecs et éventuels retries dans le scénario système.
6. Calculer l'énergie en Wh par intégration de `V(t) × I(t)`, et non à partir d'un simple courant moyen supposé.
7. Reporter la mesure par événement dans WP03, avec scénarios 10/30/72 événements/jour, IR, SD, audio et LoRa.

| Résultat par modèle | Valeur |
|---|---|
| Version/hash modèle et firmware | À renseigner |
| Rappel humain jour/nuit et effectif | À mesurer |
| Rappel/précision animal et effectif | À mesurer |
| Fausses alertes animales | À mesurer |
| Latence médiane/p95, avec périmètre | À mesurer |
| RAM/PSRAM et tensor arena | À mesurer |
| Énergie Wh par inférence et par cycle | À mesurer |
| Stabilité sur 20 inférences minimum | À mesurer |

## 7. Décision

Le modèle retenu doit satisfaire les seuils ADR-010, rester stable, tenir dans les ressources disponibles et être intégré au gate énergie WP03. Une latence supérieure à 2 s, un OOM, un rappel humain insuffisant ou une énergie incompatible déclenche l'arbitrage prévu par ADR-001/010 : optimisation, autre modèle ou migration MCU. Ne pas conclure automatiquement qu'un STM32U5 résout le problème.

## 8. Clôture

- [ ] Données, annotations et licences documentées.
- [ ] Comparaison d'au moins deux modèles sur le même jeu de test.
- [ ] Aucune donnée factice dans les métriques rapportées.
- [ ] Résultats jour/nuit et erreurs conservés.
- [ ] Latence, mémoire, stabilité et Wh mesurés sur ESP32-S3.
- [ ] Modèle retenu et seuils inscrits dans ADR-010/progress.md.
- [ ] Impact énergétique intégré à WP03 ; arbitrage réalisé si un critère échoue.
