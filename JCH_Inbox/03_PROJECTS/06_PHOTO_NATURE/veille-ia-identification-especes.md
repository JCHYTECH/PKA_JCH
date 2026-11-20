# Veille — IA d'identification d'espèces & agents naturalistes

> Périmètre et baseline de la veille technologique demandée par JC le 2026-11-14.
> Suivi par : veille hebdo automatisée (Dobby 🦉). Source racine : transcript **Spécio** (studio Sim).
> Dernière mise à jour : 2026-11-16

## Pourquoi
Spécio a montré qu'une nouvelle génération d'outils IA cible l'identification d'espèces sur photo.
Objectif : repérer **l'apparition** d'outils IA / agents IA dans ce domaine, et décider à froid
« creuser / s'en souvenir / écarter » — sans jamais adopter ni acheter en veille.

## Comment les appeler (terminologie)
Trois familles, par niveau d'autonomie :

1. **Outil d'identification par IA** (vision) — logiciel/app qui propose une espèce à partir d'une photo.
   Ex. Spécio, iNaturalist, ObsIdentify, Merlin Bird ID, Seek, Excire, PictureThis.
2. **Outil bioacoustique** (son) — identifie par le chant/cri.
   Ex. BirdNET, Merlin Sound ID, InsectNet (orthoptères), BatSound.
3. **Agent IA naturaliste** (émergent) — pipeline autonome qui enchaîne identification → validation
   → catalogage → publication/partage, au-delà de la simple suggestion.
   Ex. émergents à surveiller (le pattern « HackerTube » appliqué au naturalisme).

À part : **modèles de fondation taxonomiques** (BioCLIP et dérivés) — brique sous-jacente, utile en
veille amont mais pas un « produit » pour JC. Dernier dérivé relevé : BioCLIP 2.5 Huge (Imageomics, fév 2026).

## Baseline — outils déjà connus (ne pas re-signaler)
| Outil | Type | Éditeur | Note |
|-------|------|---------|------|
| **Spécio** | ID vision | Sim (FR) | 450 k espèces, IA locale, 249 € one-shot / 99 € famille — **s'en souvenir** (décision JC 14/11) |
| iNaturalist | ID vision + communauté | iNaturalist (OSS) | gratuit, open data, 300 M+ observations |
| Merlin Bird ID | ID vision + son | Cornell Lab | gratuit, oiseaux |
| ObsIdentify | ID vision | Observation.org | gratuit, EU |
| BirdNET / BirdNET-Go | bioacoustique | Cornell/K. Lisa Yang | open source |
| InsectNet | bioacoustique/vision | Iowa State | classification orthoptères — déjà dans PKA (gelé) |
| Excire | organisation/ID photo | Excire (DE) | Lightroom plugin, payant |
| SpeciesNet | ID vision (modèle, pièges photo) | Google Research | open source, ~2 500 catégories camera-trap — **s'en souvenir** (16/11) |
| Perch v2 / SurfPerch | bioacoustique (modèle fondation) | Google DeepMind | open model (Kaggle), >10 k espèces oiseaux + mammifères/amphibiens — **s'en souvenir** (16/11) |
| DeepFaune | ID vision (pièges photo) | CNRS (FR) | gratuit, local, 43 classes faune FR hexagonale — **s'en souvenir** (16/11) |

## Requêtes de veille (à lancer chaque cycle)
- FR : `nouveau logiciel identification espèces animaux photos IA` · `agent IA photographie animalière`
- EN : `AI species identification wildlife photography software 2026` · `AI agent naturalist photo ID`
- EN (modèles) : `taxonomic vision-language model BioCLIP new`
- EN (son) : `bioacoustic species identification model new release`

## Critères de décision (verdict)
- **Creuser** : outil/agent qui couvre la faune de JC (oiseaux/insectes belges + alpins), local,
  non-abonnement, et qui complète réellement le workflow PHOTO_NATURE/Argus.
- **S'en souvenir** : prometteur mais hors périmètre immédiat, ou info à archiver.
- **Écarter** : redondant avec l'existant, cloud-only abonnement, ou signal faible/bruit.

## Sortie
Chaque cycle écrit `TEAM_Inbox/YYYY-MM-DD_dobby_veille-ia-identification-especes.md`
et met à jour la baseline ci-dessus. Aucune action d'achat ni d'adoption en veille.