---
projet: NUANCES
domaine: Principes d'installation BESS
auteur: [[Furet]]
date: 2026-05-10
statut: draft
---

# Installation BESS — Dimensionnement, Raccordement, Normes et Sécurité

## 1. Concepts fondamentaux

### 1.1 Capacité vs Puissance
Deux grandeurs distinctes doivent être dimensionnées indépendamment :

- **Capacité (kWh)** : énergie totale stockable. Déterminée par la durée de couverture souhaitée et les besoins en énergie.
- **Puissance (kW / kW peak)** : flux d'énergie maximal entrant ou sortant. Déterminée par les pointes de charge ou d'injection.

Le ratio Puissance/Capacité = **C-rate** (taux de charge/décharge).

### 1.2 C-Rate : définition opérationnelle
- **1C** : la batterie se vide (ou se charge) en 1 heure à puissance nominale
- **0,5C** : décharge en 2 heures — 100 kWh à 50 kW
- **2C** : décharge en 30 minutes — 100 kWh à 200 kW

**Exemples pratiques :**
- Résidentiel solar self-consumption : 0,3C–0,5C (priorité durée de vie)
- Commercial demand charge management : 0,5C–1C
- Grid frequency regulation : 1C–2C (court, répété)
- Long-duration backup : 0,2C–0,25C

**Impact sur la durée de vie :** Un C-rate élevé génère plus de chaleur interne et stress chimique. Pour maximiser le nombre de cycles, il convient de rester en dessous de 1C pour les applications stationnaires.

---

## 2. Dimensionnement : méthode de calcul

### 2.1 Étape 1 — Définir le besoin en énergie (kWh)
```
Capacité requise (kWh) = Consommation à couvrir (kWh) / DoD
```
- **DoD (Depth of Discharge)** : profondeur de décharge maximale recommandée
  - LFP : 100% DoD techniquement possible, 80–90% recommandé pour la durée de vie
  - NMC : 80% DoD recommandé
  - VRFB : 100% DoD (sans dégradation)

**Exemple résidentiel :**
- Consommation nocturne à couvrir : 8 kWh/jour
- DoD retenu : 90%
- Capacité installée requise : 8 / 0,9 = 8,9 kWh → choisir 10 kWh

### 2.2 Étape 2 — Définir la puissance crête (kW)
```
Puissance nominale requise (kW) = Charge de pointe simultanée (kW)
```
- Vérifier le C-rate résultant : Puissance / Capacité ≤ 1C (recommandé stationnaire)
- Pour demand management : identifier la durée de la pointe → ajuster C-rate

**Exemple [[commercial]] :**
- Pointe de demande à écrêter : 150 kW sur 30 minutes
- Énergie requise : 150 kW × 0,5h = 75 kWh
- C-rate : 150/75 = 2C → acceptable pour des pointes courtes, mais accélère le vieillissement

### 2.3 Étape 3 — Corriger pour les pertes système
```
Capacité effective = Capacité installée × Efficacité round-trip × (1 - pertes câblage)
```
- Efficacité round-trip LFP : 92–96%
- Pertes câblage/conversion typiques : 2–5%
- Facteur vieillissement sur 10 ans : prévoir -20% de capacité résiduelle (LFP) → surdimensionner de 25% si budget le permet

### 2.4 Cas d'usage typiques — gammes de dimensionnement

| Application | Capacité | Puissance | C-rate typique | Commentaire |
|-------------|----------|-----------|---------------|-------------|
| Résidentiel standard | 5–15 kWh | 3–7 kW | 0,3–0,5C | Couplage avec PV 3–10 kWp |
| Résidentiel étendu | 15–30 kWh | 5–15 kW | 0,3–0,7C | Maison >200 m², voiture électrique |
| Commercial PME | 100–500 kWh | 50–250 kW | 0,3–1C | Demand charge, UPS, PV |
| Community storage | 500 kWh–5 MWh | 200 kW–2 MW | 0,2–0,5C | 50–500 foyers équivalents |
| Industriel | 1–10 MWh | 500 kW–5 MW | 0,5–1C | Process, peak shaving |
| Grid-scale (4h) | 10–100+ MWh | 5–50 MW | 0,25C | Marché de balancing |
| Van aménagé (mobile) | 20–60 kWh | 3–10 kW | 0,2–0,3C | Usage off-grid, services |
| Camion/remorque mobile | 100–500 kWh | 50–200 kW | 0,3–0,5C | Events, chantiers, rural |

