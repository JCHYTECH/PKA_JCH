# Analyse transcript — « La technologie au service des recensements d'oiseaux migrateurs »

> Dobby 🦉 · 2026-11-17 · skill `/analyse-transcript`

## Nature
- **Type** : YouTube Short (reportage grand public), **Radio-Canada Info**, FR
- **Durée** : 02:31 · **URL** : https://www.youtube.com/shorts/eJs-8TYr3vo
- **Sujet** : la technologie (radar, acoustique, IA) appliquée au comptage des oiseaux migrateurs

## Thèse
Du comptage manuel d'il y a 100 ans aux radars météo, enregistreurs acoustiques et IA,
l'ornithologie se « robotise » littéralement — mais l'humain garde sa place : « les deux
vont coexister ».

## Points clés
1. **Historique** : il y a 100 ans, comptage à l'œil des oiseaux passant devant la lune (calepin).
2. **Radar météo** : a révélé ~**4 milliards d'oiseaux** migrant chaque année en Amérique du Nord.
3. **Acoustique** : enregistrement des cris toute la nuit pendant la migration
   (mi-juillet → début novembre), des centaines d'heures par appareil.
4. **~40 enregistreurs** installés de part et d'autre du fleuve Saint-Laurent.
5. **Motus Audio** : réseau d'écoute (boîtes blanches) déployé au Canada, écoute à distance en direct.
6. **IA** : identification des chants/cris sur des dizaines de milliers d'heures — « une autre révolution ».
7. **Futur** : caméra qui détecte le mouvement dans le ciel, zoome, puis identifie l'espèce.
8. **Place de l'humain** : la machine compte, l'ornithologue « absorbe le plaisir de voir passer les oiseaux ».

## Confirmé (fact-check)
- ✅ **Établi** (vérifié web) : **Motus Audio** est une extension bioacoustique réelle du
  Motus Wildlife Tracking System (Birds Canada, lancé 2014 en radiotélémétrie) — source
  Audubon + motus.org + birdscanada.org. Le chiffre ~4 Md d'oiseaux migrateurs (Amérique du
  Nord) est une figure publiée (Dokter et al., 2018). L'ornithologie radar est un champ
  établi (BirdCast / Cornell).
- ⚠️ **Affirmé par le reportage** : « ~40 enregistreurs le long du Saint-Laurent »,
  « centaines d'heures par appareil » — détails non recoupés.
- ❓ **Spéculatif** : la caméra qui zoome puis identifie (« on pourrait s'imaginer un jour »)
  — présenté par la source comme futur hypothétique.

## Impact croisé PKA
- 🔴 **03_WILDNEXUS / NEXUS_ACOUSTIC** — cœur : le workflow décrit (enregistreurs acoustiques
  nocturnes + IA d'identification + réseau distribué) est exactement l'ambition de
  NEXUS_ACOUSTIC (BirdNET / TweetyBERT / LEAFNET). **Motus Audio = référence réelle et
  réplicable** pour le réseau acoustique de JC.
- 🟡 **03_WILDNEXUS / WILDNEXUS_DEVICE** — confirme la pertinence d'un enregistreur autonome
  de nuit + IA embarquée (edge).
- 🟡 **Musaraigne (Edge AI / TinyML)** — cas d'usage réel d'IA acoustique à grande échelle.

## Actions proposées
- **P2 · (Dobby)** — Router la référence dans `NEXUS_ACOUSTIC/99_REFERENCES/` (fait ✓).
- **P2 · (veille, au signal JC — projet gelé)** — Noter Motus Audio comme benchmark de réseau
  acoustique distribué ; étudier leur architecture (recorder → téléversement → IA) à la
  reprise de NEXUS_ACOUSTIC.
- **P3 · (roadmap)** — Triptyque utile à garder : radar (volume, 4 Md) vs acoustique
  (espèces) vs caméra (individus).

## Livrable / Routing
- **Rapport** : `NEXUS_ACOUSTIC/99_REFERENCES/2026-11-17_dobby_analyse-transcript-motus-audio.md`
- **Transcript** : `NEXUS_ACOUSTIC/99_REFERENCES/2026-11-17_transcript-la-technologie-au-service-des-recensements-d-ois.md`

## Note
Le sous-projet NEXUS_ACOUSTIC est **gelé** (dépend de la reprise WILDNEXUS DEVICE) — la
référence est routée et documentée, aucun chantier lancé.
