# Pack minimal Obsidian — Automatisation du vault et amélioration de la vue graphe
[[obsidian]]

Version : 1.0  
Objectif : mettre en place une structure simple, stable et automatisable pour mieux classer les notes, améliorer la vue graphe, exploiter Graphify et préparer l’usage de Dataview / Templater / Extended Graph.

---

## 1. Principe général

L’objectif n’est pas seulement d’avoir plus de liens entre les notes.  
L’objectif est d’obtenir un graphe lisible, interprétable et utile pour réfléchir à des actions, des stratégies, des projets, des sources et des décisions.

Le système repose sur cinq éléments :

1. Une arborescence claire du vault.
2. Des propriétés YAML standardisées.
3. Quelques tags visuels contrôlés.
4. Des templates de notes.
5. Des règles de couleur et de filtrage pour la vue graphe.

Graphify est conservé comme moteur d’enrichissement relationnel, mais il ne doit pas remplacer votre structure personnelle.

---

## 2. Arborescence recommandée du vault

Créer les dossiers suivants dans Obsidian :

```text
00-INBOX/
01-PROJETS/
02-DOMAINES/
03-RESSOURCES/
04-ACTIONS/
05-REFERENCES/
06-GRAPHIFY/
90-ARCHIVES/
99-TEMPLATES/
```

### Rôle des dossiers

| Dossier | Rôle |
|---|---|
| `00-INBOX` | Notes brutes, idées rapides, éléments non encore classés |
| `01-PROJETS` | Projets actifs ou structurés |
| `02-DOMAINES` | Domaines permanents de réflexion |
| `03-RESSOURCES` | Articles, livres, vidéos, documents, sources externes |
| `04-ACTIONS` | Actions à faire, checklists, plans opérationnels |
| `05-REFERENCES` | Fiches stables : espèces, personnes, sociétés, lieux, outils |
| `06-GRAPHIFY` | Notes générées ou enrichies par Graphify |
| `90-ARCHIVES` | Notes anciennes ou terminées |
| `99-TEMPLATES` | Modèles de notes |

---

## 3. Propriétés YAML minimales

Chaque note importante devrait contenir un bloc YAML au début.

```yaml
---
type:
status:
domain:
graph_group:
graph_role:
created:
updated:
---
```

Version minimale acceptable :

```yaml
---
type:
status:
domain:
graph_group:
---
```

---

## 4. Vocabulaire contrôlé

### 4.1 Types de notes

Utiliser de préférence une valeur parmi celles-ci :

```text
note
projet
action
source
concept
personne
outil
espece
lieu
decision
question
graphify
```

### 4.2 Statuts

```text
inbox
actif
a_traiter
en_cours
decision
archive
```

### 4.3 Domaines

Adapter progressivement, mais éviter de créer trop de variantes.

```text
photo
macro
wildlife
printing
business
diatech
obsidian
ia
zoologie
juridique
maison
moto
```

### 4.4 Rôle graphique

```text
hub
source
action
question
decision
archive
```

---

## 5. Tags visuels recommandés

Les tags suivants peuvent être utilisés dans le corps des notes pour faciliter la coloration dans la vue graphe native d’Obsidian :

```text
#hub
#action
#decision
#question
#source
#graphify
#archive
#photo
#macro
#printing
#strategie
```

Conseil : garder les tags importants visibles dans le corps de la note, par exemple :

```markdown
## Tags visuels
#action #obsidian
```

---

## 6. Règles de couleur pour la vue graphe native

Dans la vue graphe d’Obsidian, ouvrir les réglages du graphe puis aller dans `Groups`.

Créer les groupes suivants :

```text
path:"01-PROJETS"
path:"02-DOMAINES"
path:"03-RESSOURCES"
path:"04-ACTIONS"
path:"05-REFERENCES"
path:"06-GRAPHIFY"
path:"90-ARCHIVES"
```

### Couleurs proposées

| Groupe | Couleur recommandée | Sens |
|---|---|---|
| `01-PROJETS` | Bleu | Projets actifs |
| `02-DOMAINES` | Violet | Domaines de connaissance |
| `03-RESSOURCES` | Gris clair | Sources documentaires |
| `04-ACTIONS` | Orange | Actions à faire |
| `05-REFERENCES` | Vert | Fiches stables |
| `06-GRAPHIFY` | Cyan | Notes générées ou enrichies |
| `90-ARCHIVES` | Gris foncé | Notes archivées |

---

## 7. Règles de filtrage utiles dans le graphe

### Afficher uniquement les projets

```text
path:"01-PROJETS"
```

### Afficher uniquement les actions

