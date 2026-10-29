# BRIEF — Renard 🦊 + Clio 📜 — Refonte du Pacte d'Actionnaires VETALYX (2 couches)

**PRIORITY** : medium
**DEADLINE** : pas de deadline (veille, non bloquant) — à planifier sur reprise du projet
**Émis par** : Dobby 🦉, le 2026-09-30
**Projet** : 08_VETALYX

---

## MISSION

Refondre le Pacte d'Actionnaires Fondateurs VETALYX (v3, 31/05/2026) en une architecture à **2 couches** intégrant DIAHO comme actionnaire fondateur à 40 %, **en vérifiant systématiquement la concordance avec les Statuts SRL**, qui seront rédigés **en français uniquement**.

## CONTEXTE

Changement de stratégie acté le 18/08/2026 : DIAHO (Chine) entre au capital **dès la constitution** comme fondateur à 40 % (apport en nature PI, Art. 5:7 CSA), les 4 fondateurs belges passant à 4 × 15 % (60 %). L'ancien pacte v3 (4 fondateurs à 25 %) est structurellement obsolète : parties, capital et majorités de décision doivent être refondus. Le pacte reste nécessaire car le CSA laisse la gouvernance confidentielle hors statuts ; les statuts ne portent que le minimum publié au Moniteur.

## ENTRÉES DISPONIBLES

- Pacte v3 : `legal/contrat-europeens/VAL-Pacte-Actionnaires_VETALYX_Renard_2026-05-31.md`
- Statuts SRL v2 (19/08) : `legal/contrat-diaho/2026-08-21_jade_traduction-statuts-srl-vetalyx-FR-ZH.md` (source .docx : `legal/contrat-europeens/VAL-Statuts-SRL_VETALYX_19-8-26.docx`)
- ⚠️ **Version statuts la plus récente** : `legal/Creation Vetalyx avec Chinois/2026-09-22_jade_traduction-statuts-srl-vetalyx-FR-ZH(1).docx` — à utiliser comme référence autoritaire
- Revue juridique Renard (10/08) : `legal/contrat-diaho/2026-08-10_renard_revue-juridique-entree-diaho-vetalyx.md`
- Analyse capital Dobby v2 (10/08) : `legal/contrat-diaho/2026-08-10_dobby_analyse-entree-capital-diaho-vetalyx-belgique.md`
- Thread projet : `thread-vetalyx.md`
- Seing privé (clauses gouvernance/anti-dilution à recycler) : rechercher `FF-Accord-Seing-Prive` / seing privé du 31/05

## LIVRABLE ATTENDU

Deux documents .md dans `legal/` (ou `00_LIVRABLES/`) :
1. **Pacte d'Actionnaires VETALYX** (les 5 : DIAHO 40 % + 4 fondateurs 15 %) — couche 1.
2. **Convention de bloc des Fondateurs** (les 4 fondateurs, coordination du 60 %) — couche 2.

Chaque clause référencée contre l'article des Statuts correspondant. **Table de concordance exigée en tête de chaque document.**

## CONTRAINTES — CONCORDANCE STATUTS (CRITIQUE)

