---
date: 2026-11-16
source: dobby
domain: arteon
type: sélection-test
status: actif
lang: fr
---

# Test M1 — Sélection de photos (jugement en aveugle)

> Dobby 🦉 — 2026-11-16 · Prépare le jalon M1 de la conception V1 (`service-correction-photo-conception.md`) :
> 10–20 corrections manuelles + jugement en aveugle par ~5 photographes.
> Critère d'arrêt : si « pire + indifférent » > 50 %, on stoppe.

---

## Le corpus

`PHOTO/analyses/thumbnails/` — les ~52 photos de JC, identifiées par espèce (rapports Argus,
`02_ARTEON/passe-utile/2026-05-11_argus_batch_rapport_*.md`). Doublons d'espèce présents
(4 rouge-gorge, 4 bernache, 3 flamants, 2 cygnes, 2 cormorans, 3 grenouilles).

**Règle de sélection** : une photo par espèce, pour maximiser la diversité de sujets et couvrir
les 12 looks du pack. 16 photos retenues (dans la fourchette 10–20).

---

## Les 16 photos retenues

| # | Fichier | Espèce | Look testé | Pourquoi celle-ci |
|---|---------|--------|------------|-------------------|
| 1 | `LrC to-6.jpg` | Rouge-gorge familier | **Signature** (base universel) | portrait d'oiseau classique, référence |
| 2 | `LrC to-3.jpg` | Buse variable | **Plumage sombre** (rapace) | sujet sombre, plumes |
| 3 | `LrC to-13.jpg` | Choucas des tours | **Plumage sombre** (corvidé noir) | noir profond, test du « débouche les noirs » |
| 4 | `LrC to-9.jpg` | Héron cendré | **Plumage clair** (gris) | sujet pâle, contre-jour doux |
| 5 | `LrC to-45.jpg` | Cygne tuberculé | **Plumage clair** (blanc pur) | test de la « coulée bleue » sur blanc |
| 6 | `LrC to-41.jpg` | Martin-pêcheur d'Europe | **Plumage coloré** (fleuron) | bleu/orange, la photo signature du pack |
| 7 | `LrC to-14.jpg` | Geai des chênes | **Plumage coloré** (bleu) | bleu à rehausser, fond végétal |
| 8 | `LrC to-12.jpg` | Vache des Highlands | **Mammifères** (fourrure fauve) | seul mammifère du corpus |
| 9 | `LrC to-25.jpg` | Scarabée vert | **Macro** (insecte) | iridescence, détail |
| 10 | `LrC to-38.jpg` | Platane (fruits) | **Macro** (botanique) | texture, neutre |
| 11 | `LrC to-29.jpg` | Oie cendrée + canards en vol | **Action / vol** (ISO haut) | mouvement, bruit à maîtriser |
| 12 | `LrC to-36.jpg` | Foulque capturant un serpent d'eau | **Action** (scène) | instant, contraste fort |
| 13 | `LrC to-2.jpg` | Paysage hivernal (chapelle + lac) | **Paysage** | ambiance, profondeur |
| 14 | `LrC to-19.jpg` | Grèbe à cou noir | **Contre-jour / eau** (ambiance) | reflets, lumière diffuse |
| 15 | `LrC to-52.jpg` | Foulque macroule, étang brumeux | **Contre-jour / brume** | brume réelle, le cas le plus « Munier » |
| 16 | `LrC to-4.jpg` | Sculpture d'aigle (bois flotté) | **Noir & blanc** | structure/contraste, candidat monochrome |

---

## Couverture des 12 looks

| Look | Couvert | Photo(s) |
|------|---------|----------|
| Signature | ✅ | 1 |
| Plumage sombre | ✅ | 2, 3 |
| Plumage clair | ✅ | 4, 5 |
| Plumage coloré | ✅ | 6, 7 |
| Golden hour | ⚠️ partiel | — (aucune photo lever/coucher clairement identifiée ; 13 s'en approche) |
| Mammifères | ✅ | 8 |
| **Nocturne** | ❌ **absent du corpus** | aucune chouette/photo de nuit dans les 52 |
| Macro | ✅ | 9, 10 |
| Action / vol | ✅ | 11, 12 |
| Paysage | ✅ | 13 |
| Noir & blanc | ✅ | 16 |
| Contre-jour / brume | ✅ | 14, 15 |

**Deux trous à trancher avec JC** :
1. **Nocturne** : aucune photo de nuit dans le corpus. Soit on l'écarte du test (le look reste non testé),
   soit JC fournit une photo de chouette/blaireau/nuit hors corpus.
2. **Golden hour** : le corpus n'a pas de lever/coucher franc. `LrC to-2` (hivernal) peut servir d'approximation.

---

## Protocole M1 (rappel)

1. **Correction manuelle** sur les **fichiers source** dans Lightroom (pas les vignettes) — un look + 2 ajustements max (expo, WB), conformément au contrat « direction, pas valeur ».
2. **Jugement en aveugle** : 16 paires avant/après, présentées sans ordre, à ~5 photographes → « préféré / indifférent / pire » + intention d'achat.
3. **Critère d'arrêt** : « pire + indifférent » > 50 % → stop (la demande n'existe pas).

> ⚠️ Les vignettes (`PHOTO/analyses/thumbnails/`) sont des JPEG réduits. Les corrections du test
> doivent se faire sur les **originaux** (RAW/pleine résolution) présents dans le catalogue Lightroom de JC.

---

*Découle de : `strategy/service-correction-photo-conception.md` (V1, jalon M1).*
