# F1 — WildNexus FIELD
> Nœud caméra autonome · Version P0 MVP
> Fiche produit — 2026-06-19 (mis à jour 2026-06-30)

---

## Positionnement

Le FIELD est le **produit d'entrée** WildNexus. Un nœud caméra autonome, robuste, accessible à tout naturaliste. Il capture des images jour/nuit, détecte la présence animale, et transmet des alertes par radio. Pas de cloud, pas de complexité — juste un piège photo intelligent, ouvert et connectable.

**Persona cible :** Naturaliste amateur, association locale, propriétaire de terrain naturel.

---

## Spécifications techniques

| Catégorie | Composant | Détail |
|-----------|-----------|--------|
| **MCU** | ESP32-S3 WROOM-1 N8R8 | 8 MB Flash, 8 MB PSRAM, Wi-Fi désactivé hors config |
| **Caméra** | OV5640 DVP 5MP | M12 mount, NoIR, lentille 2.8mm f/1.8, champ 90-100° |
| **Détection** | PIR Panasonic EKMB1203111 | 2-3 µA, FOV 86°H × 84°V, range ~5 m |
| **IR nocturne** | 4× LED Vishay VSLB3940 940nm | Invisible faune, pulsé < 5s |
| **Audio** | 2× Knowles SPH0645LM4H-B | I2S MEMS, 65 dB SNR, 20Hz-10kHz, spatialisation stéréo |
| **Stockage** | microSD SanDisk Extreme 32GB | ~50 000 images (5MP JPEG), Swissbit pSLC en option terrain |
| **Radio** | LoRa SX1262 (RAK3172) | EU868 P2P, SF7-SF12, 500m-3km forêt |
| **Énergie** | 8× AA (4S2P) | Lithium L91 : 7 000 mAh, NiMH Eneloop Pro : 5 000 mAh |
| **Régulation** | TPS62840DLCR | Buck 60 nA Iq, 3.0V out, 750 mA |
| **Autonomie** | 60 jours minimum garanti | 10 événements/jour, Lithium L91, -10°C à +45°C |
| **Boîtier** | Hammond 1555 modifié IP67 | ABS, 150×100×60 mm, trappe piles, fenêtre optique anti-buée |
| **Fixation** | Sangle arbre | Supports ronds 10-40 cm diamètre |
| **AI onboard** | Binaire animal/non-animal | Edge Impulse FOMO, < 100ms inference |
| **Configuration** | Smartphone (BTLE/Wi-Fi) | Provisioning Espressif, pas d'écran onboard |

---

## Architecture de communication

```
FIELD (nœud) ──LoRa uplink──→ STATION (gateway)
                              └── alerte email/app

FIELD ←──LoRa downlink── STATION (demande image)
FIELD ──LTE-M burst────→ STATION (image 5MP, ~3-5 Mo)
```

- **Uplink :** paquet 48 octets binaire (cf. ADR-014 — horodatage, ID, score IA, batterie, RSSI, compteur)
- **Downlink :** paquet 16 octets binaire (cf. ADR-014 — demande image spécifique)
- **Pas de LoRaWAN, pas de TTN** — infrastructure propre, zéro dépendance externe
- **LTE-M (SIM7080G) optionnel** — pour téléchargement d'image à la demande seulement

---

## BOM estimatif (production 100 unités)

| Composant | Qté | Prix unit. | Total |
|-----------|-----|-----------|-------|
| ESP32-S3-WROOM-1-N8R8 | 1 | ~4.00€ | 4.00€ |
| OV5640 DVP + M12 lens | 1 | ~8.00€ | 8.00€ |
| PIR EKMB1203111 | 1 | ~18.00€ | 18.00€ |
| LED IR VSLB3940 | 4 | ~0.37€ | 1.48€ |
| SPH0645LM4H-B | 2 | ~3.00€ | 6.00€ |
| RAK3172 LoRa module | 1 | ~8.00€ | 8.00€ |
| TPS62840 + inducteur + passifs | 1 | ~3.00€ | 3.00€ |
| Holder AA Keystone 2463 | 2 | ~3.00€ | 6.00€ |
| PCB + assembly (JLCPCB) | 1 | ~10.00€ | 10.00€ |
| Hammond 1555 boîtier modifié | 1 | ~15.00€ | 15.00€ |
| microSD 32GB | 1 | ~8.00€ | 8.00€ |
| Divers (câbles, joints, visserie) | 1 | ~5.00€ | 5.00€ |
| **Total BOM** | | | **~92.45€** |

**Prix de vente cible :** 149-179€ (marge ~40%, hors piles)

> ⚠️ Le BOM production (92.45€) diffère du budget prototype P0 (307€ pour 2 nœuds, cf. `08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md`). Le prototype inclut l'outillage (PPK2), les frais annexes, la réserve casse, et utilise des DevKit au lieu de PCB dédié.

---

## Ce qui est INCLUS

- 1× nœud FIELD assemblé et flashé
- 1× sangle de fixation arbre
- 1× carte microSD 32GB
- Documentation : déploiement, configuration smartphone, remplacement piles
- Mise à jour firmware OTA (via smartphone)
- **Piles AA NON incluses** — standard industrie caméra de chasse

## Ce qui n'est PAS inclus

- Piles AA (fournies par l'utilisateur)
- Gateway STATION (vendue séparément)
- Abonnement LTE (optionnel, SIM 1NCE ~10€/an)
- Cloud / dashboard (STATION le fournit localement)
- Garantie étendue (standard 2 ans)

---

## Différenciation vs pièges photos existants

| | WildNexus FIELD | Browning / Reconyx / Bushnell |
|---|---|---|
| **Ouverture** | Open source, firmware modifiable | Fermé, propriétaire |
| **Connectivité** | LoRa P2P + LTE optionnel | Cellulaire propriétaire ou SD-only |
| **IA** | Binaire embarquée, entraînable | Aucune ou propriétaire |
| **Audio** | Stéréo MEMS pour monitoring | Rare, qualité médiocre |
| **Extensibilité** | Bus capteur documenté | Aucune |
| **Données** | Format standard, API locale | Export propriétaire |
| **Prix** | ~150€ | 200-600€ |

---

## Chemin d'adoption

```
Acheter 1 FIELD → déployer dans son jardin → recevoir alertes LoRa
→ Acheter 1 STATION → dashboard local, gateway
→ Acheter 2-3 FIELD supplémentaires → couvrir tout le terrain
→ Passer à FIELD+ (ajout solaire + micro amélioré)
```

---

*Références : ADR-001 (MCU), ADR-002 (caméra IR), ADR-003 (radio), ADR-004 (stockage), ADR-005 (énergie), ADR-006 (boîtier), ADR-007 (détection), ADR-013 (acoustique/micros), ADR-014 (payload LoRa).*
