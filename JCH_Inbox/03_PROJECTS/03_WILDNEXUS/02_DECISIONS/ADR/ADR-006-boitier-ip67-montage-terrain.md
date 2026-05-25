# ADR-006 — Boîtier IP67 et montage terrain

**Date :** 2026-05-18  
**Dernière mise à jour :** 2026-05-25  
**Statut :** Accepté
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
- camouflage réel : limiter la détectabilité visuelle du boîtier par la couleur, la forme et l'intégration au support.

L'étanchéité IP67 (immersion 1 m / 30 min) est le minimum requis. L'objectif terrain est d'atteindre IP67 sur le long terme, pas seulement à la sortie d'usine.

### Contrainte thermique — condensation

Le phénomène de condensation interne est le principal risque de défaillance à long terme sur un boîtier hermétique en environnement humide. Les cycles thermiques (nuit froide → jour chaud) créent une pression différentielle qui, combinée à l'humidité piégée au moment du scellage, dépose de l'eau sur les surfaces internes froides.

**Stratégie de mitigation retenue : chaleur passive ESP32-S3.**

Lors de chaque cycle actif (capture + inférence + transmission, 10–30 s à ~1.3 W), l'ESP32-S3 et la caméra dissipent suffisamment de chaleur pour maintenir la température interne au-dessus du point de rosée ambiant, à condition que :

1. le volume interne soit réduit (< 200 cm³) pour limiter la masse d'air à chauffer ;
2. les parois aient une isolation thermique minimale (mousse intérieure ou air-gap) pour retenir la chaleur entre les cycles ;
3. le boîtier profite d'une couleur verte ou sombre sans créer de surchauffe excessive.

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
| Couleur | vert forêt prioritaire ; anthracite seulement si disponibilité/thermique meilleure |
| Presse-étoupes | 1 minimum pour antenne LoRa externe si nécessaire ; emplacements réservés P1 possibles |
| Face plane | utile pour extension P1, mais panneau solaire non requis P0 |

Le P0 doit aussi produire une **estimation sérieuse des dimensions finales** après verrouillage des choix hardware : PCB, holder 8× AA, caméra, PIR, micro, microSD, bloc capteurs, antenne LoRa, joints, accès maintenance et réserve P1. Cette estimation devient un livrable de fin M-01 avant achat boîtier définitif.

### Boîtier P1 — impression 3D forme organique (décision retenue)

JCH dispose d'une imprimante 3D. Le boîtier P1 sera réalisé par impression 3D avec une forme organique conçue pour maximiser le camouflage terrain. Cette décision est ferme.

Principes retenus :

