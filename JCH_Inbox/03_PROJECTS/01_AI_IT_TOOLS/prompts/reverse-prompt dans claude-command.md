# /reverse-prompt

Analyse rétrospectivement l'ensemble de cette conversation et produis le prompt unique qui aurait permis d'obtenir le résultat final directement, sans les allers-retours intermédiaires.

Procède en trois temps :

## 1. DIAGNOSTIC (bref, en prose)

- Quel était l'objectif réel atteint en fin de chat ?
- Quelles informations as-tu dû me demander ou inférer en cours de route ?
- Quels malentendus ou détours ont allongé la conversation ?

## 2. PROMPT RECONSTRUIT (bloc de code)

Structure obligatoire :

- Rôle / expertise attendue
- Contexte utilisateur pertinent (ce que tu aurais dû savoir d'emblée)
- Objectif précis et livrable attendu
- Contraintes techniques (OS, outils, formats, versions)
- Format de sortie exact (fichier, structure, frontmatter, etc.)
- Critères de qualité ou de refus
- Ton et style de réponse

## 3. NOTES D'USAGE (liste courte)

- Variables à adapter selon le projet (ex. `{nom_session}`, `{chemin_vault}`)
- Préférences déjà couvertes par le profil utilisateur — donc à ne PAS dupliquer
- Limites connues du prompt (cas qu'il ne couvre pas)

---

Le prompt reconstruit doit être **autonome** : un assistant qui le reçoit sans contexte préalable doit pouvoir produire le même livrable final en une seule passe.
