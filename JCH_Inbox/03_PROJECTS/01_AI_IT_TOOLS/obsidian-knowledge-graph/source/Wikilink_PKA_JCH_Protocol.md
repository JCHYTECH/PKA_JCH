# PKA_JCH – Protocole de Wikilinking Automatique pour Dobby

## Objectif général

Ce document définit précisément :
- le rôle de Dobby dans la gestion des wikilinks,
- les procédures automatiques à appliquer,
- les contrôles qualité,
- les moments où JC doit intervenir,
- et le workflow permanent lors de la création de nouveaux documents.

Le but est de transformer PKA_JCH en :
- système documentaire relationnel,
- mémoire persistante AI-compatible,
- knowledge graph exploitable,
- base de coordination multi-agents.

---

# 1. OBJECTIFS DU WIKILINKING

Le wikilinking doit permettre :

- la connexion automatique des connaissances,
- la navigation intelligente,
- l’exploitation par les agents AI,
- la création d’un graphe relationnel,
- la réduction de la duplication documentaire,
- la continuité mémoire entre modèles AI.

Le système doit rester :
- lisible par un humain,
- stable,
- gouvernable,
- et réversible.

---

# 2. RÔLE DE DOBBY

Dobby devient :

- coordinateur documentaire,
- superviseur du graphe de connaissances,
- gestionnaire des relations documentaires,
- contrôleur qualité des liens.

Dobby NE DOIT PAS :
- modifier massivement sans validation,
- créer des milliers de liens aveugles,
- créer des liens ambigus,
- casser la lisibilité humaine.

---

# 3. ARCHITECTURE CIBLE

## Structure générale

PKA_JCH/
├── 00_INBOX
├── 01_DASHBOARDS
├── 02_COMPANY
├── 03_PROJECTS
├── 04_AI_SYSTEM
├── 05_REGULATORY
├── 06_BUSINESS
├── 07_PHOTO
├── 08_HARDWARE
├── 09_SOFTWARE
├── 90_TEMPLATES
├── 91_ATTACHMENTS
└── 99_SYSTEM

---

# 4. TYPES DE NOTES À WIKILINKER

## PRIORITÉ 1 — Liens critiques

Toujours wikilinker :

- projets,
- agents,
- sociétés,
- technologies,
- hardware,
- logiciels,
- normes,
- réglementations,
- décisions,
- fournisseurs,
- clients,
- composants.

Exemples :

[[BirdNET]]
[[ESP32]]
[[WildMesh]]
[[Dobby]]
[[Claude]]
[[ChatGPT]]
[[Raspberry Pi 5]]

---

## PRIORITÉ 2 — Relations métiers

- workflows,
- procédures,
- concepts techniques,
- API,
- protocoles.

---

## PRIORITÉ 3 — Relations contextuelles

- discussions connexes,
- projets similaires,
- technologies proches.

Ces liens peuvent être suggérés mais non imposés.

---

# 5. PROCESSUS INITIAL DE WIKILINKING GLOBAL

## ÉTAPE 1 — INVENTAIRE GLOBAL

Dobby doit :

1. Scanner tous les fichiers .md
2. Construire une liste de :
   - titres de notes,
   - aliases,
   - tags,
   - dossiers,
   - concepts fréquents.

Sortie attendue :

99_SYSTEM/indexes/
- note_index.md
- project_index.md
- technology_index.md
- agent_index.md

JC :
- aucune intervention sauf erreur majeure.

---

## ÉTAPE 2 — CRÉATION DU DICTIONNAIRE CENTRAL

Créer :

99_SYSTEM/knowledge_dictionary.md

Contenu :

- nom canonique,
- aliases,
- catégorie,
- dossier source,
- ambiguïtés potentielles.

Exemple :

BirdNET:
- aliases:
  - BirdNET-Go
- category:
  - AI Bioacoustics
- folder:
  - 03_PROJECTS/WildMesh

JC :
- validation unique du dictionnaire principal.

IMPORTANT :
Cette étape est la principale intervention humaine.

---

## ÉTAPE 3 — PREMIER PASSAGE AUTOMATIQUE

Dobby doit :

1. Lire chaque note
2. Détecter concepts connus
3. Vérifier existence note cible
4. Ajouter wikilinks automatiquement

Exemple :

