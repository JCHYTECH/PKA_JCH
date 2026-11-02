# S2 — WildNexus STATION+
> Gateway + IA multi-taxons + corrélation multimodale · Version P1+
> Fiche produit — 2026-06-19 (mis à jour 2026-06-30)

---

## Positionnement

La STATION+ est la **station de recherche** WildNexus. Elle ajoute l'intelligence centralisée : classification multi-taxons, corrélation caméra+audio+environnement, exports scientifiques standardisés. C'est le hub d'un réseau FIELD+ pour la recherche écologique.

**Persona cible :** Laboratoire de recherche, parc national, observatoire biodiversité.

---

## Évolutions vs STATION

| Composant | STATION | STATION+ |
|-----------|---------|----------|
| **Compute** | RPi 5 4GB | RPi 5 8GB + Google Coral TPU (USB) |
| **IA** | — | Classification multi-taxons (mammifères, oiseaux, orthoptères, amphibiens) |
| **Corrélation** | — | Caméra + audio + environnement → événement composite |
| **Stockage** | SSD 256GB | SSD 1TB NVMe |
| **Dashboard** | Monitoring temps réel | + Analytics avancé (heatmaps, tendances, rapports) |
| **API** | REST locale | REST + WebSocket + export Camtrap-DP / Darwin Core |
| **Audio** | — | Pipeline bioacoustique complet (segmentation, classification) |
| **Cloud bridge** | — | Sync optionnelle vers cloud scientifique (RGPD compliant) |

---

## Capacités IA — Multi-taxons

### Modèles embarqués (TPU Coral)

| Modèle | Cible | Taille | Latence | Statut développement |
|--------|-------|--------|---------|---------------------|
| MobileNetV2 + FOMO | Mammifères (15 spp) | 3.5 MB | 8 ms | ⏳ À entraîner |
| BirdNET-Lite | Oiseaux chanteurs (200 spp EU) | 18 MB | 45 ms | ⏳ Basé sur BirdNET (Cornell) — écosystème analysé |
| InsectNet-CNN | Orthoptères (30 spp) | 12 MB | 25 ms | 🟡 Pipeline en cours (dataset Conocephalus fuscus prêt) |
| AmphibianNet | Amphibiens (10 spp) | 5 MB | 12 ms | ⏳ Non commencé |

> ⚠️ Ces modèles sont des **cibles produit P1**. InsectNet est le plus avancé (pipeline de collecte XC + segmentation actif). Les autres sont en planification.

### Corrélation multimodale

```
Événement caméra (chevreuil, score 0.92, 23:14)
  + Audio (cri chevreuil, score 0.78, 23:14:02)
  + Environnement (T=8°C, H=85%, P=1012hPa)
  → Événement composite : "Chevreuil — comportement vocal nocturne"
```

Le dashboard affiche non pas des événements isolés, mais des **scènes écologiques composites**.

---

## Exports scientifiques

| Format | Description |
|--------|-------------|
| **Camtrap-DP** | Standard pièges photo (GBIF, Wildlife Insights) |
| **Darwin Core** | Standard GBIF occurrences |
| **GeoJSON** | Cartographie interactive |
| **CSV** | Analyse statistique (R, Python) |
| **Audio WAV** | Segments audio étiquetés (espèce, confiance, horodatage) |

---

## Spécifications techniques

| Catégorie | Composant | Détail |
|-----------|-----------|--------|
| **Compute** | RPi 5 8GB + Google Coral TPU USB | 4 TOPS INT8, inference parallèle |
| **Radio** | RAK3172 LoRa + SIM7080G LTE | Même base que STATION |
| **Stockage** | SSD NVMe 1TB | ~8M événements composites |
| **Énergie** | PoE+ (Power over Ethernet) + UPS optionnel | Installation fixe 24/7 |
| **Boîtier** | Rack 19" 1U ou boîtier renforcé | Ventilation active |
| **Refroidissement** | Ventilateur + heatsink actif | TPU Coral chauffe en continu |

---

## BOM estimatif

| Composant | Qté | Prix unit. | Total |
|-----------|-----|-----------|-------|
| RPi 5 8GB | 1 | ~80.00€ | 80.00€ |
| Google Coral TPU USB | 1 | ~60.00€ | 60.00€ |
| RAK3172 + antenne | 1 | ~15.00€ | 15.00€ |
| SIM7080G LTE | 1 | ~15.00€ | 15.00€ |
| SSD NVMe 1TB | 1 | ~80.00€ | 80.00€ |
| Alim PoE+ HAT | 1 | ~20.00€ | 20.00€ |
| Boîtier rack/renforcé | 1 | ~40.00€ | 40.00€ |
| **Total BOM** | | | **~310.00€** |

**Prix de vente cible :** 599-799€

---

## Ce qui est INCLUS

- 1× STATION+ configurée (OS + Docker + modèles IA)
- 1× Google Coral TPU USB
- 1× antenne LoRa 868MHz extérieure
- 1× alimentation PoE+
- Pipeline bioacoustique pré-installé
- Dashboard analytics avancé
- Licences modèles IA (permanentes, mises à jour 2 ans)
- Exports Camtrap-DP / Darwin Core

## Ce qui n'est PAS inclus

- Nœuds FIELD/FIELD+ (vendus séparément)
- Écran / moniteur
- UPS (optionnel)
- Abonnement cloud bridge (optionnel)

---

## Différenciation vs recherche institutionnelle

| | WildNexus STATION+ | Infrastructure institutionnelle |
|---|---|---|
| **Coût déploiement** | ~700€ + nœuds | 10 000-100 000€ |
| **Complexité** | Auto-configurée | Équipe technique dédiée |
| **Données** | Export standards scientifiques | Formats propriétaires |
| **Évolutivité** | Ajout nœuds FIELD progressif | Infrastructure figée |
| **Maintenance** | Mise à jour OTA, auto-diagnostic | Contrat support |

---

*Références : ADR-001, ADR-003, ADR-009, ADR-012 (stratégie test), ADR-014 (payload LoRa).*

> ⚠️ Les modèles IA (InsectNet-CNN, AmphibianNet) sont des **cibles P1**. Leur disponibilité dépend de l'avancement des pipelines de collecte et d'entraînement. InsectNet est le plus avancé.
