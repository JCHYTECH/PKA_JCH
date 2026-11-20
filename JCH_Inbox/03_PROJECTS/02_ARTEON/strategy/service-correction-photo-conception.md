---
date: 2026-11-16
source: dobby
domain: arteon
type: conception
status: v1 (gelé après conseil)
lang: fr
---

# Service de correction photo « Naturaliste » — Conception V1

> Dobby 🦉 — 2026-11-16 · V0 passée au conseil (5 stances). Verdict : **NO-GO service automatisé · GO conditionnel**
> (test manuel falsifiable + pivot plugin/contenu + funnel d'abord). Cette V1 fige le recadrage.
> Verdict complet : `TEAM_Inbox/2026-11-16_dobby_conseil_correction-photo.md`.

---

## 0. Le recadrage (ce qui a changé entre V0 et V1)

| V0 (avant conseil) | V1 (après conseil) |
|--------------------|--------------------|
| Construire un service qui reçoit → corrige → renvoie | **Ne pas construire de service.** Tester à la main, puis pivoter |
| `/recommend` = brique 🔴 bloquante | `/recommend` = **fictif** tant qu'il n'y a pas de dataset A/B pour la calibrer |
| Architecture A (batch) recommandée | A = mode manuel déguisé ; pas d'orchestrateur tant que la demande n'est pas prouvée |
| MVP : /recommend → pipeline → ingestion → restitution | MVP : **test manuel → contenu avant/après → plugin → dataset** |
| Gouvernance en 🟡 | Gouvernance = préalable dur si un jour on héberge (catalogue séparé, suppression, consentement) |

**Principe directeur** : la fin est « preuve concrète + acquisition du pack ». La correction est un **moyen**, pas l'objectif. On ne construit pas l'étape 3 d'un entonnoir vide.

---

## 1. Vision (inchangée)

Faire du regard ARTEON/Naturaliste une preuve démontrable qui convertit vers le pack — **sans engager la marque
sur la retouche automatisée de photos de tiers** avant d'avoir prouvé la demande.

---

## 2. État des lieux (inchangé, avec les faits qui ont tranché)

- MCP Lightroom local (M5) : 14 outils — la correction est **faisable en manuel**, pas en service.
- Funnel : **0 vente, 0 email, Ghost en 404** — aucun utilisateur n'a jamais envoyé de photo.
- Argus : 58 analyses = les photos de JC ; tables `retouch_proposals`/`retouch_sessions` **vides** (dataset A/B non capté).
- Pack : 12 looks partageant le même invariant (ombres 220°, hautes 38°) — `recommend` ne peut pas les discriminer par EXIF.
- Précédent : L'Instant Lu déjà NO-GO sur la critique photo à l'acte, pour les mêmes raisons.

---

## 3. La séquence cible (V1) — pas un pipeline

```
M1 · Test manuel falsifiable   →  M2 · Contenu avant/après   →  M3 · Plugin (pivot)   →  M4 · Dataset A/B → /recommend calibré
```

### M1 — Test manuel falsifiable (le premier jalon, PAS le dernier)
- 10–20 photos du corpus, corrigées **à la main** via le MCP (une après-midi).
- **Jugement en aveugle** par ~5 photographes : « préféré / indifférent / pire » + intention d'achat du pack.
- **Critère d'arrêt** : si « pire + indifférent » > 50 %, on arrête — la demande n'existe pas.
- C'est le test que la V0 repoussait en M4 ; le conseil le remonte en M1.

### M2 — Contenu avant/après (l'actif immédiat)
- Les paires produites en M1 deviennent la **galerie de la landing** (pas un email privé).
- Deux phrases de justification naturaliste par paire (le « pourquoi » — la seule chose non commoditisable).
- Bouton de **pré-commande** à coût nul (« je corrige votre photo, X € ») : compter les clics. Zéro clic = zéro service.

### M3 — Pivot plugin (au lieu d'héberger)
- Le moteur est déjà un plugin Lightroom Lua (`_local/lightroom-mcp/plugin/LightroomMCP.lrplugin`).
- **Livrer le plugin** (abonnement ~39 €/an) plutôt que d'héberger : 0 upload, 0 donnée personnelle, RGPD non-sujet, scalabilité = nombre d'installations.
- Le service hébergé (archi A/B) ne revient **que** si M2 révèle une demande réelle (≥ 3 demandes spontanées/semaine).

### M4 — Dataset A/B → `/recommend` calibré (le vrai différenciateur, plus tard)
- Servir **deux** corrections (look A vs B, un seul paramètre d'écart) à chaque utilisateur, récupérer le vote.
- Alimente `retouch_proposals` (déjà en base, vide) : ~5 200 paires/an pour ≈ 0 € de collecte.
- C'est **ce dataset** qui calibre `/recommend` — pas l'inverse. `/recommend` n'est plus une brique à coder, c'est un modèle à entraîner sur les votes.

---

## 4. Ce qu'on ne fait PAS (garde-fous issus du conseil)

1. **Pas d'orchestrateur** tant que la demande n'est pas prouvée (M2 n'a pas converti → pas de M3/M4 d'infra).
2. **Pas d'ingestion publique** ni d'exposition réseau de la M5 (archi B = non-starter).
3. **Pas de correction automatique gratuite** qui court-circuite le pack (cannibalisation). Si correction payante → jugement humain, à l'unité.
4. **Pas d'import dans le catalogue de production de JC** : catalogue séparé/jetable par lot, suppression documentée, consentement explicite à la réutilisation. (Valable dès M1.)
5. **Pas de promesse non tenable** : le grade global ne recadre/débruite/redresse pas — le dire, ne pas vendre « regard de zoologiste » sur un JPEG de téléphone.

---

## 5. Questions résolues par le conseil

1. **Lead-magnet vs payant** → ni l'un ni l'autre pour l'instant : **contenu + plugin** ; payant à l'unité seulement avec jugement humain, si demande.
2. **Correction auto vs jugement expert** → la correction auto **ne suffit pas** comme preuve expert ; le jugement reste humain.
3. **A vs B** → **aucune des deux** maintenant ; plugin d'abord, hébergement seulement si M2 convertit.
4. **RAW vs JPEG** → à trancher dès M1 : JPEG = simple mais marge nulle (le preset ne vaut que sur RAW) ; le plugin (M3) résout le problème en local.
5. **Qui est l'expert** → **JC** (humain) pour le test M1 et le contenu ; Argus en appui seulement pour le dataset A/B (M4).

---

## 6. Jalons & critères

| Jalon | Livrable | Critère de passage |
|-------|----------|--------------------|
| M1 | 10–20 corrections manuelles + test aveugle | « pire+indifférent » ≤ 50 % sinon stop |
| M2 | galerie avant/après + bouton pré-commande | ≥ 3 demandes spontanées/semaine pour envisager la suite |
| M3 | plugin Lightroom packagé | ≥ 20 installations / premiers abonnés |
| M4 | dataset A/B alimenté | `/recommend` calibré sur votes, taux de préférence mesurable |

---

*Pré-requis vérifiés : outils MCP réels, pack committé, Argus en base.*
*Conseil : 5 stances (`TEAM_Inbox/2026-11-16_dobby_conseil-correction-photo_*.md`) + verdict (`..._conseil_correction-photo.md`).*