---

## 3. Architecture système : AC vs DC coupling

### 3.1 DC Coupling (couplage DC)
La batterie est connectée directement en courant continu, en amont de l'onduleur principal (hybride).

```
PV Array → Charge Controller → DC Bus ← Batteries
                                    ↓
                               Onduleur hybride
                                    ↓
                               Réseau / Charges AC
```

**Avantages :**
- Rendement global supérieur (évite une conversion DC→AC→DC supplémentaire)
- Possibilité de recharger les batteries même si le réseau est absent (island mode)
- Meilleure intégration dans les nouvelles installations PV+BESS

**Inconvénients :**
- Nécessite un onduleur hybride dédié (remplacement si PV existant)
- Plus complexe à intégrer en retrofit sur installation existante
- Tension DC doit être compatible entre PV, batteries et onduleur

**Efficacité :** 92–96% round-trip (moins de conversions)

### 3.2 AC Coupling (couplage AC)
La batterie dispose de son propre onduleur bidirectionnel. Elle se connecte sur le bus AC de l'installation.

```
PV Array → Onduleur PV → Bus AC ← Onduleur bidirectionnel ← Batteries
                             ↓
                     Réseau / Charges
```

**Avantages :**
- Indépendance de l'onduleur PV existant : retrofit facile
- Flexibilité : batterie peut se charger depuis le réseau, le PV, ou les deux
- Évolutif : ajout de modules simples

**Inconvénients :**
- Rendement légèrement inférieur (double conversion AC↔DC)
- En island mode : risque de boucle de charge (stabilité à gérer)
- Coût système légèrement supérieur (deux onduleurs)

**Efficacité :** 88–93% round-trip

### 3.3 Choix pratique
| Situation | Recommandation |
|-----------|---------------|
| Nouvelle installation PV+BESS | DC coupling (hybride) |
| Retrofit sur PV existant (onduleur OK) | AC coupling |
| Site sans PV (BESS seul) | AC coupling |
| Off-grid / island mode prioritaire | DC coupling |
| Community storage multi-sources | AC coupling (flexibilité) |

---

## 4. Composants clés du système

### 4.1 BMS — Battery Management System
Le BMS est le cerveau de sécurité de toute installation BESS. Il assure :

**Fonctions de protection :**
- Surveillance tension cellule par cellule (overcharge, deep discharge)
- Surveillance température (arrêt si > seuil critique)
- Protection court-circuit et surintensité
- Cell balancing (actif ou passif) pour homogénéiser le SOC

**Fonctions de mesure :**
- SOC (State of Charge) : estimation de l'énergie restante
- SOH (State of Health) : capacité résiduelle vs initiale
- SOP (State of Power) : puissance instantanée disponible

**Exigences réglementaires :**
- UL 1973 (USA) : BMS doit répondre à des exigences de sécurité fonctionnelle
  - Référence UL 991 (hardware) et UL 1998 (software)
  - Tolérance aux défauts simples (single-fault tolerance) obligatoire
- IEC 62619 : analyse de sécurité fonctionnelle requise (IEC 61508 ou ISO 13849 applicables)
- Redondance : capteurs temperature et voltage doublés dans les systèmes critiques

**Niveaux de BMS :**
- **Cell BMS** (niveau cellule) : monitoring individuel
- **Module BMS** : agrégation par module
- **Pack BMS / MBMS (Master)** : supervision globale, interface avec l'onduleur et le réseau
- **EMS (Energy Management System)** : couche de gestion au-dessus du BMS, pilote la stratégie de charge/décharge

### 4.2 Power Conversion System (PCS / Onduleur bidirectionnel)
- Convertit le DC batterie en AC réseau (décharge) et inversement (charge)
- Taille : de 3 kW (résidentiel) à plusieurs MW (grid-scale)
- Fonctionnalités avancées : reactive power support, frequency response, black start capability
- Standards de connexion réseau : IEEE 1547 (USA), VDE-AR-N 4105 (Allemagne), G99 (UK), RTE C14/100 (France)

### 4.3 Thermal Management System (TMS)
- **Passive cooling** : dissipation naturelle + ventilation — résidentiel <30 kWh
- **Active air cooling** : ventilateurs — [[commercial]] jusqu'à ~500 kWh
- **Liquid cooling** : circuits eau/glycol — grid-scale et haute densité (Tesla Megapack, CATL EnerC)
- Température optimale LFP : 15–35°C — au-delà de 45°C, vieillissement accéléré

