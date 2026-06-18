# ADR-012 — Stratégie de test P0

**Date :** 2026-06-12  
**Statut :** proposé  
**Owner PKA :** [[Forge]] + [[Castor]] + [[Fourmi]]  
**Agent WildNexus :** `wildnexus-firmware-ulp` + `wildnexus-hardware-physical`  
**Jalon :** M-02 — Prototype banc  

## Contexte

M-02 est le premier jalon physique du projet : le système complet (ESP32-S3 + OV5640 + LoRa + microSD) doit fonctionner sur table avant tout déploiement extérieur. Sans stratégie de test formelle, les résultats M-02 ne sont pas reproductibles et le GO/NO-GO vers M-03 (terrain) n'est pas objectivable.

L'ADR-010 (Sécurité/RGPD Edge AI) impose deux points de réserve directement dépendants de cette stratégie :
- **R4** : Benchmark Edge AI ESP32-S3 (précision filtre animal vs non-animal)
- **R5** : Impact énergétique Edge AI × ADR-005 (autonomie 60 jours)

Un protocole partiel existe déjà (`2026-06-08_protocole-m02-esp32s3-ppk2.md`, Phases A–J) couvrant l'intégration de base. Ce document le complète avec les phases manquantes (K–P).

## Décision proposée

Adopter une stratégie de test en **3 phases + 1 suite de régression**, avec critères GO/NO-GO explicites par phase.

### Phase 1 — Intégration Hardware (banc M-02)

| # | Test | Outil | Critère GO | NO-GO |
|---|------|-------|------------|-------|
| H1 | ESP32-S3 alive (blink + Serial) | USB-C, moniteur série | Message `WildNexus ESP32-S3 alive` | Pas de réponse |
| H2 | Deep sleep carte nue | PPK2 Source Meter | < 100 µA | > 200 µA irréductible |
| H3 | Stabilité sleep/wake 100 cycles | Script automatique | 100 cycles OK | Blocage récurrent |
| H4 | microSD init + écriture + retour sleep | Firmware minimal | Fichier écrit, deep sleep retrouvé | Échec systématique |
| H5 | Caméra OV5640 capture + stockage SD | CameraWebServer ou script | Image 5MP écrite sur SD < 3s | Pas d'image, timeout |
| H6 | LoRa P2P ping ESP32 → ESP32 | RadioLib, SX1262 | Ping OK à 1m, RSSI > −30 dBm | Pas de lien |
| H7 | PIR trigger → wake → capture → LoRa TX | PPK2 + analyseur logique | Cycle complet < 5s, retour sleep | Blocage dans le pipeline |
| H8 | Buck TPS62840 rendement | PPK2, charge résistive | Rendement > 85% à 10 mA | < 70% ou oscillation |

### Phase 2 — Performance énergétique (banc M-02)

| # | Test | Outil | Critère GO | NO-GO |
|---|------|-------|------------|-------|
| E1 | Courant idle (deep sleep + PIR + buck) | PPK2, moyenne 1h | < 150 µA | > 300 µA |
| E2 | Courant capture + stockage SD | PPK2, pic | < 300 mA pendant < 3s | > 500 mA |
| E3 | Courant LoRa TX SF7 | PPK2, pulse | < 120 mA pendant < 100 ms | > 200 mA |
| E4 | Projection autonomie 60j (8× AA L91) | Calcul depuis mesures E1–E3 | ≥ 60 jours (modèle ADR-005) | < 45 jours |
| E5 | Impact Edge AI vs sans IA | PPK2, comparatif | Δ conso < 20% du budget total | Δ > 50% |

### Phase 3 — Benchmark Edge AI (banc M-02)

| # | Test | Données | Critère GO | NO-GO |
|---|------|--------|------------|-------|
| I1 | Précision filtre animal vs non-animal | 100 images test (50 positif, 50 négatif) | Précision > 85%, rappel > 90% | Précision < 70% |
| I2 | Faux positifs (branche, ombre, vent) | 50 images sans animal | < 10% faux positifs | > 25% |
| I3 | Latence inférence | Chronométrage firmware | < 500 ms sur ESP32-S3 | > 2s |
| I4 | Robustesse luminance (aube/crépuscule) | 20 images basse lumière | Précision maintenue > 75% | Effondrement < 50% |

### Phase 4 — Fiabilité et endurance

| # | Test | Condition | Critère GO | NO-GO |
|---|------|-----------|------------|-------|
| R1 | Endurance 24h continue | Boucle capture/stockage/sleep cyclique | 0 crash, 0 corruption SD | ≥ 1 crash |
| R2 | Undervoltage (batterie faible) | Alim variable 6V → 3V | Arrêt propre, redémarrage OK | Corruption FS, blocage |
| R3 | microSD hot-swap | Retrait/réinsertion sous tension | Détection, réinit OK | Crash, corruption |
| R4 | LoRa duty cycle saturation | Rafale 20 événements | Respect duty cycle, pas de perte silencieuse | Saturation non gérée |

### Suite de régression (continue)

Après M-02, une suite minimale de tests de régression est exécutée à chaque modification firmware ou hardware :
- H2 (deep sleep), H3 (stabilité 10 cycles), H4 (microSD), E1 (courant idle)
- Durée cible : < 15 minutes — exécutable par [[Fourmi]] sans supervision

## Alternatives considérées

| Option | Pour | Contre | Statut |
|--------|------|--------|--------|
| Tests manuels sans protocole | Rapidité apparente | Non reproductible, pas de traçabilité, JCH ne peut pas valider | Rejeté |
| Suite automatisée complète (CI/CD hardware) | Reproductibilité maximale | Infrastructure lourde (contrôleur GPIB, chambre climatique), prématuré P0 | P1 |
| Protocole papier + PPK2 | Reproductible, traçable, faible coût | Fastidieux pour régressions fréquentes | **Retenu P0** |

## Conséquences

- [[Fourmi]] devient l'opérateur principal des tests M-02 — exécute, documente, remonte les écarts.
- Chaque test produit un artéfact horodaté : capture PPK2, log série, image témoin.
- Les critères GO/NO-GO de ce document conditionnent le passage à M-03.
- Le protocole complet (Phases A–P) est consigné dans `08_TECH_NOTES/protocole-m02-complet.md`.

## Sources

- ADR-005 (énergie et autonomie)
- ADR-010 §R4–R5 (benchmark Edge AI, impact énergétique)
- Protocole existant `2026-06-08_protocole-m02-esp32s3-ppk2.md` (Phases A–J)
- BOM WP02 shortlist v0.2 — composants Option A

## Prochaine action

1. [[Forge]] + [[Castor]] révisent et complètent les critères si nécessaire
2. [[Fourmi]] prépare le banc : breadboard, PPK2, ESP32-S3, OV5640
3. Exécution Phase 1 dès réception des composants Option A
