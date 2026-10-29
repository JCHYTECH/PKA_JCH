# ADR-013 — Couche acoustique : microphones et monitoring sonore

**Statut :** Accepté  
**Date :** 2026-06-19  
**Décideur :** Dobby 🦉 + JCH  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Portée :** P0 immédiat + upgrade path P1

---

## Contexte

La session du 2026-06-19 a démontré qu'un pipeline acoustique complet (enregistrement → segmentation → classification → manifold 3D → densité de population) est réalisable avec l'iPhone de JCH. Le micro MEMS Knowles SPH0645LM4H-B est déjà dans le BOM (A06) pour la détection d'événements sonores.

La question : ce micro suffit-il pour étendre WildNexus au monitoring acoustique passif multi-espèces (oiseaux, orthoptères, amphibiens) ?

---

## Décision

### Microphone principal — SPH0645LM4H-B (maintenu)

| Spécification | Valeur |
|---------------|--------|
| Modèle | Knowles SPH0645LM4H-B |
| SNR | 65 dB(A) → bruit équivalent 29 dB SPL |
| Bande passante | 20 Hz – 10 kHz |
| Sensibilité | −26 dBFS @ 94 dB SPL |
| Interface | I2S digital 24-bit |
| Consommation | 600 µA actif / 10 µA sleep |
| Prix | ~3.44€ (DigiKey) |

**Validation pour l'usage acoustique :**

| Scénario | Distance | Niveau reçu | Marge/bruit | Verdict |
|----------|----------|-------------|-------------|---------|
| Grillon (4.7 kHz) | 20 m | 43 dB SPL | +14 dB | ✅ |
| Merle (2-4 kHz) | 20 m | 48 dB SPL | +19 dB | ✅ |
| Mésange (4-8 kHz) | 20 m | 38 dB SPL | +9 dB | ✅ |
| Grenouille (<2 kHz) | 20 m | 48 dB SPL | +19 dB | ✅ |
| Sauterelle ultrason (>15 kHz) | — | — | — | ❌ Hors bande |
| Chauve-souris (20-80 kHz) | — | — | — | ❌ Hors bande |

### Nombre de micros par nœud : 2

Deux micros en opposition sur le boîtier (baseline ~10-15 cm selon l'orientation de montage) permettent :
- Spatialisation azimutale grossière (±4–7° à 4.7 kHz)
- Redondance (1 micro défaillant = le nœud continue de fonctionner)
- Séparation gauche/droite pour le comptage d'individus

La précision de triangulation fine vient du **maillage inter-nœuds LoRa** (baseline 50-200 m, résolution <0.1°), pas des micros intra-nœud. Le réseau fait le travail de localisation fine ; les 2 micros locaux donnent la direction immédiate.

### Upgrade path — ICS-43434 (P1)

Si le besoin ultrason émerge (sauterelles haute fréquence, chauves-souris) :

| Spécification | ICS-43434 (TDK/InvenSense) |
|---------------|---------------------------|
| Bande passante | 20 Hz – 20 kHz |
| SNR | 65 dB(A) |
| Interface | I2S (pin-compatible SPH0645LM4H-B) |
| Prix | ~5€ |

---

## Conséquences

### Impact BOM

| Item | Coût unitaire | Qté | Total |
|------|--------------|-----|-------|
| SPH0645LM4H-B (A06) | 3.44€ | 2 → 4 (2 par nœud) | +6.88€ |
| Membrane Gore-Tex acoustique | ~1€ | 2 | +2€ |
| Joint torique micro | ~0.50€ | 2 | +1€ |
| **Total ajouté par nœud** | | | **~10€** |

### Impact casing

- 2 ouvertures circulaires (Ø 5 mm) sur faces opposées du boîtier Hammond 1554A
- Membrane Gore-Tex acoustique collée derrière chaque ouverture (IP67 conservé)
- Micro soudé sur PCB flexible ou monté directement sur PCB principal face à l'ouverture
- **Pas de changement de format du boîtier** — les ouvertures s'intègrent dans les faces existantes

### Impact firmware

- Acquisition I2S dual-channel (ESP32-S3 a 2 canaux I2S natifs)
- Buffer circulaire 10s en PSRAM
- Extraction features spectrales (FFT 1024 points, 10 descripteurs) toutes les 15 minutes
- Transmission LoRa : 40 bytes par segment spectral → 1.9 KB/jour
- Stockage SD : segments audio complets 3s toutes les heures → 13 MB/jour

### Impact architecture réseau

- Chaque nœud transmet ses features spectrales horodatées + position GPS connue
- La gateway centrale agrège les features de tous les nœuds
- Le manifold 4D (UMAP) est généré en post-traitement sur le serveur PKA (M5)
- 10 nœuds × 48 segments/jour × 10 features = 14 400 points par mois → manifold interactif

---

## Alternatives considérées

| Alternative | Rejetée parce que |
|-------------|-------------------|
| Micro électret analogique + ADC externe | Complexité circuit, consommation, calibration |
| Micro ultrason dédié (Knowles SPH0655) | Surdimensionné pour P0, coût ×2 |
| 1 seul micro par nœud | Perte de la spatialisation intra-nœud, pas de redondance |
| 3-4 micros par nœud | Complexité casing, consommation I2S, gain marginal |

---

## Références

- Session 2026-06-19 — Pipeline acoustique complet sur iPhone (InsectNet)
- TEAM_Inbox/2026-06-19_dobby_arbor-densite-acoustique-orthopteres.md
- TEAM_Inbox/2026-06-19_dobby_recherche-zoom-f3-micro-bioacoustique.md
- BOM WildNexus v0.2 — A06 Knowles SPH0645LM4H-B
- SOP-10-batterie-aa-buck.md v1.1 (note dropout voltage AMS1117)
