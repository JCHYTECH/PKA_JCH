# PKA_DECOUVERTES — Cahier des charges V2

Date de création : 2026-06-02 21:03  
Projet : Agent spécialisé pour transformer le groupe Telegram **DECOUVERTES** en base de lieux touristiques exploitables dans **PKA_JCH** et Obsidian.

---

# 1. Objectif général

Le groupe Telegram **DECOUVERTES** sert à collecter rapidement des idées de lieux à visiter.

Les membres du groupe peuvent envoyer librement :

- textes
- photos
- screenshots
- liens Internet
- coordonnées GPS
- commentaires courts
- idées spontanées

L'objectif du projet est de transformer automatiquement ces contenus bruts en fiches structurées de lieux touristiques, utilisables pour préparer des sorties, voyages, circuits photo ou itinéraires en van.

Le système ne doit pas demander aux utilisateurs de structurer leurs messages. Le groupe Telegram reste un outil simple et naturel.

---

# 2. Principe général

Pipeline cible :

```text
GROUPE TELEGRAM DECOUVERTES
        |
        v
BOT TELEGRAM COLLECTEUR
        |
        v
DOSSIER BRUT / FILE D'ATTENTE
        |
        v
AGENT PKA_DECOUVERTES
        |
        +--> Analyse texte
        +--> Analyse image / screenshot
        +--> Analyse lien web
        +--> Reconnaissance lieu probable
        |
        v
AGENT VERIFICATION
        |
        v
FICHE OBSIDIAN NORMALISEE
        |
        v
TABLEAU DE BORD LIEUX A VISITER
```

---

# 3. Rôle du bot Telegram

Le bot Telegram ne doit pas être l'intelligence principale du système.

Son rôle doit rester limité à la collecte :

- recevoir les messages du groupe DECOUVERTES
- identifier l'auteur
- conserver la date et l'heure
- extraire le texte
- récupérer les liens
- télécharger les images
- télécharger les documents éventuels
- sauvegarder les métadonnées
- transmettre le tout à l'agent spécialisé

Le bot doit fonctionner comme une passerelle fiable entre Telegram et le système PKA_JCH.

---

# 4. Arborescence recommandée dans PKA_JCH

Arborescence proposée :

```text
PKA_JCH/
│
└── JCH_Inbox/
    │
    └── 00_INBOX/
        │
        └── DECOUVERTES_Telegram/
            │
            ├── 00_raw/
            │   ├── text/
            │   ├── images/
            │   ├── links/
            │   └── metadata/
            │
            ├── 01_queue/
            │
            ├── 02_processing/
            │
            ├── 03_needs_review/
            │
            ├── 04_validated_places/
            │
            ├── 05_rejected/
            │
            └── 99_logs/
```

---

# 5. Agents impliqués

## 5.1 [[Dobby]] — Coordinateur général

[[Dobby]] reste le coordinateur du système PKA_JCH.

Responsabilités :

- surveiller que le pipeline fonctionne
- assigner les tâches aux agents spécialisés
- demander une validation humaine seulement si nécessaire
- maintenir la cohérence avec le vault Obsidian
- éviter les doublons
- générer des rapports périodiques

---

## 5.2 Agent PKA_DECOUVERTES

Agent central du projet.

Responsabilités :

- recevoir les contenus collectés
- analyser texte, image et lien
- proposer une identification du lieu
- créer une fiche structurée
- attribuer un score de confiance
- décider si la fiche peut être validée ou doit être revue

---

## 5.3 Agent Vision / Screenshot

Agent spécialisé dans les images.

Responsabilités :

- lire les screenshots
- extraire le texte visible
- identifier les noms de lieux
- reconnaître une interface Google Maps, Instagram, Facebook, blog, site touristique
- identifier les panneaux, cartes, noms de villes, paysages ou monuments
- proposer une hypothèse de localisation

---

## 5.4 Agent Web / Vérification

Agent chargé de confirmer les informations.

Responsabilités :

