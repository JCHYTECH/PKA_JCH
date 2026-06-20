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
