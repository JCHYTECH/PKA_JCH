# WildNexus — P0 Architecture Brief
### Document de référence unique · Gel des décisions · Orientation équipe

**Version :** 1.0  
**Date :** 2026-05-18  
**Auteur :** Dobby 🦉 — consolidation session JCH  
**Statut :** Actif — document de référence pendant l'absence de JCH  

---

## 1. Ce qu'on construit

Un **nœud caméra autonome** capable de capturer et d'identifier la présence de faune (animal / non-animal), de stocker les images localement et de transmettre des métadonnées via LoRa, opérationnel 60 jours en forêt belge sur 8 piles AA.

Ce n'est pas un piège photo amélioré. C'est le premier bloc d'une infrastructure distribuée d'observation écologique ouverte.

---

## 2. Où on en est — Cycle 01 / M-01 en cours

| Jalon | Description | Statut |
|-------|-------------|--------|
| **M-01** | Architecture gelée | **En cours — Cycle 01** |
| M-02 | Prototype banc fonctionnel | À venir |
| M-03 | EVT terrain validé | À venir |
| M-04 | Open source publié | À venir |

**Cycle 01 objectif :** valider toutes les décisions d'architecture avant toute commande de composants.

---

## 3. Périmètre P0 — ce qu'on construit et ce qu'on ne construit pas

### Dans P0

- Nœud caméra autonome (1 unité prototype + 1 spare)
- Capture image jour et nuit (IR)
- Détection événementielle (PIR)
- Filtre embarqué animal / non-animal (Edge AI binaire)
- Transmission LoRa P2P — métadonnées uniquement (~50 octets/événement)
- Stockage local microSD
- Configuration terrain simple (BLE ou équivalent)
- Autonomie 60 jours batterie seule
- Boîtier IP67 terrain
- Gateway LoRa P0 (ESP32-S3 + SX1262, ~25 €)
- Documentation suffisante pour reproduire le socle

### Hors P0 — décisions actées

| Sujet | Décision | Phase |
|-------|----------|-------|
| Radio cellulaire LTE-M (image à la demande) | Architecture validée, implémentation différée | **P1** |
| Panneau solaire + MPPT | Footprint mécanique prévu, hardware non câblé | **P1** |
| Bioacoustique | Matière documentée, non bloquant P0 | **P1** |
| Reconnaissance espèce fine | P0 = binaire animal/non-animal seulement | **P1** |
| Capteur environnement SHT31 | Optionnel, différé si budget serré | **P1 ou optionnel P0** |
| Faune Autour PWA | Projet adjacent, synergie P2 | **P2** |
| Réseau public de stations | Gouvernance non prête | **P2** |
| App native iOS/Android | PWA suffisante | **Hors scope** |

### Règle anti-scope-creep

Toute proposition d'ajout répond obligatoirement à trois questions :
1. Est-ce nécessaire pour prouver le nœud caméra autonome ?
2. Son absence rend-elle M-03 invalide ?
3. Peut-elle être remplacée par une interface ou une hypothèse documentée ?

Si les réponses ne justifient pas l'inclusion → reste hors P0.

---

## 4. Décisions architecture — tableau consolidé

| ADR | Sujet | Décision | Statut |
|-----|-------|----------|--------|
| **ADR-001** | MCU | ESP32-S3 (interface caméra DVP native, BLE, ULP, écosystème) — fallback STM32U5 si autonomie insuffisante | ✅ Accepté |
| **ADR-002** | Caméra | OV5640 5MP M12 DVP (Arducam) + lentille M12 IR-corrigée f/1.8 (Lensation ou Evetar) | ✅ Accepté |
| **ADR-003** | Radio | LoRa P2P EU868 — RAK3172 (SX1262) — gateway DIY ESP32-S3 + SX1262 breakout | ✅ Accepté |
| **ADR-004** | Stockage | microSD industrielle 16 GB | Ouvert |
| **ADR-005** | Énergie | **8 × AA standard (modèle industrie caméra de chasse)** — 4S2P → TPS62840 → 3.3 V | ✅ Accepté v0.2 |
| **ADR-006** | Boîtier | IP67 ABS/PC Hammond/Spelsberg — compartiment AA accessible sans outil | Ouvert |
| **ADR-007** | PIR | PIR basse conso (Panasonic EKMB) | Ouvert |

### Notes critiques par ADR

**ADR-001 (MCU)** — Test firmware : 100 cycles banc suffisants P0 (1 000 cycles = P1).

**ADR-002 (Caméra)** — Lentille M12 : choisir Lensation ou Evetar selon disponibilité EU et prix. Pas de courbe MTF requise P0 — les deux sont dans le bon tier. Aberrations documentées pendant le prototype, correction optique différée post-prototype.

