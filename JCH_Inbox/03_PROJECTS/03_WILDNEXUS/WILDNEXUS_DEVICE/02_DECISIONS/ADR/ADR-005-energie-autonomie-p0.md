# ADR-005 — Énergie et autonomie P0

**Date :** 2026-05-18  
**Dernière mise à jour :** 2026-11-05 — correction datasheet, sécurité d'entrée et statut des preuves
**Statut :** accepté pour l'architecture — autonomie et sécurité du pack non validées (révision v0.3 ; décision JCH historique : batteries AA standard)
**Owner PKA :** [[Bruno]] + [[Chouette]]  
**Agent WildNexus :** `wildnexus-hardware-physical`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

P0 vise un nœud caméra autonome opérationnel 60 jours sans intervention humaine, sur batterie seule, en milieu naturel belge (température cible : -10 °C à +45 °C, humidité élevée). Cette autonomie est un critère de sortie à mesurer, pas une performance déjà démontrée.

Le MCU retenu est l'[[ESP32-S3]] (ADR-001). Profil énergétique :

| Mode | Courant @ 3.3 V |
|------|----------------|
| CPU actif @ 240 MHz | 240–300 mA |
| Deep sleep ULP | 10–20 µA (MCU seul) |

Consommateurs externes principaux : caméra (~50–80 mA), [[LoRa]] TX (~120 mA, ~2 s), microSD (~50–100 mA), LEDs IR (~300–500 mA, pulsé < 5 s). Système event-driven : pleine charge 10–30 s par événement seulement.

## Décision

### Batterie P0 — 8 × AA standard, fourni par l'utilisateur

Adopter le **modèle industrie caméra de chasse** : 8 piles AA logées dans le compartiment arrière du boîtier, fournies et gérées par l'utilisateur.

**Rationale :**
- Supprime entièrement la conception BMS, circuit de charge et MPPT du PCB
- Piles AA disponibles partout — aucun risque supply chain
- Coût de production réduit ; coût opérationnel reporté sur l'utilisateur (standard industrie)
- Eneloop Pro opérationnelles à −20 °C — meilleures que LiFePO4 en froid extrême
- Energizer Ultimate Lithium L91 AA : chimie lithium–disulfure de fer (Li-FeS2), 1,5 V nominal — ne pas confondre avec les piles Li-SOCl2. Capacité et tension maximale doivent être prises dans la fiche fabricant et vérifiées au banc.

**Configuration électrique : 4S2P** (4 cellules en série × 2 groupes parallèles)

| Paramètre | NiMH rechargeable (Eneloop Pro) | Alcaline (Energizer) | Lithium (Energizer Ultimate) |
|-----------|--------------------------------|---------------------|------------------------------|
| Tension nominale | 4.8 V | 6.0 V | 6.0 V |
| Capacité totale | ~5 000 mAh | ~5 000 mAh | ~7 000 mAh |
| Énergie totale | ~24 Wh | ~30 Wh | ~42 Wh |
| Température min. | −20 °C | −18 °C | −40 °C |
| Précédent LiFePO4 2×18650 | — | — | ~12.8 Wh (référence) |

L'énergie disponible est **2 à 3 fois supérieure** à l'ancienne solution LiFePO4 18650.

**Budget autonomie :**

Les anciennes extrapolations sont retirées : elles ne couvraient pas tous les cycles audio, le rendement de conversion, le froid, les retransmissions ni les profils jour/nuit. Elles mélangeaient également une capacité en mAh à la tension du pack avec des consommations à 3,3 V.

WP03 est désormais la seule procédure de calcul autorisée. Le scénario de référence est 10 événements/jour ; 30 et 72 événements/jour servent de scénarios de robustesse. Le calcul doit être mené en Wh à la batterie, avec capacité utilisable déclassée et mesures PPK2. À titre de cohérence dimensionnelle, 7 000 mAh à 6 V nominal représentent environ 42 Wh, et non 7 000 mAh disponibles à 3,3 V.

### Régulation tension — buck converter basse consommation

| Paramètre | Valeur |
|-----------|--------|
| Entrée | Plage recommandée TI 1,8–6,5 V ; compatibilité du pack 4S2P à démontrer sur toute sa plage réelle |
| Sortie | 3.3 V régulé, à vérifier sous pics |
| Composant recommandé | TPS62840 (Texas Instruments) — Iq typique 60 nA ; rendement à mesurer à chaque niveau de charge |
| Courant de sortie max | 750 mA maximum composant — suffisance pour les pics combinés [[ESP32-S3]] + périphériques à valider |
| Courant quiescent | 60 nA typique pour le circuit intégré seul — la consommation de la carte complète reste à mesurer |

