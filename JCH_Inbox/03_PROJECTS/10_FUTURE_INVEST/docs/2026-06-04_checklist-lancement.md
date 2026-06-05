---
project: Future Invest
type: checklist
author: "[[Dobby]]"
team: ["[[Bruno]]", "[[Forge]]"]
created: 2026-06-04
status: en cours
---

# Checklist de Lancement — Future Invest

> Cocher chaque item dans l'ordre. Ne pas passer à la phase suivante
> si des items bloquants de la phase précédente sont ouverts.

---

## PHASE 0 — Fondations (avant toute ligne de code)

### 0.1 Profil investisseur
- [ ] Remplir le questionnaire [[Bruno]] → `strategy/2026-06-04_bruno_profil-investisseur.md`
- [ ] [[Bruno]] analyse les réponses et produit le profil finalisé
- [ ] Marchés cibles identifiés (ex. : E-mini S&P 500, Or, Blé…)
- [ ] Paramètres de risque de départ définis :
  - `MAX_DAILY_LOSS` = ___
  - `MAX_DRAWDOWN_PCT` = ___
  - `MAX_POSITION_SIZE` = ___

### 0.2 Recherche communautaire DIY
- [ ] Exécuter le prompt de recherche → `research/2026-06-04_prompt-recherche-diy.md`
- [ ] Sauvegarder les résultats → `research/2026-06-04_resultats-recherche-diy.md`
- [ ] Extraire les recommandations applicables à notre architecture

### 0.3 Formation personnelle minimale ([[Bruno]] recommande)
- [ ] Comprendre ce qu'est un contrat Futures (taille, marge, expiration, rollover)
- [ ] Comprendre l'effet de levier et ses conséquences concrètes
- [ ] Lire la documentation IBKR sur les Futures (gratuit, section "Education")
- [ ] Tester manuellement 5 trades sur la plateforme paper IBKR

---

## PHASE 1 — Environnement technique

### 1.1 Broker
- [ ] Ouvrir un compte Interactive Brokers (IBKR)
  - URL : ibkr.com → "Open Account"
  - Type de compte : Individual / Margin Account
  - Activer les permissions Futures lors de l'ouverture
- [ ] Activer le compte Paper Trading (simulation)
  - Dans TWS : File → Paper Trading Account
- [ ] Télécharger et installer TWS Gateway (la version légère sans interface graphique)
- [ ] Tester la connexion API manuellement (TWS Gateway doit tourner en arrière-plan)

### 1.2 Environnement de développement
- [ ] Installer Python 3.11+
- [ ] Créer un environnement virtuel dédié :
  ```bash
  python -m venv future-invest-env
  source future-invest-env/bin/activate
  ```
- [ ] Installer les dépendances de base :
  ```bash
  pip install ib_insync anthropic fastapi streamlit redis pandas httpx pdfplumber
  ```
- [ ] Installer Docker Desktop (pour Redis et TimescaleDB)
- [ ] Cloner ou initialiser le dépôt Git du projet

### 1.3 Clés API
- [ ] Créer une clé API Anthropic (claude.ai → API)
- [ ] Créer une clé NewsAPI (newsapi.org — plan gratuit 1000 req/jour)
- [ ] Créer un fichier `.env` (ne jamais committer dans Git) :
  ```
  IBKR_HOST=127.0.0.1
  IBKR_PORT=7497
  ANTHROPIC_API_KEY=...
  NEWS_API_KEY=...
  MAX_DAILY_LOSS_USD=___
  MAX_DRAWDOWN_PCT=___
  TELEGRAM_BOT_TOKEN=...
  TELEGRAM_CHAT_ID=...
  ```
- [ ] Créer un bot Telegram (via @BotFather) et noter le token

---

## PHASE 2 — Validation rétrospective (avant tout paper trading)

### 2.1 Bibliothèque d'événements historiques
- [ ] Documenter 10 événements passés dans `research/events/` :
  - [ ] 2010 — Embargo export blé Russie
  - [ ] 2012 — Sécheresse maïs USA
  - [ ] 2020 — Pétrole négatif (COVID)
  - [ ] 2021 — Blocage canal de Suez
  - [ ] 2022 — Guerre Ukraine (blé, engrais)
  - [ ] 2023 — Ban export riz Inde
  - [ ] + 4 événements au choix selon les marchés retenus
- [ ] Pour chaque événement : chaîne causale + prix historiques + résultat réel

### 2.2 Test de l'Event Analyzer sur rétrospectifs
- [ ] Faire tourner l'Event Analyzer sur les 10 événements passés
- [ ] Comparer les chaînes causales générées vs ce qui s'est réellement passé
- [ ] Scorer chaque analyse (juste / partiellement juste / faux)
- [ ] Ajuster les prompts sur les erreurs récurrentes
- [ ] Score cible avant de passer à la suite : ≥ 7/10 analyses correctes

### 2.3 Backtesting des règles de risque
- [ ] Récupérer les données historiques des instruments cibles (5 ans minimum)
- [ ] Simuler les règles de risque sur données historiques
- [ ] Vérifier que le circuit-breaker aurait fonctionné lors des crises passées
- [ ] Finaliser `MAX_DAILY_LOSS`, `MAX_DRAWDOWN_PCT`, `ATR_SPIKE_FACTOR`

---

## PHASE 3 — Paper Trading (argent fictif, système live)

### 3.1 Déploiement initial
- [ ] Déployer le Risk Supervisor en premier (avant tout exécution)
- [ ] Tester le circuit-breaker manuellement (simuler un breach)
- [ ] Vérifier que l'alerte Telegram arrive bien sur le téléphone
- [ ] Déployer l'Event Analyzer connecté au Decision Layer
- [ ] Premier run complet en paper trading : 1 event → analyse → décision → exécution simulée

### 3.2 Période de rodage (minimum 4 semaines)
- [ ] Tracker chaque trade dans `logs/`
- [ ] Analyser les résultats chaque semaine avec [[Bruno]]
- [ ] Identifier les faux positifs du circuit-breaker
- [ ] Ajuster les paramètres si nécessaire
- [ ] Performance minimale requise avant passage en live :
  - Pas de runaway algorithm
  - Circuit-breaker déclenché ET humain notifié correctement sur au moins 2 événements
  - P&L paper trading positif ou légèrement négatif (acceptable en phase test)

---

## PHASE 4 — Go Live (capital réel)

- [ ] Validation formelle de [[Bruno]] sur le profil de risque final
- [ ] Passer le compte IBKR de Paper à Live
- [ ] Démarrer avec un capital réduit (20-30% du capital total prévu)
- [ ] Augmenter progressivement après 4 semaines de live stable
- [ ] Mettre en place un reporting hebdomadaire dans `logs/`

---

## Documents de référence

| Document | Emplacement |
|----------|------------|
| Profil investisseur | `strategy/2026-06-04_bruno_profil-investisseur.md` |
| Architecture système | `architecture/2026-06-04_event-analyzer-architecture.md` |
| Prompt recherche DIY | `research/2026-06-04_prompt-recherche-diy.md` |
| Résultats recherche DIY | `research/2026-06-04_resultats-recherche-diy.md` *(à créer)* |

## Voir aussi

- [[INDEX|Future Invest — Index projet]]
- [[Bruno]] — profil investisseur, validation risque
- [[Forge]] — architecture technique, déploiement
- [[Dobby]] — orchestrateur
