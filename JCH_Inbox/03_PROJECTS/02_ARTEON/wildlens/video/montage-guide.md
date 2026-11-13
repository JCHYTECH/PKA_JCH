---
date: 2026-11-01
source: editorial-dobby
domain: arteon/blogging
project: WildLens
status: draft
type: montage-guide
lang: fr
---

# Guide de montage — « L'IA ne parlera jamais le langage du vivant »

> Assemblage dans **DaVinci Resolve**. Tout est dans `video/` : `vo/` (audio), `clips/` (vidéos IA), `assets/` (images).
> Durée totale voix off : **8 min 19 s**.

---

## Setup global

- **Résolution** : 1920×1080 (16:9) · **25 fps** (ou 30).
- **Piste A1** : la voix off — 9 MP3, dans l'ordre, bout à bout.
- **Piste V1** : les visuels principaux (images/clips).
- **Piste V2** : surimpressions (spectrogramme), textes, titres.
- **Musique** : sur **A2**, **−18 dB sous la voix**, fondu 2 s entrée/sortie.
- **Transitions** : Cross Dissolve 1 s entre les scènes.
- **Images fixes** : **Dynamic Zoom** (zoom 105→110 %, Ease In/Out) pour le mouvement parallaxe.

---

## Timeline (timecodes cumulés)

| Scène | Timecode | Audio | Visuel (V1) |
|-------|----------|-------|-------------|
| 1 | 0:00 → 0:38 | `scene-01.mp3` | `assets/03-manuscrit-voynich.jpg` (zoom lent) + titre (V2) |
| 2 | 0:38 → 1:51 | `scene-02.mp3` | Voynich → carte « Linéaire A · Rongorongo · Indus » (texte) → papyrus Herculanum (stock) |
| 3 | 1:51 → 2:50 | `scene-03.mp3` | baleine (stock) + `clips/clip-b-spectrogramme.mp4` en surimpression (V2) |
| 4 | 2:50 → 3:24 | `scene-04.mp3` | `assets/05-cerveau-passereau.jpg` → tracé neuronal → partition |
| 5 | 3:24 → 4:33 | `scene-05.mp3` | `assets/06b-fleur-uv.jpg` → spectre 20 Hz–150 kHz → `assets/06-umwelt-grenouille.jpg` |
| 6 | 4:33 → 5:38 | `scene-06.mp3` | `clips/clip-a-trou.mp4` + boucle 4 nœuds |
| 7 | 5:38 → 6:33 | `scene-07.mp3` | `assets/08-anciens-corvide.jpg` → manuscrits → indicateur (stock) + **×3** |
| 8 | 6:33 → 7:24 | `scene-08.mp3` | `assets/09-dialecte-mesange.jpg` → `clips/clip-c-convergence.mp4` → citation |
| 9 | 7:24 → 8:19 | `scene-09.mp3` | `assets/11-cloture-brume.jpg` (zoom lent) + signature WildLens |

---

## Titres / textes (Effects Library → Titles → Text+)

**Titre (scène 1, 0:00 → 0:38) :**
- Ligne 1 (Space Grotesk, bold) : **L'IA ne parlera jamais le langage du vivant**
- Ligne 2 (Lora, italique) : *Du manuscrit de Voynich au chant des oiseaux — pourquoi la machine voit les motifs, pas le sens.*

**Surtitres de section** (coin haut-gauche, début de scène) :
1. *Le manuscrit qui résiste* (scène 2)
2. *Le même mur, côté animal* (scène 3)
3. *Le cerveau ne suffit pas* (scène 4)
4. *La fleur qu'on ne voit pas* (scène 5)
5. *Peut-on déduire un monde inconnu ?* (scène 6)
6. *Ce que les anciens savaient* (scène 7)
7. *La loi du dialecte* (scène 8)

**Citation (scène 8, fin) :**
> « Le dialecte est le luxe des signaux non vitaux. »

**Clôture (scène 9) :**
> « La machine cartographie ce qui est mesurable. Le sens appartient à celui qui reste immobile, qui écoute — et qui accepte d'être regardé en retour. »

---

## Procédure DaVinci Resolve (pas à pas)

1. **Importer** : `File → Import → Media` (ou glisser dans le **Media Pool**) → les 9 MP3 de `vo/`, les 3 MP4 de `clips/`, les 10 images de `assets/`.
2. **Timeline** : `File → New Timeline` → 1920×1080, 25 fps → nomme-la « WildLens-IA-vivant ».
3. **Voix off** : glisse `scene-01.mp3` … `scene-09.mp3` sur **A1**, dans l'ordre, bout à bout (elles se collent automatiquement).
4. **Visuels** : glisse chaque image/clip sur **V1**, calé sur la durée de sa scène (cf. timeline). Utilise **V2** pour le spectrogramme en surimpression (scène 3) et les textes.
5. **Zoom (Ken Burns)** : sélectionne une image fixe → **Inspector → Video → Dynamic Zoom** → coche « Dynamic Zoom », choisis « Ease In / Ease Out ». (Alternative manuelle : keyframes sur le paramètre Zoom.)
6. **Clips IA** : `clip-b` en **V2** (opacité ~60 %) sous la baleine (scène 3) ; `clip-a` (scène 6) et `clip-c` (scène 8) en **V1** plein écran.
7. **Textes** : **Effects Library → Titles → Text+** → glisse sur **V2** → édite le texte dans l'Inspector. Pose le titre, les 7 surtitres, les 2 citations aux timecodes.
8. **Transitions** : **Effects Library → Video Transitions → Cross Dissolve** → glisse entre les scènes (1 s).
9. **Musique** : importe ta nappe, pose sur **A2**, règle le niveau à **−18 dB** sous la voix, fondu 2 s (Inspector → Volume keyframes, ou Fairlight).
10. **Étalonnage** : page **Color** → harmonise les plans (un léger réchauffement global + contraste doux suffit). C'est ici que le « look WildLens » se crée.
11. **Sous-titres** : en Studio, `Timeline → Transcribe` → les sous-titres se génèrent depuis la VO automatiquement.
12. **Export** : page **Deliver** → format **MP4 · H.264**, 1920×1080, 25 fps, « Render ».

---

## Bonus Studio (ta licence)

- **Transcription auto** : `Timeline → Transcribe` → sous-titres générés depuis la VO (étape 11).
- **Voice Isolation** (Fairlight) : isole/nettoie la voix Brian — utile pour la séparer de la musique si besoin.
- **Magic Mask** : détache le sujet (héron, mésange) pour un parallaxe avancé, si tu veux pousser le mouvement.
- **Noise Reduction** (Neural Engine) : supprime un éventuel souffle de la VO.

---

## Checklist finale

- [ ] Aucune image de faune générée par IA (uniquement les 3 clips abstraits).
- [ ] Fond clair partout, pas de plan sombre.
- [ ] Voix audible au-dessus de la musique (−18 dB).
- [ ] Sous-titres calés sur la VO.
- [ ] Durée finale ≈ 8 min 30.
- [ ] Signature « WildLens » à la fin.
- [ ] Étalonnage harmonisé entre les plans.

---

*Tu es en **DaVinci Resolve Studio** : transcription auto, Voice Isolation et Neural Engine sont débloqués (voir « Bonus Studio »).*
