# Rapport de Recherche — [[Furet]] 🦡
**Mandaté par :** [[Dobby]] 🦉 | **Date :** 2026-06-01  
**Objet :** Faisabilité DIY du générateur de sons d'oiseaux mixikid

---

## Verdict

**DIY faisable — mais le code DSP de synthèse aviaire de mixikid est derrière un paywall Patreon.** On peut construire le hardware nous-mêmes avec des composants standards. Pour le firmware, deux options : écrire notre propre synthèse DSP (avec libDaisy open-source) ou adapter des projets open-source existants. On n'est pas prisonniers de son PCB custom.

---

## 1. Daisy Seed — disponibilité et prix

| Vendeur | Pays | Notes |
|---------|------|-------|
| **electro-smith.com** | US (direct) | Prix officiel ~$29.95 |
| **Thonk** (thonk.co.uk) | UK | ~£25 |
| **Electrokit** (electrokit.com) | Suède | ~€30-35 |
| **SchneidersLaden** (schneidersladen.de) | Allemagne | ~€32 |
| **Signal Sounds** (signalsounds.eu) | UK | ~£24 |
| **Exploding Shed** (exploding-shed.com) | Allemagne | Version avec headers soudés |

**Livraison en Belgique :** Electrokit (Suède) et SchneidersLaden (Allemagne) sont les plus proches. Estimation : **€30-40 livré** depuis l'UE.

## 2. Alternatives matérielles

| Plateforme | Prix approx. | Audio qualité | Communauté | Verdict |
|------------|-------------|---------------|------------|---------|
| **Daisy Seed** | €30-40 | 24-bit/192kHz, codec dédié AK4556 | Forte (synth DIY) | **Recommandé** |
| **Teensy 4.0 + Audio Shield** | €35-50 | 16-bit/44.1kHz, lib PJRC mature | Très forte | Excellente alternative |
| **ESP32 + PCM5102** | €8-15 | 16-bit, I2S, DSP limité | Très forte | Budget. Projet ESP32-Birdie existe |
| **RPi Pico (RP2040)** | €5-10 | Pas de FPU | Moyenne | Inadapté pour synthèse temps réel |

**Recommandation :** Daisy Seed est le meilleur rapport qualité/prix pour la synthèse audio.

## 3. Code et firmware

### Le code de mixikid
- **PAS open-source** — accessible uniquement via Patreon (tier "Plus")
- Donne accès aux : *"Project files (sketches, CAD, PCB, code)"*

### Alternatives open-source
- **libDaisy / DaisySP** (MIT license) — librairie DSP officielle Electro-Smith
- **DaisyDuino** (MIT license) — support Arduino pour Daisy Seed
- **ML_SynthTools** — librairie multi-plateforme (Daisy, Teensy, ESP32, Pico)
- **bkshepherd/DaisySeedProjects** — collection projets hardware+software

**Conclusion firmware :** La partie spécifique « synthèse aviaire » est la vraie valeur de mixikid. Le reste est standard et open-source.

## 4. PCB custom vs breadboard

- Daisy Seed a des headers 2.54mm → parfait pour breadboard
- Circuit simple : Daisy Seed + 3 potards 10kΩ + jack 3.5mm + alim USB
- PCB de mixikid généré par Flux (IA text-to-PCB) — reproductible
- **Prototypage breadboard viable**, PCB optionnel pour la version finale

## 5. BOM estimé

| Composant | Prix approx. |
|-----------|-------------|
| Daisy Seed (headers soudés) | €35 |
| 3x potentiomètre 10kΩ | €3 |
| Jack audio 3.5mm | €2 |
| Breadboard + jumpers | €8 |
| Boîtier (impression 3D ou alu) | €10-20 |
| Câble USB-C | €5 |
| **Total** | **€63-73** |

## 6. Pertinence WILDNEXUS / BirdNET-Pi

| Aspect | Daisy Seed synth | RPi BirdNET-Pi |
|--------|-----------------|----------------|
| **Portabilité** | Excellente (poche) | Faible |
| **Latence audio** | Très basse (DSP temps réel) | Variable |
| **Qualité audio** | 24-bit/192kHz | 16-bit |
| **Autonomie** | Excellente (USB power bank) | Faible |
| **Usage terrain** | Leurre acoustique idéal | Reconnaissance seulement |

## Recommandation finale

**Option A — Patreon + kit (~€90, 2-3 sem.)**
Accès au code/schémas, dépendance créateur.

**Option B — DIY from scratch (~€70, 4-8 sem.)**
Daisy Seed + libDaisy, souveraineté totale, courbe DSP.

**Option C — Hybride (recommandé) (~€80, 3-5 sem.)**
1 mois Patreon pour aspirer specs + code, construire sur breadboard, forker/adapter.

👉 **Conseil [[Furet]] : Option C.** Un mois de Patreon (€5-10) pour voir le code, puis décider si on fork ou on reconstruit.
