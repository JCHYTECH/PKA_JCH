---
name: capture
description: Transformer n'importe quel input (mail, note, idée, extrait) en entrée knowledge formatée dans team.db. Version PKA améliorée (shadow du skill fondation).
---

# /capture — Capture de connaissance

Transforme un input brut en entrée structurée dans la base de connaissance PKA.

> **Version PKA** — cross-ref avec `ingest` pour éviter la confusion.

## Usage

```
/capture <texte libre>
/capture "L'API Gmail rend la TVA exigible à l'encaissement, même sans facture"
/capture <fichier>   # lire et capturer le contenu d'un fichier
```

## Étapes d'exécution

### 1. Analyser l'input

Identifier :
- **Type** : `fact` / `insight` / `concept` / `quote` / `framework` / `decision` / `reference`
- **Domaine** : `legal` / `finance` / `photo` / `AI` / `veterinaire` / `iot` / `travel` / `business` / `personal`
- **Projet lié** : 03_WILDNEXUS / 02_ARTEON / 08_VETALYX / 06_PHOTO_NATURE / etc.
- **Source** : conversation / document / web / JCH

### 2. Formuler l'entrée

Reformuler en une phrase atomique, claire, réutilisable — sans contexte implicite.

Exemples :
- ❌ "Comme on en a parlé, la TVA s'applique à l'avance"
- ✅ "En droit belge, une avance de trésorerie encaissée par un assujetti TVA rend la taxe exigible immédiatement à la date d'encaissement."

### 3. Insérer dans team.db

```sql
INSERT INTO knowledge (type, domain, project, content, source, created_by, created_at)
VALUES ('<type>', '<domain>', '<projet>', '<contenu_reformulé>', '<source>', 'Corbeau', '<today>');
```

### 4. Confirmer

```
CAPTURE ✓
Type    : fact
Domaine : legal
Projet  : 08_VETALYX
Contenu : En droit belge, une avance de trésorerie...
ID      : 42
```

## Règles

- Une capture = une idée atomique. Si l'input contient plusieurs idées → créer plusieurs entrées.
- Ne jamais paraphraser de façon à changer le sens
- Corbeau est le seul à écrire dans `knowledge` — /capture passe par lui
- Si le schéma `knowledge` n'a pas les colonnes attendues → signaler à Castor

## Skills liés

- **`ingest`** — Pour router un fichier complet vers son dossier projet et l'indexer dans `file_index`. Utiliser `ingest` d'abord pour déplacer le fichier, puis `capture` pour en extraire les connaissances.
