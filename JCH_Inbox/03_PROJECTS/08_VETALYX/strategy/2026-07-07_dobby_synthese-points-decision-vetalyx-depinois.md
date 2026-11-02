---
date: 2026-07-07
project: Vetalyx
type: decision-synthesis
source: "Note de cadrage Alain Depinois (AWDN Partners) + corpus Vetalyx"
model: kimi-k2.7-code
---

## Addendum — Clarification JCH (2026-07-07)

> Cette synthèse a été produite après une première lecture de la note Depinois. JCH a ensuite précisé :
> **La note n'est pas un ordre de modification des priorités actuelles. Les priorités restent inchangées.**
> **Vetalyx est et reste une plateforme de diagnostics vétérinaires sensu largo.**
> **L'objectif est d'augmenter la réflexion stratégique et d'identifier d'autres MVP possibles pour le futur.**

### Conséquences sur la lecture de cette synthèse

- Les 14 points de décision ne sont **pas des décisions à trancher immédiatement**, mais des axes de réflexion pour enrichir la roadmap.
- La recommandation Dobby (scénario C ajusté) doit être comprise comme une **option stratégique future**, pas comme un plan de pivot à exécuter maintenant.
- Les 7 briefs ont été repositionnés en **mode exploration / veille stratégique**, avec des deadlines non bloquantes.
- L'allergie IgE reste le MVP prioritaire et le cœur du plan actuel.

### Reformulation de la recommandation

**Recommandation révisée** : maintenir l'allergie IgE comme MVP prioritaire, tout en intégrant les vectoriels/biomarqueurs dans un **pipeline stratégique de MVP futurs**. Préparer la plateforme (marque, réglementaire, fournisseurs) pour pouvoir accueillir ces extensions quand le moment sera pertinent, sans impacter la roadmap actuelle.

---

# Synthèse des points d'attention, réflexion et décision — Vetalyx

> Dobby 🦉 — Kimi K2.7
> Contribution de l'équipe : Vasco 🐺, Renard 🦊, Clio 📜, Furet 🦡, Bruno 🦫, Hermine ⚖️, Atlas 🌍, Milan 🎯

---

## 1. Executive summary

La note de cadrage d'Alain Depinois (2026-06-25) remet en question le MVP commercial de Vetalyx. Elle propose de remplacer l'allergie animale comme porte d'entrée par des **tests rapides infectieux/vectoriels et biomarqueurs** (panel Lyme/Anaplasma/Ehrlichia/Dirofilaria, FeLV/FIV, CRP/SAA), plus facilement commercialisables sous AFMPS.

**Enjeu central** : Vetalyx doit-il rester une société d'allergologie vétérinaire, devenir une plateforme de diagnostics rapides vétérinaires multi-domaines, ou lancer une ligne infectieuse/biomarqueur en parallèle de l'allergie ?

**Décisions à trancher avant la réunion avec les partenaires chinois** :
1. Périmètre produit du MVP (allergie seule / vectoriel seul / double track)
2. Validation de la capacité fournisseur sur les 3 familles de produits
3. Architecture réglementaire et allégations par famille
4. Impact sur le business plan, la valorisation et le pacte fondateurs
5. Positionnement de marque et identité Vetalyx
6. Séquence de lancement géographique et commerciale
7. Gouvernance et allocation des ressources d'une structure pré-lancement

---

## 2. Matrice des points d'attention et de décision

