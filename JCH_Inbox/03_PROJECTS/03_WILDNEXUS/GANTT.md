# WildNexus P0 — Vue de dépendances

Version révisée : 2026-11-05. Projet gelé ; reprise post-van non datée. La vue détaillée et les critères sont dans `PLANNING_GANTT.md`.

Les anciennes barres Q1–Q3 2027 étaient des estimations devenues obsolètes. Elles sont retirées plutôt que remplacées par de nouvelles dates sans disponibilité confirmée.

```mermaid
flowchart LR
    GO[Signal de reprise JCH] --> R0[R0 Inventaire, factures, schémas et budget]
    R0 --> R1A[Banc caméra, PIR, SD et mesures]
    R0 --> MIC[Identifier micros et PIR]
    MIC --> R1B[Audio réel et pipelines]
    R1A --> R1B
    R1A --> R1C[Benchmark IA sur images réelles]
    BUY[Achat radio autorisé et reçu] --> R1D[Radio et gateway]
    R1A --> R2[Intégration et énergie]
    R1B --> R2
    R1C --> R2
    R1D --> R2
    POWER[SOP-10 revue et levée] --> R2
    R2 --> M2{M-02 démontré ?}
    M2 -->|oui| R3[Boîtier, ADR-018, RGPD et EVT]
    M2 -->|non| FIX[Correction ou arbitrage] --> R2
    R3 --> M3{EVT validé ?}
    M3 -->|oui| R4[Publication, DVT, conformité et industrialisation]
    M3 -->|non| FIX
```

Les 37/37 tests hôte historiques restent une preuve logicielle, pas une validation de ce chemin matériel. La projection budgétaire provisoire de 904 € dépasse le seuil interne de 900 € : aucune nouvelle commande sans réconciliation et autorisation.

Plane et le fichier JSON de seed sont des instantanés à revoir à la reprise. Ne pas rejouer les anciennes dates ni lancer de remplacement externe automatique depuis ce document.
