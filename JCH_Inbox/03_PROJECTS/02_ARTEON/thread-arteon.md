# Thread — ARTEON

> Living document — maintenu par Dobby 🦉 en fin de session sur `/save`.
> **Dernière mise à jour** : 2026-11-22 — template v2 réconcilié + procédure de rédaction + #4 rédigée (pigeon ramier) + rendu PDF Ghost + impression
> **Statut** : 🟢 actif — site FR en production (4 éditions : #1 publiée 18/11, #3 28/11, #2 05/12, #4 brouillon 22/11)

---

## Vue d'ensemble

Photographie naturaliste éditoriale — marque ARTEON + service WildLens + futur L'Instant Lu. Shopify + Ghost + WhiteWall. Instagram sert de couche de découverte vers Ghost. Restructuration 3 projets photo terminée (02/07). Roadmap : **4 étapes terminées, 8 en attente, 1 rouge**.

---

## État actuel

| Axe | Statut | Détail |
|-----|--------|--------|
| Global | 🟢 | Relance engagée — quatre éditions présentes (dernière : 31/10), publication à vérifier au cas par cas ; launchd hebdo réactivé |
| Roadmap 13 étapes | 🟠 | **4 ✅ · 8 ⏳ · 1 🔴** — étapes 1 à 4 closes ; étape 12 rouge |
| Charte de marque | ✅ | Livrée (étape 4/13) |
| WildLens / Ghost | 🟢 | **Site FR en production** — `https://wildlens.arteon.be` 200, DNS + SSL + Mailgun ✅ ; thème ARTEON **en français** déployé ; **4 éditions FR** : #1 publiée 18/11, #3 programmée 28/11, #2 programmée 05/12, #4 (pigeon ramier) brouillon 22/11 ; template v2 (Cadre/Virage/Objectif/Constat) + procédure `ref/procedure-redaction-edition.md` + double-check Ghost/Markdown ; reste : abonnement |
| Presets Naturaliste | 🟢 | **36 XMP** (12 looks × 3 forces) + mode d'emploi + landing ; **slider proportionnel MCP** (brique 2 : sélecteur 12 looks) |
| Instagram | 🟢 | **1ᵉʳ post publié 17/11** (robin.jpg) → `https://www.instagram.com/p/Df2zb1LCDgT/` ; **légende passée en FR** (édition manuelle — l'API Graph ne permet pas la modif de légende) ; reste : lien en bio + premier relevé insights |
| Shopify | ⏳ | V1 non préparée (aucune action depuis 02/07) |
| WhiteWall | 🟠 | **Repositionné** : fournisseur interchangeable (pas marchand de labo) — conseil 17/11 |
| Tirages / Éditions | 🟠 | **GO conditionnel** — « ARTEON Éditions, le tirage documenté » (édition numérotée, corpus propre, provenance anti-IA) ; séquence presets → WildLens → édition #1 → affiliation (label) → B2B |
| L'Instant Lu | 🟠 | Backend Argus diagnostiqué (52 analyses) ; conseil 6 stances → **NO-GO « lancer tel quel », recadrage presets + WildLens**, badge « Vérifié » gelé |

> ⚠️ **Blocage structurel identifié (22/10)** : la matière et la charte existent,
> mais l'exécution éditoriale exige du temps créatif JC, mobilisé sur IOT/VETALYX.
> Les 8 étapes non closes de la roadmap ne doivent pas être présentées comme acquises.

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-11-22 | **Le Constat (④) devient systématique** — angle pro-nature / anti-spécisme (plus optionnel). #4 : chasse de la tourterelle des bois, « autorités françaises laxistes », sources non-NGO (Conseil d'État / Légifrance / FACE) | Décision JC en rédaction #4 |
| 2026-11-22 | **Template WildLens réconcilié** — photo en tête = feature image Ghost, sommaire cliquable = TOC thème (hors Markdown). Double-check Ghost/Markdown obligatoire. Rôles : Virage = innovation techno, Objectif = sujet technique | Comparaison rendu Ghost #1 vs source Markdown |
| 2026-11-22 | **Édition #3 assumée telle quelle** — reste sur l'ancienne structure 5 sections (pas de repassage au format v2 4 sections). Le format v2 (Cadre/Virage/Objectif/Constat) s'applique aux éditions suivantes. | Décision JC après réconciliation du nommage des sections |
| 2026-11-19 | **Pivot WildLens « tout en français »** — FR pour le lancement (audience francophone première cible), EN en réserve, IT plus tard ; pas de compte Instagram séparé par langue avant traction. 3 éditions traduites + réimportées, thème FR déployé, locale fr. | Décision stratégique après analyse du funnel et de l'audience cible ; JC valide le pivot |
| 2026-11-17 | **Pilier tirage/galerie repositionné « ARTEON Éditions »** — NO-GO « intermédiaire d'impression » (marge ~22 % net, CAC > marge) ; GO conditionnel « éditeur de tirages documentés » (marge 42–61 %, corpus propre + provenance anti-IA) ; affiliation = label payant, pas marketplace | Conseil 5 stances → `TEAM_Inbox/2026-11-17_dobby_conseil_tirage-galerie.md` ; JC valide le rôle d'éditeur. ⚠️ Lacune : compétences impression photo non disponibles |
| 2026-11-16 | **Différenciateur repositionné sur 3 piliers complets** : le grading (roues ColorGrade) était droppé par le SDK Lightroom — récupéré via les clés legacy `SplitToning*` (substitution dans `looks.mjs`). Courbe paramétrique + grading + TSL désormais tous vérifiés proportionnels en prod. | Proposition 1 + isolation catalogue + confirmation visuelle des roues |
| 2026-11-16 | **Partie C (Amount natif) : la « supériorité sur le Amount » est falsifiée** — le Amount scale la saturation du grading, la TSL, le grain et le base (mesuré ×0,5/×2). Différenciateur recadré sur la courbe paramétrique scalable + l'invariant documenté (pas sur le grading). | `measure-amount.mjs` + read-back `SplitToning*` |
| 2026-11-16 | **P0+P1 presets appliqués** : WB/expo découplées des 36 XMP, 3ᵉ roue grading (midtones) + Luminance + Blending/Balance par look, contrat de look `{forme/ancre/amplitude}` documenté ; brique 3 (masques IA) designée → Forge | 7 transcripts Lightroom analysés + scripts `strip_wb_expo_xmp.py` / `add_midtone_grading_xmp.py` |
| 2026-11-15 | **L'Instant Lu recadré** : NO-GO « lancer tel quel » — retirer badge, prix ≥4-5 €, valider l'espèce, « conseil éditorial » ; presets + WildLens prioritaires | Conseil 6 stances parallèles |
| 2026-11-15 | **Presets Naturaliste 36 + curseur proportionnel** = différenciateur technique (le Amount natif ne scale pas la courbe ni le grading — nous si) ; aucun XMP tiers (licence) ; premium = masques IA | Étude marché + cartographie fonctionnelle |
| 2026-11-14 | **WildLens multilingue** : EN (base) + FR + IT ; changeur de langue + détection géoloc IP (langue par défaut) ; section **Keywords** en tête de chaque édition | Relecture JC de l'édition #4 : section chasse traduite EN ; keywords ajoutés en tête |
| 2026-11-15 | **Self-host Ghost sur VPS Hostinger KVM 1** (datacenter UE) — abandon Ghost(Pro) 18 $/mois ; VPS = brique d'infra réutilisable PKA | Coût annuel ~78-144 $ vs 156-348 $ ; thème custom libre ; souveraineté liste d'abonnés |
| 2026-11-12 | Recréation Ghost sur `wildlens-journal.ghost.io` (option A) | Ancien compte inaccessible (carte inconnue) ; rien de publié à perdre ; JC exécute le signup, Dobby migre URLs + credentials |
| 2026-11-13 | **Compte récupéré — pas de recréation** ; domaine final `wildlens.arteon.be` | Connexion admin `wildlens.ghost.io` réussie (essai 14 j) ; finaliser le site existant ; domaine custom dans un second temps |
| 2026-11-05 | Aucune publication Instagram sans nouvelle demande explicite de JC | Préparation technique validée, mais autorisation de publication non accordée |
| 2026-11-05 | Ghost mis en pause après e-mail au support | Reprendre la destination éditoriale après réponse du support |
| 2026-10-24 | Positionnement éditorial : se démarquer par l'info, les questions soulevées, les solutions (pas les « 5 astuces ») | Différenciation vs blogs/newsletters |
| 2026-10-24 | Réactivation launchd `com.dobby.wildlens-weekly` + édition #5 rédigée | Reprise cadence hebdo |
| 2026-07-02 | WildLens promu service prioritaire | Sans extraction en projet autonome |
| 2026-07-02 | INDEX croisés ARTEON/PHOTO_AI_JURY/PHOTO_NATURE | 3 couches d'un même système unifiées |

---

## TTD — Pending

- [ ] **P1 · 2026-12-12 · (JC)** Valider l'édition #4 (pigeon ramier) → `draft → scheduled` + poser la photo en feature image Ghost
- [ ] **P1 · — · (Jade)** Traduire les 3 éditions en italien (FR livré, EN en réserve) — après traction FR
- [ ] **P2 · — · (Dobby)** Recoller le hashtag #photographyethics (coupé au collage Instagram)
- [ ] **P3 · — · (JC)** Renouveler le token Instagram avant le 04/01/2026 (60 j)
- [ ] **P4 · — · (JC)** Allouer du temps créatif éditorial — blocage structurel : 8 étapes roadmap non closes
- [ ] **P6 · — · (Forge)** Presets brique 3 : masques IA (sujet/œil/plumage/arrière-plan) — design `strategy/brique-3-masques-ia-design.md`, tâche `task_a60c239c` ; brique 4 : endpoint `/recommend` (EXIF niveau 1 d'abord, Dobby)
- [ ] **P7 · — · (JC)** Nettoyer le doublon de preset LRC (37 importés au lieu de 36) + galerie avant/après définitive (12 paires)
- [ ] **P8 · M1 test aveugle · (JC + Dobby)** Correction manuelle de 16 photos (sélection `strategy/m1-test-aveugle-selection.md`) + jugement en aveugle ~5 photographes — critère « pire+indifférent » ≤ 50 % sinon stop. Préalables : mapping `LrC to-NN` → RAW `~/Pictures/` (JC fournit, ou correction directe dans Lightroom) ; trancher Nocturne (absent du corpus) + Golden hour (partiel). Découle du conseil `TEAM_Inbox/2026-11-16_dobby_conseil_correction-photo.md` (NO-GO service, GO conditionnel).
- [ ] **P9 · — · (JC + Dobby)** Choisir le tireur (compétence impression) — JC : s'associer à un pro du tirage ; Dobby : fournisseur white-label maintenant (coût unitaire + clause défauts), association différée post-édition #1 + apport marché B2B. Gate trafic avant galerie (2 000 visites qualifiées / 60 j)
- [ ] **P10 · — · (Dobby)** Tester l'édition #1 en pré-vente bornée (coût ~300–400 €, kill criteria : ≥ 8 préventes = GO) — uniquement après presets + WildLens

## TTD — Done (session 2026-11-05)

- [x] 2026-11-05 · Authentification Meta et lectures validées ; procédure Instagram documentée
- [x] 2026-11-05 · Première publication contrôlée sans publier ; diagnostic Ghost et e-mail au support

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-11-22 | Template v2 réconcilié (4 sections), procédure de rédaction + double-check Ghost/Markdown, #4 rédigée (pigeon ramier + Constat tourterelle), #2 corrigée, #3 assumée, outil `bin/wildlens-ghost-pdf` + 4 PDF + impression | `wildlens/ref/procedure-redaction-edition.md`, `wildlens/editions/fr/wildlens-edition-4-pigeon-ramier.md`, `bin/wildlens-ghost-pdf`, `scripts/wildlens_weekly.py`, `strategy/plan-action-wildlens.md` |
| 2026-11-20 | Renumérotation Ghost résolue (#4→#1) + nettoyage structure 02_ARTEON + **pivot FR** (3 éditions traduites, thème FR, locale fr) + clipper iPad→inbox | `wildlens/editions/final/`, `wildlens/editions/fr/`, `bin/pka-clip-pull`, `_local/launchd-plists/com.dobby.pka-clip-pull.plist` |
| 2026-11-15 | Presets 36 XMP + slider proportionnel MCP + étude L'Instant Lu (conseil NO-GO/recadrage) + recensement marché + cartographie fonctionnelle + VPS Hostinger créé | `presets-naturaliste/`, `_local/lightroom-mcp/scripts/looks.mjs`, `strength_server.mjs`, `strategy/recensement-presets-xmp-animaliere.md`, `strategy/cartographie-fonctionnelle-presets.md`, `strategy/plan-reorientation-instant-lu.md` |
| 2026-11-15 | Renumérotation éditions, décision self-host Hostinger, achat VPS + installation Ghost ; recherche mails Gandi (orban45.be identifiée) | `wildlens/runbook-ghost-selfhost-hostinger.md`, `wildlens/editions/_archive/` |
| 2026-11-05 | Instagram préparé sans publication ; Ghost diagnostiqué puis mis en pause après e-mail au support | `docs/procedure-acces-instagram-wildlens.md`, `wildlens/instagram-launch-kit.md` |
| 2026-10-24 | Positionnement éditorial différencié, launchd réactivé et édition #5 rédigée | `wildlens/instagram-launch-kit.md` |
| 2026-07-02 | Restructuration 3 projets photo, WildLens promu, INDEX croisés | — |

---

## Liens

- INDEX : `03_PROJECTS/02_ARTEON/INDEX.md`
- WildLens INDEX : `03_PROJECTS/02_ARTEON/wildlens/INDEX.md`
- Executive summary interne (chantiers / ordre / gardes-fous) : `strategy/arteon-executive-summary.md`
- Plan « produit fini » WildLens : `strategy/plan-wildlens-produit-fini.md`
- Roadmap : 13 étapes, 4 ✅, 8 ⏳, 1 🔴 (reprise des éditions WildLens)

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
