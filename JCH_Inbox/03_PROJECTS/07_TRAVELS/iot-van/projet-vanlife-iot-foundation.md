# Vanlife IOT — Document Fondateur

**Version :** v0.1 DRAFT
**Date :** 2026-06-04
**Statut :** DRAFT — Pour validation JCH
**Rédigé par :** [[Dobby]] 🦉 — template WildNexus
**Propriétaire :** Jean-Claude Havaux — JCHYTECH
**Véhicule :** Stylevan Origin Equinox 4 (Ford Transit Custom)

---

## Table des matières

| § | Section | Responsable |
|---|---------|-------------|
| 1 | Carte d'identité | JCH · [[Dobby]] |
| 2 | Contexte et origine | JCH |
| 3 | Vision et ambition | JCH · [[Atlas]] |
| 4 | Rationale stratégique | [[Dobby]] · [[Forge]] |
| 5 | Non-négociables | JCH · [[Renard]] |
| 6 | Objectifs & KPIs | [[Dobby]] · [[Atlas]] |
| 7 | État de l'art | [[Furet]] |
| 8 | Architecture système | [[Forge]] · [[Chouette]] |
| 9 | Propriété intellectuelle & garantie | [[Renard]] (en attente) |
| 10 | Work packages (phases) | [[Forge]] · [[Chouette]] |
| 11 | Plan de validation | [[Dobby]] · [[Forge]] |
| 12 | Registre des risques | [[Dobby]] · tous |
| 13 | Budget | [[Bruno]] · [[Forge]] |
| 14 | Outputs et impact | [[Dobby]] · [[Cigogne]] |
| 15 | Conditions de sortie | JCH |

---

## 1. Carte d'identité du projet

| Champ | Contenu |
|-------|---------|
| **Nom du projet** | Vanlife IOT |
| **Propriétaire** | Jean-Claude Havaux — JCHYTECH |
| **Véhicule** | Stylevan Origin Equinox 4 (Ford Transit Custom) — livraison 2026 |
| **Statut** | Actif — Phase design |
| **Version document** | v0.1 DRAFT |
| **Date** | 2026-06-04 |
| **Rédigé par** | [[Dobby]] 🦉 |
| **Validé par** | JCH (en attente) |

**Définition du succès :** Un van connecté où la domotique est invisible — le tableau de bord se consulte spontanément en voyage, les alertes arrivent sans bruit, Siri répond, et l'installation n'a pas compromis la garantie ni l'agrément de vie à bord.

**Budget :** ~635 € (4 phases) | **Durée :** ~4 week-ends + 2h | **Démarrage :** après validation garantie

---

## 2. Contexte et origine

Le Stylevan Equinox 4 est un fourgon aménagé haut de gamme sur Ford Transit Custom. Son équipement électrique de série (CBE DS300, batterie LiFePO4 150 Ah, panneau solaire 236 W) est fiable mais fermé : pas d'API, pas de supervision à distance, pas d'alerte.

En parallèle, le projet WildNexus a accumulé des leçons concrètes sur l'intégration Raspberry Pi 5 en environnement contraint : sensibilité à l'undervoltage USB-C, corruption microSD, conflits SQLite, gestion d'énergie en deep sleep. Ces leçons sont directement transférables au van.

L'opportunité est claire : mutualiser la plateforme RPi 5 + Tailscale + modem LTE entre WildNexus (terrain) et Vanlife IOT (van), partager les achats, les procédures, et la maintenance.

---

## 3. Vision et ambition

### Court terme (2026)
Un RPi 5 dans le meuble central, silencieux, invisible. Dashboard Lovelace accessible depuis l'iPad du van. Alertes frigo, température cellule, niveau d'eau, production solaire. Siri qui allume la lumière en prononçant une phrase.

### Moyen terme (2027)
Système appris — automatisations qui anticipent : ventilation auto en cas de surchauffe, alerte gel, verrouillage électro-aimant des tiroirs en roulant. Parlant au van et au réseau WildNexus via Tailscale.

