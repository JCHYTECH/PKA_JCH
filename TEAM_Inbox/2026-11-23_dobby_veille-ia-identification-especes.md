# Veille IA identification d'espèces — 2026-11-23

Périmètre : outils ID vision, bioacoustique, agents naturalistes, modèles de fondation taxonomiques.
Baseline relue (2026-11-16). Requêtes FR + EN lancées (Tavily). Verdicts à froid, aucune action d'achat ni d'adoption.

## Bilan de la semaine

Semaine calme. Pas de nouveauté au niveau « agent naturaliste » (pipeline autonome). Deux outils
à archiver, le reste est du bruit (apps génériques de reconnaissance animale, redondantes avec
iNaturalist/Merlin/ObsIdentify).

## Nouveautés

### 1. AddaxAI — ID vision (pièges photo) — s'en souvenir
- **Éditeur** : Addax Data Science (NL), collaboration avec Smart Parks
- **Type** : outil ID vision, orienté pièges photo / écologie (photos + vidéos)
- **Prix** : gratuit, open source (app MIT ; chaque modèle d'espèce a sa propre licence)
- **Lien** : https://addaxdatascience.com/addaxai
- **Points clés** : 100 % local (aucun upload, aucune connexion après install) ; détection MegaDetector v5
  + modèles d'espèces régionaux (dont **DeepFaune** pour l'Europe) + embeddings DINOv2 ; Mac Apple Silicon,
  Windows, Linux ; export Camtrap DP / Timelapse / CSV. 18 365 téléchargements.
- **Verdict** : s'en souvenir. Outil sérieux et gratuit, mais cible le piégeage photo écologique, pas le
  workflow photo naturaliste de JC (PHOTO_NATURE/Argus). À ressortir si JC se met au camera-trap.

### 2. A2O Bioacoustics Search Platform — bioacoustique (moteur de similarité) — s'en souvenir
- **Éditeur** : Development Seed + Google Research + Australian Acoustics Observatory (A2O)
- **Type** : outil bioacoustique, moteur de recherche par similarité audio (embeddings Perch)
- **Prix** : plateforme de recherche (open, à destination des écologues)
- **Lien** : https://developmentseed.org/projects/google-a2o-search
- **Verdict** : s'en souvenir. Vraie nouveauté de plateforme bioacoustique (Perch opérationnalisé en
  recherche vectorielle), mais hors workflow immédiat de JC. À archiver.

## Écartés (signal faible / bruit)

- **CrossPrism Nature Id** — écarté. ID vision local/offline « bugs, oiseaux, fleurs », référencé
  uniquement dans un annuaire IA (tyy.ai), aucun site éditeur ni app store confirmé. Signal faible.
- **AniPet (AppSwarm Corp)** — écarté. Énième app générique de reconnaissance animale (freemium),
  redondante avec l'existant. Bruit.
- **Wildbook / Wildlife RE-ID (Natural Solutions)** — hors périmètre : re-identification d'individus
  pour la recherche, pas un outil d'identification d'espèce pour photographe.

## Modèles de fondation — rien de nouveau

BioCLIP-2 (NIPS 2025, 214 M images / 868 k espèces) déjà couvert par la baseline via le dernier dérivé
relevé « BioCLIP 2.5 Huge (Imageomics, fév 2026) ». Rien de plus récent cette semaine.

## Requêtes utilisées

- FR : « nouveau logiciel identification espèces animaux photos IA » · « agent IA photographie animalière identification »
- EN : « AI species identification wildlife photography software 2026 » · « AI agent naturalist photo ID new tool »
- EN modèles : « taxonomic vision-language model BioCLIP new release »
- EN son : « bioacoustic species identification model new release 2026 »
