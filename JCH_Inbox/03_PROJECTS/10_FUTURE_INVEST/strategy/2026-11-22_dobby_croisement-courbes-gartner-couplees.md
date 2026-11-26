---
project: Future Invest
type: strategy
author: "[[Dobby]]" (lens [[Bruno]])
created: 2026-11-22
status: draft v1 — à valider par JCH
scope: Croisement des courbes Gartner couplées — méthode du décalage des creux
dependance: 2026-11-22_dobby_univers-instruments-trough-gartner.md
---

# Croisement des courbes Gartner couplées — le décalage des creux

## Principe (intuition JC)

Une technologie n'évolue pas sur une courbe isolée : **sa courbe est couplée** à
d'autres. L'IA pilote les data centers, qui pilotent les métaux, qui pilotent
l'énergie. Chaque maillon a **son propre cycle**, et les creux sont **décalés**
dans le temps.

> « Il y a toujours un décalage des creux entre courbes corrélées. Si on comprend
> mieux l'évolution d'une courbe, on peut affiner nos choix. » — JC

Ce décalage est **exploitable** : comprendre la courbe amont (driver) permet
d'anticiper le creux de la courbe aval (driven), avant qu'il ne se produise.

## Pourquoi le décalage existe (structurel, pas accidentel)

Le lag vient de la **nature physique de chaque maillon** :

- **Sentiment / financier** (IA logicielle) : réagit en **jours-semaines**. C'est la courbe rapide.
- **CAPEX** (data centers) : réagit en **trimestres-années** (on n'annule pas un data center à moitié construit).
- **Physique / demande** (métaux, énergie) : réagit en **années** (exploration minière, réseau, réacteurs).

Conséquence : le creux du driver (sentiment) **précède toujours** le creux des
courbes pilotées (physique). La demande physique continue de croître pendant que
le sentiment s'effondre — c'est là que naît la mauvaise évaluation.

## Le graphe de couplage de notre univers

```
IA générative (driver — sentiment, rapide)
        │ pilote
        ▼
Data centers (CAPEX, moyen)  ────────────►  Énergie (gaz, nucléaire/uranium)
        │ pilote                                   ▲
        ▼                                          │
Métaux critiques (cuivre, lithium, nickel) ────────┘
        │ pilote
        ▼
Réseau / électrification (cuivre, argent)
```

| Courbe | Vitesse de cycle | Phase vs IA | Lag estimé | Signal exploitable |
|--------|------------------|-------------|------------|--------------------|
| **IA générative** | rapide (sentiment) | référence | 0 | entrée en trough = top départ |
| **Data centers** | moyen (CAPEX) | en retard | +6–18 mois | le buildout continue après le trough IA |
| **Métaux critiques** (cuivre, uranium, lithium, nickel) | lent (physique) | en retard long | +12–24 mois | la demande suit le buildout, pas le sentiment |
| **Énergie** (gaz, nucléaire) | lent | en retard long | +12–24 mois | idem |
| **Batteries / stockage** (lithium) | lent | en retard long | +18–36 mois | idem |

*Lags à calibrer en Phase 2 (backtest) sur les épisodes 2008 / 2020 / 2026.*

## La règle exploitable — « vente de sympathie » transitoire

Quand le driver (IA) entre en trough, les courbes pilotées subissent une
**vente de sympathie** transitoire : le marché vend tout (cascade de liquidité),
métaux compris — alors que leur demande physique (lag) continue de croître.

**C'est exactement ce qu'on a mesuré cette semaine :**
- IA (driver) : Nasdaq −10,5 % → entre en trough.
- Courbes pilotées : cuivre −9,9 %, argent −16,2 % → **vendues avec**, par flux.
- MAIS leur fondamental (demande data centers, IEA : cuivre +7 Mt à 2040) est **intact** et en retard de phase.

**Conséquence pour nos choix :**
1. La baisse des pilotées pendant le trough du driver est **une baisse de flux, pas de fondamentaux** → fenêtre d'opportunité.
2. Le **creux d'une courbe pilotée** ne coïncide PAS avec le creux du driver — il est **en retard**. Acheter la pilotée « trop tôt » (au creux du driver) = attraper la vente de sympathie ; le vrai point bas de la pilotée arrive **après**, quand la demande physique devient évidente.
3. Lire le driver en temps réel (position Gartner, sentiment) = **anticiper le timing** de la pilotée.

## Opérationnalisation dans l'Event Analyzer

Le décalage des creux **est déjà** la chaîne causale temporelle (Niveau 1 → 4 :
24-72 h → 1-4 semaines → 1-6 mois → >6 mois). On le généralise au **croisement
des courbes** :

1. **Graphe de couplage** : chaque instrument est rattaché à sa courbe + sa courbe amont (driver).
2. **Estimation du lag** : pour chaque lien driver→driven, une fourchette de décalage (à calibrer).
3. **Sortie de l'Opinion Engine enrichie** :
   ```
   instrument: "Futures Cuivre (HG)"
   courbe: "métaux critiques"
   driver: "IA générative" (lag estimé +12-24 mois)
   opinion: "baisse actuelle = vente de sympathie (flux), pas fondamental"
   fenêtre: "point bas attendu APRÈS la stabilisation du driver IA"
   ```

## Double-check humain + IA sur le couplage

Le couplage lui-même est soumis au protocole double-check (cf. doc
`univers-instruments-trough-gartner.md`) :

- **IA** : trace le graphe de couplage + estime les lags (données : IEA, Sprott, capex des hyperscalers).
- **JC (scientifique)** : valide la **causalité physique** du couplage. Exemple : « la
  demande électrique = chaîne génération→transport→distribution→refroidissement,
  chaque maillon = cuivre, aucune substitution court terme » → le lag métaux est
  réel, pas un artefact statistique.

Un couplage validé par les deux = un levier de timing. Un désaccord = ne pas trader ce lag.

## Références

- sprott.com (data centers 460→800 TWh 2026 — le buildout continue)
- iea.org/reports/global-critical-minerals-outlook-2026 (cuivre +7 Mt 2040, demande pilotée par EV/stockage/réseaux)
- globalxetfs.co.jp (pic d'offre minière cuivre fin de décennie — l'offre, encore plus lente, lag double)
- gartner.com (GenAI trough, agentic AI peak — positionnement du driver)
