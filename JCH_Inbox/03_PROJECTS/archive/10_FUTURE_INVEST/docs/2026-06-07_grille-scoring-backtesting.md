---
project: Future Invest
type: scoring-grid
author: "[[Bruno]]" + "[[Dobby]]"
created: 2026-06-07
status: validé — à appliquer en Phase 2
---

# Grille de Scoring — Backtesting Phase 2

> Définit ce que signifie "correct" pour les 10 analyses rétrospectives.
> Objectif : atteindre ≥ 7/10 avant de passer au paper trading.
> Sans cette grille, le score est subjectif et inutilisable.

---

## 1. Les 3 dimensions d'évaluation

Chaque analyse rétrospective est notée sur **3 dimensions indépendantes** :

| Dimension | Poids | Question centrale |
|---|---|---|
| **D1 — Direction** | 40 % | Le système a-t-il prédit le bon sens (hausse / baisse / neutre) ? |
| **D2 — Instrument** | 30 % | A-t-il identifié le bon instrument financier impacté ? |
| **D3 — Horizon** | 30 % | L'impact s'est-il produit dans la fenêtre temporelle prédite ? |

---

## 2. Barème par dimension

### D1 — Direction (40 pts max)

| Résultat | Score | Définition |
|---|---|---|
| Direction correcte | 40 | Hausse prédite + hausse réelle, ou baisse + baisse |
| Direction neutre prédite, mouvement réel < 2% | 40 | Prédiction de stabilité validée |
| Direction incorrecte | 0 | Hausse prédite, baisse réelle (ou inverse) |
| Pas d'opinion formulée | 20 | Le système a refusé de se prononcer — ni bonus ni malus total |

### D2 — Instrument (30 pts max)

| Résultat | Score | Définition |
|---|---|---|
| Instrument principal correct | 30 | L'instrument le plus impacté est dans le top 2 de l'Opinion Engine |
| Instrument de même famille | 20 | Ex : ZW prédit, ZC réellement impacté (tous deux grains) |
| Instrument d'un secteur adjacent | 10 | Ex : blé prédit, pétrole impacté (corrélation indirecte) |
| Instrument incorrect | 0 | Aucun des instruments prédits n'a bougé significativement |

### D3 — Horizon (30 pts max)

| Résultat | Score | Définition |
|---|---|---|
| Impact dans la fenêtre prédite ± 30 % | 30 | Horizon "1-4 semaines" → impact entre J+7 et J+36 |
| Impact hors fenêtre mais même direction | 15 | Direction correcte, timing décalé au-delà de ±30% |
| Impact dans la fenêtre mais trop tardif | 10 | Impact réel arrivé après la fenêtre |
| Pas d'impact mesurable | 0 | Aucun mouvement > 3% sur l'instrument dans les 3 mois |

---

## 3. Score total et verdict

| Score total (/100) | Verdict | Signification |
|---|---|---|
| 80–100 | ✅ Juste | Analyse fiable, utilisable en trading |
| 50–79 | ⚠️ Partiellement juste | Logique correcte, calibrage à affiner |
| 0–49 | ❌ Faux | Revoir les prompts ou les sources concernées |

**Seuil de passage en paper trading : ≥ 7 analyses avec score ≥ 50/100**
(dont au moins 3 avec score ≥ 80/100)

---

## 4. Fiche de scoring — Template par événement

```markdown
## Événement : [Titre]
**Date réelle :** YYYY-MM-DD
**Source :** [référence]

### Analyse générée par l'Event Analyzer
- Direction prédite : [haussier / baissier / neutre]
- Instrument(s) identifié(s) : [liste]
- Horizon prédit : [ex: 1-4 semaines]
- Conviction : [forte / modérée / faible]

### Ce qui s'est réellement passé
- Mouvement réel : [ex: ZW +8% en J+12]
- Instrument le plus impacté : [ex: ZW Chicago]
- Délai réel : [ex: J+12]

### Scoring
| Dimension | Score | Justification |
|---|---|---|
| D1 Direction | /40 | |
| D2 Instrument | /30 | |
| D3 Horizon | /30 | |
| **Total** | **/100** | |
| **Verdict** | ✅/⚠️/❌ | |

### Leçons
- Ce que le système a bien vu :
- Ce qu'il a raté :
- Ajustement prompt suggéré :
```

---

## 5. Les 10 événements rétrospectifs (Phase 2.1)

| # | Événement | Marché principal | Difficulté estimée |
|---|---|---|---|
| 01 | 2010 — Embargo export blé Russie | ZW (Blé Chicago) | Moyenne |
| 02 | 2012 — Sécheresse maïs USA | ZC (Maïs Chicago) | Faible |
| 03 | 2020 — Pétrole négatif (COVID) | CL (WTI) | Élevée |
| 04 | 2021 — Blocage canal de Suez | Indices + pétrole | Élevée |
| 05 | 2022 — Guerre Ukraine (blé, engrais) | ZW + fertilisants | Moyenne |
| 06 | 2023 — Ban export riz Inde | Riz + substituts | Moyenne |
| 07–10 | À définir selon marchés retenus (D1 profil) | TBD | TBD |

---

## Voir aussi

- [[2026-06-04_checklist-lancement]] — Phase 2 backtesting
- [[2026-06-04_event-analyzer-architecture]] — architecture Event Analyzer
- [[Bruno]] — validation des scorings
- [[Dobby]] — orchestrateur
