# 📋 PKA Kanban — Fiche Dummies

> Pilotage des projets PKA via le Kanban (Plane). Status, rituels, dashboard.

---

## 🚀 ACCÈS

| Action | Comment |
|--------|---------|
| Ouvrir Plane | Via navigateur — URL configurée dans `JCH_Inbox/99_SYSTEM/pka_plane_config.json` |
| Dashboard Kanban | L'interface Plane affiche les cartes par statut |

---

## 🗂️ STATUTS CANONIQUES

Une carte passe par ces 7 statuts, dans l'ordre :

| # | Statut | Signification |
|---|--------|---------------|
| 1 | **A qualifier** | Nouvelle tâche, pas encore évaluée |
| 2 | **Prêt** | Prête à être prise |
| 3 | **En cours** | En train d'être traitée |
| 4 | **En attente** | Bloquée (dépendance externe, attente JCH) |
| 5 | **En validation** | Le travail est fait, JCH doit valider |
| 6 | **Terminé** | Validée et livrée |
| 7 | **Archive** | Classée |

---

## 🏷️ TYPES DE CARTES

| Type | Usage |
|------|-------|
| `task` | Tâche standard |
| `decision` | Décision à prendre |
| `document` | Document à produire |
| `bug` | Correction de bug |
| `idea` | Idée à creuser |
| `follow-up` | Suivi à faire |
| `deliverable` | Livrable concret |

---

## 🏷️ LABELS (3 familles)

| Famille | Labels |
|---------|--------|
| **Nature** | `decision`, `execution`, `research`, `document`, `follow-up`, `bug`, `idea` |
| **Domaine** | `legal`, `finance`, `tech`, `photo`, `branding`, `ops`, `travel`, `science` |
| **Contexte** | `urgent`, `bloque-externe`, `en-attente-jch`, `delegue`, `a-planifier`, `quick-win` |
| **Niveau** | `strategique`, `tactique`, `operationnel` |

---

## 🔄 RITUEL QUOTIDIEN

| Moment | Action |
|--------|--------|
| Matin | Checker les cartes `En validation` (à valider) |
| Journée | Déplacer les cartes au fil de l'avancement |
| Soir | `pka-save` pour archiver les décisions du jour |

---

## 👤 QUI FAIT QUOI ?

| Rôle | Responsabilité |
|------|----------------|
| **Dobby** | Crée et pilote les cartes, assigne aux spécialistes |
| **Forge** | Crée des cartes techniques |
| **JCH** | Valide les cartes en statut `En validation` |

---

## ⚡ ASTUCES

- Une carte bloquée → passe en `En attente` + label `bloque-externe`
- Une carte urgente → label `urgent`, Dobby la priorise
- Une carte en attente de toi → statut `En validation` + label `en-attente-jch`
- Tu veux voir que tes tâches à valider → filtre `En validation`

---

*Fiche générée par Dobby 🦉 — 3 juin 2026*