- rechercher le lieu sur Internet
- trouver le site officiel
- confirmer l'adresse
- confirmer les coordonnées GPS
- confirmer les horaires
- vérifier les prix
- vérifier le parking
- vérifier l'accès van ou camping-car
- signaler les incertitudes

---

## 5.5 Agent Obsidian / Markdown

Agent chargé de produire les fiches finales.

Responsabilités :

- créer une note Markdown normalisée
- ajouter le YAML
- ajouter les wikilinks
- classer la fiche dans le bon dossier
- mettre à jour les tableaux de bord Dataview

---

# 6. Structure JSON d'échange entre agents

Chaque élément Telegram doit être transformé en objet JSON standard.

Exemple :

```json
{
  "telegram_message_id": "123456",
  "telegram_group": "DECOUVERTES",
  "author": "JC",
  "datetime": "2026-06-02T18:45:00+02:00",
  "content_type": "image_with_caption",
  "text": "À voir lors du prochain voyage en van",
  "links": [],
  "media_files": [
    {
      "file_path": "00_raw/images/2026-06-02_1845_123456.jpg",
      "media_type": "screenshot"
    }
  ],
  "analysis_status": "pending",
  "place_candidates": [],
  "confidence": null
}
```

---

# 7. Fiche lieu Obsidian — Modèle standard

Chaque lieu validé doit devenir une fiche Markdown.

Exemple YAML :

```yaml
---
type: lieu_a_visiter
status: a_verifier
source: telegram
source_group: DECOUVERTES
date_capture:
pays:
region:
ville:
nom_lieu:
gps:
van_friendly: incertain
parking: incertain
is_overnight: false
interet_photo: 0
interet_nature: 0
interet_patrimoine: 0
interet_van: 0
priorite: 3
saison_recommandee:
temps_visite:
score_confiance: 0
tags:
  - decouvertes
  - lieu_a_visiter
---
```

Structure de la note :

```md
# Nom du lieu

## Résumé

## Pourquoi visiter

## Intérêt touristique

## Intérêt photo

## Accès voiture / van

## Informations pratiques

## Source Telegram

## Vérification web

## Score de confiance

## Décision

## Tâches restantes
```

---

# 8. Système de scoring touristique

Chaque lieu reçoit plusieurs scores de 0 à 5.

| Critère | Description |
|---|---|
| Intérêt photo | Potentiel photographique |
| Intérêt nature | Paysage, faune, flore, randonnée |
| Intérêt patrimoine | Monument, village, architecture, histoire |
| Intérêt van | Parking, accès, possibilité de dormir à proximité |
| Facilité d'accès | Distance, route, parking |
| Fiabilité information | Niveau de vérification |
| Priorité globale | Synthèse finale |

Exemple :

```yaml
interet_photo: 5
interet_nature: 4
interet_patrimoine: 2
interet_van: 4
fiabilite: 3
priorite: 4
```

---

# 9. Gestion des statuts

Statuts recommandés :

```text
raw
analysed
needs_review
verified
validated
visited
rejected
duplicate
```

Définition :

- `raw` : élément collecté, non analysé
- `analysed` : première analyse terminée
- `needs_review` : intervention humaine nécessaire
- `verified` : informations vérifiées sur Internet
- `validated` : fiche utilisable
- `visited` : lieu déjà visité
- `rejected` : lieu non retenu
- `duplicate` : doublon identifié

---

# 10. Détection des doublons

L'agent doit comparer chaque nouveau lieu avec la base existante.

Critères de détection :

- nom identique ou proche
- coordonnées GPS proches
- même URL
- même ville + même type de lieu
- même image déjà envoyée
- même lieu capturé via plusieurs screenshots

Décision :

- si doublon certain : fusionner
- si doublon probable : envoyer en `needs_review`
- si lieu nouveau : créer fiche

---

# 11. Modèles IA à utiliser

## 11.1 Répartition recommandée

Le MacBook M1 32 Go peut être utilisé pour les tâches locales suivantes :

