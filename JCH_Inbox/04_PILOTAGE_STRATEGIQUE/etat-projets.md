# État des projets — One-Pager
> Tableau de bord unique de tous les projets actifs PKA_JCH.
> Dernière mise à jour : 2026-10-19 par Dobby 🦉 — deadline IOT Van prolongée au 15/12 (JC). RPi 5 boot résolu, HAOS 18.3. VETALYX réactivé (juridique).
> 
> **Lecture :** 🔴 = P0 deadline dure, 🟢 = actif autonome, ⚪ = gelé/reporté

---

## 🔴 P0 — Deadline 15 décembre 2026 (installation IOT Van)

| # | Projet | Statut | Dernière action | Prochaine étape | Blocage | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|---------|----------------|
| 1 | **IOT / Vanlife** | 🔴 P0 | Van Lupo livré (30/07), RPi 5 boot résolu (NVMe retiré 01/10, HAOS 18.3), hardware quasi complet. | Commander 8 capteurs Zigbee (~88€) + silentblocs + coating, intégrer WiCAN Pro, installer dans le van. | — (deadline 15/12) | Forge, Araignée, Dobby |

---

## 🟢 P1 — Actifs autonomes (pas de charge JC)

| # | Projet | Statut | Dernière action | Prochaine étape | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|----------------|
| 2 | **PHOTO_NATURE** | 🟢 autonome | INDEX à jour, keyworder fonctionnel, presets Argus | — (tourne seul) | Lynx, Nova, Héron |
| 3 | **PHOTO_AI_JURY** | 🟢 autonome | argus_critique.db actif (58 analyses) | Activer MCP Lightroom (30 min JC) | Argus |
| 4 | **AI_IT_TOOLS** | 🟢 autonome | 10 thread files créés, skills actifs | Maintien | Dobby, Forge |

---

## 🔶 Réactivé — VETALYX (juridique, actif depuis août)

| # | Projet | Statut | Dernière action | Prochaine étape | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|----------------|
| 5 | **VETALYX** | 🔶 actif (juridique) | DIAHO 40 % fondateur acté (18/08). Contrat-cadre v3, statuts SRL v22/09, pacte actionnaires v1 + convention bloc v1 produits (30/09). | Appliquer corrections fond juridique (véto DIAHO → statuts), trancher qualification AFMPS/FAMHP, valider avec notaire + UCM. | Renard, Clio, Jade |

---

## ⚪ Gelés — reprise à replanifier

| # | Projet | Statut | Raison du gel | Reprise prévue |
|---|--------|--------|---------------|----------------|
| 6 | **WILDNEXUS** | ⚪ gelé | Bench loop non repris en septembre (focus IOT/VETALYX). Panier Mouser ~279€ non commandé. | À replanifier post-van |
| 7 | **ARTEON + WildLens** | ⚪ gelé | Relance éditoriale exige créativité JC | À replanifier |
| 8 | **InsectNet** | ⚪ gelé | Migration M1 non urgente | À replanifier |
| 9 | **TRAVELS** | ⚪ gelé | Planif voyage en roulant. Meuble banquette 104×55×25 en design. | En roulant |
| 10 | **NEXUS_ACOUSTIC** | ⚪ gelé | Dépend de WildNexus P0 | Post-WildNexus |

---

## Projets inactifs / archivés

| Projet | Statut | Note |
|--------|--------|------|
| WILDMESH | ⚪ gelé | Réseau LoRa mesh — en attente de maturité WildNexus |
| FUTURE_INVEST | ⚪ gelé | Archivé le 2026-06-23 |
| Maison off-grid | ⚪ concept | Phase concept uniquement |
| FAUNE_AUTOUR | ⚪ gelé | PWA extraite dans PHOTO_NATURE |

---

## Résumé

| Indicateur | Valeur |
|------------|--------|
| Projets totaux | 10 |
| 🔴 P0 (deadline dure) | 1 — IOT/Vanlife |
| 🔶 Réactivé | 1 — VETALYX (juridique) |
| 🟢 P1 (autonome) | 3 — PHOTO_NATURE, PHOTO_AI_JURY, AI_IT_TOOLS |
| ⚪ Gelés | 5 — WILDNEXUS, ARTEON, InsectNet, TRAVELS, NEXUS_ACOUSTIC |
| Prochaine échéance | **15 décembre 2026** — installation IOT Van |

---

## Relations inter-projets photo

```
PHOTO_NATURE (terrain, technique, keyworder)
        │
        │ photos brutes + presets Argus
        ▼
PHOTO_AI_JURY (moteur IA Argus — 58 analyses, MCP LR)
        │
        │ rapports PDF + presets XMP + conseil papier
        ▼
ARTEON (shop + marque + L'Instant Lu)
        │
        │ acquisition
        ▼
WildLens (journal hebdomadaire — tête du funnel)
```

*Mise à jour par Dobby 🦉 à chaque changement d'état d'un projet.
Source : MEMORY.md, TEAM_Inbox/, 03_PROJECTS/, kanban, wiki/Daily.*
