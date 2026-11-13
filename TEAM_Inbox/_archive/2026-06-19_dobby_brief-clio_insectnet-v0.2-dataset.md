# Brief — Clio 🦜 : Extension dataset InsectNet V0.2 (reformulé)

**Date :** 2026-06-19  
**Émis par :** Dobby 🦉  
**Deadline :** 2026-06-24  
**Priorité :** P1 — prépare l'extension V0.2 du classifieur

## Contexte mis à jour

Depuis le brief du 17 juin, la situation a changé :
- **Le classifieur V0.1 est fait.** CNN from scratch sur mel-spectrogrammes, F1=0.98 sur 5 espèces, testé sur 200 segments Xeno-Canto + 1447 segments iPhone de JC.
- **L'approche BirdNET a été testée et écartée** — ne capture que la fréquence porteuse pour les insectes.
- **Le dataset V0.1** : 5 espèces, 187 enregistrements XC (qualité A+B, worldwide), 5 442 segments.

La question n'est plus « quelle architecture choisir ? » mais **« comment passer de 5 à 15-20 espèces pour V0.2 ? »**

## Mission

Évaluer **InsectSet459** comme source d'extension du dataset InsectNet.

## Questions précises

1. **Couverture** — Combien de nos 5 espèces V0.1 sont dans InsectSet459 ? Combien d'espèces européennes supplémentaires (>20 enregistrements) sont disponibles ?
2. **Qualité** — Les enregistrements InsectSet459 sont-ils des segments propres ou des enregistrements bruts ? Y a-t-il des métadonnées GPS/date ?
3. **Licence** — Quelle est la licence d'InsectSet459 ? Compatible avec un usage scientifique non commercial ?
4. **Format** — Format audio, sample rate, durée typique ? Compatible avec notre pipeline 3s ?
5. **Complémentarité** — InsectSet459 + Xeno-Canto = redondance ou complémentarité ? (XC couvre déjà bien l'Europe)

## Livrable

Un fichier unique : `INSECTNET/01_RESEARCH/insectset459-evaluation.md`

Format : 5 sections répondant aux 5 questions ci-dessus + une recommandation finale (adopter / compléter / ignorer).

## Références

- `04_MODELS/baseline-results.md` — résultats V0.1
- `02_DATASET/alpine-species-inventory.md` — 132 espèces alpines XC
- `TEAM_Inbox/2026-06-17_dobby_brief-clio_insectnet-research.md` — brief original (contexte historique)
- `.arbor/research/insectnet/TREE.md` — arbre de décision Arbor