**ADR-003 (Radio)** — LoRa seul pour P0. LTE-M différé P1 (architecture validée dans ADR-003 pour éviter refonte). Un seul stack radio à implémenter en WP03. Duty cycle EU868 à calculer avant M-02.

**ADR-005 (Énergie)** — Changement majeur de session : exit LiFePO4 18650 + BMS + MPPT. Modèle AA donne 2–3× plus d'énergie (~24–42 Wh vs 12.8 Wh), simplifie massivement WP02 et WP03. Piles non dans le budget projet — achat utilisateur.

| Type pile | Énergie | Autonomie à 3 evt/h |
|-----------|---------|---------------------|
| Eneloop Pro (NiMH) | 24 Wh | ~57 jours ✅ |
| Energizer Ultimate (Lithium) | 42 Wh | ~80 jours ✅ |

---

## 5. Philosophie d'ingénierie — règle de décision active

> **Quand l'écart technique entre deux options est faible ou non discriminant pour le cas d'usage P0, retenir le produit le plus robuste au meilleur rapport qualité/prix. Ne pas sur-spécifier.**

**Règle de tiebreak :** si discriminer deux options coûte plus de temps que la différence ne vaut, clôturer la question et choisir le plus robuste/disponible/économique.

**Application par WP :**

| WP | Consigne |
|----|---------|
| WP01 Architecture | Décisions à un niveau d'abstraction raisonnable — pas de précision excessive sur paramètres non bloquants M-01 |
| WP02 Hardware | Composants : disponibilité EU et robustesse terrain priment sur performance marginale |
| WP03 Firmware | Stack minimaliste — un seul stack radio (LoRa), mesurer avant d'optimiser |
| WP04 Edge AI | Classifieur binaire le plus simple atteignant le seuil P0 — pas de sur-ingénierie avant terrain |
| WP05 EVT | Protocole suffisant pour décision go/no-go — pas exhaustif |
| WP06 Open Source | Documentation minimale viable — pas une thèse |

---

## 6. BOM et budget P0

**Enveloppe :** 1 000 € maximum — tout dépassement projeté > 900 € → arrêt et arbitrage JCH.

| Poste | Composant | Coût estimé |
|-------|-----------|------------:|
| MCU | ESP32-S3 DevKitC × 2 | ~24 € |
| Caméra capteur | OV5640 M12 DVP × 2 | ~40 € |
| Caméra lentille | M12 IR-corrigée f/1.8 × 2 | ~70 € |
| IR LEDs | 850 nm × 4 lots | ~16 € |
| Radio LoRa | RAK3172 EU868 × 2 | ~24 € |
| Gateway | ESP32-S3 DevKit + SX1262 breakout | ~25 € |
| Énergie | TPS62840 + holders AA × 2 nœuds | ~10 € |
| Stockage | microSD industrielle 16 GB × 2 | ~24 € |
| Boîtier | Hammond IP67 × 2 | ~30 € |
| PIR | Panasonic EKMB × 2 | ~10 € |
| Passifs + connecteurs | — | ~50 € |
| PCB JLCPCB 5 pcs | — | ~55 € |
| Outillage | Nordic PPK2 (non négociable) | ~100 € |
| Outillage divers | câbles, multimètre, sangle | ~80 € |
| Frais de port + douane | — | ~40 € |
| Consommables terrain | silica gel, joints | ~20 € |
| Marge casse | 1 composant/catégorie | ~120 € |
| **Réserve 24 %** | — | **~162 €** |
| **TOTAL** | | **~900 €** |

**Hors budget (décision séparée si requis) :**
- Avis FTO/PI externe : 500–3 000 €
- 3e nœud complet : ~175 €
- Dataset IR externe : 200–1 000 €

**Règle d'achat individuel > 50 € :** signaler à JCH avant commande.

---

## 7. Assignments WP et prochaines actions

### WP01 — Conception & Architecture · *Dobby*
- [ ] Valider que tous les ADR ouverts (004, 006, 007) sont cadrés avant M-01
- [ ] Mettre à jour document fondateur v0.2 → v0.3 avec les décisions de cette session

### WP02 — Hardware & Enclos · *Forge + Castor*
- [ ] Schéma électronique : ESP32-S3 + OV5640 DVP + RAK3172 + TPS62840 + MOSFETs coupure + holder AA 4S2P + PIR
- [ ] Dimensionner PCB ≤ 150 × 100 mm
- [ ] ADR-006 : définir compartiment AA IP67 accessible sans outil
- [ ] Supply register : confirmer liens fournisseurs + prix livrés Liège

### WP03 — Firmware ULP · *Castor + Forge*
- [ ] Machine d'états : veille → réveil PIR → capture → inférence → stockage → LoRa TX → veille
- [ ] Un seul stack radio : LoRa P2P uniquement (LTE-M différé P1)
- [ ] Monitoring tension AA via ADC (seuils : alerte < 4.0 V, coupure < 3.6 V)
- [ ] Désactiver Wi-Fi hors configuration terrain

