# WILDNEXUS — Dossier technico-commercial V0
## « Bible » du projet — point zéro pour le démarrage technique

**Version :** V0.2 (intégration revue expert + corrections factuelles)
**Date :** 2026-10-29
**Statut :** DRAFT consolidé — revue expert intégrée (§ annexe). Validation JC requise.
**Propriétaire :** Jean-Claude Havaux — JCHYTECH
**Rédaction :** Dobby 🦉 (orchestration PKA_JCH)
**Sources techniques autoritatives :** `09_PRODUCT_SHEETS/F1_FIELD.md` (BOM 92,45 €, 8×AA 4S2P), `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md` v0.4 (758 €/242 €), `01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md` v0.4.
**Documents absorbés :** `executive-summary.md` (v1.0), `MASTER_ARCHITECTURE_WN.md` (mai 2026), `wildnexus-founding-document-v0.2/v0.3`.

> ⚠️ **Règle d'or** : ce dossier distingue systématiquement **P0 (engagé)** de **P1/P2 (vision)**. Toute promesse commerciale se lit à l'aune de cette distinction. La gouvernance « Satellite-Lite » prime : robustesse et vitesse avant optimum théorique.

> 🔧 **Correctifs V0.2 (suite revue expert)** : (1) BOM corrigé de « <22 € » (erroné) à **92,45 €** (fiche F1, production 100 u.) ; (2) budget corrigé à **~758 € engagé / ~242 € réserve** ; (3) architecture énergie précisée (**8×AA 4S2P**, TPS62840 **3,0 V**) avec **alerte** sur le rail 3,0 V ; (4) distinction claire **zéro abonnement DATA ≠ abonnement SERVICE** ; (5) segmentation conformité promue en co-primaire. Voir §19 (revue des experts).

---

## 0. Fiche signalétique (TL;DR)

| Élément | Valeur |
|---|---|
| **Nom** | WildNexus™ |
| **Entité** | JCHYTECH (Jean-Claude Havaux) |
| **Nature** | Nœud caméra-piège autonome à déclenchement intelligent + radio longue portée ; plateforme distribuée à terme |
| **Phase** | M-02 (prototype banc) — P0 |
| **Budget P0** | Enveloppe 1 000 € — **~758 € engagé/prévu, réserve ~242 €** |
| **Cœur technique P0 (F1 FIELD)** | ESP32-S3-WROOM N8R8 · OV5640 5MP NoIR + PIR Panasonic EKMB1203111 + 4× IR 940 nm · 2× Knowles SPH0645LM4H-B · IA binaire (Edge Impulse FOMO, <100 ms) · LoRa SX1262/RAK3172 EU868 P2P · **8× AA (4S2P)** L91 · buck TPS62840DLCR **3,0 V** · microSD 32 GB · boîtier Hammond 1555 IP67 |
| **Promesse P0** | Nœud autonome crédible : capture jour/nuit, audio local, trigger binaire, alerte LPWAN, **60 j à 10 événements/jour**, **zéro abonnement data** |
| **BOM production (100 u.)** | **~92,45 €** (hors piles) → prix cible 149-179 €, **marge brute ~40 %** |
| **Modèle éco** | Vente matériel (nœud + Station séparée) + licence duale + services (monitoring-as-a-service, conformité biodiversité) |
| **Différenciateur** | Nœud autonome **zéro abonnement data** (LoRa, pas de SIM), open source, conforme EU — vs ~799 $ concurrents cell/sat |
| **P1 (non engagé)** | Solaire/LiFePO4, ID espèce (SpeciesNet/BirdNET), multi-capteurs, LoRa Gen4 image, LTE-M image, cloud collaboratif |

---

## 1. Résumé exécutif V0

WildNexus transforme le piège photographique d'un instrument passif et « îlot » en **nœud autonome intelligent et connecté en longue portée**, à coût maîtrisé et **sans abonnement de données**. Le problème est documenté et massif : **75 à 90 % des déclenchements** de caméras-pièges classiques sont des **faux positifs** (vent, végétation), et le tri manuel paralyse chercheurs et gestionnaires.