### Long terme
Le van comme station d'observation mobile — capable de relayer les données WildNexus depuis le terrain, d'analyser la qualité de l'air, de servir de gateway LoRa en bivouac.

---

## 4. Rationale stratégique

| Choix | Option retenue | Alternatives écartées |
|-------|---------------|----------------------|
| Plateforme domotique | Home Assistant OS sur RPi 5 | S+ (fermé), ALD (cher), Homey (limité) |
| Stockage | SSD NVMe | microSD (corruption chronique — leçon WildNexus) |
| Alimentation | Convertisseur DC-DC 12V→5V USB-C PD 5A | Bloc secteur 230V (double conversion, perte) |
| Protocole capteurs | Zigbee (Sonoff/Aqara) | Z-Wave (plus cher, moins de choix), BLE (portée, fiabilité) |
| VPN | Tailscale (même tailnet que WildNexus) | ZeroTier (plus complexe), WireGuard pur (maintenance) |
| Solaire | Victron SmartSolar + SmartShunt | CBE PRS300 fermé, Antarion Bluetooth propriétaire |

**Levier principal :** la convergence avec WildNexus — même RPi 5, même stockage SSD, même VPN, même modem LTE, mêmes leçons d'échec. Chaque euro dépensé sert les deux projets.

---

## 5. Non-négociables

1. **Garantie** — aucune modification irréversible du véhicule sans validation expresse. Pas de perçage, pas de coupe de fil d'origine. Tout branchement doit être dérivable (porte-fusible, connecteur amovible).
2. **Sécurité route** — rien qui puisse gêner la conduite, créer un court-circuit, ou surcharger un circuit. Fusible dédié sur chaque dérivation.
3. **Robustesse** — SSD NVMe obligatoire. Pas de microSD pour le système.
4. **Discrétion** — installation invisible dans le meuble central. Pas de câble apparent, pas de boîtier qui traîne.
5. **Réversibilité** — tout doit pouvoir être démonté en 30 minutes pour revente ou intervention garantie.

---

## 6. Objectifs & critères de succès

| Objectif | Mesure | Cible |
|----------|--------|-------|
| Monitoring environnemental | Dashboard HA temps réel | ±0.5°C, refresh < 1 min |
| Sécurité passive | 5 capteurs portes + alertes | Notification < 30 s |
| **Détection présence extérieure** | **PIR extérieur déclenche lumière** | **< 2 s entre détection et allumage** |
| Consultation mobile | Dashboard iPad/iPhone via Wi-Fi van | HTTP 200, latence < 2 s |
| Contrôle vocal | Siri (HomeKit Bridge) | Taux réussite > 90 % |
| Résilience stockage | Zéro corruption après coupure | SSD NVMe bootable |
| Consommation électrique | Pi 5 en routine | < 15 W (target 10 W) |

**Succès si :** dashboard consulté spontanément en voyage, au moins 2 automatisations actives, Siri fonctionnel.
**Échec si :** système perçu comme nuisance, corruption SSD, garantie compromise.

---

## 7. État de l'art

> *À compléter par [[Furet]] 🦡 — veille sur les solutions vanlife IoT en 2026*

**Solutions existantes :**
- **S+** — domotique intégrée Stylevan, fermée, pas d'API publique
- **ALD** — système tiers professionnel, budget x5
- **Home Assistant + RPi** — solution open source, adoptée par la communauté vanlife, bien documentée
- **Victron ecosystem** — standard solaire/batterie, API VE.Direct, intégration HA native

**Leçons WildNexus capitalisables :**
- Undervoltage RPi 5 → câble USB-C PD 5A e-mark obligatoire
- Corruption microSD → SSD NVMe obligatoire
- Conflits SQLite → API REST pour tout accès concurrent
- GPS u-blox → résistant, faible consommation

---

## 8. Architecture système