- tri de messages
- résumé court
- extraction de champs simples
- classification
- OCR basique
- première lecture d'images
- génération de brouillons de fiches
- détection de doublons simples

Les tâches suivantes sont mieux confiées à un modèle cloud :

- reconnaissance difficile de lieux à partir de screenshots ambigus
- recherche web
- vérification de sources
- raisonnement complexe
- comparaison multi-sources
- génération finale de fiches critiques
- liens avec horaires et tarifs récents

---

# 12. Modèles locaux adaptés au MacBook M1 32 Go

## 12.1 Modèles texte

### Mistral 7B / Mistral Small

Usage recommandé :

- extraction d'informations
- résumé
- classification
- génération Markdown
- scoring simple

Avantages :

- rapide
- léger
- utilisable en local
- bon pour les workflows automatisés

Limites :

- pas multimodal
- connaissance non à jour
- ne vérifie pas Internet seul

---

### Llama 3.1 / 3.2 8B

Usage recommandé :

- raisonnement texte
- classification
- création de fiches
- nettoyage de notes
- extraction YAML

Avantages :

- bon équilibre qualité/vitesse
- compatible Ollama
- adapté à un Mac 32 Go en quantification 4-bit ou 5-bit

Limites :

- pas suffisant pour reconnaissance visuelle spécialisée sans modèle vision séparé

---

### Qwen 2.5 / Qwen 3 7B ou 14B

Usage recommandé :

- extraction structurée
- JSON
- classification
- raisonnement technique
- génération de fiches propres

Avantages :

- bon en structuration
- bon en extraction
- intéressant pour les agents

Limites :

- la version 14B peut être plus lente sur M1
- privilégier 7B si le système doit rester fluide

---

# 13. Modèles locaux multimodaux

## 13.1 Qwen2.5-VL 7B

Usage recommandé :

- lecture de screenshots
- compréhension de documents visuels
- extraction d'informations depuis images
- première reconnaissance de lieux

Qwen2.5-VL est particulièrement intéressant pour documents, diagrammes et compréhension visuelle structurée.

Recommandation :

- modèle local principal pour les screenshots
- utiliser en première passe
- envoyer vers Claude/GPT/Gemini si confiance faible

---

## 13.2 Llama 3.2 Vision 11B

Usage recommandé :

- description d'image
- questions/réponses sur image
- captioning
- reconnaissance visuelle générale

Recommandation :

- bon candidat local si la vitesse reste acceptable
- plus lourd que les petits modèles texte
- à tester sur M1 32 Go avant usage permanent

---

## 13.3 Gemma 3 multimodal

Usage recommandé :

- analyse image + texte
- résumé
- extraction
- tâches multilingues

Gemma 3 est annoncé comme multimodal, avec traitement texte et image, et existe en tailles 4B, 12B et 27B.

Recommandation :

- tester Gemma 3 4B et 12B
- éviter 27B pour le M1 si l'objectif est l'automatisation fluide

---

# 14. Recommandation pratique pour votre MacBook M1 32 Go

## Configuration locale conseillée

Utiliser **Ollama** comme serveur local de modèles.

Modèles à tester en priorité :

```bash
ollama pull qwen2.5vl:7b
ollama pull llama3.2-vision:11b
ollama pull gemma3:12b
ollama pull qwen2.5:7b
ollama pull llama3.1:8b
```

Choix recommandé par rôle :

| Rôle | Modèle local conseillé |
|---|---|
| Classification texte | qwen2.5:7b ou llama3.1:8b |
| Génération Markdown | qwen2.5:7b |
| Analyse screenshot | qwen2.5vl:7b |
| Description image | llama3.2-vision:11b |
| Agent rapide de tri | mistral:7b |
| Vérification critique | Claude / GPT / Gemini cloud |

---

# 15. Architecture hybride recommandée

Le meilleur choix est une architecture hybride :