Le marché est soutenu par la **loi** autant que par l'écologie : **CSRD** (ESRS E4 biodiversité), **TNFD** (France moteur), **Biodiversity Net Gain** britannique (suivi obligatoire 30 ans) et **EU Nature Credits** (cadre 2026) créent une demande de **données de biodiversité continues, standardisées, auditables**. C'est là que se situe la marge durable.

La stratégie est **frugale et prouvable** : réussir d'abord le **nœud P0** (AA, IA binaire, LoRa), puis étendre (P1). Le cloud IA n'est pas à réinventer (SpeciesNet open source 65 M images, Pytorch-Wildlife). WildNexus gagne sur **le terrain, l'autonomie, le coût et l'absence d'abonnement data**.

**Réalisme économique (corrigé)** : le BOM de production est **92,45 €** (fiche F1), pas 22 € — la marge brute visée est **~40 %** au niveau nœud, avant coûts complets (assemblage, test, certification, logistique, support). Voir §19 (revue financière) : à modéliser sérieusement avant tout pitch investisseur.

---

## 2. Problème, marché et demande

### 2.1 Le problème
- **Bruit de déclenchement** : 75-90 % d'images vides → tri humain coûteux.
- **Données tardives** : récupération SD par visites → information périmée.
- **La visite perturbe** : le passage du naturaliste modifie le comportement observé.
- **Deux mondes disjoints** : caméras grand public fermées (SD, IA nulle, pas de réseau) vs infrastructures institutionnelles lourdes/coûteuses.
- **Gap WildNexus** : nœud autonome, intelligent, connecté, abordable, remontant l'essentiel sans intervention.

### 2.2 Ordres de grandeur du marché (sources tierces — à recouper avant usage investisseur)
- Caméras-pièges : ~1,12 Md$ (2025) → ~2,18 Md$ (2034), CAGR ~7,7 % ; ~1,8 M u. (2024) → ~2,9 M/an (2030) *(Dataintelo)*.
- Wildlife tracking : ~1,35 Md$ (2024) → ~5,09 Md$ (2034), CAGR ~14,2 % *(market.us)*.
- Bio-acoustique/PAM : ~8,8 % CAGR ; PAM dominant *(MarketResearchFuture)*.
- Financement biodiversité : >4,5 Md$ 2025-2030 *(Dataintelo)*.
- Crédits biodiversité : ~37,5 Md$ en 2032 (26 % CAGR) *(Pandion/WEF)*.

> ⚠️ Cabinets hétérogènes → **ordre de grandeur de pitch uniquement**, pas une prévision financière. Cette prudence est un point fort à conserver.

### 2.3 Demande réglementaire (moteur EU/FR)
- **CSRD** (UE) : reporting ESG dont **biodiversité (ESRS E4)**, double matérialité.
- **TNFD** : 500+ organisations ; **France moteur** (lancement Paris 2021).
- **UK BNG** : premier marché de crédits biodiversité **obligatoire**, **suivi 30 ans**.
- **EU Nature Credits** : cadre opérationnel visé **2026**.
- **Conséquence** : besoins de **preuves terrain continues et auditables** → WildNexus = instrument de conformité.

### 2.4 Segments cibles (corrigé : conformité en co-primaire)
1. **Co-primaire A** : bureaux d'études écologues, collectivités, opérateurs BNG/CSRD/TNFD — acheteurs de **conformité** (pouvoir d'achat + besoin récurrent).
2. **Co-primaire B** : réserves naturelles, parcs nationaux/régionaux, associations (France : ~350 réserves, 11 parcs nationaux).
3. **Secondaire** : recherche académique (écologie, éthologie, bioacoustique).

---

## 3. Concurrence et positionnement

