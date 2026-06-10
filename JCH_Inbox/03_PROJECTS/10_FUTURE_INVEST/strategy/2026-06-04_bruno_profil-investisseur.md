---
project: Future Invest
author: "[[Bruno]]"
created: 2026-06-04
status: partiellement rempli — 2026-06-06 (Dobby analyse comportementale, questions chiffrées en attente)
type: questionnaire
---

# Profil Investisseur — Questionnaire [[Bruno]]

> Remplis chaque champ avec tes mots. Pas besoin de jargon.  
> Tu peux répondre groupe par groupe ou tout d'un coup.

---

## Groupe A — Capital et objectifs

**A1. Montant alloué au projet**

> _(Fourchette approximative. Ne jamais mettre en jeu ce qu'on ne peut pas se permettre de perdre.)_

```
Réponse : 
```

**A2. Objectif financier**

> _(Complément de revenu mensuel / croissance de capital long terme / phase d'apprentissage / autre)_

```
Réponse : Construction d'un système qui fonctionne + croissance de capital à moyen terme.
Pas un objectif de revenu mensuel. L'intérêt intellectuel de l'architecture est aussi
un moteur — le projet est autant une infrastructure d'ingénierie qu'un projet financier.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

**A3. Horizon de jugement du système**

> _(Sur quelle durée veux-tu évaluer si ça fonctionne ? 6 mois, 1 an, 3 ans ?)_

```
Réponse : 2 à 3 ans minimum. Capacité démontrée à tenir des projets sur des décennles
(ZENTECH 2000–2022). Pas de pression de performance à court terme.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

---

## Groupe B — Tolérance au risque

**B1. Réaction instinctive à une perte de 20 % en un mois**

> _(Je coupe tout / Je fais confiance aux règles / J'analyse d'abord)_

```
Réponse : J'analyse d'abord. Aversion au risque non documenté, pas au risque calculé.
Une perte anticipée dans le système est acceptable. Une perte surprise déclenche une
remise en question du système, pas une réaction émotionnelle de vente panique.
Pattern observé : demande systématiquement une analyse avant de valider toute décision
à impact irréversible.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

**B2. Perte maximale acceptable sur une seule journée**

> _(Ce montant deviendra la règle MAX_DAILY_LOSS dans le circuit-breaker.)_

```
Réponse : 
```

**B3. Disponibilité de cet argent**

> _(Capital disponible sans destination prévue dans les 2-3 ans, ou non ?)_

```
Réponse : Capital disponible sans destination prévue sur 2-3 ans. Profil multi-projets
avec revenus de mandats de Board Director (Revatis, Artialis, DIM3). Pas de dépendance
à ce capital pour les besoins courants.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

---

## Groupe C — Disponibilité et style

**C1. Temps disponible par jour/semaine**

> _(Moins d'1h par jour / 1 à 3h par jour / Disponible à plein temps)_

```
Réponse : Moins d'1h par jour en moyenne. 5+ projets actifs simultanément
(WildNexus, Vetalyx, Arteon, IOT van, Photo Nature). Le système doit fonctionner
de façon quasi-autonome — la validation humaine doit être une décision ponctuelle,
pas une surveillance continue.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

**C2. Préférence horaire**

> _(Matin / Soir / Flexible — impact sur les marchés actifs)_

```
Réponse : Flexible. Vie partagée Belgique/Italie + voyages van. Pas d'horaire fixe.
Le système de notification Telegram doit pouvoir atteindre quelle que soit la timezone.
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

**C3. Style de trading préféré**

> _(Trades rapides, quelques minutes à heures, beaucoup de signaux / Trades longs, plusieurs jours, moins d'interventions)_

```
Réponse : Trades longs, event-driven, swing trading (plusieurs jours à 2-3 semaines).
Peu d'interventions. L'architecture même de l'Event Analyzer — construite avant ce
questionnaire — présuppose ce style : sources macro/fondamentales (WASDE, FAO, GDELT),
horizons temporels en semaines dans les outputs de l'Opinion Engine.
[Déduit par analyse architecturale Dobby — confirmé par JCH — 2026-06-06]
```

---

## Groupe D — Univers d'investissement

**D1. Marché qui attire le plus**

| Marché | Description simple | Exemples |
|--------|-------------------|----------|
| Indices boursiers | Direction globale des bourses US ou européennes | S&P 500, Nasdaq, DAX |
| Énergie | Pétrole, gaz — très volatils, liés à la géopolitique | WTI, Brent |
| Métaux | Or, argent — valeurs refuge | Or (GC), Argent (SI) |
| Crypto Futures | Bitcoin, Ethereum — 24h/24, très volatils | BTC Futures CME |
| Taux d'intérêt | Évolution des taux des banques centrales | Obligations US (ZN, ZB) |

```
Marché(s) retenu(s) : Commodités agricoles (blé, riz, maïs, soja) + Énergie (WTI, Brent)
en priorité. Or (GC) possible comme valeur refuge. Indices boursiers en option secondaire.
Raison : Lecture naturelle de l'actualité géopolitique à travers l'impact sur les
ressources naturelles — formation zoologie, 40 ans IVD/diagnostic (chaîne agricole/
alimentaire), projets actifs WildNexus (monitoring biodiversité). Capacité d'analyse
fondamentale des chocs d'offre/demande agricoles directement supérieure à la moyenne.
Crypto Futures exclu : trop spéculatif, déconnecté des fondamentaux lisibles.
Taux d'intérêt : à confirmer — complexité technique élevée pour démarrage.
[Déduit par analyse comportementale Dobby — confirmé par JCH — 2026-06-06]
```

**D2. Expérience en investissement**

> _(Actions, ETF, crypto spot, options… Si oui, lesquels et depuis combien de temps ?)_

```
Réponse : Investisseur en capital-risque et startups depuis 20+ ans (board director
Revatis, Artialis, DIM3, DIAHO China). Expérience trading algorithmique sur marchés
organisés : débutant — c'est l'objet de ce projet. Compréhension fine des mécanismes
de valorisation d'entreprise et des dynamiques sectorielles (IVD, eHealth, biotech).
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

---

## Groupe E — Contexte et contraintes

**E1. Pays de résidence fiscale**

> _(Impacte le choix du broker et la structure juridique.)_

```
Réponse : Belgique (résidence principale — Liège). Double nationalité belge/italienne.
⚠️ Point d'attention Renard : vérifier implications fiscales belges sur les Futures
(taxe sur comptes-titres, traitement des plus-values sur instruments dérivés en Belgique).
[Confirmé par analyse comportementale Dobby — 2026-06-06]
```

**E2. Broker existant**

> _(As-tu déjà un compte chez un courtier ? Si oui, lequel ?)_

```
Réponse : 
```

**E3. Exclusions éthiques ou personnelles**

> _(Secteurs, actifs ou pratiques à exclure pour des raisons éthiques ou personnelles.)_

```
Réponse : 
```

---

## Voir aussi

- [[INDEX|Future Invest — Index projet]]
- [[Bruno]] — analyste finance & investissement
- [[Dobby]] — orchestrateur
