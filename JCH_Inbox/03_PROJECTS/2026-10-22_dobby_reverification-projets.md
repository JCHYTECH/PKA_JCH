# Re-vérification des 7 projets restants

> 2026-10-22 · Dobby 🦉 · seconde passe après la correction VETALYX
> Méthode : arborescence réelle + **thread files** (source de vérité), pas les
> `executive-summary.md` datés de juillet.

---

## Résumé des corrections

| Projet | Ancienne note | **Note révisée** | Écart |
|---|---|---|---|
| 01_AI_IT_TOOLS | 8/10 | **8/10** | ✅ juste |
| 02_ARTEON | 4/10 | **3/10** | −1 (pire que noté) |
| 03_WILDNEXUS | 3/10 | **5/10** | +2 (sous-évalué) |
| 05_PHOTO_AI_JURY | 7/10 | **7/10** | ✅ juste |
| 06_PHOTO_NATURE | 8/10 | **7/10** | −1 (bug bloquant découvert) |
| 07_TRAVELS | 4/10 | **7/10** | +3 (très sous-évalué) |
| 11_IOT | 6/10 | **6/10** | ✅ juste |

---

## 01_AI_IT_TOOLS — 8/10 (confirmé)

**Réalité mesurée** : 117 fichiers `.md`, 34 skills, **126 scripts Python**,
57 binaires `bin/`, plus les 4 livrables d'aujourd'hui (memory-review,
mcp_guard, llm_trace, memory_eval, memory_export).

Le thread file date du 03/07 mais l'activité réelle est quotidienne et
documentée dans `outils-index.md` (mis à jour aujourd'hui).

**Pas 10 car** : le thread file n'est pas tenu à jour (03/07 vs 22/10), et
certains scripts sont des prototypes non testés en production.

---

## 02_ARTEON — 3/10 (déclassé)

**Le thread file confirme le blocage, et c'est pire que noté :**
- WildLens édition #1 matérialisée, **#2 = template vide** — *« 0 édition depuis 3 mois »* (constat du 03/07, donc 6 mois aujourd'hui)
- Shopify : ⏳ V1 à préparer (rien)
- WhiteWall : ⏳ intégration à configurer (rien)
- L'Instant Lu : ⏳ backend à construire (rien)
- Roadmap : **13 étapes → 5 ✅, 7 ⏳, 1 🔴**

**Ce qui existe** : 45 fichiers, charte de marque livrée (étape 4/13),
10 Mo de contenu. La matière est là — l'exécution est arrêtée.

**Pas 2 car** : la charte et l'édition #1 existent réellement.
**Pas 4 car** : 7 étapes sur 13 sont vides depuis juillet.

---

## 03_WILDNEXUS — 5/10 (rehaussé de +2)

**Réalité bien plus avancée que mon « 3/10 gelé » :**
- **225 fichiers, 218 Mo** — le plus gros projet du workspace
- **17 ADRs** (14 acceptés, 1 sous réserve, 2 proposés)
- Hardware **entièrement reçu** : PPK2, ESP32-S3, ESP32-CAM, OV5640,
  Mouser #39492997, Miuzei, MP1584 ×5, SPH0645LM4H-B ×2
- **24 protocoles/SOPs** documentés
- **SOP-01/02/03 exécutées avec résultats** (PPK2, deep sleep mesuré, CSV)
- 3 sous-projets structurés : WILDNEXUS (device), INSECTNET (orthoptères),
  NEXUS_ACOUSTIC (oiseaux/amphibiens)

**Le vrai blocage est ciblé, pas global** : panier Mouser **~279 €** non
commandé débloque LoRa (SOP-07) et le payload spectral (SOP-16). Et
SOP-13 (I2S) *« peut démarrer dès que le pinout est mappé — pas bloqué par
Mouser »*.

**Pas 7 car** : phases D et E du banc M-02 en attente, firmware repo à créer,
et rien n'est encore en production terrain.

---

## 05_PHOTO_AI_JURY — 7/10 (confirmé)

**Thread à jour (03/07) confirme** : 58 analyses, 73.8/100, 81 % d'acceptation,
prompt calibré du 14/06. MCP Lightroom **partiellement installé** — il manque
« Start Server ».

Seulement 5 fichiers `.md` mais **82 Mo** : l'essentiel est dans
`argus_critique.db` et les PDF d'analyses.

**Pas 8 car** : le MCP Lightroom n'est pas activé, donc pas d'intégration
automatisée au flux de travail.

*(Note : c'est ce projet qui a reçu aujourd'hui l'outil de détection IA, en
niveau 1 seulement.)*

---

## 06_PHOTO_NATURE — 7/10 (déclassé de −1)

**Réalité** : 168 fichiers `.md`, 4.4 Mo. Keyworder IA (Gemma4 local,
62 catégories), 11 presets Argus, cross-réfs ARTEON, impression ET8550
documentée, guides terrain (focus stacking, macro).

**Pourquoi je baisse** : la session d'aujourd'hui a révélé un **bug bloquant
préexistant** — `UnboundLocalError` sur `headline` faisait planter chaque photo
en mode normal, tout en écrivant correctement les keywords. Le keyworder
« fonctionnait » mais signalait un échec systématique.

**Pas 8 car** : ce bug, plus l'absence de retour visuel (corrigé aujourd'hui
en partie) et le geste manuel Lightroom toujours présent.

