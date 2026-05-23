# ADR-002 — Choix caméra / IR P0

**Date :** 2026-05-18
**Statut :** accepté — 2026-05-18
**Owner PKA :** Nova + Lynx
**Agent WildNexus :** `wildnexus-camera-imaging`
**Jalon :** M-01 Architecture P0 gelée

## Contexte

P0 doit produire une image de qualité équivalente aux meilleurs pièges photographiques du marché (Reconyx, Browning haut de gamme), de jour comme de nuit, sans architecture Linux permanente.

Les meilleurs pièges photo professionnels reposent sur un capteur 5–12 MP réels couplé à une optique de qualité — pas sur les mégapixels interpolés affichés en marketing. L'OV5640 5 MP en configuration M12 mount avec une lentille IR-corrigée f/1.8 atteint ce niveau de performance, tout en restant compatible natif avec l'ESP32-S3 via interface DVP (ADR-001 accepté).

La décision sépare deux composants distincts à sourcer séparément :

1. **Capteur image** — OV5640 5 MP, module M12 mount, interface DVP
2. **Lentille** — M12 IR-corrigée f/1.8, sourcing qualité indépendant du module capteur

## Décision

### Capteur : OV5640 5 MP — module M12 mount — interface DVP

Retenir l'**OV5640 5 MP en format M12 mount avec interface DVP** comme capteur P0.

| Paramètre | Valeur |
|-----------|--------|
| Capteur | OmniVision OV5640 |
| Résolution max | 5 MP (2592 × 1944) |
| Résolutions configurables | 5 MP / 3 MP / 1080p / 720p / VGA |
| Interface hôte | DVP (Digital Video Port) — natif ESP32-S3 |
| Format monture | M12 (S-mount) — lentille interchangeable |
| Sensibilité IR | capteur NoIR (sans filtre IR-cut intégré) ou avec IR-cut motorisé |
| Fournisseur primaire | Arducam OV5640 M12 DVP |
| Alternative | Module OV5640 M12 générique (Mouser, AliExpress pro) |

La résolution est configurable par firmware selon le besoin : 5 MP pour les captures événementielles sauvegardées, résolution réduite (VGA) pour l'inférence embarquée animal / non-animal.

### Lentille : M12 IR-corrigée f/1.8 — sourcing séparé

La lentille est une décision d'achat indépendante du module capteur. Elle doit obligatoirement être **IR-corrigée** : sans correction IR, le plan focal se décale entre lumière visible (jour) et IR 850/940 nm (nuit), rendant les images nocturnes floues quelle que soit la qualité du capteur.

| Paramètre | Valeur cible |
|-----------|-------------|
| Monture | M12 (S-mount) |
| Ouverture | f/1.8 minimum |
| Distance focale | 4–6 mm (champ ~60–90°) pour couverture terrain standard |
| Correction IR | obligatoire (850 nm et 940 nm) |
| Distance mise au point min. | < 1 m |
| Fournisseur primaire | Lensation (DE) ou Evetar (EU) |
| Prix indicatif | 25–50 € |
| Validation qualité | recherche documentaire web en priorité (forums, benchs publiés) avant validation bench prototype |
| Critère de choix final | si l'écart technique entre fournisseurs est faible, retenir le plus robuste au meilleur rapport qualité/prix — ne pas sur-spécifier |

### Éclairage IR nocturne

LEDs IR en mode **pulsé uniquement** sur déclenchement (< 5 s par capture), conformément à ADR-005 et ADR-006.

