# ADR-006 — Boîtier IP67 et montage terrain

**Date :** 2026-05-18
**Statut :** proposé
**Owner PKA :** Chouette
**Agent WildNexus :** `wildnexus-hardware-physical`
**Jalon :** M-01 Architecture P0 gelée

## Contexte

Le nœud WildNexus opère en milieu naturel belge : forêt, lisière, zones humides. Les conditions terrain imposent :

- températures de -10 °C à +45 °C selon la saison ;
- humidité relative fréquemment proche de 100 % (forêt, rosée, brouillard) ;
- pluie, neige et cycles gel/dégel ;
- montage sur tronc, poteau ou support végétal — sans outillage spécialisé ;
- interventions terrain rares (remplacement batterie, carte SD, maintenance silica gel).

L'étanchéité IP67 (immersion 1 m / 30 min) est le minimum requis. L'objectif terrain est d'atteindre IP67 sur le long terme, pas seulement à la sortie d'usine.

### Contrainte thermique — condensation

Le phénomène de condensation interne est le principal risque de défaillance à long terme sur un boîtier hermétique en environnement humide. Les cycles thermiques (nuit froide → jour chaud) créent une pression différentielle qui, combinée à l'humidité piégée au moment du scellage, dépose de l'eau sur les surfaces internes froides.

**Stratégie de mitigation retenue : chaleur passive ESP32-S3.**

Lors de chaque cycle actif (capture + inférence + transmission, 10–30 s à ~1.3 W), l'ESP32-S3 et la caméra dissipent suffisamment de chaleur pour maintenir la température interne au-dessus du point de rosée ambiant, à condition que :

1. le volume interne soit réduit (< 200 cm³) pour limiter la masse d'air à chauffer ;
2. les parois aient une isolation thermique minimale (mousse intérieure ou air-gap) pour retenir la chaleur entre les cycles ;
3. le boîtier soit orienté de façon à maximiser l'absorption solaire passible de jour (face sombre exposée).

En dernier recours — notamment lors de nuits longues à très basse fréquence d'événements — un **sachet de silica gel renouvelable** absorbe l'humidité résiduelle. Ce sachet est accessible sans outil à chaque intervention batterie.

Aucun chauffage actif n'est prévu : le coût énergétique serait incompatible avec le budget autonomie (ADR-005).

## Décision proposée

### Boîtier

Retenir un **boîtier ABS ou polycarbonate IP67 standard du commerce** pour le prototype P0 (Hammond, Spelsberg ou équivalent), avec les contraintes suivantes :

| Critère | Valeur cible |
|---------|-------------|
| Indice étanchéité | IP67 minimum |
| Volume interne | 150–250 cm³ |
| Dimensions externes | ≤ 150 × 100 × 60 mm |
| Joint torique | remplaçable, silicone |
| Matière | ABS ou PC (résistance UV, -40 °C à +80 °C) |
| Couleur | sombre (anthracite ou vert forêt) — absorption solaire passive + camouflage |
| Presse-étoupes | 2 minimum (antenne LoRa, câble panneau solaire) — IP67 après passage câble |
| Face plane | 1 face externe ≥ 110 × 75 mm pour montage panneau solaire 2 W (ADR-005) |

### Montage terrain

- Fixation par **sangle réglable UV-résistante** sur tronc ou poteau, sans perçage du boîtier principal.
- Orientation : face panneau solaire exposée au sud, caméra vers la zone d'observation.
- Hauteur standard de pose : 40–80 cm (observation faune au sol) ou 150–200 cm (oiseaux, passage).

### Gestion condensation

| Élément | Rôle | Intervalle remplacement |
|---------|------|------------------------|
| Silica gel 5 g (sachet) | Absorption humidité résiduelle | À chaque intervention batterie (~60 jours P0) |
| Joint torique silicone | Étanchéité périmètre couvercle | Inspection annuelle |
| Chaleur passive ESP32-S3 | Maintien température interne > point de rosée | Passif — aucune maintenance |

