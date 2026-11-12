# WP03 — Budget énergie & gate « 60 jours » (PPK2)

**Projet :** WildNexus P0 — M-02/M-03
**Work-package :** WP03 (Énergie & mesure) — critère de sortie P0
**Rédaction :** Dobby 🦉 — consolidation initiale 2026-10-29
**Révision :** 2026-11-05 — modèle complet, correction des seuils et des règles de sécurité
**Statut :** Protocole à exécuter — autonomie non démontrée

> **But :** mesurer avec le PPK2 la chaîne complète du nœud et déterminer si la cible de 60 jours est atteinte au profil de référence de 10 événements/jour. Aucune autonomie ne doit être présentée comme garantie avant ces mesures et l'EVT 30 jours.

---

## 0. Gates électriques avant toute mesure

### Rail de sortie

La cible est **3,3 V ± 3 % en charge**, y compris pendant les pics caméra, IA, SD, IR et LoRa. Le feedback du TPS62840 doit être configuré en conséquence. Le courant maximal de 750 mA du composant ne prouve pas que la carte complète tolère les pics combinés.

### Entrée du régulateur et pack 8×AA

- Le TPS62840 a une plage de fonctionnement recommandée de **1,8 à 6,5 V** selon Texas Instruments.
- L'architecture retenue reste **8×AA en 4S2P**, mais sa tension maximale réelle doit être démontrée avant connexion, en particulier avec des L91 neuves et à froid.
- **6 AA en série sont interdits** sur ce régulateur : environ 9 V nominal, hors plage.
- Si le pack 4S2P ne garantit pas une entrée ≤6,5 V dans tous les cas, arrêter et réviser ADR-005 ; ne pas « essayer pour voir ».
- Ne jamais injecter 3,3 V dans une broche DevKit marquée 5 V. Le schéma exact et le point d'injection doivent être validés avant mesure.
- SOP-10 reste suspendue jusqu'à la levée de ces gates.

Sécurité générale : sortie d'alimentation OFF avant câblage, polarité vérifiée, aucune alimentation USB concurrente, et câblage PPK2 conforme au manuel Nordic officiel.

---

## 1. Briques existantes

| Brique | Fichier | Usage |
|---|---|---|
| Deep sleep 30 s | `PROTOCOLES/SOP-02-deep-sleep-30s.md` | Firmware et mesure du courant de veille |
| Mesure deep sleep PPK2 | `PROTOCOLES/SOP-03-ppk2-deep-sleep.md` | Acquisition µA |
| Réveil court 20 cycles | `PROTOCOLES/SOP-04-wake-short-20-cycles.md` | Profil de réveil |
| Cycle événement simulé | `PROTOCOLES/SOP-05-simulation-cycle-evenement.md` | Premier profil fonctionnel, insuffisant seul pour l'autonomie produit |
| Alimentation AA + buck | `PROTOCOLES/SOP-10-batterie-aa-buck.md` | Suspendue jusqu'aux gates électriques |
| Benchmark IA | `PROTOCOLES/SOP-11-benchmark-edge-ai.md` | Mesure du modèle réellement retenu |
| Budget audio | `PROTOCOLES/SOP-18-budget-energie-audio.md` | Mesures I2S, FFT, WAV et SD |
| Gabarit mesures | `PROTOCOLES/2026-06-08_mesures-esp32s3-ppk2_template.csv.md` | Saisie des données |
| Modèle autonomie | `03_ENERGIE_AUTONOMIE/WildNexus_P0_Autonomy_Model.xlsx` | Consolidation des scénarios |

---

## 2. Mesures requises — événement caméra

Tous les états doivent être mesurés avec les périphériques réellement actifs. Des délais logiciels simulant une caméra ou une radio absente ne constituent pas une mesure produit.

| État | Point de mesure | Courant | Durée | Énergie ou charge |
|---|---|---:|---:|---:|
| Deep sleep carte complète | Batterie et/ou rail 3,3 V, point horodaté | ___ | continu | ___ |
| Réveil PIR | ___ | ___ | ___ | ___ |
| Capture caméra | ___ | ___ | ___ | ___ |
| Inférence du modèle retenu | ___ | ___ | ___ | ___ |
| Pulse IR nocturne | ___ | ___ | ___ | ___ |
| Écriture image + sidecar SD | ___ | ___ | ___ | ___ |
| Transmission LoRa TX, sans retry | ___ | ___ | ___ | ___ |
| Transmission LoRa avec retries | ___ | ___ | ___ | ___ |
| **Total événement jour** | — | — | — | **___** |
| **Total événement nuit** | — | — | — | **___** |

Le ratio jour/nuit doit être explicite pour chaque scénario. Un scénario conservateur avec IR sur chaque événement doit être calculé séparément.

## 3. Mesures requises — cycles audio et maintenance

Ces charges sont obligatoires dans le budget P0 ; elles ne peuvent pas être remplacées par une estimation non datée.

