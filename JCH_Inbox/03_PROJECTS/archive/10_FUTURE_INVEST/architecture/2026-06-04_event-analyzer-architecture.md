---
project: Future Invest
module: Event Analyzer
author: "[[Forge]]"
reviewed_by: "[[Bruno]]"
created: 2026-06-04
status: draft v1
---

# Event Analyzer — Architecture du Module

## Rôle dans le système global

L'Event Analyzer est le **module d'intelligence amont** du système Future Invest.
Il se déclenche avant toute décision de trading : il transforme un événement réel
(économique, géopolitique, climatique) en une analyse multi-couches et en opinions
de positionnement structurées.

```
┌─────────────────────────────────────────────────────────────────┐
│                      FUTURE INVEST SYSTEM                       │
│                                                                  │
│  [EVENT ANALYZER] → [DECISION LAYER] → [EXECUTION] → [RISK]    │
│       ↑                    ↑                                    │
│  JCH saisit        JCH valide ou                                │
│  l'événement       rejette la thèse                             │
└─────────────────────────────────────────────────────────────────┘
```

---

## Architecture interne — Vue d'ensemble

```
ENTRÉE : Événement textuel (ex. "Mauvaise récolte de riz en Inde")
    │
    ▼
┌──────────────────┐
│ EVENT DECOMPOSER │  LLM — découpe l'événement en dimensions d'analyse
│   (Agent #0)     │  Output : liste structurée de questions à investiguer
└────────┬─────────┘
         │
    ┌────┴──────────────────────────────────────────┐
    │  COLLECTEURS PARALLÈLES (Agents #1 à #5)      │
    │                                               │
    │  #1 Agent Agricole      → FAO, USDA, Sentinel │
    │  #2 Agent Géopolitique  → GDELT, NewsAPI      │
    │  #3 Agent Flux Commerce → UN Comtrade         │
    │  #4 Agent Marchés       → Prix futures, ETF   │
    │  #5 Agent Macro         → Inflation, devises  │
    └────────────────────────┬──────────────────────┘
                             │
                    ┌────────▼────────┐
                    │   SYNTHESIZER   │  LLM — chaîne causale complète
                    │   (Agent #6)    │  Input : tous les rapports des agents
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ OPINION ENGINE  │  LLM — formule les opinions
                    │   (Agent #7)    │  de positionnement (pas des conseils)
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ RAPPORT FINAL   │  HTML ou Markdown structuré
                    │  + Dashboard    │  envoyé à JCH pour validation
                    └─────────────────┘
```

---

## Détail de chaque agent

### Agent #0 — Event Decomposer

**Rôle :** Prendre l'événement brut et le découper en questions précises
à investiguer pour chaque dimension.

**Prompt type :**
```
Tu es un analyste macro senior. L'événement suivant vient de se produire :
"{EVENT}"

Décompose cet événement en 5 dimensions d'analyse :
1. Impact agricole / sectoriel direct
2. Impact géopolitique et relations internationales
3. Impact sur les flux commerciaux mondiaux
4. Impact sur les marchés financiers (commodités, devises, indices)
5. Impact macro-économique (inflation, banques centrales, taux)

Pour chaque dimension, liste 3 questions précises à investiguer.
Format : JSON structuré.
```

**Output exemple (récolte riz Inde) :**
```json
{
  "agricole": [
    "Quel est le déficit de production estimé en tonnes ?",
    "Quelles sont les réserves stratégiques actuelles de l'Inde ?",
    "Quel pays peut substituer les exports indiens ?"
  ],
  "geopolitique": [
    "L'Inde a-t-elle annoncé des restrictions d'export ?",
    "Quels pays africains dépendent le plus des exports indiens ?",
    "Y a-t-il des tensions diplomatiques avec les pays fournisseurs alternatifs ?"
  ],
  ...
}
```

---

### Agent #1 — Agricole

**Sources interrogées :**

