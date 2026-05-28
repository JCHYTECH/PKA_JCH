# WildNexus — Rapport d'exécution : Série / Parallèle

**Date :** 2026-05-25
**Périmètre :** WP02 → M-02 → M-03
**Owner :** [[Dobby]]
**Contexte :** M-01 (architecture gelée) est atteint. WP02 (procurement) est en cours.

---

## État des lieux

| Jalon | Statut |
|-------|--------|
| M-01 — Architecture P0 gelée | ✅ Tous les ADR acceptés (sauf ADR-006 boîtier, proposé) |
| WP02 — Shortlist achat | ✅ Produite (Option A ~425€ + Option B ~200€, total ~760€/1000€) |
| WP02 — Encombrement | ✅ v0.2 produit (Hammond 1554CAGY recommandé) |
| M-02 — Prototype banc | 🔴 Bloqué — attend PPK2 + composants |

**Blocages critiques :**
- PPK2 non commandé → bloque toutes les mesures énergie → bloque M-02
- Arducam non contacté → bloque confirmation caméra → bloque commande
- Panier Mouser non groupé → bloque montage banc

---

## Chaînes SÉRIE (dépendances strictes)

### Chaîne 1 — Énergie → Boîtier → Proto terrain

```
Commande PPK2  →  M-02 mesures énergie  →  ADR-006 boîtier  →  WP03 proto terrain
    ⬆️                    (4AA vs 8AA,             (choix batterie         (assemblage final)
  BLOQUANT              3 scénarios)              + boîtier final)
```

- **PPK2** : priorité absolue, ~100€, Mouser ou Nordic Semi shop
- **M-02** : démarre dès réception PPK2. Durée estimée : 2-3 jours de mesures
- **ADR-006** : déjà proposé (Hammond 1554CAGY), fermeture après M-02
- **WP03** : assemblage proto → après réception de tous les composants

### Chaîne 2 — Caméra

```
Contacter Arducam  →  Confirmation OV5640 DVP M12  →  Commande caméra  →  Banc M-02
```

- Email Arducam : confirmer pinout, NoIR ou IR-cut, monture M12
- Bloquant pour la commande — ne pas acheter sans fiche technique

### Chaîne 3 — Composants Mouser

```
Grouper panier  →  Commande groupée  →  Réception  →  Montage banc M-02
```

- Panier : A01, A03–A12, B03, B05–B06
- Économies de port significatives en groupant

---

## Actions PARALLÈLE (indépendantes, démarrables maintenant)

### 🔵 Priorité haute

| Action | Owner | Bloquant ? | Effort |
|--------|-------|------------|--------|
| **Commander PPK2** | JCH / [[Dobby]] | Oui — bloque Chaîne 1 | 5 min |
| **Contacter Arducam** (email) | [[Dobby]] / [[Forge]] | Oui — bloque Chaîne 2 | 15 min |
| **Grouper panier Mouser** | [[Forge]] | Oui — bloque Chaîne 3 | 30 min |
| **Demander devis Lensation** (2× M12 f/1.8 IR) | [[Dobby]] / [[Forge]] | Non | 10 min |

### 🟡 Priorité medium — zero impact P0, avance utile

| Action | Owner | Livrable | Pourquoi maintenant |
|--------|-------|----------|---------------------|
| **FTO / Licence** | [[Renard]] + [[Hermine]] | Note juridique v0.2 | Bloque publication future, pas le proto — mais prend du temps |
| **Stratégie tests firmware** (T03.6) | [[Forge]] + [[Castor]] | Plan de test nRF52840 | Peut se préparer sur DevKit sans attendre le proto |
| **Pipeline classifieur** (T04.5) | [[Nova]] + [[Clio]] | Framework évaluation | Préparer les scripts d'évaluation avant d'avoir les données |

### 🟢 Priorité basse — activités de fond

| Action | Owner | Livrable / Note |
|--------|-------|-----------------|
| **Supply register complet** | [[Forge]] | Documentaire, peut avancer en continu |
| **RGPD terrain** (signalétique) | [[Renard]] | Modèle pancarte + procédure floutage |
| **InsectNet — test validation** | [[Furet]] | Tester Raven + clustering HDBSCAN sur enregistrements existants |

---

## Ce qui peut partir EN MÊME TEMPS cette semaine

```
┌─────────────────────────────────────────────────────────┐
│               LUNDI — MARDI (parallelisable)             │
├─────────────────────────────────────────────────────────┤
│ □ Commander PPK2 (JCH)                                   │
│ □ Contacter Arducam (Dobby)                              │
│ □ Demander devis Lensation (Dobby)                       │
│ □ Grouper panier Mouser (Forge)                          │
│ □ Lancer FTO/Licence (Renard + Hermine)                  │
│ □ Préparer stratégie tests firmware (Forge + Castor)     │
├─────────────────────────────────────────────────────────┤
│                 MERCREDI — VENDREDI                       │
├─────────────────────────────────────────────────────────┤
│ → Réponse Arducam reçue → commande caméra                │
│ → Panier Mouser finalisé → commande groupée              │
│ → PPK2 expédié → préparer protocole mesures M-02         │
│ → Stratégie tests firmware v0.1 livrée                   │
│ → FTO v0.2 en relecture                                  │
├─────────────────────────────────────────────────────────┤
│             SEMAINE SUIVANTE (dès réception)              │
├─────────────────────────────────────────────────────────┤
│ → M-02 mesures énergie (2-3 jours)                       │
│ → ADR-006 fermé (choix batterie + boîtier final)          │
│ → WP02 encombrement v0.3                                 │
│ → WP03 assemblage proto banc                             │
└─────────────────────────────────────────────────────────┘
```

---

## Résumé exécutif

**3 chaînes série** dépendent d'actions que JCH peut débloquer en 5 minutes (commander PPK2).  
**6 actions parallèles** peuvent démarrer immédiatement sans attendre le hardware.  
**Coût total restant :** ~760€ sur 1000€ — réserve saine de ~240€.

Le chemin critique tient en une phrase : **PPK2 → M-02 → ADR-006 → proto**. Tout le reste peut avancer en parallèle.
