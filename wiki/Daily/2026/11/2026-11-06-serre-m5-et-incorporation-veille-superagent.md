---
date: 2026-11-06
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-06 — Serre sur M5 et incorporation veille SuperAgent

## Session — 20:39 — Serre sur M5 + incorporation veille DeepSeek

### Contexte
- Modèle : deepseek-v4
- Projet : 11_IOT + 01_AI_IT_TOOLS (multi-projet)

### Résumé
Deuxième partie de session : second ZBDongle-E branché sur M5 (temporaire) + bascule AirGuard Serre vers M5 ; analyse de 3 transcripts DeepSeek SuperAgent et incorporation des 4 idées dans PKA (mémoire par topic, routage léger/lourd, limite de projets, batching gateway).

### Actions
- **Zigbee maison/serre** : second ZBDongle-E reçu → affecté au **M5** (temporaire). Pont série `serial_bridge.py` relancé (v4), Z2M up (EmberZNet 7.4.4, canal 15). **AirGuard Serre** ré-appairé du Lupo vers le M5 (LQI 255/255). Valve d'eau + LuxSerre identifiés **périmés** (dernier contact juillet).
- **Veille SuperAgent** : 3 transcripts NoteGPT analysés → 4 idées incorporées :
  1. **Mémoire par topic** — `topic-file-template.md` + section « Topics » du skill `pka-thread-file` + démo `11_IOT/topic-zigbee.md`.
  2. **Routeur léger / workers lourds** — règle ajoutée à `SOUL.md`.
  3. **Limite ~4 projets actifs** — règle ajoutée à `SOUL.md`.
  4. **Batching + routage direct** — `group_key()` + `route_followups()` + rapport coalescé dans `pka_gateway.py`.
- **Routage** : 3 transcripts → `01_AI_IT_TOOLS/99_REFERENCES/deepseek-superagent_2026-11-06/`.

### Décisions
- Second ZBDongle-E : **M5 temporaire** (le M1 est en décommission, le M5 voyage) — un RPi dédié permanent reste à provisionner.
- Les 4 idées SuperAgent sont adoptées (détail : `docs/system/2026-11-06_dobby_veille-superagent-router-workers.md` + `SOUL.md`).

### Prochaines étapes
- Ré-appairer la valve d'eau + LuxSerre sur le M5 (quand JC les aura localisés).
- Provisionner un RPi dédié permanent pour la maison/serre (remplacer le M5).
- Rien d'autre : le chantier veille est 4/4 implémenté.
