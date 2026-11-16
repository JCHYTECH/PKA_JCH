---
date: 2026-11-16
source: dobby
domain: arteon
type: contrat
status: actif
lang: fr
---

# Contrat de look — Pack Naturaliste (forme / ancrage / amplitude)

> Dobby 🦉 — 2026-11-16 · Suite P1. Un look n'est plus une teinte fixe : c'est un triplet documenté
> `{ forme d'harmonie, plage d'ancrage, amplitude }`. Le XMP livre l'**instance par défaut** ;
> la brique `/recommend` livrera l'**instance adaptée** à la dominante mesurée de l'image.
>
> Principe issu des transcripts grading : le grade **accentue** la couleur déjà présente, il ne la
> réécrit pas ; les tons moyens « font l'équilibrage » ; l'abstention est une option légitime.

---

## Le contrat en une ligne

`{ forme, ancrage, amplitude }` — ex. « Y complémentaire : ancre les ombres à l'opposé de la
dominante détectée, doré en hautes, tons moyens en équilibrage ». Le curseur de force ne fait
varier que **l'amplitude** (saturation + luminance), jamais la teinte — c'est la sémantique des
raccourcis Lightroom (`Shift` = verrouille la teinte, libère la saturation) et du `presetAmount` natif.

---

## Signature chromatique du pack (invariant)

- **Ombres** : bleu acier 220° (déjà documenté, cf. P0-2) — quelques looks décalent (Nocturne 230°, Contre-jour 210°).
- **Hautes lumières** : doré 38–40° — décalé vers 35° (Nocturne) ou 40° (Golden hour).
- **Tons moyens** : la roue ajoutée en P1 — c'est elle qui rend les 12 looks réellement distincts.

---

## Table de contrat (valeurs base, force 100 %)

| Look | Ombre | Moyen | Haute | Lum (S/M/H) | Blend | Bal | Forme | Ancrage |
|------|-------|-------|-------|-------------|-------|-----|-------|---------|
| Signature Fin Art Cinématique | 220°/10 | 40°/3 | 38°/6 | 0/0/0 | 50 | −20 | complémentaire (acier/doré) | ombres |
| Plumage sombre | 220°/10 | 30°/6 | 38°/6 | −8/0/0 | 65 | −10 | complémentaire chaude | ombres (noirs veloutés) |
| Plumage clair | 220°/10 | 200°/2 | 38°/6 | 0/0/0 | 40 | +10 | complémentaire froide | hautes (blancs propres) |
| Golden hour | 220°/10 | 40°/8 | 40°/7 | 0/0/+5 | 75 | +25 | analogue chaude | hautes (halo doré) |
| Plumage coloré | 220°/10 | 210°/5 | 38°/6 | 0/0/0 | 50 | 0 | complémentaire (bleu moyen) | moyen (rehausse bleus) |
| Mammifères | 220°/10 | 25°/6 | 38°/6 | −5/0/0 | 60 | −10 | analogue chaude (fauve) | ombres |
| Nocturne | 230°/10 | 215°/5 | 35°/6 | −6/0/0 | 55 | −5 | complémentaire froide | ombres (nuit) |
| Macro | 220°/10 | 0°/2 | 38°/6 | 0/0/0 | 45 | 0 | neutre | — (détail d'abord) |
| Action / vol | 220°/10 | 210°/3 | 38°/6 | 0/0/0 | 35 | 0 | complémentaire froide | neutre (ne mord pas le bruit) |
| Paysage | 220°/6 | 45°/4 | 38°/4 | 0/0/0 | 55 | +10 | analogue chaude | hautes |
| Noir & blanc | 220°/0 | 0°/0 | 38°/0 | 0/0/0 | 50 | −20 | monochrome | — |
| Contre-jour / brume | 210°/6 | 195°/4 | 38°/5 | 0/0/0 | 85 | +15 | complémentaire douce | hautes (atmosphère) |

**Légende** : `Lum (S/M/H)` = Luminance ombre / moyen / haute (négatif = assombrit la plage). `Blend` = dureté de transition. `Bal` = biais ombre(−)/haute(+).

**Règle de force** : Doux = saturation + luminance × 0.4 · Fort = × 2.0. Teinte, Blending et Balance **constants** entre les 3 forces.

---

## Ordre d'exécution documenté (réponse au piège « on n'apprend rien »)

1. **Regarde la dominante** de la scène (lumière + sujet + fond) — pas le look d'abord.
2. **Choisis le look** dont l'ancrage correspond (sujet sombre → Plumage sombre ; blanc → Plumage clair ; couchant → Golden hour…).
3. **Corrige les tons moyens en dernier** (ils font l'équilibrage), puis laisse `Blend`/`Bal` faire le fondu.
4. **Abstiens-toi** si le grade « colle » comme un filtre : baisse la Luminance de la plage concernée, ou saute la plage.

---

## Ce que le XMP ne fait PAS (par contrat)

Ni balance des blancs, ni exposition (retirées en P0-1), ni débruitage IA dépendant du boîtier,
ni rattrapage d'un flou ou d'une sous-exposition de plusieurs IL. Le preset donne la **direction**,
l'utilisateur la **valeur**.

---

*Découle de : `TEAM_Inbox/2026-11-16_dobby_synthese-enrichissement-xmp-plugin-animalier.md` (rec. 5).*
*Appliqué par : `scripts/add_midtone_grading_xmp.py` (P1-4).*
