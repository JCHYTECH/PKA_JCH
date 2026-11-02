---
name: jade-traduction-bilingue
description: Traduction bilingue FR/EN ↔ ZH pour VETALYX/DIAHO — format, terminologie figée, Tone Note. Déclencher sur "traduis", "traduction", "DIAHO", "Jade", "bilingue", "courrier Dr Wu", "contrat chinois".
---

# Skill — jade-traduction-bilingue

## Déclencheurs
- « traduis », « traduction », « bilingue », « FR-ZH », « EN-ZH »
- Toute mention de **DIAHO**, **Jade**, partenaires chinois de VETALYX
- Contrats, Quality Agreement, statuts, courriers, analyses juridiques destinés aux Chinois

## Source canonique
`docs/system/procedure-traduction-jade.md` — procédure complète (à lire avant toute traduction). Ce skill en est le pointeur d'exécution.

## Acteurs
- **Jade 🦩** — traductrice scientifique & juridique EN↔ZH, sens-pour-sens (jamais mot-à-mot).
- **Renard 🦊** — briefe Jade sur le registre et les termes clés **AVANT** toute traduction juridique.
- **Dobby 🦉** — orchestration, révision finale, livraison, archivage.
- **Vasco 🐺** — revue qualité (Quality Agreement).

## Règle transverse
Tout document contractuel ou stratégique impliquant DIAHO est **bilingue dès la première rédaction** (Jade co-intervient dès le départ, pas en bout de chaîne).

## Trois sens de traduction
1. **FR → ZH** (sortant) : bilingue paragraphe-par-paragraphe, en-tête `Rédigé/Traduit/Révisé par` en FR **et** ZH. **Pas de Tone Note.**
2. **ZH → FR/EN** (entrant) : sens-pour-sens, **Tone Note obligatoire**, flagger les termes sans équivalent (traduction explicative, jamais d'approximation).
3. **EN → ZH** (contrat anglais) : bilingue EN/ZH, l'anglais fait foi.

## Tone Note (obligatoire après ZH → FR/EN)
```
TONE NOTE
---------
Registre : [formal / semi-formal / cautious / warm / transactional]
Température : [registre émotionnel global]
Signaux : [ce qui se joue entre les lignes]
Lecture : [interprétation d'intention de Jade]
```
Ne jamais lisser un signal que JC doit entendre.

## Terminologie figée (extrait — la liste complète est dans la procédure)
| Source | Cible |
|--------|-------|
| DIAHO / DiaHo / Diaho | **迪亚霍** (⚠️ jamais 迪奥) |
| Zheda Dixun | 浙大迪迅 |
| Contrat-cadre | 框架协议 |
| Quality Agreement | 质量协议 |
| LFIA | 侧向层析免疫分析 |
| Savoir-Faire | 专有技术 |
| Non-concurrence | 不竞争 |
| Force majeure | 不可抗力 |

> Registre : 商务专业 sans rigidité. Éviter les formules administratives excessives (兹, 特此). « 您 » systématique = respect dû au partenaire.

## Nommage & livraison
- Nommage : `YYYY-MM-DD_jade_traduction-[objet]-[FR|EN]-ZH.md`
- Dépôt : `JCH_Inbox/03_PROJECTS/08_VETALYX/legal/contrat-diaho/` (contrats DIAHO) ; documents de constitution → `.../legal/Creation Vetalyx avec Chinois/`
- `.docx` de l'inbox → convertir en `.md` via pandoc avant traduction.

## Points de vigilance
1. **DIAHO = 迪亚霍** (décision explicite JC), pas 迪奥.
2. Documents juridiques : **Renard briefe avant**, pas après.
3. La traduction ZH d'un contrat **ne fait pas foi** — le texte source prime.
4. Conserver les marques de révision (`~~…~~`, `PROPOSITION : …`).
5. Noms propres chinois : substituer les noms officiels si JC les fournit.
