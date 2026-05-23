# WildNexus — Budget P0

**Version :** v0.2
**Date :** 2026-05-18
**Statut :** Enveloppe ferme — 1 000 € maximum
**Owner :** Bruno

## 1. Contrainte

Enveloppe globale P0 fixée à **1 000 €** — volontairement serrée pour forcer la créativité et les arbitrages. Tout dépassement est bloquant sauf décision explicite de JCH.

> ⚠️ Le budget existant v0.1 estimait un scénario frugal à 10 kEUR. La cible 1 000 € impose des compromis identifiés ci-dessous. Certains de ces compromis créent un **risque de médiocrité** sur des critères qualité — ils sont signalés explicitement.

---

## 2. Périmètre retenu à 1 000 €

| Choix structurant | Décision |
|-------------------|---------|
| Nombre de nœuds | **2 nœuds** (au lieu de 3–5 prévu initialement) |
| PCB | **DevKit + breakout boards** — pas de PCB dédié P0 |
| FTO / licence externe | **Analyse interne uniquement** — pas de conseil PI externe |
| Dataset IA | **Terrain JCH uniquement** — pas de dataset commercial |
| Déplacements EVT | **Belgique locale** — pas de déplacement longue distance |

---

## 3. Ventilation des 1 000 €

### Électronique — 2 nœuds complets

| Poste | Unité | × 2 nœuds | Sous-total |
|-------|------:|----------:|-----------:|
| ESP32-S3 DevKit | ~12 € | × 2 | ~24 € |
| OV5640 M12 DVP (Arducam) | ~20 € | × 2 | ~40 € |
| Lentille M12 IR-corrigée f/1.8 | ~35 € | × 2 | **~70 €** |
| LED IR 850 nm × 4 | ~8 € | × 2 | ~16 € |
| LoRa RAK3172 ou Murata 1SJ | ~12 € | × 2 | ~24 € |
| microSD 16 GB industrielle | ~12 € | × 2 | ~24 € |
| 2× 18650 LiFePO4 | ~12 € | × 2 | ~24 € |
| Panneau solaire 6V 2W + CN3791 | ~12 € | × 2 | ~24 € |
| Boîtier Hammond IP67 | ~15 € | × 2 | ~30 € |
| SHT31 (temp + humidité) | ~5 € | × 2 | ~10 € |
| PIR basse conso | ~5 € | × 2 | ~10 € |
| MOSFET, résistances, capacités, connecteurs | ~25 € | × 2 | ~50 € |
| **Sous-total électronique** | | | **~346 €** |

### PCB et assemblage

| Poste | Montant |
|-------|--------:|
| PCB JLCPCB 5 pcs (minimum lot) | ~40 € |
| Frais de port et douane EU | ~15 € |
| **Sous-total PCB** | **~55 €** |

### Outillage et banc de test

| Poste | Montant |
|-------|--------:|
| Nordic PPK2 (mesure courant deep sleep — critique ADR-005) | ~100 € |
| Multimètre / alimentation de labo si absent | ~50 € |
| Câbles, adaptateurs, sangle terrain UV | ~30 € |
| **Sous-total outillage** | **~180 €** |

### Frais annexes

| Poste | Montant |
|-------|--------:|
| Ports et frais de livraison composants | ~40 € |
| Consommables terrain (silica gel, joints, vis) | ~20 € |
| Marge casse et reprise (1 composant/catégorie) | ~120 € |
| **Sous-total annexes** | **~180 €** |

### Réserve imprévus

| Poste | Montant |
|-------|--------:|
| Réserve 24 % | **~239 €** |

---

### Total

| Bloc | Montant |
|------|--------:|
| Électronique 2 nœuds | ~346 € |
| PCB | ~55 € |
| Outillage | ~180 € |
| Frais annexes | ~180 € |
| Réserve | ~239 € |
| **TOTAL** | **~1 000 €** |

---

## 4. Risques de médiocrité — signalement explicite

| # | Compromis | Impact qualité | Seuil d'alerte |
|---|-----------|---------------|----------------|
| ⚠️ M1 | **Lentille** : si budget force < 20 € (AliExpress non IR-corrigé) | Vision nocturne floue au-delà de 2 m — objectif qualité piège photo **non atteint** | Ne pas descendre sous 30 € / lentille. Lensation reste la cible à 35 €. |
| ⚠️ M2 | **2 nœuds au lieu de 3–5** | Un seul nœud de secours terrain — pas de triangulation, pas de redondance EVT | Acceptable P0 si objectif = proof of concept, pas déploiement terrain réel |
| ⚠️ M3 | **DevKit au lieu de PCB dédié** | Encombrement boîtier, fragilité connecteurs, fiabilité terrain moindre | Acceptable P0 uniquement — tout PCB P1 doit être dédié |
| ⚠️ M4 | **OV5640 vs IMX462** | Vision nocturne plafonnée à ~3–5 m quelle que soit la puissance LED | Décision architecture P0 assumée — flaggée dès l'ADR-002. IMX462 = P1. |
| ⚠️ M5 | **Pas de Nordic PPK2** | Impossible de mesurer le courant deep sleep avec précision → critère ADR-005 non vérifiable | Nordic PPK2 est **non négociable** — il doit rester dans le budget. |

---

## 5. Règle de dépassement

Tout achat individuel > 50 € doit être signalé à JCH avant commande.
Si le total projeté dépasse 900 €, stopper et arbitrer avant de commander le reliquat.

---

## 6. Ce qui sort du budget 1 000 €

Ces postes sont **exclus** de l'enveloppe et nécessitent une décision séparée si requis :

| Poste exclu | Estimation | Condition de réintégration |
|-------------|----------:|---------------------------|
| Avis FTO / PI externe | 500–3 000 € | Si partenariat industriel ou levée envisagée |
| PCB dédié P0 (au lieu de DevKit) | 200–400 € | Si DevKit s'avère incompatible avec le boîtier IP67 |
| 3e nœud complet | ~175 € | Si les 2 nœuds tombent en panne simultanément terrain |
| Dataset IR externe | 200–1 000 € | Si dataset terrain insuffisant pour entraîner le classifieur |
