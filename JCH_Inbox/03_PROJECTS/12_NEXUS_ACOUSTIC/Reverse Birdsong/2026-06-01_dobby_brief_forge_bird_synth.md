# Brief Construction — [[Forge]] 🦦
**Mandaté par :** [[Dobby]] 🦉 | **Date :** 2026-06-01  
**Objet :** Prototype DIY Bird Sound Generator (projet mixikid)  
**Réf. interne :** PKA-WN-BIRD-001

---

## 1. Ce qu'on essaie d'accomplir

Construire un prototype de **générateur de sons d'oiseaux** portable — un petit boîtier à 3 potards capable de synthétiser des chants d'oiseaux. Usage cible : leurre acoustique de terrain pour WILDNEXUS (playback d'espèces).

---

## 2. Base technique

| Élément | Valeur |
|---------|--------|
| **Cœur** | Electro-Smith **Daisy Seed** — STM32 H7 480MHz + codec AK4556 24-bit/192kHz |
| **Contrôles** | 3× potentiomètre 10kΩ **linéaire (B10k)** → pitch, speed, croakiness |
| **Sortie** | Jack 3.5mm stéréo TRS line level |
| **Alim** | USB-C data (power bank ou secteur) |
| **Firmware** | DaisyDuino (Arduino) ou libDaisy (C++ bare metal), les deux MIT |

---

## 3. Référence externe — projet mixikid

Le créateur **mixikid** (Aaron) a déjà réalisé ce projet :

| Plateforme | Lien |
|-----------|------|
| Instagram (post original) | https://www.instagram.com/reel/DYf801IuBy4/ |
| Facebook (détails techniques) | https://www.facebook.com/61587439861111/videos/1675174480709861/ |
| Patreon (code + schémas + CAD + PCB) | https://www.patreon.com/cw/mixikid/membership |
| TikTok | https://www.tiktok.com/@mixikid.com/video/7641385734238293266 |
| YouTube | https://www.youtube.com/channel/UCixKSOPKPx_SWT9oNJON8tg |

**Point clé :** le code DSP de mixikid est derrière un paywall Patreon (tier "Plus", ~€5-10/mois). Tout le hardware — Daisy Seed, libDaisy/DaisySP (MIT), circuit — est standard. On peut construire sans lui. Option : 1 mois de Patreon pour aspirer les specs, à valider avec JCH.

Rapport [[Furet]] complet : `TEAM_Inbox/2026-06-01_furet_mixikid_bird_synth_diy.md`

---

## 4. Bon de commande — DigiKey Belgique (digikey.be)

**Port gratuit dès 50€, livraison 1-2 jours.**

| # | Article | Qté | Recherche DigiKey | Prix est. |
|---|---------|-----|-------------------|-----------|
| 1 | Daisy Seed (headers soudés) | 1 | `DAISY-SEED` | ~€28 |
| 2 | Breadboard 830 pts (MB-102, 165×55mm) | 1 | `breadboard 830` | ~€10 |
| 3 | Potentiomètre 10kΩ linéaire B10k | 3 | `potentiometer 10k linear` | ~€3 |
| 4 | Jack 3.5mm stéréo TRS panel mount | 1 | `audio jack 3.5mm stereo panel` | ~€3 |
| 5 | Fils jumper M-M (kit) | 1 | `jumper wire male male kit` | ~€6 |
| 6 | Câble USB-C data 1m (option si <50€) | 1 | `usb-c cable data` | ~€4 |

- **Total : ~€50-54 → port gratuit**
- **Plan B :** Mouser Belgique (mouser.be) ou Farnell Belgique (be.farnell.com) — même politique
- **À vérifier :** Daisy Seed version "with soldered headers", potards linéaires B10k (pas A10k), jack stéréo TRS

BC détaillé : `TEAM_Inbox/2026-06-01_BC_bird_synth_prototype.md`

---

## 5. Breadboard : dimensions et disposition

### Format : 830 points (MB-102) = 165×55mm, 63 rangées

Le Daisy Seed occupe 20 rangées. Le half-size (400 pts, 30 rangées) serait trop juste.

### Layout

```
Rail + ──────────────────────────────────────────── Rail -
       [POT1]     [POT2]     [POT3]        [JACK]
       pitch       speed      croak        L  R  G
         │           │          │           │  │  │
         ▼           ▼          ▼           ▼  ▼  ▼
    ┌──A0─────────A1─────────A2──────┐  ┌──18 19 20──┐
    │                                │  │            │
    │         DAISY SEED             │  │   ESPACE   │
    │         20 rangées             │  │   LIBRE    │
    │                                │  │            │
    └──GND───────3.3V──────USB───────┘  └────────────┘
Rail - ──────────────────────────────────────────── Rail +
```

- Potards → rail haut, ADC A0-A2, câblés GND + 3.3V
- Jack → rail bas, broches 18-20 (L, R, GND)
- Daisy Seed → centre, chevauche le canal
- Alim → USB-C direct sur Daisy Seed (pas d'alim breadboard séparée)

---

## 6. Phases de construction

### Phase 1 — Prototype breadboard
- [ ] Commander le matériel (BC section 4)
- [ ] Câbler 3 potards sur ADC + jack sur line out
- [ ] Firmware minimal : lecture ADC → DSP → audio out
- [ ] Test : son qui sort, potards qui modifient en temps réel

### Phase 2 — Synthèse aviaire
- [ ] Synthèse sur DaisySP/libDaisy : sawtooth modulé + ADSR
- [ ] Itérer vs enregistrements réels (mésange, pinson, merle)
- [ ] Objectif : 3-5 espèces reconnaissables

### Phase 3 — Package terrain
- [ ] Boîtier (impression 3D ou alu)
- [ ] Power bank USB, autonomie >8h
- [ ] Option : OLED pour nom d'espèce

---

## 7. Contraintes

- **Pas de WiFi, pas de cloud, pas de serveur** — autonome terrain
- **Pas de dépendance runtime au code mixikid**
- **Breadboard d'abord**, PCB après validation
- **Documenter** pour reproductibilité

---

## 8. Ressources techniques

| Ressource | Lien |
|-----------|------|
| DaisyDuino (MIT) | https://github.com/electro-smith/DaisyDuino |
| DaisySP (MIT) | https://electro-smith.github.io/DaisySP/ |
| Guide démarrage | https://diyelectromusic.com/2024/12/18/getting-started-with-daisy-seed/ |
| Projets communauté | https://github.com/bkshepherd/DaisySeedProjects |
| Forum Electro-Smith | https://forum.electro-smith.com/ |
| ML_SynthTools | https://audio-file.org/2024/03/16/ml_synthtools-arduino-synthesizer-library/ |

---

## 9. Restitution

- Code → `scripts/bird_synth/`
- Doc → `TEAM_Inbox/2026-06-XX_forge_bird_synth_prototype.md`
- Photos breadboard + BOM final

---

## 10. Délai

Phase 1 : 2 semaines après réception matos. Phases 2-3 : selon priorité JCH.

---

*"La complexité est un symptôme, pas une solution." — [[Forge]]*
