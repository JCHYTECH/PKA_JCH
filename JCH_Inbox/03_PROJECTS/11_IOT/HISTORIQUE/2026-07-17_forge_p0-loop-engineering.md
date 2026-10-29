# P0 Loop Engineering — Implémentation Forge 🔨

> **Forge 🔨** — 2026-07-17
> Mandaté par Dobby 🦉 suite à l'analyse Loop Engineering complétive

---

## Résumé

Deux actions P0 ont été implémentées et testées avec succès.

---

## 1. `bin/pka-loop` — Commande `/loop` unifiée ✅

Wrapper bash unifié sur les 6 loops PKA existantes, basé sur l'anatomie Cherny en 6 parties.

### Ce qui a été fait

- **Syntaxe courte** par nom de loop : `forge`, `bench`, `edge`, `seo`, `sigma`, `research`
- **Syntaxe longue** (anatomie Cherny) : `--trigger`, `--scope`, `--action`, `--budget`, `--stop`, `--report`
- **Logging** automatique dans `_local/logs/pka-loop.log` (format JSON-ligne avec timestamp)
- **`--dry-run`** : affiche ce qui serait exécuté sans logger
- **`--help`** : aide complète avec exemples

### Mapping des noms courts → skills

| Nom court | Skill PKA | Déclencheur par défaut |
|-----------|-----------|----------------------|
| `forge` | `forge-loop` | `forge loop` |
| `bench` | `bench-loop` | `bench loop` |
| `edge` | `edge-ai-loop` | `edge ai loop` |
| `seo` | `seo-loop` | `seo loop` |
| `sigma` | `sigma-loop` | `sigma loop` |
| `research` | `arbor-research` | `arbor research` |

### Exemples d'usage

```bash
# Lancer une forge-loop avec budget 3 itérations
bin/pka-loop forge --budget 3 --stop "score >= 4/5"

# Lancer une bench-loop sur les SOPs 1 à 6
bin/pka-loop bench --scope "SOP-1..SOP-6"

# Lancer une recherche Arbor avec hypothèse
bin/pka-loop research --action "hypothese: les grillons sont plus actifs a 22C"

# Anatomie Cherny complète
bin/pka-loop --trigger "chaque push sur main" \
             --scope "src/*.py" \
             --action "code-review-pro" \
             --budget "3 iterations, 50k tokens" \
             --stop "score >= 4/5" \
             --report "PR comment"

# Dry-run (voir sans exécuter)
bin/pka-loop seo --scope "https://monsite.com" --dry-run
```

### Tests effectués

- ✅ `--help` : affiche l'aide complète
- ✅ Les 6 noms courts (forge, bench, edge, seo, sigma, research) résolvent correctement
- ✅ La syntaxe longue (anatomie Cherny) fonctionne avec tous les paramètres
- ✅ `--dry-run` n'écrit pas dans le log
- ✅ L'exécution réelle écrit dans `_local/logs/pka-loop.log` au format JSON
- ✅ Les noms invalides sont rejetés avec un message clair
- ✅ Compatible bash 3.2 (macOS default)

---

## 2. `bin/pka-watch-inbox` — Surveillance INBOX ✅

Script bash de surveillance automatisée du dossier `JCH_Inbox/00_INBOX/`.

### Ce qui a été fait

- **Scan** de `JCH_Inbox/00_INBOX/` en ignorant `.DS_Store` et `_captures/`
- **Détection** des nouveaux fichiers par comparaison avec un état persistant
- **3 actions** à chaque détection :
  1. **Log** dans `_local/logs/pka-watch.log`
  2. **État** mis à jour dans `_local/state/inbox-watch.json` (JSON)
  3. **Alerte** écrite dans `TEAM_Inbox/YYYY-MM-DD_forge_watch-inbox-alert.md`
- **Modes** : `--once` (scan unique), `--daemon` (boucle infinie, sleep 300s), `--help`
- **Idempotent** : un fichier déjà connu n'est pas re-détecté

### Fichiers produits

| Fichier | Rôle |
|---------|------|
| `_local/logs/pka-watch.log` | Journal des événements (timestamp, niveau, message) |
| `_local/state/inbox-watch.json` | État persistant (fichiers connus, dates, tailles) |
| `TEAM_Inbox/*_forge_watch-inbox-alert.md` | Alerte markdown par nouveau fichier |

### Exemples d'usage

```bash
# Scan ponctuel
bin/pka-watch-inbox --once

# Surveillance continue (Ctrl+C pour arrêter)
bin/pka-watch-inbox --daemon

# Aide
bin/pka-watch-inbox --help
```

### Tests effectués

- ✅ `--help` : affiche l'aide complète
- ✅ `--once` : scan unique fonctionnel, détecte les nouveaux fichiers
- ✅ Le fichier existant `TowBox_V5_Swing_Union.pdf` a été correctement détecté
- ✅ L'état JSON a été créé avec les bonnes propriétés (size_bytes, first_detected, last_seen, alert_sent)
- ✅ L'alerte markdown a été générée dans `TEAM_Inbox/` avec chemin, taille, date
- ✅ Second scan : 0 nouveau fichier (idempotence confirmée)
- ✅ `.DS_Store` et `_captures/` sont correctement ignorés

---

## 3. `_local/launchd-plists/com.dobby.pka-watch-inbox.plist` ✅

Fichier launchd pour exécution périodique toutes les 5 minutes.

### Installation (par JC)

```bash
# Copier le plist dans les LaunchAgents
cp _local/launchd-plists/com.dobby.pka-watch-inbox.plist ~/Library/LaunchAgents/

# Charger (démarrage immédiat + périodique)
launchctl load ~/Library/LaunchAgents/com.dobby.pka-watch-inbox.plist

# Vérifier qu'il tourne
launchctl list | grep pka-watch

# Arrêter
launchctl unload ~/Library/LaunchAgents/com.dobby.pka-watch-inbox.plist
```

**Note :** Le plist contient un commentaire avec une variante `StartCalendarInterval` pour une exécution en journée uniquement (8h-18h, lun-ven) si vous préférez ne pas scanner la nuit.

---

## Fichiers livrés

| Fichier | État |
|---------|------|
| `bin/pka-loop` | ✅ Créé, exécutable, testé |
| `bin/pka-watch-inbox` | ✅ Créé, exécutable, testé |
| `_local/launchd-plists/com.dobby.pka-watch-inbox.plist` | ✅ Créé |
| `TEAM_Inbox/2026-07-17_forge_p0-loop-engineering.md` | ✅ Ce fichier |

---

## Prochaines étapes suggérées

1. **Activer le watch-inbox** : installer le plist launchd (voir section 3)
2. **Tester pka-loop en conditions réelles** : `bin/pka-loop forge --budget 3` puis copier le trigger dans Dobby
3. **P1** : Compound mémoire (workflow erreur → règle SOUL.md)
4. **P1** : Dashboard loops (page HTML statique)

---

*Forge 🔨 — PKA_JCH — 2026-07-17*
