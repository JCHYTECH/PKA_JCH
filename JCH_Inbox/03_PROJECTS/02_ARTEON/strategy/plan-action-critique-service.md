---
date: 2026-05-02
tags: [plan, arteon, critique-service, roadmap, strategie]
type: project-plan
status: actif
kpi: €1000/mois CA service critique wildlife
---

# Plan d'action complet — Service Critique ARTEON + Site V1

> KPI unique : **€1 000/mois de chiffre d'affaires** sur le service de critique photo wildlife.  
> Orchestré par Dobby — équipe complète mobilisée.

---

## 1. La math du KPI

> **✓ DÉCIDÉ — 2026-05-02 : €1,90 TTC**  
> Sous la barre des €2 → achat impulsif, pas de délibération. TVA BE 21% incluse.

**Structure tarifaire :**

| Offre | Prix TTC | Prix HT | Marge nette |
|-------|----------|---------|-------------|
| 1ère analyse (inscription) | **Gratuite** | — | -€0,20 (acquisition) |
| Pack Découverte 2 analyses | **€0,99** | €0,82 | +€0,42 |
| Analyse standard | **€1,90** | €1,57 | **€1,37** |
| Pack 5 analyses | **€7,50** | €6,20 | €5,20 |
| Pack 10 analyses | **€13,90** | €11,49 | €9,49 |

**Mix cible réaliste (€1,90 + B2B) :**
- 421 analyses individuelles × €1,57 HT = **€661**
- 2 clubs photo × forfait €200/mois = **€400**
- **Total : €1 061/mois CA HT**

| Scénario | Analyses/mois | Analyses/jour | Faisabilité |
|----------|---------------|---------------|-------------|
| 100% individuel | 637 | 21 | Ambitieux |
| 421 individuel + 1 club | 421 | 14 | Réaliste mois 3 |
| **280 individuel + 2 clubs** | **280** | **9** | **Cible confortable** |

---

## 2. Personas — Qui achète

### Persona A — Thomas "L'Aspirant" (cœur de cible)
- **Profil** : 38-50 ans, ingénieur ou cadre, Belgique/France/Suisse
- **Équipement** : Canon R5 ou Nikon Z8 + 400-600mm, investissement 5 000-10 000€
- **Comportement** : Suit BBC Wildlife PotY, participe aux concours régionaux, frustré de plafonner
- **Problème** : Ses photos stagnent à 70/100 niveau jury — il ne sait pas pourquoi
- **Lecteur** : WILDLENS depuis le début
- **WTP** : €2,90/analyse, 3-4 analyses/mois = **~€10/mois**
- **Conversion** : Article WILDLENS technique → landing page → 1 analyse gratuite → abonné

### Persona B — Marie-Claire "La Contemplative"
- **Profil** : 52-65 ans, retraitée ou mi-temps, Belgique rurale
- **Équipement** : Sony A7IV + 200-600mm, mammifères et oiseaux de jardin
- **Comportement** : Cherche un regard expert structuré, pas des likes
- **WTP** : €2,90/analyse, 2 analyses/mois
- **Conversion** : Bouche-à-oreille club photo → recommandation directe

### Persona C — Club Photo Nature (B2B — Volume)
- **Profil** : Association 20-50 membres, réunion mensuelle, concours internes
- **Besoin** : Outil commun de notation pour leurs soirées de critique, formation des membres
- **Valeur** : Score partagé + rapport imprimable pour chaque participant
- **WTP** : €150-250/mois — accès illimité membres
- **Conversion** : Approche directe via Miel/Delphi sur les fédérations photo (LPO, Natagora, clubs régionaux)

### Persona D — Éditeur / Site Web Éthique (B2B — Certification)
- **Profil** : Magazine nature en ligne, galerie wildlife, concours photo, plateforme communautaire naturaliste
- **Besoin** : Garantir que les photos publiées respectent les standards éthiques ARTEON — pas d'appâtage, pas d'IA, pas de trucage
- **Valeur** : Badge **"Vérifié L'Instant Lu"** affiché sur les photos publiées — signal de confiance pour leur audience
- **WTP** : €100-400/mois selon volume — ils paient pour la crédibilité, pas le volume
- **Offre** : Licence mensuelle incluant X analyses + accès API + badge certifié
- **Conversion** : Approche ciblée — 10 plateformes identifiées par Iris + Delphi, pitch sur l'éthique comme différenciation éditoriale

### Funnel de conversion cible

```
WILDLENS lecteurs (~500) → Landing page → 1 analyse gratuite → Payant
        10% CTR               30% essai            40% conversion
= 50 visiteurs/mois   → 15 essais → 6 nouveaux clients/mois
```

