# WP03 — Budget énergie & gate « 60 jours » (PPK2)

**Projet :** WildNexus P0 — M-02/M-03
**Work-package :** WP03 (Énergie & mesure) — **critère de sortie P0**
**Rédaction :** Dobby 🦉 — 2026-10-29 (consolidation)
**Statut :** Doc de pilotage — **fédère l'existant**, ne remplace pas les SOPs.

> **But** : prouver (mesure PPK2) que le nœud tient **≥ 60 jours** avec piles AA (L91, 8×AA 4S2P), et **verrouiller la tension de rail**. C'est le point bloquant n°1 signalé par la revue R&D.

---

## 0. Décision à trancher d'emblée — tension de rail

| Source | Tension buck TPS62840 |
|---|---|
| Fiche `F1_FIELD.md` | **3,0 V** (à vérifier — valeur suspecte) |
| `SOP-10-batterie-aa-buck.md` | **3,3 V ± 0,1 V** (cible de test) |
| Datasheet ESP32-S3 / OV5640 / MEMS | 3,3 V nominal ; **3,0 V = limite basse marginale** |

**➜ Décision WP03 : rail = 3,3 V.** Configurer le feedback du TPS62840 pour 3,3 V. La valeur « 3,0 V » de la fiche F1 est corrigée (erreur) sauf preuve contraire au banc. **Gate** : si le buck ne tient pas 3,3 V en charge (pics caméra/IR), revoir le dimensionnement (inductance, capa) avant de poursuivre.

---

## 1. Briques existantes (ne pas dupliquer — carte des SOPs)

| Brique | Fichier | Usage |
|---|---|---|
| Deep sleep 30 s | `PROTOCOLES/SOP-02-deep-sleep-30s.md` | Firmware + mesure courant veille |
| Mesure deep sleep PPK2 | `PROTOCOLES/SOP-03-ppk2-deep-sleep.md` | Source Meter, mesure µA |
| Réveil court 20 cycles | `PROTOCOLES/SOP-04-wake-short-20-cycles.md` | Profil réveil |
| Cycle événement simulé | `PROTOCOLES/SOP-05-simulation-cycle-evenement.md` | Séquence 11 s (PIR 2s + cam 5s + SD 2s + LoRa 2s) |
| **Alim AA + buck** | `PROTOCOLES/SOP-10-batterie-aa-buck.md` | 6×AA banc, buck 3,3 V, mesure Ampère Meter |
| Protocole global PPK2 | `PROTOCOLES/Manuel de protocole technique _ Tests de consommation ESP32-S3 & PPK2.md` | Phases A-E + grille Go/No-Go |
| Gabarit mesures | `PROTOCOLES/2026-06-08_mesures-esp32s3-ppk2_template.csv.md` | Saisie |
| Modèle autonomie | `03_ENERGIE_AUTONOMIE/WildNexus_P0_Autonomy_Model.xlsx` | Calcul autonomie |

> ⚠️ Sécurité (voir SOP-03/SOP-10) : **jamais USB + PPK2 simultanément** ; sortie PPK2 OFF avant câblage ; VOUT→5V, GND→GND ; couper si >500 mA.

---

## 2. Budget énergie à formaliser (gabarit à remplir)

Objectif : passer des courants mesurés à un **mAh/événement**, puis à l'autonomie.

| État | Courant (mesuré PPK2) | Durée | Charge (mAh) |
|---|---|---|---|
| Deep sleep (veille) | ___ µA | (continu) | ___ mAh/jour |
| Réveil PIR | ___ mA | ~2 s | ___ |
| Capture caméra + IA | ___ mA | ~5 s | ___ |
| Pulse IR nocturne | ___ mA | <5 s | ___ |
| Écriture SD | ___ mA | ~2 s | ___ |
| Transmission LoRa TX | ___ mA | ~2 s | ___ |
| **Total / événement** | — | ~11 s actif | **Σ = ___ mAh** |

**Seuils de référence (grille officielle du Manuel PPK2) :**

| Mesure | Go | Orange | No-Go |
|---|---|---|---|
| Deep sleep | **< 100 µA** | 100-150 µA | > 200 µA |
| Charge / événement | **< 1,5 mAh** | 1,5-2,5 mAh | > 2,5 mAh |
| Autonomie | **≥ 60 j** | 45-60 j | < 45 j |
| Stabilité | 100 cycles sans erreur | 1-2 erreurs isolées | blocage récurrent |

> 📌 **Note DevKit** : le DevKit (régulateur AMS1117 + LEDs) gonfle la conso ; ~150 µA en deep sleep y est une **contrainte plateforme documentée**. La validation finale se fait sur **PCB nu** (P1).

---

## 3. Calcul d'autonomie (à renseigner)

```
Capacité batterie 8×AA 4S2P (L91)  ≈ 7 000 mAh (à ~6 V nominal)
mq_jour = I_veille(mA) × 24 h  +  N_évènements/jour × Charge_évènement(mAh)
autonomie(jours) = Capacité_mAh / mq_jour
```

**Hypothèses de dimensionnement (à fixer explicitement) :**
- Fiche produit F1 : **10 événements/jour** → cible 60 j.
- Manuel PPK2 (grille) : autonomie évaluée à **3 événements/heure (≈72/j)** — **hypothèse bien plus sévère**.
- **➜ Décision WP03** : établir l'autonomie **sur 3 scénarios** (10, 30, 72 événements/jour) pour lever l'ambiguïté et publier la courbe. Le critère Go = 60 j **au profil de référence F1 (10/j)** ; le scénario 72/j informe la robustesse.

---

## 4. Livrables & critères d'acceptation (WP03)

1. **Tableau de mesures PPK2 complété** (gabarit CSV) — états du §2.
2. **Budget énergie signé** : mAh/événement + mAh/jour pour 10/30/72 évt/j.
3. **Autonomie extrapolée** sur les 3 scénarios ; verdict Go/Orange/No-Go.
4. **Tension rail confirmée à 3,3 V** en charge (pics caméra/IR).
5. **Rapport de stabilité** (100 cycles, SOP-04).
6. Mise à jour du `progress.md` (tracker M-02) + `WildNexus_P0_Autonomy_Model.xlsx`.

**Acceptation WP03 = critère de sortie P0** : autonomie extrapolée **≥ 60 j au profil F1 (10 évt/j)**, deep sleep **< 100 µA** (orange ≤150 µA toléré sur DevKit), ≥1,5 mAh maîtrisé par événement.

---

## 5. Séquence d'exécution recommandée

1. **SOP-10** : valider buck 3,3 V seul (avant ESP32).
2. **SOP-02/03** : deep sleep → courant de veille.
3. **SOP-04** : réveil court, 20 cycles.
4. **SOP-05** : cycle événement simulé (11 s) → charge/événement.
5. Reporter dans le **modèle d'autonomie** + grille Go/No-Go → verdict.
6. Si No-Go : arbitrage avec [[Forge]]/[[Castor]] (optimisation i2s/caméra/rail) — **avant** toute optimisation « à l'aveugle »** (principe WP03 : mesurer d'abord).

---

*Consolidation WP03 — fédère SOP-02/03/04/05/10 + Manuel PPK2 + modèle d'autonomie. Ne remplace pas les SOPs opérationnels.*
