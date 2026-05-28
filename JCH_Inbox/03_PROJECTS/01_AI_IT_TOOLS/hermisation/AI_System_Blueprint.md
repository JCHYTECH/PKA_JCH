---
date: 2026-05-28
type: system-blueprint
status: draft
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 1 — Cartographie et stabilisation"
source:
  - "[[MEMORY]]"
  - "[[TEAM/ROSTER]]"
  - "[[TEAM/team.db]]"
  - "[[PKA Hermisation]]"
---

# AI System Blueprint — PKA_JCH

## Position

Ce document est la carte initiale du système AI [[PKA_JCH]]. Il précède toute infrastructure nouvelle.

Décision de phase : **ne pas installer, connecter ou orchestrer de nouvelle couche technique tant que cette cartographie n'est pas validée par JCH.**

Ce blueprint applique le principe suivant :

> Comprendre le système avant de l'automatiser.

## Statuts de certitude

| Statut | Sens |
|---|---|
| Confirmé | Observé directement dans les fichiers, la base `TEAM/team.db`, les scripts ou les configurations. |
| Observé | Présent dans le dépôt ou les journaux, mais fonctionnement réel à vérifier en runtime. |
| Inféré | Déduit de conventions, noms de fichiers ou documentation existante. |
| À vérifier | Information utile mais non prouvée au moment de cette version. |

## Sources consultées

| Source | Utilité | Statut |
|---|---|---|
| `TEAM/team.db` | Roster, tables système, index de fichiers. | Confirmé |
| `TEAM/ROSTER.md` | Miroir humain du roster. | Confirmé |
| `MEMORY.md` | Règles de comportement, projets actifs, politiques. | Confirmé |
| `ADAPTER-PROMPT.md`, `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Codex.md` | Pointeurs runtime et identité Dobby. | Confirmé |
| `scripts/model_config.json` | Routage modèles par tâche. | Confirmé |
| `scripts/launchd/*.plist` | Automatisations macOS prévues ou actives. | Observé |
| `JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation/` | Cadrage Hermisation, garde-fous, roadmap. | Confirmé |
| `JCH_Inbox/99_SYSTEM/security/policy.md` | Politique sécurité PKA. | Confirmé |

## Résumé exécutif

Le système actuel n'est pas un système multi-agent autonome. C'est un **vault opérationnel file-first**, piloté par [[Dobby]], enrichi par :

- un roster de 28 membres actifs ;
- des spécialistes conceptuels avec identités et responsabilités ;
- des scripts Python et shell ;
- des services planifiés via launchd ;
- des dashboards HTML locaux ;
- des connecteurs externes partiels : Dropbox, Gmail, Outlook, Google Calendar, Plane, Telegram, Tailscale ;
- un routage de modèles AI centralisé par tâche.

Le risque principal n'est pas le manque d'outils. Le risque principal est la **surautomatisation avant stabilisation documentaire**.

## 1. Inventaire des agents

### 1.1 Types d'agents

| Type | Description | Autonomie actuelle | Statut |
|---|---|---:|---|
| Orchestrateur | [[Dobby]], point d'entrée et synthèse. | L1-L2 selon tâche | Confirmé |
| Spécialistes PKA | 27 rôles experts dans `TEAM/`. | L0-L1, exécutés via Dobby | Confirmé |
| Scripts automatisés | Python/shell sous `scripts/` et `bin/`. | L1-L2 selon script | Confirmé |
| Services launchd | Exécution périodique ou au démarrage. | L2 | Observé |
| Dashboards | Interfaces HTML locales. | L0-L1 | Confirmé |
| Modèles AI | Claude, Ollama, NVIDIA/DeepSeek, OpenAI, Google, autres providers configurés. | Dépend de l'appelant | Confirmé |
| Hermes-like | Concepts seulement, pas infrastructure activée. | L0 | Confirmé |

### 1.2 Roster conceptuel

Source : `TEAM/team.db`, 28 membres actifs.

