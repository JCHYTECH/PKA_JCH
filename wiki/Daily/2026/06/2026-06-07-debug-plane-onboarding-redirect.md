---
date: 2026-06-07
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-06-07 — debug-plane-onboarding-redirect

## Session — 18:12 — debug-plane-onboarding-redirect

### Contexte
- Modèle : Codex CLI / GPT-5
- Projet : 01_AI_IT_TOOLS

### Résumé
Diagnostic et correction Plane self-hosted v1.3.1 : après login, redirection erronée vers Create your workspace malgré workspace pka-jch existant. Cause racine identifiée : profil onboarding incohérent dans profiles, avec is_onboarded=false, last_workspace_id NULL et étapes workspace_* à false.

### Actions
Lecture du contexte Dobby/PKA. Inspection Docker Plane API/Web/Postgres. Vérification des tables users, profiles, workspaces, workspace_members, workspace_user_properties. Correction SQL : profiles.is_onboarded=true, is_tour_completed=true, last_workspace_id=pka-jch, onboarding_step complet ; users.is_email_verified=true et is_email_valid=true ; purge sessions Django ; création de workspace_user_properties manquante.

### Décisions
Pour Plane self-hosted après import/restauration DB, vérifier systématiquement profiles.last_workspace_id, profiles.is_onboarded, profiles.onboarding_step et workspace_user_properties avant de conclure à un problème de credentials ou CORS.

### Prochaines étapes
Si le problème réapparaît côté navigateur, purger Clear site data pour 127.0.0.1:8088. Conserver ce diagnostic comme runbook Plane local.
