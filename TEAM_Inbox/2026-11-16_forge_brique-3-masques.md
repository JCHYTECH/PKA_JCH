---
date: 2026-11-16
source: forge
domain: arteon
type: rapport
status: à valider JC
lang: fr
---

# Brique 3 — Masques IA animaliers : décision de montée MCP, code prêt à tester, procédure

> Forge ⚒️ pour JC — 2026-11-16.
> Entrée : `JCH_Inbox/03_PROJECTS/02_ARTEON/strategy/brique-3-masques-ia-design.md`.
> Contexte croisé : `strategy/2026-11-16_probleme-colorgrade-sdk-lightroom.md` (résolu B).
>
> **Aucune modification de `_local/lightroom-mcp/` n'a été faite.** Aucune commande destructive,
> aucun achat, aucune interaction Lightroom. Le code ci-dessous est **non exécuté** : il est prêt,
> pas validé. Tout ce qui est affirmé sur les deux versions est vérifié sur pièces (fichiers locaux,
> npm, sources upstream) — les points non vérifiables sont marqués « À VALIDER ».

---

## 0. Résumé exécutif

1. **La montée est justifiée et techniquement possible, mais pas par un `git pull`.** La 0.27.0 a
   réarchitecturé le serveur (toolsets, bridge/broker, previews, 72 outils) ; la copie locale porte
   du travail non commité (5 fichiers modifiés + 5 scripts) qui serait écrasé. Verdict : **worktree
   séparé + swap unique du plugin**, puis port de 3 clés en patch (voir §1.5).
2. **La montée règle la brique 3 entièrement** : 15 outils de masquage, dont `combine_mask`
   (`add` / `subtract` / **`intersect`**) = exactement le primitif « sujet ∩ X » du design §2.
3. **Elle ne règle pas les roues Color Grading** (toujours absentes de l'allowlist upstream) et
   **elle fait régresser la brique 1** : `SplitToning*` n'est pas dans la liste upstream, donc les
   presets Naturaliste perdraient leur grading. Les clés `ToneCurvePV2012*` ne sont pas dans la
   liste non plus (contrairement à ce qu'annonce le design §5) — seulement dans
   `POINT_CURVE_SETTING_KEYS`.
4. **Contrainte dure à accepter avant tout code** : les écritures de masques sont **gated LrC 15.6 /
   process version 15.4** en dur (`TESTED_LIGHTROOM_VERSIONS`). Si le LrC de JC n'est pas 15.6, la
   brique 3 ne passe pas par MCP.
5. Le primitif « sujet ∩ pinceau » **n'existe pas comme un seul appel** : il s'obtient en deux temps
   (pinceau d'abord, puis `combine_mask` `intersect` `subject`), et Lightroom stocke l'intersection
   **inversée** (`inverted: true` au `list_masks`) — c'est le piège n°1 du chantier.

---

## 1. Évaluation de la montée 0.4.1 → 0.27.0

### 1.1 État réel de la copie locale (vérifié)

- `_local/lightroom-mcp/server/package.json` → `"version": "0.4.1"`.
- C'est un **clone git imbriqué** (`.git/` répertoire), pas un submodule enregistré : pas de
  `.gitmodules` dans PKA_JCH, mais le dépôt parent suit un pointeur (`M _local/lightroom-mcp`).
  Conséquence : un commit interne doit être accompagné d'un commit du pointeur parent.
- **Arbre de travail sale** (le point qui décide de la stratégie de montée) :
  - modifiés : `plugin/LightroomMCP.lrplugin/HandlerDevelop.lua`, `HandlerMetadata.lua`,
    `PhotoLookup.lua`, `server/src/tool-contracts.ts`, `tests/e2e/mcp-runner.mjs` ;
  - non suivis : `scripts/apply_strength.mjs`, `scripts/avant-apres.mjs`, `scripts/looks.mjs`,
    `scripts/strength_server.mjs`, `tests/strength-sweep/`.
- Le travail local **n'est pas cosmétique** : `tool-contracts.ts` et `HandlerDevelop.lua` ajoutent
  ~40 clés SDK (courbes de points `ToneCurvePV2012*`, TSL `*Adjustment*`, `ColorGrade*`,
  `SplitToning*`) et `apply_develop_preset` gagne `preset_amount` (0–200).
- **Outils locaux : 14.** Aucun outil de masquage, aucun `create_develop_preset`.

### 1.2 Ce que contient réellement 0.27.0 (vérifié)

Source : `registry.npmjs.org/@mskalski/lightroom-mcp/latest` (0.27.0, `gitHead c6551e2`, publié,
provenance SLSA) + `server/src/tool-contracts.ts`, `toolsets.ts`, `cli.ts`, `index.ts`, `plugin/*`
sur `main`.

- **72 contrats d'outils** répartis en **3 toolsets** : `core`, `develop`, `masks`.
  Défaut = `core` seul → **les masques n'apparaissent que si `LIGHTROOM_MCP_TOOLSETS=masks` (ou
  `all`) est exporté**. Point de config à ne pas oublier.
- Nouvelles variables d'environnement : `LIGHTROOM_MCP_TOOLSETS`, `LIGHTROOM_MCP_READ_ONLY` (masque
  et refuse les écritures), `LIGHTROOM_MCP_TOKEN_PATH`, ports séparés
  `LIGHTROOM_MCP_REQUEST_PORT` / `LIGHTROOM_MCP_RESPONSE_PORT`.
- **Toolset `masks` — 15 outils** : `list_masks`, `get_mask`, `create_mask`, `create_mask_batch`
  (≤ 200 photos), `create_gradient_mask`, `update_gradient_mask`, `create_brush_mask`,
  `add_brush_strokes`, `create_range_mask` (luminance / **color** / depth), `delete_masks`,
  `set_mask_adjustments`, `invert_mask`, `set_mask_curves` (courbe locale 4 canaux),
  `edit_mask_point_colors` (Point Color local, 8 échantillons), **`combine_mask`**
  (`add` | `subtract` | `intersect`).
- **Toolset `develop` enrichi** : `create_develop_preset` (checkpoint de réglages *develop*, pas de
  masque), `get_develop_preset`, `compare_develop_presets`, `export_develop_preset`,
  `apply_develop_preset` avec `preset_uuid`, `dry_run` et **recalcul des masques IA sur LrC 13.3+**,
  snapshots, `apply_auto_adjustments`, `set_lens_blur`, `match_photo_style`.
- Infra : `Bridge`/`broker`, heartbeat, lock d'instance, `install-plugin` automatique
  (`~/Library/Application Support/Adobe/Lightroom/Modules/LightroomMCP.lrplugin`), paquet `.mcpb`.
- Dépendances : Node ≥ 20, `@modelcontextprotocol/server ^2.4.0`, `jpeg-js`, `ajv`.

### 1.3 Ce que la montée règle — et ce qu'elle ne règle pas

Règle :

- les 4 masques du design §2 deviennent scriptables (sujet, fond, plage de luminance, plage de
  couleur) ;
- le primitif d'intersection existe (`combine_mask`) ;
- les réglages locaux par masque sont exposés (`set_mask_adjustments`, noms `local_*`) ;
- la recette « anti-coulée » a deux implémentations possibles (plage de couleur, ou Point Color
  local) ;
- la courbe locale par masque existe (`set_mask_curves`) — utile pour la sculpture de lumière (§4.2) ;
- `dry_run` permet de mesurer un preset sans écrire (utile à la brique 2 / avant-après).

Ne règle pas :

- **les roues Color Grading** : `ColorGradeShadowHue/Sat` et `ColorGradeHighlightHue/Sat` restent
  absentes de l'allowlist upstream. La substitution `SplitToning*` du 16/11 reste la seule voie ;
- **`preset_amount`** : disparu de `apply_develop_preset` upstream (remplacé par `dry_run`,
  `preset_uuid`, `preset_scope`). C'est une capacité **locale uniquement** — et le flux brique 1
  actuel (`looks.mjs` → `set_develop_settings`) ne l'utilise pas, donc la perte est théorique ;
- **les courbes de points en réglage global** : `ToneCurvePV2012*` est déclaré dans
  `POINT_CURVE_SETTING_KEYS` mais **pas** dans `DEVELOP_SETTING_KEYS`, alors que la description de
  `set_develop_settings` les annonce. Incohérence upstream : considérer ces clés comme non fiables,
  exactement le garde-fou du design. La courbe disponible et fiable en 0.27.0 est **paramétrique**
  (`Parametric*`) + **locale** (`set_mask_curves`).

### 1.4 Le vrai verrou : la version de Lightroom

`plugin/GuardedMaskWrite.lua` :

```lua
local TESTED_LIGHTROOM_VERSIONS = { ["15.6"] = true }
local TESTED_PROCESS_VERSIONS   = { ["15.4"] = true }
```

`GuardedMaskWrite.preflight()` appelle `requireTestedVersions(processVersion)` **avant toute
écriture** : hors 15.6 / PV 15.4, le plugin refuse et n'écrit rien. Ce n'est pas un avertissement,
c'est un mur. `create_mask_batch`, `create_brush_mask`, `create_range_mask`, `update_gradient_mask`
sont en plus documentés « Lightroom Classic 15.6 only » ; `set_mask_adjustments` et `combine_mask`
sont annoncés LrC 11+ (API `LrDevelopController.getAllMasks` / `selectTool` / `selectMask`).

Mécanique d'écriture (à connaître avant de signer) :

```lua
catalog:withWriteAccessDo(description, function()
    photo:applyDevelopSettings({ MaskGroupBasedCorrections = entries })
end)
```

puis lecture de contrôle, comparaison champ à champ, et **rollback** vers l'état précédent si un
écart est détecté. `MaskGroupBasedCorrections` **est** une clé officiellement ajoutée au SDK 11
(changelog Adobe « Changes to the Lightroom SDK 11 »), donc le garde-fou « pas de clé non
documentée » tient **au niveau de la clé racine**. Ce qui est reverse-engineered et non documenté,
c'est la **structure interne** de chaque correction (`What`, `CorrectionMasks`, `Mask/Paint.Dabs`,
`Mask/RangeMask.CorrectionRangeMask`…). D'où le gate de version et le guarded write.

