# ADR-005 — Énergie et autonomie P0

**Date :** 2026-05-18  
**Statut :** accepté — 2026-05-18 (révision v0.2 — décision JCH : batteries AA standard, modèle industrie caméra de chasse)  
**Owner PKA :** [[Bruno]] + [[Chouette]]  
**Agent WildNexus :** `wildnexus-hardware-physical`  
**Jalon :** M-01 Architecture P0 gelée

## Contexte

P0 doit démontrer un nœud caméra autonome opérationnel 60 jours sans intervention humaine, sur batterie seule, en milieu naturel belge (température : -10 °C à +45 °C, humidité élevée).

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
- Energizer Ultimate Lithium AA : 3 500 mAh @ 1.5 V — énergie supérieure à toute solution 18650

**Configuration électrique : 4S2P** (4 cellules en série × 2 groupes parallèles)

| Paramètre | NiMH rechargeable (Eneloop Pro) | Alcaline (Energizer) | Lithium (Energizer Ultimate) |
|-----------|--------------------------------|---------------------|------------------------------|
| Tension nominale | 4.8 V | 6.0 V | 6.0 V |
| Capacité totale | ~5 000 mAh | ~5 000 mAh | ~7 000 mAh |
| Énergie totale | ~24 Wh | ~30 Wh | ~42 Wh |
| Température min. | −20 °C | −18 °C | −40 °C |
| Précédent LiFePO4 2×18650 | — | — | ~12.8 Wh (référence) |

L'énergie disponible est **2 à 3 fois supérieure** à l'ancienne solution LiFePO4 18650.

**Budget autonomie recalculé :**

| Fréquence événements | Conso/jour | Autonomie NiMH 5 Ah | Autonomie Lithium 7 Ah |
|---------------------|-----------|--------------------|-----------------------|
| 1 /heure | ~29 mAh | ~172 jours ✅ | ~241 jours ✅ |
| 3 /heure | ~87 mAh | ~57 jours ✅ | ~80 jours ✅ |
| 5 /heure | ~145 mAh | ~34 jours ⚠️ | ~48 jours ⚠️ |

L'objectif 60 jours est atteint confortablement jusqu'à 3 événements/heure avec NiMH, et jusqu'à ~4/heure avec Lithium.

### Régulation tension — buck converter basse consommation

| Paramètre | Valeur |
|-----------|--------|
| Entrée | 4.0–6.5 V (couvre NiMH déchargé à alcaline neuf) |
| Sortie | 3.3 V régulé |
| Composant recommandé | TPS62840 (Texas Instruments) — Iq = 5 µA, rendement > 90 % |
| Courant de sortie max | 750 mA — suffisant pour pic [[ESP32-S3]] + périphériques |
| Courant quiescent | 5 µA — négligeable sur budget deep sleep |

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

## Tests obligatoires avant acceptation M-02

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
- le TPS62840 ne supporte pas le pic de courant carte complète (fallback : TPS563201 ou MP2307).
