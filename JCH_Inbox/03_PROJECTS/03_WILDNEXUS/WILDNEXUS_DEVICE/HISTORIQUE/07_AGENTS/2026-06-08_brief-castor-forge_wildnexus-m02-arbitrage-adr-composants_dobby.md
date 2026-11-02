# Brief — Arbitrage M-02 : Contradictions ADR × Contrainte Composants

**Date :** 2026-06-08  
**De :** [[Dobby]]  
**Pour :** [[Castor]] + [[Forge]]  
**Projet :** [[WildNexus]]  
**Objet :** Arbitrage sur 3 contradictions ADR confirmées par NotebookLM, avec contrainte réelle des composants disponibles

---

## 1. Contexte

NotebookLM a audité le protocole M-02 (`2026-06-08_protocole-m02-esp32s3-ppk2.md`) contre les ADR et le Scope Lock. Trois contradictions sont confirmées. Mais l'analyse doit tenir compte des composants **effectivement disponibles** au 2026-06-08.

### État réel des composants

| Composant | Statut | Disponible ? |
|-----------|--------|:---:|
| ESP32-S3 DevKit × 2 | Commandé + reçu | ✅ |
| PPK2 | Commandé 2026-06-05 | ❓ |
| Panier Mouser (~162 €) | Non commandé | ❌ |
| — Micro MEMS I2S (A06) | Dans panier | ❌ |
| — PIR Panasonic (A05) | Dans panier | ❌ |
| — Buck TPS62840 (A08) | Dans panier | ❌ |
| — LEDs IR 850/940nm | Dans panier | ❌ |
| — Piles AA lithium (A16) | Dans panier | ❌ |
| — Breadboard + alim labo | Dans panier | ❌ |
| Caméra OV5640 DVP M12 | Bloquée Arducam | ❌ |
| Module LoRa SX1262 | Pas dans le panier | ❌ |
| Module microSD SPI | Pas dans le panier | ❌ |
| YubiKey PIV / HSM | Non commandé | ❌ |

**Bilan :** seuls l'ESP32-S3 et le PPK2 sont potentiellement en mains. Tous les périphériques et le banc d'alimentation sont indisponibles.

---

## 2. Les 3 contradictions confirmées

### Contradiction 1 — Edge AI absent (ADR-010)

**Ce que dit l'ADR-010 :**
> Le benchmark MobileNet-SSD (latence < 2s, recall > 90% jour, > 80% nuit) doit être exécuté avant fermeture M-02. Si latence > 2s ou OOM → trigger migration MCU (STM32U5/RV1106).

**Réalité matérielle :**
- Pas de caméra OV5640 (bloquée Arducam)
- Pas de firmware MobileNet-SSD compilé
- Pas de LEDs IR pour test nuit
- → **Impossible de benchmarker l'Edge AI aujourd'hui**

**Question [[Castor]] + [[Forge]] :**
Faut-il ajouter une Phase K (Edge AI Bench) comme placeholder dans le protocole, avec conditions de déclenchement (dès réception OV5640 + firmware), ou considérer que ce benchmark est repoussé hors M-02 ? Si repoussé, l'ADR-010 doit être amendé (le trigger de migration MCU devient conditionnel à disponibilité caméra).

### Contradiction 2 — Micro MEMS absent (Scope Lock)

**Ce que dit le Scope Lock :**
> Capture audio locale courte via micro mono (Knowles SPH0645LM4H-B, réf A06) — dans le périmètre P0.

**Réalité matérielle :**
- A06 est dans le panier Mouser, non commandé
- → **Test audio impossible aujourd'hui**

**Question [[Castor]] + [[Forge]] :**
Le micro MEMS est-il vraiment P0 now, ou P1 later ? Si P0 maintenu → ajouter Phase L placeholder et commander le panier Mouser. Si P1 → amender le Scope Lock.

### Contradiction 3 — Provisioning absent (ADR-011)

**Ce que dit l'ADR-011 :**
> Le test de provisioning complet (lecture serial → dérivation clés → gravure eFuse → verrouillage) doit être inclus dans WP04 pour M-02. Script `wildnexus_provision.py` à développer avant M-02.

**Réalité matérielle :**
- Pas besoin de matériel externe pour un test simplifié (lecture serial + gravure eFuse dummy)
- Pas de YubiKey PIV → dérivation complète HKDF impossible
- Script `wildnexus_provision.py` n'existe pas
- → **Provisioning simplifié faisable, provisioning complet bloqué**

**Question [[Castor]] + [[Forge]] :**
Faut-il ajouter une Phase M (Provisioning) au protocole avec un test simplifié (lecture serial → eFuse dummy sans YubiKey), ou exiger le provisioning complet (script + YubiKey) et le bloquer tant que le matériel n'est pas là ?

---

## 3. M-02 minimal viable — ce qui est testable aujourd'hui

Avec les composants disponibles, le protocole M-02 peut exécuter :

| Phase | Contenu | Faisable ? |
|-------|---------|:----------:|
| A | Vérification ESP32-S3 alive | ✅ |
| B | Firmware deep sleep minimal | ✅ |
| C | Mesure PPK2 Source Meter | ✅ (si PPK2 reçu) |
| D | Mesure référence active | ✅ |
| E | Simulation cycle WildNexus | ✅ |
| F | Test microSD SPI | ❌ Pas de module |
| G | Test LoRa SX1262 | ❌ Pas de module |
| H | Test caméra OV5640 | ❌ Pas de caméra |
| I | Test PIR | ❌ Pas de capteur |
| J | Test alimentation AA + buck | ❌ Pas de buck ni piles |
| K | Edge AI Bench (nouveau) | ❌ Pas de caméra ni firmware |
| L | Audio MEMS (nouveau) | ❌ Pas de micro |
| M | Provisioning eFuse (nouveau) | 🟡 Partiel possible |

---

## 4. Questions à trancher

1. **Stratégie M-02 :** exécuter partiel maintenant (A→E) ou attendre la livraison du panier Mouser pour tout faire d'un coup ?

2. **Benchmark Edge AI :** placeholder dans le protocole ou amendement ADR-010 pour décaler le trigger ?

3. **Micro MEMS :** P0 maintenu (→ commander panier Mouser) ou rétrogradé P1 (→ amender Scope Lock) ?

4. **Provisioning :** test simplifié sans YubiKey maintenant, ou attente du script complet ?

5. **Commande panier Mouser :** JCH doit-il déclencher la commande maintenant (~162 €) pour débloquer les phases F→J ?

6. **Module LoRa + microSD :** absents du panier Mouser — oversight ou volontaire ? À ajouter ?

---

## 5. Sortie attendue

- Arbitrage clair sur chaque contradiction (go / no-go / amendement ADR)
- Recommandation sur le calendrier M-02 (partiel maintenant vs complet plus tard)
- Si contradiction ADR maintenue → proposition d'amendement
- Liste des commandes à déclencher sans délai
