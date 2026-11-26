# Risques et frottements — Transverses PKA_JCH

> Dernière mise à jour : 2026-11-26 — Dobby 🦉 — statuts v3 + pacte v4 VETALYX finalisés (24/11, DIAHO observateur) ; RPi Lupo booté (25/11) ; CPL réseau décidé (25/11)
> Rôle : lister les points qui ralentissent plusieurs projets à la fois

---

## Actifs

| Risque | Impact | Projets touchés | Action |
|--------|--------|----------------|--------|
| **Deadline IOT Van 15 décembre** | P0 — installation complète | IOT | Reste : revalider lot P1 (~121 €), WiCAN Pro + RUT240 (session atelier), Time Machine auto, bracket Be Camper. RPi Lupo booté 25/11. |
| **Ligne Proximus dégradée** | Réseau maison instable (latence 2 s, 10,5 % perte, 6,15 Mbit/s le 14/11) | IOT, AI_IT_TOOLS | CPL décidé (25/11) : TL-WPA8631P → recommandé TL-PA7017P ; valider tableau/phase + prises avant commande. Rapport `rapport-box-proximus-2026-11-14.md`. |
| **Panier Mouser restant (~279€)** | Bloque LoRa + SOP-16 RF | WILDNEXUS | À commander à la reprise (gates de reprise en cours). |
| **Documentation lacunaire** | Répétition questions ×5 | Tous | Glossaire (ZH, L(M), state files, TTL), registre décisions, archive diagnostics, cartographie instances HA. |
| **Dispersion JCH** | 10 projets, focus dilué | Tous | IOT (P0) + VETALYX (juridique) + Future Invest + autonomes actifs. |

## Surveillés

| Risque | Impact | Projets touchés |
|--------|--------|----------------|
| Surcharge documentaire | MEMORY.md ~75KB, fichiers s'empilent | Tous |
| Stack hardware fragmentée | ESP32 + RPi + XIAO = 3 toolchains | WILDNEXUS, IOT, LEAFNET |
| Multi-modèles IA | Claude, DeepSeek, Gemini, Qwen, Kimi selon usage | AI_IT_TOOLS |
| VanRoll test sans données | Régression non diagnostiquée | TRAVELS/IOT |
| Session JSONs en root | Fichiers JSON session_* dans la racine | Tous |

## Résolus

| Risque | Résolution | Date |
|--------|-----------|------|
| Véto DIAHO contractuel ≠ statutaire | DIAHO **observateur** au conseil (Art. 14 + 33), statuts v3 + pacte v4 finalisés | 2026-11-24 |
| Incohérences statuts SRL | Statuts v3 + pacte v4 finalisés (capital 4 000 € libéré, apport espèces, AB Advices) | 2026-11-24 |
| RPi 5 Lupo boot bloqué | NVMe retiré 01/10 → boot OK + HAOS 18.3 | 2026-10-01 |
| PPK2 bloquant | Reçu et utilisé | ~2026-06-10 |
| Arducam MOQ 10 | OV5640 en stock | 2026-06-12 |
| Deadline WildNexus | Gelé — décision JC | 2026-07-11 |
| Trous mémoire Dobby | Bootstrap memory v2 + script fraîcheur | 2026-06-19 |
| PV PI en attente août | Reçu 01/07 (6 semaines d'avance) | 2026-07-01 |
