# WildNexus — Budget P0

**Version :** v0.4
**Date :** 2026-06-30 (mise à jour avec achats réels post-Juin)
**Statut :** Enveloppe ferme — 1 000 € maximum
**Owner :** [[Bruno]]

## 1. Contrainte

Enveloppe globale P0 fixée à **1 000 €** — volontairement serrée pour forcer la créativité et les arbitrages. Tout dépassement est bloquant sauf décision explicite de JCH.

> ⚠️ Le budget existant v0.1 estimait un scénario frugal à 10 kEUR. La cible 1 000 € impose des compromis identifiés ci-dessous. Certains de ces compromis créent un **risque de médiocrité** sur des critères qualité — ils sont signalés explicitement.

## 2. Périmètre retenu à 1 000 €

| Choix structurant | Décision |
|-------------------|---------|
| Nombre de nœuds | **2 nœuds** (au lieu de 3–5 prévu initialement) |
| PCB | **DevKit + breakout boards** — pas de PCB dédié P0 |
| FTO / licence externe | **Analyse interne uniquement** — pas de conseil IP externe |
| Dataset IA | **Terrain JCH uniquement** — pas de dataset commercial |
| Déplacements EVT | **Belgique locale** — pas de déplacement longue distance |

## 3. Suivi des achats réels (2026-06-30)

### Commandes reçues

| Commande | Fournisseur | Montant | Date réception | Composants clés |
|----------|------------|---------|----------------|-----------------|
| Mouser #39411684 | Mouser | ~100€ | ✅ Juin | PPK2 (inclus ici ou séparé) |
| ESP32-S3-DevKitC-1 ×2 | Amazon MiMiU | 21,98€ | ✅ 10/06 | MCU P0 |
| Nordic PPK2 | Mouser | ~100€ | ✅ Juin | Mesure conso — non négociable |
| ESP32-CAM OV2640 (avec caméra) ×2 | Hailege Amazon.de | ~25€ | ✅ 21/06 | Dev DVP |
| ESP32-CAM (cartes seules) ×4 | — | — | ✅ 23/06 | Debug ESP32 |
| OV5640 DVP M12 ×5 | Camemake.eu + AliExpress | ~30€ | ✅ 12-24/06 | Caméra finale P0 |
| USB-C TTL FT232RL ×3 | AZDelivery Amazon | 9€ | ✅ 21/06 | Debug serial |
| Mouser #39492997 | Mouser | 128,20€ | ✅ Juin | MEMS, IR 940nm, PIR, buck, BME688, SHT31, antennes, dissipateurs |
| Miuzei Starter Kit | Amazon | ~35€ | ✅ 10/06 | 235 composants, breadboard |
| **Sous-total reçu** | | **~479€** | | |

### En attente de commande

| Commande | Fournisseur | Montant estimé | Statut | Composants clés |
|----------|------------|----------------|--------|-----------------|
| Panier Mouser restant (11 composants) | Mouser | ~279€ | ⏳ À commander | LoRa SX1262/RAK3172, connecteurs, passifs BOM |
| **Sous-total en attente** | | **~279€** | | |

### Récapitulatif

| Bloc | Montant |
|------|--------:|
| Composants reçus | ~479€ |
| Panier Mouser restant | ~279€ |
| **Total engagé/prévu** | **~758€** |
| Enveloppe | 1 000€ |
| **Réserve restante** | **~242€** |

> ✅ Le projet reste sous enveloppe avec une réserve confortable de ~242€.

## 4. Ventilation théorique des 1 000 € (v0.3 — plan initial)

### Électronique — 2 nœuds complets

| Poste | Unité | × 2 nœuds | Sous-total |
|-------|------:|----------:|-----------:|
| ESP32-S3 DevKit | ~12 € | × 2 | ~24 € |
| OV5640 M12 DVP | ~20 € | × 2 | ~40 € |
| Lentille M12 IR-corrigée f/1.8 | ~35 € | × 2 | ~70 € |
| LED IR 940 nm × 4 | ~8 € | × 2 | ~16 € |
| LoRa RAK3172 | ~12 € | × 2 | ~24 € |
| microSD 16 GB industrielle | ~12 € | × 2 | ~24 € |
| 2× holder 4× AA (4S2P) | ~2 € | × 2 | ~4 € |
| Régulateur buck TPS62840 | ~2 € | × 2 | ~4 € |
| Boîtier Hammond IP67 | ~15 € | × 2 | ~30 € |
| SHT31 (temp + humidité) | ~5 € | × 2 | ~10 € |
| PIR basse conso | ~5 € | × 2 | ~10 € |
| MOSFET, résistances, capacités, connecteurs | ~25 € | × 2 | ~50 € |
| **Sous-total électronique** | | | **~307 €** |

### PCB et assemblage — ~55 €
### Outillage et banc de test — ~180 € (inclut PPK2)
### Frais annexes — ~180 €
### Réserve — ~239 €

## 5. Risques de médiocrité — signalement explicite

| # | Compromis | Impact qualité | Seuil d'alerte |
|---|-----------|---------------|----------------|
| ⚠️ M1 | **Lentille** : si budget force < 20 € (AliExpress non IR-corrigé) | Vision nocturne floue au-delà de 2 m | Ne pas descendre sous 30 € / lentille. Lensation reste la cible à 35 €. |
| ⚠️ M2 | **2 nœuds au lieu de 3–5** | Un seul nœud de secours terrain | Acceptable P0 si objectif = proof of concept |
| ⚠️ M3 | **DevKit au lieu de PCB dédié** | Encombrement boîtier, fragilité connecteurs | Acceptable P0 uniquement — tout PCB P1 doit être dédié |
| ⚠️ M4 | **OV5640 vs IMX462** | Vision nocturne plafonnée à ~3–5 m | Décision architecture P0 assumée (ADR-002) |
| ⚠️ M5 | **Pas de Nordic PPK2** | Impossible de mesurer le deep sleep | PPK2 **non négociable** — ✅ acquis |

## 6. Règle de dépassement

Tout achat individuel > 50 € doit être signalé à JCH avant commande.
Si le total projeté dépasse 900 €, stopper et arbitrer avant de commander le reliquat.

## 7. Ce qui sort du budget 1 000 €

| Poste exclu | Estimation | Condition de réintégration |
|-------------|----------:|---------------------------|
| Avis FTO / IP externe | 500–3 000 € | Si partenariat industriel ou levée envisagée |
| PCB dédié P0 (au lieu de DevKit) | 200–400 € | Si DevKit incompatible avec boîtier IP67 |
| 3e nœud complet | ~175 € | Si les 2 nœuds tombent en panne simultanément terrain |
| Dataset IR externe | 200–1 000 € | Si dataset terrain insuffisant pour entraîner le classifieur |

---

*Mis à jour v0.4 le 2026-06-30 — suivi des achats réels ajouté, ventilation théorique conservée en §4 pour référence.*