### Gate de sécurité électrique — obligatoire avant tout essai pack

- **Ne jamais utiliser 6 AA en série (~9 V nominal)** sur le TPS62840 : cette ancienne instruction SOP-10 dépasse la plage recommandée de 6,5 V.
- **Ne pas connecter le pack 4S2P L91** tant que la tension maximale de piles neuves, les tolérances et le fonctionnement à froid n'ont pas démontré une entrée toujours ≤6,5 V. Si cette marge n'est pas démontrée, rouvrir la topologie du pack ou le régulateur avant tout essai.
- **Ne pas injecter 3,3 V dans la broche 5 V d'un DevKit.** Le point d'injection et le câblage PPK2 doivent être validés sur le schéma exact de la carte.
- SOP-10 reste suspendue tant que ces trois points ne sont pas levés et consignés dans le protocole.

### Gestion des périphériques — coupure MOSFET individuelle

Inchangé : chaque périphérique à forte consommation (caméra, [[LoRa]], microSD, LEDs IR) coupé physiquement via MOSFET P-channel entre les cycles actifs.

Objectif deep sleep carte complète : **< 100 µA** (MCU + buck converter + leakage MOSFETs).

### LEDs IR — mode pulsé uniquement

Inchangé : < 5 s par événement, aucun éclairage continu.

### Solaire — différé P1

Le solaire n'est pas dans le scope P0. Le boîtier (ADR-006) prévoit mécaniquement la possibilité d'un panneau externe en P1, sans contraindre le design P0.

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| **8 × AA standard (utilisateur)** | Zéro BMS, supply universel, énergie supérieure, modèle industrie éprouvé | Coût opérationnel utilisateur | **Retenu P0 — décision JCH 2026-05-18** |
| 2 × 18650 LiFePO4 | Compact, rechargeable intégré | BMS requis, circuit de charge, supply chain, 2× moins d'énergie | Remplacé par AA |
| 2 × 18650 Li-Ion | Densité énergie | Risque thermique IP67, froid | Écarté |
| Pack LiPo souple | Volume flexible | Gonflage froid, soudure | Écarté |
| Solaire P0 | Autonomie longue durée | Complexité PCB, non nécessaire avec AA | Différé P1 |

## Conséquences

- **WP02 (hardware)** : supprimer BMS, CN3791, connecteur de charge du schéma. Ajouter TPS62840 (ou équivalent) + support 8× AA 4S2P. Conserver MOSFET de coupure périphériques.
- **ADR-006 (boîtier)** : prévoir compartiment AA accessible sans outil côté terrain — dimension standard holder 4×AA × 2 groupes.
- **WP03 (firmware)** : monitoring tension batterie via ADC [[ESP32-S3]] sur diviseur résistif (4.8 V → 3.3 V plage ADC). Seuils d'alerte : < 4.0 V = batterie faible, < 3.6 V = coupure préventive.
- **Supply register** : remplacer LiFePO4 18650 + CN3791 par holders AA + TPS62840. Piles non achetées par le projet.
- **Budget** : économie ~30–40 € sur composants batterie/charge. Les piles ne sont pas dans l'enveloppe 1 000 €.
- Le benchmark M-02 mesure le courant deep sleep carte complète avant tout autre test.

## Tests obligatoires pour la validation M-02

L'acceptation de l'architecture ne signifie pas que ces tests sont déjà réussis.

| Test | Critère minimal |
|------|----------------|
| Courant deep sleep carte complète (tous MOSFET coupés) | < 100 µA mesuré au Nordic PPK2 |
| Courant deep sleep sans MOSFET (référence) | documenté |
| Cycle complet réveil → capture → stockage → [[LoRa]] TX → sommeil | énergie totale < 1.5 mAh par événement |
| Autonomie simulée 1 événement/heure | calcul vérifié par mesure capacité résiduelle J+7 |
| LEDs IR en mode pulsé | durée flash ≤ 5 s, courant pic documenté |
| Tension buck converter sous charge pic | régulation stable 3.3 V ± 3 % pendant cycle actif |

## Critère de révision

Réviser cette ADR si :

- le deep sleep carte complète dépasse 200 µA de façon non réductible ;
- la fréquence réelle terrain dépasse 5/heure de façon continue sur le site EVT ;
- le TPS62840 ne supporte pas le pic de courant carte complète ;
- la tension maximale du pack 4S2P ne laisse pas une marge démontrée dans la plage d'entrée recommandée du régulateur.

Tout changement de topologie batterie ou de régulateur exige une révision explicite de cette ADR et de SOP-10 avant essai.