### 3.1 Paysage (benchmarks publics)
- **TrailGuard AI** (RESOLVE/Intel→Luxonis) : ~799 $/cam, edge AI, cell/satellite, batterie 1-2 ans, données sat ~15-20 $/mois. Pivot industriel.
- **Nightjar** : **freemium** (« gratuit sur 2 caméras ») + ~799 $/cam ; cellulaire.
- **Wildlife Insights** (Google + partenaires) : plateforme cloud **gratuite**, **SpeciesNet open source** (65 M images, 2000+ classes, ~88 % détection de vides, <2 % erreur), MegaDetector → **à intégrer, pas à concurrencer**.
- **Pytorch-Wildlife** (Microsoft) : framework open source + modèles.
- **AudioMoth** : logger acoustique open source très bon marché (~100 $, plein spectre) — référence PAM low-cost.
- **Wildlife Acoustics** (Song Meter Micro 2 ~249 $, 280 h, IP67 ; SM5 Li-ion + **port solaire**) : CA 10-25 M$ — le « premium » à battre sur prix/autonomie.

### 3.2 Positionnement WildNexus (clarifié)
- **Ne pas se battre sur le cloud IA** (gratuit/open source côté Google/MS).
- **Triple avantage** : (1) **zéro abonnement DATA** (LoRa P2P, pas de SIM par défaut) ; (2) **prix nœud** (149-179 €) vs ~799 $ ; (3) **conformité EU + données standardisées**.
- **Nuance TCO (correctif marketing)** : le prix 149-179 € est **le nœud seul**. Le système utile = nœud **+ Station** (gateway, ~249-299 €). Le TCO complet doit être communiqué (ex. 1 nœud + 1 station ≈ 400-480 €, + piles). Vs TrailGuard 799 $ + abonnement ≥180 $/an. **L'avantage reste net mais doit être chiffré honnêtement.**
- **Distinction à marteler** : « zéro abonnement **DATA** » (pas de SIM cellulaire) ≠ « pas de service payant » — un **abonnement SERVICE** (HaaS/dashboard/conformité) reste possible et souhaitable. Les deux ne se contredisent pas.

---

## 4. Vision et architecture (P0 → P2)

### 4.1 Vision
**Infrastructure distribuée d'observation écologique** : réseau de nœuds autonomes capturant, filtrant, transmettant et structurant des données multimodales (image, audio, environnement, temps, géo) vers une Station locale, sans dépendre du cloud.

### 4.2 Progression (incrémentale)
- **P0** : nœud terrain minimal crédible (robustesse, autonomie, trigger binaire, LoRa, SD, IP67).
- **P1** : bioacoustique, IA embarquée/ID via pipelines, multi-capteurs, gateways, exports standardisés.
- **P2** : plugins, API publique, SDK, réseau collaboratif, cloud scientifique, orchestration multi-sites.

### 4.3 Architecture matérielle hiérarchisée
- Majorité du temps en **ultra-basse consommation** (veille, scheduling, détection PIR, gestion énergie).
- Sous-systèmes énergivores (caméra, IR, IA) **activés uniquement sur événement**.
- MCU P0 : **ESP32-S3** (alt. STM32U5 / nRF54 envisageables en P1).

---

## 5. Spécification technique P0 (F1 FIELD — source F1_FIELD.md)

### 5.1 Composants (réels)
| Fonction | Composant | Détail |
|---|---|---|
| MCU | ESP32-S3-WROOM-1 N8R8 | 8 MB Flash, 8 MB PSRAM ; Wi-Fi off hors config |
| Caméra | OV5640 DVP 5MP | M12, NoIR, 2.8 mm f/1.8, 90-100° |
| Détection | PIR Panasonic EKMB1203111 | 2-3 µA, FOV ~86°×84°, ~5 m *(stock actuel : EKMB1303111 — à aligner)* |
| IR nocturne | 4× Vishay VSLB3940 940 nm | pulsé < 5 s |
| Audio | 2× Knowles SPH0645LM4H-B | I2S MEMS, 65 dB SNR, 20 Hz-10 kHz |
| Stockage | microSD 32 GB | Swissbit pSLC option terrain |
| Radio | LoRa SX1262 (RAK3172) | EU868 P2P, SF7-SF12, **500 m-3 km forêt** |
| Énergie | **8× AA (4S2P)** | L91 7 000 mAh / Eneloop Pro 5 000 mAh |
| Régulation | TPS62840DLCR | buck 60 nA Iq, **3,0 V**, 750 mA |
| IA onboard | Edge Impulse FOMO binaire | **< 100 ms** |
| Boîtier | Hammond 1555 IP67 | ABS 150×100×60 mm, trappe piles |
| Config | Smartphone (BTLE/Wi-Fi) | provisioning Espressif |

