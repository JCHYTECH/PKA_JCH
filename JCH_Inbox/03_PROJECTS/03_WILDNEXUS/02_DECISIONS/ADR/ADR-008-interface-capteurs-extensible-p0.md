# ADR-008 — Interface capteurs extensible P0

**Date :** 2026-05-23  
**Statut :** accepté  
**Owner PKA :** Castor  
**Agent WildNexus :** `wildnexus-program-manager-system-architect`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

WildNexus doit préserver l'évolution multi-capteurs sans transformer le P0 en station scientifique complète.

## Décision

Le Satellite Lite P0 intègre :

- caméra OV5640/IR ;
- PIR ;
- micro mono pour clips audio courts locaux ;
- mesure tension batterie ;
- interface I2C/SPI/UART documentée pour extensions ;
- réserve d'encombrement et de fixation pour un petit bloc capteurs environnementaux.

Les capteurs suivants doivent être pris en compte dans l'encombrement P0, même s'ils ne sont pas tous montés dès le premier prototype :

- BME688 ou équivalent air/température/humidité/pression ;
- AS7341 ou équivalent lumière/spectral/lux ;
- GPS/GNSS compact, réservé P1/Smart sauf besoin terrain démontré ;
- audio scientifique avancée ;
- ultrasons, thermique, sol/eau, mmWave.

Principe JCH : **moins on change de choses après le P0, mieux c'est**. Le boîtier, le PCB et les accès internes doivent donc prévoir une marge réaliste pour ces capteurs, sans les rendre obligatoires fonctionnellement en P0.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| Capteurs minimaux + bus documenté + volume réservé | limite P0, préserve futur, réduit les changements boîtier/PCB | nécessite discipline d'interface et estimation mécanique | retenu |
| Station multi-capteurs complète P0 | valeur scientifique immédiate | scope creep, énergie, boîtier, firmware | rejeté |
| Aucun micro P0 | simplicité | ferme trop la trajectoire bioacoustique | rejeté |

## Conséquences

- Le micro mono devient standard P0, mais pas la reconnaissance bioacoustique.
- Le PCB doit réserver au moins une interface capteur proprement documentée et un emplacement physique pour petit module capteurs.
- L'estimation d'encombrement WP02 doit inclure le bloc capteurs, même si certaines pièces sont non montées en P0.
- Les métadonnées doivent pouvoir accueillir des champs futurs sans migration lourde.
- Toute évolution P1 doit viser compatibilité mécanique avec le boîtier P0, sauf raison technique forte documentée.

## Critère de révision

Réviser si l'intégration micro ou la réserve capteurs compromet l'autonomie, l'étanchéité, le stockage, la stabilité firmware P0 ou impose un boîtier trop grand pour le terrain.
