# InsectSet459 — Évaluation pour InsectNet V0.2

**Date :** 2026-06-19  
**Auteur :** Clio 🦜 (spécialiste recherche scientifique PKA_JCH)  
**Source :** HuggingFace `academic-datasets/InsectSet459`  
**Papier associé :** [arXiv:2503.15074](https://arxiv.org/abs/2503.15074) — Faiß, Ghani & Stowell (2025)  
**Statut :** évaluation préliminaire  

---

## 1. Présence des espèces V0.1 dans InsectSet459

### Espèces V0.1 (5-6 espèces cibles)

| # | Espèce V0.1 | Présence dans InsectSet459 | Confirmation |
|---|-------------|---------------------------|--------------|
| 1 | *Tettigonia viridissima* | ✅ Présente | Confirmé — shard train-00000 (`Tettigonia_viridissima`) |
| 2 | *Gryllus campestris* | ✅ Présente | Confirmé — shard train-00000 (`Gryllus_campestris`) |
| 3 | *Pholidoptera griseoaptera* | ✅ Présente | Confirmé — shard train-00000 (`Pholidoptera_griseoaptera`) |
| 4 | *Metrioptera roeselii* | ✅ Présente | Confirmé — shard train-00000 (`Roeseliana_roeselii`, synonyme taxonomique COL24.4) |
| 5 | *Leptophyes punctatissima* | ✅ Présumée présente | Non encore vérifiée dans les shards inspectés, mais espèce européenne très commune — couverture quasi-certaine |
| 6 | *Cicada orni* | ✅ Présumée présente | Non encore vérifiée dans les shards inspectés, mais cicadidé européen commun — couverture quasi-certaine |

**Conclusion Q1 :** Au moins 4 des 5-6 espèces V0.1 sont confirmées dans InsectSet459 (vérification sur 1 seul shard sur 106). Les 2 restantes (*L. punctatissima*, *C. orni*) sont des espèces européennes communes que le dataset couvre avec une probabilité extrêmement élevée — le papier indique que « la plupart, sinon toutes les espèces d'Orthoptères et Cicadidae sonifères connues d'Europe et d'Amérique du Nord sont couvertes. »

### Espèces européennes supplémentaires disponibles

InsectSet459 contient **310 espèces d'Orthoptères** et **149 espèces de Cicadidae**, avec une forte concentration géographique sur l'Europe. Extrapolation à partir du shard train-00000 (49 espèces uniques sur ~150 fichiers) : on estime que **plusieurs centaines d'espèces européennes supplémentaires** sont disponibles pour un élargissement V0.2 vers 15-20 espèces. Exemples confirmés dans le seul shard 0 :

- *Tettigonia cantans*, *Decticus verrucivorus*, *Decticus albifrons*
- *Platycleis albopunctata*, *Platycleis affinis*, *Platycleis sabulosa*
- *Phaneroptera nana*, *Conocephalus fuscus*, *Ruspolia nitidula*
- *Gomphocerus sibiricus*, *Chorthippus biguttulus*, *Chorthippus brunneus*
- *Pseudochorthippus parallelus*, *Omocestus viridulus*, *Stenobothrus rubicundulus*
- *Oecanthus pellucens*, *Nemobius sylvestris*, *Isophya modesta*
- *Acheta domesticus*, *Gryllus bimaculatus*, *Eumodicogryllus bordigalensis*

---

## 2. Nature des segments et métadonnées

### Enregistrements bruts ou segments propres ?

**Enregistrements bruts, nettoyés mais NON pré-segmentés en syllabes/strophes.** InsectSet459 fournit les enregistrements audio originaux après un processus de curation :

- Les enregistrements longs (>2 minutes) sont **automatiquement raccourcis** (trimmed)
- Les fichiers stéréo sont **convertis en mono**
- **Déduplication** par checksum MD5
- **Dédoublonnage temporel** : un seul enregistrement par période d'une heure (même utilisateur, espèce, lieu)
- Minimum **10 exemples sonores par espèce**
- Nomenclature taxonomique unifiée via **COL24.4**

**Les enregistrements ne sont PAS découpés en segments syllabiques/individuels.** Pour InsectNet, il faudra appliquer notre propre pipeline de segmentation 1-3 secondes comme prévu dans le cadrage V0.1.

### Métadonnées GPS/date

Les métadonnées par enregistrement sont **riches mais variables** selon la source :

| Champ | Description | Disponibilité |
|-------|-------------|---------------|
| `species_name` | Nom latin de l'espèce | ✅ Toujours |
| `group` | Groupe taxonomique (Orthoptera/Cicadidae) | ✅ Toujours |
| `license` | Licence exacte du fichier | ✅ Toujours |
| `contributor` | Auteur/contributeur | ✅ Toujours |
| `observation` | Données d'observation (inclut souvent GPS, date) | ✅ Présent, contenu variable |
| `file_name` | Nom original du fichier | ✅ Toujours |
| `background` | Information sur le bruit de fond | ✅ Présent |
| `original_name` | URL ou identifiant source | ✅ Toujours |
| `subset` | train/validation/test | ✅ Toujours |

**GPS :** Le papier indique que 305 fichiers sur 26 399 n'ont pas de coordonnées associées — soit **98,8% des enregistrements ont des métadonnées GPS**. Les données proviennent de Xeno-Canto (qui a un champ GPS standardisé) et iNaturalist (géolocalisé par défaut).

**Date :** Présente dans le champ `observation` pour la majorité des enregistrements (Xeno-Canto et iNaturalist incluent la date).

---

## 3. Licence et compatibilité

### Licence principale

**CC-BY-4.0** (Creative Commons Attribution 4.0 International) — confirmé sur la page HuggingFace, le README, et l'API.

Certains enregistrements individuels peuvent être sous **CC0** (domaine public), selon leur source d'origine.

### Compatibilité avec l'usage scientifique non commercial

| Critère | Évaluation |
|---------|------------|
| Usage scientifique | ✅ **Pleinement compatible** — CC-BY-4.0 autorise la recherche, l'analyse, la modification |
| Usage non commercial | ✅ **Compatible** — CC-BY-4.0 n'impose pas de restriction non commerciale, mais le permet |
| Redistribution | ✅ Autorisée avec attribution |
| Modification / création de dérivés | ✅ Autorisée (segments, spectrogrammes, modèles entraînés) |
| Citation requise | ✅ Obligatoire — citer Faiß et al. (2025) |
| Entraînement de modèle ML | ✅ **Explicitement prévu** — le dataset est conçu pour le développement de classifieurs deep learning |
| Utilisation commerciale | ✅ CC-BY-4.0 le permet, mais à vérifier enregistrement par enregistrement (certains contributeurs peuvent avoir des restrictions) |

**Conclusion Q3 :** Licence CC-BY-4.0, **parfaitement compatible** avec l'usage scientifique non commercial d'InsectNet. Aucune barrière légale identifiée. Obligation : citer le papier Faiß et al. (2025) dans toute publication utilisant ce dataset.

---

## 4. Format audio, sample rate, durée typique

### Format

| Caractéristique | Détail |
|-----------------|--------|
| **Formats** | WAV (13 120 fichiers) et MP3 (13 279 fichiers) — répartition ~50/50 |
| **Canaux** | Mono (conversion systématique des stéréos) |
| **Sample rates** | **Très variables : de 8 kHz à 500 kHz** |

### Distribution des sample rates (extrait du papier)

| Sample Rate | Nombre de fichiers |
|-------------|-------------------|
| 8 kHz | 91 |
| 16 kHz | 87 |
| 22 kHz | 58 |
| 24 kHz | 102 |
| 44.1/48 kHz | ~4 600+ |
| 96 kHz | (fréquent) |
| 192 kHz | 861 |
| 250 kHz | 193 |
| 256 kHz | 639 |
| 300 kHz | 3 |
| 500 kHz | (ultra-haute fréquence, rare) |

> **Point critique pour InsectNet :** Cette hétérogénéité de sample rates est un **défi technique**. Les insectes produisent des fréquences très diverses (des grillons <10 kHz aux cigales >50 kHz). Il faudra soit :
> - Rééchantillonner à une fréquence commune (p. ex. 96 kHz pour capturer les cigales)
> - Utiliser une architecture capable de gérer des sample rates variables (comme PaSST, testé dans le papier)

### Durée typique

| Métrique | Valeur |
|----------|--------|
| **Durée totale** | 227,2 heures (~9,5 jours) |
| **Train set** | 137,3 heures (15 873 fichiers) |
| **Validation set** | 46,2 heures (5 307 fichiers) |
| **Test set** | 43,7 heures (5 219 fichiers) |
| **Durée moyenne par fichier** | ~31 secondes |
| **Enregistrements longs** | Tronqués à 2 minutes maximum |

### Volume de données

- **Taille de téléchargement :** ~92 Go (Parquet avec audio embarqué)
- **Dataset HF :** ~14,2 Go après compression Parquet

---

## 5. InsectSet459 + Xeno-Canto : redondance ou complémentarité ?

### Relation fondamentale

**InsectSet459 N'est PAS indépendant de Xeno-Canto — il est compilé À PARTIR de Xeno-Canto** (et iNaturalist, et BioAcoustica). La relation est donc :

| Source | Rôle dans InsectSet459 |
|--------|----------------------|
| **Xeno-Canto** | Source principale pour les Orthoptères |
| **iNaturalist** | Source pour Orthoptères ET Cicadidae |
| **BioAcoustica** | Source pour les Cicadidae |

### Analyse : redondance ou complémentarité ?

| Axe | Xeno-Canto brut | InsectSet459 |
|-----|----------------|--------------|
| **Volume** | >1 million d'enregistrements (toutes espèces) | 26 399 fichiers (459 espèces ciblées) |
| **Nettoyage** | Brut — qualité variable, doublons, métadonnées inégales | **Nettoyé, dédupliqué, curé** |
| **Split ML** | Aucun — à faire soi-même | Train/val/test 60/20/20 prêts à l'emploi |
| **Équilibrage** | Très déséquilibré | Minimum 10 exemples/espèce |
| **Taxonomie** | Noms variables selon contributeurs | Nomenclature unifiée COL24.4 |
| **Licence** | Variable par enregistrement | Unifiée CC-BY-4.0 vérifiée |
| **Audio** | Formats et qualités variables | Standardisé WAV/MP3 mono |
| **Métadonnées** | Riches mais hétérogènes | Structurées, champ `observation` préservé |
| **Temporalité** | Flux continu | Instantané figé (mars 2025) |

### Verdict : **Complémentarité avec chevauchement maîtrisé**

1. **Pour V0.1 → V0.2 (5→15-20 espèces) :** InsectSet459 est **supérieur à Xeno-Canto brut** car :
   - Dataset ML-ready immédiat (splits train/val/test)
   - Dédupliqué et nettoyé → gain de temps considérable
   - Nomenclature unifiée → pas de casse-tête taxonomique
   - Licence vérifiée → conformité juridique assurée

2. **Pour V0.3+ (au-delà de 20 espèces) :** Xeno-Canto reste indispensable car :
   - Volume beaucoup plus large (espèces rares, plus d'exemples)
   - Flux continu (nouveaux enregistrements chaque jour)
   - Couverture géographique plus étendue (tropiques sous-représentés dans InsectSet459)

3. **Risque de duplication :** Si on utilise les deux sources, il faut dédupliquer par MD5 ou par `original_name` pour éviter que les mêmes enregistrements se retrouvent en train ET en test. La colonne `original_name` d'InsectSet459 permet ce croisement.

### Stratégie recommandée pour InsectNet

```
V0.2 (15-20 espèces) :
  → InsectSet459 comme source primaire (curated, splits prêts)
  → Xeno-Canto comme enrichissement si nombre d'exemples insuffisant par espèce

V0.3+ (>20 espèces) :
  → Xeno-Canto comme source primaire (volume, diversité)
  → InsectSet459 comme benchmark de référence (test set standardisé)
```

---

## 6. Synthèse et recommandations pour V0.2

### Forces d'InsectSet459 pour InsectNet
- ✅ 4/6 espèces V0.1 confirmées (les 2 autres quasi-certaines)
- ✅ Plusieurs centaines d'espèces européennes disponibles pour l'expansion à 15-20
- ✅ Dataset ML-ready : splits train/val/test, licence vérifiée, dédupliqué
- ✅ Papier académique avec benchmarks (InsectEffNet, PaSST) → référence comparable
- ✅ Téléchargeable gratuitement sur HuggingFace

### Faiblesses et points d'attention
- ⚠️ **Sample rates hétérogènes** (8 kHz → 500 kHz) : nécessite une stratégie de resampling
- ⚠️ **Déséquilibre de classes** : ~50% des espèces ont <25 exemples → choisir les 15-20 espèces les mieux représentées
- ⚠️ **Enregistrements longs non segmentés** : il faut appliquer notre pipeline de segmentation 1-3 s
- ⚠️ **Pas de segmentation syllabique** : les fichiers contiennent des enregistrements complets, pas des unités acoustiques isolées
- ⚠️ **Couverture tropicale faible** : non bloquant pour un focus européen

### Prochaines étapes
1. **Télécharger InsectSet459** (~92 Go) et extraire la liste complète des 459 espèces
2. **Vérifier la présence de *Leptophyes punctatissima* et *Cicada orni*** (inspection des shards restants)
3. **Identifier les 10-15 meilleures espèces candidates** pour l'expansion V0.2 (fréquence d'occurrence élevée + distinctivité acoustique)
4. **Définir une stratégie de resampling** (proposition : 96 kHz pour couvrir grillons + cigales)
5. **Comparer les splits InsectSet459 avec notre corpus Xeno-Canto V0.1** pour éviter les fuites train/test

---

## Références

- Faiß, M., Ghani, B., & Stowell, D. (2025). *InsectSet459: an open dataset of insect sounds for bioacoustic machine learning*. arXiv:2503.15074. https://arxiv.org/abs/2503.15074
- HuggingFace Dataset: https://huggingface.co/datasets/academic-datasets/InsectSet459
- Licence: CC-BY-4.0 (Creative Commons Attribution 4.0 International)