---

## 07_TRAVELS — 7/10 (rehaussé de +3, le plus gros écart)

**Mon « 4/10 gelé » était très loin du réel.** Mesures :

- **729 fichiers `.md`** — le plus grand volume documentaire du workspace
- **726 Mo** au total
- **pka-decouvertes : 647 lieux validés** + **590 en file d'attente**
- 11 `spots_van` (bivouacs), 9 circuits, 12 mymaps, 11 rapports
- `lupo-planner-import.json` : **191 Ko** d'import généré
- 2 voyages réalisés documentés (Italie 21/08–19/09, Wadden 30/06)
- Lupo Planner + pipeline DÉCOUVERTES opérationnels

**C'est un projet qui tourne**, pas un projet gelé. Le seul manque structurel :
**aucun thread file** (`thread-travels.md` absent) alors que tous les autres
projets en ont un.

**Pas 8 car** : pas de thread file, et 590 éléments en queue = arriéré de
traitement.

---

## 11_IOT — 6/10 (confirmé)

**Thread à jour (05/10), très détaillé.** Écarts avec mon résumé :

- **RPi 5 boot résolu** ✅ HAOS **18.3**, Supervisor+Core à jour, Healthy
- **NVMe retiré** définitivement — SD seule (décision)
- **Alim : décision X1205 → Geekworm X1200** (achat différé, ~50-70 €)
- **RUT240 Teltonika (4G) en stock** — remplace le ZTE, à intégrer
- WiCAN Pro **installé**, SNZB-02DR2 **appairé** (07/10)
- Reste : **7 capteurs ~88 €** + silentblocs + coating

**Incohérence dans le thread** : l'en-tête dit *« deadline 1er novembre 2026 »*
mais la vue d'ensemble dit *« deadline 7 août »* et *« priorité absolue jusqu'au
7 août »* — deux deadlines contradictoires. `etat-projets.md` (19/10) dit
**15 décembre**. Trois dates pour un même jalon.

**Pas 7 car** : l'installation physique dans le van n'est pas faite, et
la deadline est floue.

---

## Points transverses découverts

**1. Les thread files ne sont pas tous à jour**
- 01_AI_IT_TOOLS : 03/07 (3,5 mois de retard)
- 02_ARTEON : 03/07
- 05_PHOTO_AI_JURY : 03/07
- 03_WILDNEXUS : 05/07
- 11_IOT : **05/10** ✅
- 08_VETALYX : **06/10** ✅
- 07_TRAVELS : **absent**

→ Le skill `pka-thread-file` dit « mis à jour automatiquement en fin de
session », mais 4 projets sur 8 ont 3+ mois de retard.

**2. Trois deadlines contradictoires pour l'IOT Van**
`1er novembre` (thread) / `7 août` (thread, vue d'ensemble) / `15 décembre`
(etat-projets.md du 19/10).

**3. 07_TRAVELS n'a pas de thread file** malgré 729 fichiers — le projet le
plus volumineux est le moins piloté.

---

## Classement révisé (8 projets)

| Rang | Projet | Note |
|---|---|---|
| 1 | 01_AI_IT_TOOLS | 8/10 |
| 2 | 05_PHOTO_AI_JURY | 7/10 |
| 3 | 06_PHOTO_NATURE | 7/10 |
| 4 | 07_TRAVELS | 7/10 |
| 5 | 11_IOT | 6/10 |
| 6 | 08_VETALYX | 6/10 |
| 7 | 03_WILDNEXUS | 5/10 |
| 8 | 02_ARTEON | 3/10 |

**Moyenne : 6,1/10**

---

## Recommandations immédiates

1. **Créer `thread-travels.md`** — 729 fichiers sans fil conducteur, c'est le
   trou le plus béant.
2. **Trancher la deadline IOT** — trois dates circulent, une seule doit rester.
3. **Mettre à jour 4 thread files** (AI_TOOLS, ARTEON, PHOTO_AI_JURY, WILDNEXUS).
4. **Vider la queue DÉCOUVERTES** — 590 éléments en attente, 647 déjà validés.
5. **Commander le panier Mouser (279 €)** — débloque deux SOPs WildNexus pour
   un coût marginal.

*Sources : thread files des 8 projets · arborescences complètes · progress.md
WildNexus · etat-projets.md (19/10) · mesures `du`/`find` du 2026-10-22.*