```text
LOCAL MACBOOK M1
- réception fichiers
- pré-tri
- OCR simple
- première analyse image
- extraction JSON
- brouillon Markdown

CLOUD LLM
- recherche web
- validation multi-sources
- reconnaissance difficile
- synthèse finale
- arbitrage en cas d'incertitude
```

Cette architecture évite de surcharger le MacBook tout en gardant une forte autonomie locale.

---

# 16. Règles de décision local/cloud

Utiliser le local si :

- le texte est clair
- le lieu est explicitement nommé
- l'image contient un nom lisible
- le lien est simple
- la fiche peut être créée comme brouillon

Utiliser le cloud si :

- le lieu est ambigu
- l'image est un screenshot sans nom évident
- le lieu doit être reconnu visuellement
- les horaires ou tarifs doivent être confirmés
- la décision a un impact sur un itinéraire réel
- il faut comparer plusieurs sources

---

# 17. Prompts de base pour les agents

## 17.1 Prompt Agent Texte

```text
Tu es l'agent PKA_DECOUVERTES. Analyse ce message Telegram.
Extrais tous les indices permettant d'identifier un lieu touristique.
Retourne uniquement un JSON structuré avec :
nom_lieu, pays, region, ville, type_lieu, interet_touristique,
interet_photo, van_friendly, informations_manquantes,
score_confiance, action_recommandee.
```

---

## 17.2 Prompt Agent Vision

```text
Tu es l'agent Vision de PKA_DECOUVERTES.
Analyse cette image ou ce screenshot.
Identifie tout texte visible, nom de lieu, carte, panneau, monument,
coordonnée, logo d'application ou indice géographique.
Propose jusqu'à 3 lieux candidats avec score de confiance.
Retourne uniquement un JSON.
```

---

## 17.3 Prompt Agent Vérification Web

```text
Tu es l'agent Vérification de PKA_DECOUVERTES.
À partir du lieu candidat, vérifie les informations en ligne.
Priorise les sources officielles.
Confirme : nom exact, adresse, GPS, horaires, prix, parking,
accès van, restrictions, site officiel.
Retourne les sources et un score de fiabilité.
```

---

## 17.4 Prompt Agent Obsidian

```text
Tu es l'agent Obsidian de PKA_JCH.
Transforme ce JSON vérifié en fiche Markdown conforme au modèle
PKA_DECOUVERTES.
Ajoute YAML, résumé, intérêt touristique, intérêt photo, accès van,
sources, score de confiance et tâches restantes.
```

---

# 18. Tableau de bord Obsidian

Créer une note :

```text
PKA_JCH/01_DASHBOARDS/Dashboard_DECOUVERTES.md
```

Contenu Dataview possible :

```dataview
TABLE pays, region, ville, van_friendly, interet_photo, priorite, status
FROM "JCH_Inbox/00_INBOX/DECOUVERTES_Telegram/04_validated_places"
WHERE type = "lieu_a_visiter"
SORT priorite DESC
```

---

# 19. Étapes de mise en œuvre

## Étape 1 — Stabiliser Telegram

- confirmer que le bot est dans le groupe DECOUVERTES
- vérifier qu'il reçoit les messages
- vérifier qu'il peut télécharger les images
- sauvegarder les messages bruts

Validation JC :

- envoyer un texte simple
- envoyer un lien
- envoyer un screenshot
- vérifier que les trois sont sauvegardés

---

## Étape 2 — Créer le format JSON standard

- créer le schéma JSON
- traiter les messages en file d'attente
- stocker un fichier `.json` par message

Validation JC :

- ouvrir 2 ou 3 JSON
- vérifier que les champs sont compréhensibles

---

## Étape 3 — Installer les modèles locaux

Sur le MacBook M1 32 Go :

- installer Ollama
- installer 2 modèles texte
- installer 1 modèle vision
- tester temps de réponse et qualité

Validation JC :

- choisir le modèle local par défaut

---

## Étape 4 — Analyse texte automatique

- messages texte vers JSON enrichi
- extraction lieu/type/intérêt
- création d'un brouillon Markdown