---

## 5. Normes et certifications applicables

### 5.1 Normes internationales (niveau cellule et composant)

**IEC 62619:2022 — Cellules et modules Li-ion stationnaires**
- Standard de référence international pour la sécurité des batteries Li-ion en usage stationnaire
- Couvre : conditions d'abus (surcharge, court-circuit, choc thermique), analyse de sécurité fonctionnelle
- Certification : 3–6 mois, ~50 000–80 000 € de tests
- Applicable à : LFP, NMC, NCA — tout usage stationnaire

**IEC 62485-5 — Installation sécurisée des systèmes de batteries**
- Règles d'installation, ventilation, câblage
- Complète IEC 62619 au niveau système

**IEC 62933-2-1 — Performance et sécurité ESS**
- Méthodes de test pour les systèmes de stockage stationnaires

### 5.2 Normes système (ESS complet)

**UL 9540:2023 — Standard for Energy Storage Systems and Equipment (USA/Canada)**
- Certification système complet : batterie + PCS + TMS + BMS + enclosure
- Couvre : sécurité électrique, thermique, logicielle
- Durée : 6–12 mois, coût : 82 000–96 000 $
- Requis pour : tout BESS vendu aux USA — devient référence de facto pour assurabilité
- UL 9540A : test spécifique sur le risque de propagation d'incendie (thermal runaway propagation)

**UL 1973 — Standard for Batteries for Use in Light Electric Rail Applications and Stationary Applications**
- Certification niveau batterie seule pour applications stationnaires
- Précondition fréquente avant UL 9540

**UL 1741 / UL 1741-SA — Onduleurs et équipements de connexion réseau**
- Standard pour les PCS connectés au réseau

### 5.3 Normes européennes

**EN 50604-1:2016 — Secondary lithium cells and batteries for light EV applications**
- Applicable aussi au stationnaire léger

**EN IEC 62619 (transposition européenne)**
- Alignée sur IEC 62619, appliquée via CE marking

**IEC/UL 62368-1 — A/V, IT and communication equipment**
- Applicable aux systèmes BESS avec interface numérique

**NFPA 855:2023 (USA — référence internationale pour sécurité incendie)**
- Standard pour l'installation des systèmes stationnaires de stockage d'énergie
- Inclut : distances de séparation, exigences ventilation, suppression incendie, accès secours
- Influence les codes du bâtiment en Europe via transposition nationale

**EN 61439 — Low-voltage switchgear and controlgear assemblies**
- Applicable aux armoires électriques intégrées aux BESS

### 5.4 CE Marking (Europe)
- Obligation légale pour tout BESS commercialisé dans l'UE
- Directives applicables : LVD (Basse Tension), EMC, RED (pour équipements radio si applicable), RoHS
- EU Battery Regulation 2023/1542 : ajoute des exigences carbone footprint, labelling, passeport numérique

---

## 6. Cas d'usage détaillés

### 6.1 Résidentiel (5–20 kWh)
**Architecture type :**
- PV 6–12 kWp + onduleur hybride 5–10 kW + batterie LFP 10–20 kWh
- DC coupling recommandé en installation neuve
- Compteur communicant obligatoire (Linky en France, smart meter en Belgique)
- Connexion réseau : raccordement monophasé ou triphasé selon puissance PCS

**Contraintes d'installation :**
- Garage : ventilation naturelle ou forcée minimum
- Cave : hygrométrie contrôlée (<85% HR), température >5°C
- Extérieur : IP55 minimum, protection UV, anti-intrusion
- Distance chauffière ou matières inflammables : > 1 m (NFPA 855 référence)
- Habitations : JAMAIS dans espaces habitables (chambres, séjour)

**Puissance de connexion :**
- France : autorisation Enedis obligatoire au-dessus de 3 kVA d'injection
- Belgique : attestation RGIE + approbation gestionnaire réseau (Fluvius, ORES, RESA)

**Coût indicatif 2025 :**
- Système résidentiel 10 kWh complet installé : 6 000–12 000 € (selon marché et produit)
- Payback avec PV : 7–12 ans selon tarification locale

### 6.2 Commercial et industriel (100–500 kWh)
**Architecture type :**
- AC coupling sur tableau BT existant
- BESS conteneurisé ou rack installé en local technique dédié
- PCS 50–250 kW
- EMS communicant avec compteur d'énergie et automate de gestion

