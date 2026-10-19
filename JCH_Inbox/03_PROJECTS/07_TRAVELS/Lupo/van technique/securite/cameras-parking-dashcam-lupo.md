# Caméras Parking + Dashcam — Lupo 🐺
> Dobby 🦉 — 2026-10-13 (rév. 3 — livraison complète ; reste le montage)
> Projet : 11_IOT / Vanlife (deadline 01/11) × 07_TRAVELS
> **Statut :** livré le 13/10 (dashcam + OEM bracket + kit hardwire + rallonge 10/15 m) — reste le montage (microSD reportée)

---

## 1. Contexte & contraintes

| Contrainte | Implication |
|-----------|-------------|
| Van = **Westfalia Kelsey 2026** (Ford Transit Custom Tourneo V710, 2.0 EcoBlue 170ch 4×4, **5,45 m LWB**) | Câble arrière long, hayon + attelage porte-vélo |
| **Vue arrière obstruée par le mobilier** | Rétroviseur intérieur inutilisable → rétroviseur numérique |
| **Caméra de recul d'usine masquée par le porte-vélo** | Caméra arrière **haut sur hayon** |
| **Radars avant trop prudents** | Besoin de **voir** le pare-chocs avant → caméra de pare-chocs |
| Dashcam / preuve | Rien d'usine n'enregistre → enregistrement avant + arrière |

---

## 2. Solution retenue — Wolfbox G900 TriPro **Bumper** (tout-en-un)

**Une seule unité, 3 caméras, 1 miroir 12" :**

1. **Avant 4K** — capteur Sony **IMX678** (STARVIS 2) au pare-brise → dashcam preuve.
2. **Arrière 2.5K** — étanche, montage extérieur **haut du hayon** → recul + vue permanente (au-dessus du porte-vélo).
3. **Pare-chocs avant 1080P** — montée sur la **calandre** → voir le sol/bout du van (les radars sont trop prudents).

- Assistance recul (3 niveaux + lignes au doigt), mode parking (hardwire), boucle, G-sensor, GPS, Wi-Fi 5,8 GHz, commande vocale, écran 12" IPS splitté.
- **⚠️ Prendre la version « Stoßfänger » (pare-chocs), PAS « Kabinen » (habitacle).**

*(Existant)* **Reolink Argus MagiCam** — conservée en caméra de **sécurité/bivouac**.

> Comparaison antérieure : G840S (2 canaux) + caméra de grille séparée remplacés par ce G900 TriPro Bumper, plus intégré et capteurs supérieurs (arrière 2.5K vs 1080p, avant STARVIS 2).

---

## 3. Liste d'achat consolidée — statut de réception (13/10)

| # | Élément | Réf | Qté | Prix indicatif | Statut |
|---|---------|-----|-----|----------------|--------|
| 1 | **Wolfbox G900 TriPro Bumper** (3 canaux, miroir 12") | de.wolfbox.com — « G900TriPro Stoßfänger-Version » | 1 | **326–466 €** (acheté 378 €) | ✅ Reçu 13/10 |
| 2 | **Wolfbox OEM bracket** (support rétro d'origine) | Wolfbox | 1 | — | ✅ Reçu 13/10 |
| 3 | **Kit hardwire G900TriPro** (mode parking) | Wolfbox « Multifunktionales Hardwire-Kit für G900TriPro » | 1 | ~25 € | ✅ Reçu 13/10 |
| 4 | **Rallonge câble caméra arrière 33/50 ft (10/15 m)** | Wolfbox — pour G840S/G900/G850PRO/G840H | 1 | ~28 € | ✅ Reçue 13/10 |
| 5 | **microSD High Endurance 256 Go** (dashcam) | SanDisk / Samsung PRO Endurance | 1 | ~40 € | ⏳ Plus tard (JC) |
| 6 | *(option)* Filtre CPL anti-reflet | Wolfbox — G840S/G850/G900 | 1 | ~21 € | ⏳ Optionnel |

**Reçu au 13/10 :** dashcam + OEM bracket + kit hardwire + rallonge 10/15 m. **Reste :** microSD (achat plus tard).

> ⚠️ microSD dashcam **séparée** de la Samsung PRO Endurance 256 Go du RPi 5 (HA OS).

---

## 4. Plan de montage

### 4.1 Caméra arrière — HAUT du hayon (au-dessus du porte-vélo)
- **Emplacement :** haut du hayon, centrée, sous la ligne de toit (zone feu stop), **inclinée ~35–45° vers le bas**.
- **Pourquoi haut :** dégage le porte-vélo (la caméra d'usine, basse, est masquée). Vue plongeante = bon repère pour reculer.
- **Câble :** passe-câble du hayon → charnière → **plafond** → miroir avant. **5,45 m de van → la rallonge 10/15 m est reçue.**

### 4.2 Caméra de pare-chocs avant (1080P) — calandre
- **Emplacement :** calandre Transit Custom, décentrée, **inclinée vers le sol** (voir le sol à 0,5–2 m + les ailes).
- **⚠️ Éviter le radar ADAS / capteurs d'origine** (souvent derrière le badge ou la grille basse).
- Câble : traverse le compartiment moteur → passe-câble → tableau de bord → miroir.

### 4.3 Miroir + caméra avant 4K
- Miroir 12" fixé via **bracket OEM** sur le support d'origine du rétroviseur ; caméra avant collée en haut du pare-brise.
- **Kit hardwire** sur circuit **ACC (batterie moteur)** via fusible tap, **coupure basse tension** pour le mode parking.

### 4.4 Règle électrique Lupo (deux réseaux)
- **ACC / batterie moteur** → dashcam (hardwire). S'éteint à l'arrêt (sauf mode parking, protégé).
- **Cellule (CBE / LiFePO4 100 Ah)** → NE PAS brancher la dashcam ici.
- *(Réf. Reolink : `camera-reolink-argus-magicam-lupo.md`)*

---

## 5. Points d'attention

- **Variante** : vérifier « Stoßfänger » (pare-chocs), pas « Kabinen » (habitacle).
- **IP caméra pare-chocs** : **IP67 confirmé** (JC, 06/10) — étanche à la poussière et à l'immersion temporaire, adapté au montage extérieur sur calandre.
- **Longueur câbles** : arrière 5,45 m → rallonge 10/15 m reçue ; pare-chocs → vérifier la longueur fournie.
- **Porte-vélo** : vérifier le débattement du hayon vélo monté.
- **ADAS** : ne jamais recouvrir radar/caméra d'origine.

---

## 6. Prochaines étapes

1. ~~Commander~~ ✅ tout reçu (dashcam + OEM bracket + kit hardwire + rallonge). Reste : microSD (achat plus tard).
2. Monter : arrière haut hayon → pare-chocs calandre → miroir/dashcam → câblage ACC (deadline 01/11).
3. `hardware-state.md` et `etat-projets.md` mis à jour (réception 13/10).

*Source : discussion Dobby ↔ JC du 06/10/2026 + de.wolfbox.com. Réf. fiche van : `Lupo Itself/OLDIES/achat-van/fiche-technique-lupo-kelsey.md`.*
