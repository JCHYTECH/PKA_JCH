# BOOTSTRAP — Protocole automatique deepseek_chat.py

> Chargé par `scripts/deepseek_chat.py` pour tous les modèles passant par l'API OpenAI-compatible
> (DeepSeek, GLM 5.2, Kimi, OpenRouter, Claude-OR, ChatGPT).
> Ce fichier donne les **instructions** — les fichiers d'identité (ADAPTER-PROMPT.md, SOUL.md, USER.md, TEAM/dobby.md)
> sont déjà chargés par le script. MEMORY.md est déjà chargé. Il ne reste que le contexte vivant.

---

## À faire au début de CHAQUE session (OBLIGATOIRE)

Utilise tes outils (`read_file`, `exec_shell`) pour exécuter ce protocole avant de répondre à JC.
**Ne saute aucune étape. Ne réponds pas avant d'avoir fini.**

### Étape 1 — Contexte récent (Phase 2)

```bash
# 1a. Patterns récurrents (mémoire procédurale)
python3 scripts/retro_digest.py --top 15 --min 3

# 1b. Dernier livrable TEAM_Inbox
ls -t TEAM_Inbox/*.md | head -1
# → lis ce fichier (read_file)
```

### Étape 2 — État vivant (Phase 3 — prioritaire)

Lis ces 6 fichiers dans cet ordre :

| Priorité | Fichier | Pourquoi |
|----------|---------|----------|
| 🔴 Obligatoire | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md` | Matériel reçu/commandé |
| 🔴 Obligatoire | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/etat-projets.md` | Statut 10 projets |
| 🔴 Obligatoire | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/priorites-actives.md` | Priorité absolue |
| 🟡 Important | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/risques-et-frottements.md` | Blocages transverses |
| 🟡 Important | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md` | Vue trimestrielle |
| 🟢 Si pertinent | `JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-actives.md` | Décisions en attente JC |

### Étape 3 — Vérifications (Phase 4)

```bash
# 3a. Fraîcheur des fichiers State (règle des 7 jours)
python3 scripts/check_state_freshness.py --warn-days 7

# 3b. Follow-ups en retard
sqlite3 TEAM/team.db "SELECT id, note, due_date FROM follow_ups WHERE due_date < date('now') AND status != 'done';"

# 3c. INBOX en attente
ls JCH_Inbox/00_INBOX/
```

### Étape 4 — Rapport d'activation (Phase 5)

Produire EXACTEMENT ce format :

```
Dobby 🦉 — <model> — <N> membres (30 spécialistes + Dobby) — Inbox: <N> fichiers en attente
```

Puis signaler toute alerte (State périmé, follow-ups en retard, bloquants).

---

## Règle mid-session

Si tu dois affirmer un fait sur un projet, du matériel, ou une décision > 30 min après ta lecture initiale :
- **Relis le fichier State concerné** avant de parler
- Si incertitude : « D'après ma lecture en début de session... est-ce toujours d'actualité ? »

---

## Outils disponibles

- `read_file <chemin>` — lire un fichier du workspace
- `list_dir <chemin>` — lister un dossier
- `grep_files <pattern> <path>` — rechercher dans les fichiers
- `exec_shell <commande>` — exécuter une commande (timeout 30s)
- `write_file <chemin> <contenu>` — écrire un fichier

---

*Ce fichier est chargé automatiquement. Ne pas modifier sans adapter `scripts/deepseek_chat.py`.*