→ **Décision de risque** : acceptable **parce que** l'écriture est gardée (preflight + read-back +
restore) et versionnée. Inacceptable si on l'expose à des utilisateurs sur une version non testée.

### 1.5 Verdict et options

**Verdict : GO sur la montée, en side-by-side, avec un patch de parité obligatoire.**

- **Option A — `git pull --rebase` dans `_local/lightroom-mcp` : NON.** Conflits garantis sur
  `tool-contracts.ts` (réécrit intégralement : `toolset`, `title`, `annotations` par contrat) et
  `HandlerDevelop.lua` (allowlist + `preset_amount`), et perte des scripts non suivis en cas de
  `git clean`. Risque élevé pour un gain nul : ces scripts n'ont pas besoin d'être dans le dossier
  upstream.
- **Option B — worktree séparé : OUI (recommandé).** `git worktree add ../lightroom-mcp-027 <sha>`
  laisse l'arbre local (sale) intact, donne un checkout propre en lecture/écriture, et se supprime
  d'un `git worktree remove`. Un seul dépôt, deux états.
- **Option C — clone nu séparé (`git clone --depth 1`) : acceptable** si on préfère une isolation
  totale (pas de `fetch` commun). Un cran moins élégant, même résultat.
- **Option D — attendre : NON.** Le verrou n'est pas la 0.27.0, c'est la version de Lightroom ; tant
  qu'elle n'est pas confirmée, aucune option n'avance. Le side-by-side permet justement de trancher
  en 10 minutes.

**Patch de parité à porter sur 0.27.0 (après validation brique 3), 3 ajouts seulement :**

1. `SplitToningShadowHue/Saturation`, `SplitToningHighlightHue/Saturation`, `SplitToningBalance`
   (+ éventuellement `ColorGradeBlending`) dans `server/src/tool-contracts.ts`
   (`DEVELOP_SETTING_KEYS`) **et** `plugin/LightroomMCP.lrplugin/HandlerDevelop.lua`
   (`ALLOWED_DEVELOP_SETTING_KEYS`) — sinon la brique 1 perd son grading ;
2. `preset_amount` dans le contrat `apply_develop_preset` + handler (optionnel, aucune dépendance
   actuelle) ;
3. `ToneCurvePV2012*` : **ne pas porter**. L'allowlist locale les accepte mais le SDK les droppe
   silencieusement (cf. doc colorgrade, point 3). Les garder serait une fausse capacité.