| Agent | Fonction | Autonomie actuelle | Criticité | Données principales | Statut |
|---|---|---:|---|---|---|
| [[Dobby]] | Orchestration générale, triage, synthèse, mémoire. | L1-L2 | Élevée | Tout PKA, `MEMORY.md`, `TEAM/`, `JCH_Inbox/`, `wiki/` | Confirmé |
| [[Bouvier]] | Recrutement et onboarding spécialistes. | L1 | Moyenne | `TEAM/`, roster, responsabilités | Confirmé |
| [[Furet]] | Recherche senior, veille, profils de compétences. | L1 | Moyenne | `knowledge`, projets, web si demandé | Confirmé |
| [[Castor]] | Base de données et systèmes. | L1-L2 | Élevée | `TEAM/team.db`, scripts DB, schémas | Confirmé |
| [[Corbeau]] | Curateur de connaissance. | L1 | Élevée | `wiki/Knowledge`, `knowledge`, `knowledge_links` | Confirmé |
| [[Delphi]] | CRM et relations. | L1 | Moyenne | `contacts`, `interactions`, `follow_ups` | Confirmé |
| [[Héron]] | Impression photo. | L1 | Faible-Moyenne | PHOTO, papiers, presets, impressions | Confirmé |
| [[Lynx]] | Édition photo. | L1 | Moyenne | PHOTO, Lightroom, Photoshop, analyses | Confirmé |
| [[Jade]] | Traduction EN/ZH et analyse culturelle. | L1 | Élevée pour VETALYX/DIAHO | Contrats, documents bilingues, Chine | Confirmé |
| [[Renard]] | Conseil juridique contrats. | L1 | Élevée | Contrats, CGU, pactes, risques | Confirmé |
| [[Iris]] | Tendances et stratégie recherche. | L1 | Moyenne | Idées, veille, marchés | Confirmé |
| [[Forge]] | Développement, intégrations, automatisations. | L1-L2 | Élevée | `scripts/`, dashboards, APIs, runtime | Confirmé |
| [[Ariane]] | Onboarding plateformes. | L1 | Moyenne | SOPs, comptes, procédures | Confirmé |
| [[Bruno]] | Finance et investissement. | L1 | Moyenne | Modèles financiers, fiscal, business | Confirmé |
| [[Sybil]] | Journal personnel et mémoire quotidienne. | L1-L2 | Élevée | `wiki/Daily`, `journal`, goals | Confirmé |
| [[Clio]] | Littérature scientifique. | L1 | Élevée pour scientifique | Publications, clinical, bioacoustique | Confirmé |
| [[Sigma]] | Analyse données financières. | L1 | Moyenne | Tableurs, chiffres, projections | Confirmé |
| [[Vega]] | Direction créative web/brand. | L1 | Moyenne | ARTEON, identité, maquettes | Confirmé |
| [[Trace]] | SEO et visibilité. | L1 | Moyenne | SEO, contenus, analytics | Confirmé |
| [[Miel]] | Community et contenu marque. | L1 | Moyenne | Réseaux, publications, calendriers | Confirmé |
| [[Vasco]] | Produit vétérinaire Vetalyx. | L1 | Élevée | VETALYX, clinique, allergie animale | Confirmé |
| [[Nova]] | R&D photographie. | L1 | Moyenne | PHOTO, workflows, outils | Confirmé |
| [[Argus]] | Critique photo et jury. | L1-L2 | Moyenne | PHOTO_AI_JURY, `argus_critique.db` | Confirmé |
| [[Pie]] | Analyse mails et service client. | L1-L2 | Élevée si emails actifs | Emails, imports, triage | Confirmé |
| [[Chouette]] | Terrain, caméras, bioacoustique. | L1 | Élevée pour WILDNEXUS | RPi, BirdNET, terrain, matériel | Confirmé |
| [[Milan]] | OSINT et intelligence industrielle. | L1 | Moyenne-Élevée | Veille, concurrents, marché | Confirmé |
| [[Atlas]] | Architecture documents stratégiques/R&D. | L1 | Moyenne-Élevée | Dossiers techniques, synthèses longues | Confirmé |
| [[Hermine]] | Propriété intellectuelle et brevets. | L1 | Élevée si IP | Brevets, invention, liberté exploitation | Confirmé |

