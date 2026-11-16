# Thread — ARTEON

> Living document — maintenu par Dobby 🦉 en fin de session sur `/save`.
> **Dernière mise à jour** : 2026-11-15 — pack presets Naturaliste (36 XMP) + slider proportionnel MCP + étude L'Instant Lu (NO-GO/recadrage) + VPS Hostinger créé
> **Statut** : 🟢 relance engagée — VPS Hostinger créé + Ghost installé, domaine final `wildlens.arteon.be` (DNS à pointer)

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
| WildLens / Ghost | 🟢 | **VPS Hostinger créé + Ghost installé 15/11** (IP `2.25.8.208`) ; reste DNS/SSL/Mailgun/migration ; domaine final `wildlens.arteon.be` |
| Presets Naturaliste | 🟢 | **36 XMP** (12 looks × 3 forces) + mode d'emploi + landing ; **slider proportionnel MCP** (brique 2 : sélecteur 12 looks) |
| Instagram | 🟠 | Authentification Meta et lectures validées ; première publication préparée mais non effectuée par choix de JC |
| Shopify | ⏳ | V1 non préparée (aucune action depuis 02/07) |
| WhiteWall | ⏳ | Intégration non configurée |
| L'Instant Lu | 🟠 | Backend Argus diagnostiqué (52 analyses) ; conseil 6 stances → **NO-GO « lancer tel quel », recadrage presets + WildLens**, badge « Vérifié » gelé |

> ⚠️ **Blocage structurel identifié (22/10)** : la matière et la charte existent,
> mais l'exécution éditoriale exige du temps créatif JC, mobilisé sur IOT/VETALYX.
> Les 8 étapes non closes de la roadmap ne doivent pas être présentées comme acquises.

---

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
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

- [ ] **P1 · — · (JC)** Relire le brouillon Ghost « WildLens — Edition #4 » (slug `wildlens-edition-4`) puis donner le feu vert
- [ ] **P2 · — · (Dobby, après relecture)** Pousser les 3 autres éditions en brouillon via `scripts/ghost_import.py`
- [ ] **P3 · — · (JC + Forge)** Finir la migration WildLens : DNS A `wildlens` → `2.25.8.208`, `ghost setup ssl`, Mailgun, import contenu (VPS créé + Ghost installé 15/11)
- [ ] **P4 · — · (JC)** Allouer du temps créatif éditorial — blocage structurel : 8 étapes roadmap non closes
- [ ] **P5 · — · (Forge + Jade, après feu vert)** Traduire les éditions en FR + IT ; builder le changeur de langue Ghost (EN/FR/IT) avec détection géoloc IP pour la langue par défaut
- [ ] **P6 · — · (Forge)** Presets brique 3 : masques IA (sujet/œil/plumage/arrière-plan) — design `strategy/brique-3-masques-ia-design.md`, tâche `task_a60c239c` ; brique 4 : endpoint `/recommend` (EXIF niveau 1 d'abord, Dobby)
- [ ] **P7 · — · (JC)** Nettoyer le doublon de preset LRC (37 importés au lieu de 36) + galerie avant/après définitive (12 paires)

## TTD — Done (session 2026-11-05)

- [x] 2026-11-05 · Authentification Meta et lectures validées ; procédure Instagram documentée
- [x] 2026-11-05 · Première publication contrôlée sans publier ; diagnostic Ghost et e-mail au support

---

## Historique sessions

| Date | Résumé session | Livrable |
|------|---------------|----------|
| 2026-11-15 | Presets 36 XMP + slider proportionnel MCP + étude L'Instant Lu (conseil NO-GO/recadrage) + recensement marché + cartographie fonctionnelle + VPS Hostinger créé | `presets-naturaliste/`, `_local/lightroom-mcp/scripts/looks.mjs`, `strength_server.mjs`, `strategy/recensement-presets-xmp-animaliere.md`, `strategy/cartographie-fonctionnelle-presets.md`, `strategy/plan-reorientation-instant-lu.md` |
| 2026-11-15 | Renumérotation éditions, décision self-host Hostinger, achat VPS + installation Ghost ; recherche mails Gandi (orban45.be identifiée) | `wildlens/runbook-ghost-selfhost-hostinger.md`, `wildlens/editions/_archive/` |
| 2026-11-05 | Instagram préparé sans publication ; Ghost diagnostiqué puis mis en pause après e-mail au support | `docs/procedure-acces-instagram-wildlens.md`, `wildlens/instagram-launch-kit.md` |
| 2026-10-24 | Positionnement éditorial différencié, launchd réactivé et édition #5 rédigée | `wildlens/instagram-launch-kit.md` |
| 2026-07-02 | Restructuration 3 projets photo, WildLens promu, INDEX croisés | — |

---

## Liens

- INDEX : `03_PROJECTS/02_ARTEON/INDEX.md`
- WildLens INDEX : `03_PROJECTS/02_ARTEON/wildlens/INDEX.md`
- Roadmap : 13 étapes, 4 ✅, 8 ⏳, 1 🔴 (reprise des éditions WildLens)

---

*Fichier maintenu par Dobby 🦉 via le skill `pka-thread-file`.*