### 1.6 Diff / plan de montée (non appliqué — à exécuter après feu vert)

Aucune de ces commandes n'a été lancée. Elles sont écrites pour être rejouées telles quelles.

```bash
# 0) Sauvegarde du plugin 0.4.1 actuellement chargé (réversibilité)
[M5] cp -R "$HOME/Library/Application Support/Adobe/Lightroom/Modules/LightroomMCP.lrplugin" \
         "$HOME/PKA_JCH/_local/backup-LightroomMCP-0.4.1.lrplugin"

# 1) Récupérer l'upstream sans toucher l'arbre courant
[M5] cd "$HOME/PKA_JCH/_local/lightroom-mcp"
[M5] git fetch origin --tags
[M5] git log --oneline -1 origin/main          # attendu : c6551e2 (gitHead npm 0.27.0)

# 2) Checkout propre en worktree (l'arbre sale reste intact)
[M5] git worktree add ../lightroom-mcp-027 c6551e2
[M5] cd ../lightroom-mcp-027/server
[M5] npm ci && npm run build
[M5] node dist/index.js --version              # attendu : 0.27.0

# 3) Vérifier que le toolset masks répond AVANT d'installer le plugin
[M5] cd "$HOME/PKA_JCH/_local/lightroom-mcp-027/server"
[M5] LIGHTROOM_MCP_TOOLSETS=all node -e '
  const {spawn}=require("child_process");
  const p=spawn("node",["dist/index.js"],{stdio:["pipe","pipe","inherit"],env:{...process.env}});
  let buf="";p.stdout.on("data",d=>{buf+=d;
    const m=buf.match(/\{"jsonrpc".*\}/g)||[];
    for(const l of m){const o=JSON.parse(l);
      if(o.id===2){const t=JSON.parse(o.result.content?.[0]?.text||"{}");
        console.log("outils exposés:",t.tools?t.tools.length:"?");p.kill();}}});
  const send=o=>p.stdin.write(JSON.stringify(o)+"\n");
  send({jsonrpc:"2.0",id:1,method:"initialize",params:{protocolVersion:"2025-06-18",capabilities:{},clientInfo:{name:"probe",version:"0"}}});
  send({jsonrpc:"2.0",method:"notifications/initialized",params:{}});
  send({jsonrpc:"2.0",id:2,method:"tools/list",params:{}});
'

# 4) Installer le plugin 0.27.0 (remplace le 0.4.1 dans Modules)
[M5] node dist/index.js install-plugin

# 5) Dans Lightroom : File > Plug-in Manager > Lightroom MCP > Reload Plug-in, puis Start Server
#    (si « failed to open localhost:58763 » : quitter Lightroom complètement et rouvrir)

# Rollback intégral
[M5] rm -rf "$HOME/Library/Application Support/Adobe/Lightroom/Modules/LightroomMCP.lrplugin"
[M5] cp -R "$HOME/PKA_JCH/_local/backup-LightroomMCP-0.4.1.lrplugin" \
         "$HOME/Library/Application Support/Adobe/Lightroom/Modules/LightroomMCP.lrplugin"
[M5] cd "$HOME/PKA_JCH/_local/lightroom-mcp" && git worktree remove ../lightroom-mcp-027 --force
```

Note d'exploitation : **les deux serveurs ne peuvent pas tourner en même temps sur le même
Lightroom**. Le dossier Modules ne contient qu'un `LightroomMCP.lrplugin`, et les deux versions
visent les mêmes ports. Le swap est donc un aller-retour, pas une coexistence — sauf à dupliquer le
plugin sous un autre nom et à repatcher ses ports dans Plug-in Manager (faisable, non recommandé
pour un premier test).

---

## 2. Contraintes réelles du SDK (ce que le code peut faire)

### 2.1 Modèle d'objet

Un masque = un *groupe de corrections* (`MaskGroupBasedCorrections[]`) contenant des *composants*
(`CorrectionMasks[]`), chacun d'un type :

- `Mask/Image` — sélection IA (sujet, ciel, fond) : `tool.type = "aiSelection"`,
  `subtype = subject|sky|background` ;
- `Mask/Paint` — pinceau : `Dabs`, `Radius`, `Flow`, `CenterWeight` ;
- `Mask/RangeMask` — plage : `CorrectionRangeMask`, `SampleType` 1 = couleur, 2 = luminance,
  −1 = profondeur ;
- `Mask/Gradient`, `Mask/CircularGradient`, `Mask/Aggregate` (union de `Masks`).

`list_masks` renvoie :

```json
{ "success": true, "photo_id": "...", "count": 2,
  "masks": [ { "id": "…", "name": "Sujet", "hidden": false,
               "tools": [ { "id": "…", "type": "aiSelection", "subtype": "subject",
                            "inverted": false, "range": null } ] } ] }
```

### 2.2 L'intersection : deux appels, dans cet ordre

`combine_mask` ne prend **pas** un pinceau en entrée : il combine un composant **détecté**
(`subject`, `sky`, `background`) **dans** un masque existant.

```json
{ "photo_id": "…", "mask_id": "<masque pinceau>", "operation": "intersect", "type": "subject" }
```

Donc le primitif « sujet ∩ pinceau » = **pinceau d'abord**, intersection ensuite :

1. `create_brush_mask` → nouveau masque, `mask_id` + `tool_id` ;
2. `combine_mask { mask_id, operation: "intersect", type: "subject" }` → nouveau `tool_id` ;
3. `set_mask_adjustments { mask_id, adjustments: { local_Exposure: … } }`.

**Piège** : si on crée le masque sujet d'abord puis qu'on ajoute le pinceau via
`create_brush_mask { mask_id }`, le pinceau s'ajoute en **union** (élargit) — l'inverse de ce qu'on
veut. Et Lightroom stocke l'intersection comme un **soustrait inversé** (`inverted: true` au
`list_masks`). Toute retouche ultérieure du pinceau doit être vérifiée à l'overlay, pas supposée.

### 2.3 Le piège de la plage de couleur

`create_range_mask type=color` exige un échantillon `{ x, y, l, a, b }` où `l`, `a`, `b` sont les
**rangs internes** de Lightroom (0..1 : plus sombre→plus clair, vert→rouge, bleu→jaune), **pas du
sRGB, pas calculables depuis le RGB de l'image**. Deux voies seulement :