Validation JC :

- vérifier 5 fiches générées

---

## Étape 5 — Analyse image / screenshot

- envoyer image à modèle vision local
- extraire texte et indices
- générer candidats de lieux
- basculer vers cloud si confiance faible

Validation JC :

- tester sur 10 screenshots réels

---

## Étape 6 — Analyse liens

- ouvrir la page
- extraire titre, contenu, adresse, résumé
- vérifier source officielle si possible
- créer fiche

Validation JC :

- vérifier 5 liens réels

---

## Étape 7 — Vérification web

- confirmer adresse, GPS, horaires, parking
- ajouter sources
- passer statut `verified`

Validation JC :

- contrôle ponctuel uniquement

---

## Étape 8 — Intégration Obsidian

- créer fiches Markdown
- ajouter YAML
- ajouter wikilinks
- alimenter Dashboard_DECOUVERTES

Validation JC :

- ouvrir Obsidian en Reading View
- vérifier le tableau de bord

---

# 20. Points où JC doit intervenir

Interventions minimales souhaitées :

1. Validation du dossier d'installation
2. Validation de 5 fiches de test
3. Choix du modèle local par défaut
4. Validation du format de fiche
5. Décision en cas de lieu ambigu
6. Validation finale du pipeline

Tout le reste doit être automatisé par [[Dobby]] et les agents spécialisés.

---

# 21. Risques et limites

## 21.1 Reconnaissance des screenshots

Un screenshot d'un lieu sans nom visible peut être difficile à identifier.

Solution :

- extraire tous les indices
- proposer plusieurs candidats
- demander validation humaine si nécessaire

---

## 21.2 Informations touristiques périmées

Horaires, tarifs et accès changent.

Solution :

- toujours ajouter date de vérification
- prioriser sources officielles
- garder un statut `a_verifier` si doute

---

## 21.3 Limites du MacBook M1

Le M1 32 Go est utilisable mais ne doit pas être considéré comme un serveur lourd permanent.

Solution :

- tâches simples en local
- tâches critiques ou lourdes en cloud
- file d'attente pour éviter la surcharge

---

## 21.4 Vie privée

Telegram peut contenir des messages personnels.

Solution :

- ne traiter que le groupe DECOUVERTES
- conserver les sources localement
- éviter de publier automatiquement des données privées
- anonymiser si export externe

---

# 22. Choix technique recommandé

## Stack initiale

- Telegram Bot API
- Python
- Ollama
- Qwen2.5 7B
- Qwen2.5-VL 7B
- Claude ou GPT pour vérification complexe
- Obsidian
- Markdown
- Dataview

## Base de données optionnelle

Pour commencer, les fichiers JSON + Markdown suffisent.

Plus tard :

- SQLite pour index local
- table `places`
- table `telegram_sources`
- table `web_sources`
- table `visits`

---

# 23. MVP recommandé

Le MVP doit rester simple.

Fonctions minimales :

1. Le bot reçoit un message Telegram
2. Le message est sauvegardé
3. L'agent extrait un lieu candidat
4. Une fiche Markdown brouillon est créée
5. JC valide ou rejette

Ne pas commencer par :

- carte interactive
- circuits automatiques
- scoring complexe
- automatisation totale

Ces fonctions viendront après validation du pipeline de base.

---

# 24. Conclusion

Le projet **PKA_DECOUVERTES** est réaliste et cohérent avec le système PKA_JCH.

Le MacBook M1 32 Go peut jouer un rôle utile comme nœud local d'analyse, notamment pour :

- tri
- extraction
- classification
- génération de fiches
- première analyse de screenshots

Cependant, l'architecture la plus robuste est hybride :

- local pour autonomie et confidentialité
- cloud pour reconnaissance difficile, web et validation critique

Le bon démarrage consiste à construire un MVP simple autour de Telegram, JSON, Ollama et Markdown, puis à renforcer progressivement l'analyse multimodale et la vérification web.