```text
path:"04-ACTIONS"
```

### Masquer les notes Graphify

```text
-path:"06-GRAPHIFY"
```

### Afficher uniquement les notes Graphify

```text
path:"06-GRAPHIFY"
```

### Afficher les hubs

```text
tag:#hub
```

### Afficher les actions

```text
tag:#action
```

### Afficher les décisions

```text
tag:#decision
```

---

## 8. Convention de nommage

Utiliser une convention lisible, même sans automatisation.

```text
PROJ - Nom du projet.md
ACT - Nom de l’action.md
SRC - Nom de la source.md
DEC - Nom de la décision.md
CONCEPT - Nom du concept.md
ESPECE - Nom scientifique.md
OUTIL - Nom de l’outil.md
HUB - Nom du domaine.md
GRAPHIFY - Sujet analysé.md
```

Exemples :

```text
PROJ - Amélioration du vault Obsidian.md
ACT - Configurer les couleurs de la vue graphe.md
SRC - Article sur Graphify.md
DEC - Utiliser Extended Graph pour les liens typés.md
CONCEPT - Graphe de connaissance personnel.md
HUB - Photographie animalière.md
HUB - Impression photo.md
HUB - IA et automatisation.md
```

---

## 9. Notes hubs recommandées

Créer quelques notes centrales qui serviront de points d’ancrage dans le graphe.

```text
HUB - Photographie animalière
HUB - Macro photographie
HUB - Impression photo
HUB - DIATECH
HUB - Obsidian et PKM
HUB - IA et automatisation
HUB - Zoologie
HUB - Stratégie entrepreneuriale
HUB - Maison off-grid
```

Chaque note importante devrait pointer vers au moins un hub.

Exemple :

```markdown
## Liens principaux
- [[HUB - Obsidian et PKM]]
- [[HUB - IA et automatisation]]
```

---

## 10. Template — Projet

À sauvegarder dans :

```text
99-TEMPLATES/Template - Projet.md
```

```markdown
---
type: projet
status: actif
domain:
subdomain:
priority: moyenne
graph_group:
graph_role: hub
created: {{date}}
updated: {{date}}
---

# {{title}}

## Résumé

## Objectif

## Contexte

## Hypothèses

## Décisions

## Actions liées

## Sources liées

## Concepts liés

## Relations

Domaines :
- 

Sources :
- 

Actions :
- 

Décisions :
- 

## Tags visuels
#projet #hub
```

---

## 11. Template — Action

À sauvegarder dans :

```text
99-TEMPLATES/Template - Action.md
```

```markdown
---
type: action
status: a_traiter
domain:
priority: moyenne
graph_group:
graph_role: action
created: {{date}}
updated: {{date}}
---

# {{title}}

## Action à réaliser

## Contexte

## Projet lié

## Décision associée

## Prochaine étape

## Échéance

## Relations

Projet :
- 

Sources :
- 

Décisions :
- 

## Tags visuels
#action
```

---

## 12. Template — Source

À sauvegarder dans :

```text
99-TEMPLATES/Template - Source.md
```

```markdown
---
type: source
status: actif
domain:
source_type:
author:
url:
graph_group:
graph_role: source
created: {{date}}
updated: {{date}}
---

# {{title}}

## Résumé

## Idées utiles

## Points techniques

## Citations ou éléments importants

## Utilité pour mes projets

## Notes liées

## Relations

Domaines :
- 

Projets :
- 

Concepts :
- 

## Tags visuels
#source
```

---

## 13. Template — Décision

À sauvegarder dans :

```text
99-TEMPLATES/Template - Decision.md
```

```markdown
---
type: decision
status: decision
domain:
graph_group:
graph_role: decision
created: {{date}}
updated: {{date}}
---

# {{title}}

## Décision

## Pourquoi cette décision ?

## Alternatives considérées

## Conséquences

## Actions déclenchées

## Sources utilisées

## Relations

Projet :
- 

Actions :
- 

Sources :
- 

## Tags visuels
#decision
```

---

## 14. Template — Concept

À sauvegarder dans :

```text
99-TEMPLATES/Template - Concept.md
```

```markdown
---
type: concept
status: actif
domain:
graph_group:
graph_role: hub
created: {{date}}
updated: {{date}}
---

# {{title}}

## Définition

## Pourquoi c’est important

## Exemples

## Applications

## Notes liées

## Sources

## Tags visuels
#concept
```

---

## 15. Template — Graphify

À sauvegarder dans :

```text
99-TEMPLATES/Template - Graphify.md
```