- `copy_sample_from { mask_id, tool_id }` — copier un échantillon créé une fois à la main dans l'UI
  (Tools > Create New Mask > Color Range). **Déterministe, recommandé.**
- fournir un rang à la main (ex. héron blanc sous ciel : `l ≈ 0.92`, `a ≈ 0.42`, `b ≈ 0.45`) —
  **hypothèse par photo**, à recalibrer.

`intersect` n'est **pas** supporté par `create_range_mask` (`mode: add | subtract` uniquement) →
même contournement : plage d'abord, puis `combine_mask intersect subject`.

---

## 3. Code prêt à tester

### 3.1 Fichier à déposer (après feu vert, hors du dépôt upstream)

Chemin proposé : `_local/brique3/brique3_masks.mjs` (à côté du clone, jamais dedans, pour ne pas
polluer le worktree 0.27.0). Lancer avec `LRM_MCP_ROOT` pointant sur `_local/lightroom-mcp-027`.

```js
#!/usr/bin/env node
/**
 * brique3_masks.mjs — brique 3 ARTEON/WildLens : 4 masques animaliers + recettes.
 *
 * Cible : lightroom-mcp >= 0.27.0, toolset `masks` (LIGHTROOM_MCP_TOOLSETS=all).
 * Exige Lightroom Classic 15.6 (process version 15.4) — gate dure côté plugin.
 *
 * Usage :
 *   LRM_MCP_ROOT=~/PKA_JCH/_local/lightroom-mcp-027 node brique3_masks.mjs inspect
 *   ... subject | background | eye --x .42 --y .31 | plumage --min .55 --max 1
 *   ... anticoulee --variant range --copy-from <maskId:toolId>
 *   ... stack            # enchaîne 1→4 sur l'état courant
 *   ... measure --before a.jpg --after b.jpg --rect .3,.2,.4,.5
 *
 * Sélection : photo courante de Lightroom, ou --photo-id <id>.
 * Pendant un run : ne pas toucher Lightroom (le plugin bascule le module Develop).
 */
import { spawn } from "node:child_process";
import { once } from "node:events";
import fs from "node:fs";
import path from "node:path";
import { createRequire } from "node:module";

const REPO = process.env.LRM_MCP_ROOT || path.resolve(process.cwd(), "lightroom-mcp-027");
const SERVER_BIN = path.join(REPO, "server", "dist", "index.js");
const PROTOCOLS = ["2025-06-18", "2024-11-05"];
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/* ---------------- Réglages par défaut — design §2 ----------------
 * Unités Lightroom : exposition en stops (-4..4), le reste -100..100,
 * temperature/tint LOCAUX = décalage -100..100 (pas des Kelvin).
 * Ces valeurs sont des POINTS DE DÉPART, à caler sur RAW réels (design §6.3).
 */
export const DEFAULTS = {
  sujet:      { exposure: 0.30, contrast: 12, highlights: -20 },
  oeil:       { exposure: 0.35, clarity: 20, sharpness: 35 },
  plumage:    { texture: 15, sharpness: 25, saturation: 5, highlights: -15 },
  fond:       { exposure: -0.25, texture: -15, clarity: -5, temperature: -6, tint: 0 },
  anticoulee: { saturation: -45, temperature: 10, tint: 2 },
};

const LOCAL = {
  exposure: "local_Exposure", contrast: "local_Contrast", highlights: "local_Highlights",
  shadows: "local_Shadows", whites: "local_Whites", blacks: "local_Blacks",
  texture: "local_Texture", clarity: "local_Clarity", dehaze: "local_Dehaze",
  temperature: "local_Temperature", tint: "local_Tint", saturation: "local_Saturation",
  sharpness: "local_Sharpness", noise: "local_LuminanceNoise",
};
const toLocal = (adj) => Object.fromEntries(
  Object.entries(adj).map(([k, v]) => [LOCAL[k] ?? k, v]));

/* ---------------- Client MCP stdio minimal ---------------- */
class Mcp {
  constructor() { this.proc = null; this.buf = ""; this.next = 1; this.pending = new Map(); }

  async start() {
    this.proc = spawn("node", [SERVER_BIN], {
      stdio: ["pipe", "pipe", "pipe"],
      env: { ...process.env, LIGHTROOM_MCP_TOOLSETS: process.env.LIGHTROOM_MCP_TOOLSETS || "all" },
    });
    this.proc.stdout.setEncoding("utf8");
    this.proc.stderr.setEncoding("utf8");
    this.proc.stderr.on("data", (d) => process.env.LRM_DEBUG && process.stderr.write(d));
    this.proc.stdout.on("data", (c) => { this.buf += c; this._drain(); });
    this.proc.on("exit", (code) => {
      for (const { reject } of this.pending.values()) reject(new Error(`server exited ${code}`));
      this.pending.clear();
    });

    let lastErr;
    for (const protocolVersion of PROTOCOLS) {
      try {
        await this._rpc("initialize", {
          protocolVersion, capabilities: {},
          clientInfo: { name: "brique3-masks", version: "0.1.0" },
        }, 15000);
        lastErr = null; break;
      } catch (e) { lastErr = e; }
    }
    if (lastErr) throw lastErr;
    this._notify("notifications/initialized", {});

    const deadline = Date.now() + 20000;
    while (Date.now() < deadline) {
      try {
        const r = await this._rpc("tools/call", { name: "list_masks", arguments: {} }, 4000);
        if (!r.isError) return;              // plugin prêt (toolset masks exposé)
      } catch { /* pas encore */ }
      await sleep(400);
    }
    throw new Error("plugin non prêt : Reload Plug-in + Start Server faits ? toolset `masks` exposé ?");
  }

  _drain() {
    let i;
    while ((i = this.buf.indexOf("\n")) !== -1) {
      const line = this.buf.slice(0, i).trim(); this.buf = this.buf.slice(i + 1);
      if (!line) continue;
      let m; try { m = JSON.parse(line); } catch { continue; }
      if (m.id != null && this.pending.has(m.id)) {
        const { resolve, reject } = this.pending.get(m.id); this.pending.delete(m.id);
        m.error ? reject(new Error(JSON.stringify(m.error))) : resolve(m.result);
      }
    }
  }
  _send(o) { this.proc.stdin.write(JSON.stringify(o) + "\n"); }
  _notify(method, params) { this._send({ jsonrpc: "2.0", method, params }); }
  _rpc(method, params, timeout = 60000) {
    const id = this.next++;
    const p = new Promise((resolve, reject) => {
      const t = setTimeout(() => { this.pending.delete(id); reject(new Error(`timeout ${method}`)); }, timeout);
      this.pending.set(id, {
        resolve: (v) => { clearTimeout(t); resolve(v); },
        reject: (e) => { clearTimeout(t); reject(e); },
      });
    });
    this._send({ jsonrpc: "2.0", id, method, params });
    return p;
  }
  async call(name, args = {}, timeout = 120000) {
    const r = await this._rpc("tools/call", { name, arguments: args }, timeout);
    const text = r?.content?.[0]?.text ?? "";
    let parsed; try { parsed = JSON.parse(text); } catch { parsed = { raw: text }; }
    if (r?.isError) throw new Error(`${name}: ${text}`);
    return parsed;
  }
  async stop() {
    if (!this.proc) return;
    this.proc.stdin.end();
    try { await Promise.race([once(this.proc, "exit"), sleep(1500)]); } catch {}
    if (this.proc.exitCode === null) this.proc.kill("SIGKILL");
  }
}

/* ---------------- Résolution photo ---------------- */
async function resolvePhotoId(mcp, cli) {
  if (cli["photo-id"]) return String(cli["photo-id"]);
  const sel = await mcp.call("get_selected_photos", { limit: 1 });
  const arr = Array.isArray(sel) ? sel : (sel.photos ?? []);
  if (!arr.length) throw new Error("aucune photo sélectionnée dans Lightroom (ou --photo-id)");
  return String(arr[0].id ?? arr[0].path);
}

/* ---------------- Primitives ---------------- */
const maskId = (r) => String(r.mask_id ?? r.mask?.id ?? r.masks?.[0]?.id);

const createAiMask = (mcp, photoId, type, adjustments) =>
  mcp.call("create_mask", { photo_id: photoId, type, ...(adjustments ? { adjustments } : {}) });

const brushDot = (mcp, photoId, { x, y, radius = 0.012, feather = 100 },
                  { name, maskId: into } = {}) =>
  mcp.call("create_brush_mask", {
    photo_id: photoId,
    strokes: [{ points: [{ x, y }], radius, feather }],
    ...(into ? { mask_id: into } : {}),
    ...(name && !into ? { name } : {}),
  });

const intersectSubject = (mcp, photoId, maskIdValue) =>
  mcp.call("combine_mask", {
    photo_id: photoId, mask_id: maskIdValue, operation: "intersect", type: "subject",
  });

const addLocalAdjustments = (mcp, photoId, maskIdValue, adjustments) =>
  mcp.call("set_mask_adjustments", {
    photo_id: photoId, mask_id: maskIdValue, adjustments: toLocal(adjustments),
  });

/* ---------------- Les 4 masques ---------------- */
async function maskSujet(mcp, photoId) {
  const r = await createAiMask(mcp, photoId, "subject", DEFAULTS.sujet);
  return { mask_id: maskId(r), role: "sujet", created: r };
}

async function maskFond(mcp, photoId) {
  const r = await createAiMask(mcp, photoId, "background", DEFAULTS.fond);
  return { mask_id: maskId(r), role: "fond", created: r };
}

/** Œil = sujet ∩ pinceau. Le pinceau part seul, l'intersection le recadre. */
async function maskOeil(mcp, photoId, { x, y, radius = 0.012 }) {
  const brush = await brushDot(mcp, photoId, { x, y, radius }, { name: "Œil" });
  const id = maskId(brush);
  await intersectSubject(mcp, photoId, id);
  await addLocalAdjustments(mcp, photoId, id, DEFAULTS.oeil);
  return { mask_id: id, tool_id: brush.tool_id, role: "oeil", intersection: "brush ∩ subject" };
}

/** Plumage = sujet ∩ plage de luminance (hautes lumières du plumage). */
async function maskPlumage(mcp, photoId, { min = 0.55, max = 1.0, falloff = 0.12 }) {
  const range = await mcp.call("create_range_mask", {
    photo_id: photoId, type: "luminance",
    luminance: { min, max, falloff },
    name: "Plumage — luminance",
  });
  const id = maskId(range);
  await intersectSubject(mcp, photoId, id);
  await addLocalAdjustments(mcp, photoId, id, DEFAULTS.plumage);
  return { mask_id: id, tool_id: range.tool_id, role: "plumage", range: { min, max, falloff } };
}

/* ---------------- Recette « anti-coulée » (§4.1) ---------------- */
/**
 * Variante « range » : plage de couleur (bleu du ciel réfléchi) ∩ sujet, puis
 * désaturation + réchauffement. `sample` doit venir de l'UI (copy_sample_from)
 * ou de create_range_mask(color) déjà calibrée : l, a, b ne sont pas calculables.
 */
async function anticouleeRange(mcp, photoId, { copyFrom, sample, amount = 0.5, invert = false }) {
  const args = { photo_id: photoId, type: "color", color: {}, name: "Anti-coulée" };
  if (copyFrom) args.color.copy_sample_from = copyFrom;   // { mask_id, tool_id }
  else if (sample) args.color.sample = sample;            // { x, y, l, a, b }
  else throw new Error("anti-coulée : fournir --copy-from <maskId:toolId> ou --sample x,y,l,a,b");
  if (amount != null) args.color.amount = amount;
  if (invert) args.invert = true;

  const range = await mcp.call("create_range_mask", args);
  const id = maskId(range);
  await intersectSubject(mcp, photoId, id);
  await addLocalAdjustments(mcp, photoId, id, DEFAULTS.anticoulee);
  return { mask_id: id, tool_id: range.tool_id, role: "anticoulee", variant: "range" };
}

/**
 * Variante « pointcolor » : pas de nouveau masque, on agit DANS le sujet.
 * SrcHue 0..6 (0 rouge, ~1 jaune, ~2 vert, ~3 aqua, ~4 bleu, ~5 violet),
 * SrcSat/SrcLum 0..1. Valeurs de départ héron blanc / ciel bleu — à vérifier
 * avec get_mask (les swatches reviennent en clair).
 */
async function anticouleePointColor(mcp, photoId, { subjectMaskId } = {}) {
  const id = subjectMaskId || maskId(await createAiMask(mcp, photoId, "subject"));
  const blue = {
    SrcHue: 4.05, SrcSat: 0.32, SrcLum: 0.78,
    SatScale: -0.60, HueShift: 0.0, LumScale: 0.0, RangeAmount: 0.55,
  };
  const r1 = await mcp.call("edit_mask_point_colors", {
    photo_id: photoId, mask_id: id, action: "add", swatch: blue,
  });
  let r2 = null;   // réinjection d'un peu de jaune (variante couchant)
  try {
    r2 = await mcp.call("edit_mask_point_colors", {
      photo_id: photoId, mask_id: id, action: "add",
      swatch: { SrcHue: 1.05, SrcSat: 0.55, SrcLum: 0.85, SatScale: 0.15, RangeAmount: 0.4 },
    });
  } catch (e) { r2 = { skipped: String(e.message) }; }
  return { mask_id: id, role: "anticoulee", variant: "pointcolor", blue: r1, yellow: r2 };
}

/* ---------------- Mesure d'overspray (hors Lightroom) ---------------- */
/**
 * overspray = Δluma moyen HORS sujet / Δluma moyen DANS le sujet.
 * Rect en coordonnées normalisées « x,y,w,h » (0..1).
 *   < 0.10 → masque propre ; 0.10–0.25 → à raffiner ; > 0.25 → le masque déborde.
 */
function measureOverspray(beforePath, afterPath, rectStr) {
  const require = createRequire(path.join(REPO, "server", "package.json"));
  const jpeg = require("jpeg-js");
  const a = jpeg.decode(fs.readFileSync(beforePath), { useTArray: true });
  const b = jpeg.decode(fs.readFileSync(afterPath), { useTArray: true });
  if (a.width !== b.width || a.height !== b.height) throw new Error("dimensions différentes");
  const [rx, ry, rw, rh] = rectStr.split(",").map(Number);
  const x0 = Math.round(rx * a.width), x1 = Math.round((rx + rw) * a.width);
  const y0 = Math.round(ry * a.height), y1 = Math.round((ry + rh) * a.height);

  const luma = (d, i) => 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
  let inSum = 0, inN = 0, outSum = 0, outN = 0;
  for (let y = 0; y < a.height; y++) {
    for (let x = 0; x < a.width; x++) {
      const i = (y * a.width + x) * 4;
      const d = Math.abs(luma(b.data, i) - luma(a.data, i));
      if (x >= x0 && x < x1 && y >= y0 && y < y1) { inSum += d; inN++; }
      else { outSum += d; outN++; }
    }
  }
  const inside = inN ? inSum / inN : 0;
  const outside = outN ? outSum / outN : 0;
  const index = inside ? outside / inside : 0;
  return {
    inside_mean_delta: +inside.toFixed(3),
    outside_mean_delta: +outside.toFixed(3),
    overspray_index: +index.toFixed(3),
    verdict: index < 0.10 ? "propre" : index <= 0.25 ? "à raffiner" : "déborde",
    rect: { x0, y0, x1, y1 },
  };
}

/* ---------------- CLI ---------------- */
function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i].startsWith("--")) {
      const k = argv[i].slice(2);
      const v = argv[i + 1] && !argv[i + 1].startsWith("--") ? argv[++i] : true;
      out[k] = v;
    } else out._.push(argv[i]);
  }
  return out;
}
const num = (v, d) => (v == null || v === true ? d : Number(v));

async function main() {
  const cli = parseArgs(process.argv.slice(2));
  const cmd = cli._[0] || "inspect";

  if (cmd === "measure") {
    console.log(JSON.stringify(measureOverspray(cli.before, cli.after, cli.rect), null, 2));
    return;
  }

  const mcp = new Mcp();
  await mcp.start();
  const report = { command: cmd, steps: [] };
  try {
    const photoId = await resolvePhotoId(mcp, cli);
    report.photo_id = photoId;

    const run = async (label, fn) => {
      try {
        const v = await fn();
        report.steps.push({ step: label, ok: true, result: v });
        console.log(`OK  ${label}`);
        return v;
      } catch (e) {
        report.steps.push({ step: label, ok: false, error: String(e.message) });
        console.log(`ERR ${label} — ${e.message}`);
        throw e;
      }
    };

    switch (cmd) {
      case "inspect":
        report.masks = await run("list_masks", () => mcp.call("list_masks", { photo_id: photoId }));
        break;
      case "subject":
        report.mask = await run("sujet", () => maskSujet(mcp, photoId));
        break;
      case "background":
        report.mask = await run("fond", () => maskFond(mcp, photoId));
        break;
      case "eye":
        report.mask = await run("oeil (pinceau inter sujet)", () => maskOeil(mcp, photoId, {
          x: num(cli.x, 0.5), y: num(cli.y, 0.5), radius: num(cli.radius, 0.012),
        }));
        break;
      case "plumage":
        report.mask = await run("plumage (luminance inter sujet)", () => maskPlumage(mcp, photoId, {
          min: num(cli.min, 0.55), max: num(cli.max, 1.0), falloff: num(cli.falloff, 0.12),
        }));
        break;
      case "anticoulee": {
        if ((cli.variant || "range") === "pointcolor") {
          report.mask = await run("anti-coulee (point color dans le sujet)",
            () => anticouleePointColor(mcp, photoId, { subjectMaskId: cli["subject-mask"] }));
        } else {
          const copyFrom = cli["copy-from"]
            ? { mask_id: String(cli["copy-from"]).split(":")[0],
                tool_id: String(cli["copy-from"]).split(":")[1] }
            : null;
          const sample = cli.sample
            ? (([x, y, l, a, b]) => ({ x, y, l, a, b }))(cli.sample.split(",").map(Number))
            : null;
          report.mask = await run("anti-coulee (plage couleur inter sujet)",
            () => anticouleeRange(mcp, photoId, { copyFrom, sample, amount: num(cli.amount, 0.5) }));
        }
        break;
      }
      case "stack": {
        report.ordre = ["sujet", "plumage", "oeil", "fond"];
        report.masques = [];
        report.masques.push(await run("1. sujet", () => maskSujet(mcp, photoId)));
        report.masques.push(await run("2. plumage", () => maskPlumage(mcp, photoId, {})));
        if (cli.x != null && cli.y != null) {
          report.masques.push(await run("3. oeil", () => maskOeil(mcp, photoId, {
            x: num(cli.x, 0.5), y: num(cli.y, 0.5), radius: num(cli.radius, 0.012),
          })));
        }
        report.masques.push(await run("4. fond", () => maskFond(mcp, photoId)));
        break;
      }
      case "undo":
        report.undo = await run("undo_last_step", () => mcp.call("undo_last_step", {}));
        break;
      default:
        throw new Error(`commande inconnue : ${cmd}`);
    }
  } finally {
    await mcp.stop();
    const out = path.join(process.cwd(), `brique3-${cmd}-${Date.now()}.json`);
    fs.writeFileSync(out, JSON.stringify(report, null, 2));
    console.log(`\nrapport : ${out}`);
  }
}

main().catch((e) => { console.error(`ERREUR: ${e.message}`); process.exit(1); });
```

