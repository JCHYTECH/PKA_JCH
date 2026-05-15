---
date: 2026-05-02
tags: [daily]
type: daily
status: active
---

# 2026-05-02 — Session PKA

## Actions — Session 8

- **Température EXIF** : `read_exif_temp()` ajoutée dans `run_analysis.py` — lit tag 37888 via PIL, fallback `exiftool`
- **PDF enrichi** : ligne Température affiche `XXXX K → YYYY K` si EXIF dispo + indicateur `▲/▼ N/5` (temp_level fourni par Claude)
- **XMP corrigé** : `WhiteBalance="Custom"` forcé dans `generate_xmp.py` quand `ColorTemperature` présent — LR interprétait comme delta relatif → bug +100 résolu
- **Lua JPEG fix** : `Temperature` ignoré sur JPEG dans `ArgusAnalysis.lua` (slider -100/+100, pas Kelvin)
- **Support CR3** : `dng_extract.py` mis à jour — cascade de tags (`-JpgFromRaw` → `-PreviewImage` → `-OtherImage`), suppression preview avant extraction, chemin exiftool hardcodé (`/opt/homebrew/bin/exiftool`)
- **exiftool installé** : `brew install exiftool` (v13.55) — nécessaire pour extraction preview RAW Canon CR3
- **Prompt Claude** : `temp_level` (-5 à +5) ajouté au JSON — Claude évalue l'intensité de la correction température
- **`language: french`** ajouté dans `~/.claude/settings.json`
- **Pipeline CR3 validé** depuis Lightroom : extraction preview → analyse Opus 4.7 → PDF + XMP cohérents ✓

## Décisions — Session 8

- **Temperature JPEG non appliquée** via LrDevelopController : limitation LR SDK confirmée (échelle -100/+100 incompatible Kelvin) — valeur indiquée dans PDF uniquement
- **exiftool chemin hardcodé** : PATH LR sandbox ne contient pas `/opt/homebrew/bin` — solution pérenne
- **temp_level côté Claude** : plus fiable que calcul local (Claude connaît le contexte photo)

## Prochaine étape