### 1.3 Agents runtime et automatisations

| Agent / service | Fonction réelle | Modèle | Inputs | Outputs | Fréquence | Autonomie | Criticité | Statut |
|---|---|---|---|---|---|---:|---|---|
| `pka_system_check.py` | Vérifie état système et écrit rapports. | Aucun direct observé | Vault, fichiers système | `TEAM_Inbox/*_system_check.md` | 6 h via launchd | L2 | Élevée | Observé |
| `pka_vault_maintenance.py` | Maintenance vault, conventions, corrections limitées. | Aucun direct observé | Vault markdown | Logs, corrections possibles | 02:00 via launchd | L2 | Élevée | Observé |
| `dropbox_watch.py` | Surveille Dropbox VETALYX. | Aucun direct observé | `/Users/jchavauxm5/Dropbox/VETALYX` | Snapshots, rapports | WatchPaths | L2 | Élevée | Observé |
| `gmail_gatekeeper.py` | Scan Gmail selon politique. | À vérifier | Gmail config/token | Logs, triage possible | 20 min via launchd | L2 | Élevée | Observé |
| `outlook_imap.py` | Gatekeeper Outlook/IMAP. | À vérifier | Outlook/IMAP | Logs, triage possible | 15 min via launchd | L2 | Élevée | Observé |
| `email_digest.py` | Digest email. | Claude Haiku configuré pour `email_digest` | Emails / configs | Digest/logs | 09:00, 14:00, 20:00 | L2 | Moyenne | Observé, mais MEMORY indique digest suspendu |
| `dashboard_server.py` | Serveur dashboard local. | Aucun | Dashboards, fichiers PKA | HTTP local `127.0.0.1:8787` | KeepAlive | L2 | Moyenne | Observé |
| `plane-autostart.sh` | Maintien Plane local. | Aucun | Plane config | Service Plane | 5 min + RunAtLoad | L2 | Moyenne | Observé |
| `pka_save.py` | Sauvegarde interactive/session. | Dépend usage | Résumés, projets | Daily, TEAM_Inbox, mémoire | Manuel | L1 | Élevée | Confirmé |
| `model_client.py` | Routeur d'appels modèles. | Voir `scripts/model_config.json` | Prompts/tâches | Réponses modèle | Appelé par scripts | L1-L2 | Élevée | Confirmé |
| Scripts InsectNet | Téléchargement, segmentation, QC audio. | À vérifier | Audio/datasets | Spectrogrammes, inventaires, QC | Manuel | L1-L2 | Moyenne | Confirmé |
| Scripts procurement | BOM, Digi-Key, achats. | À vérifier | BOM, API Digi-Key | Rapports, paniers | Manuel | L1 | Moyenne-Élevée | Confirmé |
| Telegram bot | Interface Dobby Telegram. | Claude Sonnet configuré pour `telegram_bot` | Telegram, contexte Dobby | Réponses, conversation DB | Potentiellement permanent | L2 | Élevée | Observé |

### 1.4 Routage modèles observé

Source : `scripts/model_config.json`.

| Tâche | Provider | Modèle | Statut |
|---|---|---|---|
| Défaut | Anthropic | `claude-sonnet-4-6` | Confirmé |
| Journal | Ollama | `qwen3.6:latest` | Confirmé |
| Retro | Ollama | `qwen3.6:latest` | Confirmé |
| Weekly report | Anthropic | `claude-sonnet-4-6` | Confirmé |
| Email digest | Anthropic | `claude-haiku-4-5-20251001` | Confirmé |
| Telegram bot | Anthropic | `claude-sonnet-4-6` | Confirmé |
| Skill write | Ollama | `gemma4:latest` | Confirmé |
| Skill search | Ollama | `gemma4:latest` | Confirmé |
| NVIDIA | NVIDIA | `deepseek-v4-pro` | Confirmé |
| Codex session courante | OpenAI | GPT-5 | Confirmé par runtime |

