# Mandat — FTO WildNexus v0.2

**De :** [[Dobby]] 🦉  
**À :** [[Renard]] 🦊 + [[Hermine]] ⬜  
**Date :** 2026-05-30  
**Priorité :** 🟡 Medium (ne bloque pas le proto M-02, mais prend du temps — à lancer maintenant)

---

## Contexte

Le projet WildNexus entre en phase M-02 (prototype banc). Le matériel est en cours de procurement. Aucune analyse **Freedom to Operate (FTO)** ni stratégie de licence n'a encore été produite.

Le rapport d'exécution WP02 du 2026-05-25 identifie cette action comme parallélisable : elle ne bloque pas le prototype matériel, mais bloque toute publication future et toute exploitation commerciale. La [[daily]] du 2026-05-17 mentionnait déjà le besoin de « mandater [[Renard]] sur FTO + sélection licences open source » — le mandat n'a jamais été exécuté.

Le document fondateur WildNexus (§5 et §9) liste le FTO comme non-négociable et place [[Renard]] comme owner des clauses contractuelles et licences.

---

## Objectif

Produire une **note juridique FTO v0.2** couvrant :

### 1. Analyse FTO (Freedom to Operate)
- Cartographier les brevets actifs dans les domaines suivants :
  - Caméra-piège déclenchée par capteur PIR + IA edge
  - Réseau LoRa mesh pour monitoring faune
  - Classification audio embarquée (BirdNET-like)
- Identifier les risques de contrefaçon pour un prototype non [[commercial]] (P0) et pour une exploitation future
- Signaler tout brevet bloquant nécessitant un avis externe

### 2. Licences open source
- Auditer les dépendances logicielles identifiées dans l'architecture P0 :
  - BirdNET / BirdNET-Go / BirdNET-Pi
  - Home Assistant (si utilisé comme base)
  - Framework nRF Connect SDK (Nordic)
  - Bibliothèques Python d'analyse (librosa, TensorFlow Lite…)
- Vérifier la compatibilité des licences entre elles (GPL, MIT, Apache, CC)
- Recommander une licence pour le projet WildNexus lui-même

### 3. RGPD & terrain
- Statut juridique des enregistrements audio en milieu naturel (Belgique)
- Obligations de signalétique sur le terrain (pancarte information)
- Procédure de floutage/anonymisation si capture accidentelle de personnes

### 4. Propriété intellectuelle
- Clarifier la propriété du code, des designs hardware, et des données collectées
- Statut de JCH comme inventeur vs. contributeurs open source
- Clause de non-concurrence éventuelle avec Vetalyx / JCHYTECH

---

## Livrable attendu

- Fichier : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/FTO/2026-05-XX_renard-hermine_fto-wildnexus-v0.2.md`
- Format : analyse structurée, pas un avis juridique formel (budget P0 : pas de conseil PI externe pour l'instant)
- Sections : FTO brevets | Licences open source | RGPD terrain | PI
- Pour chaque brevet identifié : numéro, titulaire, périmètre, risque estimé (faible/moyen/élevé)

---

## Contraintes

- **Budget :** 0 € — analyse interne uniquement (pas de conseil PI externe en P0)
- **Délai :** 1 semaine (pas bloquant pour M-02, mais doit être prêt avant toute publication)
- **Périmètre :** P0 uniquement — ne pas anticiper P1/P2 sauf si un brevet identifié les impacte directement

---

## Références

- [[wildnexus-founding-document-v0.2]] — §5 (Non-négociables), §9 (Propriété intellectuelle)
- [[WILDNEXUS_ADR_INDEX]] — ADR-001 à ADR-009 (décisions techniques à auditer)
- [[2026-05-25_rapport_execution_serie_parallele_WP02]] — T01.2 Licence/FTO
- [[WILDNEXUS_P0_BUDGET_RANGE]] — exclusion FTO externe
- `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/05_VISUALS_DASHBOARDS/wildnexus-flowmap.html` — flux décisionnel
