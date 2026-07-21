# PHOTO_AI_JURY — Executive Summary

> Document interne — outil PKA. Usage externe possible : démonstration IA.
> Généré le 2026-07-03 par Dobby 🦉. Version 1.0.

---

## En une phrase

**Argus est un moteur IA de critique photographique naturaliste — il évalue, note et conseille chaque image avec une rigueur de jury de concours.**

---

## Ce que fait Argus

Pour chaque photo nature soumise :
1. **Analyse technique** — exposition, netteté, composition, bruit, profondeur de champ
2. **Analyse naturaliste** — identification espèce, comportement, saison, habitat
3. **Analyse artistique** — impact visuel, narration, originalité
4. **Score** — note /100 avec justification détaillée
5. **Recommandation** — papier, tirage, format, preset Lightroom

---

## Performances

| Métrique | Valeur |
|----------|--------|
| Analyses cumulées | 58 |
| Score moyen | 73.8/100 |
| Taux d'acceptation JC | 81% |
| Modèle | Prompt calibré (14/06/2026) |

---

## Intégration

- **Lightroom** — MCP partiellement installé (export direct presets + XMP)
- **PHOTO_NATURE** — reçoit les photos brutes du workflow terrain
- **ARTEON/WildLens** — fournit les sélections finales et les critiques éditoriales

---

## Pipeline

```
PHOTO_NATURE ──→ Argus analyse ──→ Score + Preset ──→ ARTEON (shop)
                                         │
                                         └──→ WildLens (critique éditoriale)
```

---

## Prochaine étape

Activer MCP Lightroom (Start Server) pour automatiser l'export des analyses vers le catalogue.

---

*Document principalement interne. L'outil démontre la capacité PKA à déployer une IA spécialisée sur un domaine expert.*
