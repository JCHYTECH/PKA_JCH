# ADR-001 — Choix MCU P0

**Date :** 2026-05-18  
**Statut :** accepté — 2026-05-18 (confirmé par JCH : ESP32-S3 retenu sur coût / performances / disponibilité / communauté)  
**Owner PKA :** Castor + Forge  
**Agent WildNexus :** `wildnexus-firmware-ulp`  
**Jalon :** M-01 Architecture P0 gelée  

## Contexte

P0 doit prouver un noeud caméra autonome : veille basse consommation, réveil événementiel, capture image, filtre animal / non-animal, stockage local, configuration terrain simple et transmission LPWAN événementielle.

Le MCU doit donc couvrir trois contraintes qui tirent dans des directions différentes :

- basse consommation réelle sur cycle complet ;
- intégration caméra / stockage / radio sans complexité excessive ;
- vitesse de prototypage suffisante pour M-02.

Le P0 ne doit pas dépendre d'un Raspberry Pi ou d'un Linux permanent.

## Décision proposée

Retenir **ESP32-S3 comme MCU candidat primaire pour le prototype P0 M-02**, avec une règle de sortie stricte :

- ESP32-S3 reste le choix P0 si le budget énergie complet démontre l'objectif de 60 jours batterie seule ;
- STM32U5 reste le fallback basse consommation si ESP32-S3 échoue sur autonomie, stabilité veille/réveil ou robustesse firmware ;
- nRF54L15 est conservé comme option BLE / 2.4 GHz future, mais non prioritaire P0 car il ne résout pas directement le besoin caméra + LPWAN.

Raison : ESP32-S3 combine une interface caméra documentée, BLE/Wi-Fi utiles au provisioning, sécurité embarquée, outillage mature et vitesse de prototypage. Le risque principal est énergétique ; il doit être mesuré tôt, pas supposé résolu.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| ESP32-S3 | Interface caméra, BLE/Wi-Fi, USB, SPI/I2C/UART, ULP, secure boot, écosystème rapide | Consommation à prouver ; Wi-Fi à désactiver en usage terrain ; besoin probable de PSRAM | Candidat primaire P0 |
| STM32U5 | Très basse consommation, sécurité, mémoire élevée selon variante, meilleure trajectoire produit terrain | Intégration caméra et stack applicative plus exigeantes ; prototypage plus lent | Fallback si ESP32-S3 échoue énergie |
| nRF54L15 | Excellente trajectoire BLE basse consommation, sécurité, coprocesseur RISC-V, provisioning terrain solide | Radio 2.4 GHz seulement ; ne remplace pas LPWAN ; intégration caméra moins directe | Option future / provisioning |
| Raspberry Pi / Linux permanent | Développement logiciel rapide, caméra facile, IA plus confortable | Consommation, boot, SD, maintenance, autonomie incompatibles avec la philosophie P0 | Rejeté pour noeud terrain P0 |

## Sources primaires consultées

- Espressif ESP32-S3 : https://www.espressif.com/en/products/socs/esp32s3/docs
- STMicroelectronics STM32U5 : https://www.st.com/en/microcontrollers-microprocessors/stm32u5-series.html
- Nordic nRF54L15 : https://www.nordicsemi.com/Products/nRF54L15

## Conséquences

- WP03 doit produire une machine d'états firmware centrée sur veille, réveil, capture, stockage, transmission et retour sommeil.
- WP03 doit désactiver Wi-Fi hors configuration ou maintenance.
- WP02 doit prévoir PSRAM / flash / microSD selon le pipeline caméra retenu.
- ADR-002 caméra doit éviter de choisir un module qui force Linux ou USB host lourd sans justification.
- ADR-003 radio doit rester découplé du MCU principal via SPI/UART pour permettre un fallback STM32U5.

## Tests obligatoires avant acceptation

| Test | Critère minimal |
|---|---|
| Courant deep sleep carte complète | compatible avec budget 60 jours batterie seule |
| Réveil événementiel → capture → stockage → sommeil | cycle stable sur 100 répétitions banc — 1 000 cycles = critère P1 |
| Capture image utilisable | image exploitable à 5 m de jour et de nuit selon ADR-002 |
| Transmission LPWAN courte | paquet événement transmis puis retour sommeil |
| Provisioning terrain | configuration BLE ou autre méthode sans ordinateur portable |

## Critère de révision

Réviser cette ADR si :

- ESP32-S3 ne tient pas le budget énergie complet ;
- l'interface caméra retenue impose un host que l'ESP32-S3 ne peut pas gérer proprement ;
- STM32U5 démontre une intégration caméra/stockage/radio suffisamment rapide pour M-02 ;
- le coût ou la disponibilité ESP32-S3 devient bloquant pour 5 prototypes.
