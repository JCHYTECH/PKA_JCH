---
date: 2026-05-01
tags: [daily]
type: daily
status: active
---

# 2026-05-01 — Session PKA

## Actions

- Recrutement et onboarding de **Miel 🐝 #20** — Community Manager & Brand Content Creator (Instagram, Facebook, newsletters)
- Recrutement et onboarding de **Vasco 🐺 #21** — Veterinary Product Specialist Vetalyx (allergologie chats & chiens, IVD + nutraceutiques)
- Recrutement et onboarding de **Nova 🦋 #22** — Photography R&D Specialist (photographie computationnelle, chronophotographie numérique)
- Création de l'**organigramme HTML interactif** (`wiki/organigramme.html`) — 20 membres, clusters fonctionnels, fond sombre, tooltips
- Mise à jour de l'organigramme en **v13** : ajout départements Photographie, Vetalyx (Vasco), Energy (vide/pointillés), Nova dans R&D Visuelle
- Tous les fichiers `TEAM/` créés : `miel.md`, `vasco.md`, `nova.md`
- `team.db` mis à jour : members #20, #21, #22 + responsibilities
- `ROSTER.md` passé de v10 à v13
- `CLAUDE.md` mis à jour avec les 3 nouveaux membres
- Mémorisé : pause recrutement effective — équipe gelée à 22 spécialistes

## Décisions

- **Pause recrutement** : l'équipe est complète à 22 membres. Aucun nouveau recrutement sans analyse ou besoin identifié.
- **Arteon reste hors Hostinger Horizons** : stack Shopify + WhiteWall + Ghost incompatible avec Horizons. Horizons pour DIM3, JCHYTECH et futurs sites.
- **Nova : réel uniquement** — aucun élément généré par IA, tout pixel vient des archives JCH. Double livrable obligatoire : image + processus documenté.
- **Vasco / Clio binôme structurel** : Clio cherche et extrait, Vasco interprète cliniquement. Deux versions de chaque synthèse : clinicien + propriétaire.
- **Energy department** : département créé dans l'organigramme, vide, prêt pour futurs recrutements.
- **Product Management** : nouveau département créé avec Vasco comme premier membre (Vetalyx).

## Prochaine étape