- Exigence faune : la longueur d'onde doit être choisie pour être **non visible ou non perturbante pour les animaux cibles**, pas seulement peu visible pour l'humain.
- Longueur d'onde candidate : **850 nm** (portée supérieure, mais lueur rouge visible et potentiel de perception par certaines espèces)
- Alternative candidate : **940 nm** (beaucoup plus discrète, portée inférieure, contrainte plus forte sur puissance / optique / sensibilité capteur)
- Décision ouverte : le type précis de LED IR doit être déterminé avant achat, en croisant perception spectrale des espèces cibles, portée terrain, sensibilité OV5640 NoIR et consommation.
- Choix final 850 vs 940 nm, ou autre longueur d'onde IR disponible : à trancher sur revue documentaire + test terrain avant M-02.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| OV5640 5 MP M12 DVP + lentille qualité | Natif ESP32-S3, résolution configurable, lentille interchangeable, communauté active | Sensibilité nocturne inférieure aux STARVIS Sony | **Retenu P0** |
| IMX462 MIPI (Sony STARVIS) | Excellente basse lumière, 2 MP mais qualité image remarquable | MIPI non natif ESP32-S3, ISP dédié requis, complexité P0 | P1 si OV5640 insuffisant nuit |
| IMX327 MIPI + ISP | Très bonne sensibilité nocturne | Même problème MIPI + ISP ; hors portée MCU seul | P1/P2 |
| OV5640 monobloc (lentille fixe collée) | Moins cher, plus compact | Lentille non remplaçable, qualité optique limitée, pas IR-corrigé | Rejeté — qualité insuffisante |
| OV2640 2 MP | Très simple, bon marché | Résolution insuffisante pour cible qualité piège photo | Baseline référence seulement |
| ArduCAM Mega SPI 5MP | Interface SPI simple | Lentille intégrée non remplaçable, qualité optique non maîtrisée | Rejeté — même raison |

## Sources primaires consultées

- OmniVision OV5640 datasheet : https://www.ovt.com/products/ov5640/
- Arducam OV5640 M12 DVP : https://www.arducam.com
- Lensation M12 IR-corrected lenses : https://www.lensation.de
- Evetar M12 lenses : https://www.evetar.com
- Espressif ESP32-S3 camera DVP interface : https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/camera_driver.html

## Conséquences

- WP02 (hardware) intègre le module OV5640 M12 DVP sur le schéma PCB avec connecteur nappe DVP 24 broches.
- Le supply register doit avoir deux lignes distinctes : capteur OV5640 M12 + lentille M12 IR-corrigée.
- La lentille est commandée séparément du module — prévoir délai fournisseur EU (Lensation : 3–7 jours).
- ADR-006 (boîtier) doit prévoir une fenêtre optique plate traitée anti-reflet, alignée sur le module M12.
- La résolution de capture (5 MP) et la résolution d'inférence (VGA) sont configurées par firmware — deux modes documentés dans WP03.
- Le choix 850 nm vs 940 nm IR est un test terrain, pas une décision de conception bloquante pour P0.

## Tests obligatoires avant acceptation M-02

| Test | Critère minimal |
|------|----------------|
| Image jour à 5 m | animal ou mire naturaliste nettement identifiable |
| Image nuit IR 850 nm à 5 m | détail suffisant pour valider présence animal / non-animal |
| Visibilité faune de l'IR | longueur d'onde validée comme non visible ou non perturbante pour les espèces cibles |
| Comparaison résolution 5 MP vs 3 MP vs VGA | différence documentée pour choix firmware |
| Mise au point jour vs nuit (IR-correction) | pas de dérive de mise au point entre les deux modes |
| Cycle réveil → capture → stockage → extinction | énergie < 1.5 mAh par cycle (ADR-005) |
| Fenêtre boîtier | pas de reflet IR dominant sur l'image nocturne |

## Critère de révision

Réviser cette ADR si :

- l'OV5640 montre une sensibilité nocturne insuffisante pour l'identification d'espèces à 5 m ;
- la revue faune montre que la longueur d'onde IR candidate est visible ou perturbante pour les espèces cibles ;
- une intégration IMX462 MIPI sans ISP externe devient accessible sur ESP32-S3 ;
- la lentille M12 IR-corrigée retenue introduit une aberration chromatique mesurable à f/1.8 — les aberrations seront observées et documentées pendant le prototype ; la correction optique (profil calibration) est une tâche post-prototype ;
- le boîtier IP67 retenu (ADR-006) ne permet pas une fenêtre optique compatible M12 sans reflets.