### 5.2 Fonctions P0
Capture jour/nuit · audio local (clip WAV 3 s/60 min + features FFT 1024/15 min, ADR-014/016/017) · trigger PIR + filtre **binaire** animal/non-animal · LoRa P2P événementiel (uplink 48 o / downlink 16 o, ADR-014) · stockage SD + sidecars JSON · config terrain · **autonomie ≥60 j à 10 évts/j, -10/+45 °C** · IP67 · doc reproductible.

### 5.3 ⚠️ Architecture énergie — point à verrouiller (R&D)
- Architecture retenue : **8× AA en 4S2P** → buck TPS62840 → **rail 3,0 V**, 750 mA, Iq 60 nA.
- **Alerte R&D** : 3,0 V est **la limite basse** de l'ESP32-S3 (et proche des besoins OV5640/MEMS). À **confirmer en WP03** (marge, chute en fin de vie piles, pics de courant caméra/IR). Si insuffisant, passer le rail à 3,3 V.
- **Blocage n°1 R&D** : **aucun budget énergie formalisé** n'existe encore (nb de cellules oui, mais pas : J/événement, courant de veille, courant caméra/IR, profil LoRa, budget thermique). Or **60 j = critère de sortie P0**. → **WP03 (mesure PPK2) prioritaire avant toute optimisation**.

### 5.4 Choix validés par la recherche externe
- **Piles primaires lithium (L91/Li-SOCl2)** : standard IoT longue durée, faible autodécharge, -40/+85 °C → **bon choix P0** ; solaire = P1 (BMS/MPPT).
- **LoRa SX1262** : bon compromis P0 ; veille **LoRa Gen4 (LR2021, mars 2025, ≤2,6 Mbit/s)** pour transfert image P1.
- **IA binaire S3 (FOMO)** : <100 ms confirmé (fiche F1) ; cohérent avec un train FOMO léger.
- **LTE-M (SIM7080G) optionnel** : image à la demande (P1), SIM 1NCE ~10 €/an.

### 5.5 Hors P0 (rappel)
BirdNET/ID espèce fine · reconnaissance individuelle · réseau public · multi-taxons · cloud complet · app native · monitoring 24/7 · **upload image/audio via LoRa** (notification seulement). → P1/P2.

---

## 6. Intégration pipelines (économie de R&D)

- **Images** : MegaDetector + SpeciesNet (open source) ou Wildlife Insights.
- **Oiseaux/amphibiens** : BirdNET. **Insectes** : InsectNet + InsectSet459.
- **Sorties standard** : Camtrap-DP (images), Darwin Core (occurrences), indices écoacoustiques (audio).
- **Bénéfice** : zéro R&D de modèle en P0 ; crédibilité scientifique ; alignement open source.

---

## 7. Plan de développement P0 (work-packages)

| WP | Objet | Critère de sortie |
|---|---|---|
| WP01 | Architecture & ADRs | 14 ADRs gelés, schéma système |
| WP02 | Hardware nœud | Alim, capteurs, média (gelé : tout ajout capteur = conso) |
| WP03 | Énergie & mesure | **Budget énergie (J/évt, veille, pics) + 60 j extrapolés au PPK2** |
| WP04 | Firmware | Machine d'états (PIR + cycles audio), deep sleep, SD, LoRa |
| WP05 | Connectivité | LoRa P2P nœud→gateway, format 0x05 (**bloqué : RAK3172 backorder**) |
| WP06 | Boîtier & terrain | IP67, EVT 30 j |

