# ANALYSE — BIRDER DINOv2-bio
> Dobby 🦉 — DeepSeek TUI 0.8.39 — 2026-07-03  
> Source : `https://huggingface.co/birder-project/vit_reg4_so150m_p14_ls_dino-v2-bio`  
> Spécialistes mobilisés : Clio 🦉, Forge 🔨, Musaraigne 🦇

---

## 1. Résumé exécutif

**BIRDER** est un framework open-source de computer vision pour l'analyse d'images de faune sauvage. Ce modèle spécifique — `vit_reg4_so150m_p14_ls_dino-v2-bio` — est un encodeur d'images Vision Transformer (ViT) entraîné en self-supervised (DINOv2) sur **31 millions de photographies** d'organismes vivants (plantes, champignons, insectes, poissons, oiseaux, mammifères).

**⚠️ Ce n'est PAS un modèle bioacoustique.** Il travaille sur des photos RGB, pas sur des spectrogrammes audio. C'est un complément visuel au pipeline TweetyBERT/InsectSet459 analysé ce matin.

**Verdict** : Modèle pertinent pour 2 usages PKA — (1) classification automatique des photos naturalistes de JC (PHOTO_NATURE/ARTEON), (2) encodeur alternatif pour spectrogrammes InsectSet459 (les spectrogrammes sont des images). Le framework `birder` (GitLab) fournit l'infrastructure d'inférence clé en main.

---

## 2. Détails techniques

| Champ | Valeur |
|-------|--------|
| **Architecture** | SoViT-150M/14 — Vision Transformer 133.6M params, 4 register tokens |
| **Training** | DINOv2 self-supervised (pas de labels humains) |
| **Images d'entraînement** | ~31M : iNaturalist 2021, BIOSCAN-5M, TreeOfLife-10M, IP102, TreeOfLife-200M, Birder dataset privé |
| **Embedding** | 896 dimensions |
| **Résolutions** | 224×224, 252×252 (recommandé), 336×336 px |
| **Framework** | `birder` (pip install birder) — inférence + transformation |
| **Licence** | Apache 2.0 |
| **Dépôt** | HuggingFace : `birder-project/vit_reg4_so150m_p14_ls_dino-v2-bio` |
| **Code source** | GitLab : `gitlab.com/birder/birder` |
| **Taille sur disque** | ~1.6 GB (3 checkpoints .pt) |
| **Date publication** | 9 mai 2026 (dernière màj 22 mai) |
| **Téléchargements** | 7 157 (depuis mai 2026) |

### Datasets d'entraînement

| Dataset | Contenu |
|---------|---------|
| TreeOfLife-10M-EOL | Photographies naturalistes EOL |
| iNaturalist 2021 | Observations citoyennes mondiales |
| BIOSCAN-5M | Insectes (pièges Malaise, scanner) |
| TreeOfLife-200M | Subset haute diversité |
| IP102 v1.1 | 102 classes d'insectes ravageurs |
| iWildCam 2022 | Caméra-pièges (subset) |
| Birder dataset | Dataset privé (non détaillé) |

### Benchmarks (modèle 252px)

| Benchmark | Top-1 (%) |
|-----------|-----------|
| CUB-200 (oiseaux) | 92.3 |
| NEWT (tritons/salamandres) | 89.1 |
| SnakeCLEF (serpents) | 85.7 |
| iNaturalist 2021 | 81.2 |

---

## 3. Différence fondamentale : Birder vs TweetyBERT

| | Birder (DINOv2-bio) | TweetyBERT |
|---|---|---|
| **Domaine** | Vision (photos RGB) | Audio (spectrogrammes) |
| **Input** | Photographie d'organisme | Fichier audio → Mel spectrogram |
| **Architecture** | ViT 133M params | Transformer custom |
| **Sortie** | Embedding 896-dim | Embedding + tokens de parsing |
| **Usage PKA** | Photos naturalistes, spectrograms-as-images | Analyse de chants d'oiseaux/insectes |
| **Edge (ESP32)** | ❌ 133M params | ❌ Transformer lourd |
| **Backend (M5)** | ✅ | ✅ |

---

## 4. Pont Birder ↔ Spectrogrammes

**Approche valide** : Un spectrogramme Mel est une image 2D (temps × fréquence). Les modèles de vision entraînés sur ImageNet ont déjà été utilisés avec succès pour la classification bioacoustique (BirdCLEF, DCASE). Birder, entraîné spécifiquement sur de la biodiversité, pourrait être **supérieur** à un ViT générique pour cette tâche.

**Pipeline potentiel PKA** :
```
Audio → Mel spectrogram (224px) → Birder DINOv2-bio → embedding 896d → classifieur linéaire
```

Avantage sur TweetyBERT : modèle plus large (133M vs TweetyBERT ~?), embedding plus riche (896d), pré-entraîné sur des motifs biologiques variés.

Inconvénient : pas conçu pour l'audio, pas de résolution temporelle fine (2.7ms de TweetyBERT).

---

## 5. Impact cross-projets

| Projet | Impact | Détail |
|--------|--------|--------|
| **PHOTO_NATURE** | 🔴 Majeur | Classification automatique des photos wildlife de JC — 81% top-1 iNat2021 |
| **ARTEON / WildLens** | 🟡 Élevé | Tri automatique, tagging éditorial, curation de contenu |
| **NEXUS_ACOUSTIC** | 🟡 Élevé | Encodeur alternatif/complémentaire à TweetyBERT sur spectrogrammes |
| **WILDNEXUS** | ⚪ Léger | Trop lourd pour edge (133M). Backend M5 uniquement |
| **InsectNet** | 🟢 Modéré | Classification visuelle d'insectes (complément à l'acoustique) |

---

## 6. Propositions d'intégration

### 🔴 P0 (<2 sem) — Benchmark spectrogrammes

- **Action** : Extraire 100 spectrogrammes d'InsectSet459 → inference Birder 252px → classification linéaire → benchmark vs TweetyBERT
- **Responsable** : Forge 🔨 + Clio 🦉
- **Deadline** : 17 juillet
- **Métrique** : Top-1 accuracy sur 10 espèces d'orthoptères communes

### 🟡 P1 (<1 mois) — Pipeline photos naturalistes

- **Action** : Installer `birder` (pip), créer script `bin/pka_birder_classify.py`, tester sur 100 photos wildlife de JC
- **Responsable** : Forge 🔨 + Lynx 🦊
- **Deadline** : 31 juillet
- **Livrable** : Rapport de précision + intégration workflow PHOTO_NATURE

### ⚪ P2 (1-3 mois) — Fusion bimodale

- **Action** : Combiner embeddings Birder (spectro) + TweetyBERT (audio) → classifieur multimodal
- **Responsable** : Clio 🦉 + Musaraigne 🦇
- **Deadline** : Septembre 2026

---

## 7. Téléchargement

```bash
[M5] pip install birder
[M5] python -c "import birder; birder.load_pretrained_model('vit_reg4_so150m_p14_ls_dino-v2-bio-252px', inference=True)"
```

Taille : ~530 MB par checkpoint. Les 3 checkpoints = ~1.6 GB.

---

## 8. Sources validées

- Modèle HF : `birder-project/vit_reg4_so150m_p14_ls_dino-v2-bio` ✅
- README complet : 22 KB markdown ✅
- GitLab BIRDER : `gitlab.com/birder/birder` ✅
- Article DINOv2 : arXiv 2304.07193 ✅
- Article ViT registers : arXiv 2309.16588 ✅
- 7 157 téléchargements, 10 likes, dernière màj 22 mai 2026 ✅
