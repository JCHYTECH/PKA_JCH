# WildNexus — 5 Actions Gemma3 : Formalisation

> Généré le 2026-06-07 — Source : analyse gemma3:12b sur fichiers réels + évaluation spécialistes ([[Araignée]], [[Forge]], [[Chouette]])
> Intégré dans `wildnexus-plane-seed-backlog.md`

---

## P0 (3 actions, jalons M-01/M-02)

### Action 1 — Bench courant deep sleep carte complète
| Champ | Valeur |
|-------|--------|
| **Task** | T02.5b |
| **WP** | WP02 — Hardware & Enclos |
| **Responsable** | [[Araignée]] (#30) |
| **Matériel** | Nordic PPK2 ou équivalent |
| **Seuil** | <100 µA cible ; fallback STM32U5 si >150 µA irréductible après optimisation MOSFET |
| **Jalon** | M-02 (Prototype banc fonctionnel) |
| **Source** | gemma3 #A / ADR-001 |

### Action 2 — Protocole test cycle complet 60 jours
| Champ | Valeur |
|-------|--------|
| **Task** | T05.3 |
| **WP** | WP05 — Validation terrain EVT |
| **Responsable** | [[Forge]] (#12) |
| **Protocole** | Deep sleep → réveil → capture → TX → retour veille, avec critères acceptation mesurés |
| **Jalon** | M-02 (avant déploiement terrain) |
| **Source** | gemma3 #F / ADR-005 |

### Action 3 — Test portée LoRa forêt (3 sites)
| Champ | Valeur |
|-------|--------|
| **Task** | T01.3 (renforcé) |
| **WP** | WP01 — Conception & Architecture |
| **Responsable** | [[Chouette]] (#25) + [[Araignée]] (#30) |
| **Sites** | Clairière, sous-bois dense, lisière |
| **Mesures** | SF7 et SF12, distance max fiable, taux perte paquets |
| **Jalon** | M-01 (Architecture gelée) |
| **Source** | gemma3 #C/#H / ADR-003 |

---

## Haute priorité (2 actions, avant S01)

### Action 4 — Gestion condensation boîtier
| Champ | Valeur |
|-------|--------|
| **Task** | T02.3b |
| **WP** | WP02 — Hardware & Enclos |
| **Responsable** | [[Chouette]] (#25) |
| **Solutions** | Pastille déshydratante silica gel 10g (change tous les 3 mois) + évent Gore-Tex M12 |
| **Test** | 48h forêt de Soignes (5°C, brouillard) avant S01 |
| **Source** | gemma3 #G / ADR-006 |

### Action 5 — Extension budget P0
| Champ | Valeur |
|-------|--------|
| **Task** | T01.6 (étendu) |
| **WP** | WP01 — Conception & Architecture |
| **Responsable** | [[Nova]] (#22) + [[Forge]] (#12) |
| **Postes** | Acquisition dataset IR belge faune nocturne, coût stockage cloud/backoffice, frais déplacement EVT terrain |
| **Jalon** | M-01 |
| **Source** | gemma3 #E |

---

## Références croisées

| Action | Point gemma3 | Fichier source | Spécialiste | Verdict |
|--------|-------------|----------------|-------------|---------|
| 1 | A — ESP32-S3 conso | ADR-001 | [[Araignée]] | À nuancer |
| 2 | F — Validation 60j | ADR-005 | [[Forge]] | Accepté |
| 3 | C/H — LoRa forêt | ADR-003 | [[Araignée]] + [[Chouette]] | Accepté |
| 4 | G — Condensation | ADR-006 | [[Chouette]] | À nuancer |
| 5 | E — Budget | Budget Range | [[Forge]] | À nuancer |

*Intégré dans : [[wildnexus-plane-seed-backlog]].md*
