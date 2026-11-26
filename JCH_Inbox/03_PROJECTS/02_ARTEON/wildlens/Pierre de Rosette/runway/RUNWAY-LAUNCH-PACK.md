# Runway Launch Pack — « Pourquoi on ne peut pas encore parler aux animaux »

> WildLens · Pierre de Rosette · 5 clips aquarelle animée
> Option C : style aquarelle vibrante, jamais photoréaliste
> Temps total estimé : **~20-30 min** sur runwayml.com

---

## Avant de commencer

- **Compte :** runwayml.com (Gen-4, crédits disponibles)
- **Résolution :** 1080p (ou 720p si contrainte de crédits)
- **Durée :** 5-6 secondes par clip
- **Images de référence :** disponibles dans `runway/` pour upload (optionnel mais recommandé)

---

## Clip 1 — Chien silhouette (Scène 1 : « Le rêve »)

**Usage :** juste après le portrait animal, transition vers l'idée qu'on ne comprend pas.

**Prompt Runway :**
```
Animated watercolor painting. Soft warm brown and terracotta tones. A silhouette of a dog gently turning its head in profile, as if listening. Loose brushstrokes, pigments blooming on wet paper. No photorealistic details. Contemplative, calm. Warm ivory background with ochre washes. Gentle motion, no sudden movement. 16:9, 5 seconds.
```

| Paramètre | Valeur |
|-----------|--------|
| Style | Watercolor Animation |
| Duration | 5 s |
| Aspect ratio | 16:9 |
| Negatif prompt | photorealistic, realistic fur, eyes, detailed face |
| Image ref | Non (génération pure) |

**Générer 2 variations → garder la plus douce.**

---

## Clip 2 — Cachalot + spectrogramme (Scène 2 : « Le mur »)

**Usage :** illustrer le cachalot quand on parle de ses clics. Le spectrogramme qui traverse l'animal = motif sans sens.

**Image de référence :** `cachalot-spectrogramme.png` (uploader comme style reference)

**Prompt Runway :**
```
Animated watercolor illustration. A sperm whale rendered in deep teal and indigo washes, floating vertically in dark ocean space. Translucent geometric spectrogram lines pulse across its body like musical notation. Pigment droplets disperse into wave patterns. Loose brushstrokes, wet-on-wet effect. No photorealistic details. Artistic, scientific, beautiful. 16:9, 5 seconds.
```

| Paramètre | Valeur |
|-----------|--------|
| Style | Watercolor Animation |
| Duration | 5 s |
| Aspect ratio | 16:9 |
| Negatif prompt | photorealistic, realistic whale, detailed eye |
| Image ref | `cachalot-spectrogramme.png` (style + composition) |

**Générer 2 variations → garder celle où le spectrogramme est le plus lisible.**

---

## Clip 3 — Mandarin 🦆 (Scène 3 : « Le parallèle Voynich »)

**Usage :** transition Voynich → animal. Le mandarin émerge de l'écriture ancienne. **C'est le clip le plus important** — moment visuel fort de la vidéo.

