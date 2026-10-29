# Roadmap — Améliorations P2 (vision long terme)
> Extraits du plan d'amélioration Hermes → PKA.
> Ajouté le 2026-06-19.

---

## P2.1 — Skills auto-générées depuis l'expérience

**Inspiration :** Hermes crée automatiquement des skills après des tâches complexes.

**Concept PKA :**
- Après une session où une tâche complexe est réussie (ex: session procurement),
  Dobby propose de générer une skill
- La skill est créée en draft dans `skills/`
- Revue humaine (JC ou Dobby) → validation → publication
- Boucle Arbor : hypothèse = « cette tâche mérite une skill » → expérience =
  génération + test → insight = la skill réduit-elle le temps/erreurs ? →
  décision = publier ou rejeter

**Dépendances :** Memory Nudge (P0#3) — détection des tâches complexes.

---

## P2.2 — Gateway unifiée multi-canal ✅ Implémenté

**Implémentation :** `scripts/pka_gateway.py` (423 lignes, 2026-06-19)

**Canaux actifs :** local_inbox, dropbox_inbox, apple_notes, git_commits
**En attente :** telegram (bot hors service)
**Stockage :** `team.db` (table `gateway_messages`) — messages normalisés avec canal, priorité, statut
**Déploiement :** launchd `com.dobby.pka-gateway.plist` — scan continu toutes les 60s

**À faire plus tard :** rebrancher Telegram quand le bot sera remis en route.