```markdown
---
type: graphify
status: actif
domain:
generated_by: graphify
graph_group:
graph_role: source
created: {{date}}
updated: {{date}}
---

# {{title}}

## Résumé Graphify

## Relations détectées

## Concepts importants

## Notes à vérifier manuellement

## Liens suggérés

## Actions possibles

## Tags visuels
#graphify
```

---

## 16. Dashboard Dataview minimal

Créer une note :

```text
Dashboard - Qualité du vault.md
```

Contenu :

```markdown
# Dashboard - Qualité du vault

## Notes à traiter

```dataview
TABLE type, status, domain, graph_group
FROM ""
WHERE status = "a_traiter" OR status = "inbox"
SORT file.mtime DESC
```

## Actions ouvertes

```dataview
TABLE domain, priority, file.mtime
FROM "04-ACTIONS"
WHERE type = "action" AND status != "archive"
SORT priority DESC
```

## Projets actifs

```dataview
TABLE domain, status, graph_group
FROM "01-PROJETS"
WHERE type = "projet" AND status = "actif"
SORT domain ASC
```

## Notes Graphify

```dataview
TABLE domain, graph_group, file.mtime
FROM "06-GRAPHIFY"
WHERE type = "graphify"
SORT file.mtime DESC
```

## Notes sans domaine

```dataview
TABLE type, status, file.folder
FROM ""
WHERE !domain
SORT file.mtime DESC
```
```

---

## 17. Workflow quotidien recommandé

### Nouvelle note

1. Créer la note dans `00-INBOX`.
2. Appliquer un template.
3. Remplir `type`, `status`, `domain`, `graph_group`.
4. Ajouter au moins un lien vers un hub.
5. Ajouter un tag visuel si nécessaire.

### Traitement d’une note

1. Déplacer la note dans le bon dossier.
2. Vérifier le YAML.
3. Ajouter les liens principaux.
4. Identifier si la note est une source, une action, une décision ou un concept.
5. Laisser Graphify enrichir les relations si utile.

### Consultation du graphe

1. Commencer par le graphe global.
2. Filtrer par dossier.
3. Filtrer par tag.
4. Masquer Graphify si le graphe devient trop dense.
5. Utiliser les hubs pour comprendre les grands clusters.

---

## 18. Workflow Graphify recommandé

Graphify doit rester dans son propre espace :

```text
06-GRAPHIFY/
  graphify-notes/
  graphify-reports/
  graphify-maps/
  graphify-imports/
```

Chaque note générée ou enrichie par Graphify doit contenir :

```yaml
---
type: graphify
generated_by: graphify
status: actif
domain:
graph_group:
---
```

Règle importante :

> Graphify enrichit le réseau, mais les notes humaines restent les notes de référence.

---

## 19. Prompt IA de classification automatique

À utiliser avec ChatGPT ou un assistant IA pour classer une note brute.

```text
Tu es mon assistant d’organisation Obsidian.

Analyse la note ci-dessous et propose :
1. Le type de note parmi : note, projet, action, source, concept, personne, outil, espece, lieu, decision, question, graphify.
2. Le statut parmi : inbox, actif, a_traiter, en_cours, decision, archive.
3. Le domaine parmi : photo, macro, wildlife, printing, business, diatech, obsidian, ia, zoologie, juridique, maison, moto.
4. Le graph_group recommandé.
5. Le graph_role parmi : hub, source, action, question, decision, archive.
6. Les tags visuels recommandés.
7. Le dossier cible.
8. Les liens internes à créer ou suggérer.
9. Une version restructurée de la note au format Markdown avec YAML complet.

Contraintes :
- Ne crée pas trop de tags.
- Utilise uniquement le vocabulaire contrôlé.
- Si une information manque, laisse le champ vide plutôt que d’inventer.
- Propose au moins un lien vers une note HUB si c’est pertinent.

Voici la note à analyser :

[COLLER LA NOTE ICI]
```

---

## 20. Ordre d’installation recommandé

1. Créer les dossiers.
2. Créer les templates.
3. Installer ou activer Templater.
4. Installer ou activer Dataview.
5. Configurer les groupes de couleur dans la vue graphe native.
6. Tester sur 10 notes seulement.
7. Ajuster les valeurs de `domain` et `graph_group`.
8. Intégrer progressivement Graphify.
9. Tester Extended Graph si la vue native devient insuffisante.

---

## 21. Règle d’or

Ne pas chercher à tout automatiser immédiatement.

La bonne progression est :

```text
Standardiser → Visualiser → Contrôler → Enrichir → Automatiser en masse
```

Un vault Obsidian devient puissant quand il reste compréhensible par son propriétaire.  
L’automatisation doit servir la lisibilité, pas produire du bruit.

---
