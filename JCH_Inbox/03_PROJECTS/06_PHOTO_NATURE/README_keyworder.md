# PHOTO_NATURE — Photo Keyworder

> Auto-tagging de photos nature par vision model local.
> 100% autonome — pas d'API Google, pas de cloud.

## Fonctionnement

```
Photo (JPEG/PNG/TIFF)
  → encodée base64
  → envoyée à Ollama (gemma4 local M5 ou llama3.2-vision:11b M1)
  → le modèle identifie : sujet, comportement, saison, lumière, compo, habitat
  → keywords écrits en IPTC + XMP + HierarchicalSubject
  → Lightroom les lit automatiquement
```

## Usage

```bash
# Preview (dry-run) sur un dossier
python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/ --dry-run

# Taguer pour de vrai (écrit les métadonnées)
python3 scripts/photo_keyworder.py --input ~/Desktop/Photos/

# Utiliser le M1 (modèle vision plus précis)
python3 scripts/photo_keyworder.py --input ~/Photos/ --m1

# Mode verbeux
python3 scripts/photo_keyworder.py --input ~/Photos/ --verbose
```

## Reprise sur échec (2026-10-22)

Le traitement est désormais **robuste** :

```bash
# 3 tentatives par image (backoff 1s → 2s), configurable
python3 scripts/photo_keyworder.py --input ~/Photos/ --retries 3

# Reprendre UNIQUEMENT les photos en échec
python3 scripts/photo_keyworder.py --input ~/Photos/ --retry-failed
```

- Pendant le traitement : barre de progression + **ETA** réelle
  (`[████████░░░░░░░░] 142/500 (28%) ETA 1m42s`)
- En fin de traitement : rapport `Images / Tagged / Cached / Errors / Time`
- En cas d'échec : `keyword_failed.json` liste les photos avec la raison,
  et `--retry-failed` les reprend sans rescanner tout le dossier.
- Si aucun échec, le fichier de reprise est **automatiquement nettoyé**.

**Limite connue** : le cache (`keyword_cache.json`) n'est pas écrit en
`--dry-run` — c'est voulu (rien ne doit changer en simulation), mais cela
signifie qu'un dry-run suivi d'un run réel refera tout le travail.

## Après taguage — dans Lightroom

1. Sélectionner les photos taguées
2. Menu : **Metadata → Read Metadata from Files**
3. Les keywords apparaissent en hiérarchie dans le panneau Keywords

## Catégories de keywords

| Catégorie | Exemple |
|-----------|---------|
| **Faune** | `Faune\|oiseau\|mésange`, `Faune\|mammifère\|chevreuil` |
| **Flore** | `Flore\|arbre\|chêne`, `Flore\|fleur\|orchidée` |
| **Comportement** | `Comportement\|statique\|perché`, `Comportement\|alimentation\|chasse` |
| **Saison** | `Saison\|Printemps` |
| **Moment** | `Moment\|Aube`, `Moment\|Crépuscule` |
| **Lumière** | `Lumière\|Contre-jour`, `Lumière\|Lumière douce` |
| **Composition** | `Composition\|Gros plan`, `Composition\|Fond flou` |
| **Habitat** | `Habitat\|Forêt`, `Habitat\|Marais` |
| **Technique** | `Technique\|Bokeh`, `Technique\|Net` |
| **Ambiance** | `Ambiance\|paisible`, `Ambiance\|dramatique` |
| **Auto** | `Auto\|Confiance_Haute` (indique tag auto, niveau de confiance) |

## Fichiers

| Fichier | Rôle |
|---------|------|
| `keyword_taxonomy.json` | Taxonomie complète (80+ espèces faune, 40+ flore, comportements, etc.) |
| `keyword_prompt.md` | Prompt envoyé au modèle vision |
| `keyword_cache.json` | Cache des images déjà traitées (fingerprint = nom + taille + date) |
| `../scripts/photo_keyworder.py` | Script principal |

## Performance

| Modèle | Machine | Temps/image |
|--------|---------|-------------|
| gemma4 | M5 (local) | ~18s |
| llama3.2-vision:11b | M1 (Tailscale) | ~8-12s (estimé) |

## Prochaines améliorations possibles

- Connecter à `argus_critique.db` pour enrichir les tags avec les scores Argus
- Génération automatique de planches contact par keyword
- Export Lightroom Smart Collections basé sur les keywords auto
- Fine-tuning d'un modèle spécialisé faune européenne
