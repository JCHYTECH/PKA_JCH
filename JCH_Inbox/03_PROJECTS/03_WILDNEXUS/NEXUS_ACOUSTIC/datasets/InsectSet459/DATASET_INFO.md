# InsectSet459 — Fiche Dataset
> Dobby 🦉 — 2026-07-03
> Source : Zenodo DOI 10.5281/zenodo.18554693
> Stockage local : `NEXUS_ACOUSTIC/datasets/InsectSet459/`

---

## Résumé

| Champ | Valeur |
|-------|--------|
| **Taille totale** | 83.7 GB (zip) |
| **Fichiers audio** | 26 298 |
| **Durée audio** | 9.5 jours |
| **Espèces** | 459 (310 Orthoptera + 149 Cicadidae) |
| **Split** | Train 60% / Validation 20% / Test 20% |
| **Licence** | CC BY 4.0 (tous les fichiers) |
| **Publication** | Nature Scientific Data, 2026 |
| **Auteurs** | Marius Faiß (Max Planck) + Dan Stowell (Naturalis) |

## Structure

```
InsectSet459/
├── Train_Val_Test_README.txt          ✅ 20.5 kB (téléchargé)
├── InsectSet459_Train_Val_Test_Annotation.csv  ✅ 6.9 MB (téléchargé)
├── Train.zip                          ⏳ 51.2 GB
├── Validation.zip                     ⏳ 16.4 GB
└── Test.zip                           ⏳ 16.0 GB
```

## Top 15 espèces européennes d'orthoptères (pertinentes PKA)

| Espèce | Fichiers | Durée |
|--------|----------|-------|
| Gryllus campestris | 675 | 4:08:12 |
| Tettigonia viridissima | 620 | 4:32:58 |
| Oecanthus pellucens | 492 | 3:45:51 |
| Chorthippus biguttulus | 335 | 4:21:41 |
| Roeseliana roeselii | 291 | 2:14:01 |
| Tettigonia cantans | 263 | 2:22:00 |
| Pseudochorthippus parallelus | 225 | 2:26:11 |
| Chorthippus brunneus | 205 | 2:10:02 |
| Conocephalus fuscus | 153 | 1:21:59 |
| Platycleis albopunctata | 139 | 1:30:37 |
| Leptophyes punctatissima | 132 | 1:30:10 |
| Ruspolia nitidula | 119 | 1:08:23 |
| Nemobius sylvestris | 115 | 0:58:50 |
| Gryllotalpa gryllotalpa | 141 | 1:27:31 |
| Decticus verrucivorus | 89 | 1:17:50 |

---

## [M5] Commandes de téléchargement

```bash
cd /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/03_WILDNEXUS/NEXUS_ACOUSTIC/datasets/InsectSet459

# Train (51.2 GB) — le plus gros, à lancer en premier
curl -L -O "https://zenodo.org/records/18554693/files/Train.zip"

# Validation (16.4 GB)
curl -L -O "https://zenodo.org/records/18554693/files/Validation.zip"

# Test (16.0 GB)
curl -L -O "https://zenodo.org/records/18554693/files/Test.zip"

# Vérification intégrité
md5 Train.zip Validation.zip Test.zip
# Attendu :
# Train.zip      = 46f535ca43559bcd87b45d6fab189c5f
# Validation.zip = 0027a6ae81bd5b06526339efcfa285d5
# Test.zip       = e2037e90f51b35eb89bb9cea516c0a6d
```

**Temps estimé** : ~1-2h selon connexion (83.7 GB total).