| ID | Domaine | Point d'attention / Question | État actuel | Options | Recommandation préliminaire | Owner suggéré | Urgence | Risque si non tranché |
|---|---|---|---|---|---|---|---|---|
| D1 | **Stratégie** | Quel est le cœur de métier de Vetalyx ? | Allergie IgE | A. Allergie<br>B. Vectoriels<br>C. Plateforme diagnostics rapides | **C** — plateforme diagnostics rapides, avec allergie comme différenciateur structurant | Atlas + Vasco | 🔴 Critique | Perte de cohérence, message confus, investissement dilué |
| D2 | **Produit MVP** | Quel produit lancer en P0 ? | Test rapide 6 lignes IgE | A. Allergie seule<br>B. Vectoriel seul<br>C. Double track | **C** — vectoriel chien + allergie chat/chien selon capacité fournisseur | Vasco + Clio | 🔴 Critique | Mauvais product-market fit, lancement trop lent |
| D3 | **Fournisseur** | Zheda Dixun peut-il fournir qualité vectoriel/biomarqueurs ? | Non vérifié | A. Oui, unique fournisseur<br>B. Oui, avec backup<br>C. Non, chercher autre | **B** — valider capacité DIXUN, qualifier backup | Furet + Milan | 🔴 Critique | Lancement sur produit non qualifié, rupture supply chain |
| D4 | **Réglementaire** | Quel cadre pour chaque famille de tests ? | Cadre vétérinaire national, peu documenté | A. AFMPS simple<br>B. AFSCA/Sciensano institutionnel<br>C. Marquage CE/IVDR | **A** pour P0 ; documenter B/C pour P1 | Renard | 🔴 Critique | Blocage réglementaire, allégations illégales |
| D5 | **Allégations** | Quelles promesses clinico-commerciales ? | Test de triage allergies | A. Diagnostic<br>B. Triage/support décision<br>C. Suivi | **B** pour toutes les familles en P0 | Renard + Vasco | 🟠 Haute | Plaintes, retrait marché, perte crédibilité KOL |
| D6 | **Financier** | Impact sur business plan 5 ans ? | Calibré sur allergie | A. Rester<br>B. Pivot<br>C. Hybride | **C** — scénarios à modéliser | Bruno + Sigma | 🟠 Haute | Mauvaise valorisation, burn rate imprévu |
| D7 | **Corporate** | Le pacte 25/25/25/25 résiste-t-il à un pivot ? | Signé | A. Oui<br>B. Révision nécessaire<br>C. Non | **A** avec mise à jour de l'objet social si pivot confirmé | Renard + Hermine | 🟡 Moyenne | Conflit entre fondateurs, blocage décisionnaire |
| D8 | **Marque** | Vetalyx = allergie ou diagnostics rapides ? | Allergie | A. Allergie<br>B. Vectoriels<br>C. Umbrella diagnostics | **C** — plateforme diagnostics rapides vétérinaires | Vega + Milan | 🟠 Haute | Confusion client, perte d'équité de marque |
| D9 | **Commercial** | Quelle séquence géographique et canal ? | France/Benelux P0 | A. Même<br>B. Autres pays d'abord<br>C. Multicanal | **A** — France/Benelux P0, validation rapide vectoriel | Atlas + Furet | 🟡 Moyenne | Lancement dispersé, ressources éparpillées |
| D10 | **Scientifique** | Niveau de preuve requis pour vectoriels/biomarqueurs ? | Allergie en cours | A. Validation analytique<br>B. KOL clinique<br>C. Les deux | **C** — mais allégé vs allergie car tests mieux validés industriellement | Clio + Vasco | 🟠 Haute | Allégations non fondées, rejet communauté scientifique |
| D11 | **Organisation** | Ressources humaines pour double track ? | Structure pré-lancement | A. All-in sur un produit<br>B. Recrutement<br>C. Outsourcing | **A ou C** — ne pas disperser l'équipe core | Bruno + Dobby | 🟡 Moyenne | Surcharge équipe, exécution dégradée |
| D12 | **Partenariat DIAHO** | L'accord DIAHO couvre-t-il les vectoriels/biomarqueurs ? | Allergie exclusive | A. Oui<br>B. À renégocier<br>C. Non | **B** — vérifier et adapter si nécessaire | Renard | 🟠 Haute | Conflit contractuel, perte exclusivité |
| D13 | **IP** | Y a-t-il des brevets bloquants sur panels vectoriels ? | Non étudié | A. FTO à faire<br>B. Risque faible<br>C. Risque élevé | **A** — FTO rapide sur les 3 familles | Hermine | 🟡 Moyenne | Procès ou retrait produit |
| D14 | **Opportunités** | MedFluid NAST reste-t-il dans le pipeline ? | T2 2027 | A. Oui<br>B. Non<br>C. Accélérer | **A** — reste complément T2 2027, pas priorité P0 | Vasco + Bruno | 🟢 Basse | Dispersion si accéléré |

