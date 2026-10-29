# ADR-007 — Détection événementielle P0

**Date :** 2026-05-23  
**Statut :** accepté  
**Owner PKA :** [[Nova]] + [[Forge]]  
**Agent WildNexus :** `wildnexus-edge-ai-cv`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

P0 doit prouver un Satellite Lite autonome, pas une station d'IA complète. Les dépôts [[inbox]] confirment que YOLO moderne et [[BirdNET]] complet ne sont pas réalistes sur [[ESP32-S3]] en P0.

## Décision

Retenir une détection P0 en trois niveaux :

1. **PIR basse consommation** comme déclencheur principal.
2. **Capture image et audio court** après événement.
3. **Préfiltrage simple embarqué** : animal / non-animal ou score de présence, sans reconnaissance d'espèce.

YOLO, [[BirdNET]], reconnaissance espèce fine et analyse bioacoustique lourde sont exclus du Satellite Lite P0. Ces traitements appartiennent à Base/Master Nexus P1 ou à un Satellite Smart futur.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|---|---|---|---|
| PIR + préfiltrage simple | basse consommation, réaliste [[ESP32-S3]] | classification limitée | retenu |
| YOLO sur [[ESP32-S3]] | séduisant pour autonomie analytique | RAM/CPU/vidéo insuffisants pour fiabilité terrain | rejeté P0 |
| [[BirdNET]] sur [[ESP32-S3]] | valeur scientifique forte | non réaliste pour reconnaissance complète P0 | rejeté P0 |
| Analyse sur Base/Master | puissance suffisante | dépend d'une brique P1 | retenu P1 |

## Conséquences

- P0 stocke les raws locaux et transmet seulement métadonnées/alertes [[LoRa]].
- Les seuils de détection doivent être ajustables sans reflasher tout le firmware.
- Les données collectées P0 servent à entraîner ou valider les modèles P1.

## Critère de révision

Réviser si un modèle embarqué ultra-léger démontre sur banc et terrain un gain net sans compromettre autonomie, stabilité et simplicité firmware.