---

## 3. Décision stratégique clé

> **Ne pas attendre ARTEON V1 pour lancer le service critique.**

Le service lance sur **`critique.arteon.be`** (landing page autonome) dès que le backend est prêt.  
ARTEON V1 continue en parallèle et intègre le service à son lancement.

Avantages :
- Revenus 8-10 semaines plus tôt
- Données réelles avant V1
- Preuve de concept pour les investisseurs/partenaires
- Finance partiellement la construction ARTEON V1

---

## 4. Les deux workstreams parallèles

```
WORKSTREAM 1 — SERVICE CRITIQUE (critique.arteon.be)
    Objectif : €1 000/mois
    Délai cible : J+49 lancement → J+90 KPI atteint

WORKSTREAM 2 — ARTEON SITE V1 (arteon.be complet)
    Objectif : Site complet avec service intégré
    Délai cible : J+90 à J+120
```

---

## 5. Plan détaillé — Toutes les tâches

### PHASE 0 — Validation interne sur photos JCH (J0–J7)

> Aucune photo tierce — zéro RGPD. JCH valide la qualité avant d'exposer le service.

| # | Tâche | Owner | Durée | Bloque |
|---|-------|-------|-------|--------|
| 0.1 | Sélectionner 50 photos JCH variées (oiseaux, mammifères, rapaces, eau, lumières difficiles) | JCH + Lynx | 2j | 0.2 |
| 0.2 | Passer les 50 photos dans le pipeline Argus local (plugin LR) | Argus | 3j | 0.3 |
| 0.3 | JCH évalue chaque rapport : pertinence critique, qualité preset XMP, cohérence scores | JCH | 2j | Calibration prompt |
| 0.4 | Calibration prompt selon retours JCH | Argus | 2j | Backend |
| 0.5 | ✅ Critères éthiques définis — filtre `filter_ethics.py` à coder | Forge | parallèle | Backend |

> **Go/No-Go phase 0** : JCH satisfait de la qualité sur ses propres photos → on passe à la suite.

---

### SEMAINE 1 — Décisions & fondations (J0–J7)

| # | Tâche | Owner | Série/Parallèle | Durée | Bloque |
|---|-------|-------|-----------------|-------|--------|
| 1.1 | ✅ **Nom choisi : `L'Instant Lu`** — 2026-05-02 | JCH | - | ✓ | Débloqué |
| 1.2 | ✅ **Critères éthiques définis** — voir §12 | Argus + JCH | - | ✓ | Débloqué |
| 1.3 | Lancer la charte graphique ARTEON (étape 4) | Vega | Parallèle | 5j | Landing page |
| 1.4 | ✅ **Prix : €1,90 TTC** + gratuit inscription + pack découverte | Bruno + JCH | - | ✓ | Débloqué |
| 1.5 | Setup `l-instant-lu.arteon.be` (DNS, certificat SSL) | Forge | Parallèle | 1j | Backend |

> **Point de synchronisation S1** : Phase 0 terminée + charte lancée → go backend.

---

### SEMAINE 2-3 — Backend technique (J7–J21)

| # | Tâche | Owner | Série/Parallèle | Durée | Dépend de |
|---|-------|-------|-----------------|-------|-----------|
| 2.1 | API FastAPI — endpoint `POST /analyse` | Forge | Série | 3j | 1.6 |
| 2.2 | Upload endpoint + stockage Cloudflare R2 | Forge | Série après 2.1 | 2j | 2.1 |
| 2.3 | Worker async — pipeline Python → Claude → PDF + XMP | Forge | Série après 2.2 | 3j | 2.2 |
| 2.4 | Calibration du prompt selon résultats test 50 photos | Argus | Parallèle 2.1 | 3j | 1.4 |
| 2.5 | Stripping EXIF GPS à l'upload (RGPD) | Forge | Parallèle 2.2 | 1j | 2.2 |
| 2.6 | CGU/CGV service critique (rédaction) | Renard | Parallèle | 4j | 1.2 |
| 2.7 | Politique RGPD mise à jour arteon.be | Renard | Parallèle 2.6 | 2j | - |
| 2.8 | Templates fiche artiste ARTEON (étape 5) | Vega | Parallèle | 3j | 1.3 |
| 2.9 | Template fiche produit ARTEON (étape 6) | Vega | Parallèle 2.8 | 2j | 2.8 |

---

### SEMAINE 3-4 — Paiement & delivery (J14–J28)

