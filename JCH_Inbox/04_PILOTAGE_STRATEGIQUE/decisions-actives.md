# Décisions actives — En attente de JC

last_updated: 2026-10-24

> **Fichier State** — Décisions non encore tranchées, en attente d'arbitrage explicite de JC.
> Lire avant toute suggestion d'action qui pourrait déjà avoir été tranchée.

---

## Format

| Date | Sujet | Contexte | Options | Décision |
|------|-------|----------|---------|----------|
| YYYY-MM-DD | Intitulé court | Pourquoi cette décision se pose | Option A / Option B | ⏳ En attente |

---

## Décisions en attente

### VETALYX — reliquats post-arbitrage (01/10)

| Date | Sujet | Contexte | Options | Décision |
|------|-------|----------|---------|----------|
| 2026-10-01 | Mécanique des 6 000 € restants | Capital 10 000 € souscrit, 4 000 € libéré. Comment formaliser les 6 000 € non libérés ? | A) Compte-courant / B) Augmentation future / C) Capital libéré seulement | ⏳ À préciser (Renard/notaire) |

### VETALYX — constat contrats v4/v2 (2026-10-24) — 🔁 à ré-arbitrer à la réponse des Chinois

> **Trace du constat Dobby** (`TEAM_Inbox/2026-10-24_dobby_analyse-contrats-vetalyx-v4-v2.md`). Ré-ouvrir quand DIAHO / Dixun / Li Yan répondront à notre envoi des contrats.

| # | Sujet | Constat | À trancher |
|---|-------|---------|------------|
| C1 | Véto DIAHO : statuts vs pacte | Décision #1 (01/10) = véto DANS les statuts. Note ISC + statuts v2 (05/10) = véto RETIRÉ des statuts, gardé au pacte. | Ré-injecter dans les statuts, ou confirmer l'inversion (discrétion ISC) ? |
| C2 | Objet social Art. 5 trop large | Email Alain = « scope limité à la distribution pour éviter l'ICS ». Art. 5 liste R&D, manufacture, médicaments vétérinaires, compléments. Contredit décision #7. | Restreindre Art. 5 ou assumer le secteur sensible ? |
| C3 | Nom représentant | Contrat-cadre l.18 « Jean-Christophe HAVAUX » → « Jean-Claude ». | Correction rédactionnelle. |
| C4 | Nom chinois DIAHO | « 迪亚霍 vs 迪鸿 » encore open point ; Jade a figé 迪亚霍. | Purger du contrat. |
| C5 | Seuil exclusion Art. 11 | « 50 % du capital » vs décision #6 « base votants + 50 % ». | Vérifier base de calcul (Renard). |
| C6 | Conseil Art. 14/33 | 3 sièges transitoires mais pas de règle fixe ; siège DIAHO non réservé (écart décision #3). | Fixer composition (Renard). |

### VETALYX — réponse DIAHO 28/10 (contrat-cadre v4) — 🔴 à arbitrer

> Trace : `08_VETALYX/legal/2026-10-28_dobby_analyse-reponse-chinois-v4.md`. Réponse à notre envoi 07/10.

| # | Sujet | Contexte | Options |
|---|-------|----------|---------|
| R1 | Arbitrage | V4 = Hangzhou/CIETAC (CN+EN). Nous : Genève/ICC. | A) Refuser → Genève/ICC / B) Siège neutre tiers / C) Accepter |
| R2 | Droit applicable | V4 = droit belge + chinois (transactions liées). Nous : belge seul. | A) Belge seul / B) Belge + chinois limité / C) Accepter |
| R3 | Tiers (Dixun) | V4 = DIAHO seule, pas de tiers. Nous (07/10) : Dixun signe. | A) DIAHO seule / B) Dixun signataire / C) Dixun garant |
| R4 | Objet social | DIAHO veut élargir (alimentation, classe 31). Nous : restreindre (ISC/ICS). | A) Restreindre / B) Élargir limité / C) Accepter |
| R5 | Véto / voix | DIAHO demande confirmation 40 % voix + siège conseil. | A) Confirmer statuts / B) Confirmer pacte / C) Négocier |

