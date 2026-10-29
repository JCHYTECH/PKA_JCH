---
date: 2026-05-26
project: VETALYX
type: flowcharts
status: draft-v1
owner: [[Dobby]]
clinical_lead: [[Vasco]]
topic: Logigrammes protocole KOL et sous-protocole DBS
---

# VETALYX - Logigrammes validation clinique et DBS

## 1. Logigramme protocole clinique KOL

```mermaid
flowchart TD
    A[Animal chien/chat en consultation routine] --> B{Signes compatibles allergie ?}
    B -- Non --> C[Controle potentiel non allergique]
    B -- Oui --> D[Cas allergie suspectee]

    C --> E{Consentement proprietaire}
    D --> E
    E -- Refus --> F[Sortie et soin standard]
    E -- Accord --> G[Inclusion et ID etude pseudonymise]

    G --> H[Questionnaire clinique standardise]
    H --> I[Score clinique: prurit, lesions, otite, puce, traitements]
    I --> J[Exclusions minimales: parasites, infection, dermatophytose si suspectee]

    J --> K[Prelevement sang routine]
    K --> L[Test rapide VETALYX en clinique]
    K --> M[Serum/plasma pour test IgE de reference]
    K --> N[Sous-protocole DBS si consentement specifique]

    L --> O[Lecture test rapide et resultats par ligne]
    M --> P[ELISA / immunoblot / microarray reference]
    N --> Q[DBS conserve basse temperature]

    O --> R[Decision clinique initiale documentee]
    P --> S[Comparaison rapide vs reference]
    Q --> T[Comparaison DBS vs serum/plasma si laboratoire compatible]

    R --> U[Follow-up 4-8 semaines si possible]
    S --> V[Analyse concordance par famille allergenique]
    T --> W[Analyse faisabilite et stabilite DBS]
    U --> X[Rapport KOL final]
    V --> X
    W --> X
```

## 2. Logigramme sous-protocole DBS avec partenaire chinois

```mermaid
flowchart TD
    A[Animal inclus dans protocole KOL] --> B{Consentement DBS specifique ?}
    B -- Non --> C[Pas de DBS - serum/plasma uniquement]
    B -- Oui --> D[Prelevement sang veineux]

    D --> E[Serum/plasma reference]
    D --> F[Depot DBS volume controle]

    F --> G[Sechage horizontal 2-4 h temperature ambiante controlee]
    G --> H[Photo ou scan du spot + trace volume et heure]
    H --> I[Ensachage individuel: barriere + dessicant + indicateur humidite]
    I --> J[Stockage 2-8 C le jour meme]

    J --> K{Conservation >72 h ?}
    K -- Non --> L[Expedition sous froid vers laboratoire]
    K -- Oui --> M[Congelation -20 C par defaut]
    M --> N{Biobanque ou reanalyse future ?}
    N -- Oui --> O[-80 C si disponible]
    N -- Non --> L
    O --> L

    E --> P[Test IgE reference serum/plasma]
    L --> Q[Extraction DBS selon SOP partenaire chinois]

    Q --> R{Assay chinois compatible eluats DBS ?}
    R -- Non --> S[DBS non exploitable pour IgE - revoir extraction/assay]
    R -- Oui --> T[Test IgE sur eluats DBS]

    P --> U[Resultats serum/plasma]
    T --> V[Resultats DBS]
    U --> W[Analyse pairée serum/plasma vs DBS]
    V --> W

    W --> X[Concordance positif/negatif]
    W --> Y[Correlation semi-quantitative si applicable]
    W --> Z[Effet stockage, humidite, hematocrite, delai]

    X --> AA[Rapport technique DBS au partenaire chinois]
    Y --> AA
    Z --> AA
```

## 3. Logigramme decision go/no-go DBS

```mermaid
flowchart TD
    A[Fin sous-etude DBS] --> B{Taux echantillons exploitables >90% ?}
    B -- Non --> C[No-go DBS routine: ameliorer SOP prelevement/stockage]
    B -- Oui --> D{Assay partenaire chinois reproductible ?}

    D -- Non --> E[No-go analytique: revoir extraction, papier, volume, seuils]
    D -- Oui --> F{Concordance DBS vs serum/plasma >=80% par grandes familles ?}

    F -- Non --> G[Go limite recherche: DBS non utilisable comme matrice terrain]
    F -- Oui --> H{Faibles positifs correctement detectes ?}

    H -- Non --> I[Go prudent: DBS utilisable seulement classes fortes / screening]
    H -- Oui --> J{Stabilite basse temperature acceptable J0-J28 ?}

    J -- Non --> K[Go conditionnel: reduire delai, renforcer froid, tester -80 C]
    J -- Oui --> L{SOP executable par clinique sans ecarts majeurs ?}

    L -- Non --> M[Go technique mais non deployable: simplifier kit DBS]
    L -- Oui --> N[Go DBS terrain: matrice alternative candidate]

    N --> O[Etape suivante: validation multicentrique plus large]
    I --> O
    K --> O
```

## 4. Notes d'utilisation

- Ces logigrammes doivent etre presentes comme support de discussion avec les KOL et le partenaire chinois.
- Le DBS est volontairement isole du flux principal : il s'agit d'un **sous-protocole analytique**, pas d'une condition de succes du test rapide.
- Le serum/plasma reste la reference obligatoire tant que le pontage DBS n'est pas valide.
- Les seuils DBS ne doivent pas etre supposes identiques aux seuils serum/plasma.