Avant :
BirdNET tourne sur Raspberry Pi.

Après :
[[BirdNET]] tourne sur [[Raspberry Pi 5]].

---

## ÉTAPE 4 — DÉTECTION D’AMBIGUÏTÉ

Si ambiguïté :

NE PAS linker automatiquement.

Créer :

99_SYSTEM/review_queue.md

Format :

- "Apple"
Possible matches:
- Apple Inc
- Apple Fruit

JC :
- validation ponctuelle uniquement.

---

## ÉTAPE 5 — CONTRÔLE QUALITÉ

Dobby doit vérifier :

- liens cassés,
- doublons,
- liens circulaires inutiles,
- liens excessifs,
- lisibilité.

Règles :

- Maximum 1 lien par concept significatif dans un paragraphe.
- Éviter surcharge visuelle.
- Priorité à lisibilité humaine.

---

# 6. GESTION DES NOUVEAUX DOCUMENTS

## RÈGLE FONDAMENTALE

Tout nouveau document DOIT passer par pipeline de normalisation.

---

# 7. PIPELINE NOUVEAU DOCUMENT

## ÉTAPE 1 — DÉTECTION

Quand nouveau fichier apparaît :

Dobby :
- détecte création,
- identifie dossier,
- identifie type.

---

## ÉTAPE 2 — NORMALISATION

Ajouter YAML minimal si absent :

```yaml
type:
status:
dateCreated:
dateModified:
tags:
```

---

## ÉTAPE 3 — EXTRACTION DES ENTITÉS

Dobby extrait :

- projets,
- technologies,
- agents,
- sociétés,
- matériels,
- réglementations,
- concepts.

---

## ÉTAPE 4 — MATCHING

Comparer avec :
knowledge_dictionary.md

Si correspondance :
→ proposer wikilink.

---

## ÉTAPE 5 — INSERTION AUTOMATIQUE

Insertion automatique UNIQUEMENT si :
- confiance élevée,
- ambiguïté faible,
- note cible existante.

Sinon :
→ review_queue.md

---

## ÉTAPE 6 — ENRICHISSEMENT

Ajouter éventuellement :

- tags,
- backlinks,
- relations,
- métadonnées.

---

# 8. RÈGLES DE GOUVERNANCE

## INTERDICTIONS

Dobby NE DOIT PAS :

- créer des liens vers des notes inexistantes,
- créer des milliers de micro-notes,
- renommer sans validation,
- déplacer des notes critiques,
- supprimer du contenu.

---

## AUTORISATIONS

Dobby PEUT :

- ajouter wikilinks,
- ajouter aliases,
- enrichir YAML,
- générer suggestions,
- créer rapports qualité.

---

# 9. INTERVENTIONS DE JC

Le système doit minimiser les interventions humaines.

JC intervient uniquement :

## OBLIGATOIRE

- validation initiale du dictionnaire,
- résolution ambiguïtés importantes,
- validation conventions.

---

## OPTIONNEL

- revue qualité ponctuelle,
- validation restructurations majeures.

---

## INTERDICTION

JC ne doit PAS :
- faire du wikilinking manuel massif,
- maintenir les liens à la main,
- corriger systématiquement les agents.

---

# 10. RÈGLES NOMMAGE

IMPORTANT.

Toujours utiliser :

- noms explicites,
- stabilité,
- cohérence.

Éviter :
- noms vagues,
- acronymes seuls,
- variations multiples.

BON :
[[Raspberry Pi 5]]

MAUVAIS :
[[Pi]]

---

# 11. OBJECTIF FINAL

Créer :

- mémoire relationnelle,
- knowledge graph exploitable,
- système documentaire AI-native,
- continuité inter-modèles,
- plateforme R&D augmentée.

Le wikilinking doit devenir :
- automatique,
- stable,
- contrôlé,
- et invisible pour JC.

---

# 12. ÉVOLUTIONS FUTURES

## PHASE 2

Ajouter :
- embeddings,
- recherche sémantique,
- clustering,
- détection automatique de similarités.

---

## PHASE 3

Ajouter :
- vector database,
- IA locale,
- relation scoring,
- génération automatique de dashboards.

---

## PHASE 4

Dobby orchestre :
- circulation connaissance,
- enrichissement documentaire,
- propagation inter-projets,
- intelligence relationnelle globale.

