# S1 — WildNexus STATION
> Gateway LoRa + dashboard local · Version P1
> Fiche produit — 2026-06-19

---

## Positionnement

La STATION est le **hub local** du réseau WildNexus. Elle collecte les alertes LoRa des nœuds FIELD, stocke les données, et fournit un dashboard web accessible sans cloud. Une STATION par site, jusqu'à 50 nœuds FIELD connectés.

**Persona cible :** Gestionnaire de réserve, association naturaliste, propriétaire multi-terrains.

---

## Architecture

```
FIELD ×1..50 ──LoRa──→ STATION ──Wi-Fi/Ethernet──→ Dashboard local
                              └── LTE (optionnel) ──→ Alertes email
                              └── SSD local ──→ Export données
```

---

## Spécifications techniques

| Catégorie | Composant | Détail |
|-----------|-----------|--------|
| **Compute** | Raspberry Pi 5 4GB | Ou CM5 + carrier board |
| **Radio** | RAK3172 (SX1262) LoRa | EU868, même module que FIELD |
| **Connectivité** | Wi-Fi 5 + Ethernet GbE | Dashboard local accessible réseau |
| **LTE (option)** | SIM7080G | Backup si Wi-Fi down, alertes SMS |
| **Stockage** | SSD NVMe 256GB | Jusqu'à 2M événements, 10 000 images |
| **OS** | Raspberry Pi OS Lite | Docker pour services |
| **Dashboard** | WildNexus Dashboard (web) | Carte temps réel, timeline, alertes |
| **API** | REST locale | Export JSON/CSV, intégration outils tiers |
| **Énergie** | USB-C PD 5V/5A | Ou PoE HAT (Power over Ethernet) |
| **Boîtier** | Boîtier RPi officiel | Ou rail DIN pour installation fixe |
| **Antenne** | Antenne LoRa 868MHz extérieure | SMA, 3 dBi, à fixer en hauteur |

---

## Dashboard — Fonctionnalités

- **Carte temps réel :** position de chaque nœud FIELD, dernier événement, niveau batterie
- **Timeline :** tous les événements par nœud, filtrables par score IA, espèce, date
- **Galerie :** images téléchargées à la demande (LTE-M burst)
- **Alertes :** configurable par espèce cible, heure, niveau batterie critique
- **Export :** CSV, JSON, Camtrap-DP (standard scientifique)
- **Statistiques :** heatmap activité, tendances saisonnières
- **Admin :** provisioning nouveaux nœuds, mise à jour firmware OTA

---

## BOM estimatif

| Composant | Qté | Prix unit. | Total |
|-----------|-----|-----------|-------|
| Raspberry Pi 5 4GB | 1 | ~60.00€ | 60.00€ |
| RAK3172 + antenne | 1 | ~15.00€ | 15.00€ |
| SSD NVMe 256GB | 1 | ~30.00€ | 30.00€ |
| Alim USB-C PD 5V/5A | 1 | ~15.00€ | 15.00€ |
| Carte microSD 32GB (OS) | 1 | ~8.00€ | 8.00€ |
| Boîtier + câbles | 1 | ~10.00€ | 10.00€ |
| **Total BOM** | | | **~138.00€** |

**Prix de vente cible :** 249-299€

---

## Ce qui est INCLUS

- 1× STATION pré-configurée (OS + services Docker)
- 1× antenne LoRa 868MHz extérieure (3m câble)
- 1× alimentation USB-C PD
- Dashboard web pré-installé
- Documentation : installation, configuration nœuds, export données

## Ce qui n'est PAS inclus

- Nœuds FIELD (vendus séparément)
- Abonnement LTE (optionnel)
- Écran / moniteur (dashboard accessible via navigateur)

---

## Différenciation

| | WildNexus STATION | Solutions cloud propriétaires |
|---|---|---|
| **Données** | Locales, vous les possédez | Cloud, vous les louez |
| **Coût récurrent** | 0€ (hors LTE optionnel) | Abonnement mensuel |
| **Offline** | Fonctionne sans Internet | Dépendance réseau |
| **API** | REST locale, standard ouvert | Propriétaire, limitée |
| **Vie privée** | Images ne quittent pas le site | Transit cloud tiers |

---

## Chemin d'adoption

```
Acheter 1 FIELD → tester dans le jardin
→ Acheter 1 STATION → dashboard local, plus besoin de relever la SD
→ Ajouter 3-5 FIELD → couverture complète
→ Passer à STATION+ (IA espèces + corrélation)
```

---

*Références : ADR-003 (radio), ADR-004 (stockage), ADR-009 (architecture satellite/base/cloud).*
