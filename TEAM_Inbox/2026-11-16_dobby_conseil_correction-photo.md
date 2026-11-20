---
date: 2026-11-16
source: dobby
domain: arteon
type: conseil-verdict
status: actif
lang: fr
---

# CONSEIL — VERDICT · Service de correction photo « Naturaliste »

> Dobby 🦉 chairman · 2026-11-16 · 5 stances lues comme données brutes. Verdict souverain, pas un vote.

## Décision

Concevoir un service ARTEON qui reçoit une photo, la corrige (look « Naturaliste »), la renvoie corrigée — faut-il GO, et sous quelle forme ?

## Recommandation

**NO-GO sur le service automatisé** (architecture A batch comme B temps réel, telles que conçues en V0).
**GO CONDITIONNEL** sur : (1) un **test manuel falsifiable en premier**, (2) un **pivot « plugin + contenu avant/après »**, (3) le **funnel d'abord**.

## Arguments pour le GO conditionnel

- La preuve avant/après est un **actif réel**, produisible en un après-midi en manuel (le MCP Lightroom existe déjà).
- L'upside n'est pas le service mais ses **sous-produits** : livrer le plugin (O1, ~39 €/an × 150 abonnés, zéro serveur), capter un dataset de préférences A/B (O2, tables `retouch_proposals` déjà en base, vides), nourrir une « Clinique » éditoriale WildLens (O3, 52 épisodes/an sans temps créatif JC).
- Le **test en aveugle** coûte une journée et tranche la seule vraie question : est-ce que ça convertit ?

## Arguments contre le service automatisé

- **Funnel vide** : 0 vente, 0 email, Ghost en 404, aucun utilisateur n'a jamais envoyé de photo — on conçoit l'étape 3 d'un entonnoir qui n'a jamais eu d'étape 1.
- **`/recommend` est fictif** : choisir parmi 12 looks qui partagent le même invariant (ombres 220°, hautes 38°, tons moyens à 2–8 % de saturation) via l'EXIF est un `switch` arbitraire, pas un « regard ». Le chaînon « 🔴 bloquant » de la V0 n'existe pas.
- **La correction auto ne tient pas la promesse** : un grade global ne recadre pas, ne débruite pas, ne redresse pas — sur un JPEG de téléphone réel, l'avant/après est plat, parfois pire. La valeur perçue est dans le recadrage/netteté/bruit, exactement ce que le pipeline ne touche pas.
- **La chaîne MCP n'est pas automatisable en l'état** : « Start Server » à la main, photo sélectionnée dans l'UI, écritures sérialisées sur catalogue verrouillé. Le « batch » retombe en pilotage manuel.
- **Précédent non retenu** : le conseil L'Instant Lu avait déjà dit NO-GO sur la critique photo à l'acte, pour les mêmes raisons (prix < coût réel, promesse non tenable).

## Objection la plus forte

**Premiers Principes** — le cadrage est faux : la V0 énonce elle-même que la fin est « preuve concrète + acquisition du pack » ; la correction n'est qu'un moyen. On industrialise la **commodité** (la correction est saturée : Etsy, auto-enhance de chaque téléphone) et on **cannibalise le pack** (livrer le résultat sans le savoir retire la raison de payer 29 €). Le vrai déficit est une *séquence* de distribution, pas un pipeline.

**Réponse à l'objection** : acceptée. La V1 recadre entièrement : plus de service à construire, un test manuel + un pivot plugin/contenu, et la demande doit être **prouvée avant** l'infrastructure (bouton de pré-commande à coût nul ; seuil de 3 demandes spontanées/semaine avant toute ligne d'orchestrateur).

## Résidu de risque (assumé)

Même le pivot suppose que les avant/après convertissent. Si la galerie ne convertit pas, le manque est la **demande**, pas la livraison — aucun pipeline n'y changera rien.

## Dissent

- **Expansionniste** maintient un GO — mais sur la forme **plugin / dataset A/B / lot B2B**, jamais le service hébergé ; il rejoint donc le NO-GO sur l'archi A/B.
- **Outsider** maintient que l'intuition est bonne mais l'**emballage** à refaire : fichier accepté (RAW vs JPEG), promesse testable, preuve, et séparer service/formation/produit.
- **Contrarian**, **Premiers Principes** et **Prémortem** convergent sur NO-GO service, GO test manuel.

---

*Livrables de stances : `TEAM_Inbox/2026-11-16_dobby_conseil-correction-photo_{contrarian,premiers-principes,expansionniste,outsider,premortem}.md`.*
*Décision reportée dans la V1 : `02_ARTEON/strategy/service-correction-photo-conception.md`.*
