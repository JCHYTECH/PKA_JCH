---
date: 2026-05-02
tags: [projet, arteon, [[Argus]], produit-web, strategie, wildlife]
type: knowledge
domain: AI-Tools
status: réflexion
---

# [[Argus]] Web Service — Réflexion stratégique

> Service de critique photographique IA pour abonnés ARTEON.  
> Orchestré par [[Dobby]] — contributions : [[Iris]] (marché), [[Vega]] (produit), [[Bruno]] (finance), [[Forge]] (technique), [[Renard]] (légal), [[Argus]] (contenu expert).

---

## 1. Définition du projet

Un photographe naturaliste visite arteon.be, upload sa photo wildlife, paie, et reçoit dans les minutes suivantes :

- Un **rapport PDF professionnel** — critique sur 5 axes, scores, analyse chromatique, recommandations de retouche
- Un **preset XMP Lightroom personnalisé** pour sa photo spécifique
- Une **liste de corrections concrètes** (balance des blancs cible, exposition, etc.)

Le moteur IA est [[Claude]] Opus 4.7 (vision). L'expert fictif qui signe = à définir (voir §4).

---

## 2. Opportunité marché — [[Iris]] 🦅

### Ce qui existe et ses lacunes

| Service | Prix | Problème |
|---------|------|----------|
| PhotoCritique.ai | $0,20/image | Généraliste, pas de preset, pas de PDF |
| PhotoMentor.pro | $40/an | Feedback basique |
| Critique humaine pro | 5–10€/image | Cher, long, pas de preset |
| Coaching photo wildlife | 2 000–5 000€ | Inaccessible aux amateurs |
| Formations en ligne (Cornell, School of Photography) | 200–800€ | Communautaire, pas personnalisé |

### Gaps identifiés

1. **Aucun service spécialisé wildlife** — tous les services IA sont généralistes
2. **Aucun preset XMP personnalisé par photo** — inexistant sur le marché
3. **Aucun PDF structuré de style jury** avec scoring par axe
4. **Workflow fragmenté** — critique + preset = deux recherches séparées
5. **Trou de prix** — entre le gratuit générique ($0) et le pro humain (5-10€) : rien de qualitatif

### Marché cible

- Photographes nature/wildlife amateurs sérieux (segment à croissance rapide)
- Investissement équipement : 1 000–10 000€ — consentent à payer pour progresser
- Marché caméra wildlife : 612M USD (2025) → 896M USD (2030), CAGR 8%
- Besoin non satisfait : feedback expert abordable + actionnable dans Lightroom

### Conclusion [[Iris]]

**Opportunité claire, créneau vide.** La combinaison critique spécialisée wildlife + preset XMP + rapport PDF n'existe nulle part.

---

## 3. Modèle économique — [[Bruno]] 🐻

### Coût de revient par analyse

| Poste | Coût estimé |
|-------|-------------|
| [[Claude]] Opus 4.7 (image ~1500px + prompt + réponse) | ~0,20–0,25€ |
| Génération PDF (serveur, CPU) | ~0,02€ |
| Stockage + bande passante (S3/R2) | ~0,01€ |
| **Total coût variable** | **~0,25€/analyse** |

*Avec prompt caching sur le system prompt : coût réduit à ~0,15€/analyse.*

### Options de pricing

#### Option A — Crédit à l'unité
| Offre | Prix | Marge |
|-------|------|-------|
| 1 analyse | 4,90€ | ~4,65€ (95%) |
| Pack 5 analyses | 19,90€ (3,98€/u) | ~4,65€/u |
| Pack 10 analyses | 34,90€ (3,49€/u) | ~3,24€/u |

#### Option B — Abonnement mensuel
| Tier | Prix/mois | Inclus | Cible |
|------|-----------|--------|-------|
| Observateur | 9,90€ | 3 analyses/mois | Débutant sérieux |
| Naturaliste | 19,90€ | 8 analyses/mois | Amateur actif |
| Expert | 39,90€ | 20 analyses/mois + priorité | Passionné intensif |

#### Option C — Hybride (recommandée)
- 1 analyse gratuite à l'inscription (acquisition)
- Packs crédits pour usage occasionnel
- Abonnement pour utilisateurs réguliers
- **ARTEON Members** (abonnés existants) : tarif préférentiel (-20%)

