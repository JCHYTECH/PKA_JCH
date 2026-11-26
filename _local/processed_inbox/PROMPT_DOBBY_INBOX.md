# Mandat [[Dobby]] — Surveillance des livrables agents

## Contexte

La table `inbox` de `team.db` ne couvre pas le flux retour des spécialistes vers JCH.
Résultat : impossible de savoir si un livrable a été produit, présenté, validé ou rejeté.

## Ce que tu dois faire

### Étape 1 — Migration `team.db`

Exécute ce script SQL sur `team.db` :

```sql
-- Ajouter colonne type de livrable
ALTER TABLE inbox ADD COLUMN deliverable_path TEXT;
ALTER TABLE inbox ADD COLUMN delivered_at TEXT;
ALTER TABLE inbox ADD COLUMN validated_at TEXT;
ALTER TABLE inbox ADD COLUMN validated_by TEXT DEFAULT 'JCH';
ALTER TABLE inbox ADD COLUMN rejection_reason TEXT;

-- Les nouveaux statuts autorisés sont :
-- pending     → reçu, non traité
-- in_progress → spécialiste en cours
-- delivered   → livrable produit, en attente validation JCH
-- validated   → JCH a approuvé
-- rejected    → JCH a rejeté (rejection_reason obligatoire)
-- cancelled   → abandonné

-- La colonne direction accepte désormais aussi : TEAM→JCH
```

### Étape 2 — Règle opérationnelle [[Dobby]]

À partir de maintenant, chaque fois que tu mandates un spécialiste :

1. **À l'envoi** : créer une entrée `inbox` direction `JCH→TEAM`, statut `in_progress`
2. **À la livraison** : mettre à jour la même entrée — statut `delivered`, `deliverable_path` = chemin du fichier dans `TEAM_Inbox/`
3. **À la validation JCH** : mettre à jour — statut `validated` ou `rejected` + `rejection_reason` si rejeté

### Étape 3 — Rapport de situation

Après la migration, produire un rapport de l'état actuel :

- Nombre d'entrées `pending` en souffrance avec date et spécialiste concerné
- Confirmer que les 6 entrées `pending` existantes sont toujours d'actualité ou à passer en `cancelled`

### Étape 4 — Dashboard

Mettre à jour `01_DASHBOARDS/hub.html` pour afficher :
- Livrables `in_progress` en cours
- Livrables `delivered` en attente de validation JCH
- Livrables `rejected` non retraités

Brief [[Forge]] pour le dashboard si nécessaire.

## Contraintes

- Ne pas supprimer ni modifier les 230 entrées existantes
- Le schéma existant reste intact — additions seulement
- Confirmer la migration à JCH avant de toucher au dashboard
