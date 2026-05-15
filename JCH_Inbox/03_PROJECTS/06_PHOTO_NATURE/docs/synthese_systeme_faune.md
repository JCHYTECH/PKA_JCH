---
tags:
  - type/project
  - status/active
---
# Synthèse – Système de fiches naturalistes (Obsidian + Squarespace)

## Objectif
Mettre en place un système structuré pour :
- documenter des observations naturalistes (macro / téléobjectif)
- organiser une base de données personnelle
- publier facilement sur un site (Squarespace)

---

## 1. Fiche signalétique (web)

Création d’un template HTML/CSS :
- design lisible et structuré
- sections :
  - description
  - habitat
  - répartition
  - classification
  - note naturaliste
- intégration facile dans Squarespace via bloc Code

👉 Version recommandée : HTML statique avec remplacement manuel

---

## 2. Workflow recommandé

Obsidian = base de travail  
Squarespace = publication

Processus :
1. Création fiche dans Obsidian
2. Structuration + enrichissement
3. Export vers site web

---

## 3. Architecture Obsidian

Dossiers :

Faune/
- Fiches
- Taxonomie
- Lieux
- Observations
- Templates

Concepts :
- 1 note = 1 espèce
- liens internes = relations biologiques
- backlinks = navigation automatique

---

## 4. Templates Obsidian

Deux niveaux :

### A. Template simple
- insertion manuelle
- structure standard

### B. Template avancé (Templater)
- prompts utilisateur
- génération automatique
- renommage fichier

---

## 5. Templater – fonctionnement

Plugin à installer :
- Templater (community plugin)

Utilisation correcte :
Cmd + P → Templater: Create new note from template

⚠️ Ne pas utiliser :
Insert Template (plugin différent)

---

## 6. Template automatisé (fonctionnalités)

- saisie guidée :
  - nom scientifique
  - classification
  - lieu
- insertion image automatique
- création liens taxonomiques :
  - classe
  - ordre
  - famille
  - genre
  - espèce
- renommage automatique fichier

---

## 7. Problèmes rencontrés

### Templater parsing error
Cause :
- erreur syntaxe JS
- mélange de syntaxes
- mauvais déclencheur

Solution :
- utiliser bloc <%* ... %>
- générer contenu via tR +=

---

## 8. Bonnes pratiques

- toujours tester avec template minimal
- éviter les champs vides dans le renommage
- importer image avant exécution template
- standardiser les noms

---

## 9. Résultat final

Système obtenu :

- base de données naturaliste personnelle
- organisation scientifique (taxonomie)
- journal d’observation terrain
- pipeline vers publication web

---

## 10. Évolutions possibles

- Dataview (requêtes dynamiques)
- cartographie des observations
- export HTML automatique
- automatisation création taxonomie
- index par comportements animaux

---

## Conclusion

Le système construit permet de passer de simples notes à :

→ un outil naturaliste structuré  
→ une base de connaissances exploitable  
→ un support de publication cohérent
