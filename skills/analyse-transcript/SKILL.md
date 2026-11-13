---
name: analyse-transcript
description: Analyser un transcript (NoteGPT / YouTube / vidéo / podcast) — comprendre le contenu, le confirmer, puis conseiller les usages possibles dans le système PKA. Déclencher sur "analyse ce transcript", "analyse le transcript", "NoteGPT", "transcript", "analyse cette vidéo", "que fait-on de ça".
---

# /analyse-transcript — Comprendre + Confirmer + Conseiller

> Version canonique PKA — 2026-11-07 — Dobby 🦉
> Complément de `/inbox-analysis` (analyse générique) et `/ingest` (routing). Ce skill est spécialisé **transcripts** (NoteGPT, YouTube, podcast, réunion).

## Déclencheur

JC dépose un transcript (`.txt` souvent `NoteGPT_Transcript_*.txt`, `.md`, `.srt`) et dit « analyse ce transcript » ou une variante.

## Objectif — 3 livrables, toujours dans cet ordre

1. **Comprendre** — synthèse fidèle du contenu.
2. **Confirmer** — séparer ce qui est établi de ce qui est affirmé, signaler les incertitudes.
3. **Conseiller** — comment utiliser les infos dans le système PKA.

---

## Exécution

### 0 — Accès au fichier

- Si le chemin est **hors workspace** (ex. `~/Downloads/`), copier d'abord dans `JCH_Inbox/00_INBOX/` :
  ```bash
  cp "/chemin/hors/workspace/Transcript_X.txt" ~/PKA_JCH/JCH_Inbox/00_INBOX/
  ```
  (lecture hors workspace = bloquée ; en YOLO on copie, sinon demander à JC).
- Repérer les repères temporels (`00:01:00 - 00:02:00`) et les sauts de ligne parasites.

### 1 — Deep Read (intégral)

- Lire **tout** le transcript (chunks si > 200 lignes).
- Extraire : sujet, thèse, auteur/chaîne, date si présente, revendications clés, chiffres, sources citées, limites/contrepoints énoncés par la source elle-même.

### 2 — Comprendre (synthèse)

Restituer en 3 blocs :
- **Nature** : type de contenu (vidéo, podcast…), durée, langue, positionnement de l'auteur.
- **Thèse** : l'idée centrale en 1-2 phrases.
- **Points clés** : liste des faits/arguments principaux, avec chiffres et noms.

### 3 — Confirmer (fact-check structuré)

Classer chaque revendication importante en 3 colonnes :
- ✅ **Établi** — corroboré par la source elle-même + sources externes citées (loi, étude, communiqué).
- ⚠️ **Affirmé par l'auteur** — plausible mais reposant sur son seul dire.
- ❓ **Non prouvé / incertain** — ce que la source reconnaît ne pas pouvoir démontrer.

Règle : un transcript fait souvent son propre fact-check (l'auteur nuance ses claims). **Reporter fidèlement ses propres contrepoints** — ne pas amplifier le sensationnel.

Vérification web **optionnelle** (`web_search` Tavily d'abord, jamais Bing) uniquement si : claim factuel vérifiable + JC le demande + enjeu élevé. Sinon, restituer la position de la source telle quelle.

### 4 — Conseiller (usage dans le système)

1. **Routing** du fichier → `03_PROJECTS/<projet>/99_REFERENCES/<sujet>_<date>/` (convention NoteGPT existante). Table de mapping projet = celle de `/ingest`.
2. **Impact croisé** — lister les projets PKA touchés avec sévérité 🔴🟡🟢⚪.
3. **Captures de connaissance** — idées atomiques → table `knowledge` (team.db, écrivain Corbeau), cf. `/ingest`.
4. **Actions** — proposer P0/P1/P2 avec action/responsable/deadline si pertinent.

### 5 — Rapport à JC

```
## Transcript — <titre>
**Nature** : …   **Thèse** : …
**Confirmé** : N établi · M affirmé · K non prouvé
**Livrable** : `TEAM_Inbox/YYYY-MM-DD_dobby_analyse-transcript-[sujet].md`
**Routing** : `03_PROJECTS/<projet>/99_REFERENCES/…`
**Actions** : …
```

---

## Règles absolues

- Toujours commencer par « JC, » ou « JC — ».
- Langue = celle de JC (FR par défaut).
- **Ne jamais paraphraser** — analyser, synthétiser, proposer.
- Distinguer explicitement : ce que dit la source / ce qui est prouvé / ce qui reste incertain.
- Transcript hors workspace → copier dans `00_INBOX/`, jamais le traiter sur place.
- Ne jamais laisser le transcript traité dans `00_INBOX/` — router + déplacer.
- Web : `web_search` (Tavily) en premier, Bing en dernier recours.
