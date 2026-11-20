# Veille IA identification d'espèces & agents naturalistes — 2026-11-16

> Cycle hebdo. Périmètre : `JCH_Inbox/03_PROJECTS/06_PHOTO_NATURE/veille-ia-identification-especes.md`.
> Recherches : web_search (Tavily), requêtes FR + EN du périmètre.
> Règle stricte : ne rien acheter, ne rien adopter, ne rien installer.

## Résumé
4 nouveautés relevées (3 modèles de fondation + 1 outil FR), toutes en « s'en souvenir ».
Aucun nouvel « agent IA naturaliste » — la catégorie émergente reste vide cette semaine.

## Nouveautés (hors baseline)

1. **SpeciesNet** — Google Research
   - Type : ID vision (modèle, orienté pièges photo)
   - Prix : open source (gratuit)
   - Lien : https://research.google/blog/where-wild-things-roam-identifying-wildlife-with-speciesnet
   - Détail : ~2 500 catégories animales, entraîné sur 65 M d'images labellisées (écosystème Wildlife Insights), sorti en open source.
   - Verdict : **s'en souvenir** — modèle notable mais ciblé camera-trap, pas le workflow photo naturaliste de JC.

2. **Perch v2 (+ SurfPerch)** — Google DeepMind
   - Type : bioacoustique (modèle de fondation)
   - Prix : open model (Kaggle, gratuit)
   - Lien : https://deepmind.google/blog/how-ai-is-helping-advance-the-science-of-bioacoustics-to-save-endangered-species
   - Détail : classifieur oiseaux >10 k espèces, généralisé mammifères/amphibiens/bruit anthropique et milieux sous-marins ; intégré BirdCLEF 2026.
   - Verdict : **s'en souvenir** — brique amont bioacoustique, référence montante à côté de BirdNET.

3. **BioCLIP 2.5 Huge** — Imageomics (Ohio State)
   - Type : modèle de fondation taxonomique
   - Prix : open source
   - Lien : https://github.com/Imageomics/bioclip-2
   - Détail : fév 2026, OpenCLIP ViT-H/14, TreeOfLife-200M (214 M d'images, ~868 k espèces).
   - Verdict : **s'en souvenir** — mise à jour du dérivé BioCLIP (déjà en veille amont).

4. **DeepFaune** — CNRS (CEFE/LECA/LBBE)
   - Type : ID vision (pièges photo, faune FR hexagonale)
   - Prix : gratuit, local (sans serveur distant)
   - Lien : https://www.deepfaune.cnrs.fr
   - Détail : 43 classes (ongulés, grands/petits mammifères, domestiques, + « oiseau » 8 sous-classes) ; Windows/Linux/Mac ; détection puis classification.
   - Verdict : **s'en souvenir** — FR, local, gratuit, mais mammifères/pièges photo, pas oiseaux/insectes photo naturaliste.

## Écartés (signal faible / redondant)
- **TrapTagger** — OSS camera-trap, redondant avec SpeciesNet/DeepFaune.
- **A2O Bioacoustic Search Platform** (Development Seed + Google Research) — moteur de similarité audio pour la recherche/conservation, pas un produit pour JC.
- **Wild Me / Wildbook** (Conservation X Labs) — photo-identification *individuelle* (re-ID), pas d'identification d'espèce.
- **WolfVue** — signal faible (post Reddit).
- **Animal Identifier AI Scan**, **iSpecies** — apps mobiles cloud par abonnement, redondantes avec iNaturalist/Seek/PictureThis.

## Agent IA naturaliste (émergent)
Rien de nouveau. Le pattern « HackerTube » appliqué au naturalisme n'a pas produit de nouveau produit ce cycle. À surveiller au prochain cycle.

## Baseline
3 entrées ajoutées : SpeciesNet, Perch v2/SurfPerch, DeepFaune. Paragraphe « À part » mis à jour (BioCLIP 2.5 Huge).

## Prochain cycle
Re-lancer les requêtes du périmètre. Surveiller en priorité : apparition d'un « agent naturaliste » produit, et tout outil ID vision couvrant oiseaux/insectes belges + alpins, local, sans abonnement.
