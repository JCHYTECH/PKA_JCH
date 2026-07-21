# PROMPT — Analyse de fichier INBOX
> Template réutilisable pour Dobby 🦉 — chaque fois qu'un fichier est déposé dans `JCH_Inbox/00_INBOX/`
> Version 1.0 — 2026-07-03
> **Version skill canonique** : `skills/inbox-analysis/SKILL.md` — chargée automatiquement en session
> Ce fichier est la référence détaillée. Le skill est la version exécutable compacte.

---

## Déclencheur

JC dépose un ou plusieurs fichiers dans l'INBOX et dit : « lis, analyse, détermine les améliorations, intègre dans nos projets ».

---

## Phases d'exécution (silencieuses — ne pas narrer)

### Phase 0 — Discovery
- Scanner `JCH_Inbox/00_INBOX/` → identifier les nouveaux fichiers (hors `.processed`, `.DS_Store`)
- Pour chaque fichier : noter le nom, la taille, le format
- Si un fichier a déjà été traité dans une session précédente → le signaler, ne pas retraiter

### Phase 1 — Deep Read
- Lire le fichier **en entier** (toutes les lignes, pas de skim)
- Si >500 lignes → lire par chunks de 200 lignes, assembler mentalement
- Extraire :
  - Thèse/argument central
  - Technologies/produits/projets mentionnés
  - Auteurs, sources, URLs
  - Code, pipelines, spécifications techniques
  - Dates de publication, versions
  - Limitations, critiques, alternatives mentionnées

### Phase 2 — Multi-Angle Analysis (délégation parallèle)

Ouvrir **autant de sub-agents que nécessaire** en parallèle, chaque spécialiste analyse le même fichier sous son angle :

| Spécialiste | Angle | Questions clés |
|-------------|-------|---------------|
| **Clio** 🦉 | Scientifique | Pertinence académique, validité méthodologique, limitations, adaptabilité à nos domaines (orthoptères, bioacoustique) |
| **Forge** 🔨 | Technique/Ingénierie | Faisabilité, dépendances, intégration dans notre stack, charge compute/stockage |
| **Musaraigne** 🦇 | Edge/TinyML | Peut-on l'embarquer sur ESP32/RPi ? Alternatives légères ? |
| **Chouette** 🦉 | Dashboard/Visualisation | Comment visualiser ces données ? Quel dashboard ? |
| **Araignée** 🕷️ | IoT/Hardware | Implications capteurs, consommation, déploiement terrain |
| **Argus** 👁️ | Qualité/Évaluation | Scoring objectif, forces/faiblesses, risques |
| **Miel** 🍯 | Éditorial/Marketing | Potentiel contenu WildLens/ARTEON, valeur narrative |
| **Sigma** 📊 | Finances/Stratégie | Coûts, ROI, impact budgétaire |

**Règle** : n'ouvrir un spécialiste que si le fichier touche son domaine. Minimum 2, maximum 6. Toujours inclure Clio pour la validation scientifique.

### Phase 3 — Web Validation (DuckDuckGo)

Pour chaque affirmation clé du document :
- Rechercher la source originale (DOI, GitHub, arXiv)
- Vérifier la date de publication
- Chercher des alternatives, critiques, benchmarks comparatifs
- Identifier des ressources complémentaires (datasets, outils, frameworks)

**Règle moteur** : `web.run` (DuckDuckGo) en premier, jamais `web_search` (Bing) sauf fallback.

### Phase 4 — Cross-Project Impact Mapping

Pour chaque projet PKA actif, évaluer l'impact :

| Niveau | Label | Critère |
|--------|-------|---------|
| 🔴 | Impact majeur | Change la roadmap, débloque un jalon, découverte critique |
| 🟡 | Impact élevé | Enrichit significativement, nouvelle capacité |
| 🟢 | Impact modéré | Intéressant mais pas urgent, veille à maintenir |
| ⚪ | Impact léger | Mention, pas d'action immédiate |

