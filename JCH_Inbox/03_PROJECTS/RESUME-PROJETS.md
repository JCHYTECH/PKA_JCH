# Résumé des projets — PKA_JCH (03_PROJECTS)

> Généré le 2026-10-22 par Dobby 🦉 — synthèse fondée sur `etat-projets.md` (MAJ 2026-10-19),
> les `executive-summary.md` et l'arborescence réelle des dossiers.
> **Échelle d'avancement : 0** = très tôt (description encore à consolider) → **10** = pleinement opérationnel.

## Vue d'ensemble

| # | Projet | Avancement |
|---|--------|-----------|
| 1 | `01_AI_IT_TOOLS` | **8/10** |
| 2 | `02_ARTEON` / WildLens | **3/10** |
| 3 | `03_WILDNEXUS` | **5/10** |
| 4 | `05_PHOTO_AI_JURY` | **7/10** |
| 5 | `06_PHOTO_NATURE` | **7/10** |
| 6 | `07_TRAVELS` | **7/10** |
| 7 | `08_VETALYX` | **6/10** |
| 8 | `11_IOT` | **6/10** |

---

## 01_AI_IT_TOOLS — 8/10

**Description** : Infrastructure IA multi-modèles qui fait fonctionner tout PKA_JCH — orchestrateur Dobby, 31 spécialistes, `team.db`, `MEMORY.md`, bibliothèque de skills, hub OpenRouter, graphify, vault Obsidian. Le système nerveux du projet.

**Livrables attendus**
- Socle mémoire State/Log (`team.db`, `MEMORY.md`, boucle mémoire autonome)
- Bibliothèque de 30+ skills
- Knowledge graph (graphify) maintenu
- Routage multi-modèles (DeepSeek / Claude / Gemini / Qwen / Kimi + local Ollama)

**Avancement** : **8/10** — socle opérationnel et autonome. Pas 10 car évolution continue (boucle mémoire tout juste ajoutée, maintenance permanente des skills).

---

## 02_ARTEON / WildLens — 4/10

**Description** : Marque de photographie naturaliste éditoriale — galerie ARTEON (Shopify + tirages WhiteWall) et journal hebdomadaire WildLens (Ghost), avec L'Instant Lu (conseil photo) en tête de funnel.

**Livrables attendus**
- Galerie Shopify en ligne + intégration WhiteWall
- WildLens : édition hebdomadaire régulière
- Backend L'Instant Lu
- Charte de marque (livrée)

**Avancement** : **4/10** — charte livrée et édition #1 matérialisée, mais **relance éditoriale bloquée** (0 édition depuis 3 mois) ; Shopify, WhiteWall et L'Instant Lu non lancés.

---

## 03_WILDNEXUS — 3/10

**Description** : Projet ombrelle bioacoustique de terrain — device P0 (ESP32-S3, caméra PIR, micros stéréo I2S, LoRa) qui capture l'audio, et pipelines de classification (InsectNet pour les orthoptères, BirdNET / NEXUS_ACOUSTIC pour oiseaux et amphibiens).

**Livrables attendus**
- Device P0 assemblé et testé
- Pipeline de classification audio (InsectNet + NEXUS_ACOUSTIC)
- Datasets évalués (InsectSet459)
- ADR (contrat amont audio)

**Avancement** : **3/10** — design et recherche avancés (ADR-013/016/017, 13 scripts InsectNet, datasets évalués), mais **gelé** : panier Mouser (~279€) non commandé, dépend du P0 IOT.

---

## 05_PHOTO_AI_JURY — 7/10

**Description** : Argus, moteur IA de critique photographique naturaliste — analyse technique, naturaliste et artistique, score /100, recommandation de tirage et de preset Lightroom.

**Livrables attendus**
- Analyses fiables et calibrées
- Presets Lightroom exportables (XMP)
- Intégration MCP Lightroom

