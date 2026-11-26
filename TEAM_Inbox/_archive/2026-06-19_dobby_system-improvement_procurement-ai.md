# Analyse système — AI Agents Reshaping Electronics Procurement
> Grille 6 axes — system-improvement-ingest
> Date : 2026-06-19 | Source : NoteGPT Transcript (Podcast Controllers and Podcast)

---

## Résumé du document

Podcast avec Alan et Karan, co-fondateurs de **Bedrock Chain** — startup norvégienne qui automatise le procurement pour les EMS (Electronic Manufacturing Services). MVP en une semaine, 5 co-fondateurs (4 AI + 1 mécanique/procurement). Fonctionnalités : upload BOM → nettoyage → matching fournisseurs → RFQ automatisé. Discussion sur la sécurité supply chain, les lead times, et l'impact des tarifs.

---

### AXE 1 — EXACTITUDE DU CONTENU ET DU CODE

**Insight :** Bedrock automatise le nettoyage de BOM — détection d'erreurs, matching fournisseurs, RFQ standardisé. Leur argument : les humains oublient des lignes dans les spreadsheets, les lead times sont obsolètes.

**Applicabilité PKA :**
- **WildNexus** : notre pipeline procurement (`scripts/procurement/`) fait déjà du dual-search Mouser/DigiKey + validation MPN. Bedrock confirme la direction.
- **Amélioration possible** : ajouter un « BOM health check » automatique avant chaque commit BOM — vérifier que chaque ligne a un MPN valide, un prix < 24h, un lead time vérifié.
- **Priorité :** P2 | **Effort :** faible (extension du script existant)

---

### AXE 2 — MÉMOIRE ET APPRENTISSAGE CONTINU

**Insight :** Bedrock insiste sur « avoir l'information quand on en a besoin » — lead times, tarifs, disponibilité en temps réel.

**Applicabilité PKA :**
- Notre `supply_cache` dans team.db stocke déjà les résultats de recherche. 
- **Amélioration** : auto-invalider les entrées cache après 7 jours (lead times changent), envoyer une alerte si un composant BOM change de statut (obsolète, NRND, lead time ×5).
- **Priorité :** P2 | **Effort :** moyen

---

### AXE 3 — TRANSVERSALITÉ ENTRE MODÈLES

**Insight :** Aucun insight direct — le document est centré procurement, pas architecture agent.

---

### AXE 4 — INTUITION DU SYSTÈME

**Insight :** « You need an AI hero in your company to give you that push » — idée qu'une PME a besoin d'un agent IA interne pour rester compétitive.

**Applicabilité PKA :**
- PKA est exactement cet « AI hero » pour les projets de JC.
- **Amélioration** : Dobby pourrait scanner proactivement les BOMs et suggérer des alternatives quand un composant devient NRND.
- **Priorité :** P2 | **Effort :** moyen

---

### AXE 5 — ARBOR ET LOOPS

**Insight :** « AI agents running continuously to break into supply chain systems » → pénétration testing automatisé.

**Applicabilité PKA :**
- Notre `pka_prompt_guard.py` est un début. On pourrait étendre avec un « security loop » : agent qui teste les endpoints PKA en continu → rapport de vulnérabilités.
- **Arbor Loop candidate :** « Security Audit Loop » — hypothèse = « ce endpoint est vulnérable » → test → correctif → re-test.
- **Priorité :** P2 | **Effort :** élevé

---

### AXE 6 — INNOVATION ARCHITECTURALE GLOBALE

**Insight :** Bedrock = startup à 5 qui a fait un MVP en 1 semaine. Leçon : itération rapide > perfection.

**Applicabilité PKA :**
- Pour les nouveaux outils PKA, appliquer la règle « MVP en une session, pas en un mois ».
- Exemple : `pka_memory_nudge.py` codé en une session aujourd'hui.

---

## Synthèse

- **Top insight :** BOM health check automatique — applicable immédiatement à WildNexus
- **Recommandation :** Étendre le pipeline procurement avec cache auto-invalidant (7j)
- **Projets :** WildNexus (procurement), AI_IT_TOOLS (sécurité)
- **Fichier :** pas de P0 — document informatif, confirme la direction existante
