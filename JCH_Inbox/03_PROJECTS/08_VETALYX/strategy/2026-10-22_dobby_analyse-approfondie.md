# VETALYX — Analyse approfondie (correction et mise à jour)

> 2026-10-22 · Dobby 🦉 · **corrige et complète** le RESUME-PROJETS du même jour
> Déclencheur : JC m'a fait remarquer que le tour initial était trop superficiel.

---

## 0. Correction de mon premier passage

Le `RESUME-PROJETS.md` du 2026-10-22 notait VETALYX **4/10** avec pour seule
mention « business plan et roadmap non définis ». **C'était faux.** J'avais lu
`executive-summary.md` (généré le 2026-07-03, périmé) sans explorer le contenu.

Ce qui existe réellement et que je n'avais pas vu :

| Élément | Volume / état |
|---|---|
| `business-plan/` | BP V3 (254 l.), **modèle financier Excel**, exec summaries V2 et V3, MASTER_STRUCTURE.pptx |
| `strategy/` | 27 fichiers — stratégie vétérinaire (113 Ko), pilote France, MedFluid/NAST, Vita X Taiwan, note Depinois |
| `legal/` | Contrat-cadre v4.1 + **annexes 1→10**, statuts SRL FR/EN v2, pacte v2, convention de bloc v2 |
| `regulatory/` | Réglementation EU/FR/DE + dossier technique DIXUN + grille IVDR |
| `clinical/` | Protocoles, consensus composition, rapports de validation |
| `market/` | Analyse potentiel marché vétérinaire (89 Ko), Market Evidence Pack, HCA Spray |
| `investors/` | Investor deck, defensive Q&A, exec summary investisseurs |
| `operations/` | Master Action Plan, tableau de bord financier, checklist opérationnelle, timesheets |
| `00_LIVRABLES/` | 22 livrables spécialistes (Renard, Clio, Jade, Vasco, Bruno…) |

**Note révisée : 6/10** (voir §6 pour la justification).

---

## 1. Ce qu'est VETALYX (version exacte)

Société **belge** (Marche-en-Famenne, SRL), diagnostic vétérinaire rapide.
MVP : **allergie IgE chien/chat**. Fournisseur : **Zheda Dixun** (CN), fédéré
par **DIAHO** (CN). Marchés cibles : FR, IT, ES, DE, BE.

**Structure capitalistique (à jour 2026-10-06)** :
- Capital 10 000 € (4 000 libérés)
- **DIAHO 40 %** dès la constitution (apport en espèces 1 600 €)
- 4 fondateurs belges : **4 × 15 %** (dont JCH)
- Mission de préparation stratégique pour DIAHO : **120 000 € HT**
  (100 K€ + 20 K€ validations cliniques/sérothèque)

---

## 2. Le business plan — chiffres réels

**Horizon Y1 (2026) → Y5 (2030)** :

| | 2026 | 2027 | 2028 | 2029 | 2030 |
|---|---|---|---|---|---|
| **Total Revenue** | 299 700 | 856 088 | 2 295 375 | 4 490 850 | **7 209 585** |
| **EBITDA** | 40 980 | 170 904 | 968 564 | 2 352 058 | **4 203 383** |

Croissance **×24 sur 5 ans**, marge EBITDA passant de 14 % à **58 %**.
Le BP V3 est recalé sur le modèle Excel (dont 2 008 erreurs `#REF!` ont été
neutralisées le 06/10) et intègre DIAHO à 40 %.

**Réserves déclarées dans le document lui-même** :
- *« Business plan data are a draft version needing update linked to investments strategies »*
- *« Instrumentation is key for success »*
- Focus vétérinaire strict, test humain écarté (non recommandé)

---

## 3. La roadmap — deux documents distincts, à ne pas confondre

### 3.1 Pilote France (12 mois, 4 phases) — `strategy/Veterinary_Project_Strategy_Update.md`

| Phase | Durée | Contenu |
|---|---|---|
| 1 — Préparation | M0–M3 | Portefeuille produit, conformité réglementaire et étiquetage, documentation FR, shortlist cliniques et partenaires B2B |
| 2 — Déploiement | M3–M6 | **40–60 cliniques directes**, 1er partenariat B2B signé, premières ventes |
| 3 — Validation | M6–M9 | **120–180 cliniques**, ajustement prix/packaging/message |
| 4 — Décision scale | M9–M12 | **200–300 cliniques actives**, décision nationale, package de réplication EU |

**Hypothèses chiffrées** : ~7 000 cliniques en France, cible 1,5–2,5 % la
première année ; 4–6 kits/clinique/mois ; 28–35 € le kit.

**Revenu annualisé du pilote** : 270 K€ (bas) / **420 K€ (base)** / 630 K€ (haut).

**Modèle d'affaires dual** : cliniques directes (40–50 %) + écosystème B2B
(distributeurs, labos, groupes de cliniques) (50–60 %).

**Playbook réplicable** documenté pour DE, IT, ES, BE, avec portes de décision
au mois 6 (go/no-go) et mois 9–12 (scale/pause).

### 3.2 Les 14 points de décision stratégique — `strategy/2026-07-07_...depinois.md`

Issus de la note de cadrage **Alain Depinois (AWDN Partners)**. Question
centrale : VETALYX reste-t-il allergologie, ou devient-il **plateforme de
diagnostics rapides** (allergie + vectoriels + biomarqueurs) ?

**Point crucial** : un addendum JCH du 07/07 précise explicitement que
*« la note n'est pas un ordre de modification des priorités […] les 14 points
ne sont pas des décisions à trancher immédiatement »*. La recommandation
initiale de Dobby (scénario C, pivot) a été **rétrogradée en option de veille**.

