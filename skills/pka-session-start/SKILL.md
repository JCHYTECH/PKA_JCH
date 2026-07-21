---
name: pka-session-start
description: Protocole de démarrage de session [[Dobby]] — 5 phases silencieuses alignées sur dobby-memory-bootstrap.md. S'exécute à chaque début de session.
model: kimi-k2.7-code
---

# Skill — pka-session-start

## Déclencheur
- Automatique à chaque début de session (premier message, "dobby", invocation explicite de Dobby)
- S'exécute silencieusement ; ne jamais narrer les phases sauf anomalie
- Ne jamais bloquer la session pour un problème non critique

---

## Phase 1 — Identité & Personnalité (Config)

Lire silencieusement (si non déjà injectés via le pointer outil actif) :
- `ADAPTER-PROMPT.md` — bootstrap universel, architecture PKA
- `SOUL.md` — persona, règles de comportement
- `USER.md` — profil JC, setup, préférences
- `TEAM/dobby.md` — responsabilités et frontières du rôle orchestrateur

Identifier et mémoriser le modèle actif (depuis le contexte système) pour attribution des entrées mémoire de la session.

---

## Phase 2 — Contexte & Historique (Log)

```bash
# Journal chronologique — contexte, PAS l'état actuel
cat /Users/jchavauxm5/PKA_JCH/MEMORY.md

# Patterns récurrents issus des rétrospectives
python3 /Users/jchavauxm5/PKA_JCH/scripts/retro_digest.py --top 15 --min 3

# Dernière note livrée dans TEAM_Inbox (system check, daily, ou livrable)
ls -t /Users/jchavauxm5/PKA_JCH/TEAM_Inbox/*.md 2>/dev/null | head -1
# → lire ce fichier

# Inventaire des scripts, skills et outils disponibles
cat /Users/jchavauxm5/PKA_JCH/docs/system/outils-index.md

# Point d'entrée de la base de connaissances
cat /Users/jchavauxm5/PKA_JCH/wiki/index.md

# Registre des décisions structurelles historiques
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-pka.md
```

> Les fichiers Log donnent le **contexte**, pas l'état actuel.

---

## Phase 3 — État Vivant (State — lire AVANT toute affirmation)

```bash
# Matériel reçu / commandé / attendu
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/hardware-state.md

# Statut vivant des projets actifs
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/etat-projets.md

# Décisions en attente de JC
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/decisions-actives.md

# Priorités portefeuille actives
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/priorites-actives.md

# Risques et frictions transverses
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/risques-et-frottements.md

# Roadmap court terme
cat /Users/jchavauxm5/PKA_JCH/JCH_Inbox/04_PILOTAGE_STRATEGIQUE/roadmap-90-jours.md

# Registres procurement — glob dynamique (pérenne, tous projets)
find /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS \
  \( -name "*procurement*.md" -o -name "*BOM*.md" -o -name "*shortlist*.md" \) \
  2>/dev/null
# → lire chaque fichier trouvé

# Protocoles d'avancement — glob dynamique
# Règle : ne jamais déduire l'avancement d'un protocole depuis des artefacts (CSV, logs)
find /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS \
  -name "progress.md" -path "*/PROTOCOLES/*" 2>/dev/null
# → lire chaque fichier trouvé
```

**Règle cardinale :** tout fichier State avec `last_updated` > 7 jours → flagguer (voir Phase 4).

---

## Phase 4 — Vérifications automatiques

```bash
# Vérification ancienneté State (règle des 7 jours)
python3 /Users/jchavauxm5/PKA_JCH/scripts/check_state_freshness.py --warn-days 7

# Recherche historique cross-session avant toute réponse sur passé/projet/préférence
python3 /Users/jchavauxm5/PKA_JCH/scripts/pka_retrieve.py --fts "<mots-clés contexte session>"

# Follow_ups en retard dans team.db
sqlite3 /Users/jchavauxm5/PKA_JCH/TEAM/team.db \
  "SELECT id, note, due_date FROM follow_ups WHERE due_date < date('now') AND status != 'done';" 2>/dev/null

# Scanner l'inbox
ls /Users/jchavauxm5/PKA_JCH/JCH_Inbox/00_INBOX/
```

Vérifications à effectuer :
- Fichiers State > 7j → lister et flagguer dans le rapport
- Incohérence MEMORY.md ↔ State → alerter si contradictoire
- Registres avec statut « BLOQUANT » ou « ATTENTE » > 14 jours → signaler
- Follow_ups en retard → signaler dans le rapport

---

## Phase 5 — Rapport d'activation (une seule ligne)

Format obligatoire :
```
Dobby 🦉 — <model-id> — <N> membres (<N-1> spécialistes + Dobby) — Inbox: <N> fichiers en attente
```

Si des alertes existent (State périmé, bloquants, follow_ups) → les ajouter après la ligne d'activation, concisément.

Exemple avec alertes :
```
Dobby 🦉 — claude-sonnet-4-6 — 31 membres (30 spécialistes + Dobby) — Inbox: 0 fichiers en attente
⚠️ hardware-state.md — dernier update 2026-06-20 (17j) — à rafraîchir
⚠️ 1 follow_up en retard : contact #12 depuis 2026-06-18
```

---

## Règle mid-session

Si une affirmation sur un State doit être faite > 30 min après la lecture initiale, ou si JC donne une info qui invalide un State :
- Relire le fichier State concerné avant d'affirmer
- Préfixer si incertitude : « D'après ma lecture en début de session... est-ce toujours d'actualité ? »

---

## Règles mémoire (pour toute écriture en session)

Tout nouveau fichier mémoire créé pendant la session doit inclure dans son frontmatter :
```yaml
model: <current-model-id>
```

Pour les captures en temps réel, privilégier `pka_memory_capture.py` avec le modèle actif renseigné.

---

## En cas de problème

| Situation | Action |
|-----------|--------|
| Fichier introuvable | Continuer ; noter dans le rapport si critique |
| Script Python en erreur | Continuer sans bloquer |
| `MEMORY.md` absent | Signaler « MEMORY.md introuvable — contexte dégradé » |
| `team.db` inaccessible | Continuer, ne pas bloquer |
| Pointer outil incomplet | Lire explicitement `ADAPTER-PROMPT.md` + `TEAM/dobby.md` |

---

## Voir aussi
- [[Dobby]]
- [[docs/system/dobby-memory-bootstrap.md|Dobby Memory Bootstrap]]
- [[skills/pka-system-check/SKILL.md|pka-system-check]]
- [[skills/pka-pointer-sync/SKILL.md|pka-pointer-sync]]
- [[skills/pka-file-versioning/SKILL.md|pka-file-versioning]]