Les Statuts sont **en français uniquement** ; toute version ZH est une traduction de travail non opposable. Le pacte doit :
- référencer les Statuts FR (et non l'inverse) ;
- ne pas contredire les dispositions statutaires (le pacte ne lie que les associés, non opposable aux tiers — hiérarchie rappelée Art. 32 des statuts).

### Points de concordance à traiter (vérifiés par Dobby sur statuts v2 19/08 — à re-vérifier sur la version 22/09)

1. **Apport DIAHO — INCOHÉRENCE MAJEURE** : statuts v2 Art. 7 mentionnent DIAHO à 1 600 € **en espèces**, alors que la stratégie prévoit un **apport en nature PI** (Art. 5:7 CSA + rapport réviseur). À corriger dans les statuts ou à trancher explicitement.
2. **Capital nominal** : Art. 7 note + Art. 8 « 4 000 EUR (10 000 euros) » ambigu — clarifier capital souscrit (4 000 €) vs capital autorisé (10 000 €), et l'aligner avec le pacte.
3. **Identité de Bosseloir** : statuts = « AB Advices (Alain Bosseloir) » (personne morale) ; pacte v3 = « Alain BOSSELOIR » (personne physique). Harmoniser (impact signature, lock-up, non-concurrence).
4. **Nombre de parties** : statuts = 5 parties ; pacte v3 = 4. Redéfinir le terme « Fondateurs » (5 désormais) et la terminologie.
5. **Majorités / décisions réservées** : statuts Art. 21 (AGE) = 3/4 par défaut, « sauf décisions énumérées au Pacte (unanimité) ». Le pacte doit lister précisément ces décisions (véto DIAHO + bloc fondateurs) — c'est le point d'ancrage statutaire.
6. **Agrément 75 %** : statuts Art. 11 = agrément 75 % du capital. Avec DIAHO 40 %, les 4 fondateurs seuls (60 %) ne l'atteignent pas → DIAHO a un véto implicite. À assumer explicitement dans le pacte.
7. **Conseil / administrateurs** : statuts Art. 14 (1+ administrateurs, option observateur) + Art. 33 (4 premiers administrateurs placeholder). Le pacte doit définir le siège de DIAHO (administrateur ou observateur) et l'aligner sur Art. 33.
8. **Conventions réglementées** : statuts Art. 18 (autorisation du conseil, abstention de l'intéressé). Étendre/aligner le pacte (Art. 6 v3) au cas DIAHO = actionnaire + cocontractant commercial (contrat-cadre + mission 120 K€).
9. **Hiérarchie pacte/statuts** : statuts Art. 32 = « le Pacte prévaut entre les associés ». Confirmer la hiérarchie, mais rappeler : le pacte n'est pas opposable aux tiers.
10. **Contestations** : statuts Art. 28 renvoie au Pacte. Le pacte doit contenir la procédure réelle (conciliation → médiation → arbitrage CEPANI/ICC) ; redesigner le shotgun v3 (Art. 20) pour le 40/60.
11. **Dissolution** : statuts Art. 26 = AGE (3/4). Pacte v3 Art. 5 = unanimité. Résoudre la tension (le pacte engage les associés à voter ensemble, mais le seuil statutaire reste 3/4).
12. **Langue** : rédaction du pacte en FR, statuts en FR. Version ZH = traduction de travail (Jade), non opposable.

### Modifications de fond (refonte article-à-article)

- **Parties / capital** : ajouter DIAHO ; capital DIAHO 40 % + 4 × 15 %.
- **Administration** : siège DIAHO (administrateur ou observateur).
- **Comité** : scinder Comité fondateurs (couche 2) / conseil (couche 1).
- **Décisions réservées** : deux listes (véto DIAHO / bloc fondateurs) — remplace l'unanimité des 4.
- **Conflits d'intérêts** : renforcer (DIAHO actionnaire + cocontractant).
- **Lock-up / transferts** : garder lock-up 3 ans fondateurs ; ajouter lock-up DIAHO + verrou PI ; préemption ordre fondateurs → DIAHO → tiers.
- **Exclusion** : cas DIAHO (PI invalide, manquement contrat-cadre, sanction ISC/UBO) ; tenir compte que 40 % ne s'exclut pas à 75 %.
- **Évaluation** : garder méthode + plancher pré-revenus ; plancher = valorisation réviseur pour la PI.
- **Anti-dilution (Art. 12-14 v3)** : recycler les clauses du seing privé (full-ratchet / weighted average DIAHO, préemption fondateurs, tag/drag). L'« option de production » disparaît.
- **Non-concurrence / confidentialité** : étendre à DIAHO (territoire EU + PI).
- **Décès / départ** : good/bad leaver fondateurs ; changement de contrôle DIAHO + réversion PI.
- **Deadlock** : shotgun 40/60 + arbitrage.
- **Reporting** : garder (mensuel dès 100 K€) + droits d'information DIAHO.

### Risques juridiques à intégrer (Revue Renard 10/08)

- **AM1** : DIAHO solidairement responsable en tant que fondateur (5:4/5:16 CSA) — à acter.
- **AM2** : statuts FR/NL/DE uniquement ; minimum dans statuts, confidentiel au pacte.
- **AM3** : LOI/term sheet d'engagement avant notaire (plus de filet de sécurité).
- **ISC** : risque faible mais croît si droits de veto dès les statuts.
- **UBO** : personnes physiques derrière DIAHO publiées au registre.

## INTERACTIONS

- **Jade 🦩** — traduction ZH non opposable (si demandée).
- **Notaire externe** — validation apport en nature, ISC, statuts.
- ⚠️ **Vasco 🐺** en veille active — NE PAS briffer sans accord de JCH.

---

*Brief généré par Dobby 🦉 — skill `brief`. Archivé dans team.db (inbox).*

---

## ADDENDUM — Vérification concordance sur statuts v22/09 (Dobby, 2026-09-30)

La version la plus récente des statuts (`Creation Vetalyx avec Chinois/2026-09-22_jade_traduction-statuts-srl-vetalyx-FR-ZH(1).docx`) a été extraite (370 lignes) et comparée à la v2 du 19/08. Résultat de la vérification :

- **Point 1 (apport DIAHO) — NON RÉSOLU.** Art. 7 identique : DIAHO 1 600 € **en espèces**, pas d'apport en nature PI. À corriger ou trancher.
- **Point 2 (capital) — NON RÉSOLU.** Art. 8 « 4 000 EUR (10 000 euros) » inchangé.
- **Point 3 (Bosseloir) — AGGRAVÉ.** Art. 7 = « AB Advices (Alain Bosseloir) » mais tableau Signatures = « Alain BOSSELOIR ». Incohérence interne aux statuts eux-mêmes.
- **NOUVEAU — Art. 15 (dépenses).** La v22/09 ajoute un seuil de 30 000 € (approbation du conseil), présent en ZH et EN mais **absent du texte FR**. FR/ZH/EN désynchronisés.
- **NOUVEAU — Langue.** La v22/09 introduit une couche **EN** en plus de FR/ZH. À retirer pour la version finale FR uniquement (consigne JCH).

**Base de concordance :** la v22/09 confirme les 3 écarts majeurs déjà signalés et en ajoute 2 (seuil 30 K€ non repris en FR ; couche EN à purger). Extrait texte brut conservé dans `tmp/_statuts_2209_extract.txt`.
