# PHOTO_AI_JURY — Executive Summary

> Document interne — outil PKA. Usage externe possible : démonstration IA.
> Version 1.2 — état consolidé le 2026-11-06 ; source opérationnelle : `thread-photo-ai-jury.md`.

## En une phrase

**Argus est un moteur IA de critique photographique naturaliste : il évalue, note et conseille chaque image avec une grille inspirée d'un jury de concours.**

## Ce que fait Argus

Pour chaque photo nature soumise :

1. **Analyse technique** — exposition, netteté, composition, bruit, profondeur de champ ;
2. **Analyse naturaliste** — identification espèce, comportement, saison, habitat ;
3. **Analyse artistique** — impact visuel, narration, originalité ;
4. **Score** — note /100 avec justification détaillée ;
5. **Recommandation** — papier, tirage, format et preset Lightroom.

## Métriques historiques Phase 0

| Métrique | Valeur | Portée |
|---|---:|---|
| Analyses cumulées | 58 | Bilan historique Phase 0 |
| Score moyen | 73,8/100 | Phase 0.3 |
| Taux d'acceptation JC | 81 % | 16 analyses évaluées sur 58 |
| Prompt | Calibré le 14/06/2026 | Version historique documentée |

Ces valeurs ne sont pas recalculées dans cette revue documentaire.

## Persistance : base canonique réconciliée

Le contrôle du 06/11 établit :

- `05_PHOTO_AI_JURY/argus_critique.db` : **base canonique**, 52 analyses (IDs 7–58), 52 hashes/PDF/XMP, 16 évaluations de rapports ; l'orphelin historique ID 1 de la file de modération est conservé ;
- `scripts/argus_db.py` : chemin partagé par `run_analysis.py` et les scripts internes de reporting ;
- `PHOTO/argus_critique.db` : **0 octet**, fichier conservé intact, sans fusion.

Les 58 analyses restent le bilan historique de Phase 0, distinct des 52 lignes SQLite. Le journal de `run_analysis.py` ignore toujours les erreurs d'écriture pour ne pas bloquer une analyse : l'existence d'un rapport ne prouve donc pas sa persistance en base. Le schéma v1, vérifié intègre et sans violation de clé étrangère, ajoute trois tables **vides** pour le retour de retouche explicite de JCH. Aucun vote de rapport n'est converti en style artistique.

## Intégration et limites

- **Lightroom** — test technique MCP réussi le 2026-11-06 sur `Evieux-42.CR3`, copie virtuelle RAW confirmée par JC : 8/8 lectures, exposition `0 → +0,10 → 0`, restauration dans `finally` et nouvelle lecture indépendante à `0`. Aucun preset ni lot n'a été appliqué. Ce succès ne constitue pas une validation artistique ; celle-ci reste nécessaire avant toute généralisation.
- **PHOTO_NATURE** — reçoit les photos du workflow terrain ; les 11 presets sont stockés dans `06_PHOTO_NATURE/tech/presets-argus/`.
- **ARTEON / WildLens** — consomme les sélections et critiques éditoriales.
- **Détection d'images IA** — niveau 1 seulement : provenance C2PA et EXIF. Les classifieurs ViT sont désactivés après 12/12 faux positifs ; aucune détection fiable de toute image générée n'est revendiquée.

## Pipeline

```text
PHOTO_NATURE → Argus analyse → Score + preset → ARTEON
                              └→ WildLens (critique éditoriale)
```

## Prochaines étapes

1. Recueillir les choix de retouche explicites de JCH dans le socle vide ; ne pas fabriquer de dataset de style à partir des votes sur les rapports.
2. Faire juger les propositions Lightroom A/B par JCH, avec tutoriel et validation sur image inédite ; le test technique réversible est déjà réussi.
3. Conserver la détection IA au niveau de preuve réellement mesuré.

*Document principalement interne. Détails et historique : `INDEX.md`, `thread-photo-ai-jury.md` et `ai-image-detection.md`.*