| Source | Ce qu'on y lit | Accès |
|--------|---------------|-------|
| FAO FAOSTAT | Statistiques mondiales production/export par pays | API gratuite |
| USDA WASDE | Rapport mensuel offre/demande mondiale (grain, oléagineux) | PDF gratuit (parsing) |
| Sentinel Hub (ESA) | Images satellites des zones de culture | Freemium |
| NOAA Climate | Données météo et prévisions saisonnières | API gratuite |

**Output :** rapport chiffré sur l'ampleur du choc d'offre.

---

### Agent #2 — Géopolitique

**Sources interrogées :**

| Source | Ce qu'on y lit | Accès |
|--------|---------------|-------|
| GDELT Project | Base mondiale d'événements géopolitiques en temps réel | API gratuite |
| NewsAPI | Presse mondiale (Reuters, AP, AFP, presse locale) | Freemium (1000 req/jour gratuit) |
| ACLED | Données conflits et instabilité par région | Gratuit pour usage non-[[commercial]] |

**Output :** carte des risques géopolitiques liés à l'événement.

---

### Agent #3 — Flux Commerciaux

**Sources interrogées :**

| Source | Ce qu'on y lit | Accès |
|--------|---------------|-------|
| UN Comtrade | Import/export par pays et par produit (HS code) | Gratuit (limité) / ~600$/an |
| World Bank DataBank | Données macro commerce international | API gratuite |
| Baltic Exchange (proxy) | Indices de fret maritime | Via Yahoo Finance ou Investing |

**Output :** carte des flux commerciaux impactés + pays gagnants/perdants.

---

### Agent #4 — Marchés Financiers

**Sources interrogées :**

| Source | Ce qu'on y lit | Accès |
|--------|---------------|-------|
| Yahoo Finance API | Prix historiques et actuels (futures, ETF, actions) | Gratuit |
| Investing.com | Prix commodités, futures agricoles | Scraping / API payante |
| CBOE | Données volatilité (VIX et équivalents) | Gratuit |
| CME Group | Données officielles [[contrats]] futures | Gratuit (différé 10min) |

**Output :** liste des instruments financiers directement et indirectement impactés.

---

### Agent #5 — Macro-économique

**Sources interrogées :**

| Source | Ce qu'on y lit | Accès |
|--------|---------------|-------|
| FRED (Federal Reserve) | Données macro US (inflation, taux, emploi) | API gratuite |
| World Bank DataBank | PIB, inflation, balance commerciale par pays | API gratuite |
| BIS (Banque des Règlements Internationaux) | Flux de capitaux, données bancaires | Gratuit |
| Banque Centrale Européenne | Données zone euro | API gratuite |

**Output :** analyse des pressions macro et des réponses probables des banques centrales.

---

### Agent #6 — Synthesizer

**Rôle :** Prend les 5 rapports des agents collecteurs et construit
la **chaîne causale complète** avec les liens de causalité entre chaque niveau.

**Prompt type :**
```
Tu es un stratégiste macro senior. Voici les analyses de 5 dimensions
d'un même événement : {REPORTS_JSON}

Construis une chaîne causale complète en 4 niveaux :
- Niveau 1 (impact direct) : dans les 24-72h
- Niveau 2 (impact secondaire) : dans les 1-4 semaines
- Niveau 3 (impact tertiaire) : dans les 1-6 mois
- Niveau 4 (impact structurel) : au-delà de 6 mois

Pour chaque niveau, indique la probabilité d'occurrence (haute/moyenne/faible)
et les facteurs qui pourraient invalider le scénario.
```

---

### Agent #7 — Opinion Engine

**Rôle :** Formule des **opinions de positionnement** (pas des conseils financiers)
basées sur la chaîne causale. Chaque opinion est accompagnée de :
- La logique causale qui la sous-tend
- Les conditions d'invalidation
- Un niveau de conviction (fort/modéré/faible)
- L'horizon temporel estimé

**Format de sortie :**
```json
{
  "opinions": [
    {
      "instrument": "Futures Blé Chicago (ZW)",
      "direction": "haussier",
      "horizon": "1-4 semaines",
      "logique": "Substitution riz→blé en Asie du Sud-Est",
      "conviction": "modérée",
      "invalidation": "Bonne récolte blé annoncée en Australie ou Ukraine"
    }
  ]
}
```