---

## 3. Analyse par dimension

### 3.1 Stratégique — Atlas 🌍 + Vasco 🐺

**Constat** : La proposition Depinois ne conteste pas le marché cible (clinique vétérinaire généraliste) ni la logique commerciale (test rapide en consultation). Elle conteste le **produit d'entrée**.

**Tension fondamentale** :
- L'allergie est un marché de niche structurant, avec peu de concurrents dans le mid-market et une forte différenciation possible (panels régionaux).
- Les vectoriels/biomarqueurs sont des marchés plus matures, plus concurrentiels, mais avec une adoption clinique plus immédiate et un cycle de vente plus court.

**Question clé pour JCH** : Vetalyx veut-il construire un **monopole de niche** (allergie) ou une **plateforme de diagnostics rapides** (plusieurs familles) ?

**Position Atlas** : Un document fondateur doit d'abord trancher les non-négociables. Si le non-négociable est « devenir la référence européenne du diagnostic rapide vétérinaire en cabinet », alors l'allergie est un pilier, pas la totalité. Si le non-négociable est « allergologie vétérinaire accessible », le pivot est une dérive.

**Décision requise** : Validation ou révision des non-négociables du document fondateur Vetalyx.

---

### 3.2 Clinico-scientifique — Clio 📜 + Vasco 🐺

**Constat** : Le corpus Vetalyx démontre déjà une prudence clinique sur l'allergie :
- Test IgE alimentaire = support au régime d'éviction, pas diagnostic.
- Test rapide DIXUN actuel insuffisant pour l'Europe sans redesign.
- Besoin de validation KOL (n≥30) et de données DBS.

**Pour les vectoriels** :
- Panel Lyme/Anaplasma/Ehrlichia/Dirofilaria a une logique clinique forte en Europe (maladies émergentes, saisonnalité, décision immédiate).
- Tests FeLV/FIV très standardisés, adoption routinière.
- CRP/SAA : biomarqueurs d'inflammation, utiles pour le suivi mais interprétation contextuelle.

**Risque scientifique** : la note Depinois sous-estime peut-être la concurrence et la qualité requise. Un test vectoriel chinois à bas coût doit prouver sensibilité/spécificité face aux panels IDEXX/Zoetis.

**Décision requise** : Niveau de preuve clinique minimal accepté pour chaque famille de tests avant lancement.

---

### 3.3 Réglementaire — Renard 🦊

**Constat** : Le corpus mentionne un cadre vétérinaire national par pays, pas IVDR/MDR. La note Depinois oppose AFMPS (commercialisable) et AFSCA (institutionnel, à éviter).

**Points de vigilance** :
- Même en AFMPS, les allégations doivent être prudentes.
- « Diagnostic rapide » est un terme à risque si le test est un triage.
- CRP/SAA ne peut pas être vendu comme outil diagnostique autonome.
- Importation Chine → France/Belgique nécessite documentation technique, traçabilité, étiquetage.

**Décision requise** : Valider le cadre réglementaire par famille de tests et les wordings d'allégation autorisés.

---

### 3.4 Commercial / Marché — Furet 🦡 + Milan 🎯

**Constat** : Le marché des vectoriels est plus saturé (IDEXX SNAP 4Dx, Zoetis Witness, Bioguard, etc.). Cependant, un panel multiplex chien européen intégré pourrait trouver une place.

**Intelligence concurrentielle à produire** :
- Prix des panels vectoriels concurrents en Europe.
- Parts de marché par pays.
- Critères de décision des vétérinaires (prix, marque, support, rapidité).
- Positionnement des distributeurs (Centravet, Alcyon, etc.).

**Décision requise** : Validation de l'opportunité de marché réelle pour chaque famille en France/Benelux.

---

### 3.5 Financier — Bruno 🦫

**Constat** : Le business plan actuel est calibré sur l'allergie avec des projections ambitieuses (7,2 M€ CA année 5, 58,3 % EBITDA).

**Impacts d'un pivot ou double track** :
- Coût R&D et validation : vectoriels potentiellement moins chers (tests mieux établis), mais nécessitent quand même validation analytique.
- Cycle de vente : vectoriels plus court → CA plus tôt.
- Marge : concurrence plus forte → pression sur les prix.
- Besoin en fonds : double track = plus de capital.