**Image de référence :** `03-manuscrit-voynich.jpg` (uploader pour le style d'écriture)

**Prompt Runway :**
```
Animated watercolor painting. A mandarin duck emerging from ancient handwritten script. The feathers form from ink strokes and calligraphy marks — deep teal, orange, purple and gold pigments bleeding into wet paper. The bird turns its head gracefully, trailing ink drops that become swimming motion. Loose watercolor texture visible. No photorealistic feathers. Elegant, poetic, East Asian ink wash influence. 16:9, 6 seconds.
```

| Paramètre | Valeur |
|-----------|--------|
| Style | Watercolor Animation |
| Duration | 6 s |
| Aspect ratio | 16:9 |
| Negatif prompt | photorealistic, realistic duck feathers, photograph |
| Image ref | `03-manuscrit-voynich.jpg` (inspiration écriture) |

**Générer 3 variations → c'est le clip héros. Prendre le temps de choisir.**

---

## Clip 4 — Abeille + fleur UV (Scène 4 : « Le piège des sens »)

**Usage :** illustrer l'Umwelt — l'abeille qui voit l'UV. Le passage de visible à UV.

**Image de référence :** `06b-fleur-uv.jpg` (uploader pour les couleurs UV)

**Prompt Runway :**
```
Animated watercolor abstract. A stylized bee silhouette in deep amber, approaching a flower rendered in ultraviolet glow colors — electric violet, luminous blue, neon pink against soft ivory. The bee leaves a trail of pigment like pollen. Wet-on-wet blooms, loose watercolor texture. The flower pulses gently revealing hidden patterns. Vibrant, dreamlike, no photorealistic details. 16:9, 5 seconds.
```

| Paramètre | Valeur |
|-----------|--------|
| Style | Watercolor Animation |
| Duration | 5 s |
| Aspect ratio | 16:9 |
| Negatif prompt | photorealistic, realistic bee, photograph |
| Image ref | `06b-fleur-uv.jpg` (palette et inspiration) |

**Générer 2 variations → garder la plus vibrante.**

---

## Clip 5 — Chimpanzé + dauphin (Scène 5 : « Alors, on fait quoi ? »)

**Usage :** illustrer les tentatives passées (langue des signes, imitations).

**Prompt Runway :**
```
Animated watercolor diptych. Left: a chimpanzee face in profile, loose brushstrokes of umber and sienna, thoughtful expression. Right: a dolphin arcing through water, teal and cerulean washes. Both rendered as artistic sketches — visible brush marks, pigment bleeding, paper texture. The two animals fade into each other through a gentle watercolor wash. No photorealistic features. Scientific illustration meets fine art. 16:9, 6 seconds.
```

| Paramètre | Valeur |
|-----------|--------|
| Style | Watercolor Animation |
| Duration | 6 s |
| Aspect ratio | 16:9 |
| Negatif prompt | photorealistic, realistic fur, realistic skin, realistic eye |
| Image ref | Non (génération pure) |

**Générer 2 variations → garder celle où le fondu entre les deux animaux est le plus fluide.**

---

## Checklist avant lancement

- [ ] Compte runwayml.com actif et crédits disponibles
- [ ] Navigateur ouvert sur https://runwayml.com
- [ ] 3 images de référence dans `runway/` prêtes à uploader
- [ ] Ce fichier ouvert en lecture

---

## Procédure pas à pas (Runway Gen-4)

### Pour chaque clip :

1. **Aller sur** https://runwayml.com → **Products** → **Gen-4**
2. **Coller le prompt** dans la zone de texte
3. **Paramétrer :**
   - Duration : 5 ou 6 s (selon le clip)
   - Aspect Ratio : 16:9
   - Style : **Watercolor Animation** (dans la galerie de styles)
4. **(Optionnel) Uploader l'image de référence** si indiquée
5. **Ajouter le négatif prompt** (texte en rouge dans les paramètres avancés)
6. **Cliquer Generate**
7. **Attendre ~2-4 min** par clip
8. **Télécharger** le MP4 → le sauvegarder dans `runway/output/` avec le bon nom

### Nommer les fichiers :

| Clip | Nom fichier |
|------|-------------|
| 1 | `clip-01-chien-silhouette.mp4` |
| 2 | `clip-02-cachalot-spectrogramme.mp4` |
| 3 | `clip-03-mandarin-voynich.mp4` |
| 4 | `clip-04-abeille-uv.mp4` |
| 5 | `clip-05-chimpanze-dauphin.mp4` |

### Si un clip rate :

- **Résultat flou ?** → Ajouter « sharp watercolor edges, defined brushstrokes » au prompt
- **Résultat trop réaliste ?** → Renforcer négatif prompt + « visible paper texture, wet watercolor effect »
- **Résultat vide/incohérent ?** → Relancer une variation, parfois le seed change tout
- **Si toujours raté après 3 essais** → me donner le résultat, j'ajuste le prompt

---

## Résumé visuel de la série

```
Clip 1 : 🐕 Silhouette chien          → Douceur, écoute
Clip 2 : 🐋 Cachalot + spectrogramme  → Science, motif sans sens
Clip 3 : 🦆 Mandarin + écriture       → Élégance, transition
Clip 4 : 🐝 Abeille + UV              → Révélation, couleur
Clip 5 : 🐵🐬 Chimpanzé + dauphin     → Diptyque, double regard
```

---

*Généré par Dobby 🦉 · 2026-11-02*