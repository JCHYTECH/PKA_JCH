# Risques et frottements — Transverses PKA_JCH

> Dernière mise à jour : 2026-07-15 — Dobby 🦉 — Alignement post-gel WILDNEXUS
> Rôle : lister les points qui ralentissent plusieurs projets à la fois

---

## Actifs

| Risque | Impact | Projets touchés | Action |
|--------|--------|----------------|--------|
| **Deadline Lupo 7 août** | P0 — IOT Van doit être prêt | IOT | Tout le hardware reçu, assemblage en cours. Reste : mise en boîtier + config HA finale + commande capteurs Zigbee. |
| **Panier Mouser restant (~279€)** | Bloque LoRa (RAK3172) + SOP-16 test RF | WILDNEXUS | Reporté septembre. Mouser #39492997 reçu 08/07. |
| **Dispersion JCH** | 10 projets, focus dilué | Tous | Gel effectif de 6 projets jusqu'à septembre. Reste actif : IOT Van (P0) + 3 autonomes. |
| **Données GBIF insectes rares** | geomodel moins précis que pour oiseaux | NEXUS_ACOUSTIC | Accepter 15-25% FP reduction vs 30-40% |
| **ESP32-S3 sans NPU** | birdnet-stm32 non portable | WILDNEXUS, LEAFNET | FOMO via Edge Impulse comme baseline |
| **State files périmés** | 5 fichiers CRITICAL (>14j), 9 WARNING (>7j) | Tous | Nettoyage en cours (session 15/07) |

## Surveillés

| Risque | Impact | Projets touchés |
|--------|--------|----------------|
| Surcharge documentaire | MEMORY.md ~75KB, fichiers s'empilent | Tous |
| Stack hardware fragmentée | ESP32 + RPi + XIAO = 3 toolchains | WILDNEXUS, IOT, LEAFNET |
| Multi-modèles IA | Claude, DeepSeek, Gemini, Qwen, Kimi selon usage | AI_IT_TOOLS |
| WildLens en pause | 0 édition depuis 3 mois, perte d'élan éditorial | ARTEON |
| Session JSONs en root | 16 fichiers JSON (session_*) dans la racine — ~10 MB | Tous |

---

## Résolus

| Risque | Résolution | Date |
|--------|-----------|------|
| PPK2 bloquant | Reçu et utilisé | ~2026-06-10 |
| Arducam MOQ 10 | OV5640 dispos en stock, Camemake backup | 2026-06-12 |
| Deadline WildNexus 30 juin → 15 juillet → septembre | WILDNEXUS gelé jusqu'à septembre — décision JC post-état des lieux | 2026-07-11 |
| Trous mémoire Dobby | Bootstrap memory v2 + script fraîcheur + system check actif | 2026-06-19 |
| PV PI en attente août | Reçu avec 6 semaines d'avance (01/07) | 2026-07-01 |