**Décision requise** : Modéliser 3 scénarios (allergie pure, vectoriel pur, hybride) et leur impact sur runway et valorisation.

---

### 3.6 Fournisseur / Supply chain — Furet 🦡

**Constat** : Le catalogue DIXUN contient un document « Animal Diseases Test-WellRay-202504.pdf », mais la capacité exacte n'a pas été extraite.

**Questions à trancher** :
- DIXUN peut-il produire panel vectoriel chien avec les 4 agents (Lyme, Anaplasma, Ehrlichia, Dirofilaria) ?
- Quelles performances analytiques (sensibilité/spécificité) ?
- FeLV/FIV : technologie disponible ?
- CRP/SAA : format compatible test rapide ?
- Documentation réglementaire disponible (ISO, audits) ?
- Existe-t-il un fournisseur backup (Hangzhou Darui, Gangzhu, Zhunxin) ?

**Décision requise** : Go/no-go fournisseur par famille de tests avant la réunion chinoise.

---

### 3.7 Corporate / Juridique — Renard 🦊 + Hermine ⚖️

**Constat** : Le pacte fondateurs 25/25/25/25 est signé. L'objet social de la SRL est probablement calibré sur les diagnostics vétérinaires de manière large.

**Points de vigilance** :
- Accord DIAHO : porte-t-il sur l'allergie exclusivement ou sur diagnostics vétérinaires ?
- Exclusivité territoriale : couvre-t-elle les nouvelles familles ?
- IP : brevets ou marques déposées sur allergie uniquement ?
- Objet social : suffisamment large pour intégrer vectoriels/biomarqueurs ?

**Décision requise** : Revue juridique des contrats existants et adaptation si pivot confirmé.

---

### 3.8 Marque / Marketing — Milan 🎯 + Vega 🦚

**Constat** : Vetalyx est déjà identifiée comme marque allergologie. Un pivot ou une extension nécessite un repositionnement.

**Options de positionnement** :
- **Allergie** : message clair, mais marché plus long à construire.
- **Diagnostics rapides vétérinaires** : message plus large, mais moins différenciant.
- **Sous-marques** : Vetalyx Allergy + Vetalyx Vectorial + Vetalyx Care (biomarqueurs).

**Décision requise** : Architecture de marque et promesse principale.

---

## 4. Scénarios intégrés

### Scénario A — Allergie first (stay the course)
- **MVP** : test rapide 6 lignes IgE chien/chat, 3 SKUs régionaux.
- **Avantages** : cohérence avec investissement, différenciation forte, marge élevée.
- **Risques** : validation longue, éducation marché, test DIXUN à redessiner.
- **Approbation requise** : confirmer que l'allergie reste le cœur de métier.

### Scénario B — Vectoriel first (pivot Depinois)
- **MVP** : panel vectoriel chien + FeLV/FIV + CRP/SAA.
- **Avantages** : cash-flow rapide, adoption clinique immédiate.
- **Risques** : concurrence forte, repositionnement marque, perte investissement allergie.
- **Approbation requise** : accepter un pivot de cœur de métier.

### Scénario C — Double track
- **P0** : vectoriel chien + FeLV/FIV (cash-flow rapide).
- **P1** : allergie redessinée EU (différenciateur).
- **P2** : CRP/SAA + MedFluid NAST (écosystème).
- **Avantages** : diversification, cash-flow tôt, marque plateforme.
- **Risques** : dispersion ressources, complexité opérationnelle, besoin de capital.
- **Approbation requise** : accepter augmentation complexité et besoin en fonds.

### Scénario D — Intégration sélective (recommandation Dobby)
- **MVP** : allergie reste le produit phare, mais on négocie l'ajout d'un panel vectoriel chien dès le lancement.
- **Avantages** : pas de pivot brutal, réponse aux deux opportunités.
- **Risques** : message moins clair, complexité supply chain dès le départ.
- **Approbation requise** : valider que l'allergie reste la priorité stratégique.

---

## 5. Recommandation Dobby

