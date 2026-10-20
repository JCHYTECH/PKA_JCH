# Brief équipe — Changement architecture batterie WildNexus P0

**De :** [[Dobby]] 🦉  
**Date :** 2026-05-18  
**Priorité :** Haute — impacte PCB, boîtier, firmware et budget  
**Référence :** `ADR-005 v0.2`

---

## Décision JCH

**La solution batterie WildNexus P0 passe au modèle industrie caméra de chasse : 8 piles AA standard fournies par l'utilisateur.**

Fini le LiFePO4 18650 + BMS + CN3791. Le compartiment arrière du boîtier accueille 8 piles AA (alcaline, NiMH rechargeable, ou lithium) — exactement comme un Browning ou Reconyx.

---

## Ce qui change par WP

### [[Forge]] + [[Castor]] — WP02 Hardware (IMPACT FORT)

**Supprimer du schéma PCB :**
- Cellules 18650 LiFePO4 et leur support
- Circuit BMS
- CN3791 MPPT et tout le circuit de charge solaire
- Connecteur batterie 18650

**Ajouter au schéma PCB :**
- Régulateur buck TPS62840 (Texas Instruments) — Iq = 5 µA, entrée 4.0–6.5 V, sortie 3.3 V
- Connecteur vers holder 8× AA 4S2P (4 en série × 2 parallèles = 4.8–6 V)
- Diviseur résistif ADC pour monitoring tension batterie (4.8 V → plage [[ESP32-S3]])

Les MOSFET de coupure périphériques **restent inchangés**.

---

### [[Chouette]] — ADR-006 Boîtier (IMPACT FORT)

Le compartiment batterie change complètement :
- Prévoir logement pour **2 holders 4× AA** (standard du commerce, ~15 × 57 × 57 mm chacun)
- Accessible **sans outil** depuis l'extérieur (couvercle séparé ou face arrière amovible)
- Joint IP67 sur le compartiment batterie — priorité absolue
- La face plane pour panneau solaire **n'est plus une contrainte de forme P0** — prévoir simplement un point de fixation optionnel pour P1

---

### [[Forge]] — WP03 Firmware (IMPACT MODÉRÉ)

- Monitoring tension batterie via ADC : seuil alerte < 4.0 V, coupure préventive < 3.6 V
- Supprimer tout code de gestion charge / MPPT
- La courbe de décharge AA est différente de LiFePO4 — documenter dans WP03

---

### [[Bruno]] — Budget + Supply register (IMPACT MODÉRÉ)

**Retirer du supply register :**
- 2× 18650 LiFePO4 — remplacé
- CN3791 MPPT — supprimé
- Panneau solaire 6V 2W — différé P1, sortir du budget P0

**Ajouter au supply register :**
- TPS62840 (ou TPS563201 comme alternative) — Mouser/DigiKey, ~1–2 €
- 2× holders 4× AA (standard, AliExpress/Amazon, ~2–3 € les deux)

**Impact budget :** économie nette ~30–40 €. Les piles AA ne sont **pas dans l'enveloppe 1 000 €** — achat utilisateur.

---

### [[Nova]] + [[Clio]] — WP04 Edge AI (IMPACT NUL)

Aucun changement sur le pipeline IA. Pour information uniquement.

---

### [[Chouette]] — WP05 EVT terrain (INFORMATION)

Le protocole terrain EVT s'en trouve simplifié : remplacement batterie = 8 piles AA standard achetées en supermarché. Prévoir un stock de piles de rechange dans le kit terrain.

---

## Ce qui ne change pas

- Objectif deep sleep < 100 µA
- MOSFET de coupure périphériques
- Nordic PPK2 obligatoire pour benchmark M-02
- Tests M-02 énergie (cycle complet, deep sleep)

---

*Référence complète : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/ADR/ADR-005-energie-autonomie-p0.md`*
