# Analyse & Plan de Réorganisation — WildNexus
> Dobby 🦉 — synthèse multi-spécialistes (Bouvier, Castor, Sybil)
> 2026-06-19

---

## 1. Diagnostic — Ce qui va bien

La fondation documentaire de WildNexus est **solide et cohérente** :
- **P0 Scope Lock** (v0.2, 2026-05-23) — verrou de périmètre clair : nœud caméra autonome uniquement
- **Master Architecture** (706 lignes) — vision P0→P1→P2, architecture hiérarchisée, variantes BASIC/ADVANCED
- **Founding Document** (831 lignes) — document fondateur complet avec cartographie des responsabilités
- **14 ADRs** — décisions architecturales documentées (MCU, caméra IR, LoRa, stockage, énergie, boîtier IP67, sécurité/RGPD, provisioning, tests, acoustique)
- **INDEX.md** — navigation claire, explicitement structuré

Le périmètre P0 est verrouillé. La structure 00-08 est logique. La gouvernance est documentée.

## 2. Diagnostic — Ce qui dérive

### 2.1 Sous-projets absorbés dans 06_COMPONENTS/

| Sous-projet | Taille | Statut selon Scope Lock | Problème |
|-------------|--------|------------------------|----------|
| **BIOACOUSTIC/** | ~100+ fichiers, sous-dossiers INSECTNET, hardware, raw_audio, data, Reverse Birdsong | P1 deferred | Projet complet "Faune Autour - Radar de Biodiversité Acoustique" avec son propre Document Unique de Projet. N'a rien à faire dans WildNexus P0. |
| **FAUNE_AUTOUR_APP/** | source/, docs/, assets/, README | Adjacent ou P2 | Projet gelé séparé listé dans etat-projets.md mais son code vit DANS WildNexus |
| **ESP-DIVE/** | Sous-marin RC ESP32 | Exploration hardware | Intéressant pour waterproofing/énergie mais pas un sous-projet WildNexus |

### 2.2 08_TECH_NOTES/ — fourre-tout

12 fichiers mélangent :
- BirdNET webinar → bioacoustique, pas P0
- Insectes vol → entomologie générale
- ESP32-CAM lens hack → hardware hacking
- Transcript "L'IA code les ESP32" → veille technologique
- RPi-ZTE-Proximus LTE → connectivité IoT
- Audio "Ingénierie extrême WildNexus et VanMaison" → réflexion personnelle JCH

### 2.3 07_AGENTS/ — briefs hors scope

10+ briefs d'agents dont certains sont hors WildNexus :
- `brief-renard_relance-garantie-van` → projet Van/Camping, pas WildNexus
- Certains briefs sont redondants avec TEAM_Inbox/

### 2.4 05_VISUALS_DASHBOARDS/ — mélange data

Les CSV PPK2 (4 fichiers) sont des données de mesure hardware, pas des visuels.

### 2.5 Bioacoustique partout

Le sujet bioacoustique est éparpillé :
- 06_COMPONENTS/BIOACOUSTIC/ (projet complet)
- 08_TECH_NOTES/ (BirdNET webinar, insectes vol)
- TEAM_Inbox/ (briefs Chouette, Clio, recherche Lucio Arese, Zoom F3)
- ADR-013 (couche acoustique microphones P0)

## 3. Propositions de sous-projets à extraire

### 3.1 NEXUS_ACOUSTIC — Projet bioacoustique autonome

**À extraire de WildNexus → projet séparé** (comme InsectNet l'a été).

Contenu :
- Tout `06_COMPONENTS/BIOACOUSTIC/` → `03_PROJECTS/12_NEXUS_ACOUSTIC/`
- Sous-dossier INSECTNET déjà existant → pont naturel avec le projet InsectNet
- `08_TECH_NOTES/2026-05-25_analyse_BirdNET_webinar_WildNexus_InsectNet.md`
- `08_TECH_NOTES/Insectes vol.md`
- `08_TECH_NOTES/yt_birdweather-puck-field-workflow.md`
- Briefs TEAM_Inbox liés (Chouette, Clio)
- Recherche Lucio Arese 3D sonogram → documentation
- Recherche Zoom F3 + LOM MikroUši → procurement

**Spécialistes :** Clio 🐬 (scientifique), Chouette 🦉 (DSP), Musaraigne (Edge AI)

### 3.2 FAUNE_AUTOUR — Extraction propre

**Extraire de WildNexus → `03_PROJECTS/FAUNE_AUTOUR/`** (ou archiver si gelé).

Contenu :
- Tout `06_COMPONENTS/FAUNE_AUTOUR_APP/` → projet dédié

### 3.3 ESP-DIVE — Archive technique

**Archiver dans WildNexus** comme référence hardware (waterproofing, power management).

Contenu :
- `06_COMPONENTS/ESP-DIVE/` → `03_P0_ENGINEERING/99_REFERENCES/ESP-DIVE/`

## 4. Plan de réorganisation

### 4.1 Structure cible

```
03_WILDNEXUS/
├── 00_GOVERNANCE/          # inchangé
├── 01_FOUNDATION/          # inchangé
├── 02_DECISIONS/           # inchangé
├── 03_P0_ENGINEERING/
│   ├── 00_INDEX/
│   ├── 01_ARCHITECTURE_SYSTEME/
│   ├── 02_HARDWARE_SATELLITE/
│   ├── 03_ENERGIE_AUTONOMIE/
│   ├── 04_CONNECTIVITE_MESH_LORA_LTE/
│   ├── 05_SIMULATION/
│   ├── 07_PROCUREMENT_BOM/
│   ├── 08_BUDGET_MODELES/
│   ├── 09_BENCHMARKS_PRODUITS/
│   ├── 10_PROTOCOLES/          # renommé (ex-PROTOCOLES)
│   ├── 98_TEMPLATES_REGISTERS/
│   └── 99_REFERENCES/          # nouveau : tout ce qui est référence externe
│       ├── ESP-DIVE/
│       ├── datasheets/
│       └── veille/
├── 05_VISUALS_DASHBOARDS/  # nettoyé : CSV PPK2 → 03_P0_ENGINEERING
├── 06_COMPONENTS/          # devient 06_ADJACENT/ — uniquement ponts vers autres projets
│   └── README.md            # explique où trouver NEXUS_ACOUSTIC, FAUNE_AUTOUR, etc.
├── 07_AGENTS/              # nettoyé : briefs hors-scope archivés
├── 08_TECH_NOTES/           # reclassé : bioacoustique → NEXUS_ACOUSTIC, veille → 99_REFERENCES
├── INDEX.md                # mis à jour
└── Start.md                # mis à jour
```

### 4.2 Mapping before → after

| Avant | Après | Raison |
|-------|-------|--------|
| `06_COMPONENTS/BIOACOUSTIC/` | `03_PROJECTS/12_NEXUS_ACOUSTIC/` | Projet distinct P1 |
| `06_COMPONENTS/FAUNE_AUTOUR_APP/` | `03_PROJECTS/FAUNE_AUTOUR/` | Projet gelé distinct |
| `06_COMPONENTS/ESP-DIVE/` | `03_P0_ENGINEERING/99_REFERENCES/ESP-DIVE/` | Référence hardware |
| `06_COMPONENTS/PPK2/` | `03_P0_ENGINEERING/99_REFERENCES/PPK2/` | Outil de mesure |
| `06_COMPONENTS/Inventaire Technique*.md` | `03_P0_ENGINEERING/99_REFERENCES/` | Logistique |
| `06_COMPONENTS/2026-05-*_procurement*.md` | `03_P0_ENGINEERING/07_PROCUREMENT_BOM/` | Doublons procurement |
| `05_VISUALS_DASHBOARDS/ppk-*.csv` | `03_P0_ENGINEERING/03_ENERGIE_AUTONOMIE/mesures/` | Données de mesure |
| `08_TECH_NOTES/2026-05-25_analyse_BirdNET*` | → `12_NEXUS_ACOUSTIC/` | Bioacoustique |
| `08_TECH_NOTES/Insectes vol.md` | → `12_NEXUS_ACOUSTIC/` | Bioacoustique |
| `08_TECH_NOTES/yt_birdweather*` | → `12_NEXUS_ACOUSTIC/` | Bioacoustique |
| `08_TECH_NOTES/ESP32-Cam M12 Lens Hack.pdf` | `03_P0_ENGINEERING/99_REFERENCES/` | Hardware ref |
| `08_TECH_NOTES/yt_ai-wildlife-monitoring*` | `03_P0_ENGINEERING/99_REFERENCES/veille/` | Veille |
| `08_TECH_NOTES/L_ingénierie_extrême*.m4a` | Archive personnelle JCH | Audio réflexion |
| `07_AGENTS/brief-renard_relance-garantie-van*` | `03_PROJECTS/07_TRAVELS/` ou archive | Hors WildNexus |

### 4.3 Renommage 06_COMPONENTS → 06_ADJACENT

Le dossier `06_COMPONENTS` porte à confusion — il suggère des composants DU projet, alors qu'il contient des projets ADJACENTS. Renommer en `06_ADJACENT` avec un README qui liste :
- NEXUS_ACOUSTIC → `../12_NEXUS_ACOUSTIC/`
- FAUNE_AUTOUR → `../FAUNE_AUTOUR/`
- ESP-DIVE (archive référence) → `../03_P0_ENGINEERING/99_REFERENCES/ESP-DIVE/`

## 5. Gouvernance recommandée

| Sous-projet | Spécialiste primaire | Rôle |
|-------------|---------------------|------|
| **WildNexus P0** (caméra autonome) | Forge ⚒️ + Nova 🌟 | Hardware + Firmware + Test harness |
| **WildNexus P0** (énergie) | Fourmi 🐜 + Bruno 🐻 | Mesures PPK2, modèle autonomie, BOM |
| **WildNexus P0** (capteurs/boîtier) | Araignée 🕷️ | Intégration, IP67, connectique |
| **WildNexus P0** (terrain) | Chouette 🦉 | Déploiement, test terrain |
| **NEXUS_ACOUSTIC** (P1) | Clio 🐬 | Science bioacoustique, standards |
| **NEXUS_ACOUSTIC** (P1) | Chouette 🦉 | DSP, microphones, spectrogrammes |
| **NEXUS_ACOUSTIC** (P1) | Musaraigne 🐭 | Edge AI, classification embarquée |
| **FAUNE_AUTOUR** | ⚪ Gelé | Pas d'assignation active |

## 6. Prochaines étapes

1. ✅ Validation JCH de cette analyse
2. Création `03_PROJECTS/12_NEXUS_ACOUSTIC/` + extraction
3. Extraction FAUNE_AUTOUR → son propre dossier
4. Nettoyage 08_TECH_NOTES, 06_COMPONENTS, 05_VISUALS
5. Mise à jour INDEX.md, etat-projets.md, MEMORY.md
6. Mise à jour des fichiers pointeurs (AGENTS.md, CLAUDE.md, DEEPSEEK.md, GEMINI.md, QWEN.md)
7. **Arbor analysis** du projet WildNexus master → MVP → flagship (demandé par JCH)

---

*Préparé par Dobby 🦉 avec analyse structurelle (Bouvier), taxonomique (Castor) et mémorielle (Sybil).*