```
Capteurs Zigbee → RPi 5 (HA OS, SSD NVMe, Zigbee dongle)
├─ 2x Sonoff SNZB-02 (T° cellule)
├─ 2x Sonoff SNZB-02 (T° frigo)
├─ 5x Aqara MCCGQ11LM (portes)
└─ (future) fuite eau, CO₂

Capteurs filaires
├─ GPS USB u-blox 7
├─ ESP32 + MPU6050 (inclinaison)
└─ PIR extérieur 12V IP65 → Sonoff SNZB-04 (contact sec Zigbee)

Actionneurs
├─ Relais 12V ← HA (allumage spot extérieur sur détection PIR)
└─ Spot LED extérieur 12V (existant ou ajouté)

Énergie
├─ Victron SmartSolar MPPT 100/20 → VE.Direct USB
├─ Victron SmartShunt 500A → VE.Direct USB
└─ DC-DC 12V→5V USB-C PD 5A ← F3 DS300

Réseau
├─ Wi-Fi AP : VanLife_Network (RPi 5 hotspot)
├─ LTE : MF833U1 / iPhone partage
├─ VPN : Tailscale (même tailnet que WildNexus)
└─ Apple : iPad (dashboard) + iPhone (Siri) + CarPlay
```

---

## 9. Propriété intellectuelle & garantie

**Analyse garantie :** en attente — brief envoyé à [[Renard]] le 2026-05-30, relancé le 2026-06-04.

**Points à clarifier :**
- Impact sur la garantie Stylevan du branchement sur F3 DS300
- Impact sur la garantie Ford du perçage/modification électrique
- Couverture assurance en cas d'incendie lié à l'installation
- Conditions de revente avec l'installation en place

**Licence :** l'ensemble de la config HA, des automatisations YAML et des dashboards sera publié sous licence open source (MIT) une fois stabilisé.

---

## 10. Work packages (phases)

### Phase 0 — Préparation

| Tâche | Owner | Livrable |
|-------|-------|----------|
| T0.1 | [[Renard]] | Avis garantie |
| T0.2 | JCH | Commande matériel phases 0-1 |
| T0.3 | [[Dobby]] | Localisation DS300 et goujon -B2 dans le van |
| T0.4 | [[Dobby]] | Brief [[Chouette]] — installation terrain |

### Phase 1 — Setup base (~1 week-end)

| Tâche | Owner | Livrable |
|-------|-------|----------|
| T1.1 | [[Forge]] | Flash SSD HA OS, test secteur |
| T1.2 | [[Forge]] | Wi-Fi VanLife_Network, appairage Zigbee |
| T1.3 | [[Forge]] | Dashboard Lovelace + HomeKit Bridge + test Siri |
| T1.4 | [[Forge]] | Test stabilité 24h |

### Phase 2 — Installation van (~1 jour)

| Tâche | Owner | Livrable |
|-------|-------|----------|
| T2.1 | [[Chouette]] | Fixation Pi meuble central |
| T2.2 | [[Chouette]] | Câblage alim F3 + masse -B2 |
| T2.3 | [[Chouette]] | Fixation 7 capteurs portes/température |
| T2.4 | [[Chouette]] + JCH | Test complet : iPad, iPhone, Siri |

### Phase 2b — Présence extérieure (~2h)

| Tâche | Owner | Livrable |
|-------|-------|----------|
| T2.5 | [[Chouette]] | Montage PIR extérieur IP65 sous toit relevable |
| T2.6 | [[Forge]] | Appairage Sonoff SNZB-04 sur contact sec du PIR |
| T2.7 | [[Forge]] | Automatisation HA : PIR déclenché → spot extérieur allumé |

### Phase 3 — Solaire & jauges (~1 week-end)

| Tâche | Owner | Livrable |
|-------|-------|----------|
| T3.1 | [[Forge]] | Installation MPPT SmartSolar 100/20 |
| T3.2 | [[Forge]] | Installation SmartShunt 500A |
| T3.3 | [[Forge]] | Dashboard énergie solaire |
| T3.4 | [[Forge]] | Jauges eau (ultrason JSN-SR04T) |