### 3.2 Les 4 masques : valeurs de départ (design §2)

- **1. Sujet** — `create_mask { type: "subject", adjustments }` :
  `exposure +0.30 · contrast +12 · highlights −20`.
  Rôle : détacher l'animal. Le `+contraste` compense la perte de micro-détail du masque IA.
- **2. Œil** — `create_brush_mask` (1 dab, `radius` ≈ 0.012 du grand côté) →
  `combine_mask intersect subject` → `set_mask_adjustments` :
  `local_Exposure +0.35 · local_Clarity +20 · local_Sharpness +35`.
  C'est le point d'accroche : à faire **en dernier**, quand l'exposition globale est figée.
- **3. Plumage / pelage** — `create_range_mask { type: "luminance", min: 0.55, max: 1.0,
  falloff: 0.12 }` → `intersect subject` → `set_mask_adjustments` :
  `local_Texture +15 · local_Sharpness +25 · local_Saturation +5 · local_Highlights −15`.
  Dompter les hautes lumières du plumage **sans toucher au fond** : c'est l'intersection qui le
  garantit.
- **4. Arrière-plan** — `create_mask { type: "background", adjustments }` :
  `exposure −0.25 · texture −15 · clarity −5 · temperature −6 · tint 0`.
  Température locale négative = fond plus froid, sujet plus chaud par contraste. À inverser
  (positif) sur fond déjà chaud.