**Avancement** : **7/10** — opérationnel et autonome (58 analyses, 73,8/100, 81 % d'acceptation). Reste l'activation du MCP Lightroom.

---

## 06_PHOTO_NATURE — 8/10

**Description** : Workflow professionnel de photographie naturaliste — capture Canon → développement DxO/Lightroom → keyworder IA Gemma4 (62 catégories) → critique Argus → publication.

**Livrables attendus**
- Keyworder IA autonome (IPTC + XMP)
- Presets Argus (11 stockés)
- Pipeline capture → publication intégré
- Cross-références ARTEON

**Avancement** : **8/10** — workflow actif et autonome (keyworder déployé, 11 presets, cross-refs ARTEON). Dépend d'une pratique terrain régulière.

---

## 07_TRAVELS — 4/10

**Description** : Voyages et logistique van (Westfalia Kelsey 2026 / Ford Transit Custom), fiches destinations, pipeline DÉCOUVERTES (Telegram → fiches lieux) et Lupo Planner.

**Livrables attendus**
- Fiches destinations canoniques
- Lupo Planner opérationnel
- Pipeline DÉCOUVERTES → Planner
- Logistique stationnement / camping-scout

**Avancement** : **4/10** — briques en place (pka-decouvertes, Lupo-planner, fiches destinations), mais **gelé** : planification « en roulant », meuble banquette en design.

---

## 08_VETALYX — 6/10

**Description** : Société belge (Marche-en-Famenne) de diagnostic vétérinaire rapide — MVP allergie IgE chien/chat. Fournisseur Zheda Dixun (CN) via DIAHO (actionnaire 40 %). Marchés : FR, IT, ES, DE, BE.

**Livrables attendus**
- Contrat-cadre + annexes, statuts SRL, pacte, convention de bloc ✅
- Business plan chiffré 2026-2030 + modèle financier Excel ✅
- Pilote France 12 mois (4 phases, 200-300 cliniques) 📋 documenté, non démarré
- Qualification AFMPS / FAMHP ⏳ non tranchée
- 8 points notariés à lever ⏳

**Avancement** : **6/10** — la structuration est bien plus avancée que je ne l'avais noté (contrat-cadre v4.1 + annexes 1→10, BP V3 chiffré : CA 299 K€ → 7,2 M€, EBITDA 41 K€ → 4,2 M€, roadmap pilote France chiffrée à 420 K€ base). **Rien n'est encore vendu** et le verrou réglementaire AFMPS/FAMHP n'est pas levé.

> ⚠️ Note corrigée le 2026-10-22 : mon premier passage (4/10, « business plan et roadmap non définis ») était **faux** — il s'appuyait sur `executive-summary.md` (généré 03/07, périmé). Analyse complète : `08_VETALYX/2026-10-22_dobby_analyse-approfondie.md`.

---

## 11_IOT — 6/10

**Description** : Domotique distribuée sur 3 sites (serre + maison Esneux, Italie, van Lupo) — Home Assistant OS sur RPi 5, supervision Tailscale, zéro cloud.

**Livrables attendus**
- HA opérationnel sur les 3 sites
- Capteurs Zigbee installés
- Intégration WiCAN Pro (OBD/CAN)
- Installation complète dans le van (deadline 15/12/2026)

**Avancement** : **6/10** — HA M5 opérationnel, hardware van quasi complet, RPi 5 boot résolu (HAOS 18.3). Reste l'assemblage + capteurs Zigbee + intégration van (**deadline 15/12**).

---

## ⚠️ Re-vérification du 2026-10-22

Ce résumé a été **re-vérifié** après une première passe erronée (lecture des
`executive-summary.md` datés de juillet au lieu des thread files à jour).
4 notes corrigées : ARTEON 4→3, WILDNEXUS 3→5, PHOTO_NATURE 8→7, TRAVELS 4→7.
VETALYX 4→6 (voir son entrée). Détail : `2026-10-22_dobby_reverification-projets.md`.

**Trois constats transverses** :

1. **Les thread files ne sont pas tenus à jour** — 4 projets sur 8 ont 3+ mois
   de retard (AI_TOOLS, ARTEON, PHOTO_AI_JURY : 03/07 ; WILDNEXUS : 05/07).
2. **`07_TRAVELS` n'a aucun thread file** malgré 729 fichiers — le projet le
   plus volumineux est le moins piloté.
3. **Trois deadlines contradictoires pour l'IOT Van** : 1er novembre (thread),
   7 août (thread, vue d'ensemble), 15 décembre (etat-projets.md du 19/10).

---

## Notes transverses

- **Chaîne photo** : `PHOTO_NATURE` → `PHOTO_AI_JURY` → `ARTEON` → `WildLens`.
- **Dépendance** : `03_WILDNEXUS` est bloqué tant que le P0 `11_IOT` (bench + hardware) n'avance pas.
- **Priorités courantes** : `11_IOT` (deadline dure 15/12) et `08_VETALYX` (juridique).

*Source : `etat-projets.md` (MAJ 2026-10-19), executive summaries et arborescence des dossiers.*