### Conformal coating PCB

Le PCB P0 reçoit un **vernis de protection acrylique standard** (spray du commerce, ~5 €) en couche légère sur les composants non-connecteurs. Pas de référence imposée P0 — spec précise (MG Chemicals 419C ou équivalent industriel) dès P1 production.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| Boîtier du commerce IP67 ABS/PC | Rapide, pas de moule, validé terrain, coût < 15 € | Moins compact qu'un boîtier sur-mesure, choix limité en couleur forêt | Retenu P0 |
| Boîtier impression 3D PETG + joint | Liberté de forme, adaptation exacte PCB | Étanchéité IP67 difficile à tenir long terme, UV, vieillissement | Rejeté P0 — option P1 sur-mesure |
| Boîtier moulé sur-mesure | Optimal P1/industrialisation | Délai, coût outillage, hors scope P0 | P1/P2 |
| Chauffage actif PTC anti-condensation | Robuste en conditions extrêmes | +0.5–1 W permanent → compromet autonomie 60 jours (ADR-005) | Rejeté — remplacé par stratégie passive |
| Desiccant permanent (cartouche étanche) | Longue durée sans intervention | Coût, volume, nécessite valve de remplacement | Option P1 si silica gel insuffisant |

## Sources primaires consultées

- Hammond Electronics série 1555 / 1591 — boîtiers IP67 ABS : https://www.hammfg.com
- Spelsberg TK series IP67 polycarbonate : https://www.spelsberg.com
- MG Chemicals 419C Acrylic Conformal Coating : https://www.mgchemicals.com/products/conformal-coatings/acrylic-conformal-coating/419c/
- Silica gel terrain : sachets 5 g standard, disponibles en vrac

## Conséquences

- WP02 (hardware) dimensionne le PCB pour tenir dans 150 × 100 mm maximum.
- WP02 prévoit les presse-étoupes LoRa et solaire dès le schéma mécanique.
- ADR-005 (énergie) : pas de poste heater dans le budget — stratégie passive validée.
- ADR-003 (radio) : l'antenne LoRa passe par presse-étoupe IP67 ou reste interne selon portée mesurée.
- Le conformal coating doit être appliqué avant assemblage final, pas après — documenter dans procédure assemblage P0.
- La couleur sombre (anthracite / vert) doit être confirmée compatible avec la plage de température boîtier en plein soleil d'été (risque surchauffe si + 45 °C ambiant + absorption solaire).

## Tests obligatoires avant acceptation

| Test | Critère minimal |
|------|----------------|
| Étanchéité IP67 | immersion 1 m / 30 min sans infiltration mesurable |
| Condensation interne simulée | cycle thermique -5 °C → +35 °C × 3 répétitions, pas de condensation sur PCB — 10 cycles = critère P1 |
| Chaleur passive ESP32-S3 | mesure température interne après 10 cycles actifs successifs à -5 °C ambiant |
| Montage terrain | fixation sangle sur tronc Ø 10–40 cm, stable sans glissement après 72 h |
| Presse-étoupe IP67 sous tension câble | pas d'infiltration après traction 5 N sur câble |
| Température interne max (soleil d'été) | ~~test M-02~~ — différé P1 ; hors-saison en Belgique au moment du proto, non bloquant pour EVT forêt |

## Critère de révision

Réviser cette ADR si :

- le PCB P0 final dépasse 150 × 100 mm et nécessite un boîtier plus grand ;
- la condensation interne persiste malgré la stratégie passive (déclenche l'évaluation du chauffage actif ou d'un desiccant cartouche) ;
- l'antenne LoRa interne (sans presse-étoupe) s'avère suffisante en portée terrain (simplifie le boîtier) ;
- le panneau solaire retenu en ADR-005 dépasse le format 110 × 69 mm.