---

# 13. CONSIGNE FINALE À DOBBY

Le système documentaire doit toujours privilégier :

1. stabilité,
2. lisibilité humaine,
3. gouvernance,
4. cohérence,
5. automatisation prudente,
6. capitalisation long terme.

Le knowledge graph doit être considéré comme :
- infrastructure critique de PKA_JCH,
- mémoire centrale,
- et couche relationnelle commune à tous les agents AI.


---

# 14. GESTION DES FICHIERS NON-MARKDOWN

IMPORTANT :
Le système de wikilinking de PKA_JCH ne doit PAS se limiter aux fichiers `.md`.

Les fichiers suivants doivent également être intégrés au graphe documentaire :

- PDF,
- XLSX,
- CSV,
- PNG,
- JPG,
- SVG,
- ZIP,
- JSON,
- YAML,
- STEP,
- STL,
- scripts,
- modèles AI,
- vidéos,
- fichiers audio,
- datasheets,
- exports logiciels.

---

# 15. PRINCIPE ARCHITECTURAL

Les fichiers non-MD doivent être considérés comme :

- assets techniques,
- données,
- livrables,
- composants projet.

Les fichiers `.md` restent :

- la couche mémoire,
- la couche relationnelle,
- la couche explicative,
- la couche de gouvernance.

Le système doit donc toujours privilégier :

MD = intelligence documentaire  
Autres fichiers = ressources liées

---

# 16. CRÉATION AUTOMATIQUE DE NOTES HUB

Quand un fichier non-MD important est détecté, Dobby doit :

1. identifier le projet associé,
2. rechercher une note hub existante,
3. créer une note hub si nécessaire,
4. intégrer automatiquement les liens vers les assets.

---

## Exemple

Structure :

03_PROJECTS/WildMesh/
├── 00_INDEX.md
├── attachments/
│   ├── schematic.pdf
│   ├── firmware.zip
│   ├── prototype.step
│   └── BOM.xlsx

Le fichier :
00_INDEX.md

doit contenir :

```md
# WildMesh

## Hardware
[[schematic.pdf]]
[[BOM.xlsx]]

## Firmware
[[firmware.zip]]

## 3D
[[prototype.step]]
```

---

# 17. EMBED DES IMAGES ET SCHÉMAS

Dobby doit privilégier les embeds pour :

- schémas,
- PCB,
- photographies,
- graphes,
- renders,
- cartes,
- diagrammes.

Format :

```md
![[schema_v5.png]]
```

Cela améliore :
- la compréhension humaine,
- la navigation,
- la valeur documentaire.

---

# 18. PIPELINE SPÉCIFIQUE NON-MD

Lorsqu’un nouveau fichier non-MD apparaît :

## ÉTAPE 1 — DÉTECTION

Dobby :
- détecte extension,
- identifie projet probable,
- identifie catégorie.

---

## ÉTAPE 2 — CLASSIFICATION

Catégories possibles :

- hardware,
- software,
- regulatory,
- finance,
- media,
- AI models,
- datasets,
- firmware,
- contracts,
- scientific data.

---

## ÉTAPE 3 — RECHERCHE HUB

Dobby cherche :
- note projet,
- note technologie,
- note système,
- note décision.

---

## ÉTAPE 4 — INSERTION AUTOMATIQUE

Dobby ajoute :

```md
[[nom_fichier.pdf]]
```

ou :

```md
![[image.png]]
```

selon type.

---

## ÉTAPE 5 — ENRICHISSEMENT

Dobby peut ajouter :

- description,
- date,
- version,
- provenance,
- relation projet,
- statut.

---

# 19. RÈGLES IMPORTANTES

Dobby NE DOIT PAS :

- créer des milliers de fichiers hub inutiles,
- dupliquer assets,
- déplacer fichiers critiques sans validation,
- renommer versions validées.

---

# 20. OBJECTIF FINAL ÉTENDU

Le graphe PKA_JCH doit intégrer :

- documents,
- assets,
- hardware,
- firmware,
- images,
- datasets,
- décisions,
- workflows,
- modèles AI,
- connaissances.

L’ensemble doit fonctionner comme :

- mémoire relationnelle augmentée,
- cockpit documentaire AI-native,
- infrastructure cognitive partagée entre agents.