**Fonctions valorisables :**
- Peak shaving / demand charge management : économies sur abonnement puissance
- Stockage heures creuses / décharge heures de pointe (arbitrage tarifaire)
- Fréquence de réponse pour participation marchés de flexibilité (FCR, aFRR)
- UPS / backup critique

**Contraintes spécifiques :**
- Local batteries : classe de résistance au feu REI 120 minimum (France, décret ICPE si >200 kWh)
- Ventilation mécanique obligatoire (calcul selon gaz dégagés en cas de défaut)
- Détecteur multi-gaz (CO, H₂, HF) recommandé
- Sprinkler ou système suppression incendie : obligatoire selon NFPA 855 et réglementation ICPE

**Coût indicatif 2025 :**
- BESS 200 kWh complet installé : 80 000–150 000 € (hors génie civil)

### 6.3 Community Storage (500 kWh–plusieurs MWh)
**Modèle économique :**
- Gestion collective pour un quartier, une coopérative, une communauté d'énergie
- Facturation proratisée selon apport solaire et consommation
- Interaction avec marché spot (arbitrage, FCR) pour financer l'investissement

**Architecture type :**
- Système conteneurisé (container 20 ou 40 pieds) LFP
- PCS 500 kW–2 MW
- Connexion au réseau de distribution (poste de transformation dédié souvent nécessaire)
- EMS avancé avec monitoring en temps réel

**Réglementation :**
- RED III (EU) : permet aux communautés d'énergie de participer aux marchés d'électricité
- Belgium : communautés d'énergie reconnues par VREG/CWaPE depuis 2023
- France : communautés d'énergie renouvelable encadrées par loi APER 2023

**Coût indicatif 2025 :**
- 1 MWh communautaire (matériel + installation + raccordement) : 400 000–700 000 €
- Financement possible via IPCEI, Fonds Européens, coopératives citoyennes

### 6.4 Mobilité — Van/Camion aménagé
**Spécificités critiques :**
- Vibrations et chocs mécaniques : certification IEC 62619 + tests vibration UN38.3
- Température ambiante variable : TMS actif recommandé si déploiement Europe du Nord
- Connexion : systèmes autonomes (off-grid total) ou hybrides (recharge réseau la nuit)
- Puissance à bord : 3–10 kW pour van, 50–200 kW pour camion/remorque

**Dimensionnement type van :**
- Autonomie 1–2 jours (événements, chantiers) : 20–60 kWh LFP
- Recharge : panneau PV toit 400–800 Wc + chargeur shore power 7–22 kW
- Poids LFP 20 kWh : ~150–200 kg (module complet)

**Réglementation transport :**
- Batteries installées dans véhicule (en fonctionnement) : pas soumises ADR
- Batteries transportées comme marchandise : ADR applicable (UN 3480, UN 3481)
- Véhicule transformé (aménagement permanent) : homologation DREAL en France (R44.04 si <3,5t)
- Câblage : norme UTE C 15-100 / IEC 60364 pour installations à bord

---

## 7. Sécurité : Thermal Runaway et gestion du risque

### 7.1 Mécanisme du thermal runaway
Le thermal runaway est une réaction exothermique auto-entretenue qui se produit quand la chaleur générée dans la cellule dépasse sa capacité d'évacuation.

**Séquence :**
1. Déclencheur : surchauffe externe, surcharge, court-circuit interne, choc mécanique
2. Électrolyte liquide (Li-ion) : décomposition, génération de gaz (CO, CO₂, HF, hydrocarbures)
3. Emballement thermique : température monte à 200–900°C selon chimie
4. Éjection de gaz inflammables/toxiques + risque d'incendie
5. Propagation possible aux cellules adjacentes (thermal propagation)

**Sensibilité par chimie :**
- LFP : seuil de déclenchement ~270°C — le plus résistant
- NMC : seuil ~200°C
- NCA : seuil ~150°C
- VRFB : pas de thermal runaway (électrolyte aqueux) — avantage sécurité fondamental

### 7.2 Détection et alarme précoce
- **Capteurs de température** : surveillance multi-points, seuils d'alarme progressifs (alerte / arrêt / évacuation)
- **Capteurs de gaz** : détection CO, H₂, HF avant emballement visible
- **BMS surveillance** : delta-T inter-cellules, voltage deviation, résistance interne
- **Early Warning Systems (EWS)** : systèmes dédiés (ex : Kidde, Wagner TITANUS) — NFPA 855 les recommande

### 7.3 Ventilation

