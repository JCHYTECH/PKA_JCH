---
date: 2026-05-24
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-05-24 — insectnet-segment-qc-grouped-split

## Session — 20:17 — insectnet-segment-qc-grouped-split

### Contexte
- Modèle : codex
- Projet : WILDNEXUS

### Résumé
InsectNet V0.1 dispose maintenant d'un segment_qc.csv prudent et d'un train-test-split.csv groupe par recording_id, avec 559 segments, 434 train, 125 test et zero fuite detectee.

### Actions
Creation de scripts/insectnet_segment_qc.py et scripts/insectnet_grouped_split.py; ajout des tests pytest associes; generation de segment_qc.csv; generation de train-test-split.csv; correction du split pour viser l'equilibre par nombre de segments tout en gardant les recording_id intacts; creation du log segment-qc-and-grouped-split-log.md.

### Décisions
Tous les segments commencent en visual_qc=review, aucun keep automatique; split train/test obligatoirement groupe par recording_id; les segments rejetes seront exclus lors des prochaines generations de split.

### Prochaines étapes
Revoir segment_qc.csv pour marquer keep/reject; regenerer le split apres QC manuel; preparer ensuite une baseline CNN seulement sur segments valides et classes equilibrees.
