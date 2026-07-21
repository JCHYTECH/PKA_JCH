# Audit securite et vigilance PKA_JCH

_Date : 2026-05-13_
_Source : [[Dobby]] / [[Codex]] CLI_

## Etat observe

- `TEAM/team.db` et `team.db` existent tous les deux et ne sont pas binaires identiques.
- La base contient 25 membres actifs, alors que `AGENTS.md` annonce encore 24 specialistes.
- Les projets actifs sont dans `JCH_Inbox/03_PROJECTS/`.
- `JCH_Inbox/00_INBOX/` ne contient aucun fichier en attente.
- Les secrets applicatifs existent dans `scripts/telegram-bot/.env`.
- Plusieurs fichiers sensibles sont lisibles par le groupe et les autres utilisateurs locaux (
- Le dashboard est servi par defaut sur `127.0.0.1:8787` avec token pour acces non local.
- Les backups [[SQLite]] existent dans 
- Aucun depot [[Git]] n'a ete detecte a la racine PKA_JCH.

## Outils deja disponibles

- 
- 
- `scripts/model_client.py` et `scripts/model_config.json` : routage multi-modeles et fichiers de cles dans `~/.config/pka-jch`.
- 
- `TEAM/team.db` : source structuree pour membres, [[inbox]], file index, connaissances, CRM, journal.
- `TEAM/backups/` : historique de snapshots DB.
- `wiki/index.md`, `/lint` mentionne, et [[daily]] notes : socle documentaire pour consigner audits et incidents.
- Outils CLI disponibles via l'environnement : 

## Outils a creer

1. `scripts/pka_security_audit.py`
   - Audit local non destructif.
   - Controle permissions des fichiers sensibles.
   - Detection de secrets potentiellement commites ou places dans le mauvais repertoire.
   - Verification coherence `AGENTS.md` / `TEAM/ROSTER.md` / `TEAM/team.db`.
   - Controle existence et age des backups.
   - Verification absence de venv, logs et bases runtime dans une future sauvegarde [[Git]].
   - Sortie Markdown + JSON dans `TEAM_Inbox/` et `JCH_Inbox/99_SYSTEM/security/`.

2. `scripts/pka_vigilance.py`
   - Surveillance recurrente quotidienne.
   - Score de risque simple : vert, orange, rouge.
   - Alertes sur nouveaux fichiers en `00_INBOX`, nouveaux secrets, permissions relachees, backup absent, DB incoherente, logs volumineux.
   - Integration dashboard via endpoint `/api/security`.

3. `JCH_Inbox/99_SYSTEM/security/policy.md`
   - Regles de base : emplacement des secrets, permissions, rotation, sauvegarde, exposition reseau, donnees personnelles.

4. `JCH_Inbox/99_SYSTEM/security/allowlist.json`
   - Liste des fichiers sensibles attendus.
   - Liste des patterns acceptes pour eviter les faux positifs.
   - Liste des ports locaux autorises.

5. `JCH_Inbox/99_SYSTEM/security/incident-log.md`
   - Journal append-only des alertes et [[decisions]] de mitigation.

## Tableau des failles potentielles

| Risque | Niveau | Surface | Constat | Mitigation |
|---|---:|---|---|---|
| Secrets lisibles localement | Eleve | `.env`, cles API, tokens Telegram/OpenAI/Anthropic | `scripts/telegram-bot/.env` est en `0644` | Passer en `0600`, deplacer les secrets vers `~/.config/pka-jch`, ne garder qu'un `.env.example` dans PKA |
| Bases [[SQLite]] lisibles localement | Eleve | 
| Deux sources DB divergentes | Eleve | `team.db` racine vs `TEAM/team.db` | Les deux fichiers ne sont pas identiques | Designation stricte de `TEAM/team.db` comme source, script de drift-check, suppression ou alias controle de la copie racine apres validation |
| Drift roster/protocole | Moyen | `AGENTS.md`, `ROSTER.md`, DB | AGENTS annonce 24, DB contient 25 actifs | Ajouter controle automatique DB -> mirrors, rapport quand le compte diverge |
| Exposition dashboard | Moyen | `dashboard_server.py` | Local par defaut, mais option `--host` peut exposer le service | Interdire host non-loopback sans flag explicite, token long, cookie `Secure` si HTTPS, audit des ports |
| CSRF dashboard local | Moyen | Endpoints POST dashboard | Protection par header custom, mais pas de nonce CSRF formel | Ajouter nonce de session, verifier Origin/Host, limiter actions sensibles |
| Logs contenant donnees sensibles | Moyen | `*.log`, `conversation.db`, TEAM_Inbox emails | Les logs et historiques sont lisibles en `0644` | Redaction automatique, rotation, permissions `0600`, taille max |
| Venv versionne / surface dependances | Moyen | `scripts/telegram-bot/venv` | Le venv est dans l'arborescence de travail | Exclure via `.gitignore`, reconstruire depuis `requirements.txt`, scanner dependances avec `pip-audit` |
| Dependances [[Python]] anciennes ou vulnerables | Moyen | 
| Bot Telegram comme entree externe | Eleve | `bot.py` | Whitelist user id existe, mais erreurs/API et historique local persistent | Rate limit, limites de taille media, journal minimal, rotation token, tests d'autorisation |
| Prompt injection via fichiers ou messages | Moyen | [[inbox]], wiki, Telegram, [[Dobby]] Live | Les contenus utilisateurs peuvent devenir contexte modele | Regle d'isolation : fichiers lus comme donnees, jamais comme instructions systeme; marqueurs de confiance |
| Perte de donnees | Eleve | `TEAM/team.db`, wiki, TEAM_Inbox | Backups DB uniquement, pas de [[strategie]] complete du vault | Backup vault complet chiffre, test restauration mensuel, retention 3-2-1 |
| Absence de controle d'integrite | Moyen | fichiers systeme, scripts | Pas de hash baseline | Generer manifest SHA256 des fichiers critiques, alerte sur changement |
| Absence de depot [[Git]] detecte | Moyen | tout PKA | Pas d'historique versionne visible | Initialiser depot prive ou strategy de snapshots, 
| Donnees personnelles et emails | Eleve | TEAM_Inbox, CRM, journal | Beaucoup de contenu personnel centralise | Classification confidentialite, droits fichiers, export chiffre, politique de retention |

## Priorites

### P0 - Aujourd'hui

- Passer `.env`, DB, backups et logs en `0600`.
- Clarifier `TEAM/team.db` vs `team.db`.
- Mettre a jour 
- Creer 

### P1 - Cette semaine

- Creer `pka_security_audit.py`.
- Creer `JCH_Inbox/99_SYSTEM/security/policy.md`.
- Ajouter rapport automatique dans `TEAM_Inbox`.
- Ajouter controle dashboard `/api/security`.

### P2 - Ensuite

- Backup chiffre complet du vault.
- Audit dependances automatique.
- Manifest SHA256 des fichiers systeme.
- Journal d'incident append-only.
