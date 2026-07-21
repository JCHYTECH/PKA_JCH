---
name: inbox-analysis
description: Analyse complète d'un fichier déposé dans l'INBOX — 7 phases standardisées (Discovery → Deep Read → Délégation spécialistes → Validation web → Impact projets → Propositions → Mémoire). Déclencher sur "INBOX", "nouveau fichier inbox", "analyse le fichier", "lis et analyse", "détermine les améliorations".
---

# /inbox-analysis — Analyse de fichier INBOX

> Version canonique PKA — 2026-07-03
> Template complet : `docs/system/prompt-inbox-analysis.md`
> Ce skill s'exécute sans narration. Résultat livré en fin de cycle.

## Déclencheur

JC dépose un fichier dans `JCH_Inbox/00_INBOX/` et dit une variante de « lis, analyse, intègre ».

---

## Exécution (7 phases — silencieuses)

### 0 — Discovery
- Scanner `00_INBOX/` → nouveaux fichiers (hors `.DS_Store`)
- Si déjà traité → signaler, skip

### 1 — Deep Read
- Lire **intégralement** (chunks de 200 lignes si >500)
- Extraire : thèse, technologies, auteurs, URLs, code, dates, limitations

### 2 — Multi-Angle (délégation parallèle)

| Spécialiste | Angle | Déclencher si… |
|-------------|-------|---------------|
| Clio 🦉 | Scientifique | Contenu académique, bioacoustique, biologie |
| Forge 🔨 | Technique | Code, pipelines, architecture, dépendances |
| Musaraigne 🦇 | Edge/TinyML | ML embarqué, microcontrôleurs, optimisation |
| Chouette 🦉 | Dashboard/Viz | Visualisation, dataviz, interface |
| Araignée 🕷️ | IoT/Hardware | Capteurs, déploiement terrain, consommation |
| Argus 👁️ | Qualité | Évaluation objective, risques |
| Miel 🍯 | Éditorial | Contenu WildLens/ARTEON, narration |

**Règle** : minimum 2, maximum 6 en parallèle. Toujours Clio si contenu scientifique.

### 3 — Web Validation
- `web.run` (DuckDuckGo) pour chaque claim clé
- Chercher : source originale (DOI/GitHub), date, alternatives, datasets, benchmarks
- Jamais `web_search` (Bing) sauf fallback

### 4 — Cross-Project Impact
Pour chaque projet PKA : 🔴majeur 🟡élevé 🟢modéré ⚪léger
- WILDNEXUS, NEXUS_ACOUSTIC, InsectNet, LEAFNET, IOT, ARTEON/WildLens, PHOTO, VETALYX, AI_IT_TOOLS, TRAVELS

### 5 — Integration Proposals
```
🔴 P0 (<2 sem) → Action — Responsable — Deadline
🟡 P1 (<1 mois) → Action — Responsable — Deadline
⚪ P2 (1-3 mois) → Action — Responsable — Deadline
```

### 6 — Memory Capture

1. **Livrable** → `TEAM_Inbox/YYYY-MM-DD_dobby_analyse-[sujet].md`
   - Header : `> Dobby 🦉 — [modèle] — [date]`
   - Sections : Résumé → Analyse → Web → Spécialistes → Impact → Propositions → Actions

2. **MEMORY.md** → Entrée session courante : `[date] [projet — sujet] : Résumé. Livrable : chemin.`

3. **Source** → Déplacer vers `03_PROJECTS/[PROJET]/99_REFERENCES/[nom]_[date]/`

4. **State files** → Mettre à jour si impact état (hardware-state, etat-projets, roadmap)

### 7 — Rapport à JC
```
## Fichier X/N — titre ✅
**Livrable** : `TEAM_Inbox/...`
**N découvertes** : …
**N actions P0** : tableau action/qui/deadline
```

---

## Règles absolues

- Toujours commencer par « JC, » ou « JC — »
- Langue = celle de JC (FR par défaut)
- Web : DuckDuckGo d'abord, Bing = dernier recours
- Ne pas paraphraser le fichier — analyser, synthétiser, proposer
- Incertitude → la signaler explicitement
- Si un outil échoue → continuer sans bloquer
- Fichier traité → **jamais** laissé dans INBOX
