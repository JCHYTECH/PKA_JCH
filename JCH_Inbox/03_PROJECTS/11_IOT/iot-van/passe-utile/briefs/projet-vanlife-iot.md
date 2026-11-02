# Projet Vanlife IOT — Domotique Stylevan Equinox 4

> Document projet v1.0 — Rédigé par [[Atlas]] 🐘, mandaté par [[Dobby]] 🦉 le 2026-05-30  
> Inclut la matrice de convergence avec le projet [[WildNexus]] / BirdNET-RPi

**Projet :** VANLIFE-IOT-001 | **Véhicule :** Stylevan Origin Equinox 4 (Ford Transit Custom)  
**Propriétaire :** JCH | **Date :** 2026-05-30

---

## 1. Résumé exécutif

Le projet **Vanlife IOT** équipe un Stylevan Equinox 4 d'un système domotique basé sur **Raspberry Pi 5 + Home Assistant**, intégré à l'écosystème Apple (CarPlay, HomeKit, Siri). Le système surveille : température cellule/frigo, ouverture 5 portes, niveaux d'eau, production solaire, état batterie.

Le projet partage la plateforme RPi 5 + Tailscale + modem LTE avec **WildNexus**, permettant de mutualiser les achats, les leçons terrain, et la maintenance.

**Budget :** ~600€ | **Durée :** 3 phases sur ~4 week-ends | **Démarrage :** dès validation garantie

---

## 2. Objectifs & critères de succès

| Objectif | Mesure | Cible |
|----------|--------|-------|
| Monitoring environnemental | Dashboard HA T° cellule, T° frigo, humidité | ±0.5°C, refresh < 1 min |
| Sécurité passive | 5 capteurs portes + alertes | Notification < 30s |
| Consultation mobile | Dashboard iPhone/iPad via Wi-Fi van | HTTP 200, latence < 2s |
| Contrôle vocal | Siri domotique | Taux réussite > 90% |
| Résilience stockage | Zéro corruption après coupure | SSD NVMe bootable |

**Succès si :** dashboard consulté spontanément en voyage, au moins 2 automatisations actives, Siri fonctionnel.  
**Échec si :** système perçu comme nuisance, corruption SSD, garantie compromise.

---

## 3. Architecture système

```
Capteurs (Zigbee/GPS/CBE) → Raspberry Pi 5 (HA OS, SSD, Wi-Fi AP)
   → iPad (dashboard local) / iPhone (Siri + 4G/Tailscale) / Ford SYNC (CarPlay)
Alimentation : LiFePO4 150Ah → F3 DS300 → DC-DC 12V→5V PD 5A
Phase 3 : Victron SmartSolar + SmartShunt → VE.Direct USB → Pi 5
```

---

## 4. Budget

| Phase | Contenu | Budget |
|-------|---------|--------|
| 0-1 | Pi 5 + SSD + alim + Zigbee + 7 capteurs | 223€ |
| 2 | GPS + inclinomètre + relais | 31€ |
| 3 | Victron solaire + jauges eau | 225€ |
| Marge | Imprévus, ports | ~120€ |
| **Total** | | **~600€** |

---

## 5. Planning

### Phase 0 — Préparation
- [ ] Validation garantie — [[Renard]] 🦊 (brief 30/05)
- [ ] Commande matériel
- [ ] Localisation DS300 et goujon -B2

### Phase 1 — Setup base (~1 week-end)
1. Flash SSD HA OS → test secteur
2. Wi-Fi VanLife_Network, appairage Zigbee
3. Dashboard Lovelace + HomeKit Bridge + test Siri
4. Test stabilité 24h

### Phase 2 — Installation van (~1 jour)
1. Fixation Pi meuble central
2. Câblage alim F3 + masse -B2
3. Fixation 7 capteurs
4. Test complet — iPad, iPhone, Siri

### Phase 3 — Solaire & jauges (~1 week-end)
1. SmartSolar + SmartShunt
2. Données solaires HA
3. Jauges eau
4. Dashboard énergie complet