- Connecter `jc.havaux@jchytech.be` à Gmail (accès admin M365 requis)
- Premier brief Nova : séquence photo (combat d'oiseaux)
- Premier brief Vasco : produit Vetalyx spécifique
- Définir le contenu Energy department
- Batch processing + prompt caching (quand besoin identifié)

---

## Actions — Session 9 (continuation)

- **6 décisions ARTEON actées** dans `plan-action-critique-service.md`
- **Nom service** : *L'Instant Lu* — ancré dans le slogan "L'instant figé, la pensée en mouvement"
- **Prix** : €1,90 TTC + 1ère analyse gratuite + pack découverte €0,99 (sous la barre des €2)
- **Critères éthiques** : filtre auto (humains, IA, trucage, appâtage) + modération captivité par JCH — module `filter_ethics.py` à coder
- **Beta** : sur invitation (15 WILDLENS), précédée d'une phase 0 validation photos JCH (zéro RGPD)
- **B2B dual-track** : clubs photo (€150-250/mois) + éditeurs éthiques (badge "Vérifié L'Instant Lu", €100-400/mois)
- **Architecture** : ARTEON V1 d'abord — L'Instant Lu intégré dès le lancement, pas en parallèle
- **Idée enfants** : capturée en `ideas` DB (statut raw) — à évaluer après 6 mois de service adulte
- **Architecture & charte graphique ARTEON** : `arteon-architecture-charte.md` créé — sitemap complet, palette (Ocre #C17F3A), typo (Space Grotesk / Lora / IBM Plex Mono), 3 identités (ARTEON · WildLens · L'Instant Lu), 4 parcours utilisateurs, 8 livrables Vega priorisés
- **WildLens** : stratégie subdomain `wildlens.arteon.be` (Ghost conservé + réseau distribution) + vitrine légère sur arteon.be
- **L'Instant Lu navigation** : position stratégique — dernier item nav, fond ocre, 1er sur mobile

## Décisions — Session 9

- **L'Instant Lu** choisi comme nom (pas "L'Œil du Jury" — trop sévère) — ancré dans ADN ARTEON
- **€1,90 TTC** vs €2,90 initialement prévu : franchir la barre des €2 crée une friction, pas en dessous
- **Phase 0 photos JCH** avant beta : principe RGPD + meilleur calibrage (JCH connaît ses images)
- **Ghost en subdomain** plutôt qu'intégration Shopify : réseau de recommandation Ghost = atout distribution
- **Architecture globale avant lancement** : évite les reprises coûteuses — bonne décision stratégique

## Prochaine étape — Session 10

- Validation maquettes wireframes par JCH (Vega)
- Phase 0 : sélectionner 50 photos JCH pour validation pipeline Argus
- Connecter `jc.havaux@jchytech.be` à Gmail (accès admin M365 requis)
- Premier brief Nova : séquence photo (combat d'oiseaux)
- Premier brief Vasco : produit Vetalyx spécifique

---

## Actions — Session 10 (continuation)

- **Rapport PDF Direction A validée** — redesign complet en 3 pages : couverture, analyse (score synthèse + 5 axes + critiques), corrections (LR avant/après + retouches locales style B)
- **Clarification LR** : cellule Température affiche `4 200 K → 5 600 K` (barré/cible) — confusion éliminée
- **Badges modifications** agrandis (format `a-modif-badge-lg`) — bien visibles sur page 2
- **Fiche client** : nom fichier + client ajoutés à l'en-tête page 1
- **Pistes retouche locale** : cards style Direction B intégrées en page 3
- **Idée DNG full-service** mémorisée : ARTEON réalise les corrections si le client livre en DNG pro

## Décisions — Session 10

- **Direction A retenue** comme format final du rapport L'Instant Lu
- **3 pages** (vs 2) : structure logique propre, aucun saut de page problématique
- **Service DNG** : idée à tester en Phase 0 — offre premium distincte

## Prochaine étape — Session 11

- Forge : implémenter `pdf_report.py` (reportlab) sur la base de la Direction A validée
- Forge : construire `filter_ethics.py` + table `moderation_queue`
- Phase 0 : sélectionner 50 photos JCH pour validation pipeline Argus
- Connecter `jc.havaux@jchytech.be` à Gmail
- Brief Nova + Vasco

---

## Actions — Session 11

- **`pdf_report.py` réécrit** (Forge) — reportlab 3 pages Direction A, polices Google Fonts avec fallback, compatible `run_analysis.py`
- **`filter_ethics.py` créé** (Forge) — Claude Haiku pré-screen, 4 catégories rejet auto, 2 modération (captivité/douteux), fallback défensif si JSON non-parseable
- **Table `moderation_queue`** créée dans `argus_critique.db` — migration idempotente, 3 index, FK vers `analyses`
- **`run_analysis.py` mis à jour** — filtre éthique en Step 0, codes de sortie 2 (rejet) et 3 (modération)
- **Vega enrichie** — rôle étendu : Creative Director Arts Visuels, Web & Brand — sensibilité photographique + graphisme éditorial + regard transversal (DB + fichier TEAM/vega.md)
- **Analyse juridique complète** (Renard) — 10 axes : RGPD, PI photos/rapports, responsabilité, EU AI Act, TVA/OSS, CGU, structure juridique
- **Recherche marque ARTEON** (Renard) — risque VW modéré sur classes 35/42, faible sur 41/16 — dépôt EUTM recommandé classes 41+16 en priorité
- **5 documents légaux rédigés** dans `docs/legal/` : CGU, politique confidentialité, contrat B2B clubs, contrat licence badge, texte droits images client
- **Coordonnées JCHYTECH intégrées** dans tous les documents légaux : BCE BE 0680.640.981 · TVA BE0680640981 · Rue des Renards 4, 4130 Tilff

## Décisions — Session 11

- **JCHYTECH** = entité légale, ARTEON = marque commerciale
- **Filtrage éthique avant paiement** — architecture validée : zéro débit si refus
- **Juridiction Liège** pour les contrats B2B (domicile JCHYTECH)
- **Indépendant** maintenu comme structure — réévaluation si CA > 40 000€/an
- **Dépôt marque** : EUTM classes 41+16 en priorité après recherche d'antériorités (~400€)

## Prochaine étape — Session 12

- JCH : signer DPA Anthropic (portail API — 10 min)
- JCH : mandater conseil PI pour recherche d'antériorités marque ARTEON (~400€)
- Forge : intégrer case de renonciation droit de rétractation dans le flow paiement Stripe
- Forge : page `arteon.be/legal` (documents publics CGU + politique confidentialité)
- Forge : URL `arteon.be/certification/[id]` pour vérification des badges B2B
- Phase 0 : sélectionner 50 photos JCH pour validation pipeline Argus
- Brief Nova : séquence combat d'oiseaux
- Brief Vasco : produit Vetalyx spécifique

---

## Actions — Session 12

- **Coordonnées JCHYTECH corrigées** dans tous les docs légaux : Jean-Claude Havaux (pas Jean-Christophe), Rue des Renards 4, 4130 Tilff, BCE BE 0680.640.981
- **todo-jch.html** créé — 22 tâches, 4 niveaux d'urgence, filtres projet/urgence, cases à cocher, barre de stats
- **hub.html** créé à la racine PKA_JCH — page d'accueil avec 6 dashboards, 6 projets actifs, 22 membres de l'équipe

## Décisions — Session 12

- Hub placé à la racine `/PKA_JCH/hub.html` pour accès rapide
- Todo DB en HTML interactif (pas de backend) — suffisant pour usage solo

## Prochaine étape — Session 13

- JCH : signer DPA Anthropic
- JCH : mandater conseil PI (marque ARTEON)
- JCH : ouvrir compte bancaire pro JCHYTECH
- Phase 0 : sélectionner 50 photos pour pipeline Argus
- Brief Nova + Vasco
