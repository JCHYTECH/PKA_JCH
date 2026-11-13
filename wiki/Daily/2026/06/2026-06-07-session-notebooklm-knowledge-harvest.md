---
date: 2026-06-07
tags: [daily, session, notebooklm, knowledge-harvest]
type: daily
status: active
model: claude-sonnet-4-6
projects: [Vetalyx, WildNexus, Photo_Nature, Photo_AI_Jury, Travels, IOT, Future_Invest]
---

# Session 2026-06-07 — NotebookLM Knowledge Harvest

## Actions

### NotebookLM — Mise en place et analyse multi-projets
- Découverte des fichiers `NOTEBOOKLM_SOURCES.md` et `notebook_sources/` déjà préparés pour WildNexus, Photo_AI_Jury, Photo_Nature
- Analyse de 9 rapports NotebookLM depuis l'inbox (traités + archivés dans `.processed`)

### Vetalyx
- Analyse rapport "Le Challenger Pragmatique" + "Adaptation Panel Allergène Europe"
- Création `strategy/VETALYX_CLAIMS_MATRIX_FR.md` — message canonique FR, frontière alimentaire, terme "intolérance" banni, comparatif concurrentiel
- Formalisation `strategy/decisions.md` :
  - **DEC-001** — CCD Interference Policy : pas de CCD blocker au lancement, documentation obligatoire v1, intégration v2 après KOL (analyse Vasco — format lignes mixtes réduit l'impact, option B retenue)
  - **DEC-002** — Architecture produit : 3 SKUs régionaux (France/Benelux, Méditerranée, Allemagne/Europe Centrale) + fallback hybride

### WildNexus
- Analyse rapports synthèse stratégique + jalons critiques NotebookLM
- Création `ADR-006-boitier-ip67-p0.md` — Hammond 150×100×60mm, IP67, -10/+45°C, dos concave 10-40cm, Hammond commercial retenu vs 3D PETG
- Création `ADR-010-securite-rgpd-edge-ai.md` — filtre humain Edge AI VGA, chiffrement SD AES-128, signature firmware, trigger migration MCU (RV1106/STM32N6 si trop lourd)
- Clarification dissonances : énergie 60j/6mois = hiérarchie P0/P1 (solaire retiré P0), ESP32-S3 trigger migration = deep sleep >100-200µA ou NPU insuffisant

### IoT / Vanlife
- Analyse rapport WildNexus×Stylevan Equinox 4
- Ajout `is_overnight: false` + `score_confiance: 0` dans frontmatter YAML PKA_DECOUVERTES
- Ajout section "Check-out autonomie van" dans `routine-cigogne.md` (SOC ≥80%, Eau ≥50L, Frigo ≤7°C, Gaz = angle mort signalé)
- Spec Forge "Feedback Spot Lovelace" (5h) — pipeline bouton → `write_feedback.py` → vault

### Photo Nature
- Documentation limitation GBIF dans `docs/faune-autour.md` : délai sync semaines/mois, embargo espèces rares (Natagora), plan de secours dictionnaire local 110 entrées
- Workflow IA zones de transition : exclure reflet direct sujet, masque fusion 0.5–2px

### Photo AI Jury
- Création `notebooklm-spec-metaphore-impact-visuel.md` :
  - 5 indicateurs Impact Visuel (axe 5) extraits des 12 rapports Argus
  - Matrice détection métaphore "Résistance/Vitalité" : espèce petite + bec >15° + plumes gonflées + temp <5500K + contre-plongée
  - Diagnostic exposition : analyse histogrammes séparés hautes lumières/ombres
  - Variables d'écart de notes documentées

### Future Invest
- Analyse comportementale approfondie de JCH → profil investisseur déduit
- Remplissage partiel questionnaire Bruno (9/12 champs) : style swing/event-driven confirmé, marchés commodités agricoles + énergie, horizon 2-3 ans, HITL comme valeur
- Création `architecture/2026-06-07_contraintes-style-trading.md` — biais implicite formalisé, marchés compatibles, limites connues
- Création `docs/2026-06-07_grille-scoring-backtesting.md` — 3 dimensions (Direction 40%, Instrument 30%, Horizon 30%), barème, template fiche, 6 événements rétrospectifs listés
- Ajout protocole HITL timeout dans checklist : timeout 4h → archivage, 24h → flag "fenêtre manquée", aucune auto-exécution quelle que soit la conviction
- Mise à jour INDEX.md Future Invest

### Infrastructure PKA
- 9 rapports NotebookLM archivés dans `.processed`
- "Move delete.md" remis dans inbox sur demande

## Décisions

| Décision | Projet | Rationale |
|---|---|---|
| DEC-001 CCD = documentation + disclosure, pas hard gate | Vetalyx | Test de triage ≠ test moléculaire — standard Heska/Allercept, pas Nextmune PAX |
| DEC-002 3 SKUs régionaux physiques | Vetalyx | Panel unique insuffisant pour couvrir EU5 |
| ADR-006 Hammond commercial vs 3D PETG | WildNexus | IP67 long terme non garanti en PETG |
| ADR-010 filtre humain Edge AI sur nœud | WildNexus | RGPD by design — pas de transmission données sensibles |
| Style trading = swing event-driven | Future Invest | Déduit de l'architecture elle-même + profil JCH |
| HITL timeout 4h = archivage, jamais auto-exec | Future Invest | Valeur fondamentale JCH : décision finale appartient à l'humain |

## Prochaines étapes

- **Vetalyx** : compléter la demande CCD à DIAHO/DIXUN (J0-15) ; confirmer faisabilité 3 SKUs
- **WildNexus** : valider dimensions Hammond retenu vs volume interne PCB + holders AA
- **Future Invest** : remplir les 4 questions ouvertes (A1 montant, B2 MAX_DAILY_LOSS, E2 broker, E3 exclusions éthiques) → calibrer circuit-breaker
- **IoT** : résoudre SSH RPi (bloqueur ouvert depuis 05-06) avant implémentation Feedback Spot Lovelace
- **Photo AI Jury** : spécifier feature preset LR auto-généré depuis scores (Forge)

## Voir aussi

- [[VETALYX_CLAIMS_MATRIX_FR]]
- [[2026-06-07_contraintes-style-trading]]
- [[2026-06-07_grille-scoring-backtesting]]
- [[ADR-006-boitier-ip67-p0]]
- [[ADR-010-securite-rgpd-edge-ai]]
- [[Dobby]] · [[Vasco]] · [[Forge]] · [[Bruno]] · [[Argus]]