### Seuil de rentabilité
À 4,90€/analyse avec 0,25€ de coût variable :
- 10 analyses/jour = 146€/mois net = autofinancement infrastructure dès J1
- 100 analyses/jour = 1 460€/mois net = produit viable standalone

---

## 4. Produit & positionnement — [[Vega]] 🦚

### Nom du service

> **✓ DÉCIDÉ — 2026-05-02 : `L'Instant Lu`**

Choix de JCH, ancré dans le slogan ARTEON *"L'instant figé, la pensée en mouvement"* — lire un instant figé, c'est exactement ce que fait la critique. Ton bienveillant, expert, sans sévérité de jury.

URL : `l-instant-lu.arteon.be` ou `critique.arteon.be` avec la marque **L'Instant Lu** en façade.

### Ce que l'utilisateur reçoit

```
Upload photo wildlife
        ↓
    Paiement (Stripe via Shopify)
        ↓
    Analyse ~25 secondes
        ↓
Email ou téléchargement :
    ├── rapport_photo.pdf
    │     ├── Miniature de la photo
    │     ├── Fiche technique (si RAW : boîtier, focale, ISO…)
    │     ├── Scores jury 5 axes (/20 chacun)
    │     ├── Analyse chromatique
    │     ├── Critique détaillée par axe
    │     ├── Corrections LR recommandées (Température: 4200K→5400K ▲2/5)
    │     └── Pistes de retouche locale
    └── preset_photo.xmp
          └── Importable directement dans Lightroom Classic / LR Mobile
```

### Différenciation ARTEON

- Le ton de la critique reprend les valeurs ARTEON : scientifique, contemplatif, sans complaisance
- L'IA refuse de noter positivement une photo d'animal en détresse ou manifestement appâté (éthique intégrée)
- Scoring comparatif possible (futur) : "Votre photo se situe dans le top 30% des analyses de la semaine"

---

## 5. Architecture technique — [[Forge]] 🦦

### Ce qui change vs le plugin LR

Le plugin LR s'exécute **localement** ([[Python]] sur Mac de JCH). Le service web doit s'exécuter **côté serveur**.

### Pipeline web

```
[Browser ARTEON]
    │ Upload JPEG/RAW (max 20 MB)
    ↓
[Upload endpoint] → S3/Cloudflare R2 (stockage temporaire 24h)
    ↓
[Job queue] → async worker Python
    │   ├── Si RAW : exiftool extract preview
    │   ├── Resize → 1500px
    │   ├── Claude Opus 4.7 vision API
    │   ├── generate_xmp.py → preset.xmp
    │   ├── pdf_report.py → rapport.pdf
    │   └── color_analysis.py
    ↓
[Notification] → Email (PDF + XMP en pièce jointe) OU lien download sécurisé
    ↓
[Nettoyage] → suppression fichiers après 7 jours
```

### Stack recommandé (MVP)

| Composant | Choix | Justification |
|-----------|-------|---------------|
| Frontend | Page Shopify custom | Déjà en place sur ARTEON |
| Paiement | Stripe (via Shopify) | Déjà configuré |
| Upload | Cloudflare R2 (presigned URL) | Pas cher, rapide |
| Worker | [[Python]] [[FastAPI]] sur VPS (Hetzner ~5€/mois) | Même stack que le pipeline existant |
| Email | Resend.com ou Mailgun | Simple, fiable, ~$0/mois au départ |
| Queue | [[Redis]] simple ou job table [[SQLite]] | MVP : [[SQLite]] suffit |

### Réutilisation du code existant

Les scripts `run_analysis.py`, `pdf_report.py`, `generate_xmp.py`, `dng_extract.py` sont directement réutilisables côté serveur — c'est la valeur du travail fait.

Seul ajout : une API wrapper (`POST /analyse`) + worker async.

### Formats acceptés

JPEG, PNG, WebP + tous RAW supportés (CR3, NEF, ARW, RAF, DNG, ORF, RW2, PEF, RAW, 3FR, IIQ) — déjà géré.

---

## 6. Cadre légal — [[Renard]] 🦊

### Points à couvrir dans les CGU/CGV