Projets à évaluer systématiquement :
- WILDNEXUS P0
- NEXUS_ACOUSTIC / InsectNet / LEAFNET
- IOT (Van, Serre, Maison)
- ARTEON / WildLens
- PHOTO_AI_JURY / PHOTO_NATURE
- VETALYX
- AI_IT_TOOLS
- TRAVELS

### Phase 5 — Integration Proposals (priorisées)

Format obligatoire :

```
🔴 P0 — Actions immédiates (<2 semaines)
1. Action concrète — Responsable — Deadline

🟡 P1 — Court terme (<1 mois)
2. ...

⚪ P2 — Moyen terme (1-3 mois)
3. ...
```

Chaque action doit être : spécifique, assignée à un spécialiste, avec une deadline.

### Phase 6 — Memory Capture

1. **Livrable** → `TEAM_Inbox/YYYY-MM-DD_dobby_analyse-[sujet].md`
   - Format structuré : Résumé → Analyse → Validation web → Analyses spécialistes → Impact projets → Propositions → Actions
   - Toujours inclure la ligne `> Dobby 🦉 — [modèle] — [date]` en header

2. **MEMORY.md** → Ajouter une entrée dans la section de la session courante
   - Format : `[date] [projet — sujet] : Résumé 1-2 phrases. Livrable : chemin.`
   - Toujours inclure les sources et les décisions

3. **Source INBOX** → Déplacer vers le projet principal impacté
   - Destination : `JCH_Inbox/03_PROJECTS/[PROJET]/99_REFERENCES/[nom]_[date]/`
   - Ne jamais laisser un fichier traité dans INBOX

4. **State files** → Mettre à jour si le fichier change un état (hardware-state.md, etat-projets.md, roadmap-90-jours.md)

### Phase 7 — Rapport à JC

Format concis :
```
## Fichier X/N — [titre] ✅

**Livrable** : `TEAM_Inbox/...`

**N découvertes** :
- Découverte 1 — 1 phrase
- Découverte 2 — 1 phrase

**N actions P0** :
| Action | Qui | Deadline |
|--------|-----|----------|
| ... | ... | ... |
```

---

## Règles transversales

- **Langue** : répondre dans la langue de JC (FR par défaut)
- **Adresse** : toute réponse commence par « JC, » ou « JC — »
- **Modèle** : noter le modèle actif dans le header du livrable
- **Spécialistes** : déléguer en parallèle (`agent_open`), pas séquentiellement
- **Web** : toujours valider les claims du document par une recherche indépendante
- **Concision** : ne pas répéter le contenu du fichier source — analyser, synthétiser, proposer
- **Incertitude** : signaler explicitement ce qui est incertain vs validé
- **Ne pas bloquer** : si un outil échoue (sub-agent timeout, web indisponible), continuer avec ce qu'on a

---

## Anti-patterns (ce qu'il ne faut PAS faire)

- ❌ Lire le fichier en survol et produire une analyse superficielle
- ❌ Commenter ligne par ligne le contenu — c'est de la paraphrase, pas de l'analyse
- ❌ Faire des recommendations sans validation web
- ❌ Ignorer les projets PKA existants dans les propositions d'intégration
- ❌ Proposer des actions sans responsable ni deadline
- ❌ Laisser le fichier source dans l'INBOX après traitement
- ❌ Oublier de mettre à jour MEMORY.md

---

## Exemple d'output (après traitement d'un fichier)

```
JC,

## Fichier 1/1 — titre_du_fichier.md ✅

**Livrable** : `TEAM_Inbox/2026-07-03_dobby_analyse-sujet.md`

**3 découvertes** :
- Découverte clé 1 — impact sur projet X
- Découverte clé 2 — nouvelle technologie Y identifiée
- Découverte clé 3 — dataset Z disponible

**3 actions P0** :
| Action | Qui | Deadline |
|--------|-----|----------|
| Télécharger dataset | Dobby | Immédiat |
| Benchmark outil | Forge | +3 jours |
| Notebook validation | Clio | +7 jours |

On lance ?
```