**Recommandation principale** : **Scénario C ajusté** — lancer un **P0 vectoriel chien** (panel multiplex Lyme/Anaplasma/Ehrlichia/Dirofilaria) pour générer du cash-flow et valider le canal, puis introduire **l'allergie comme P1 différenciant** dès que le panel EU est validé. FeLV/FIV peut accompagner le P0 vectoriel. CRP/SAA reste en P2.

**Pourquoi** :
1. Le vectoriel a un cycle de validation et de vente plus court.
2. L'allergie reste le différenciateur structurant à moyen terme.
3. Même client, même canal, même réglementaire AFMPS.
4. Réduit le risque de lancer un MVP allergie qui nécessite encore beaucoup de redesign.

**Condition sine qua non** : validation préalable de la capacité DIXUN (ou backup) sur le panel vectoriel chien et FeLV/FIV.

---

## 6. Plan d'action décisionnel

| # | Action | Owner | Deadline | Décision à obtenir de JCH |
|---|---|---|---|---|
| 1 | Valider capacité DIXUN sur vectoriel + FeLV/FIV + CRP/SAA | Furet + Milan | Avant réunion chinois | Go/no-go fournisseur par famille |
| 2 | Revue réglementaire AFMPS et allégations par famille | Renard | Avant réunion chinois | Wordings autorisés |
| 3 | Revue contrats DIAHO et pacte | Renard + Hermine | 1 semaine post-réunion | Adaptations nécessaires ? |
| 4 | Modélisation financière 3 scénarios | Bruno + Sigma | 2 semaines post-réunion | Budget et valorisation acceptés |
| 5 | Revue clinique panels vectoriels | Clio + Vasco | 1 semaine post-réunion | Niveau de preuve acceptable |
| 6 | Architecture de marque | Vega + Milan | 2 semaines post-réunion | Positionnement marque validé |
| 7 | Mise à jour document fondateur | Atlas | 3 semaines post-réunion | Non-négociables validés |
| 8 | Préparation grille négociation réunion chinois | Dobby + Renard | Jour J | Mandat de négociation |

---

## 7. Questions ouvertes pour JCH

1. **Cœur de métier** : Vetalyx doit-il rester une entreprise d'allergie vétérinaire ou devenir une plateforme de diagnostics rapides vétérinaires ?
2. **MVP P0** : Acceptez-vous de lancer un panel vectoriel chien en P0, même si cela retarde ou réduit l'allergie en P1 ?
3. **Double track** : Êtes-vous prêt à financer et gérer deux lignes produit en parallèle dès le lancement ?
4. **Fournisseur** : Si DIXUN ne peut pas faire le vectoriel de qualité, acceptez-vous de chercher un autre fournisseur ou de rester sur l'allergie ?
5. **Marque** : Acceptez-vous de repositionner Vetalyx comme plateforme de diagnostics rapides, quitte à perdre un peu de clarté initiale ?
6. **Ressources** : Avez-vous les ressources humaines/financières pour accélérer le vectoriel sans sacrifier WildNexus P0 ?

---

## 8. Risques transverses à surveiller

| Risque | Niveau | Mitigation |
|---|---|---|
| Fournisseur incapable sur vectoriel | 🔴 Élevé | Due diligence technique avant réunion, plan B |
| Concurrence écrasante sur vectoriels | 🟠 Moyen | Différenciation par panel multiplex EU + prix |
| Dispersion ressources (double track) | 🟠 Moyen | Séquencer P0/P1, ne pas tout lancer en même temps |
| Perte d'identité de marque | 🟠 Moyen | Architecture de marque claire dès le départ |
| Conflit fondateurs sur pivot | 🟡 Moyen | Réunion fondateurs, alignement écrit |
| Allégations non conformes | 🔴 Élevé | Revue Renard avant tout support commercial |
| Retard réglementaire | 🟠 Moyen | Dossier RA/QA par pays, checklist structurée |

---

## Voir aussi
- [[Vetalyx - stratégie]]
- [[Vetalyx - décisions]]
- [[Vetalyx - commercial]]
- [[2026-05-26_VETALYX_Market_Evidence_Pack]]
- [[2026-07-07_dobby_analyse-note-cadrage-vetalyx-depinois]]