**Jalon critique** : lever le blocage **RAK3172 EU868** (SOP-07).

---

## 8. Roadmap et jalons

| Phase | Période | Jalon | Critère de sortie |
|---|---|---|---|
| M-01 | ✅ | Architecture gelée | ADRs + scope lock |
| M-02 | Q3 2026 | Prototype banc | Capture jour/nuit + trigger OK |
| M-03 | Q4 2026 | **EVT terrain** | **Autonomie 30 j + extrapolation 60 j** ; LoRa OK |
| M-04 | Q1 2027 | Open source + pré-séries | Repo public + 1re série |
| P1+ | 2027+ | Solaire, ID espèce, multi-capteurs | après M-03 |

---

## 9. BOM et budget (corrigé, chiffres vérifiés)

### 9.1 Budget P0 (prototype) — source `WILDNEXUS_P0_BUDGET_RANGE.md` v0.4
- **Reçu** : ~479 € (ESP32-S3 DevKit ×2, PPK2, OV2640/OV5640, MEMS, IR, PIR, buck, BME688, SHT31, antennes…).
- **À commander** : ~279 € (LoRa RAK3172 ×2, connectique, passifs, u.FL, RTC, protections, microSD).
- **Total engagé/prévu : ~758 €** · **Enveloppe 1 000 €** · **Réserve : ~242 €**.
- FTO/IP externe, 3e nœud, dataset IR externe, PCB dédié **hors budget 1 000 €** (voir §12).

### 9.2 BOM de **production** (100 unités) — source `F1_FIELD.md`
| Poste | € |
|---|---|
| ESP32-S3-WROOM-1-N8R8 | 4,00 |
| OV5640 + lentille M12 | 8,00 |
| PIR EKMB1203111 | 18,00 |
| LED IR VSLB3940 ×4 | 1,48 |
| SPH0645LM4H-B ×2 | 6,00 |
| RAK3172 LoRa | 8,00 |
| TPS62840 + passifs | 3,00 |
| Holders AA ×2 | 6,00 |
| PCB + assemblage (JLCPCB) | 10,00 |
| Boîtier Hammond modifié | 15,00 |
| microSD 32 GB | 8,00 |
| Divers | 5,00 |
| **TOTAL BOM** | **~92,45 €** |

> **Note** : le budget prototype (~758 € pour 2 nœuds DevKit + outillage PPK2 + réserve casse) ≠ BOM production (92,45 €/nœud en PCB dédié 100 u.). Ne pas confondre dans un pitch.

### 9.3 Coûts cachés à budgéter (manquants — correctif financier)
- **CE + RED** (radio EU868) : ~15-40 k€/famille.
- **Moule boîtier IP67 dédié** : ~10-30 k€ (P0 = Hammond modifié, pas de moule ; moule = pré-série P1).
- Fixture de test ICT, packaging, RMA/garantie, support, **marge distributeur 30-40 %**.
- **BFR** : à 5 000 u./an × ~92 € BOM + délais = besoin de fonds de roulement significatif (à modéliser ; ordre ~0,5 M€).

---

## 10. Modèle économique et offres

### 10.1 Matériel (gamme)
| Produit | Prix cible | Phase |
|---|---|---|
| FIELD (nœud) | 149-179 € | P0 |
| FIELD+ | 299-349 € | P1 |
| STATION (gateway) | 249-299 € | P1 |
| STATION+ | 599-799 € | P1+ |
| Nexus Acoustic | 249-299 € | P1 |

### 10.2 Licence logicielle
Hardware **CERN OHL v2** · Logiciel **AGPL v3 + licence commerciale** (dual).