**Calcul de base :**
```
Débit ventilation requis = Volume gaz potentiel dégagé (pire cas) × Facteur de sécurité / Concentration limite d'explosion (LEL)
```
- Ventilation naturelle : possible pour installations < 10 kWh dans volumes > 15 m³
- Ventilation forcée : obligatoire pour locaux fermés > 10 kWh (renouvellement air : 10–20 vol/heure en cas de détection gaz)
- Rejet de l'air vicié : toujours vers l'extérieur, jamais vers un espace occupé

### 7.4 Systèmes de suppression incendie
**NFPA 855 et standards européens :**
- Sprinkler eau : le plus fréquent pour installations grid-scale (refroidit l'environnement mais n'éteint pas le thermal runaway interne)
- Agents propres (FM-200, Novec 1230) : pour salles équipements sensibles — inefficaces contre thermal runaway Li-ion
- CO₂ haute pression : risque asphyxie, limité aux locaux non occupés
- **Systèmes intégrés au cabinet** : injection directe dans le pack (Kidde, Amerex) — tendance pour BESS conteneurisés

**Points critiques :**
- Distance minimale entre BESS et bâtiments : selon réglementation locale (NFPA 855 : 1–3 m selon taille)
- Coupure d'urgence (emergency disconnect) : obligatoire, accessible et clairement identifiée
- Plan d'intervention pompiers : obligatoire pour installations > 500 kWh en France (arrêté ICPE)
- Fiches de données de sécurité (FDS) du module batterie : transmises aux SDIS

### 7.5 Distances de séparation (NFPA 855 — référence internationale)

| Capacité du système | Distance bâtiment habité | Distance limite parcelle |
|--------------------|------------------------|------------------------|
| < 50 kWh | Intérieur autorisé (contraintes spécifiques) | — |
| 50–600 kWh | 1–3 m | 1–3 m |
| 600 kWh–5 MWh | 5–15 m | 3–10 m |
| > 5 MWh | Étude site spécifique | Étude site spécifique |

---

## Sources
- [IEC Certifications for BESS — SunLith Energy](https://sunlithenergy.com/iec-certifications-for-bess/)
- [UL 9540 Compliance Guide — Kite Compliance](https://www.kitecompliance.ai/vertical-compliance/ul9540-compliance-guide-navigating-energy-storage-safety-standards)
- [Global Standards Certifications for BESS — Battery Design](https://www.batterydesign.net/global-standards-certifications-for-bess/)
- [BESS Certifications Complete 2026 Guide — SunLith Energy](https://sunlithenergy.com/bess-certifications-guide/)
- [Safety Standards for BESS — EticaAG](https://eticaag.com/key-safety-standards-battery-energy-storage-systems/)
- [Comprehensive Guide to BESS Safety — EticaAG](https://eticaag.com/comprehensive-guide-to-bess-safety-fire-safety/)
- [NFPA 855 Guide Fire Safety — AENR Store](https://www.anernstore.com/blogs/off-grid-solar-solutions/nfpa-855-energy-storage-fire-codes)
- [NFPA 855: Battery Fire Safety Standards — Electrical Trader](https://electricaltrader.com/blogs/news/nfpa-855-battery-fire-safety-standards)
- [BESS Safety — The Hartford](https://www.thehartford.com/insights/home-workplace-safety/reducing-fire-hazards-in-bess)
- [What is C-Rate in BESS — Amble Sun](https://amblesun.solar/blog/what-is-the-c-rate-in-bess/)
- [How to Size a BESS — Ampowr](https://ampowr.com/how-to-size-battery-energy-storage-system/)
- [How to Size a BESS for an SME — Calder Electrical](https://calderelectricalservices.co.uk/how-to-size-a-bess-for-an-sme/)
- [Technical Specifications of BESS — Flex Power](https://flex-power.energy/school-of-flex/technical-specifications-battery-storage-bess/)
- [UL 1973 Certification — EticaAG](https://eticaag.com/ul-1973-certification-for-bess/)
- [Battery Energy Storage Regulatory Compliance Guide — UL Solutions](https://www.ul.com/resources/your-guide-battery-energy-storage-regulatory-compliance)
- [Lithium battery transport — Flash Battery](https://www.flashbattery.tech/en/blog/lithium-battery-transport/)
- [Lithium batteries as dangerous goods — Safety Training Plus](https://www.safetytrainingplus.com/en/blog/lithium-batteries-as-dangerous-goods-which-guidelines-apply/)
