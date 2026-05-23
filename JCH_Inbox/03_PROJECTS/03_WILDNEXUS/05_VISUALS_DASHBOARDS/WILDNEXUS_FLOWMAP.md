# WildNexus — Logigramme multi-etages

**Version :** v0.1  
**Date :** 2026-05-18  
**Statut :** interne — premiere carte de navigation  
**Owner :** Dobby  
**Contributeurs :** Atlas, Forge, Vega  

## Objet

Ce document fournit une carte logique de WildNexus a plusieurs niveaux de detail. Il distingue explicitement :

- le projet complet WildNexus ;
- le perimetre P0 strict ;
- les extensions P1/P2 a preserver sans les faire entrer dans P0 ;
- les decisions ouvertes qui conditionnent `M-01 Architecture P0 gelee`.

Sources principales :

- [INDEX.md](../INDEX.md)
- [WildNexus_MASTER_ARCHITECTURE.md](../01_FOUNDATION/WildNexus_MASTER_ARCHITECTURE.md)
- [wildnexus-founding-document-v0.2.md](../01_FOUNDATION/wildnexus-founding-document-v0.2.md)
- [WILDNEXUS_P0_SCOPE_LOCK.md](../01_FOUNDATION/WILDNEXUS_P0_SCOPE_LOCK.md)
- [WILDNEXUS_CYCLE_01_M01_READINESS.md](../00_GOVERNANCE/WILDNEXUS_CYCLE_01_M01_READINESS.md)
- [WILDNEXUS_ADR_INDEX.md](../02_DECISIONS/WILDNEXUS_ADR_INDEX.md)
- [WILDNEXUS_AGENT_MAPPING.md](../00_GOVERNANCE/WILDNEXUS_AGENT_MAPPING.md)

---

## Niveau 0 — Carte executive

Lecture en 2 minutes : WildNexus n'est pas un piege photo ameliore, mais une infrastructure distribuee d'observation ecologique. Le P0 doit prouver le noeud camera autonome avant d'ajouter la complexite scientifique.

```mermaid
flowchart LR
    A[Vision WildNexus<br/>Observation ecologique distribuee] --> B[P0<br/>Noeud camera autonome]
    B --> C[Preuve terrain<br/>3 noeuds actifs 30 jours]
    C --> D[M-03 EVT valide<br/>autonomie extrapolee 60 jours]
    D --> E[P1<br/>Intelligence scientifique avancee]
    E --> F[P2<br/>Ecosysteme distribue]

    B -. preserve interface .-> G[Bioacoustique future]
    B -. preserve interface .-> H[Faune Autour / app terrain]
    B -. preserve interface .-> I[Exports scientifiques]
    B -. preserve interface .-> J[Cloud / API / communaute]
```

---

## Niveau 1 — Phases et frontieres de scope

Ce niveau sert de garde-fou contre le scope creep. Les elements P1/P2 sont importants, mais ne doivent pas bloquer le prototype camera P0.

```mermaid
flowchart TB
    subgraph P0[P0 — Noeud camera credible et deployable]
        P0A[Capture jour / nuit]
        P0B[Detection evenementielle]
        P0C[Filtre embarque animal / non-animal]
        P0D[LPWAN evenementiel]
        P0E[Stockage local]
        P0F[Configuration terrain simple]
        P0G[Autonomie 60 jours batterie seule]
        P0H[Boitier IP67]
        P0I[Documentation de reproduction]
    end

    subgraph P1[P1 — Intelligence scientifique avancee]
        P1A[Bioacoustique]
        P1B[Classification espece]
        P1C[Reconnaissance individuelle]
        P1D[Gateways locales]
        P1E[Exports Camtrap-DP / GBIF]
    end

    subgraph P2[P2 — Ecosysteme distribue]
        P2A[API publique]
        P2B[SDK / plugins]
        P2C[Reseau collaboratif]
        P2D[Cloud scientifique]
        P2E[Orchestration multi-sites]
    end

    P0 --> P1 --> P2
    P1 -. hors P0 .-> S1[Ne pas bloquer M-01 / M-02 / M-03]
    P2 -. hors P0 .-> S1
```

---

## Niveau 2 — Flux operationnel P0

Ce flux decrit le comportement attendu du noeud camera P0, depuis la veille energetique jusqu'a la recuperation des donnees.

```mermaid
flowchart LR
    A[Veille ultra basse consommation] --> B{Evenement detecte ?}
    B -- non --> A
    B -- oui --> C[Reveil sous-systemes]
    C --> D[Capture image / sequence courte]
    D --> E[Filtre embarque animal / non-animal]
    E --> F{Animal probable ?}
    F -- non --> G[Log minimal<br/>pas de transmission]
    G --> A
    F -- oui --> H[Stockage local complet]
    H --> I[Creation metadonnees evenement]
    I --> J[Transmission LPWAN evenementielle]
    J --> K[Etat batterie / sante noeud]
    K --> A

    H -. recuperation terrain .-> L[Wi-Fi / BLE / carte locale]
    I -. schema extensible .-> M[Future acoustique / environnement / export scientifique]
```