→ **Décision de JC : allergie IgE reste le MVP.** Les 7 briefs d'exploration
(Furet, Milan, Renard, Clio, Bruno, Hermine, Vega, Atlas) sont en veille non
bloquante. Vasco est en veille active, non briffé sans accord.

---

## 4. Le juridique — état précis (et ce qui bloque encore)

**Solide :**
- Contrat-cadre **v4.1** (06/10) avec annexes 1→10 réorganisées, version **EN officielle**
- Protections VETALYX restaurées après relecture JC (stock lancement, écoulement
  12 mois, cession/changement de contrôle, assurance, garanties, marques,
  résiliation + 8 manquements graves, force majeure, nullité partielle)
- Statuts SRL FR v2, pacte v2, convention de bloc v2

**8 points encore ouverts** (`legal/note-points-restants.md`) :

1. **Libération des 6 000 €** restants — mécanique à valider par le notaire
2. **Validation notaire ISC** — le véto DIAHO est au Pacte, **pas** aux statuts,
   pour minimiser le filtrage ISC (investissements étrangers)
3. **Drag-along** — seuil `[75 %]` non arbitré
4. **Peiwen QI double qualité** — administratrice DIAHO + fondatrice 15 %.
   Bosseloir signale un risque de « position délicate »
5. **Qualification AFMPS/FAMHP** — DM vétérinaire vs médicament vétérinaire (Clio)
6. **Annexes 2 et 3** à rédiger (reporting, règlement du conseil)
7. **Faculté de désignation proportionnée** (Art. 4) — à éclaircir
8. **Composition du conseil** — 1 DIAHO + 2 fondateurs, répartition à formaliser

**Décisions structurantes déjà prises :** exercice fiscal long
(constitution → 31/12/2028), statuts **FR uniquement** (EN en traduction,
pas de ZH pour éviter les flous en litige), arbitrage Genève.

---

## 5. Les tensions réelles du projet

**5.1 Écart entre la stratégie écrite et l'exécution**
Le pilote France est chiffré (420 K€ base) et séquencé sur 12 mois. Mais rien
n'indique qu'il soit démarré : le thread de projet mentionne « reprise
septembre », et l'état global est marqué **⚪ veille**. Le BP (299 K€ en 2026)
suppose un lancement cette année.

**5.2 Le BP suppose des instruments qui ne sont pas encore réglés**
La qualification AFMPS/FAMHP n'est pas tranchée, or elle conditionne la
commercialisation. Un BP à 7,2 M€ en 2030 repose sur un cadre réglementaire
non validé.

**5.3 Le tableau de bord financier est daté du 31/05/2026**
Il annonce M1 (66 000 €) et M2 (44 000 €) « à venir » et un total de **110 000 €**
alors que le contrat signé porte **120 000 €** (100 + 20). Incohérence à réconcilier.

**5.4 Le désaccord stratégique n'est pas clos, il est gelé**
La question Depinois (allergie vs plateforme) a été repoussée, pas tranchée.
Les 14 points restent ouverts, en veille. C'est un choix assumé — mais la
marque, le pacte et le BP sont calibrés sur l'allergie seule.

---

## 6. Notation révisée : 6/10

| Dimension | Note | Justification |
|---|---|---|
| Juridique / corporate | 8/10 | Contrat-cadre v4.1 complet, statuts, pacte — reste 8 points notariés |
| Business plan | 7/10 | Chiffré, modélisé, recalé — mais « draft » de son propre aveu |
| Stratégie / roadmap | 6/10 | Pilote France documenté et chiffré, mais non démarré |
| Réglementaire | 4/10 | Qualification AFMPS/FAMHP non tranchée — bloque la vente |
| Exécution commerciale | 2/10 | Aucune clinique active, aucune vente, pas de lancement |
| Produit / clinique | 8/10 | Protocoles, consensus, rapports de validation solides |

**Pourquoi 6 et pas 4** : la profondeur documentaire est réelle et de qualité.
**Pourquoi pas plus** : rien n'est encore vendu, et le verrou réglementaire
n'est pas levé.

---

## 7. Ce que je recommande de prioriser

1. **Trancher la qualification AFMPS/FAMHP** (Clio) — c'est le verrou qui
   conditionne tout le reste. Sans lui, le BP est théorique.
2. **Nommer les 2 administrateurs fondateurs** (Art. 33) — bloque la
   constitution effective.
3. **Passer chez le notaire** — les 8 points ouverts sont listés, le notaire
   peut les lever en une séance.
4. **Décider si le pilote France démarre en 2026 ou glisse en 2027** — le BP
   et la roadmap doivent refléter la réalité, pas l'inverse.
5. **Réconcilier 110 K€ vs 120 K€** dans le tableau de bord.

---

## 8. Leçon pour le système

Mon premier passage a lu `executive-summary.md` (généré 03/07, périmé) au lieu
du `thread-vetalyx.md` (à jour au 06/10) et du contenu réel des dossiers.

**Règle à retenir** : pour noter un projet, lire le thread file et
l'arborescence **avant** les summaries générés. Les `executive-summary.md`
datent de juillet sur plusieurs projets.

*Sources : thread-vetalyx.md · INDEX.md · Vetalyx_Executive_summary_V3.md ·
legal/note-points-restants.md · strategy/Veterinary_Project_Strategy_Update.md ·
strategy/2026-07-07_...depinois.md · operations/TABLEAU_BORD_FINANCIER (31/05) ·
operations/Vetalyx_master_plan_corrigé.md · arborescence complète (22 livrables).*