---

## 11. Plan de validation

### Phase 0 — PRÊT (toutes cases vertes)

- [ ] Garantie validée par [[Renard]]
- [ ] Matériel commandé et reçu
- [ ] Emplacements DS300 et -B2 repérés dans le van
- [ ] Brief [[Chouette]] transmis

### Phase 1 — VALIDÉE

- [ ] RPi 5 booté sur SSD, HA OS accessible (port 8123)
- [ ] Wi-Fi VanLife_Network actif, iPad connecté
- [ ] Au moins 3 capteurs Zigbee appairés et visibles dans HA
- [ ] HomeKit Bridge actif, Siri répond à 2 commandes
- [ ] Stabilité 24h : zéro reboot, zéro erreur SD/log

### Phase 2 — VALIDÉE

- [ ] RPi 5 alimenté depuis F3, tension stable (5V ±0.1V mesuré)
- [ ] Tous les capteurs portes installés et fonctionnels
- [ ] Dashboard consultable depuis iPhone via Tailscale
- [ ] Test route : zéro faux positif, zéro déconnexion

### Phase 2b — VALIDÉE

- [ ] PIR extérieur IP65 monté sous toit relevable
- [ ] Détection mouvement extérieur → notification HA < 2 s
- [ ] Spot extérieur s'allume automatiquement sur détection (test jour/nuit)
- [ ] Automatisation désactivable depuis le dashboard (mode silencieux)
- [ ] Faux positifs (branchage, animaux) < 2 par nuit

### Phase 3 — VALIDÉE

- [ ] Production solaire visible dans HA (W, Wh, tension batterie)
- [ ] SmartShunt calibré : consommation totale cellule mesurée
- [ ] Niveaux eau propre/usée dans le dashboard
- [ ] Dashboard énergie : production, consommation, SOC, autonomie

---

## 12. Registre des risques

| # | Risque | Impact | Probabilité | Mitigation | Owner |
|---|--------|--------|-------------|------------|-------|
| R01 | Undervoltage RPi 5 | Critique — reboots | Élevée | USB-C PD 5A + câble e-mark | [[Forge]] |
| R02 | Corruption stockage | Critique — perte config | Élevée | SSD NVMe obligatoire | [[Forge]] |
| R03 | Garantie compromise | Bloquant | Moyenne | Attente [[Renard]] | [[Renard]] |
| R04 | Interférence Zigbee | Gênant — capteurs morts | Faible | Répéteur Sonoff S31 | [[Chouette]] |
| R05 | Surchauffe meuble central | Dégradation Pi | Faible | Boîtier alu passif Flirc | [[Chouette]] |
| R06 | Consommation Pi (~15W) | ~30 Ah/j si route rare | Moyenne | UPS shutdown < 20% SOC | [[Forge]] |
| R07 | Vol/vandalisme van | Perte matériel | Faible | Installation invisible | [[Chouette]] |
| R08 | Conflit avec écosystème CBE | Court-circuit | Faible | Porte-fusible dédié, jamais couper fil d'origine | [[Chouette]] |
| R09 | Faux positifs PIR extérieur (branchage, animaux) | Gênant — nuit, nuisance | Moyenne | Automatisation désactivable + seuil temporisation configurable | [[Forge]] |

---

## 13. Budget

### Phase 0-1 : 246 €

| Composant | Qté | Total |
|-----------|-----|-------|
| Raspberry Pi 5 8 Go | 1 | 80 € |
| Boîtier alu Flirc RPi 5 | 1 | 15 € |
| SSD NVMe 128 Go | 1 | 20 € |
| Pimoroni NVMe Base HAT | 1 | 25 € |
| Convertisseur DC 12V→5V USB-C PD 5A | 1 | 10 € |
| Câble USB-C PD e-mark 5A | 1 | 5 € |
| Porte-fusible dérivateur mini ATP + fusible 5A | 2 | 5 € |
| Interrupteur bascule 12V | 1 | 5 € |
| Clé USB Zigbee (Sonoff ZBDongle-E) | 1 | 20 € |
| Capteurs température Zigbee (Sonoff SNZB-02) | 2 | 16 € |
| Capteurs ouverture porte (Aqara MCCGQ11LM) | 5 | 40 € |
| Câbles + gaine 1.5mm² | 1 | 5 € |