### 3.3 Recettes nommées

- **« Plumage clair — anti-coulée »** — deux implémentations, à départager en test :
  - `range` : plage de couleur (bleu réfléchi) **∩ sujet** →
    `local_Saturation −45 · local_Temperature +10 · local_Tint +2`.
    Sélection déterministe si l'échantillon est copié d'un masque créé à la main (`--copy-from`).
  - `pointcolor` : dans le masque sujet, swatch bleu `SrcHue 4.05 · SrcSat 0.32 · SrcLum 0.78`
    avec `SatScale −0.60`, puis swatch jaune `SrcHue 1.05` avec `SatScale +0.15` (variante couchant).
    Plus chirurgical, mais les valeurs `Src*` sont des **hypothèses par photo**.
  - **Pendant « sujet sombre »** : même mécanique sur un corvidé — `SrcLum` plus bas (≈ 0.35),
    `RangeAmount` plus large (0.65).
- **« Sculpture de lumière »** — `create_gradient_mask` (radial) dupliqué sur les zones peu
  éclairées, même géométrie, même force. Non codé ici : géométrie à caler à la main d'abord.
- **« Œil vivant »** — c'est le masque 2 tel quel.

### 3.4 Mesure d'overspray

`measure` compare deux JPEG exportés (avant / après) et calcule :

