# Audit des skills PKA — 2026-11-25

> Dobby 🦉 — DeepSeek V4 — 2026-11-25
> Périmètre : `skills/` (38 natifs) + `.agents/skills/` (35 importés) = **73 skills**.
> Méthode : inventaire frontmatter + comptage des références par nom dans `bin/ scripts/ docs/ TEAM_Inbox/` (513 fichiers scannés, hors `node_modules` et hors dossiers skills).
> Contexte : leçon du transcript « orchestrer des agents IA » — ne pas accumuler de skills, les élaguer régulièrement.

---

## Chiffres clés

- **73 skills** au total : 38 natifs PKA + 35 importés (dont **25 SEO** du pack GitHub `AgriciDaniel/claude-seo`).
- **~29 skills (40 %)** n'ont **0 référence** dans le code/docs/briefs → jamais invoqués par le système (usage conversationnel possible pour certains).
- Les plus sollicités : `status` (139), `save` (65), `inbox-analysis` (65), `brief` (38), `conseil` (31), `ingest` (20), `analyse-transcript` (16), `decision-gate` (10). *(noms courts = faux positifs possibles, mais signalent une activité réelle)*.

---

## A. Pack SEO importé — 25 skills, quasi inutilisé → ARCHIVER

Source : `AgriciDaniel/claude-seo` (GitHub, tracé dans `skills-lock.json`).

| Usage | Skills |
|---|---|
| 0 réf (24) | seo-audit, seo-backlinks, seo-cluster, seo-competitor-pages, seo-content-brief, seo-dataforseo, seo-drift, seo-ecommerce, seo-flow, seo-geo, seo-google, seo-hreflang, seo-image-gen, seo-images, seo-local, seo-maps, seo-page, seo-plan, seo-programmatic, seo-schema, seo-sitemap, seo-sxo, seo-technical |
| 1 réf (2) | seo-content, seo-content-writer |

**Recommandation** : archiver les 25 (dossier `skills/_archive/seo-pack/`). Le besoin SEO PKA est couvert par `seo-loop` (natif) + le spécialiste **Trace**. Ne conserver que `seo-audit` si un chantier SEO site est planifié (ARTEON/WildLens).

## B. Skills natifs jamais tracés (0 réf) — STATUER / FUSIONNER

| Skill | Rôle | Verdict |
|---|---|---|
| `deep-psychology` | Analyse mécanismes psychologiques | Fusionner avec `mind-reader` (même domaine : introspection JC↔Dobby) |
| `mind-reader` | Introspection patterns de communication JC↔Dobby | Fusionner avec `deep-psychology` |
| `competitive-framework` | Positionnement/concurrence projet | Conserver si chantier positionnement à venir, sinon archiver |
| `conception-mecanique` | Checklist mécanique (meuble, caisson) | Conserver (usage ponctuel design matériel WildNexus/IoT) |

## C. Importés non-SEO à conserver (valeur spécialisée)

`code-review-pro`, `supply-chain-risk-auditor`, `insecure-defaults`, `pka-brand-identity`, `wildnexus-governance`, `figma-generate-design`, `content-quality-auditor`, `content-gap-analysis`, `save`, `find-skills`.

> Nuance : `code-review-pro`, `content-quality-auditor`, `content-gap-analysis`, `insecure-defaults` recouvrent des capacités DeepSeek V4 natives — mais leur valeur = **checklist figée reproductible** (scoring, veto checks). À garder tant qu'ils servent un workflow précis.

## D. Chevauchement « traitement des fichiers entrants »

4 skills qui se recouvrent : `inbox-analysis` (65) · `ingest` (20) · `analyse-transcript` (16) · `system-improvement-ingest` (6).

**Recommandation** : clarifier les frontières (1 doc de référence) ou fusionner `system-improvement-ingest` dans `inbox-analysis`.

## E. Cœur PKA à conserver (inchangé)

Orchestration (`pka-session-start`, `pka-system-check`, `pka-pointer-sync`, `pka-file-versioning`, `pka-thread-file`, `decision-gate`, `compound-memoire`), Loops (`forge-loop`, `edge-ai-loop`, `seo-loop`, `sigma-loop`, `bench-loop`, `arbor-research`), WildNexus (`wildnexus-adr`, `wildnexus-bom`), spécialistes (`onboarding-specialiste`, `jade-traduction-bilingue`, `voix-jc`, `dobby-voice`, `iot-vanlife`, `vente-occasion`, `bioacoustics-qc-playbook`, `brief`, `status`, `conseil`, `pka-decouvertes`, `decouvertes-to-planner`, `obsidian-knowledge-graph`, `amazon-be-search`, `gmail_imap_fetch`).

---

## Synthèse d'action

| Action | Volume | Effet |
|---|---|---|
| Archiver le pack SEO (25) | -25 skills | -34 % du catalogue, zéro usage |
| Fusionner deep-psychology + mind-reader | -1 skill | -1 doublon |
| Statuer competitive-framework | -0 ou -1 | clarification |
| Clarifier les 4 skills inbox | -0 | doc de frontière |

**Total après ménage** : ~46-47 skills, tous tracés ou à usage justifié.
**Rappel** : à chaque sortie de modèle / migration, relire-tester-supprimer (leçon du transcript).

---

## État de réalisation (2026-11-25)

- ✅ Pack SEO : **21 archivés** (`_local/archives/skills/seo-pack/`), **4 conservés** (seo-audit, seo-backlinks, seo-content-writer, seo-technical). `skills-lock.json` nettoyé (JSON valide).
- ✅ Fusion `deep-psychology` + `mind-reader` → **`introspection-jc`** (2 modes : profil cognitif / blocage). Originaux archivés (`_local/archives/skills/fusionnes-2026-11-25/`).
- ✅ `competitive-framework` archivé (`_local/archives/skills/`).
- ✅ Clarification des 4 skills « inbox » : doc de référence `docs/system/frontieres-skills-inbox.md` + note « Frontière » ancrée dans les 4 SKILL.md.
- **Catalogue : 73 → 50 skills actifs** (36 natifs + 14 importés).
