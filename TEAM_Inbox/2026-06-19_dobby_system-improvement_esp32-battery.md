# Analyse système — ESP32 Lithium Battery Power
> Grille 6 axes — system-improvement-ingest
> Date : 2026-06-19 | Source : NoteGPT Transcript (YouTube Quick Tips)

---

## Résumé du document

Tutoriel vidéo : alimenter un ESP32 avec une batterie lithium 3.7V. Problème : l'AMS1117 a un dropout voltage de 1.2V → besoin de 4.5V minimum en entrée pour réguler à 3.3V. Une batterie lithium (4.2V max) est trop basse → le régulateur passe en pass-through bruyant → lectures ADC faussées. Solution : boost converter 5V → AMS1117 → 3.3V stable.

---

### AXE 1 — EXACTITUDE DU CONTENU ET DU CODE

**Insight :** Le dropout voltage de l'AMS1117 est un piège classique. Si on lit la tension batterie via ADC avec une référence 3.3V instable, les lectures sont fausses. La solution est un boost converter.

**Applicabilité PKA :**
- **WildNexus** : tout design firmware qui lit une tension batterie doit utiliser une référence stable. Si on alimente l'ESP32-CAM directement en li-ion, les lectures ADC seront faussées.
- **Action immédiate :** vérifier les specs d'alimentation dans les SOPs WildNexus. Ajouter une note « AMS1117 dropout = 1.2V → boost converter obligatoire si li-ion seule ».
- **Priorité :** **P0 — critique pour la précision des mesures WildNexus**
- **Fichiers impactés :** `03_WILDNEXUS/03_P0_ENGINEERING/PROTOCOLES/` (SOP power)

---

### AXE 2 — MÉMOIRE ET APPRENTISSAGE CONTINU

**Insight :** Le transcript est un cas d'école de « leçon apprise sur le terrain » — l'auteur a découvert le dropout voltage en mesurant, pas en lisant la datasheet.

**Applicabilité PKA :**
- **Pattern :** toute leçon hardware découverte par l'équipe (Chouette, Araignée, Fourmi) devrait être capturée comme `knowledge` dans team.db avec le tag `hardware-lesson`.
- Notre Memory Nudge pourrait détecter ce type de pattern dans les rapports TEAM_Inbox.
- **Priorité :** P1 | **Effort :** faible

---

### AXE 3 — TRANSVERSALITÉ ENTRE MODÈLES

**Insight :** Aucun — document purement hardware.

---

### AXE 4 — INTUITION DU SYSTÈME

**Insight :** Le piège du dropout voltage n'est pas évident à la lecture de la datasheet. L'auteur l'a découvert par la mesure.

**Applicabilité PKA :**
- Dobby pourrait maintenir une base de « pièges hardware connus » et les suggérer proactivement quand un design les rencontre.
- Exemple : si un spécialiste propose un schéma avec AMS1117 + li-ion → Dobby alerte « attention dropout voltage ».
- **Priorité :** P2 | **Effort :** moyen

---

### AXE 5 — ARBOR ET LOOPS

**Insight :** Le processus de découverte (mesurer → constater anomalie → chercher la cause → corriger) est une micro boucle scientifique.

**Applicabilité PKA :**
- C'est le pattern exact de `bench-loop` : exécuter SOP → mesurer → dans spec ? → corriger → re-mesurer.
- **Renforcement :** la bench-loop devrait inclure une phase « leçon apprise → knowledge base » en sortie.
- **Priorité :** P1 | **Effort :** faible (extension bench-loop)

---

### AXE 6 — INNOVATION ARCHITECTURALE GLOBALE

**Insight :** Le transcript montre l'importance de la **validation physique** — les specs papier ne suffisent pas, il faut mesurer.

**Applicabilité PKA :**
- Renforce la philosophie WildNexus : Wokwi pour le smoke test logique, mais le banc hardware (PPK2 + Fourmi) pour les mesures réelles.
- Aucun changement architectural — c'est une confirmation.

---

## Synthèse

- **Top 3 insights :**
  1. ⚠️ Dropout voltage AMS1117 = piège pour les lectures ADC — **P0 WildNexus**
  2. Leçons hardware doivent être capturées automatiquement — P1 mémoire
  3. Bench-loop doit inclure une sortie « leçon apprise » — P1 loop
- **Recommandation principale :** Vérifier les specs d'alimentation WildNexus et ajouter une contrainte « boost converter si li-ion seule »
- **Projets :** WildNexus (power management), bench-loop
- **Arbor Loop candidate :** non — plutôt une extension de bench-loop existante
