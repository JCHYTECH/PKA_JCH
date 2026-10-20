# Brief Recherche — [[Furet]] 🦡
**Mandaté par :** [[Dobby]] 🦉  
**Date :** 2026-06-01  
**Objet :** Analyse faisabilité DIY du générateur de sons d'oiseaux mixikid

---

## Contexte

JCH a repéré sur Instagram un projet de **mixikid** (Aaron) : un générateur électronique capable de reproduire le chant de n'importe quel oiseau avec 3 potentiomètres (pitch, speed, croakiness). Le post Instagram : https://www.instagram.com/reel/DYf801IuBy4/

La question de JCH : **peut-on le faire en DIY ou dépend-on du PCB custom / composants propriétaires de mixikid ?**

## Spécifications techniques connues

| Élément | Détail |
|---------|--------|
| **Cœur** | Electro-Smith **Daisy Seed** — STM32 H7 (ARM Cortex-M7, 480 MHz) + codec audio dédié (AK4556, 24-bit 192kHz) |
| **Contrôles** | 3 potentiomètres 10kΩ — pitch, speed, croakiness |
| **Audio out** | Line level, adaptable instrument/modular |
| **PCB** | PCB custom conçu avec l'IA Flux (text-to-PCB) |
| **Firmware** | Basé sur libDaisy / DaisySP (librairie DSP open-source Electro-Smith) |

## Sources disponibles

- **Site Daisy Seed officiel** : https://daisy.audio/hardware/Seed/ — module DSP embeddé, en vente ~30$
- **GitHub DaisySeedProjects** : https://github.com/bkshepherd/DaisySeedProjects — projets hardware/software communautaires
- **Guide DIY démarrage** : https://diyelectromusic.com/2024/12/18/getting-started-with-daisy-seed/
- **Forum Electro-Smith** : https://forum.electro-smith.com/
- **Vidéo Facebook détaillée** : https://www.facebook.com/61587439861111/videos/1675174480709861/ — confirme les 3 potards 10kΩ
- **Patreon mixikid** : https://www.patreon.com/cw/mixikid/membership — fichiers projet (schémas, CAD, PCB, code)
- **TikTok** : https://www.tiktok.com/@mixikid.com/video/7641385734238293266
- **YouTube mixikid** : https://www.youtube.com/channel/UCixKSOPKPx_SWT9oNJON8tg

## Questions de recherche pour [[Furet]]

1. **Daisy Seed — disponibilité et alternatives**
   - Le Daisy Seed est-il disponible à l'achat (Electro-Smith shop, Mouser, DigiKey) ? Prix ?
   - Existe-t-il des alternatives open-source ou moins chères ? (Teensy 4.0 + Audio Shield, ESP32 + codec I2S, Raspberry Pi Pico + PCM5102)
   - Quelles sont les dépendances logicielles ? (libDaisy, DaisySP, DaisyDuino, Pure Data, Max/MSP)

2. **PCB custom vs breadboard**
   - Le PCB custom de mixikid est-il indispensable ou un montage breadboard/protoboard est-il viable ?
   - Le PCB a été généré par Flux (text-to-PCB) — peut-on reproduire cette approche ?
   - Y a-t-il des fichiers open-source (Gerber, schémas) disponibles pour un projet similaire sur GitHub ?

3. **Firmware / code**
   - Le code de mixikid est-il open-source (Patreon, GitHub) ?
   - Existe-t-il des projets open-source équivalents qu'on pourrait adapter ?
   - Quelle est la complexité DSP pour la synthèse de chants d'oiseaux ? (synthèse granulaire, modélisation physique, lecture d'échantillons ?)

4. **Faisabilité DIY globale**
   - Niveau de compétence requis (soudure, programmation DSP, conception PCB)
   - Coût total estimé (BOM) pour une version DIY
   - Temps de développement estimé
   - Option recommandée : DIY from scratch, fork d'un projet existant, ou achat du kit mixikid ?

5. **Pertinence pour WILDNEXUS / BirdNET-Pi**
   - Ce dispositif pourrait-il servir de leurre acoustique terrain ?
   - Comparaison avec la sortie audio du RPi BirdNET-Pi (qualité, latence, portabilité)
   - Intérêt pour du playback d'espèces cibles sur le terrain ?

## Format de restitution

Rapport de recherche structuré → `TEAM_Inbox/2026-06-01_furet_mixikid_bird_synth_diy.md`

## Délai

Dès que possible — JCH attend cette analyse pour décider s'il investit dans le kit mixikid ou lance un fork DIY.
