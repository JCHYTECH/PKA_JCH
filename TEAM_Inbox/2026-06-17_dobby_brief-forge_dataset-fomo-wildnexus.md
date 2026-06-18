# BRIEF — [[Musaraigne]] 🐭 — 2026-06-17 (réassigné de [[Forge]])

**PRIORITY :** high  
**DEADLINE :** 2026-06-30 (proto) / 2026-07-15 (déployable)

---

## MISSION

Constituer un dataset annoté animal/pas-animal pour entraîner un modèle **FOMO binaire** sur ESP32-S3, compatible **Edge Impulse**, ciblant la faune forestière belge.

---

## CONTEXTE

WildNexus utilise une architecture PIR (EKMB) → wake ESP32-S3 → TinyML confirmation → capture OV5640. Le modèle FOMO doit réduire les faux déclenchements PIR (vent, branches, feuillage) en validant la présence animale avant capture. Sans ce dataset, le firmware ne peut pas faire de détection on-device et consomme inutilement.

---

## ENTRÉES DISPONIBLES

- Synthèse OpenRouter Auto : `TEAM_Inbox/2026-06-17_dobby_openrouter-deepdive_wildnexus.md` (§2 TinyML)
- Datasets publics recommandés :
  - **LILA BC** (hub central de datasets pièges photo)
  - **Wildlife Insights** (projets Europe, accès académique)
  - **Caltech Camera Traps** (243K images, bon pour pré-entraînement)
  - **iNaturalist** (6 espèces cibles, complément morphologique)
- Pipeline firmware : Arduino CLI 1.5.1 + ESP32 core 3.3.9 (installé M5)
- BOM v0.3 : PIR EKMB §11 (22,30€), ESP32-S3, OV5640 déjà provisionnés
- SOP M-02 (Metrology) : workflow validation trigger

---

## LIVRABLE ATTENDU

1. **Dataset annoté** (2 000–3 000 images minimum) au format Edge Impulse :
   - 50% animal (chevreuil, sanglier, [[renard]], blaireau, écureuil, oiseaux forestiers)
   - 50% pas-animal (forêt vide, branches, pluie, brouillard, contre-jour)
   - Split train/val/test : **70/15/15 par site/caméra** — pas par image !
2. **Projet Edge Impulse** créé avec le dataset uploadé
3. **Fichier `README_dataset.md`** documentant : sources, volumes, split, limites connues
4. **Brief de retour** dans `TEAM_Inbox/` avec benchmark latence FOMO sur ESP32-S3

---

## CONTRAINTES

- Classification **binaire uniquement** (pas de multi-espèces en P0)
- Images 320×240 ou 96×96 (FOMO natif)
- Licence : préférer CC-BY ou académique pour les datasets publics
- Le dataset public est une base — les images terrain de JC (Ardenne) viendront en phase 2
- Ne pas briffer [[Nova]]/[[Miel]]/[[Vasco]] (veille active) sans accord JCH

---

## INTERACTIONS

- **JC** → fournira 500+ images de fond forêt Ardenne (phase 2, après prototype)
- **[[Chouette]]** → confirmer compatibilité caméra OV5640 avec la résolution FOMO
- **[[Dobby]]** → intégrera le dataset dans SOP M-02 après validation
