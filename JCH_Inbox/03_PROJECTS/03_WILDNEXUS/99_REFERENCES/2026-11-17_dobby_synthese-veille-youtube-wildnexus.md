# Synthèse — Veille YouTube WildNexus (9 derniers mois)

> Dobby 🦉 · 2026-11-17 · recherche `yt-dlp ytsearch` + transcription Whisper locale
> 12 requêtes · 107 vidéos uniques · 27 dans les 9 derniers mois · 8 retenues et analysées

## Les 8 vidéos retenues

| Domaine | Vidéo | Chaîne | Date | Durée |
|---|---|---|---|---|
| Vision | I Built an AI Object Tracking Camera with ESP32-CAM | Marina | 2026-06-03 | 14m30 |
| Vision | ESP32-S3 Edge AI Camera On-Device Person Detection, No Cloud | IoT Journal | 2026-09-03 | 7m22 |
| Vision | Object Detection with Xiao ESP32-S3 Sense + Edge Impulse | SBPElectronics | 2026-09-08 | 5m55 |
| Audio | DIY ESP32 AI Sound Recognition, TinyML | Smart Mercury Labz | 2026-08-31 | 16m35 |
| Audio | Listening to the Earth: AI, Bioacoustics & Wild Animal Voice Engine | AGI | 2026-04-26 | 4m48 |
| Énergie | Ultra Long Battery Life for ESPHome/Arduino | Tech Dregs | 2026-03-08 | 14m37 |
| Énergie | ESP32 Deep Sleep Explained: Batteries Can Last Months | Rolling Bob | 2026-11-03 | 4m55 |
| Connectivité | Send Sensor Data Over LoRa with Meshtastic ESP32 | Shilleh | 2026-03-17 | 12m55 |

---

## Points actionnables extraits (par chantier WildNexus)

### 🎥 Vision / caméra — WILDNEXUS_DEVICE
1. **L'ESP32-S3 est non négociable pour l'edge AI** : instructions vectorielles AI+DSP intégrées.
   L'ESP32 classique « échoue sur les maths IA ». → Cohérent avec ton choix ESP32-S3 (déjà acté).
2. **Voie la plus rapide** : Edge Impulse **MobileNet v2 transfer learning** (classification personne/objet)
   et **FOMO** (détection à bounding boxes, testé sur Xiao ESP32-S3 Sense).
3. **La résolution caméra doit matcher l'entraînement** (ex. 96×96) — config `pixel_format` exacte.
4. **Le mapping des pins caméra est la 1ʳᵉ cause d'échec d'init** — spécifique à chaque board.
5. **Matrice de dépannage** : faux positifs → images d'entraînement plus variées (lumière/fond) ;
   OOM → baisser la résolution ou prendre un modèle plus petit.
6. **Workflow YOLOv8n complet** (Marina) : ~500 photos custom, 80/20 train/val, 80 epochs, ~30 min,
   confiance 0.75. ⚠️ Mais son IA tourne sur **laptop**, pas en edge — à ne pas copier tel quel :
   WildNexus exige l'inférence sur puce.
7. **Limite honnête de FOMO** : confusion pomme/orange par couleur et reflets — la qualité du
   labeling + l'éclairage font tout. Attente réaliste pour la détection d'espèces par caméra.

### 🔊 Audio / bioacoustique — NEXUS_ACOUSTIC (+ INSECTNET)
8. **Recette Edge Impulse audio éprouvée** : micro I2S numérique (INMP441) → 2 classes
   (son cible + bruit de fond) → découpe en chunks de 1 s → bloc **MFE** (FFT 512) →
   **97 % d'accuracy**. C'est exactement le pipeline à répliquer pour cris d'oiseaux/insectes.
9. **Seuil de déclenchement en code** (force du son > 90) pour réduire les faux déclenchements.
10. **Concept frontier « Chatter »** : analyse des vocalisations comme trajectoires continues
    (rythme, pitch, intensité) au lieu d'unités discrètes — piste de recherche pour INSECTNET.