```
overspray_index = Δluma_moyen(hors rect) / Δluma_moyen(dans rect)
< 0.10 propre · 0.10–0.25 à raffiner · > 0.25 déborde
```

Deux précautions : exporter en JPEG qualité 100, mêmes dimensions, et **même cadrage** — sinon la
mesure compare deux géométries. Le `rect` doit englober le sujet avec ~5 % de marge.
Bonus : la mesure fonctionne aussi sur la 0.4.1 (elle ne dépend que des fichiers) → permet d'établir
la **ligne de base** du masquage manuel actuel avant de comparer.

---

## 4. Procédure de test (Lightroom réel)

Pré-requis : montée §1.6 faite, `LIGHTROOM_MCP_TOOLSETS=all`, photo test héron / oiseau en vol dans
une collection dédiée (ne pas travailler sur un RAW unique — masquer puis annuler sur un fichier de
référence évite de perdre des retouches existantes).

1. **[M5] Vérifier la version** : Lightroom > Aide > À propos. Attendu **15.6**.
   Si autre version → **arrêt** : le plugin refusera d'écrire les masques, la brique 3 ne passe pas
   par MCP. Noter la version exacte.
2. **[M5] Sauvegarder le plugin actuel** (§1.6, étape 0).
3. **[M5] Installer** : `node dist/index.js install-plugin` depuis `lightroom-mcp-027/server`.
4. **Lightroom** : File > Plug-in Manager > Lightroom MCP > **Reload Plug-in**, puis **Start Server**.
   Vérifier « Server running ». Si `failed to open localhost:58763` : quitter Lightroom (Cmd+Q) et
   rouvrir.
5. **Sonde de disponibilité** — doit exposer les 15 outils de masquage :
   `[M5] LIGHTROOM_MCP_TOOLSETS=all node -e '<sonde §1.6 étape 3>'`
6. **Sélectionner la photo test** dans Lightroom (Develop ou Library : le plugin bascule tout seul).
7. **[M5] `inspect`** — doit renvoyer `count: 0` sur une photo vierge de masques.
   Échec `Lightroom lists no masks...` → une alerte modale (« No sky detected ») est ouverte :
   cliquer OK dans Lightroom et relancer.
8. **[M5] `subject`** → vérifier dans Lightroom : masque « Sujet » créé, overlay visible.
   **Mesure visuelle 1** : baisser l'opacité de l'overlay et repérer les zones mordues (ailes,
   espace entre les pattes) — c'est l'overspray attendu du design §1.