- Mettre Nova au travail sur une première séquence photo (ex : combat d'oiseaux) — tester le workflow R&D
- Donner un premier brief à Vasco sur un produit Vetalyx spécifique
- Définir le contenu Energy : quels projets, quelles compétences nécessaires ?
- Donner un premier brief à Miel pour le calendrier éditorial d'une des marques
- Dashboard portfolio (Forge) : en attente validation schéma Castor

---

## Actions — Session 2 (après-midi)

- **Audit architecture PKA_JCH** — inventaire complet : 383 fichiers, 150 dossiers, 61 vides, anomalies identifiées
- **Action 1** : secrets déplacés (`credentials.json` + `token.json`) → `~/.config/pka-jch/` — scripts mis à jour
- **Action 2** : `04_KNOWLEDGE/` supprimé — doublon de `wiki/`
- **Action 3** : `JCH _Inbox` renommé → `JCH_Inbox` — 4 références mises à jour
- **Crontab corrigé** : ancien chemin `PKA _JCH` → `PKA_JCH` — 3 jobs cron opérationnels
- **Skill `/ingest` créé** — `~/.claude/skills/ingest/SKILL.md` — traitement 00_INBOX avec routing + indexation file_index
- **`/ingest` testé** : 2 fichiers traités (`CV JC.pdf` → `05_CONTEXT/`, `arteon-manifeste-long.md` → `ARTEON/docs/`)
- **Import contacts Apple** — 333 contacts importés dans `team.db.contacts` depuis Contacts.app (AppleScript)
- **Email digest amélioré** : filtre anti-spam, score contact connu (+3), indicateur `[✓]/[?]`
- **Email routing intelligent** ajouté : Renard (légal), Vasco (Vetalyx), Bruno (finance), Delphi (CRM) — insertions inbox + interactions automatiques
- **Clé Anthropic API** stockée dans `~/.config/pka-jch/anthropic_key.txt` (chmod 600)
- **Analyse Claude intégrée** dans email_digest.py : emails routés score ≥ 2 → corps lu → Claude Haiku → analyse → `TEAM_Inbox/` + push ntfy

## Décisions — Session 2

- **Remote agents rejetés** pour l'email : données sensibles (PKA pas sur GitHub, credentials locaux) — option locale Claude API retenue
- **Claude Haiku** pour analyses email (rapide, économique) — Sonnet possible pour Renard sur emails légaux complexes
- **Recrutement email assistant annulé** : Forge absorbe le rôle technique, routing métier codifié par spécialiste

## Prochaine étape — mise à jour

- Tester une vraie analyse email par Renard/Vasco/Bruno sur email entrant
- Envisager Sonnet pour Renard (emails légaux complexes)
- Mettre Nova au travail sur une première séquence photo
- Donner un premier brief à Vasco sur un produit Vetalyx
- Définir le contenu Energy department

---

## Actions — Session 3 (soir)

- **digest_history.md** créé : log local de chaque run du digest (`PKA_JCH/scripts/digest_history.md`)
- **Envoi email digest** : `send_digest_email()` ajoutée dans `email_digest.py` — digest envoyé à `jc_havaux@yahoo.com` à chaque run
- **Scope gmail.send** ajouté dans `email_digest.py` et `google_auth.py` — réauthentification OAuth2 effectuée
- **Connexion jc.havaux@jchytech.be → Gmail** : tentée, bloquée (JCH non admin Microsoft 365) — reportée

## Décisions — Session 3

- **Email digest envoyé à Yahoo** : ntfy éphémère → complété par email persistant lisible sur smartphone
- **jchytech.be / Microsoft 365** : configuration SMTP AUTH reportée — JCH n'est pas admin, à déléguer ou reprendre plus tard

## Prochaine étape — Session 3

- Connecter `jc.havaux@jchytech.be` à Gmail quand accès admin Microsoft 365 disponible
- Mettre Nova au travail sur une première séquence photo
- Donner un premier brief à Vasco sur un produit Vetalyx
- Définir le contenu Energy department

---

## Actions — Session 4 (photo)

- **Skill `photo-analyse-wildlife` installé** depuis archive `.skill` — adapté pour Claude Code local
- **`pdf_report.py` créé** — rapport PDF complet style Fin Art Cinématique (reportlab)
- **Dépendances installées** : `reportlab`, `pillow`, `numpy`
- **Structure `PKA_JCH/PHOTO/`** créée : `analyses/`, `presets/`, `sources/`, `exports/`
- **Première analyse complète** : `LrC to-59.jpg` (rouge-gorge en plein chant)
  - Score : 82/100 — EXCELLENT
  - PDF → `PHOTO/analyses/LrC to-59_analyse.pdf`
  - XMP → `PHOTO/presets/LrC to-59.xmp`
- **Argus 🦅 #23 recruté** — Photo Critic & International Jury Expert (Faucon pèlerin)
  - Overlap vérifié : complémentaire à Lynx (prescrit) et Nova/Héron (domaines distincts)
  - `team.db` mis à jour, `TEAM/argus.md` créé, organigramme v14 (cluster "Critique & Jury")
- **Pipeline LR plugin** étudié — faisabilité confirmée (Lua SDK + os.execute Python)

## Décisions — Session 4

- **Outputs photo dans PKA_JCH/PHOTO/** : centralisé dans le vault, pas sur le Desktop
- **Argus prescrit, Lynx exécute** : frontière claire définie dans `argus.md`
- **Plugin LR à construire** : clic droit → pipeline complet (Forge + Argus, session dédiée)
- **Pause recrutement maintenue à 23** après Argus — justifié par le skill photo installé

## Prochaine étape — Session 4

- Construire le plugin Lightroom Classic (Lua + Python) — clic droit → pipeline Argus ✓
- Connecter `jc.havaux@jchytech.be` à Gmail (accès admin M365 requis)
- Premier brief Nova : séquence photo (combat d'oiseaux)
- Premier brief Vasco : produit Vetalyx spécifique

---

## Actions — Session 5

- **Plugin Lightroom Classic livré** — `PHOTO/plugin/argus.lrplugin/`
- **`run_analysis.py` créé** — orchestrateur CLI : Claude API vision → color_analysis → pdf_report → generate_xmp
- **Debugs résolus** : `os.getenv` indisponible sandbox LR, progress scope hors task, mauvais Python (`/usr/bin` → `/usr/local/bin`)
- **Premier test réel depuis LR** : LrC to-67.jpg → Bernache du Canada, 76/100 TRÈS BON ✓

## Actions — Session 6 (2026-05-02)

- **XMP corrigé** : suppression du `+` sur valeurs positives (`Tint="+4"` → `"4"`) — LR parsait mal
- **XMP use_defaults=False** : preset ne contient plus que les corrections photo-spécifiques (plus de TSL/grain/vignette par défaut)
- **generate_xmp.py refactorisé** : attrs dynamiques, `use_defaults` param, `xmp_val()` normaliseur
- **Plugin Argus v1 validé** : pipeline complet LR → Claude API → PDF + XMP cohérents ✓
- **Workflow final** : `Cmd+'` (copie virtuelle) → Extras → Analyser → réglages appliqués en Develop

## Actions — Session 7 (2026-05-02 — fin)

- **Modèle upgradé** : `claude-sonnet-4-6` → `claude-opus-4-7` dans `run_analysis.py`
- **Virtual copy SDK abandonné** : `catalog:createVirtualCopies` retourne nil sur toutes signatures testées — limite LR SDK confirmée
- **AppleScript abandonné** : `io.popen('osascript')` depuis sandbox LR sans permission Accessibilité
- **Workflow stabilisé** : `Cmd+'` manuel → Extras → Analyser avec Argus (dialog de rappel intégré)
- **Dialog mis à jour** : rappel `Cmd+'` affiché avant analyse

## Décisions — Session 7

- **Cmd+' restera manuel** : virtual copy depuis SDK LR est une impasse — accepté
- **Opus 4.7 pour analyse photo** : meilleure lecture lumières/détails, coût justifié pour usage sérieux

## Prochaine étape

- Connecter `jc.havaux@jchytech.be` à Gmail (accès admin M365 requis)
- Premier brief Nova : séquence photo (combat d'oiseaux)
- Premier brief Vasco : produit Vetalyx spécifique
- Définir le contenu Energy department
- Batch processing + prompt caching (quand besoin identifié)