| Cycle | Fréquence nominale | États inclus | Énergie batterie par cycle | Énergie batterie/jour |
|---|---:|---|---:|---:|
| FFT stéréo | 96/jour | réveil, alimentation micros, I2S, acquisition, FFT, sidecar JSON, LoRa spectral | ___ | ___ |
| Clip WAV 3 s | 24/jour | réveil, micros, I2S, WAV, écriture SD, sidecar JSON | ___ | ___ |
| Configuration / maintenance | à définir | Wi-Fi/BLE, extraction, provisioning | ___ | ___ |
| Retransmissions radio | mesurée | tentatives supplémentaires et attente RX | ___ | ___ |

---

## 4. Calcul d'autonomie — Wh à la batterie

Le calcul de référence se fait en **énergie (Wh) côté batterie**. Cela évite de mélanger les mAh du pack 4S2P avec ceux du rail 3,3 V.

```text
E_batt_jour = E_veille_batt
            + N_jour × E_evenement_jour_batt
            + N_nuit × E_evenement_nuit_batt
            + 96 × E_FFT_batt
            + 24 × E_clip_batt
            + E_retransmissions_batt
            + E_maintenance_batt

autonomie(jours) = E_batt_utilisable / E_batt_jour
```

Règles :

1. Privilégier une mesure directe côté batterie : `E = V_batt × I_batt × durée` pour chaque état.
2. Si une mesure est réalisée à 3,3 V, utiliser `E_batt = E_3V3 / rendement`, avec le rendement mesuré au niveau de charge concerné. Ne pas appliquer un rendement unique non mesuré à tous les états.
3. `E_batt_utilisable` tient compte de la chimie, de la température, du courant de décharge, du vieillissement, de la coupure basse et de la dispersion des piles. La capacité nominale seule est interdite pour un verdict Go.
4. Si des mAh sont utilisés dans un tableau annexe, la tension de référence doit figurer dans chaque ligne.
5. La capacité théorique L91 du pack 4S2P est d'environ 7 000 mAh à 6 V nominal, soit environ 42 Wh ; ce n'est pas une capacité utilisable mesurée.

---

## 5. Scénarios et seuils

| Scénario | Événements caméra/jour | Jour/nuit | Usage |
|---|---:|---|---|
| Référence | 10 | ratio documenté + cas 100 % IR en sensibilité | Gate 60 jours |
| Intermédiaire | 30 | ratio documenté | Robustesse |
| Stress | 72 | ratio documenté + cas défavorable | Robustesse, pas promesse commerciale |

| Mesure | Go | Orange | No-Go |
|---|---|---|---|
| Deep sleep carte complète | <100 µA | 100–200 µA, cause et correction documentées | >200 µA |
| Charge/énergie par événement | <1,5 mAh équivalent batterie | 1,5–2,5 mAh | >2,5 mAh |
| Autonomie au scénario de référence | ≥60 jours | 45–60 jours | <45 jours |
| Stabilité | 100 cycles sans erreur | 1–2 erreurs isolées expliquées | Blocage récurrent |

L'acceptation exige **<1,5 mAh par événement**, et non ≥1,5 mAh. Pour comparer en mAh, le point de mesure et la tension doivent être identiques à ceux du seuil officiel ; sinon conserver le seuil comme référence historique et documenter une conversion en Wh validée.

---

## 6. Livrables et acceptation WP03

1. Gates électriques consignés : tension maximale pack, schéma du point d'injection et câblage PPK2 validés.
2. Tableaux caméra, audio et maintenance complétés avec fichiers PPK2 datés.
3. Budget énergie en Wh pour 10/30/72 événements/jour, incluant jour/nuit, retransmissions et pertes.
4. Autonomie extrapolée avec hypothèses de capacité utilisable et verdict Go/Orange/No-Go.
5. Tension 3,3 V confirmée sous tous les pics et stabilité de 100 cycles documentée.
6. Mise à jour de `progress.md` et de `WildNexus_P0_Autonomy_Model.xlsx`.

**Acceptation WP03 :** autonomie extrapolée ≥60 jours au scénario de référence, charge par événement <1,5 mAh ou seuil Wh équivalent validé, deep sleep <100 µA en cible carte complète, et aucune gate de sécurité ouverte.

Le résultat DevKit reste un résultat prototype. Il ne devient une caractéristique produit qu'après reproduction sur le matériel final et EVT 30 jours. La validation du PCB nu ou final ne doit pas être présentée comme déjà réalisée si ce matériel appartient à une phase ultérieure.

---

## 7. Séquence d'exécution

1. Lever les gates électriques et rouvrir SOP-10.
2. Relever veille, réveil et cycle caméra réel, puis IA jour/nuit.
3. Mesurer les 96 FFT, 24 clips, écritures SD et retransmissions LoRa.
4. Reporter les données brutes et les conversions dans le modèle.
5. Calculer les scénarios et documenter les incertitudes.
6. Si No-Go, arbitrer avec [[Forge]]/[[Castor]] à partir des mesures ; aucune optimisation à l'aveugle.
7. Confirmer ensuite par EVT 30 jours et mettre à jour la fiche produit avec le résultat réellement observé.

---

*Révision 2026-11-05 — cycles audio, Wh, pertes, froid, retransmissions et profils jour/nuit ajoutés ; inversion du seuil 1,5 mAh corrigée ; anciennes instructions électriques dangereuses bloquées.*