- **Forme organique** : silhouette non rectangulaire, imitant un élément naturel (souche, nœud de bois, pierre, accumulation d'écorce) plutôt qu'un boîtier technique visible ;
- **Ajouts type branches et excroissances** : des éléments rapportés (branches, brindilles, reliefs d'écorce, mousses simulées) sont intégrés à la conception ou fixés en post-impression pour briser la silhouette et fondre le boîtier dans son environnement immédiat ;
- **Dos arrondi** : la face arrière du boîtier est concave/arrondie pour s'adapter à la rotondité naturelle des troncs et poteaux — principale configuration de pose terrain. Cette géométrie remplace les patins souples et le berceau intermédiaire envisagés pour un boîtier commerce ;
- **Textures de surface** : écorce, grain de bois, mousse ou pierre selon le biotope cible — imprimées directement ou appliquées en post-traitement ;
- **Adaptabilité biotope** : la conception modulaire permet de varier la peau externe selon l'environnement (forêt de feuillus, conifères, zone humide, lisière pierreuse) sans modifier le cœur électronique ;
- **Matériau** : PETG ou ASA pour résistance UV et cycles thermiques — IP67 à atteindre par conception des joints et assemblage, validé par test avant déploiement P1.

Hypothèse produit à confirmer en P1 : **cœur électronique standardisé + enveloppe organique variable selon biotope**. Si la détectabilité terrain est significativement réduite, cette approche constitue une différenciation produit sérieuse.

### Montage terrain

- Fixation par **sangle réglable UV-résistante** sur tronc ou poteau, sans perçage du boîtier principal.
- Orientation : caméra vers la zone d'observation ; éventuelle face extension P1 exposée au sud si solaire ajouté plus tard.
- Hauteur standard de pose : 40–80 cm (observation faune au sol) ou 150–200 cm (oiseaux, passage).
- Le dos du boîtier ou de son support doit tenir compte de la **rotondité des troncs et poteaux** : surface arrière concave, patins souples, rainures de sangle ou berceau intermédiaire pour maximiser le calage et éviter la rotation.
- Les sangles doivent rester discrètes : couleur verte/brune/noire mate, largeur suffisante, pas de pièces brillantes visibles.

### Antenne LoRa

L'antenne LoRa doit être **la moins visible possible**.

Ordre de préférence :

1. antenne intégrée dans le boîtier si la portée terrain reste acceptable ;
2. antenne dissimulée dans une excroissance ou un relief du boîtier ;
3. antenne externe camouflée en branche, tige ou élément naturel ;
4. antenne fouet visible seulement si les tests RF démontrent que les options discrètes échouent.

Cette contrainte ne doit pas dégrader la conformité radio, l'étanchéité ni la portée minimale EVT. Elle impose un test RF comparatif entre antenne interne, antenne dissimulée et antenne externe classique.

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
| Boîtier impression 3D + joint | Liberté de forme, adaptation exacte PCB, camouflage organique, dos arrondi natif, ajouts branches | Étanchéité IP67 à qualifier sur joint et assemblage, matériau PETG/ASA à valider | **Rejeté P0 — Retenu P1 (décision ferme JCH 2026-05-25)** |
| Boîtier standard + skin camouflage | Standardise le cœur, adapte l'apparence au lieu | Interface peau/boîtier à concevoir, risque rétention eau/saleté, moins organique | Subsumé par la décision impression 3D P1 |
| Antenne intégrée / camouflée | Très faible détectabilité | portée RF à prouver, contraintes matière/orientation | À tester P0/P1 |
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
- WP02 produit une estimation dimensionnelle complète après choix hardware avant verrouillage boîtier P0, incluant la réserve capteurs définie dans ADR-008.
- WP02 prévoit le passage antenne LoRa si nécessaire et réserve mécaniquement les extensions P1 sans les rendre obligatoires P0.
- WP02 et WP05 doivent tester le calage sur supports ronds : tronc, poteau, support irrégulier.
- WP05 doit inclure une observation de détectabilité terrain : couleur, silhouette, reflets, sangle et antenne.
- ADR-005 (énergie) : pas de poste heater dans le budget — stratégie passive validée.
- ADR-003 (radio) : l'antenne LoRa reste interne ou camouflée si la portée mesurée est suffisante ; presse-étoupe externe seulement si nécessaire.
- Le conformal coating doit être appliqué avant assemblage final, pas après — documenter dans procédure assemblage P0.
- La couleur verte doit être confirmée compatible avec la plage de température boîtier en plein soleil d'été (risque surchauffe si + 45 °C ambiant + absorption solaire).

## Tests obligatoires avant acceptation

| Test | Critère minimal |
|------|----------------|
| Étanchéité IP67 | immersion 1 m / 30 min sans infiltration mesurable |
| Condensation interne simulée | cycle thermique -5 °C → +35 °C × 3 répétitions, pas de condensation sur PCB — 10 cycles = critère P1 |
| Chaleur passive ESP32-S3 | mesure température interne après 10 cycles actifs successifs à -5 °C ambiant |
| Montage terrain | fixation sangle sur tronc Ø 10–40 cm, stable sans glissement après 72 h |
| Calage sur support rond | pas de rotation significative après traction manuelle et 72 h de pose |
| Détectabilité visuelle | revue terrain : couleur, silhouette, antenne et sangle non saillantes à distance d'observation raisonnable |
| Antenne LoRa discrète | comparer antenne interne/camouflée/externe ; retenir la moins visible atteignant la portée EVT |
| Presse-étoupe IP67 sous tension câble | pas d'infiltration après traction 5 N sur câble |
| Température interne max (soleil d'été) | ~~test M-02~~ — différé P1 ; hors-saison en Belgique au moment du proto, non bloquant pour EVT forêt |

## Critère de révision

Réviser cette ADR si :

- le PCB P0 final dépasse 150 × 100 mm et nécessite un boîtier plus grand ;
- la condensation interne persiste malgré la stratégie passive (déclenche l'évaluation du chauffage actif ou d'un desiccant cartouche) ;
- l'antenne LoRa interne ou camouflée n'atteint pas la portée terrain minimale ;
- le calage sur tronc impose une géométrie arrière différente du boîtier commerce retenu ;
- le potentiel produit "skin camouflage" justifie une ADR P1 dédiée ;
- une extension solaire P1 impose un format ou une étanchéité incompatible avec le boîtier retenu.
