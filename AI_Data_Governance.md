---
date: 2026-05-28
type: governance
status: draft
owner: "[[Dobby]]"
project: "[[01_AI_IT_TOOLS]]"
phase: "Phase 1.3 — Gouvernance documentaire et runtime"
source:
  - "[[AI_System_Blueprint]]"
  - "[[AI_Runtime_Audit]]"
  - "[[Runtime_Service_Register]]"
  - "[[JCH_Inbox/99_SYSTEM/security/policy|PKA Security Policy]]"
---

# AI Data Governance — PKA_JCH

## Position

Ce document définit les règles de gouvernance documentaire, runtime et sécurité pour [[PKA_JCH]].

Il ne crée aucune nouvelle infrastructure. Il fixe les conditions minimales avant toute extension technique.

Principe central :

> L'assistant propose, JCH décide. Le système ne s'auto-étend pas.

## 1. Niveaux d'autonomie

| Niveau | Nom | Autorisé | Validation humaine |
|---|---|---|---|
| L0 | Lecture seule | Lire, auditer, résumer, diagnostiquer. | Non requise sauf secret ou donnée sensible. |
| L1 | Brouillon contrôlé | Créer notes, rapports, registres, plans, livrables non actifs. | Requise avant publication ou activation. |
| L2 | Automatisation validée | Exécuter un workflow éprouvé, borné, journalisé, réversible. | Requise avant première activation et tout changement de périmètre. |
| L3 | Action critique | Suppression, déplacement massif, publication, email, achat, secret, réseau, DB source. | Toujours explicite et préalable. |

## 2. Zones documentaires

