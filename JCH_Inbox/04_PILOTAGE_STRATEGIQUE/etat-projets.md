# État des projets — One-Pager
> Tableau de bord unique de tous les projets actifs PKA_JCH.
> Dernière mise à jour : 2026-07-11 par Dobby 🦉 — Skill pka-thread-file terminé, IOT thread mis à jour post-stabilisation Lupo (deadline 7 août, arrivée Lupo). 6 projets gelés jusqu'à septembre.
> 
> **Lecture :** 🔴 = P0 deadline dure, 🟢 = actif autonome, ⚪ = gelé/reporté

---

## 🔴 P0 — Deadline 7 août 2026 (arrivée Lupo)

| # | Projet | Statut | Dernière action | Prochaine étape | Blocage | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|---------|----------------|
| 1 | **IOT / Vanlife** | 🔴 P0 | RPi 5 assemblé (SSD + UPS HAT + accus 18650), Mouser reçu, Sonde TL-136 reçue, Step-Down HW-133 reçu, ADS1115×6 reçus | Mise en boîtier X1201-C1 + silentblocs + coating + PV PI HAT + config HA finale + commander capteurs Zigbee + préparer install Lupo | — | Forge, Araignée, Dobby |

---

## 🟢 P1 — Actifs autonomes (pas de charge JC)

| # | Projet | Statut | Dernière action | Prochaine étape | Spécialiste(s) |
|---|--------|--------|-----------------|-----------------|----------------|
| 2 | **PHOTO_NATURE** | 🟢 autonome | INDEX à jour (02/07), keyworder fonctionnel, 11 presets Argus | — (tourne seul) | Lynx, Nova, Héron |
| 3 | **PHOTO_AI_JURY** | 🟢 autonome | argus_critique.db actif (58 analyses), prompt calibré (14/06) | Activer MCP Lightroom (30 min JC) | Argus |
| 4 | **AI_IT_TOOLS** | 🟢 autonome | P0-P2 terminés (19/06), hub OpenRouter restructuré (01/07) | ✅ Skill pka-thread-file terminé (10/07), 10 thread files créés. IOT mis à jour 11/07. | Dobby, Forge |

---

## ⚪ Gelés — Reprise septembre 2026 (post-van)

| # | Projet | Statut | Raison du gel | Reprise prévue |
|---|--------|--------|---------------|----------------|
| 5 | **WILDNEXUS** | ⚪ gelé | Hardware reçu, mais bench loop = temps long. Septembre idéal. | Septembre |
| 6 | **ARTEON + WildLens** | ⚪ gelé | Relance éditoriale exige créativité JC, pas le moment | Septembre |
| 7 | **InsectNet** | ⚪ gelé | Migration M1 non urgente | Septembre |
| 8 | **TRAVELS** | ⚪ gelé | Docs créées (apps-roadtrip, Lupo Planner PWA). Planif voyage = en roulant en août. | En roulant (août) |
| 9 | **VETALYX** | ⚪ gelé | En veille depuis juin | Septembre |
| 10 | **NEXUS_ACOUSTIC** | ⚪ gelé | Dépend de WildNexus P0 | Post-WildNexus |

---

## Projets inactifs / archivés

| Projet | Statut | Note |
|--------|--------|------|
| WILDMESH | ⚪ gelé | Réseau LoRa mesh — en attente de maturité WildNexus |
| FUTURE_INVEST | ⚪ gelé | Archivé le 2026-06-23 — Freeze décidé par JC |
| Maison off-grid | ⚪ concept | 60 m² bois sur 9 000 m² — phase concept uniquement |
| FAUNE_AUTOUR | ⚪ gelé | PWA extraite dans PHOTO_NATURE — gelée |

---

## Résumé

| Indicateur | Valeur |
|------------|--------|
| Projets totaux | 10 |
| 🔴 P0 (deadline dure) | 1 — IOT/Vanlife |
| 🟢 P1 (autonome) | 3 — PHOTO_NATURE, PHOTO_AI_JURY, AI_IT_TOOLS |
| ⚪ Gelés | 6 — WILDNEXUS, ARTEON, InsectNet, TRAVELS, VETALYX, NEXUS_ACOUSTIC |
| Prochaine échéance | **7 août 2026** — arrivée Lupo, IOT doit être prêt |
| Prochaine échéance secondaire | ✅ Terminé — skill pka-thread-file livré le 11/07 |

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
Source : MEMORY.md, TEAM_Inbox/, 03_PROJECTS/, kanban.*
