# F2 — WildNexus FIELD+
> Nœud caméra autonome + acoustique + solaire · Version P1
> Fiche produit — 2026-06-19 (mis à jour 2026-06-30)

---

## Positionnement

Le FIELD+ est l'**upgrade terrain** du FIELD. Il ajoute l'autonomie solaire, une acoustique améliorée, et la connectivité longue portée. Conçu pour les déploiements longue durée sans maintenance — réserves naturelles, chercheurs terrain, suivis pluriannuels.

**Persona cible :** Réserve naturelle, chercheur en écologie, gestionnaire de site protégé.

---

## Évolutions vs FIELD

| Composant | FIELD | FIELD+ | Bénéfice |
|-----------|-------|--------|----------|
| **Énergie** | 8× AA Lithium L91 | LiFePO4 3 000 mAh + panneau solaire 5W | Autonomie illimitée (6 mois+) |
| **Acoustique** | 2× SPH0645 (10 kHz) | 2× ICS-43434 (20 kHz) + préampli | Couvre ultrason (sauterelles, chauves-souris) |
| **IA** | Binaire animal/non-animal | Espèces (FOMO multi-classes) | Identification taxonomique |
| **Radio** | LoRa P2P EU868 | LoRa P2P EU868 (+ LoRaWAN optionnel) | Compatibilité infrastructures existantes |
| **Capteurs env.** | — | BME688 (T/P/H/gaz) + SHT31 (humidité) | Contexte environnemental |
| **Boîtier** | Hammond 1555 IP67 | Boîtier alu usiné IP68 | Robustesse long terme, dissipation thermique |

---

## Spécifications détaillées

### Énergie solaire autonome

| Paramètre | Valeur |
|-----------|--------|
| Batterie | LiFePO4 3 000 mAh (2× 18650 ou pack prismatique) |
| Panneau | 5W monocristallin, 12V, ~280×180mm |
| Régulateur | MPPT intégré (BQ25570 ou équivalent) |
| Autonomie sans soleil | 30 jours (10 événements/jour) |
| Durée de vie batterie | 5-8 ans (LiFePO4, 2000+ cycles) |
| Température | -20°C à +60°C (LiFePO4) |

### Acoustique améliorée

| Paramètre | FIELD (SPH0645) | FIELD+ (ICS-43434) |
|-----------|-----------------|---------------------|
| Bande passante | 20 Hz – 10 kHz | 20 Hz – 20 kHz |
| SNR | 65 dB(A) | 65 dB(A) |
| Ultrason | ❌ | ✅ Orthoptères, chauves-souris |
| Pin-compatible | — | ✅ Drop-in replacement |

### IA embarquée — Espèces

- Classification multi-classes (10-20 espèces locales)
- Modèle FOMO / MobileNetV2 sur Edge Impulse
- Inference < 200ms, < 500KB flash
- Mise à jour OTA du modèle
- Espèces : mammifères communs + oiseaux chanteurs + orthoptères

---

## BOM estimatif (production 50 unités)

| Composant | Qté | Prix unit. | Total |
|-----------|-----|-----------|-------|
| Base FIELD (PCB + composants) | 1 | ~92.45€ | 92.45€ |
| LiFePO4 18650 3 000 mAh | 2 | ~6.00€ | 12.00€ |
| Panneau solaire 5W | 1 | ~15.00€ | 15.00€ |
| MPPT BQ25570 + passifs | 1 | ~5.00€ | 5.00€ |
| ICS-43434 (remplace SPH0645) | 2 | +2.00€ | 4.00€ |
| BME688 + SHT31 | 1+1 | ~10.00€ | 10.00€ |
| Boîtier alu usiné IP68 | 1 | ~40.00€ | 40.00€ |
| Support panneau + câblage | 1 | ~10.00€ | 10.00€ |
| **Total BOM** | | | **~188.45€** |

**Prix de vente cible :** 299-349€

---

## Ce qui est INCLUS

- 1× nœud FIELD+ assemblé (LiFePO4 pré-installée)
- 1× panneau solaire 5W + support de montage
- 1× câble solaire 3m
- 1× sangle de fixation arbre
- 1× carte microSD 32GB
- Modèle IA pré-entraîné (espèces Europe de l'Ouest)
- Documentation : installation solaire, calibration acoustique

## Ce qui n'est PAS inclus

- Gateway STATION (vendue séparément)
- Abonnement LoRaWAN (si utilisé — optionnel, pas requis)
- Recharge LiFePO4 externe (auto-suffisant)

---

## Upgrade path depuis FIELD

```
FIELD → FIELD+ : remplacer le boîtier + ajouter module solaire
                 → flasher firmware IA espèces
                 → remplacer micros (ICS-43434 drop-in)
```

**Rétrocompatibilité :** Le firmware FIELD+ peut tourner sur un FIELD (IA espèces sur micro 10 kHz). Upgrade matériel recommandé mais pas obligatoire.

---

*Références : ADR-001, ADR-002, ADR-003, ADR-005, ADR-006, ADR-008 (capteurs), ADR-013 (acoustique/micros), ADR-014 (payload LoRa).*

> ⚠️ LoRaWAN mentionné comme option P1 — aucun ADR ne valide encore cette intégration. L'option LoRaWAN dépendra d'une décision technique séparée en P1.
