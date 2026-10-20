# WildNexus — Synthèse [[inbox]] du 12 juin 2026

**Auteur :** [[Sigma]] — pour [[Dobby]]  
**Date :** 2026-06-12  
**Source :** 4 documents Tiers 1–2 de l'[[inbox]] 00_INBOX  
**Destinataire :** JCH — note d'arbitrage  

---

## 1. Documents analysés

| # | Document | Lignes | Nature | Note |
|---|----------|--------|--------|------|
| D1 | [[WILDMESH_PLUS_MASTER_ARCHITECTURE]].md | 706 | Vision stratégique P0→P2 | Bible architecture |
| D2 | [[2026-05-16_projet-wildmesh-plus_synthese-architecture]].md | 819 | Blueprint technique 13 agents | Spécifications détaillées |
| D3 | WildNexus M-02 — Validation Prototype Laboratoire.md | ~50 | Jalon actuel | Feuille de route immédiate |
| D4 | File 10-06-2026, 22 28 32.txt (OV540) | 1407 | Guide technique OV5640+LoRa | Spécifications actionnables |

---

## 2. Constats principaux

### 2.1 Alignement remarquable des ADRs avec D1

Les 11 ADRs existants couvrent l'essentiel de la phase P0 décrite dans WILDMESH_PLUS. La philosophie « P0 simple, fiable, low-power » est **strictement respectée** par les décisions déjà acceptées :

- ADR-001 (ESP32-S3) ✓
- ADR-002 (OV5640) ✓
- ADR-003 (LoRa P2P EU868) ✓
- ADR-004 (microSD industrielle) ✓
- ADR-005 (AA + buck) ✓
- ADR-007 (PIR EKMB) ✓
- ADR-009 (architecture Satellite/Base/Cloud) ✓

Le document D1 valide rétrospectivement ces choix et n'introduit **aucune contradiction bloquante** pour P0.

### 2.2 Gaps identifiés — ce qui manque aux ADRs

| Gap | Source | Impact P0 | Recommandation |
|-----|--------|-----------|----------------|
| **Plugins hardware/software** | D2 (agents A8–A10) | P1 uniquement | Nouvel ADR-014 « Architecture plugin P1 » — ne pas toucher avant M-03 |
| **Bioacoustique** | D1 §10 | P1 uniquement | ADR à créer en P1. D1 recommande de séparer caméra / bioacoustique en deux produits distincts |
| **Thermal imaging** | D1 §11 | P1+ | Architecture prête mais pas de composant P0 |
| **Double MCU (MCU low-power + SoM Linux)** | D1 §5.2, D2 §A1 | P1+ | D1 lui-même met en garde. ADR-001 a tranché ESP32-S3 seul. Ne pas rouvrir. |
| **Vari-focal M12** | D4 | P0 (optionnel) | Pas dans le BOM. D4 décrit des objectifs 2.8-12mm manuels. À considérer pour Option B si budget restant. |
| **Station de base LoRa haute puissance** | D4 | P0 (base) | LILYGO T-Beam 1W (+32 dBm) recommandé par D4. **Pas dans le BOM actuel.** |

### 2.3 Le guide OV5640 (D4) enrichit le BOM existant

Le BOM WP02 shortlist v0.1 est **déjà très complet**. D4 confirme les choix et ajoute :

**Composants déjà dans le BOM et confirmés par D4 :**
- OV5640 Arducam DVP M12 (A02) ✓
- Lentille M12 IR-corrigée 6mm (B01 Lensation LS-6028) ✓ — D4 recommande précisément 6–8mm pour 3–12m wildlife
- RAK3172-T EU868 (B02) ✓ — D4 recommande SX1262, même chip
- MOSFET power gating (A12) ✓ — D4 insiste : **obligatoire**, l'OV5640 consomme en veille logicielle
- PIR externe + deep sleep (A05) ✓ — D4 confirme le pattern trigger PIR → wake → capture → sleep

