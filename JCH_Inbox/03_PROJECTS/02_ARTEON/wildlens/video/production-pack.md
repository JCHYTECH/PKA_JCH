---
date: 2026-11-01
source: editorial-dobby
domain: arteon/blogging
project: WildLens
status: draft
type: production-pack
lang: fr
---

# Pack de production — vidéo « L'IA ne parlera jamais le langage du vivant »

> Tout ce qu'il faut pour assembler la vidéo : prompts IA (clips abstraits), liste des plans stock, et la liste de coupe.
> Voix off : **Brian (ElevenLabs)** — 9 scènes dans `video/vo/scene-NN.mp3`, ~8 min 20 s.

---

## 1. Prompts IA (clips abstraits — jamais de faune)

À lancer dans **Veo 3 / Runway / Sora**. Modèle 16:9, ~5-8 s par clip.

### Clip A — « Le trou dans l'explication » (scène 6)
> A minimalist abstract animation: a smooth stream of glowing particles flows left to right, then stops abruptly at an invisible boundary — a perfect vertical void where nothing passes. Dark teal and deep green particles on a warm ivory background. Scientific, elegant, contemplative. No text.

### Clip B — « La structure sans le sens » (scène 3, en surimpression)
> An abstract spectrogram: clean vertical lines and soft bands pulsing slowly, minimalist, dark green on ivory, scientific, calm. No text. Loops gently.

### Clip C — « Divergence puis convergence » (scène 8)
> Two identical thin waves start together, diverge into many distinct paths, then reconverge into a single clean wave. Minimalist, dark green lines on ivory, elegant. No text.

---

## 2. Plans stock à récupérer (Storyblocks / Artgrid / Pexels)

| Scène | Sujet | Terme de recherche |
|-------|-------|--------------------|
| 2 | Papyrus d'Herculanum | `Herculaneum papyrus` · `carbonized scroll` · `ancient scroll x-ray` |
| 3 | Cachalot | `sperm whale diving` · `sperm whale underwater slow motion` |
| 7 | Indicateur + miel | `honeyguide bird` · `honey hunter Africa` *(niche — sinon image fixe)* |
| 8 | (option) rapace | `hawk flying` · `raptor glide` |

> Si le papyrus ou l'indicateur sont introuvables en stock : utiliser une **image fixe** avec zoom lent (le « parallaxe 2.5D »).

---

## 3. Liste de coupe (pour Descript / DaVinci)

| Scène | Audio | Visuel principal | Note |
|-------|-------|------------------|------|
| 1 | `scene-01.mp3` (38 s) | Voynich `03-manuscrit-voynich.jpg` + titre animé | hook < 15 s |
| 2 | `scene-02.mp3` (73 s) | Voynich → carte « Linear A·Rongorongo·Indus » → papyrus Herculanum | |
| 3 | `scene-03.mp3` (59 s) | spectrogramme `04-cachalot-spectrogramme.png` (pulse) + baleine stock | |
| 4 | `scene-04.mp3` (33 s) | passereau `05-cerveau-passereau.jpg` → tracé neuronal → partition | partition « muette » |
| 5 | `scene-05.mp3` (69 s) | fleur UV `06b-fleur-uv.jpg` (visible→UV) → spectre 20 Hz–150 kHz → grenouille `06-umwelt-grenouille.jpg` | moment fort |
| 6 | `scene-06.mp3` (65 s) | **Clip A (IA)** + boucle MOTION 4 nœuds | IA légitime (abstrait) |
| 7 | `scene-07.mp3` (55 s) | corvidé `08-anciens-corvide.jpg` → manuscrits (MOTION) → indicateur + « ×3 » | |
| 8 | `scene-08.mp3` (51 s) | mésange `09-dialecte-mesange.jpg` → **Clip C (IA)** → citation | climax |
| 9 | `scene-09.mp3` (55 s) | héron crépuscule `11-cloture-brume.jpg` (parallaxe) + signature WildLens | fondu noir |

---

## Récap des livrables

- **Voix off** : `video/vo/scene-01..09.mp3` (Brian, débit 0.9) — ✅ prêt.
- **Images fixes** : `video/deck/assets/` (10 fichiers) — ✅ prêt.
- **Clips IA** : 3 prompts ci-dessus — à générer (Veo/Runway).
- **Stock** : 4 sujets à récupérer.
- **Montage** : liste de coupe ci-dessus → Descript/DaVinci.

---

*Prochaine étape possible : je peux générer moi-même les clips IA si tu me donnes une clé Runway ou Veo. Sinon, tu lances les 3 prompts et tu récupères les clips.*
