---
date: 2026-11-10
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-11-10 — Cozmo compagnon IA + corrections WildNexus (caméra et graphe)

## Session — 00:11 — Cozmo compagnon IA + corrections WildNexus (caméra et graphe)

### Contexte
- Modèle : deepseek-v4-pro
- Projet : IOT

### Résumé
Analyse du Cozmo en compagnon IA local (hôte SDK M5 + cerveau Ollama M1 gemma3:27b vision + Tailscale + RUT240) ; création du fichier de travail cozmo-reborn et backport de 2 leçons dans le rapport Karotz. Correction des 2 dérives WildNexus : skill caméra réaligné sur ADR-002 (OV5640 P0, IMX462 repli P1) et graphe graphify nettoyé (127 chemins remappés, 314 nœuds et 288 liens morts supprimés).

### Actions
- Analyse ESP Mosaico pour le device WildNexus : rejeté en P0, noté à surveiller en P1
- Réconciliation du skill wildnexus-camera-imaging avec ADR-002 (OV5640)
- Nettoyage du graphe graphify : remap 3885 occurrences, suppression 314 nœuds et 288 liens morts, re-clustering
- Analyse Cozmo compagnon IA + vérification infra en direct (M1 Ollama gemma3:27b vision, HA up)
- Création de 11_IOT/cozmo-reborn/README.md + mise à jour INDEX.md et thread-iot.md
- Backport de 2 leçons dans resurrection-karotz-2026-11-09.md

### Décisions
- Cozmo : cerveau local (Ollama M1) plutôt que cloud GPT, cohérent avec local-first
- Caméra WildNexus : OV5640 reste P0 (ADR-002), IMX462 = repli P1 si nuit insuffisante
- Graphify : remap déterministe des chemins (fichiers déplacés, pas réécrits) plutôt qu une ré-indexation LLM
- ESP Mosaico : hors périmètre P0 (pas de LoRa, caméra visible, batterie LiPo)

### Prochaines étapes
- Recenser le matériel Cozmo (modèle 1.0/2.0, état app et SDK, batterie)
- PoC Cozmo : SDK -> caméra -> gemma3:27b vision -> TTS
- Option : ré-indexation doc graphify complète si besoin
