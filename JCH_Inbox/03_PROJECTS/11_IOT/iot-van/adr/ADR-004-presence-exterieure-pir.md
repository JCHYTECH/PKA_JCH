# ADR-004 — Détection présence extérieure van

**Date :** 2026-06-04
**Statut :** proposé
**Owner PKA :** [[Chouette]] + [[Forge]]
**Jalon :** Phase 2b — Présence extérieure

## Contexte

Besoin : détecter une personne approchant du van la nuit, et déclencher un éclairage extérieur immédiat. Objectif : sécurité passive (visibilité, dissuasion) + confort (lumière en arrivant au van).

Contraintes van : capteur IP65, alim 12V dispo, pas de percement carrosserie, intelligence dans HA.

## Décision

**PIR 12V filaire alarme-grade IP65 + contact sec Zigbee Sonoff SNZB-04 pour intégration HA.**

Le PIR détecte le mouvement → contact sec → SNZB-04 détecte → HA → spot extérieur 12V via relais. Uniquement nuit (condition lux ou horaire).

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| PIR 12V + SNZB-04 | Robuste, IP65, réactif < 1s, intégration HA complète | Câble à passer | **Retenu** |
| Aqara P1 Zigbee | Sans fil, pile 2 ans | Pas IP65, portée incertaine à travers carrosserie | Écarté |
| Spot solaire PIR intégré | Autonome | Pas d'intégration HA | Écarté |
| Caméra détection mouvement | Détection + vidéo | Budget x5, complexité | Écarté |

## Conséquences

- ✅ Délai < 1 s (contact sec, pas de polling Zigbee)
- ✅ Automatisation HA : allumage, plage horaire, mode silencieux
- ✅ Pas de percement — fixation sous toit relevable
- ✅ PIR 12V auto-alimenté → pas de pile extérieure
- ⚠️ Câble 2 fils à passer vers l'extérieur
- ⚠️ Faux positifs branchage/animal → temporisation configurable
- ⚠️ Conso PIR 12V : ~10-15 mA veille, négligeable

## Critère de révision

Si > 3 faux positifs/nuit, augmenter temporisation ou restreindre zone.
