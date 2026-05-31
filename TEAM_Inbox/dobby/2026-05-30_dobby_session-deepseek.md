# Session 2026-05-30 — [[Dobby]] DeepSeek TUI

**Modèle :** DeepSeek V4 (deepseek-tui v0.8.39)
**Projets :** PKA Système, Vanlife IOT, WildNexus

---

## Résumé

Session multi-projets en 4 phases : synchronisation système, traitement [[inbox]] vanlife, audit procurement WildNexus, et mandat FTO.

---

## Actions réalisées

### 1. Resynchronisation des pointers système
- Script `generate_tool_pointers.py` exécuté → 4 fichiers mis à jour (CLAUDE.md, AGENTS.md, GEMINI.md, DEEPSEEK.md)
- Compte corrigé de 28→29 membres, 27→28 spécialistes
- [[Cigogne]] #29 ajoutée dans toutes les listes (config canonique, ADAPTER-PROMPT.md, roster CLAUDE.md)
- ADAPTER-PROMPT.md : 5 corrections + date mise à jour
- Fichiers modifiés : `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `DEEPSEEK.md`, `ADAPTER-PROMPT.md`, `tool_pointer_config.json`

### 2. Traitement [[inbox]] IOT vanlife
- Fichier brut `JCH_Inbox/00_INBOX/IOT vanlife` (1158 lignes, conversation LLM) analysé et recadré
- Création de 2 documents structurés dans `JCH_Inbox/03_PROJECTS/07_TRAVELS/vanlife/logistique/` :
  - `rpi-vanlife-guide-complet.md` (462 lignes) — référence : specs, schémas, budgets, YAML, leçons WildNexus §10
  - `rpi-vanlife-mode-emploi.md` (386 lignes) — mode d'emploi : 8 étapes ordonnées, validations, troubleshooting
- Leçons WildNexus croisées : undervoltage RPi 5, SSD vs microSD, conflits SQLite, ports erronés, autoconnexion Wi-Fi
- Fichier original déplacé → `JCH_Inbox/00_INBOX/.processed/`

### 3. Audit procurement WildNexus
- 3 composants MANUEL du rapport [[Forge]] (26/05) résolus :
  - PIR basse conso → Panasonic EKMB1303111K (Mouser BE, ~20€)
  - microSD industrielle → Swissbit S-45U 16 GB pSLC (DigiKey BE, ~18€ × 3)
  - Alimentation labo → RD UM24C (Amazon.de, ~35€)
- Rapport consolidé → `TEAM_Inbox/2026-05-30_Dobby_procurement_WILDNEXUS_update.md`
- Panier Mouser groupé : 11 composants, ~279€ — prêt à commander
- Total projeté : ~736€ / 1000€ — marge 264€

### 4. Mandat FTO WildNexus
- Mandat émis pour [[Renard]] + [[Hermine]] → `TEAM_Inbox/renard/2026-05-30_dobby_mandat-fto-wildnexus-v0.2.md`
- Périmètre : FTO brevets, licences open source, RGPD terrain, PI
- Budget 0€, délai 1 semaine, ne bloque pas M-02

---

## Décisions

- [2026-05-30] [Système] Pointers resynchronisés — 29 membres confirmé partout, [[Cigogne]] intégrée
- [2026-05-30] [Vanlife] Documentation RPi vanlife structurée en 2 docs (réf + mode d'emploi) avec leçons WildNexus
- [2026-05-30] [WildNexus] Procurement : 3 MANUEL résolus via shortlist existante — MPN déjà documentés
- [2026-05-30] [WildNexus] FTO : mandat émis pour [[Renard]]+[[Hermine]] — analyse interne, 0€

---

## Prochaines étapes

- **JCH** : commander PPK2 (~100€, Mouser BE) — bloque M-02
- **JCH** : valider panier Mouser groupé (~279€)
- **[[Dobby]]** : contacter Arducam (confirmation caméra OV5640)
- **[[Dobby]]** : demander devis Lensation (lentilles M12)
- **[[Renard]] + [[Hermine]]** : produire note FTO v0.2 (délai 1 semaine)
- **[[Forge]]** : grouper panier Mouser, supply register
- **[[Forge]] + [[Castor]]** : stratégie tests firmware
- **[[Nova]] + [[Clio]]** : pipeline classifieur
