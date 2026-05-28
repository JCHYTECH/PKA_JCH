# MEMORY-ARCHITECTURE — Mémoire transversale PKA_JCH
> Décision architecturale du 2026-05-14. Auteur : [[Dobby]] 🦉 (claude-sonnet-4-6)

---

## Problème identifié

La mémoire accumulée par [[Dobby]] lors des sessions [[Claude]] Code était **invisible depuis tout autre outil** (Gemini CLI, [[Codex]] CLI, [[ChatGPT]], DeepSeek). Elle était stockée dans un chemin [[Claude]] Code-specific :

```
~/.claude/projects/-Users-jchavauxm5-PKA-JCH/memory/
```

Ce chemin n'est ni portable ni accessible hors du harness [[Claude]] Code. Résultat : chaque changement de modèle ou d'outil repartait de zéro, sans contexte JCH, sans règles de comportement [[Dobby]], sans état des projets.

Problème secondaire : aucune mémoire n'était taguée avec le modèle qui l'avait générée — impossible de savoir quelle part du contexte venait de quel LLM.

---

## Solution implementée

### 1. Fichier `MEMORY.md` — miroir portable

Créé à la racine de `PKA_JCH/`, ce fichier est un résumé structuré de toutes les mémoires accumulées :

- Profil JCH (identité, projets actifs, setup, valeurs)
- Règles de comportement [[Dobby]] (délégation, attribution, rasoir d'Occam…)
- États projets (ARTEON, Vetalyx, PKA Digest, recrutement…)

Il est mis à jour manuellement à chaque évolution significative de la mémoire. Contrairement aux fichiers mémoire natifs de [[Claude]] Code, il est lisible par n'importe quel outil.

### 2. Champ `model` dans chaque entrée mémoire

Chaque fichier mémoire contient désormais dans son frontmatter :

```markdown
---
name: ...
type: feedback
originSessionId: xxx
model: claude-sonnet-4-6
---
```

Ce tag permet de savoir quel modèle a généré chaque règle ou connaissance. La table `memory_log` dans `team.db` consolide ces données pour un suivi statistique par modèle dans le temps.

### 3. Session Start Protocol dans les fichiers pointeurs

À chaque démarrage de session, [[Dobby]] :
1. Identifie le modèle actif
2. Charge `MEMORY.md` comme bootstrap portable principal
3. Scanne `JCH_Inbox/00_INBOX/`
4. Confirme en une ligne

Tout nouveau fichier mémoire créé hérite du tag `model:` du modèle actif.

### 4. Compliance check dans `ADAPTER-PROMPT.md`

Pour les outils hors [[Claude]] Code, une question de vérification permet de confirmer que le contexte a bien été chargé avant de commencer à travailler :

> "Qui es-tu, combien de spécialistes dans l'équipe, et quel est ton modèle actif ?"

Réponse attendue côté système : `25 membres actifs`, soit `24 spécialistes + Dobby`.

3/3 correct → session opérationnelle. Sinon → recharger le contexte manquant.

---

## Architecture résultante

```
PKA_JCH/
├── CLAUDE.md          ← Claude Code — chargé automatiquement par le harness
├── AGENTS.md          ← Codex CLI — chargé automatiquement
├── GEMINI.md          ← Gemini CLI — chargé automatiquement
├── DEEPSEEK.md        ← DeepSeek API / prompt manuel
├── ADAPTER-PROMPT.md  ← Bootstrap universel pour tout outil + compliance check
└── MEMORY.md          ← Miroir portable de la mémoire accumulée ← NOUVEAU

~/.claude/projects/.../memory/
└── *.md               ← Historique mémoire natif Claude Code (avec champ model: ajouté)

TEAM/team.db
└── memory_log         ← Traçabilité modèle par entrée mémoire ← NOUVEAU
└── skills.model       ← Modèle tracé sur chaque procédure générée ← NOUVEAU
```

---

## Flux de mise à jour

Quand une nouvelle mémoire est écrite en session [[Claude]] Code :
1. Fichier créé dans `~/.claude/projects/-Users-jchavauxm5-PKA-JCH/memory/` avec `model: <actif>`
2. Entrée insérée dans `memory_log` (team.db)
3. `MEMORY.md` mis à jour si la mémoire est structurellement importante

Quand une session se déroule hors [[Claude]] Code :
1. ADAPTER-PROMPT collé → compliance check effectué
2. Nouvelles mémoires écrites directement dans `MEMORY.md`
3. À synchroniser dans 

---

## Niveau de certitude par outil

| Outil | Chargement auto | Certitude |
|-------|----------------|-----------|
| [[Claude]] Code | ✅ Harness garanti | Certaine |
| [[Codex]] CLI | ✅ AGENTS.md | Élevée |
| Gemini CLI | ✅ GEMINI.md | Élevée |
| DeepSeek API / web | ❌ Prompt manuel | Moyenne / Faible |
| [[ChatGPT]] web | ❌ Prompt manuel | Moyenne / Faible |