---

## Stack technique

```
Python 3.11+
├── anthropic          SDK Claude (LLM orchestration)
├── httpx              Appels API asynchrones
├── asyncio            Parallélisation des agents collecteurs
├── pandas             Traitement des données structurées
├── beautifulsoup4     Parsing HTML (USDA PDF → données)
├── pdfplumber         Extraction données depuis PDF (rapports USDA/FAO)
├── fastapi            API REST interne
├── streamlit          Dashboard de présentation du rapport
└── redis              Cache des résultats (évite de re-fetcher les mêmes sources)
```

---

## Structure des fichiers du module

```
event_analyzer/
├── main.py                    Point d'entrée — reçoit l'événement
├── decomposer.py              Agent #0 — découpe l'événement
├── collectors/
│   ├── agricultural.py        Agent #1
│   ├── geopolitical.py        Agent #2
│   ├── trade_flows.py         Agent #3
│   ├── markets.py             Agent #4
│   └── macro.py               Agent #5
├── synthesizer.py             Agent #6
├── opinion_engine.py          Agent #7
├── report_generator.py        HTML/Markdown output
├── data_sources/
│   ├── fao_client.py          Wrapper API FAO
│   ├── gdelt_client.py        Wrapper API GDELT
│   ├── comtrade_client.py     Wrapper API UN Comtrade
│   └── yfinance_client.py     Wrapper Yahoo Finance
├── config.py                  Variables d'environnement et limites API
└── dashboard.py               Interface Streamlit
```

---

## Flux d'exécution — Code schématique

```python
async def analyze_event(event: str) -> AnalysisReport:
    # Étape 1 — Décomposition
    questions = await decomposer.decompose(event)

    # Étape 2 — Collecte parallèle (tous les agents tournent en même temps)
    results = await asyncio.gather(
        agricultural_agent.collect(questions["agricole"]),
        geopolitical_agent.collect(questions["geopolitique"]),
        trade_agent.collect(questions["commerce"]),
        markets_agent.collect(questions["marches"]),
        macro_agent.collect(questions["macro"]),
    )

    # Étape 3 — Synthèse causale
    causal_chain = await synthesizer.synthesize(event, results)

    # Étape 4 — Opinions de positionnement
    opinions = await opinion_engine.generate(causal_chain)

    # Étape 5 — Rapport final
    report = report_generator.build(event, causal_chain, opinions)

    return report
```

---

## Intégration avec le Decision Layer

Une fois le rapport généré, il est présenté à JCH via le Dashboard Streamlit.
JCH peut alors :
1. **Valider la thèse** → les instruments identifiés alimentent le Decision Layer
2. **Rejeter ou modifier** → ajuster les paramètres avant de passer en exécution
3. **Archiver** → sauvegarder l'analyse dans `research/` pour référence future

```
Event Analyzer Report
        ↓
[VALIDER] [MODIFIER] [ARCHIVER]
        ↓ (si validé)
Decision Layer (co-création humain/IA)
        ↓
Execution Layer (automatique)
```

---

## Limites et garde-fous

| Limite | Explication |
|--------|-------------|
| **Pas de conseils financiers** | Le système formule des opinions basées sur la logique causale — la décision finale appartient toujours à JCH |
| **Données en différé** | Les sources gratuites ont souvent 10-15min de délai — ne pas utiliser pour du scalping (trading ultra-rapide) |
| **Biais de confirmation** | Le LLM peut surestimer la certitude — chaque opinion inclut obligatoirement ses facteurs d'invalidation |
| **Événements corrélés** | Deux événements simultanés peuvent se contredire — le Synthesizer doit gérer les conflits entre agents |

---

## Voir aussi

- [[INDEX|Future Invest — Index projet]]
- [[2026-06-04_bruno_profil-investisseur|Profil investisseur — questionnaire Bruno]]
- [[Forge]] — architecte technique
- [[Bruno]] — validation des opinions de positionnement
- [[Dobby]] — orchestrateur
