# Récapitulatif session 2026-05-09 — Changements système PKA

**De :** Dobby  
**À :** Toute l'équipe  
**Date :** 2026-05-09  
**Objet :** Modifications majeures — lecture obligatoire

---

## 1. Ingest inbox — Forge

5 fichiers traités depuis `00_INBOX/` → routés vers `03_FAUNE_AUTOUR/` et indexés dans `file_index`.

---

## 2. Nouveau projet — Forge + Lynx

**`03_FAUNE_AUTOUR/`** créé en projet autonome, séparé de `PHOTO_NATURE`.  
Motif : projet tech distinct (PWA + backend + RPi + BirdNET), pas du contenu photo.

---

## 3. Restructuration complète 03_PROJECTS — Forge

**Structure standard adoptée pour tous les projets :**
```
NN_PROJECT/
  ├── INDEX.md
  ├── docs/
  │   └── media/     ← médias ici, jamais à la racine
  ├── archive/
  [optionnels : content/, legal/, tech/, comms/]
```

**Numérotation alphabétique :**
| # | Projet | Responsable |
|---|--------|-------------|
| 01 | AI_IT_TOOLS | Forge |
| 02 | ARTEON | Vega |
| 03 | FAUNE_AUTOUR | Forge + Lynx |
| 04 | NUANCES | TBD |
| 05 | PHOTO_AI_JURY | Argus + Lynx |
| 06 | PHOTO_NATURE | Lynx |
| 07 | TRAVELS | Corbeau |
| 08 | VETALYX | Vasco + Renard + Bruno |

`_SHARED` supprimé (vide). `media/` déplacé dans `docs/` sur tous les projets.

---

## 4. Réorganisation TEAM/ — Castor

`team.db` et `team-roster.html` déplacés à la racine `TEAM/`.  
`backups/` → `TEAM/backups/`.  
**Tous les scripts ont été mis à jour en conséquence.**

---

## 5. Pie — Nouveau système de filtrage email

**Table `email_senders` créée dans `team.db` :**
- 465 expéditeurs whitelistés (dont 457 contacts iOS importés)
- 28 blacklistés (Temu, AliExpress, newsletters, Facebook générique…)

**Règle whitelist-first :**
- Blacklist → score -20 → jamais affichés
- Contact exact → score +10
- Pattern whitelist → score +5
- Inconnu → score 0, apparaît une fois avec tag `[?]`

**Mélanie sur Facebook** : whitelistée. Autres Facebook : blacklistés.  
`email_digest.py` mis à jour.

---

## 6. Nouveaux crons — Castor + Sybil + Dobby

| Heure | Fréquence | Script | Responsable |
|---|---|---|---|
| 08h00 | quotidien | `backup_team_db.py` | Castor |
| 09h00 | quotidien | `email_digest.py` | Pie |
| 14h00 | quotidien | `email_digest.py` | Pie |
| 20h00 | quotidien | `email_digest.py` | Pie |
| 22h00 | quotidien | `sybil_journal.py` | Sybil |
| 23h00 | quotidien | `dobby_retro.py` | Dobby |
| 19h00 | dimanche | `dobby_weekly_report.py` | Dobby |

---

## 7. Sybil — Journal automatique quotidien

`sybil_journal.py` : collecte agenda, digest, activité team.db, fichiers modifiés.  
Écrit dans `wiki/Daily/YYYY/MM/YYYY-MM-DD-sybil-auto.md` et insère dans `journal`.  
**Champs mood/énergie/highlight laissés à JCH.**

---

## 8. Dobby — Rétrospective et rapport hebdo

- `dobby_retro.py` : analyse les sessions Claude Code du jour, identifie les inefficacités de travail, sauvegarde dans `wiki/Daily/` et `knowledge`.
- `dobby_weekly_report.py` : rapport pour JCH sur ses patterns de collaboration, envoyé par email chaque dimanche.

---

## 9. Convention de réponse — Tous

À partir de maintenant, **Dobby mentionne entre parenthèses les membres activés** à la fin de chaque réponse à JCH.  
Objectif : visibilité sur la charge équipe et identification des besoins de formation ou recrutement.

---

*Dobby 🦉 — Bonne nuit.*
