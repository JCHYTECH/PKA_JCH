# Brief équipe — Activation pendant l'absence JCH

**De :** Dobby 🦉  
**Date :** 2026-05-18  
**Contexte :** JCH part à l'étranger. Tout ce qui peut avancer sans lui doit avancer.  
**Référence :** `WILDNEXUS_P0_BRIEF_JCH.md`

---

## Ce qui est débloqué — décidez et exécutez

### Chouette — 3 actions GO

**O-03 · Boîtier IP67**  
Sélectionner et commander 2 boîtiers parmi Hammond 1555 / Spelsberg TK series.  
Critères ADR-006 : IP67, ≤ 150×100×60 mm, ABS ou PC, couleur sombre, joint torique silicone.  
Contrainte nouvelle : le couvercle ou la face arrière doit permettre un accès rapide au compartiment 8× AA sans outil.  
Achat < 50 € unitaire → décision Chouette, pas besoin d'escalader.

**O-04 · PIR (après O-03)**  
Sélectionner la variante Panasonic EKMB adaptée au FOV du boîtier retenu.  
Critère : courant ≤ 5 µA, FOV corridor de passage, disponible Mouser BE.  
Acheter 4 pièces (2 nœuds + 2 spare).

**O-05 · Shortlist sites EVT**  
Préparer 2–3 sites candidats en forêt belge : couvert dense, passage faune connu, accessibilité raisonnable.  
JCH confirme au retour — la shortlist ne bloque aucun WP en cours.

---

### Nova + Chouette — décision IR

**O-02 · Longueur d'onde IR**  
Décision : **850 nm par défaut.**  
Raison : portée supérieure, standard industrie caméra de chasse, capteur OV5640 NoIR mieux calibré à 850 nm.  
Si l'EVT révèle une perturbation comportementale sur les espèces cibles → basculer 940 nm en P1.  
Commander les LEDs IR 850 nm (lot × 4 par nœud, × 2 nœuds = 8 LEDs minimum + spare). Mouser BE.

---

### Forge + Castor — WP02 et WP03 démarrent

**WP02 — Schéma électronique**  
Tous les composants principaux sont fixés. Démarrer le schéma :
- ESP32-S3 + OV5640 DVP M12 + RAK3172 + TPS62840 + MOSFETs coupure × 4 + holders AA 4S2P + PIR (footprint EKMB générique en attendant O-04)
- PCB ≤ 150 × 100 mm
- Un seul presse-étoupe antenne LoRa (LTE-M : footprint mécanique réservé, non câblé)

**WP03 — Architecture firmware**  
Rédiger la machine d'états et l'architecture logicielle :
- États : SLEEP → PIR_WAKE → CAPTURE → INFER → STORE → LORA_TX → SLEEP
- Stack radio : LoRa P2P uniquement (RadioLib)
- Monitoring ADC tension AA : seuils 4.0 V / 3.6 V
- Wi-Fi désactivé en usage terrain

---

### Bruno — Supply register

Compléter le supply register avec :
- Liens fournisseurs directs pour chaque composant
- Prix livrés Liège (seuil livraison gratuite si connu)
- Stratégie de centralisation des commandes (Mouser prioritaire, DigiKey second panier)

---

### Renard — Préparation note licence

**O-01 · Licence open source** *(note pour JCH au retour)*  
Préparer une note comparative ≤ 2 pages :
- Options : MIT/Apache (OSI pure) vs Creative Commons NC vs dual-license vs usage-restriction propriétaire
- Implications FTO et compatibilité contributions externes
- Recommandation Renard avec justification
- JCH décide au retour — non bloquant avant M-03

---

## Ce qui n'attend pas

WP02 et WP03 peuvent démarrer dès maintenant. Les décisions boîtier (O-03) et PIR (O-04) s'intègrent au schéma sans refonte — les footprints peuvent être ajoutés quand Chouette confirme les références.

*Référence : `WILDNEXUS_P0_BRIEF_JCH.md` · `ADR-001` à `ADR-006`*
