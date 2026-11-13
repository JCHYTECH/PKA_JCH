---
name: pka-decouvertes
description: Pipeline PKA DÉCOUVERTES — identifier des lieux depuis des screenshots (inbox SITES/) ou des messages Telegram, et générer des fiches mémoire Obsidian. Deux modes : "decouvertes inbox" (screenshots dans 00_INBOX/SITES/) et "decouvertes telegram" (groupe DÉCOUVERTES). Déclencher sur "decouvertes inbox", "traite les screenshots SITES", "decouvertes telegram", "identifie les lieux", "analyse les decouvertes".
---

# pka-decouvertes — Identifier des lieux et les mettre en mémoire

Transforme des screenshots / photos de lieux en **fiches Obsidian** (GPS, région, ville, scores photo/nature/patrimoine, accès van 2 m).

**Deux entrées, un même pipeline d'analyse.** La seule différence : comment l'image entre dans `queue/`.

---

## MODE A — Screenshots dans l'inbox (`00_INBOX/SITES/`)

Les screenshots déposés manuellement dans `JCH_Inbox/00_INBOX/SITES/` **ne sont PAS captés** par le collector (qui n'écoute que Telegram). Il faut les injecter manuellement.

### Étapes

1. **Lister les images :**
   ```bash
   ls JCH_Inbox/00_INBOX/SITES/*.jpeg
   ```

2. **Injecter chaque image** (copie image + métadonnée de file d'attente).
   - Slug au format `YYYYMMDD_HHMMSS_<n>`
   - Image → `JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/raw/images/<slug>.jpg`
   - Métadonnée → `JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/queue/<slug>.json` :
     ```json
     {
       "telegram_message_id": "0",
       "telegram_group": "SITES",
       "author": "JCH",
       "datetime": "<ISO8601>",
       "content_type": "screenshot",
       "text": "",
       "links": [],
       "media_files": [
         {"file_path": "JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/raw/images/<slug>.jpg", "media_type": "screenshot"}
       ],
       "analysis_status": "pending",
       "place_candidates": [],
       "confidence": null
     }
     ```
   > `file_path` est **relatif à PKA_ROOT** (`/Users/jchavauxm5/PKA_JCH`), comme l'écrit le collector.

3. **Lancer l'analyse** (section commune plus bas).

4. **Valider**, puis **archiver les originaux de `SITES/`** (les déplacer hors inbox pour éviter le re-traitement).

---

## MODE B — Via Telegram (groupe DÉCOUVERTES)

1. Le collector `collector.py` tourne **24/7** et capte automatiquement photos, screenshots, documents, liens, textes, GPS → `raw/` + `queue/` :
   ```bash
   cd ~/PKA_JCH/scripts/decouvertes-collector && source venv/bin/activate && python3 collector.py
   ```
   ⚠️ Une seule instance. En cas de `Conflict` : `pkill -f collector.py` puis relancer.

2. **Lancer l'analyse** quand tu veux (ci-dessous).

---

## Analyse (commun aux deux modes)

```bash
cd ~/PKA_JCH/scripts/decouvertes-collector
source venv/bin/activate
python3 analyzer.py              # Claude Haiku (rapide, ~0,01€/msg)
python3 analyzer.py --cascade    # qwen3.5 → haiku → sonnet → opus (fiable)
python3 analyzer.py --limit 5    # seulement les N premiers en attente
```

L'analyzer identifie le lieu via :
- **OCR** — tesseract `fra+eng+ita+deu`, multi-passe PSM 6 → 3 → N&B
- **EXIF** — GPS si présent dans l'image
- **LLM** — synthèse en fiche structurée

Enrichissement externe : **Nominatim** (reverse geocoding) + **Overpass** (réserves naturelles 25 km, attractions 30 km, restos 15 km).

Sorties produites :
- fiche Obsidian → `drafts/`
- rapport HTML interactif → `reports/`
- carte HTML → `maps/`
- ligne CSV Google Maps → `lieux_google_maps.csv`

---

## Validation (commun)

⚠️ **Auto-validation systématique (décision JC 2026-09-21)** — on valide **tout** en bloc après chaque analyse, sans relecture :

```bash
python3 auto_validate.py            # déplace drafts/*.md → validated_places/ (idempotent)
python3 auto_validate.py --dry-run  # aperçu sans déplacement
```

Le `status` du frontmatter est conservé (`validated` / `a_enrichir` / `needs_review`). `needs_review` reste une simple étiquette informative — plus de relecture manuelle.

---

## Chemins canoniques

| Élément | Chemin (sous PKA_ROOT) |
|---------|------------------------|
| Base | `JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/` |
| Images brutes | `raw/images/` |
| Textes / liens / métadonnées | `raw/text/`, `raw/links/`, `raw/metadata/` |
| File d'attente | `queue/` |
| Fiches générées | `drafts/` |
| Fiches validées | `validated_places/` |
| Rapports / cartes | `reports/`, `maps/` |
| Logs | `logs/collector.log` |
| Secrets | `JCH_PRIVATE/decouvertes.env` |

## Vérifications rapides

```bash
ps aux | grep collector.py                        # collecteur actif ?
ls JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/queue/    # en attente ?
ls JCH_Inbox/03_PROJECTS/07_TRAVELS/pka-decouvertes/drafts/   # fiches générées ?
```

## Références

- `07_TRAVELS/pka-decouvertes/MODE_EMPLOI.md` — manuel complet
- `07_TRAVELS/pka-decouvertes/PKA_DECOUVERTES_Cahier_des_charges_V2.md` — spec pipeline
- `scripts/decouvertes-collector/collector.py` — collecte Telegram
- `scripts/decouvertes-collector/analyzer.py` — analyse (OCR + EXIF + LLM + Overpass)
