# BirdNET-Pi — Liste d'achat installation extérieure

**Date :** 16 mai 2026  
**Configuration :** [[Raspberry Pi 5]] + BirdNET-Pi (fork Nachtzuster)  
**Localisation :** Esneux-Tilff, Belgique (50.55°N, 5.57°E)

---

## 1. Microphone — Clippy EM272 Mono (TRS)

- **Produit :** Clippy EM272 Mono Microphone (capsule Primo EM272Z1)
- **Type :** Omnidirectionnel, lavalier, bruit propre 14 dBA
- **Connecteur :** Jack 3.5 mm **TRS** (2 bandes) — NE PAS prendre la version Smart/TRRS
- **Prix :** ~£35–45
- **Fournisseur :** [micbooster.com](https://micbooster.com) (UK) ou [Veldshop](https://veldshop.nl) (Pays-Bas, livraison UE plus rapide)
- **Note :** Ajouter une bonnette anti-vent en mousse (~5€) si non incluse

## 2. Carte son USB — Adaptateur TRS

- **Produit :** UGreen USB Audio Adapter (version **TRS**, pas TRRS)
- **Prix :** ~10–15€
- **Fournisseur :** Amazon BE/FR/DE
- **ATTENTION :** Les adaptateurs TRRS (3 bandes) ne fonctionnent PAS avec les micros TRS (2 bandes). Vérifier le nombre de bandes sur la prise avant achat.

## 3. Câble rallonge USB

- **Produit :** Rallonge USB-A mâle/femelle, 1 à 2 mètres
- **Prix :** ~5€
- **Fournisseur :** Amazon ou magasin électronique
- **Obligatoire :** Ne jamais brancher la carte son directement sur le RPi — les interférences électromagnétiques du processeur dégradent le signal audio.

## 4. Boîtier étanche — Sixfab IP65 Outdoor Enclosure

- **Produit :** Sixfab IP65 Outdoor Project Enclosure for [[Raspberry Pi]]
- **Protection :** IP65 (poussière + jets d'eau)
- **Matériau :** ABS, couvercle transparent polycarbonate, joint silicone
- **Inclus :** Plaque de montage RPi, passe-câbles étanches (grommets), oreilles de fixation murale/poteau, visserie
- **Compatibilité :** [[Raspberry Pi 5]] (et tous modèles RPi)
- **Prix :** ~40–50€
- **Fournisseur :** [sixfab.com](https://sixfab.com) ou Amazon UK/EU
- **Note :** Prévoir un petit trou de drainage (1–2 mm) en bas du boîtier pour évacuer la condensation.

## 5. Alimentation extérieure

- **Option A — Chargeur USB-C :** 5V / 5A (officiel RPi 5), câble suffisamment long pour passer dans le boîtier. ~15–20€
- **Option B — PoE HAT :** Si câble Ethernet disponible en extérieur. Alimentation + réseau sur un seul câble. ~25€

---

## Récapitulatif

| Composant | Prix estimé |
|---|---|
| Clippy EM272 Mono (TRS) | ~40–50€ |
| Carte son USB TRS (UGreen) | ~10–15€ |
| Rallonge USB 1–2m | ~5€ |
| Sixfab IP65 Enclosure | ~40–50€ |
| Alimentation USB-C ou PoE | ~15–25€ |
| **Total estimé** | **~110–145€** |

---

## Notes techniques

- **Micro omnidirectionnel vs directionnel :** Pour BirdNET-Pi, un micro omni est préférable. Les oiseaux chantent de toutes les directions et un micro directionnel n'apporte pas d'avantage réel dans ce contexte.
- **Interférences WiFi :** La capsule EM272 peut capter des interférences de transmetteurs WiFi (ex: Rode Wireless Go). Si problème, éloigner le micro de la source WiFi.
- **Sensibilité [[BirdNET]] :** Configuration recommandée — Sigmoid Sensitivity : 1.25, Overlap : 0.5.
- **Interface web :** Accessible depuis n'importe quel navigateur sur le réseau local à `http://tkajch.local`