9. **[M5] `plumage --min 0.55 --max 1`** → `inspect` doit montrer un composant de type plage
   (`subtype: "luminance"`) et **`inverted: true`** sur le composant IA : c'est la trace de
   l'intersection. Si `inverted` est absent, l'intersection n'a pas été prise.
10. **[M5] `eye --x <x> --y <y>`** — coordonnées normalisées de l'œil (0..1, origine haut-gauche).
    `inspect` doit montrer **deux** composants dans le masque : `Mask/Paint` + `aiSelection`.
    **Test du piège** : ajouter un dab ailleurs (`create_brush_mask` avec `mask_id` = ce masque) et
    vérifier que la zone ajoutée est **sélectionnée** (union) — donc qu'il faut re-`intersect`.
11. **[M5] `background`** → masque fond créé ; vérifier à l'overlay qu'il ne mord pas le sujet.
12. **Mesure d'overspray objective** :
    exporter « avant » (masques désactivés) puis « après », qualité 100, mêmes dimensions, puis
    `[M5] LRM_MCP_ROOT=~/PKA_JCH/_local/lightroom-mcp-027 node brique3_masks.mjs measure --before ./before.jpg --after ./after.jpg --rect .30,.20,.40,.45`
    Objectif de la brique : `overspray_index < 0.10` sur l'œil et le plumage.
    Ligne de base : refaire la mesure sur un masquage manuel pour situer le gain.
13. **Anti-coulée** : créer d'abord **une** plage de couleur à la main dans Lightroom
    (Tools > Create New Mask > Color Range, cliquer le bleu du plumage), puis
    `[M5] node brique3_masks.mjs inspect` → relever `maskId` + `toolId` de cette plage, puis
    `[M5] node brique3_masks.mjs anticoulee --variant range --copy-from <maskId>:<toolId>`
    Comparer avec `--variant pointcolor` sur la même photo (avant/après exportés).
14. **Annulation** : `undo` (appelle `undo_last_step`) ou Cmd+Z dans Lightroom ; en dernier recours,
    revenir à l'état catalogue par l'historique Lightroom. Le plugin restaure déjà l'état précédent
    en cas d'échec de lecture de contrôle — mais **pas** entre deux appels réussis.
15. **Clore** : noter version LrC, `overspray_index` des 4 masques, et le variant anti-coulée retenu.

Durée estimée : 25–35 min sur une photo. Rien de destructif : chaque masque est annulable.

---

## 5. Points à valider par JC (avant toute exécution)

1. **Version Lightroom Classic** : 15.6 avec process version 15.4 ? Si non → la brique 3 MCP est
   bloquée ; il faut soit mettre à jour LrC, soit livrer les masques comme **presets XMP** (point 5).
2. **Stratégie de montée** : worktree (recommandé) / clone nu / report. Le side-by-side implique un
   **swap unique du plugin** — pas de coexistence des deux versions sur un même Lightroom.
3. **Patch de parité brique 1** : porter `SplitToning*` (+ `ColorGradeBlending`) dans l'allowlist
   0.27.0, sinon les presets Naturaliste perdent leur grading. GO / NO GO ?
   (Ne pas porter `ToneCurvePV2012*` — le SDK les droppe.)
4. **`preset_amount`** : à porter ou à abandonner ? Aucun flux actuel n'en dépend.
5. **Canal de livraison produit** : script MCP (calibration interne) ou **preset XMP portant les
   masques** ? `apply_develop_preset` upstream recalcule les masques IA par photo sur LrC 13.3+ :
   c'est la voie « livrable client » (4 masques + réglages dans un preset), le script restant l'outil
   de calibration. À trancher avant d'industrialiser.
6. **Acceptation du risque « structure interne non documentée »** : la clé racine
   `MaskGroupBasedCorrections` est officielle (SDK 11), mais la structure des composants est
   reverse-engineered et gatée 15.6. Le guarded write (preflight + read-back + restore) est le
   garde-fou. Accepté ?
7. **Photo(s) de test** : laquelle / lesquelles ? (héron posé et oiseau en vol sont deux cas
   différents : le second tolère mal l'intersection luminance — flou de mouvement dans les hautes
   lumières.)

---

## 6. Ce qui n'a pas été fait — limites de ce rapport

- **Rien n'a été exécuté.** Ni le plan de montée, ni le code, ni Lightroom. Le code n'a même pas été
  chargé par Node : il est relu, pas testé.
- **`_local/lightroom-mcp/` est intact** : arbre sale inchangé, aucun fichier créé ni modifié.
- La **version de Lightroom installée n'a pas pu être vérifiée** : `exec_shell` et
  `task_shell_start` ont été refusés dans cette session, et le journal
  `~/Documents/LrClassicLogs/LightroomMCP.log` est hors workspace. C'est le point n°1 de la liste §5.
- Le **nombre exact de commits** entre le HEAD local et `origin/main` n'a pas été mesuré (pas de
  `git fetch` possible) : la comparaison est structurelle (fichiers, contrats, handlers), pas
  historique.
- Les **valeurs de réglages** des 4 masques sont des points de départ cohérents avec le §2 du design,
  **pas des valeurs calibrées** : le design §6.3 interdit de figer sans mesure sur RAW réels.
- Les **`SrcHue/SrcSat/SrcLum`** du Point Color et les **`l/a/b`** de la plage de couleur sont des
  hypothèses : Lightroom stocke des rangs internes par photo, non calculables depuis le RGB.

---

## 7. Références

- Design : `JCH_Inbox/03_PROJECTS/02_ARTEON/strategy/brique-3-masques-ia-design.md`
- Problème ColorGrade (résolu B) : `strategy/2026-11-16_probleme-colorgrade-sdk-lightroom.md`
- Copie locale : `_local/lightroom-mcp` (0.4.1, HEAD `d7fd07b`, arbre sale)
- Upstream : `github.com/Automaat/lightroom-mcp` @ `c6551e2` = npm `@mskalski/lightroom-mcp@0.27.0`
- Sources upstream consultées : `server/src/{tool-contracts,toolsets,cli,index}.ts`,
  `plugin/LightroomMCP.lrplugin/{PluginInfoProvider,DevelopSession,GuardedMaskWrite,MaskTypes,HandlerMasks,HandlerMaskCreate,HandlerMaskCombine,HandlerBrushMasks}.lua`
- Mécanique du curseur proportionnel : `_local/lightroom-mcp/tests/strength-sweep/README.md`