| Zone | Rôle | Niveau par défaut | Règle d'écriture |
|---|---|---:|---|
| `TEAM/team.db` | Source de vérité roster et données PKA. | L3 | Ne pas modifier sans validation explicite et backup préalable. |
| `TEAM/` | Identités spécialistes et miroirs. | L1-L3 | Écriture contrôlée; doit rester aligné avec `TEAM/team.db`. |
| `MEMORY.md` | Mémoire globale portable. | L3 | Modification seulement pour décisions consolidées. |
| `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `Codex.md`, `ADAPTER-PROMPT.md` | Pointeurs runtime. | L3 | Régénération ou édition après validation. |
| `JCH_Inbox/00_INBOX/` | Entrées non traitées. | L0-L1 | Lire et classer en brouillon; déplacement sur validation si sensible. |
| `JCH_Inbox/03_PROJECTS/` | Projets actifs. | L1-L2 | Créer/éditer documents projet avec propriétaire et wikilinks. |
| `JCH_Inbox/99_SYSTEM/` | Configs système et sécurité. | L3 | Lecture prudente; édition validée; secrets non copiés. |
| `TEAM_Inbox/` | Livrables spécialistes. | L1 | Écriture autorisée; consolidation ultérieure requise. |
| `wiki/Daily/` | Journal et mémoire de session. | L1-L2 | Écriture autorisée via `/save` ou note datée. |
| `wiki/Knowledge/` | Connaissance consolidée. | L1-L2 | [[Corbeau]] propriétaire; éviter les doublons. |
| `wiki/SOPs/` | Procédures validées. | L1-L2 | Créer SOP après workflow éprouvé. |
| `scripts/` | Automatisations. | L2-L3 | Éditer avec test; activer seulement après validation. |
| `scripts/launchd/` et `~/Library/LaunchAgents/` | Services planifiés. | L3 | Toute activation/désactivation doit être tracée. |
| `tmp/`, `scripts/logs/` | Logs et runtime. | L2 | Pas de secrets; fichiers sensibles en `0600`; rotation à définir. |
| `TEAM/backups/` | Backups DB. | L2-L3 | Génération autorisée par script validé; fichiers en `0600`. |
| `JCH_Inbox/07_ARCHIVES/` | Archives. | L0-L3 | Ne pas modifier sauf archivage validé. |

## 3. Zones interdites ou sensibles

| Zone / type | Règle |
|---|---|
| `.env`, `.env.*` | Ne jamais afficher ni copier; permissions `0600`. |
| `*token*`, `*credentials*`, `*secret*`, `*key*` | Lecture seulement si nécessaire et validée; jamais dans un livrable. |
| Logs contenant tokens/API URLs | Purger ou redacter; rotation du secret si exposition. |
| `TEAM/team.db` | Backup avant modification; vérifier avec audit. |
| Exposition réseau `0.0.0.0`, LAN, public | Validation JCH obligatoire. |
| Suppression récursive ou déplacement massif | Validation JCH obligatoire. |
| Envoi email, publication, achat, commande | Validation JCH obligatoire. |

## 4. Politique secrets

Règles obligatoires :

- Les secrets vivent hors documents versionnés quand c'est possible, idéalement sous `~/.config/pka-jch/`.
- Les `.env` runtime locaux sont tolérés uniquement avec permissions `0600`.
- Les `.env.example` contiennent seulement des placeholders.
- Les tokens/API keys ne doivent jamais apparaître dans Markdown, logs, captures ou réponses chat.
- Si un token apparaît dans un log ou un transcript, il est considéré comme compromis.
- Après exposition : rotation du secret, purge/redaction des logs, correction du logging.

## 5. Politique runtime

### 5.1 LaunchAgents

Tout LaunchAgent PKA doit avoir :

- un owner ;
- un objectif ;
- une fréquence ;
- des inputs/outputs ;
- des logs ;
- un rollback ;
- une validation JCH avant activation.

État de référence : voir [[Runtime_Service_Register]].

### 5.2 Cron

Le crontab doit rester court et lisible. Chaque ligne active doit correspondre à un service documenté dans [[Runtime_Service_Register]].

Règle : tout ajout, retrait ou modification de fréquence doit être noté dans [[AI_Runtime_Audit]] ou dans le registre runtime.

### 5.3 Docker et ports

Docker est autorisé pour les services déjà existants, notamment Plane, mais ne valide pas l'ajout d'une nouvelle stack.

Règles :

- binding local `127.0.0.1` par défaut ;
- `0.0.0.0` ou LAN uniquement après validation JCH ;
- ports documentés dans [[Runtime_Service_Register]] ;
- aucune nouvelle brique Hermes/n8n/Qdrant/Redis/PostgreSQL hors Plane sans phase technique validée.

## 6. Journalisation

Chaque automatisation L2 doit enregistrer :

- date/heure ;
- acteur/service ;
- objectif ;
- inputs principaux ;
- fichiers touchés ;
- statut ;
- erreur éventuelle ;
- besoin de validation humaine ;
- rollback si action persistante.

Les logs doivent éviter :

- corps complet d'email ;
- tokens ;
- URLs d'API contenant secrets ;
- données personnelles inutiles ;
- dumps complets de documents sensibles.

## 7. Validation humaine obligatoire

Validation JCH explicite requise pour :

- suppression ou déplacement massif ;
- modification `TEAM/team.db`;
- modification `MEMORY.md`;
- modification des pointeurs runtime ;
- activation d'un cron ou LaunchAgent ;
- modification d'un secret ;
- exposition réseau non locale ;
- installation de dépendance ou outil ;
- lancement de Docker/stack nouvelle ;
- publication externe ;
- envoi email ;
- achat ou engagement financier ;
- automatisation autonome persistante.

## 8. Registres obligatoires

| Registre | Rôle | Owner |
|---|---|---|
| [[AI_System_Blueprint]] | Carte globale du système. | [[Dobby]] |
| [[AI_Runtime_Audit]] | Audit runtime et remédiations. | [[Dobby]] + [[Forge]] |
| [[Runtime_Service_Register]] | Services actifs/suspendus/obsolètes. | [[Forge]] + [[Castor]] |
| [[Phase_1_Closure_Report]] | Clôture Phase 1 et critères de passage de phase. | [[Dobby]] |
| `JCH_Inbox/99_SYSTEM/security/incident-log.md` | Incidents sécurité. | [[Dobby]] + [[Castor]] |
| `TEAM/ROSTER.md` | Miroir roster humain. | [[Dobby]] |

## 9. Règles de passage de phase

Avant Phase technique minimale :

1. `python3 scripts/pka_security_audit.py` doit être GREEN ou exceptions documentées.
2. [[Runtime_Service_Register]] doit refléter les services actifs et suspendus.
3. Toute exposition réseau non locale doit être validée ou corrigée; Plane est le cas de référence et doit rester en `127.0.0.1` sauf validation JCH.
4. Les P0 runtime doivent être clos ou explicitement acceptés.
5. Les workflows à automatiser doivent exister d'abord comme procédure manuelle claire.

## 10. Décision

La gouvernance PKA reste file-first et audit-first.

Les bases, orchestrateurs et agents persistants ne sont pas autorisés tant que le système documentaire et runtime existant n'est pas stabilisé.

## Voir aussi

- [[AI_System_Blueprint]]
- [[AI_Runtime_Audit]]
- [[Runtime_Service_Register]]
- [[Phase_1_Closure_Report]]
- [[Dobby]]
- [[Forge]]
- [[Castor]]
- [[Corbeau]]
- [[JCH_Inbox/99_SYSTEM/security/policy|PKA Security Policy]]