11. **Validation architecture WildNexus** : TinyML bioacoustique sur ESP32-S3, détection d'appels
    en temps réel à « fractions de 1 W », jamais d'internet → déploiement à l'échelle planétaire.
    C'est mot pour mot la philosophie P0.
12. **Contexte comportemental multimodal** (audio + vision) : « la langue nécessite un contexte de
    comportement » (données OpenVid-1M). Pertinent pour la fusion caméra+micro de WildNexus.

### 🔋 Énergie / ultra-low-power — P0 (PPK2, budget énergie)
13. **Le deep sleep de l'ESP32 est « pas terrible »** (~10 µA idéal, mais le **dev board** garde
    allumés : LED d'alim, chip USB-série, régulateur → ils consomment même en deep sleep).
    Vérifier la board ET les capteurs branchés.
14. **Chiffres concrets** : radio RX ~95–100 mA, TX ~180–240 mA, deep sleep ~10 µA.
    Un capteur à 1 mA en continu fait passer la batterie de **192 jours → 58 jours**.
    Estimation : 100 mA pendant 2 s + 0,1 mA pendant 9m58 → 0,43 mA moyen → 6 mois sur 2000 mAh.
15. **RTC externe + gestion d'alim = ÷50 à ÷100 la conso de sleep** (Tech Dregs, Epson RX-8130).
    Piste sérieuse pour l'ULP WildNexus (réveil horodaté offline, sortie fréquence).
16. **Boucle canonique** : réveil → mesure → envoi → sommeil, finir le travail le plus vite possible ;
    **mémoire RTC** pour persister l'état entre les cycles.

### 📡 Connectivité — WILDMESH / LoRa
17. **Meshtastic = stack LoRa mesh prête à l'emploi** (firmware + CLI Python + web flasher).
    Canal privé + région + télémétrie, portée de plusieurs km, sans Wi-Fi/internet.
    Exemple BME280 (T°/H°/pression) → chemin le plus court pour un mesh WildNexus,
    plutôt que de rebâtir un protocole LoRa maison.

---

## Lecture transverse pour WildNexus

- **Convergence forte** : les 3 vidéos « edge » (vision + audio + bioacoustique) confirment que la
  brique de base est **ESP32-S3 + Edge Impulse + micro I2S + caméra**, le tout hors cloud.
  Rien ne contredit la cible P0 ; tout la renforce.
- **Deux écarts à retenir** : (1) le tracking caméra de Marina tourne sur laptop — l'inférence
  embarquée reste LE point dur à ne pas sous-estimer ; (2) FOMO est sensible à la couleur/éclairage,
  donc la détection d'espèces par caméra demande un dataset soigné (ta piste « entraîner sur NOS
  images » de `ai-image-detection.md` s'applique aussi ici).
- **Le budget énergie domine tout** : une fuite de 1 mA en continu divise l'autonomie par 3. Le
  travail PPK2 en cours (mesure réelle des consommations) est exactement la bonne méthode — ne
  jamais déduire d'un datasheet.

## Caveats
- 4 transcripts (Marina, Smart Mercury Labz, AGI, Rolling Bob) sont en FR via Whisper avec des
  mots mal transcrits (« objecteur »=objet, « église »=espèce/whale, « alarmée »=énergie/alimentation…).
  Les chiffres et la structure de workflow restent fiables ; les noms propres sont à revérifier.
- Fait sans web-check supplémentaire : ces points sont les dires des vidéastes, pas un fact-check
  externe. Les chiffres de conso (mA/µA) et la recette Edge Impulse sont les éléments les plus
  directement exploitables et vérifiables sur le banc.

## Routing
- Synthèse : `TEAM_Inbox/2026-11-17_dobby_synthese-veille-youtube-wildnexus.md`
- Transcripts vision/énergie/LoRa : `03_WILDNEXUS/WILDNEXUS_DEVICE/99_REFERENCES/`
- Transcripts audio : `03_WILDNEXUS/NEXUS_ACOUSTIC/99_REFERENCES/`
