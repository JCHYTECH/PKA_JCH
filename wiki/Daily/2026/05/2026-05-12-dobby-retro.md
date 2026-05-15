---
date: 2026-05-12
type: retrospective
author: Dobby
tags: [retro, meta]
---

# Rétrospective — 2026-05-12

# Rétrospective Session 2026-05-12 — Ingest PKA

## Ce qui a bien fonctionné

- **Exécution rapide du déplacement d'inbox** : Les fichiers ont été routés vers leurs destinations permanentes sans erreur de syntaxe ou de chemin. Le scan initial était exhaustif.
- **Dialogue correctif réactif** : Quand JCH a signalé `todo-jch.html` mal placé, correction immédiate et sans friction.
- **Documentation des scripts existants** : Explication claire du rôle de `dashboard.sh` et `dobby.sh`, avec justification de leur emplacement à la racine.
- **Absence de destruction/perte de données** : Même face à `file_index` inexistante, pas de création de table erratique — signal transparent du manque.

## Inefficacités détectées

1. **Demande floue initiale** : `"prends les fichiers dans inbox et deplace les dans les directory qui te semble adequat"` → pas de règles de routage explicites fournies d'emblée. Claude a dû *deviner* les destinations logiques (wiki/Knowledge/AI-Tools/). Risque : mauvais classement ou hésitations.

2. **Trois questions séquentielles sur l'architecture existante** : JCH a questonné successivement `todo-jch.html`, puis `dashboard.sh`/`dobby.sh`, puis `team.db`. Ces questions auraient pu être posées *avant* l'ingest, pas après. Délai d'exécution allongé.

3. **État fantôme non exploré proactivement** : Claude a détecté que `file_index` n'existait pas, mais n'a pas :
   - Proposé de créer le schéma attendu *immédiatement*
   - Signalé le risque d'une base vide à la racine (dette technique)
   - Demandé si cette table était censée exister d'après les specs du PKA

4. **Pas de rapport d'exécution complet** : Le tableau du INGEST s'arrête en milieu de ligne (`2026-05-12_AI_` incomplet). Impossible de vérifier que tous les fichiers ont été traités.

5. **Décision en suspens mal documentée** : `"on attends"` sur `team.db` n'est jamais archivée dans une tâche ou un memo. Risque d'oubli à la session suivante.

## Causes racines identifiées

1. **Manque de spécification préalable** : Pas de "routing rules" fourni avant l'ingest. Claude a accepté une tâche sous-spécifiée au lieu de demander les critères.

2. **Architecture PKA partiellement initialisée** : `team.db` existe mais vide. Cela crée des zones grises où Claude doit *deviner* s'il faut initialiser, patienter, ou ignorer.

3. **Communication asynchrone des besoins** : JCH découvre les problèmes d'emplacement pendant la tâche, pas avant. Suggère un manque de review de structure PKA *avant* d'ingester.

4. **Rapport incomplet** : Le tableau du INGEST s'arrête net — probablement troncature d'affichage ou arrêt prématuré. Aucun resumé final du nombre de fichiers traités.

## Règles à mémoriser pour les prochaines sessions

1. **Avant tout ingest : spécifier les règles de routage** → JCH doit fournir un dictionnaire type → destination. Si absent, Claude demande explicitement au lieu d'assumer.

2. **Complément pre-flight check** : Avant de toucher à l'inbox, valider :
   - L'existence et l'intégrité des répertoires cibles
   - L'état des bases indexantes (`file_index`, etc.)
   - L'absence de conflits de noms

3. **Détecter et signaler les états fantômes** : Si `team.db` existe mais vide, proposer immédiatement l'initialisation du schéma. Ne pas laisser pendre.

4. **Rapport exhaustif et complet** : Terminer *toujours* par un résumé :
   ```
   ✅ N fichiers traités
   ✅ N fichiers indexés
   ⚠️  N décisions en suspens (lister)
   ```

5. **Documenter les décisions en suspens** : `"on attends"` → créer une tâche `TODO: Initialiser team.db — spec manquante` et la laisser visible pour la prochaine session.

6. **Valider les répertoires cibles avant déplacement** : Si un chemin est flou (ex. `wiki/Knowledge/AI-Tools/` vs `wiki/AI/Tools/`), confirmer avec JCH plutôt que de choisir.

---

**Verdict** : Session productive mais *à optimiser en amont*. La prochaine ingest gagnera 5–10 min si les règles de routage et l'état de la base sont clarifiés avant de commencer.