| # | Tâche | Owner | Série/Parallèle | Durée | Dépend de |
|---|-------|-------|-----------------|-------|-----------|
| 3.1 | Intégration Stripe (paiement à l'unité + packs) | Forge | Série après 2.3 | 3j | 2.3 |
| 3.2 | Système de crédits utilisateur (base users) | Forge | Série après 3.1 | 2j | 3.1 |
| 3.3 | Email transactionnel — livraison PDF + XMP | Forge | Parallèle 3.1 | 2j | 2.3 |
| 3.4 | Page de résultat web (lien download sécurisé 7j) | Forge | Parallèle 3.3 | 2j | 3.3 |
| 3.5 | Landing page `critique.arteon.be` (design + copy) | Vega | Série après charte | 4j | 1.3 |
| 3.6 | Documentation "Comment lire votre rapport Argus" | Argus | Parallèle | 2j | 2.4 |
| 3.7 | Setup Shopify ARTEON (étape 8) | Forge | Parallèle | 3j | 2.8 |
| 3.8 | Formulaire affiliation ARTEON (étape 7) | Vega | Parallèle 3.5 | 2j | 2.9 |

---

### SEMAINE 5 — Tests & légal (J28–J35)

| # | Tâche | Owner | Série/Parallèle | Durée | Dépend de |
|---|-------|-------|-----------------|-------|-----------|
| 4.1 | Tests end-to-end complets (JPEG + CR3 + NEF) | Forge + Argus | Série | 3j | 3.4 |
| 4.2 | Validation CGU par JCH | JCH + Renard | Parallèle | 1j | 2.6 |
| 4.3 | Test paiement Stripe (sandbox → live) | Forge | Après 4.1 | 1j | 4.1 |
| 4.4 | Article WILDLENS "Comment l'IA juge votre photo" | Miel | Parallèle | 3j | 3.6 |
| 4.5 | SEO landing page (mots-clés, meta, structure) | Trace | Parallèle | 2j | 3.5 |
| 4.6 | Setup WhiteWall ARTEON (étape 9) | Forge | Parallèle | 2j | 3.7 |
| 4.7 | Sélection + préparation 10 photos JC (étape 11) | JCH + Lynx | Parallèle | 4j | - |

---

### SEMAINE 6-7 — Beta privée (J35–J49)

| # | Tâche | Owner | Série/Parallèle | Durée | Dépend de |
|---|-------|-------|-----------------|-------|-----------|
| 5.1 | Recrutement 15 bêta-testeurs WILDLENS | Miel + Delphi | Début S5 | 3j | 4.4 |
| 5.2 | Beta fermée — 15 utilisateurs, 1 analyse gratuite/personne | Tous | Série après 4.3 | 7j | 4.3 |
| 5.3 | Collecte feedback beta (formulaire structuré) | Delphi | Parallèle 5.2 | 7j | 5.2 |
| 5.4 | Ajustements prompt, PDF, UX selon beta | Argus + Forge | Après 5.3 | 3j | 5.3 |
| 5.5 | Intégration WILDLENS ↔ ARTEON (étape 10) | Forge | Parallèle | 3j | 3.7 |
| 5.6 | Approche 2 clubs photo pour offre B2B | Delphi | Parallèle | 5j | 3.2 |
| 5.7 | Retravail 3 éditions WILDLENS (étape 12) | Miel | Parallèle | 4j | - |

---

### SEMAINE 7-8 — Lancement public (J49–J56)

| # | Tâche | Owner | Série/Parallèle | Durée | Dépend de |
|---|-------|-------|-----------------|-------|-----------|
| 6.1 | **LANCEMENT critique.arteon.be** | Forge | Série après 5.4 | 1j | 5.4 |
| 6.2 | Email WILDLENS subscribers — annonce lancement | Miel | Série après 6.1 | 1j | 6.1 |
| 6.3 | Article WILDLENS publié (réseaux + Ghost) | Miel | Série 6.2 | 1j | 4.4 |
| 6.4 | Monitoring coûts API en temps réel (dashboard simple) | Forge | Parallèle | 2j | 6.1 |
| 6.5 | Activation SEO + Google Search Console | Trace | Parallèle | 1j | 6.1 |
| 6.6 | Finalisation ARTEON V1 (étape 13) | Vega + Forge | Parallèle | 10j | 5.5 |

---

### SEMAINE 8-12 — Croissance vers KPI (J56–J90)

| # | Tâche | Owner | Action | Cible |
|---|-------|-------|--------|-------|
| 7.1 | Conversion 1er club B2B | Delphi | Suivi + démo | +€200/mois |
| 7.2 | Article technique Argus dans WILDLENS × 1/mois | Argus + Miel | Content régulier | +trafic organique |
| 7.3 | Programme "1 analyse offerte si partage résultat" | Miel | Growth loop | +nouveaux users |
| 7.4 | **LANCEMENT ARTEON V1** | Forge + Vega | Intégration critique | Audience élargie |
| 7.5 | Analyse data `argus_critique.db` — Lynx distille 1ers presets | Lynx | Après 50 analyses | Valeur ajoutée |
| 7.6 | Revue pricing selon volume réel | Bruno | J+70 | Optimisation |

---

## 6. Chemin critique (ce qui bloque tout le reste)

```
DÉCISION NOM (J0)
    └── Charte graphique (J1→J5)
            └── Landing page (J14→J18)
                    └── Beta (J35→J49)
                            └── LANCEMENT (J49)

PARALLÈLE :
    Tests 50 photos (J1→J7) ──→ Calibration prompt (J7→J10) ──→ Qualité validée
    Backend technique (J7→J21) ──→ Stripe (J21→J24) ──→ Tests (J28→J35)
    Legal CGU (J7→J14) ──→ Validé JCH (J14) ──→ Go beta
```

**Délai incompressible minimum : 49 jours (7 semaines) avant lancement.**

---

## 7. Projection de revenus

| Période | Analyses | CA brut | Coûts API | Net |
|---------|----------|---------|-----------|-----|
| Beta (J35–J49) | 15 gratuites | €0 | €0,30 | -€0,30 |
| Mois 1 post-lancement | 80 | €232 | €1,60 | €220 |
| Mois 2 | 200 + 1 club | €780 | €4 | €766 |
| **Mois 3** | **280 + 1 club** | **€1 012** | **€5,60** | **€996** ✓ |
| Mois 6 | 400 + 2 clubs | €1 560 | €8 | €1 542 |

---

## 8. Équipe et responsabilités

| Spécialiste | Rôle dans ce projet | Charge |
|-------------|---------------------|--------|
| **Forge** 🦦 | Backend, API, Shopify, intégrations techniques | Fort |
| **Vega** 🦚 | Charte graphique, landing page, UX, templates ARTEON | Fort |
| **Argus** 🦅 | Calibration prompt, validation qualité, documentation | Moyen |
| **Miel** 🐝 | Contenu WILDLENS, emails, réseaux, growth | Moyen |
| **Renard** 🦊 | CGU, RGPD, mentions légales | Ponctuel |
| **Bruno** 🐻 | Pricing, suivi coûts, revue J+70 | Ponctuel |
| **Delphi** 🐬 | Beta recrutement, B2B clubs, CRM | Moyen |
| **Lynx** 🐆 | Validation corrections, presets distillés (dès 50 analyses) | Ponctuel |
| **Trace** 🕷️ | SEO landing page, Search Console | Ponctuel |

---

## 9. Risques et mitigations

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Qualité analyse insuffisante → bad reviews | Moyen | Fort | 50 photos testées avant lancement, beta fermée |
| Volume insuffisant mois 1-2 | Moyen | Moyen | 1 club B2B en parallèle compense |
| Coût API explose si viral | Faible | Moyen | Rate limiting (5 analyses/jour/user gratuit) |
| ARTEON V1 retard | Moyen | Faible | Service critique indépendant, non bloqué |
| Concurrent lance avant J+49 | Faible | Moyen | Avance technique pipeline LR + data déjà accumulée |
| Charge validation humaine trop élevée à volume fort | Moyen | Moyen | JCH au lancement → reviewer dédié si > 20 analyses/jour |

### Note pipeline — Validation humaine (décision 2026-05-02)

Le service n'est **pas instantané** — c'est un choix de positionnement délibéré :

```
Upload → Filtre éthique auto → IA génère analyse + PDF + XMP
    → Notification expert ARTEON
        → Expert valide avant/après + rapport (~5 min)
            → Email envoyé au client
Délai annoncé : sous 2 heures
```

**Implications :**
- Wording site : "analysée par nos experts, assistés par l'IA" — pas "IA automatique"
- JCH est le premier validateur au lancement (charge estimée : 5–10 min/analyse)
- Interface de validation à construire (Forge) : notification + aperçu avant/après + bouton Valider/Corriger
- SLA 2h : plage horaire à définir (ex. 8h–22h) avec mention hors-horaires
- Différenciateur fort vs concurrents 100% auto — justifie le prix et la qualité

---

## 10. Décisions nécessaires de JCH (dans l'ordre)

| Priorité | Décision | Délai | Impact si retard |
|----------|----------|-------|-----------------|
| ✅ 1 | **Nom du service : `L'Instant Lu`** ← DÉCIDÉ 2026-05-02 | J0 | ✓ Débloqué |
| ✅ 2 | **Prix : €1,90 TTC** + gratuit à l'inscription + pack découverte €0,99 ← DÉCIDÉ 2026-05-02 | J1 | ✓ Débloqué |
| ✅ 3 | **Critères éthiques définis** ← DÉCIDÉ 2026-05-02 — voir §12 | J1 | ✓ Débloqué |
| ✅ 4 | **Beta sur invitation (15 WILDLENS)** — précédée validation interne photos JCH ← DÉCIDÉ 2026-05-02 | J5 | ✓ Débloqué |
| ✅ 5 | **B2B dual-track** : clubs photo (€150-250/mois) + éditeurs éthiques (€100-400/mois + badge certifié) ← DÉCIDÉ 2026-05-02 | J14 | ✓ Débloqué |
| ✅ 6 | **Architecture ARTEON d'abord** — L'Instant Lu intégré dès V1, pas en parallèle ← DÉCIDÉ 2026-05-02 | J30 | ✓ Débloqué |

---

## 11. KPI dashboard — Ce qu'on mesure chaque semaine

```sql
-- Revenu semaine
SELECT strftime('%W', created_at) AS semaine,
       COUNT(*) AS analyses,
       COUNT(*) * 2.90 AS ca_brut,
       SUM(cost_usd) * 0.92 AS cout_api_eur,
       COUNT(*) * 2.90 - SUM(cost_usd) * 0.92 AS marge_nette
FROM analyses
WHERE created_at >= date('now', '-7 days')
GROUP BY semaine;
```

Indicateurs hebdomadaires :
- Nombre d'analyses payantes
- Taux de rétention (utilisateurs qui reviennent)
- Coût moyen par analyse (surveiller la dérive)
- Score moyen des photos soumises (profil de la clientèle)
- % EXCELLENT / EXCEPTIONNEL (satisfaction indicateur)

---

---

## 12. Critères éthiques — Filtre à l'arrivée

> **✓ DÉCIDÉ — 2026-05-02**

### Refus automatiques (aucune validation humaine)

| Motif | Détection | Action |
|-------|-----------|--------|
| Humain visible dans l'image | Claude Haiku vision | Refus auto + email |
| Image générée par IA | Claude Haiku vision + métadonnées | Refus auto + email |
| Trucage/manipulation évident | Claude Haiku vision | Refus auto + email |
| Appâtage déclaré (titre, description, métadonnées) | Analyse texte | Refus auto + email |

### File de validation humaine (JCH décide)

| Motif | Détection | Action |
|-------|-----------|--------|
| Animal en captivité détecté | Claude Haiku vision | Notification JCH → validation 1 clic |
| → Jugé artistiquement intéressant | JCH approuve | Pipeline Argus normal |
| → Non retenu | JCH rejette + commentaire | Email motivé envoyé |

### Pipeline filtration

```
Upload photo
    ↓
[Claude Haiku — filtre éthique ~€0,002/image]
    ├── Humain → REFUS AUTO
    ├── IA génératif → REFUS AUTO
    ├── Trucage → REFUS AUTO
    ├── Appâtage → REFUS AUTO
    ├── Captivité → FILE MODÉRATION (JCH)
    └── Conforme → Pipeline Argus complet (~€0,20)
```

### Emails de refus

Chaque refus automatique déclenche un email :
- **Motif clair** en 1-2 phrases (sans accusation)
- **Recommandation** : ce que le photographe pourrait soumettre à la place
- **Ton ARTEON** : bienveillant, éducatif, aligné avec le manifeste

Exemple (humain visible) :
> *"L'Instant Lu analyse exclusivement des sujets naturels non humains. Votre photo contient une présence humaine. Vous pouvez nous soumettre une prise de vue centrée sur l'animal ou l'environnement naturel."*

Exemple (captivité refusée) :
> *"Cette photo a été évaluée et ne répond pas aux critères artistiques requis pour une analyse complète. L'Instant Lu privilégie les images offrant une lecture comportementale ou une qualité visuelle distinctive."*

### Nouveau composant technique (Forge)

- Module `filter_ethics.py` — appel Claude Haiku, retourne `{status, motif, confidence}`
- Table `moderation_queue` dans `argus_critique.db` — photos captivité en attente
- Interface de modération minimaliste (page admin sécurisée) — JCH valide/rejette en 1 clic
- Coût filtre : ~€0,002/image → négligeable même si 90% des uploads sont refusés

---

*Plan établi le 2026-05-02 — Dobby + équipe complète*  
*Révision prévue : J+49 (jour du lancement) et J+90 (vérification KPI)*