---

## 6. Matrice de convergence WildNexus × Vanlife IOT

### Points communs — mutualisables

| Dimension | WildNexus | Vanlife | Mutualisation |
|-----------|-----------|---------|---------------|
| Compute | RPi 5, 8 Go | RPi 5 | Achats groupés, procédure flash identique |
| Alim Pi 5 | Buck TPS62840 + 8×AA | DC-DC 12V→5V USB-C PD | **Leçon undervoltage** — USB-C PD 5A obligatoire |
| Stockage | microSD industrielle (P0) | SSD NVMe obligatoire | Leçon corruption → SSD validée |
| Réseau | Modem LTE MF833U1 | Wi-Fi AP + 4G + MF833U1 | Même modem, même stack Tailscale |
| VPN | Tailscale (même tailnet) | Tailscale | birdnetpi et vanpi dans le même réseau |
| Dashboard | Interface web BirdNET (80) | Lovelace HA (8123) | Consultation mobile via Tailscale |
| Fournisseurs | Mouser, DigiKey | Amazon, Mouser | Panier groupé SSD, adaptateurs, câbles |
| Leçons | Undervoltage, corruption SD, SQLite, ports erronés | Mêmes risques | **Capitalisation directe** — chaque erreur évitée |
| Itération | M-01→M-02→M-03 | Phase 0→1→2→3 | Même approche progressive |

### Divergences

| Dimension | WildNexus | Vanlife | Raison |
|-----------|-----------|---------|--------|
| OS | RPi OS Lite (Debian) | HA OS (Buildroot) | IA audio vs domotique |
| Capteurs | Composants nus (CMS) | COTS (Zigbee) | Contrainte énergétique extrême vs pas de contrainte |
| Autonomie | 4-8 AA, 30 jours | 150 Ah, recharge roulant | Terrain isolé vs véhicule |
| Connectivité | LTE permanent | Wi-Fi local + 4G ponctuel | Données continues vs consultation |
| Coût | ~736€ (16 composants) | ~600€ (14 composants) | Ordres de grandeur comparables |

---

## 7. Gouvernance

| Rôle | Qui |
|------|-----|
| Commanditaire | JCH |
| Orchestrateur | [[Dobby]] 🦉 |
| Intégration électrique | [[Forge]] 🦦 |
| Installation terrain | [[Chouette]] 🦉 |
| Garantie & conformité | [[Renard]] 🦊 |
| Solaire | [[Nova]] 🦋 |
| Rédaction | [[Atlas]] 🐘 |

---

## 8. Risques & mitigations

| Risque | Impact | Mitigation | Source |
|--------|--------|------------|--------|
| Undervoltage Pi 5 | Critique | USB-C PD 5A + câble e-mark | WildNexus |
| Corruption stockage | Critique | SSD NVMe obligatoire | WildNexus |
| Conflit SQLite | Bloquant | API REST | WildNexus |
| Garantie véhicule | Bloquant | Attente [[Renard]] | Brief 30/05 |
| Interférence Zigbee | Gênant | Répéteur Sonoff S31 | [[Chouette]] |
| Surchauffe meuble | Dégradation Pi | Boîtier alu passif | — |
| Conso Pi (~15W) | ~30 Ah/j | UPS shutdown < 20% | — |

---

## Références

- [[stylevan-equinox4-cahier-technique-iot]] — Base technique van
- [[rpi-vanlife-guide-complet]] — Spécifications, YAML, leçons
- [[rpi-vanlife-mode-emploi]] — Installation pas-à-pas
- [[2026-05-28_retour-test-maison-rpi-birdnet-mobile]] — Leçons terrain RPi 5
- [[2026-05-30_Dobby_procurement_WILDNEXUS_update]] — Procurement WildNexus
- [[2026-05-30_dobby_brief-garantie-vanlife]] — Analyse garantie (attente)

---

*Document v1.0 — [[Atlas]] 🐘, 2026-05-30. Prochaine révision après avis [[Renard]].*
