# OpenRouter Auto Deep-Dive — WildNexus (2026-06-17)

> Session [[Dobby]] (DeepSeek TUI) → OpenRouter Auto Router (`openrouter/auto`)
> Modèle sélectionné automatiquement : **Perplexity Sonar** (×3)
> Cost-quality tradeoff réglé à 3/10 (favorise qualité)
> Coût total : ~6 300 tokens

---

## 1. Réseau LoRa — Topologie recommandée

**Verdict : tree-routing statique à 1-2 sauts, pas de mesh.**

| Option | Fiabilité forêt | Overhead | Conso | Verdict |
|---|---|---|---|---|
| LoRaWAN pur (étoile) | ★★☆ | Faible | Très faible | Fragile si relief |
| **Tree-routing statique** | ★★★ | Moyen | Faible | **Recommandé** |
| Mesh propriétaire | ★★☆ | Élevé | Élevée | Trop gourmand |
| Meshtastic | ★★☆ | Élevé | Moyen-élevé | Pas conçu pour capteurs |
| Reticulum | ★★☆ | Élevé | Moyen-élevé | Overkill |

**Points clés :**
- 500m en forêt vallonnée avec E22-900M30S → réaliste en SF12 (-130 dBm), mais pas garanti sur chaque lien
- 1 à 3 nœuds relais bien placés (points hauts, clairières) suffisent pour 20 nœuds
- TDMA léger plutôt que pure ALOHA → évite les collisions sans overhead excessif
- La consommation du relais est le facteur limitant → choisir les nœuds les mieux alimentés

→ **Action pour [[Araignée]]/[[Forge]] :** tester la portée réelle E22 en forêt avant de figer la topologie. Un survey RSSI terrain prime sur toute modélisation.

---

## 2. TinyML — Détection animal on-device

**Verdict : PIR + microcontrôleur ultra-basse conso en pré-détection → ESP32-S3 ne se réveille que pour confirmer.**

| Approche | Latence | SRAM | Conso par détection | Précision forêt |
|---|---|---|---|---|
| MobileNetV1-SSD | 500-800ms | ~300 KB | Élevée | 85-90% |
| **FOMO (Edge Impulse)** | 150-300ms | ~50 KB | Modérée | 80-88% |
| Modèle custom 2-classes | 100-200ms | ~30 KB | Faible | 75-85% |
| **PIR seul** | <1ms | 0 | ~50 µA | 50-70% (faux positifs) |
| **PIR + TinyML confirm** | PIR: <1ms / ML: 200ms | ~50 KB | ~50 µA veille | **90%+** |

**Architecture recommandée : PIR (ATtiny) → réveil ESP32 → FOMO confirmation → capture image.**
- Veille : ~50 µA (ATtiny + PIR)
- L'ESP32-S3 ne s'allume que sur trigger PIR validé
- Économie : un facteur 100-500× sur la conso vs polling caméra continu

→ **Action pour [[Forge]] :** tester FOMO via Edge Impulse sur ESP32-S3 avec un petit dataset wildlife (écureuils, chevreuils, sangliers). Le workflow Edge Impulse → Arduino est documenté.

---

## 3. Gestion thermique du boîtier

**Verdict : boîtier clair + heater batterie dédié + isolation locale batterie.**

| Configuration | Delta T interne vs ambiante |
|---|---|
| Boîtier foncé, plein soleil, fermé | +15 à +25°C |
| **Boîtier clair, même exposition** | **+3 à +8°C** |
| Ombragé + clair | +5 à +12°C |
| Ventilation (casse IP67) | -2 à -5°C |
| Isolation complète | Aide l'hiver, aggrave l'été |

**Points clés :**
- **Heater batterie : OUI, nécessaire.** L'isolation seule ne garantit pas >0°C lors des nuits à -15°C.
- Consigne heater : +2 à +5°C, piloté par thermostat
- Isolation locale autour de la batterie uniquement — pas le boîtier entier
- BMS avec interverrouillage de charge <0°C (sécurité si heater défaillant)
- PCM (matériaux à changement de phase) → non recommandé (coût, complexité, bénéfice modeste)
- Ailettes/dissipateur → seulement si mesures terrain montrent une surchauffe réelle

→ **Action pour [[Chouette]] :** intégrer un thermistor + heater pad dans le BOM. Dimensionner la puissance du heater (probablement 2-5W suffisant pour une batterie isolée).

---

## Métadonnées

- **Outil :** OpenRouter Auto (`openrouter/auto`) via Python `requests`
- **Modèle sélectionné :** `perplexity/sonar` pour les 3 requêtes
- **Paramètre cost_quality_tradeoff :** 3/10
- **Coût :** ~6 300 tokens (~0.01 USD estimé)
- **Crédit OpenRouter restant :** ~10 USD (pré-payé)
- **Projets concernés :** 03_WILDNEXUS
- **Spécialistes concernés :** [[Araignée]] (réseau), [[Forge]] (firmware), [[Chouette]] (hardware)
