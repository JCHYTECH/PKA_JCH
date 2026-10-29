---
date: 2026-05-23
source: chat-ai
domain: electronics
tags: [lipo, esp32-cam, alimentation, batteries, trail-cam, wildmesh]
status: raw
---

# Batteries — Discussion ESP32-CAM

## Piles crayon AA les plus puissantes

**Lithium non-rechargeable (meilleur absolu)**
- Energizer Ultimate Lithium L91, Energizer Advanced Lithium
- ~3000 mAh, tension initiale ~1,8V
- Excellentes sous forte charge, tiennent jusqu'à −40°C, stockage 20 ans

**NiMH haute capacité (rechargeable)**
- Eneloop Pro (2550 mAh), Varta Ready2Use (~2100 mAh)
- Tension nominale 1,2V — légèrement inférieure
- Meilleur rapport coût/usage sur le long terme

**Alcalines premium**
- Duracell Optimum, Energizer Max
- ~2500–2800 mAh en décharge lente, chutent fortement sous forte charge

---

## ESP32-CAM alimenté par piles AA

**Alimentation**
- L'ESP32-CAM a besoin de 5V en entrée (ou 3,3V direct)
- 2x AA lithium (~3,6V) → insuffisant sans boost converter
- 3x AA lithium (~5,4V) → fonctionne directement sur pin 5V
- 4x AA + buck regulator 5V → plus propre
- Consommation réelle : 150–350 mA (WiFi + caméra)
- Autonomie estimée : 8–15h en streaming continu avec 3x L91

**Capacités vidéo (MJPEG uniquement — pas de H.264)**

| Mode | Résolution | FPS réaliste |
|---|---|---|
| Streaming WiFi | QVGA (320×240) | 25–30 fps |
| Streaming WiFi | VGA (640×480) | 15–20 fps |
| Enregistrement SD | QVGA | 10–15 fps |
| Photo timelapse | jusqu'à 1600×1200 | N/A |

**Limites**
- SD + WiFi + caméra simultanément → conflits bus SPI
- RAM limitée (520KB interne, 4MB PSRAM selon version)
- Chaleur sous charge soutenue

**Cas d'usage pertinents**
- Trail cam / surveillance terrain (PIR + réveil sur interruption)
- Streaming live spot (WiFi local, MJPEG navigateur)
- Timelapse (très adapté, faible consommation)
- Nœud WILDMESH léger (attention bus SPI partagé [[LoRa]])

---

## Batterie LiPo minimale pour ESP32-CAM

**Contrainte principale**
Pics de courant jusqu'à ~500mA sur transmissions WiFi — le taux de décharge (C-rating) est aussi important que la capacité.

**Options par taille**

| Format approx. | Capacité | Commentaire |
|---|---|---|
| ~4×20×30mm | 150–200 mAh | Risqué sur pics WiFi |
| ~5×25×35mm | 300–400 mAh | Minimum raisonnable |
| ~6×30×40mm | 500–600 mAh | Confortable |

Minimum pratique : **400–500 mAh**

**Li-ion 18350** : 18×35mm, 700–900 mAh — tient bien les pics

**Circuit associé obligatoire**
- LDO 3,3V (AMS1117) ou boost converter 5V (MT3608, TPS61023)
- Module de charge TP4056 pour recharger

**Recommandations**
- Timelapse / duty cycle faible : LiPo 500 mAh suffit
- Streaming continu : ne pas descendre sous 1000 mAh

---

## Fabricants et prix LiPo 500 mAh

| Source | Prix unitaire approx. | Remarque |
|---|---|---|
| AliExpress (générique) | 1–3 € | Qualité/protection variable |
| eBay.de (Tewaycell) | ~6,50 € | Connecteur PH 2.0 ou Molex, expédié DE |
| Adafruit 1578 | ~$6,50 USD | Protection intégrée fiable, JST-PH 2mm |
| LiPol Battery Co. | Sur devis | MOQ 5 pièces, certifié IEC62133/UN38.3 |

**Connecteur standard à viser : JST-PH 2mm**

Achat recommandé pour la Belgique : **Adafruit via Mouser Europe ou DigiKey Europe** (pas de douane, livraison rapide).

**Points d'attention**
- Vérifier circuit de protection intégré (coupure surcharge/sur-décharge)
- Courant de décharge continu ≥ 1C (≥ 500 mA) pour tenir les pics WiFi

---

## LP-E17 (Canon R10) comme alimentation ESP32-CAM ?

**Specs**
- Tension nominale : 7,2V
- Capacité : 1040 mAh → ~7,5 Wh
- Connecteur propriétaire Canon

**Problèmes**
- Tension trop élevée → buck converter obligatoire (MP1584, LM2596)
- Connecteur propriétaire → dummy battery adapter LP-E17 (~5–8€ AliExpress) requis
- Volume supérieur à une LiPo plate équivalente

**Atout**
- Énergie totale ~7,5 Wh ≈ 4× une LiPo 500 mAh 3,7V (1,85 Wh)

**Verdict** : faisable en prototype de fortune si batterie spare disponible. Pas optimal pour solution définitive — une LiPo 1000–2000 mAh 3,7V + TP4056 reste plus cohérente.