### 10.3 Services / prestations (relais de croissance)
1. **Monitoring-as-a-Service (HaaS/DaaS)** : parc + dashboard + maintenance en abonnement (CapEx→OpEx). **Abonnement SERVICE**, distinct du « zéro abonnement DATA ».
2. **Rapports de conformité** (CSRD E4 / TNFD / BNG 30 ans) — livrables auditables (bureaux d'études/collectivités).
3. **Data & API licensing** (Camtrap-DP / Darwin Core / indices).
4. **Installation + formation + calibration** (prestation terrain).
5. **Freemium logiciel** (dashboard gratuit ≤2 nœuds, premium au-delà).
6. **Validation scientifique tierce** (partenariat université).

### 10.4 Économie unitaire (corrigée, hypothèses à valider)
- BOM nœud **92,45 €** · prix 149-179 € · **marge brute ~40 %** (hors piles) — **avant** assemblage/test/boîtier/certification/logistique/support. Marge **nette** nettement plus faible → **à modéliser**.
- Récurrent : abonnement service + licence pro (à chiffrer).
- Objectif an 3 : ~5 000 u./an (hypothèse historique, à re-challenger ; implique CA matériel ~0,75-0,9 M€ + récurrent).

---

## 11. Go-to-market

- **Entrée** : bureaux d'études écologues + réserves/parcs (co-primaire) ; acheteurs conformité EU.
- **Canaux** : partenariats BE, réseaux naturalistes (crédibilité terrain JCH), open source/WILDLABS, salons conservation tech.
- **Message** : « autonomie terrain + **zéro abonnement data** + conformité EU » ; **TCO system chiffré** (nœud + station, pas nœud seul).
- **Preuve** : **pilotes terrain nommés/datés/contractualisés** (à obtenir — manque actuel). Avant/après vs caméra classique : réduction du tri, remontée temps réel.
- **IA** : intégrer SpeciesNet/BirdNET, pas rivaliser.

---

## 12. Propriété intellectuelle et juridique (revue = synthèse Dobby, voir §19)

- **Marque** : WildNexus™ (JCHYTECH) déposée.
- **Hardware** : **CERN OHL v2 — variante à décider** : *P* (permissive), *W* (faiblement réciproque, compromis écosystème), *S* (fortement réciproque). **Décision non tranchée** → à valider (impact sur forks commerciaux).
- **Logiciel** : AGPL v3 + licence commerciale (cohérence dual OK).
- **Brevets/FTO** : **analyse interne seulement à ce stade** (budget P0 exclut l'IP externe). Risque : un partenariat/levée exigera un **FTO externe (0,5-3 k€)** avant toute divulgation.
- **Réglementaire produit** : **CE + RED** (EU868), CEM, sécurité — **non budgété** (§9.3).
- **RGPD** : géolocalisation, images de personnes (cas TrailGuard) → **politique de minimisation + base légale + durée de conservation à formaliser**.
- **Contrats** : CGV, licence, garantie (2 ans standard), SLA de service.

---

## 13. Risques et mitigations

| Risque | Impact | Mitigation |
|---|---|---|
| **BOM/marge surévalués** (22€→92€ corrigé) | Crédibilité / cash | Modèle financier complet (§9.3) avant pitch |
| **Budget énergie absent** (R&D) | Échec critère 60 j | **WP03 PPK2 prioritaire** ; confirmer rail 3,0 V |
| Surpromesse commerciale (solaire/ID) | Réputation | Messaging §16 ; P0 vs P1 strict |
| Backorder RAK3172 → SOP-07 | Planning M-03 | Source alt. SX1262 ; réévaluer jalon LoRa |
| Coûts cachés non budgétés (CE/RED, moule, distri) | Sous-estimation | Budgéter §9.3 |
| FTO interne seulement | Juridique/levée | FTO externe avant partenariat |
| Scope creep (capteurs/IA) | Retard, conso | Scope lock + 3 questions anti-creep |
| Dépendance mono-porteur (JCH) | Exécution | Open source, communauté, doc |
| Concurrence cloud gratuite | Prix logiciel | Se différencier terrain/autonomie/conformité |

---

## 14. KPIs et critères de succès

**P0** : trigger correct banc ; **budget énergie ≤ 60 j extrapolé** ; portée LoRa utile ≥0,5-3 km forêt ; taux d'images vides transmises <10 % ; MTBF EVT.
**P1** : précision ID (pipeline) ; coût unitaire série ; TCO vs concurrent.
**Business** : CAC, marge brute ET nette, conversion pilote→abonnement, revenu récurrent.

---

## 15. Gouvernance projet (Satellite-Lite)

- **Philosophie** : robustesse > performance ; 80 % en 5 j > 100 % en 12 sem. ; simplification si le critère P0 ne discrimine pas.
- **Scope lock P0** : AA only · IA binaire · LoRa P2P · audio local. **Interdits P0** : solaire, LiPo/LiFePO4, ID embarquée, vidéo/image sur LoRa.
- **Anti-scope-creep** (3 questions) : (1) nécessaire pour prouver le nœud ? (2) absence invalide M-03 ? (3) remplaçable par interface/hypothèse ? Sinon → hors P0.
- **Spécialistes** : Bioacoustique/DSP (Clio + Chouette) ; Hardware/Énergie (Forge + Bruno).
- **Sources de vérité** : `00_GOVERNANCE/Start.md` + `03_P0_ENGINEERING/PROTOCOLES/progress.md`.

---

## 16. Correction de messaging (décision V0)

L'`executive-summary.md` v1.0 (2026-07-03, **antérieur** au scope lock v0.4 du 2026-07-05) promettait solaire intégré, autonomie multi-saisons et classification d'espèce. **Décision V0** :
- **P0 (dire)** : nœud autonome, IA binaire, LoRa, AA, 60 j à 10 évts/j.
- **P1 (roadmap)** : solaire, ID espèce, multi-capteurs, LTE-M image.
- **Ne plus dire en P0** : « solaire intégré », « classification embarquée d'espèces », « multi-saisons sans intervention ».

---

## 17. Annexe — Sources externes (recherche 2026-10-29)
Marché : Dataintelo, Congruence/Yahoo Finance, market.us. Concurrents : Global Conservation/TrailGuard, Nightjar.tech, Wildlife Insights + google/cameratrapai (SpeciesNet), Wildlife Acoustics, Open Acoustic Devices (AudioMoth), Microsoft Pytorch-Wildlife. Réglementation : tnfd.global, CSRD/ESRS E4, GOV.UK BNG, Pandion/WEF, Gentian. Énergie/matériel : Battery Power Tips (Li-SOCl2), MDPI (battery vs solar WSN), Zbotic/Medium (TinyML ESP32-S3), fiche F1. Licensing : cern-ohl.web.cern.ch, OSI CERN-OHL-P-2.0.

---

## 18. Prochaines actions
1. **WP03 (PPK2)** : formaliser le budget énergie + confirmer rail 3,0 V — **débloque le critère 60 j**.
2. Débloquer **RAK3172** (SOP-07).
3. Corriger `executive-summary.md` (§16).
4. Modèle financier complet (marge nette, coûts cachés, BFR) — §9.3/§10.4.
5. Décider la variante **CERN OHL** + planifier FTO externe (avant partenariat/levée).
6. Obtenir 1-2 **pilotes terrain** nommés/datés.
7. Préparer le pitch « Monitoring-as-a-Service + conformité CSRD/BNG » (TCO system chiffré).

---

## 19. Revue des experts (V0.2)

> 4 revues lancées (juridique, financier, marketing, R&D). **Financier, Marketing et R&D ont rendu des verdicts exploitables.** Le sous-agent Juridique n'a pas restitué de rapport final propre via le runtime → la section juridique (§12) est une **synthèse Dobby** fondée sur le dossier + la contrainte budget (« FTO interne uniquement ») ; une validation par un avocat reste **indispensable** avant contrat. Ne pas présenter §12 comme un avis juridique.

### 19.1 Financier — verdict : **À CORRIGER** (point bloquant : BOM/marge)
- Points forts : discipline de coût P0 réelle (758 €/rés. 242 €) ; bon angle économiq. (conformité) ; lucidité sur les chiffres de marché.
- Critiques : **contradiction BOM 22 € vs 92,45 € (facteur 4)** — corrigée en V0.2 ; coûts cachés absents (CE/RED 15-40 k€, moule, fixture, RMA, support, marge distributeur 30-40 %) ; **aucun besoin de financement / burn / break-even** ; BFR stock non mentionné ; hiérarchie revenus (services vs 1 M€) contradictoire.
- Recommandations : (1) modèle financier complet avec marge nette ; (2) budgéter CE/RED + moule + distribution ; (3) scénarios de financement + BFR ; (4) réconcilier « services = relais » et volumes matériel ; (5) ne montrer à un investisseur que des chiffres consolidés.

### 19.2 Marketing — verdict : **À CORRIGER** (point bloquant : positionnement prix/TCO)
- Points forts : différenciateur LoRa « zéro abonnement » **vérifiable** ; correction de messaging exemplaire.
- Critiques : « 149-179 € vs 799 $ » **arithmétiquement trompeur** (nœud seul sans Station, EUR/USD, et modèle HaaS) — corrigé §3.2 ; demande réglementaire affirmée sans preuve tierce ; segmentation inversée (conformité) — corrigée §2.4 ; **aucun pilote nommé/daté/contractualisé**.
- Recommandations : (1) TCO **system** chiffré ; (2) preuve réglementaire sourcée ; (3) conformité en co-primaire ; (4) 1-2 pilotes contractualisés ; (5) distinguer « zéro abonnement data » ≠ « service ».

### 19.3 R&D — verdict : **À CORRIGER** (point bloquant : budget énergie absent)
- Points forts : discipline de scope exemplaire ; build-vs-buy correct (pipelines aval) ; comptabilité honnête + risque fournisseur identifié.
- Critiques : **aucun budget énergie formel** (J/évt, veille, pics) alors que 60 j = critère de sortie ; **rail 3,0 V marginal** pour ESP32-S3/OV5640 (à confirmer) ; deux affirmations du dossier contredisaient le scope lock (corrigées) ; PIR EKMB1303111 (stock) vs EKMB1203111 (F1) à aligner.
- Recommandations : (1) **WP03 PPK2 en premier** ; (2) confirmer/ajuster rail 3,0 V→3,3 V ; (3) aligner BOM stock = BOM F1 ; (4) documenter profil courant par état ; (5) sécuriser RAK3172 (alt. SX1262).

### 19.4 Juridique — synthèse Dobby (sous-agent non restitué) — verdict : **À CORRIGER**
- Points forts : dual-licensing logiciel cohérent (AGPL+commercial) ; marque déposée ; hardware open source aligné philosophie.
- À corriger : **variante CERN OHL non décidée** (P/W/S) ; **FTO interne seulement** (risque avant partenariat/levée) ; **CE/RED non budgété** ; **RGPD non formalisé** (géoloc, images de personnes) ; CGV/SLA/garanties à rédiger.
- Recommandations : (1) trancher CERN OHL ; (2) planifier FTO externe (0,5-3 k€) ; (3) budgéter CE/RED ; (4) formaliser RGPD (minimisation, base légale, conservation) ; (5) rédiger CGV/licence/SLA.

**Synthèse globale** : les 4 axes convergent sur **un même chantier prioritaire : fiabiliser les chiffres** (BOM 92,45 €, marge nette, budget énergie, coûts cachés) **et le message** (TCO system, zéro abonnement data ≠ service). Le socle technique et la discipline de scope sont solides ; le dossier est **prêt sur le fond technique P0**, **pas encore défendable en l'état devant un investisseur** sans le modèle financier complet.

---

*Fin du dossier V0.2 — consolidation de démarrage. Prochaine itération (V0.3) après : modèle financier complet, WP03 énergie, décision CERN OHL + FTO, pilotes terrain.*
