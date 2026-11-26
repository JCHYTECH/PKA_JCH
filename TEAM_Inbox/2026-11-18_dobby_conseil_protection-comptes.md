---
date: 2026-11-18
source: dobby
domain: protection-comptes
type: conseil-verdict
status: actif
lang: fr
---

# Conseil — Verdict : politique de protection des comptes et secrets PKA

> Dobby 🦉 chairman — 5 stances en parallèle (Contrarian, Premiers Principes, Expansionniste, Outsider, Prémortem), seedées par l'analyse `/analyse-transcript` protection-comptes du 18/11.
> Faits **vérifiés sur pièces par Dobby** avant de figer (ne pas répercuter les auto-rapports des stances sans contrôle).

## Décision
Adopter une politique figée de protection des comptes en ligne et des secrets pour le système PKA — à quel niveau d'ambition, et quelles règles invariables ?

## Faits vérifiés (contre-vérification Dobby)

| Fait | Source stance | Vérification |
|---|---|---|
| Repo GitHub `JCHYTECH/PKA_JCH` **public** | Contrarian | ✅ Confirmé — API GitHub `visibility: public`, `private: false` |
| « 5 secrets exposés dont une clé `sk-` » dans l'historique | Contrarian | ❌ **Faux positif** — `sk-` = CSS `-webkit-mask-image` ; `AIza` = blob base64 ; `xox`/`Bearer` = faux positifs / `Bearer localhost`. **Aucun secret réel** dans l'historique (0 correspondance sur les motifs clés réels) |
| `JCH_PRIVATE/credentials-central.md` jamais committé | Premiers Principes | ✅ Confirmé — `.gitignore` ligne 2 + `git log --all -- JCH_PRIVATE/*` vide |
| **1Password déjà installé** | Premiers Principes | ✅ Confirmé — `/Applications/1Password.app` |
| `credentials-central.md` 211 lignes en clair (local, ignoré git) | — | ✅ Confirmé — `wc -l` = 211 |
| `api_keys` en clair 0600 | — | ✅ Confirmé — `-rw-------` |

## Verdict

**Recommandation : CONDITIONNEL — niveau « B réduit », recentré sur le vrai risque.**

La politique candidate (5 règles avec 2 clés FIDO2, couverture totale, rotation automatisée) **sur-protégeait le sommet et sous-protégeait le vrai risque**. Les 5 stances convergent sur une politique plus sobre.

## Politique figée (les 6 règles invariables)

1. **Coffre = source unique.** 1Password (déjà installé). Tous les mots de passe/clés y vivent. `credentials-central.md` ne garde que des renvois (`→ coffre : entrée « HA M5 »`). **Plus aucun secret en clair.** (P0 — migration, pas un achat.)
2. **Inventaire des comptes maîtres** (6–8 : mail, Apple, Google, 1Password, GitHub, domaine/DNS, banque, Tailscale) — vivant, daté, **avec la localisation physique des moyens de secours** (pas juste l'état 2FA).
3. **Double authentification par appli (TOTP) + passkeys sur les comptes maîtres.** Pas de SMS en secours une fois l'appli en place. **Clé physique FIDO2 = différée** (risque d'auto-blocage, gain marginal pour un non-technique) — seulement si besoin plus tard, sur 2 comptes max, **jamais en unique**.
4. **Codes de secours imprimés sur papier, rangés HORS du coffre** (sinon circularité), + **une enveloppe scellée** remise à une personne de confiance (cas d'incapacité). C'est le vrai filet — valeur supérieure aux clés physiques, coût quasi nul.
5. **Rotation sur événement** (fuite suspectée), **jamais de rotation périodique** (dogme qui produit `Été2024!`).
6. **Le repo GitHub est public** : rien de sensible n'y entre jamais (`JCH_PRIVATE/` déjà ignoré, hook pre-commit à maintenir). Aucun secret exposé aujourd'hui, mais c'est une contrainte **permanente**.

## Arguments pour
- Le coffre (1Password déjà payé) donne 80 % du bénéfice pour ~0 achat et 0 complexité technique — tous les regards convergent là.
- Recentrer sur les comptes maîtres (mail en tête) plutôt que « tout durcir » évite l'abandon réaliste.
- Codes de secours papier + enveloppe scellée couvrent les deux modes d'échec réels : **perte** (clé/téléphone) et **absence de JC**.

## Arguments contre
- Niveau « B réduit » ne protège pas la flotte (M1 headless, RPi, agents à accès shell) — les secrets les plus actifs restent lisibles localement.
- Une politique « figée » mais sans rituel de reprise testée redevient vite de la décoration (le scénario Prémortem).
- Différer la clé physique laisse le mail/Apple en TOTP/passkey — un cran sous le plafond théorique.

## Objection la plus forte (dissidence obligatoire à traiter)
**Premiers Principes** — « la politique répond à la mauvaise question » : le vrai risque de JC n'est pas l'attaquant distant, mais le **risque local et agent-médié** (4 machines, agents IA à accès shell, prompt-injection via contenu ingéré ; un seul `cat` exfiltre l'infra). Aucune des actions FIDO2 ne le réduit.

**Réponse à l'objection** : acceptée et intégrée. La règle 1 ne se limite pas à « migrer le fichier » : elle impose de **réduire ce que les scripts/agents peuvent lire** (clés scopées par agent, moindre privilège, quotas de dépense). Le coffre 1Password devient le registre d'identité interrogé par les scripts au lieu de clés recopiées dans `mcp_ollama_server`, `graphify_llm_bridge`, `photo_keyworder`. C'est un chantier distinct, P1, mais il fait partie de la politique — sinon on ne traite qu'un symptôme.

## Résidu de risque (ce qu'on assume)
- On accepte de rester en TOTP/passkey sur le mail/Apple tant que la clé physique est différée.
- On accepte que la flotte (M1/RPi) ne soit pleinement couverte qu'à l'étape « identités machine » (P1), pas dès la V1.

## Dissent
- **Contrarian** maintient que le « demi-FIDO » (2 comptes faits, clé de secours non enrôlée partout) est plus dangereux que pas de FIDO — traité en différant la clé physique tant que les 2 clés ne sont pas enrôlées ensemble.
- **Outsider** juge la clé physique « excessive » pour un non-technique — aligné avec le verdict.
- **Expansionniste** pousse pour inclure les identités machine dès la V1 — accepté partiellement (règle 1 étendue), le reste en P1.

## Actions découlées (ordre)
1. **P0 — Migration coffre** : basculer les 211 lignes de `credentials-central.md` vers 1Password, ne laisser que des renvois. (Dobby prépare, JC valide.)
2. **P0 — Inventaire des comptes maîtres** : 6–8 lignes, état daté + emplacement des secours.
3. **P1 — 2FA appli + passkeys** sur mail/Apple/Google/GitHub ; codes de secours imprimés + enveloppe scellée.
4. **P1 — Moindre privilège des agents** : scopper les clés lues par les scripts (réponse à l'objection Premiers Principes).
5. **P2 — Reprise testée** (simuler la perte sur un compte non critique) avant d'envisager la clé physique.
