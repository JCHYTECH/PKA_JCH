---
date: 2026-11-16
source: dobby
domain: arteon
type: schéma
status: actif
lang: fr
---

# ARTEON — Schéma de structure & potentialités stratégiques

> Dobby 🦉 — 2026-11-16 · Vue d'ensemble de la marque, du funnel et des chantiers en cours.
> Inclut les décisions du conseil du 16/11 (service de correction photo : NO-GO automatisé, GO conditionnel).

---

## 1. L'organisation (vue d'ensemble)

- **ARTEON** — photographie naturaliste éditoriale (Jean-Claude Havaux, zoologiste)
  - **WildLens** — journal hebdomadaire (tête du funnel, Ghost sur VPS Hostinger)
  - **L'Instant Lu** — conseil éditorial photo (recadré le 15/11 : NO-GO « lancer tel quel »)
  - **Pack « Naturaliste »** — produit : 36 presets XMP (12 looks × 3 forces)
  - **Plugin Lightroom** — moteur technique (MCP, 14 outils, local M5)
  - **Service de correction photo** — potentialité, recadrée en V1 le 16/11

---

## 2. Le système photo (3 couches)

```
PHOTO_NATURE          PHOTO_AI_JURY          ARTEON                WildLens
(terrain, keyworder)  (Argus, analyses)      (marque + produits)   (journal, funnel)
        |                    |                     |                     |
        v                    v                     v                     v
   photos brutes      ->  avis/critique   ->   pack + look   ->   acquisition audience
```

---

## 3. Le funnel de conversion

```
avis d'expert + conseils  ->  pack « Naturaliste » (29 €)  ->  correction / plugin / dataset
      (L'Instant Lu)            (produit à vendre)             (potentialités V1)
```

**Principe directeur (conseil 16/11)** : la fin est « preuve concrète + acquisition du pack ».
La correction n'est qu'un moyen — on ne construit pas l'étape 3 d'un entonnoir vide.

---

## 4. Le pack « Naturaliste » (état du produit)

| Brique | État |
|--------|------|
| 36 XMP (12 looks × 3 forces) | ✅ fait |
| WB/expo découplées (P0) · « indigo »→« bleu acier » | ✅ fait |
| 3e roue grading + Luminance + Blending/Balance (P1) | ✅ fait |
| Contrat de look {forme, ancre, amplitude} | ✅ documenté |
| Guide débutant + mode d'emploi | ✅ faits |
| **Brique 3 — masques IA** (sujet/œil/plumage/fond) | EN COURS — Forge |
| **Brique 4 — `/recommend`** (choix du look) | EN ATTENTE — après dataset A/B |

---

## 5. Potentialités stratégiques (conseil du 16/11)

**Verdict : NO-GO sur le service de correction automatisé · GO conditionnel.**

La séquence retenue (V1) :

```
M1 test manuel      ->  M2 contenu avant/après  ->  M3 plugin      ->  M4 dataset A/B -> /recommend
(16 photos, aveugle)    (galerie landing)          (abonnement)       (votes)           (calibré)
```

**Les 4 upsides identifiés** (à ne pas laisser sur la table) :

- **O1 · Plugin** — livrer le moteur (déjà un plugin Lua) au lieu d'héberger : ~39 €/an × 150 abonnés, zéro serveur, RGPD non-sujet.
- **O2 · Dataset A/B** — servir 2 corrections + récupérer le vote : ~5 200 paires/an pour ~0 €, c'est lui qui calibre `/recommend`.
- **O3 · Flux éditorial** — l'avant/après devient la « Clinique » hebdo de WildLens : 52 épisodes/an sans temps créatif JC.
- **O4 · Lot B2B** — clubs/fédérations/festivals : 390 €/an/club, « exposition normalisée au regard d'un zoologiste ».

**Garde-fous** : pas d'orchestrateur tant que la demande n'est pas prouvée · pas d'exposition réseau de la M5 · pas de correction gratuite qui cannibalise le pack · catalogue séparé + consentement.

---

## 6. Infra technique

```
~/Pictures (RAW, dossiers datés)   ->   Lightroom Classic (M5, catalogue)   ->   MCP (14 outils)
                                              |                                       |
                                              v                                       v
                                    presets Naturaliste                     import / preset / export
                                              |
                                              v
                                    VPS Hostinger (Ghost — wildlens.arteon.be)
```

---

## 7. Prochaines actions (TTD)

1. **M1** — correction manuelle de 16 photos + jugement en aveugle (~5 photographes). Préalable : mapping RAW.
2. **Brique 3** — Forge (masques IA), tâche en cours.
3. **P0 IOT Van** — deadline 15/12 (hors ARTEON, mais priorité transversale).
4. **P7** — nettoyer le doublon de preset LRC + galerie avant/après définitive.

---

*Sources : `thread-arteon.md`, `strategy/service-correction-photo-conception.md` (V1), `TEAM_Inbox/2026-11-16_dobby_conseil_correction-photo.md`.*