---

## Niveau 3 — Architecture technique P0

Ce niveau separe les blocs qui devront faire l'objet d'ADR ou de specifications courtes avant `M-01`.

```mermaid
flowchart TB
    subgraph NODE[Noeud camera P0]
        MCU[MCU ultra low power<br/>ADR-001]
        CAM[Camera + IR<br/>ADR-002]
        RF[Radio LPWAN<br/>ADR-003]
        STORE[Stockage local<br/>ADR-004]
        ENERGY[Energie / batterie / solaire optionnel<br/>ADR-005]
        ENC[Boitier IP67 / montage<br/>ADR-006]
        AI[Detection evenementielle + AI binaire<br/>ADR-007]
        EXT[Interface capteurs extensible<br/>ADR-008]
    end

    MCU --> CAM
    MCU --> RF
    MCU --> STORE
    MCU --> AI
    ENERGY --> MCU
    ENERGY --> CAM
    ENERGY --> RF
    ENC --> CAM
    ENC --> ENERGY
    EXT -. preserve P1/P2 .-> MCU

    subgraph FIELD[Terrain EVT]
        SITE[Site belge]
        NODES[3 noeuds actifs]
        LOGS[Logs autonomie / radio / image]
        REVIEW[Inspection J+30]
    end

    NODE --> FIELD
```

---

## Niveau 4 — Chemin de decision vers M-01

`M-01` est pret quand les decisions structurantes sont suffisamment documentees pour autoriser le prototype banc.

```mermaid
flowchart TD
    A[Cycle 01 lance] --> B[T01.2 Licence / FTO]
    A --> C[T01.3 Radio / LPWAN]
    A --> D[T01.4 Camera / IR]
    A --> E[T01.5 MCU]
    A --> F[T01.6 Budget P0]
    A --> G[SUPPLY-01 Composants critiques]
    A --> H[RGPD terrain EVT]

    B --> I{Blocage prototypage interne ?}
    C --> J{Standard radio retenu ?}
    D --> K{Camera candidate choisie ?}
    E --> L{MCU candidat choisi ?}
    F --> M{Enveloppe P0 confirmee ?}
    G --> N{Alternatives supply listees ?}
    H --> O{Owner + livrable concret ?}

    I -- non --> READY[M-01 ready]
    J -- oui --> READY
    K -- oui --> READY
    L -- oui --> READY
    M -- oui --> READY
    N -- oui --> READY
    O -- oui --> READY

    READY --> P[M-01 Architecture P0 gelee]
    P --> Q[M-02 Prototype banc fonctionnel]
    Q --> R[M-03 EVT terrain valide]
    R --> S[M-04 Socle publie / communaute amorcee]
```

---

## Niveau 5 — Gouvernance et routage

Ce niveau clarifie qui pilote quoi. Les agents WildNexus produisent l'expertise domaine ; les specialistes PKA portent la qualite du livrable, la memoire et l'escalade.

```mermaid
flowchart TB
    JCH[JCH<br/>validation scope, cout, juridique, risques] --> DOB[Dobby<br/>orchestration]

    DOB --> SYS[wildnexus-program-manager-system-architect<br/>Dobby]
    DOB --> DOC[wildnexus-research-development-project-writer<br/>Atlas]
    DOB --> SCI[wildnexus-scientific-advisor<br/>Furet + Clio]
    DOB --> CAM[wildnexus-camera-imaging<br/>Nova + Lynx]
    DOB --> FW[wildnexus-firmware-ulp<br/>Castor + Forge]
    DOB --> HW[wildnexus-hardware-physical<br/>Chouette + Castor]
    DOB --> RF[wildnexus-rf-propagation<br/>Forge + Chouette]
    DOB --> AI[wildnexus-edge-ai-cv<br/>Nova + Clio]
    DOB --> BIO[wildnexus-bioacoustics-dsp<br/>Clio + Chouette]
    DOB --> IND[wildnexus-industrialisation<br/>Bruno + Forge]
    DOB --> IP[Licence / FTO / usage policy<br/>Renard + Hermine]
    DOB --> COM[Communication communaute<br/>Miel + Trace]
```

---

## Lecture recommandee

1. Lire le **niveau 0** pour expliquer le projet.
2. Lire le **niveau 1** pour ne pas melanger P0, P1 et P2.
3. Lire le **niveau 2** pour comprendre ce que le noeud fait sur le terrain.
4. Lire le **niveau 3** avant de produire les ADR.
5. Lire le **niveau 4** pour piloter `M-01`.
6. Lire le **niveau 5** pour router les travaux sans recreer une seconde equipe.

## Prochaine iteration proposee

La version v0.2 devrait ajouter :

- un logigramme detaille par ADR ;
- un flux donnees minimum P0 avec les 12 champs du document fondateur ;
- une carte des risques activee par jalon ;
- une vue "presentation externe" plus simple, sans details internes PKA.
