# Brief — Validation ADR-011 (Provisioning & cycle de vie des clés)

**De :** [[Dobby]] 🦉
**Pour :** [[Castor]] 🦫 + [[Forge]] 🦦
**Date :** 2026-06-08
**Priorité :** M-02 — conditionne acceptation ADR-010 (R1)
**ADR lié :** ADR-011 (proposé) → à faire passer en « accepté »

## Contexte

L'ADR-011 définit la procédure de provisioning des clés : Master Key YubiKey → HKDF → clé nœud unique en eFuse ESP32-S3.

Il est en statut « proposé ». Pour lever le point de réserve R1 de l'ADR-010, l'ADR-011 doit passer en « accepté ».

## Mission

1. Relire l'ADR-011 et vérifier chaque étape de la procédure de provisioning (§2)
2. Valider la faisabilité technique : HKDF sur YubiKey PIV, gravure eFuse ESP32-S3, moteur AES hardware
3. Identifier les points bloquants éventuels (dispo YubiKey, complexité script provisioning)
4. Si OK → passer l'ADR-011 en « accepté » avec votre validation
5. Si réserves → les documenter et proposer des alternatives

## Format livrable

`YYYY-MM-DD_castor_forge_wildnexus-adr011-validation.md` dans `TEAM_Inbox/`

## Deadline

Avant fermeture M-02.

## Voir aussi

- `ADR-011` — `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/ADR-011-provisioning-cycle-de-vie-cles.md`
- `ADR-010` — point de réserve R1