1. **Propriété intellectuelle des photos** : JCH n'acquiert aucun droit sur les photos uploadées. L'utilisateur conserve tous les droits.
2. **Usage des photos par l'IA** : Préciser que les photos sont analysées par [[Claude]] API (Anthropic) — vérifier la politique d'Anthropic sur les images soumises (pas d'entraînement sur données client pour API payante ✓ confirmé).
3. **Rétention des données** : Photos supprimées sous 7 jours. PDF/XMP = responsabilité de l'utilisateur après téléchargement.
4. **RGPD** : Upload = traitement de données (image peut contenir des métadonnées GPS). Déclaration RGPD à mettre à jour sur arteon.be.
5. **Contenu refusé** : Implémenter une clause permettant de refuser l'analyse d'images manifestement contraires à l'éthique ARTEON (appâtage documenté, détresse animale, etc.).
6. **Responsabilité des conseils** : Le rapport est un avis consultatif, pas une garantie de résultat. Clause de non-responsabilité standard.

### Note sur la facturation

Service numérique B2C = TVA applicable selon pays de l'acheteur (OSS UE). À vérifier avec le comptable de JCH.

---

## 7. Alignement avec la roadmap ARTEON

ARTEON est actuellement à l'**Étape 4 (charte graphique)**. Ce service web (appelons-le provisoirement **ARTEON Critique**) s'insère dans la roadmap comme une nouvelle entrée :

```
Étape 4  — Charte graphique ← en cours
Étape 5  — Template fiche artiste
...
Étape N  — ARTEON Critique (service IA) ← NOUVEAU
```

**Option A** : Lancer en parallèle du site V1 — service indépendant accessible depuis une URL dédiée (ex: `critique.arteon.be`)
**Option B** : Intégrer dans le site ARTEON V1 comme feature premium dès le lancement

Recommandation : **Option A** — permet de tester le service rapidement sans attendre le site V1 complet. Si ça marche, l'intégration V1 est une évidence.

---

## 8. Risques identifiés

| Risque | Probabilité | Impact | Mitigation |
|--------|-------------|--------|------------|
| Coût API explose (usage élevé) | Moyen | Moyen | Prompt caching + limite upload/jour |
| Qualité analyse insuffisante | Faible | Fort | Tests sur 50 photos avant lancement |
| Fraude (upload images non-wildlife) | Moyen | Faible | Prompt refuse, résultat médiocre, pas de remboursement si contenu non conforme |
| Concurrents copient le concept | Faible | Moyen | Avance technique + positionnement ARTEON fort |
| RGPD (images avec GPS) | Moyen | Fort | Stripping EXIF GPS à l'upload (exiftool) |

---

## 9. Prochaines étapes recommandées

### Phase 1 — Validation (2 semaines)
- [ ] JCH choisit le nom du service
- [ ] Tester 30 analyses sur des photos variées — valider la qualité
- [ ] Définir les critères éthiques d'analyse (que refuse [[Argus]] ?)
- [ ] [[Renard]] rédige les CGU/CGV du service

### Phase 2 — MVP technique (4 semaines)
- [ ] [[Forge]] construit l'API wrapper + worker async
- [ ] Page d'upload sur Shopify (ou landing page autonome)
- [ ] Intégration Stripe
- [ ] Tests end-to-end

### Phase 3 — Beta privée (2 semaines)
- [ ] 10 abonnés WILDLENS testeurs — feedback
- [ ] Ajustements prompt et PDF
- [ ] Activation du pricing

### Phase 4 — Lancement
- [ ] Annonce WILDLENS + newsletter
- [ ] 1 analyse gratuite à l'inscription
- [ ] Monitoring coûts API en temps réel

---

## 10. Questions ouvertes pour JCH

1. **Nom du service** — "L'Œil du Jury" ou autre ?
2. **Pricing** — crédits à l'unité, abonnement, ou hybride ?
3. **Timing** — lancer avant ou avec le site V1 ARTEON ?
4. **Éthique IA** — quelles photos le service refuse-t-il d'analyser ? (appâtage, animaux en cage, trucage non déclaré ?)
5. **Volume de lancement** — MVP fermé (bêta WILDLENS) ou ouverture directe ?
6. **Langue** — FR uniquement au lancement ou FR/EN d'emblée ?

---

*Document de travail — [[Dobby]] · [[Iris]] · [[Vega]] · [[Bruno]] · [[Forge]] · [[Renard]] · [[Argus]]*
*Statut : réflexion initiale — à compléter après arbitrages JCH*
