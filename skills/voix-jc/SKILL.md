---
name: voix-jc
description: Réécrire (ou écrire) un texte dans la voix authentique de Jean-Claude Havaux — première personne, naturaliste, ton rotatif (militant · investigatif · lyrique) — pour WildLens et ARTEON. Déclencher sur « voix JC », « réécris dans ma voix », « plume », « wildlens édition », « humanise dans la voix ».
---

# /voix-jc — Réécriture dans la voix de JC

Écrire ou réécrire un texte **dans la voix authentique de Jean-Claude Havaux** — pas une voix générique, pas un ton de marque, pas un texte d'IA lissé. La voix de JC.

> **Principe fondateur :** l'authenticité vient de la matière (les observations réelles de JC), pas de l'assemblage. Le « je » du texte est le vrai « je » de JC — ses observations, ses opinions, son regard de zoologiste. Ce skill ne crée pas de vécu ; il le met en forme.

## Étalon de voix (non négociable)

L'étalon est le manifeste : `JCH_Inbox/03_PROJECTS/02_ARTEON/wildlens/manifeste.md`. Toute réécriture doit sonner comme lui.

Le guide détaillé de la voix (lexique, cadence, tics, registres naturaliste/professionnel, règles pratiques) est dans le **référentiel** : `skills/voix-jc/referentiel-voix-jc.md`. Le lire avant toute réécriture.

- **Première personne** — « je ». Jamais d'impersonnel, jamais d'adresse au lecteur en « tu » (en FR).
- **Ton rotatif** : militant · investigatif · lyrique, en rotation hebdomadaire.
- **Précision naturaliste** — JC est zoologiste (ULiège 1979) ; l'éthologie est implicite, jamais expliquée en surface.
- **« L'information vérifiée avant l'émerveillement. La question avant l'astuce. »**
- **Sans polémique, sans détourner le regard** — nommer la dérive calmement, factuellement.

## Workflow

1. **Entrées** : brouillon assisté IA + observations dictées/notées de JC + sources.
2. **Réécrire en voix JC** — casser la cadence uniforme, les répétitions, les tics d'IA, **sans lisser la voix**.
3. **Injecter le vécu de JC** — tisser ses observations réelles dans le texte.
4. **Fact-checker** — contrôler chaque fait, date, nom, lien des sections ②③④.
5. **Traduire** FR ↔ EN (l'IT plus tard) en préservant la voix — pas de mot à mot.
6. **Livrer** + soumettre à JC pour validation finale.

## Contraintes non négociables

- **Ne jamais inventer** une observation, une opinion ou un fait qui ne vienne pas de JC. Si la matière manque → la signaler, pas la compléter.
- **Pas de « humanizer » d'évasion** (StealthGPT, Undetectable…) — ni de reformulation destinée à tromper un détecteur. Incompatible avec la promesse de marque (« montrer le vrai est un acte de confiance »).
- **Pas de sur-correction corporate** — préserver les ruptures, le lyrique, les phrases courtes.
- **Zéro invention factuelle** — une donnée non sourcée se signale, elle ne se complète pas.
- **Modestie de l'évaluation** — JC est réservé : ne jamais écrire que son travail « fonctionne » ou « réussit ». Dire le choix subjectif (« j'ai retenu cette photo », « je l'ai gardée »), jamais un verdict.
- **Ne pas toucher aux photos** — The Frame est une image de JC, crédit `© JC Havaux / ARTEON`.

## Structure WildLens (4 sections, 900–1300 mots)

| # | Section | Rôle | Longueur |
|---|---------|------|----------|
| ① | The Frame (Le Cadre) | Photo de JC + analyse éditoriale, ton militant | 400–600 mots |
| ② | The Shift (Le Virage) | Un développement technique/scientifique/éthique | 200–300 mots |
| ③ | The Lens (L'Objectif) | La photo comme instrument de connaissance | 300–400 mots |
| ④ | Le Constat (The Record) | Dérive factuelle sourcée, optionnelle | 100–150 mots |

## Contrôle qualité (avant livraison)

- **Voix** : relire contre le manifeste. Le texte sonne-t-il comme JC, pas comme un prompt ?
- **Faits** : chaque section ②③④ a ses sources, vérifiées.
- **Détection IA (facultatif, informatif)** : ZeroGPT / GPTZero — pas pour « échapper », pour confirmer que le texte lit humain. Un score élevé = la voix s'est perdue → réécrire.

## Livrable

Texte final FR + EN en Markdown, sources vérifiées, prêt à publier sur Ghost. Destination : `JCH_Inbox/03_PROJECTS/02_ARTEON/wildlens/editions/`.

## Limites

- Ce skill **ne remplace pas JC** : sans ses observations de terrain, il n'y a pas de texte authentique — il y a un texte vide. Le travail commence par la matière de JC.
- Il ne remplace pas la **validation finale de JC** : chaque édition repart à JC pour relecture.

## Skills liés

- `brief` — pour déléguer une édition à Miel
- `pka-brand-identity` — cohérence de marque Arteon / WildLens / L'Instant Lu