**Décisions JC (28/10, sous réserve validation Renard — cohérence) :**
- R1 : siège **neutre** (sinon arrêt d'activité) → ICC Genève, repli SIAC Singapour.
- R2 : droit **belge** pour opérations EU + droit **chinois** limité aux transactions liées (dépeçage).
- R3 : **Dixun garant** (annexe) ou au minimum contrat DIAHO↔Dixun préliminaire.
- R4 : accepter extension objet social **sauf** délais d'enregistrement ICS.
- R5 : 40 % capital → 40 % voix + 1 siège, conseil de 3 (abandon véto statutaire → droits au pacte).

> Analyse de cohérence : `08_VETALYX/legal/2026-10-28_renard_analyse-coherence-reponses-jch-v4.md`.

**Lignes de défense verrouillées (JC 28/10) :**
- L1 : pas de véto DIAHO sur l'entrée d'un investisseur / l'augmentation de capital (restent au bloc 60 % + agrément 50 %). ✅
- L2 : anti-dilution = pro-rata uniquement (Art. 15). ✅
- L4 : bloc des fondateurs décide à la majorité, pas à l'unanimité. ✅

> Réciprocité des clauses protectrices : `08_VETALYX/legal/2026-10-28_renard_check-reciprocite-clauses.md` (6 asymétries : 4 fondateurs / 2 DIAHO). Décisions JC : **Art. 21 = laisser asymétrique (option B)** ; **Art. 25 = aligné** (même droit d'information pour tous).

### IOT/Vanlife — blocage RPi 5 (résolu 01/10)

| Date | Sujet | Contexte | Options | Décision |
|------|-------|----------|---------|----------|
| 2026-09-30 | Stratégie déblocage RPi 5 Lupo | Boot gelé phase init hardware + SQUASHFS NVMe (nvme0n1p5) + duplicate_os_install + SSH perdu. | A) Réimage NVMe + purge instance HA / B) SD seule / C) Aide expert hardware | ✅ **Résolu** — NVMe retiré 01/10, HAOS 18.3 boot OK |

### Dépendances externes (validation en cours)

| Sujet | Qui | Statut |
|-------|-----|--------|
| Avis structure VETALYX + DIAHO 40 % (déclaration UBO/ISC) | UCM Belgique | ⏳ En attente de réponse |
| Validation setup Lupo-RPI | Alain Bosseloir | ⏳ En attente de discussion |

---

## Décisions tranchées — arbitrage JC du 2026-10-01 (VETALYX)

| # | Sujet | Décision JC |
|---|-------|-------------|
| 1 | Véto DIAHO : contractuel vs statutaire | **A — bascule dans les statuts** (majorités renforcées « incluant le vote de DIAHO »). Risque ISC à assumer avec notaire. |
| 2 | Apport DIAHO : nature PI vs espèces | **Espèces uniquement (1 600 €)** — PAS d'apport en nature PI. ⚠️ Inverse l'hypothèse « apport PI » du 18/08 et de l'analyse Jade 10/08. Statuts Art. 7 (espèces) corrects. |
| 3 | Siège DIAHO / conseil | **1 administrateur DIAHO + 2 fondateurs européens** ([X]=3) — proposé par Alain Bosseloir (01/10), confirmé JC. |
| 4 | Identité Bosseloir | **AB Advices** (personne morale). Harmoniser le tableau signatures. |
| 5 | Capital nominal | **10 000 € souscrit, 4 000 € libéré** (600 € ×4 + 1 600 €). 6 000 € restants à formaliser. |
| 6 | Seuil exclusion DIAHO | **Base votants (B) + seuil 50 %** — aligner pacte Art. 13 (75 %) et statuts Art. 11 (75 %) sur 50 %. |
| 7 | Qualification AFMPS/FAMHP | **Diagnostic vétérinaire (DM)** maintenant ; « médicament » ajouté plus tard via modification des statuts. |

## Arbitrage complémentaire 01/10 — relecture Alain Bosseloir

| # | Sujet | Décision JC |
|---|-------|-------------|
| 8 | Terminologie | **« fondateurs européens »** pour les 4 (DiaHo = « fondateur » 40 % distinct). |
| 9 | Annexes (A1/A2/A3 pacte + Annexes I/II statuts) | **Supprimées des documents, mais conservées en fichiers actifs** (PAS en archives). |
| 10 | Points Alain Bosseloir | **Analyse préalable de pertinence** (Renard, ÉTAPE 0) avant toute intégration — verdict par point. |

---

## Décisions antérieures (30 derniers jours)

| Date | Sujet | Décision |
|------|-------|----------|
| 2026-08-18 | DIAHO 40 % fondateur dès la constitution | Acté — mission préparation stratégique 120 K€ |
| 2026-09-29 | Standardisation matérielle IoT | Reste en 12V partout |