### WP04 — Edge AI · *Nova + Clio*
- [ ] Classifieur binaire animal / non-animal — modèle le plus simple atteignant le seuil
- [ ] Pipeline évaluation P0 : T04.5
- [ ] Dataset terrain belge IR nuit : planifier sessions collecte

### WP05 — Validation terrain EVT · *Chouette*
- [ ] Identifier site EVT forêt belge représentative
- [ ] Survey RF LoRa terrain : RSSI/SNR à 500 m, 1 km, 2 km
- [ ] Protocole EVT 30 jours : léger, suffisant pour go/no-go — pas exhaustif

### WP06 — Open Source & Communauté · *Forge*
- [ ] Documentation minimale viable après M-02 : compile + flash + reproduce
- [ ] Licence : décision JCH + Renard sur OSI vs usage-restriction (item ouvert)

---

## 8. Items ouverts — qui décide quoi

### ✅ GO — L'équipe décide sans JCH

| # | Sujet | Owner | Consigne |
|---|-------|-------|---------|
| O-02 | Longueur d'onde IR : 850 nm vs 940 nm | Nova + Chouette | **850 nm par défaut** (portée supérieure, standard industrie). Valider en EVT si perturbation faune constatée → basculer 940 nm. Pas besoin d'attendre. |
| O-03 | Boîtier exact (Hammond ou Spelsberg) | Chouette | Sélectionner selon critères ADR-006 : IP67, 150×100×60 mm max, ABS/PC sombre, compartiment AA accessible. Commander 2 unités. Achat < 50 € unitaire → go direct. |
| O-04 | PIR exact (Panasonic EKMB, variante FOV) | Chouette + Forge | Sélectionner après dimensionnement boîtier (O-03). Critère : courant ≤ 5 µA, FOV adapté au couloir de passage. Mouser BE. |
| O-05 | Shortlist sites EVT terrain | Chouette | Préparer 2–3 sites candidats (forêt belge, couvert dense, passage faune connu). JCH confirme au retour — pas bloquant pour WP02/WP03. |

### ⏸ ATTEND JCH — Bloqué sur décision personnelle

| # | Sujet | Owner | Action en attendant |
|---|-------|-------|---------------------|
| O-01 | Licence open source : OSI pure vs field-of-use restriction | **JCH + Renard** | Renard prépare une note comparative (OSI, CC, usage-restriction, dual-license) avec implications FTO — JCH décide au retour. Non bloquant avant M-03. |

---

## 9. Tests obligatoires M-02 — liste consolidée

| Test | Critère | Owner |
|------|---------|-------|
| Deep sleep carte complète (PPK2) | < 100 µA | Castor + Forge |
| Cycle réveil → capture → stockage → LoRa TX → veille | énergie < 1.5 mAh/événement | Castor + Forge |
| Firmware stabilité banc | 100 cycles stables | Castor |
| Image jour 5 m | animal identifiable | Nova |
| Image nuit IR 5 m | présence animal / non-animal validable | Nova |
| Portée LoRa forêt SF7 | RSSI/SNR documenté 500 m → 2 km | Forge + Chouette |
| Duty cycle EU868 | calcul documenté 5 evt/heure | Forge |
| IP67 boîtier | immersion 1 m / 30 min sans infiltration | Chouette |
| Condensation interne | 3 cycles -5 °C → +35 °C sans condensation PCB | Chouette |
| Buck converter sous charge | 3.3 V ± 3 % pendant cycle actif | Castor |

---

## 10. Principes non négociables

Ces points ne sont pas soumis à la règle de non-sur-spécification — ils sont des contraintes dures :

1. **Pas de Linux permanent sur le nœud** — MCU seul, pas de RPi
2. **IP67 long terme** — joint torique silicone remplaçable, pas d'impression 3D P0
3. **IR-correction obligatoire** sur la lentille — images nocturnes floues sans elle
4. **Nordic PPK2 obligatoire** pour mesurer le courant deep sleep — aucune autre méthode acceptable
5. **Deep sleep < 100 µA** — sinon fallback STM32U5 (ADR-001)
6. **Budget 1 000 € ferme** — tout dépassement projeté déclenche un arbitrage JCH
7. **Scope P0 strict** — toute proposition d'ajout passe par les 3 questions anti-scope-creep

---

*Dernière mise à jour : 2026-05-18 · Dobby 🦉 · Consolidation session JCH*  
*Fichiers sources : `ADR-001` à `ADR-006` · `WILDNEXUS_P0_SCOPE_LOCK.md` · `WILDNEXUS_ENGINEERING_PHILOSOPHY.md` · `WILDNEXUS_SUPPLY_REGISTER.md` · `WILDNEXUS_P0_BUDGET_RANGE.md`*
