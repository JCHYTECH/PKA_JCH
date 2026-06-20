# A1 — Nexus Acoustic
> Station bioacoustique autonome · Classification oiseaux + orthoptères + amphibiens
> Fiche produit — 2026-06-19

---

## Positionnement

Nexus Acoustic est un **produit standalone** de monitoring bioacoustique. Il ne nécessite pas de caméra WildNexus — c'est une station d'écoute autonome qui classifie les espèces à partir de leurs vocalisations. Peut fonctionner seul ou s'intégrer au réseau WildNexus pour la corrélation multimodale.

**Persona cible :** Ornithologue, bioacousticien, bureau d'études environnementales.

---

## Spécifications techniques

| Catégorie | Composant | Détail |
|-----------|-----------|--------|
| **Compute** | Raspberry Pi 5 4GB | Ou RPi 4 4GB pour version économique |
| **Audio** | 2× ICS-43434 MEMS I2S | 24-bit, 20Hz-20kHz, 65 dB SNR, stéréo |
| **Micro externe** | Jack 3.5mm TRS | Compatible micros externes (ex: LOM MikroUši) |
| **Classification** | BirdNET-Lite + InsectNet-CNN + AmphibianNet | 3 modèles parallèles |
| **Stockage** | SSD NVMe 256GB + microSD 32GB | ~200 000 segments audio étiquetés |
| **Radio** | LoRa SX1262 (optionnel) | Pour intégration réseau WildNexus |
| **Connectivité** | Wi-Fi 5 + Ethernet GbE | Dashboard local, API REST |
| **Énergie** | USB-C PD 5V/3A | Ou PoE HAT |
| **Boîtier** | Boîtier RPi + protection intempéries | Déploiement extérieur abrité |
| **Autonomie** | Secteur / Power bank | Pas de batterie intégrée (branchement requis) |

---

## Pipeline audio

```
Audio 24-bit 48kHz stéréo continu
  → Segmentation (WebRTC VAD + énergie)
  → Spectrogramme (Mel, 128 bands, 25ms window)
  → Classification BirdNET-Lite (oiseaux, 200 spp)
  → Classification InsectNet-CNN (orthoptères, 30 spp)
  → Classification AmphibianNet (amphibiens, 10 spp)
  → Post-processing (filtre confiance > 0.5, fusion temporelle)
  → Stockage (WAV segment + metadata JSON)
  → Dashboard (timeline, spectrogrammes, stats)
```

**Performance temps réel :**
- Jusqu'à 3 flux audio simultanés (stéréo = 2 canaux)
- Latence de classification : 2-3 secondes après vocalisation
- Taux de détection oiseaux : ~75-85% (BirdNET validated)
- Taux de détection orthoptères : ~65-80% (selon espèce)

---

## Dashboard acoustique

- **Spectrogramme temps réel :** visualisation du paysage sonore
- **Timeline espèces :** liste chronologique des détections avec score de confiance
- **Carte de présence :** heatmap temporelle par espèce
- **Statistiques :** richesse spécifique, abondance relative, phénologie
- **Export :** CSV, Darwin Core, segmentation WAV étiquetée
- **API REST :** intégration outils scientifiques (R, Python, QGIS)

---

## BOM estimatif

| Composant | Qté | Prix unit. | Total |
|-----------|-----|-----------|-------|
| Raspberry Pi 5 4GB | 1 | ~60.00€ | 60.00€ |
| ICS-43434 MEMS + carte breakout | 2 | ~5.00€ | 10.00€ |
| SSD NVMe 256GB | 1 | ~30.00€ | 30.00€ |
| Carte microSD 32GB | 1 | ~8.00€ | 8.00€ |
| Alim USB-C PD 5V/3A | 1 | ~12.00€ | 12.00€ |
| Boîtier extérieur IP65 | 1 | ~20.00€ | 20.00€ |
| Câble ethernet extérieur 10m | 1 | ~10.00€ | 10.00€ |
| **Total BOM** | | | **~150.00€** |

**Prix de vente cible :** 249-299€

---

## Versions

| Version | Compute | Modèles | Prix |
|---------|---------|---------|------|
| **Nexus Acoustic Lite** | RPi 4 2GB | BirdNET-Lite seulement (200 oiseaux) | ~179€ |
| **Nexus Acoustic** | RPi 5 4GB | BirdNET + InsectNet + AmphibianNet | ~249€ |
| **Nexus Acoustic Pro** | RPi 5 8GB + Coral TPU | Tous modèles + custom species training | ~399€ |

---

## Ce qui est INCLUS

- 1× station Nexus Acoustic pré-configurée (OS + modèles IA)
- 2× micros MEMS ICS-43434
- 1× SSD 256GB
- Dashboard acoustique web
- Licences modèles IA (permanentes)
- Documentation : installation, calibration, exports scientifiques

## Ce qui n'est PAS inclus

- Microphone externe (jack 3.5mm compatible, ex: LOM MikroUši Pro ~180€)
- Alimentation secteur (USB-C PD inclus, pas de batterie)
- Abonnement cloud (tout est local)

---

## Intégration WildNexus

```
Nexus Acoustic ──API REST──→ WildNexus STATION+
                              └── Corrélation caméra + audio
                              └── Événement composite multimodal
```

Une STATION+ peut interroger l'API de Nexus Acoustic pour corréler une détection caméra avec une détection audio quasi-simultanée, créant un événement composite « image + son + environnement ».

---

## Marché et concurrence

| | Nexus Acoustic | AudioMoth | BirdWeather PUC | Swift |
|---|---|---|---|---|
| **Prix** | ~249€ | ~80€ | ~250€ | ~450€ |
| **Classification** | Embarquée temps réel | Aucune (post-traitement) | Cloud (BirdNET) | Cloud |
| **Open source** | ✅ | ✅ Firmware | ❌ | ❌ |
| **Multi-taxons** | ✅ Oiseaux+Insectes+Amphibiens | ❌ | Oiseaux seulement | Oiseaux seulement |
| **Stockage** | SSD 256GB | microSD | Cloud | Cloud |
| **API locale** | ✅ REST | ❌ | ❌ | ❌ |

---

*Références : Projet bioacoustique Faune Autour, BirdNET-Go, InsectNet pipeline, ADR-013, recherche Lucio Arese 3D sonogram.*