Providers configurés : Anthropic, OpenAI, Google, Ollama, NVIDIA, DeepSeek, Kimi, OpenRouter.

## 2. Cartographie documentaire

### 2.1 Dossiers critiques

| Zone | Rôle | Écriture AI autorisée | Risque | Statut |
|---|---|---:|---|---|
| `TEAM/team.db` | Source de vérité équipe et données PKA. | Validation humaine requise | Perte/corruption DB | Confirmé |
| `TEAM/` | Identités spécialistes, roster miroir. | Brouillons ou mises à jour contrôlées | Divergence DB/Markdown | Confirmé |
| `MEMORY.md` | Mémoire portable et règles globales. | Validation humaine recommandée | Dérive système | Confirmé |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Codex.md`, `ADAPTER-PROMPT.md` | Pointeurs runtime et identité. | Validation humaine recommandée | Désalignement identité/protocole | Confirmé |
| `JCH_Inbox/99_SYSTEM/` | Configs système, sécurité, tokens Google présents. | Très limité | Secrets/configs sensibles | Confirmé |
| `scripts/` | Automatisations et services. | Tests + validation | Automatisation dangereuse | Confirmé |
| `scripts/launchd/` | Services planifiés. | Validation humaine obligatoire avant installation | Actions permanentes | Confirmé |
| `wiki/` | Connaissance, SOP, Daily. | Oui selon conventions | Pollution documentaire | Confirmé |
| `JCH_Inbox/03_PROJECTS/` | Projets actifs. | Oui, avec propriétaire et contexte | Mauvais classement | Confirmé |
| `TEAM_Inbox/` | Livrables spécialistes. | Oui | Accumulation non consolidée | Confirmé |

### 2.2 Dossiers runtime

| Zone | Usage | Risque | Statut |
|---|---|---|---|
| `tmp/` | Logs launchd et temporaires. | Logs sensibles ou volumineux | Observé |
| `scripts/logs/` | Logs scripts. | Secrets accidentels, rotation absente | Observé |
| `scripts/__pycache__/` | Cache Python. | Bruit documentaire | Confirmé |
| `scripts/telegram-bot/conversation.db` | Historique bot. | Données conversationnelles sensibles | Observé |
| `JCH_Inbox/00_INBOX/` | Zone d'arrivée documents. | Entrée non fiable, prompt injection documentaire | Confirmé |

### 2.3 Archives

| Zone | Usage | Écriture AI | Statut |
|---|---|---:|---|
| `JCH_Inbox/07_ARCHIVES/` | Archives et anciens imports. | Non sauf classement validé | Confirmé |
| `TEAM/backups/` | Backups DB. | Non, sauf script backup validé | Confirmé |
| `backups/` | Sauvegardes générales. | À vérifier | Observé |

### 2.4 Fichiers sensibles observés

| Fichier | Sensibilité | Action Phase 1 | Statut |
|---|---|---|---|
| `JCH_Inbox/99_SYSTEM/google_calendar_credentials.json` | Credentials Google | Marquer zone interdite aux agents non validés | Confirmé |
| `JCH_Inbox/99_SYSTEM/google_calendar_token.json` | Token Google | Marquer zone interdite, vérifier permissions | Confirmé |
| `scripts/telegram-bot/.env` | Secrets runtime Telegram | Interdit lecture/copie dans livrables | Confirmé |
| `TEAM/team.db` | Données source de vérité | Backup + accès contrôlé | Confirmé |
| `TEAM/backups/*.db` | Sauvegardes sensibles | Permissions 0600 | Confirmé |
| `scripts/model_config.json` | Providers et chemins de clés | Ne pas exposer clés, chemins acceptables | Confirmé |

### 2.5 Zones AI autorisées et interdites

| Niveau | Zones | Règle |
|---|---|---|
| Autorisé L1 | `TEAM_Inbox/`, `wiki/Daily/`, `wiki/SOPs/`, `JCH_Inbox/03_PROJECTS/*` | Création de brouillons et livrables avec wikilinks. |
| Autorisé contrôlé L2 | `scripts/`, `JCH_Inbox/01_DASHBOARDS/`, `wiki/Knowledge/` | Tests, diff, validation, journalisation. |
| Sensible L3 | `TEAM/team.db`, `MEMORY.md`, pointeurs runtime, `scripts/launchd/` | Modification seulement avec validation humaine explicite. |
| Interdit par défaut | Secrets, tokens, `.env`, credentials, suppressions massives | Pas de copie dans Markdown, pas d'exposition, pas d'autonomie. |

## 3. Cartographie workflows

### 3.1 Workflows existants

| Workflow | Description | Données | Acteurs | Automatisation | Criticité | Statut |
|---|---|---|---|---:|---|---|
| Activation Dobby | Lecture mémoire, roster, protocole, inbox. | `MEMORY.md`, `TEAM/`, `wiki/`, inbox | Dobby | Manuel à chaque session | Élevée | Confirmé |
| Inbox triage | Lire, loguer, router les fichiers entrants. | `JCH_Inbox/00_INBOX/`, `file_index` | Dobby, Pie, spécialistes | Partiel | Élevée | Confirmé |
| Sauvegarde session | Capturer décisions/actions dans Daily/TEAM_Inbox. | `pka_save.py`, `wiki/Daily` | Dobby, Sybil | Manuel interactif | Élevée | Confirmé |
| System check | Rapport périodique santé PKA. | Vault, scripts, DB | Dobby/Castor/Forge | launchd | Élevée | Observé |
| Vault maintenance | Maintenance conventions et placement. | Vault Markdown | Forge/Corbeau | launchd | Élevée | Observé |
| Dropbox VETALYX | Surveiller documents Dropbox. | Dropbox VETALYX | Forge/Vasco | launchd | Élevée | Observé |
| Email gatekeeping | Scan Gmail/Outlook, digest. | Email, configs | Pie/Dobby | launchd | Élevée | Observé |
| Dashboards | Hub, organigramme, live dashboard. | `JCH_Inbox/01_DASHBOARDS/` | Forge/Dobby | Serveur local | Moyenne | Confirmé |
| WildNexus bioacoustique | Protocoles RPi/BirdNET, QC audio, terrain. | WILDNEXUS, audio, scripts InsectNet | Chouette, Clio, Forge | Partiel | Élevée | Confirmé |
| VETALYX clinique | Documents techniques, DIXUN, validations. | VETALYX, PDF/DOCX/HTML | Vasco, Clio, Jade, Renard | Partiel | Élevée | Confirmé |
| Procurement/BOM | BOM et paniers composants. | BOM, Digi-Key API | Forge, Bruno, Chouette | Partiel | Moyenne | Confirmé |

### 3.2 Tâches répétitives

| Tâche | Automatisable ? | Niveau cible | Condition |
|---|---:|---:|---|
| Créer note Daily de session | Oui | L2 | Après validation format et `/save`. |
| Générer rapport système | Oui | L2 | Déjà partiel, doit documenter fichiers touchés. |
| Classer fichier inbox | Partiel | L1-L2 | Brouillon + validation humaine si déplacement. |
| Mettre à jour file_index | Oui | L2 | Sans suppression automatique. |
| Générer SOP à partir d'une procédure validée | Oui | L1 | Relecture JCH. |
| Surveiller dossiers externes | Oui | L2 | Scope strict, logs, pas de suppression. |
| Résumer emails | Oui | L1-L2 | Pas d'action externe sans validation. |
| Publier, envoyer, acheter, supprimer | Non autonome | L3 | Validation humaine obligatoire. |

### 3.3 Redondances et frottements

| Zone | Redondance / friction | Impact | Statut |
|---|---|---|---|
| Roster | `TEAM/team.db`, `TEAM/ROSTER.md`, pointeurs runtime. | Divergence possible. | Confirmé |
| Mémoire | `MEMORY.md`, Daily, TEAM_Inbox, transcripts. | Décisions dispersées. | Confirmé |
| AI tools | Claude, Codex, Gemini, DeepSeek, Ollama, NVIDIA. | Modèle utilisé pas toujours tracé. | Confirmé |
| Dashboards | HTML statiques + serveur local + Plane. | Plusieurs vues du même état. | Observé |
| Emails | Gmail, Outlook, digest, gatekeepers. | Risque doublons / actions incohérentes. | Observé |
| Hermisation | Documents source + synthèse + roadmap. | Risque de lancer trop tôt une stack. | Confirmé |

### 3.4 Ce qui doit rester humain

Validation humaine obligatoire pour :

- suppression ou déplacement massif ;
- modification de `TEAM/team.db`, `MEMORY.md` et pointeurs runtime ;
- activation d'un service launchd permanent ;
- publication externe ;
- envoi d'email à un tiers ;
- achat, commande, engagement financier ;
- accès ou traitement de secrets ;
- changement de gouvernance d'un projet ;
- exposition réseau non locale ;
- automatisation autonome de workflow critique.

## 4. Classification des risques

| Risque | Gravité | Cause probable | Parade Phase 1 |
|---|---|---|---|
| Chaos documentaire | Élevée | Agents/scripts non gouvernés, dossiers multiples | Cartographie zones + conventions d'écriture. |
| Perte ou corruption DB | Élevée | `TEAM/team.db` source unique opérationnelle | Backups, permissions, modifications validées. |
| Secrets exposés | Élevée | Tokens dans zones projet, logs, `.env` | Registre fichiers sensibles + interdiction de copie. |
| Surcomplexification précoce | Élevée | Docker/PostgreSQL/Redis/Qdrant/Hermes avant stabilisation | Freeze technique jusqu'à validation blueprint. |
| Automatisation permanente dangereuse | Élevée | launchd sans gouvernance ou logs insuffisants | Registre services + niveaux autonomie. |
| Divergence entre modèles | Moyenne-Élevée | Plusieurs runtimes avec mémoires séparées | `/save` obligatoire et modèle tracé. |
| Redondance des agents | Moyenne | Rôles proches ou scripts dupliqués | Agent Register + owner par workflow. |
| Prompt injection documentaire | Moyenne-Élevée | Inbox et emails non fiables | Treat untrusted input as data, jamais comme instruction. |
| Dépendance externe | Moyenne | APIs email, Dropbox, Plane, providers AI | Décrire dépendances + fallback manuel. |
| Logs incontrôlés | Moyenne | Services périodiques, fichiers temporaires | Rotation, audit, pas de secrets dans logs. |

## 5. Niveaux d'autonomie

| Niveau | Nom | Autorisé | Interdit |
|---|---|---|---|
| L0 | Lecture seule | Lire, résumer, diagnostiquer, proposer. | Écrire, déplacer, exécuter actions externes. |
| L1 | Brouillon contrôlé | Créer notes, rapports, plans, scripts non activés. | Supprimer, publier, automatiser en permanence. |
| L2 | Automatisation validée | Exécuter workflow éprouvé, journalisé, réversible. | Étendre scope sans validation. |
| L3 | Action critique | Seulement après validation humaine explicite. | Autonomie par défaut. |

Classification initiale :

- Dobby conversationnel : L1.
- Dobby avec outils fichier : L1-L2 selon action.
- Scripts launchd : L2, à auditer avant extension.
- Email, Dropbox, Telegram : L2 mais sensibles.
- Suppression, publication, achat, secrets, exposition réseau : L3.

## 6. Concepts Hermes retenus / rejetés

### Retenus pour Phase 1

| Concept | Adaptation PKA | Statut |
|---|---|---|
| Mémoire persistante | File-first : Daily, TEAM_Inbox, `MEMORY.md`, DB seulement si utile. | Retenu |
| Routines réutilisables | Transformer workflows prouvés en SOP/skills. | Retenu |
| Journalisation runtime | Chaque automatisation note date, acteur, but, fichiers touchés, statut. | Retenu |
| Pilotes limités | Documentation, architecture système, bioacoustique seulement après blueprint. | Retenu plus tard |
| Orchestration légère | Uniquement après validation manuelle des workflows. | Différé |

### Rejetés ou gelés

| Élément | Décision | Raison |
|---|---|---|
| Remplacer [[Dobby]] | Rejeté | Dobby reste orchestrateur. |
| Connecter tout le roster | Rejeté | Prolifération d'agents. |
| Autonomie critique | Rejeté | Validation humaine obligatoire. |
| Écriture filesystem libre | Rejeté | Risque documentaire. |
| Secrets en Markdown | Rejeté | Politique sécurité. |
| Docker/PostgreSQL/Redis/Qdrant/n8n/Hermes | Gelé | Phase technique ultérieure seulement. |

## 7. Freeze technique Phase 1

Pendant la Phase 1, ne pas démarrer :

- installation Hermes ;
- création d'agents persistants ;
- Docker Desktop pour ce projet ;
- PostgreSQL ;
- Redis ;
- Qdrant ;
- n8n ;
- VPS ;
- exposition réseau ;
- automatisation permanente nouvelle.

Actions autorisées :

- lire et inventorier ;
- produire registres ;
- documenter risques ;
- vérifier services existants sans les modifier ;
- créer des livrables Markdown ;
- proposer une gouvernance documentaire.

## 8. Décisions Phase 1

| Décision | Statut |
|---|---|
| Le livrable principal est `AI_System_Blueprint.md`. | Confirmé |
| `Agent_Register.md` est intégré dans ce document pour éviter la multiplication initiale des fichiers. | Proposé |
| L'infrastructure technique commence seulement après validation de la carte. | Confirmé |
| Les documents `pka-hermisation` servent de garde-fous, pas de déclencheur d'installation. | Confirmé |

## 9. Questions ouvertes

| Question | Pourquoi c'est important | Priorité |
|---|---|---|
| Quels services launchd sont réellement chargés/en cours, pas seulement présents dans `scripts/launchd/` ? | Distinguer prévu vs actif. | P0 |
| Le digest email est-il toujours suspendu malgré le plist observé ? | Éviter double vérité entre MEMORY et launchd. | P0 |
| Où doit vivre durablement le registre des zones sensibles ? | Sécurité et audit. | P1 |
| Faut-il séparer `Agent_Register.md` après validation ? | Lisibilité si le registre grossit. | P1 |
| Quels modèles sont effectivement disponibles localement via Ollama ? | Réalisme du routage modèle. | P1 |
| Quelles automatisations touchent des données externes sans revue humaine ? | Surface de risque. | P0 |

## 10. Prochaines étapes

1. Valider ce blueprint avec JCH.
2. Auditer les services réellement chargés : launchd, cron éventuel, processus permanents.
3. Produire un registre court des fichiers sensibles et permissions.
4. Vérifier contradiction `email_digest` : suspendu dans `MEMORY.md`, mais plist présent.
5. Écrire `AI_Data_Governance.md` seulement après validation du blueprint.

## 11. Livrables Phase 1 liés

| Livrable | Rôle | Statut |
|---|---|---|
| [[AI_Runtime_Audit]] | Audit runtime réel : cron, launchd, processus, ports, remédiations P0. | Créé |
| [[AI_Data_Governance]] | Règles de gouvernance documentaire, secrets, runtime, validation humaine. | Créé |
| [[Runtime_Service_Register]] | Registre des services actifs, suspendus, obsolètes et conditions de rollback. | Créé |
| [[Phase_1_Closure_Report]] | Rapport de clôture Phase 1 et conditions d'entrée en phase technique minimale. | Créé |

## Voir aussi

- [[Dobby]]
- [[TEAM/ROSTER]]
- [[MEMORY]]
- [[AI_Runtime_Audit]]
- [[AI_Data_Governance]]
- [[Runtime_Service_Register]]
- [[Phase_1_Closure_Report]]
- [[JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation/README|PKA Hermisation]]
- [[JCH_Inbox/03_PROJECTS/01_AI_IT_TOOLS/pka-hermisation/ROADMAP|Roadmap PKA Hermisation]]
- [[JCH_Inbox/99_SYSTEM/security/policy|PKA Security Policy]]