**Composants nouveaux recommandés par D4 :**
- **Heltec WiFi LoRa 32 V3** (ESP32-S3 + SX1262 intégré) — alternative au couple DevKit + RAK3172, plus compact, ~20€
- **LILYGO T-Beam 1W** (+32 dBm, SX1262) pour la station de base — ~35€, non prévu au BOM
- **Relais solaire Meshtastic** (Heltec V3 + petit panneau) pour topologie mesh montagne — concept P1

**Alerte D4 :** L'OV5640 chauffe en mode actif → prévoir dissipateur (déjà noté dans File 10-06-2026, 22 29 14.txt). Dissipation thermique à intégrer dans le design boîtier (ADR-006).

### 2.4 M-02 : le point bloquant est la stratégie de test

Le document D3 rappelle que M-02 est **bloquant pour le passage à M-03** (terrain). Les points critiques :

| Test | Statut | Bloquant ? |
|------|--------|------------|
| Intégration HW (ESP32 ↔ OV5640 ↔ LoRa ↔ SD) | Non démarré | **Oui** — nécessite composants Option A |
| Benchmark IA (filtre animal vs non-animal) | Non démarré | **Oui** — ADR-010 R4 |
| Mesure consommation PPK2 | Non démarré | **Oui** — ADR-010 R5 |
| ADR-012 (stratégie de test) | En attente | **Oui** — bloque la formalisation |
| ADR-013 (format payload LoRa) | En attente | Non bloquant pour M-02 |

---

## 3. Recommandations pour JCH

### 3.1 Actions immédiates (cette semaine)

1. **Commander l'Option A du BOM** (~396 €) — le PPK2, les ESP32-S3, les OV5640, les PIR. Sans ces composants, M-02 ne peut pas démarrer. JCH a déjà commandé PPK2 + 2× ESP32-S3 (todo t17 ✓).

2. **Assigner ADR-012 à [[Forge]] + [[Castor]]** — stratégie de test formelle. Le template est prêt (cf. livrable [[Forge]]+[[Nova]]). Priorité : cette semaine.

3. **Assigner ADR-013 à [[Forge]] + [[Chouette]]** — format payload LoRa. Peut attendre la validation du lien radio.

### 3.2 Arbitrages

| Décision | Options | Recommandation [[Sigma]] |
|----------|---------|---------------------|
| Ajouter LILYGO T-Beam 1W au BOM ? | Oui (~35 €) / Non | **Oui** — pour la station de base. Budget restant : ~271 € |
| Ajouter Heltec V3 comme alternative ? | Oui / Non | **Non pour P0** — le couple DevKit + RAK3172 est suffisant. Garder en référence P1. |
| Rouvrir ADR-001 pour STM32U5/nRF54 ? | Oui / Non | **Non** — D1 mentionne ces alternatives mais ne les recommande pas pour P0. ESP32-S3 est le bon choix. |
| Intégrer la bioacoustique en P0 ? | Oui / Non | **Non** — D1 recommande explicitement de séparer caméra et bioacoustique. Produits distincts. |

### 3.3 Prochaine session

- Inspecter les livrables de [[Chouette]]+[[Araignée]], [[Castor]]+[[Fourmi]], [[Forge]]+[[Nova]]
- Valider les BOM additions proposées par [[Castor]]+[[Fourmi]]
- Si GO JCH : lancer la commande des composants manquants
- Assigner formellement ADR-012 et ADR-013 aux agents

---

## 4. Documents produits par cette session

| Agent | Livrable | Statut |
|-------|----------|--------|
| [[Chouette]] + [[Araignée]] | Rapport gaps WILDMESH_PLUS vs ADRs | En cours |
| [[Castor]] + [[Fourmi]] | Fiche spec OV5640 + LoRa + impact BOM | En cours |
| [[Forge]] + [[Nova]] | Checklist validation M-02 + template ADR-012 | En cours |
| [[Sigma]] | Cette synthèse | ✓ |

---

**Voir aussi :** [[WILDNEXUS_ADR_INDEX]], [[WP02_shortlist_achat_P0_v0.1]], [[Start.md]]