### Phase 2 : 56 €

| Composant | Qté | Total |
|-----------|-----|-------|
| GPS USB u-blox 7 | 1 | 12 € |
| ESP32 + MPU6050 (inclinaison) | 1 | 10 € |
| Module relais 12V + électro-aimant | 2 | 9 € |
| PIR extérieur 12V IP65 (alarme-grade) | 1 | 12 € |
| Sonoff SNZB-04 (contact sec Zigbee) | 1 | 8 € |
| Spot LED extérieur 12V + câbles | 1 | 5 € |

### Phase 3 : 250 €

| Composant | Qté | Total |
|-----------|-----|-------|
| Victron SmartSolar MPPT 100/20 | 1 | 105 € |
| Victron SmartShunt 500A | 1 | 90 € |
| Câble VE.Direct USB | 2 | 40 € |
| Capteurs ultrason eau JSN-SR04T | 2 | 10 € |
| Câbles + divers | 1 | 5 € |

### Consolidé

| Poste | Montant |
|-------|---------|
| Phase 0-1 | 246 € |
| Phase 2 (incl. PIR extérieur) | 56 € |
| Phase 3 | 250 € |
| Sous-total | 552 € |
| Marge imprévus (15%) | ~83 € |
| **Total** | **~635 €** |

---

## 14. Outputs et impact

### Livrables concrets

| Phase | Livrable | Format |
|-------|----------|--------|
| P0 | Avis garantie | Document [[Renard]] |
| P1 | RPi 5 + HA opérationnel + dashboard | Fichier config YAML |
| P2 | Installation van complète | Photos + checklist |
| P3 | Dashboard énergie solaire | Fichier YAML + schéma |

### Impact attendu

- **Confort :** température et humidité visibles, frigo surveillé, pas de surprise batterie
- **Sécurité :** alertes ouverture portes, verrouillage tiroirs en roulant
- **Énergie :** production solaire mesurée, consommation connue, autonomie prévisible
- **Mutualisation :** plateforme RPi partagée avec WildNexus → coût réduit, maintenance unifiée

---

## 15. Conditions de sortie

Le projet est considéré terminé quand :

1. Dashboard consulté et jugé utile après 3 voyages
2. Au moins 2 automatisations activées et non désactivées après 1 mois
3. 0 incident lié à l'installation (court-circuit, décharge batterie, dommage van)
4. Siri fonctionnel sur au moins 2 commandes

Le projet est abandonné si :

1. [[Renard]] confirme un risque garantie non mitigable
2. Le système cause un incident électrique
3. JCH juge le rapport confort/effort insatisfaisant après 3 voyages

---

## Références

- [[projet-vanlife-iot]] — Synthèse projet v1.0 ([[Atlas]])
- [[stylevan-equinox4-cahier-technique-iot]] — Cahier technique électrique
- [[rpi-vanlife-guide-complet]] — Guide d'installation RPi + HA
- [[rpi-vanlife-mode-emploi]] — Mode d'emploi pas-à-pas
- [[VAL-BOM-Vanlife-IOT_Forge_2026-05-31]] — BOM ([[Forge]])
- [[2026-05-30_Dobby_procurement_WILDNEXUS_update]] — Procurement WildNexus (convergence)
- [[2026-05-30_dobby_brief-garantie-vanlife]] — Brief garantie [[Renard]]

---

*Document v0.1 — [[Dobby]], 2026-06-04. Template WildNexus. Prochaine revision apres validation JCH et avis [[Renard]].*
