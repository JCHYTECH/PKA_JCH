# Procédure de traduction bilingue — Jade 🦩 (VETALYX / DIAHO)

> **Objet :** cadre unique pour toute traduction FR/EN ↔ ZH impliquant DIAHO (et les partenaires chinois de VETALYX).
> **Chargée au bootstrap** (voir `docs/system/dobby-memory-bootstrap.md` Phase 1).
> **Créée :** 2026-08-21 par Dobby 🦉 — consolidation de `TEAM/jade.md`, des livrables Jade et de la règle projet VETALYX/DIAHO.
> **Référence modèle :** `docs/system/models-reference.md` (Traduction EN-ZH → Qwen/Claude + Jade ; le format et la Tone Note restent définis par Jade).

---

## 1. Règle transverse (non négociable)

**Tout document contractuel ou stratégique impliquant DIAHO est bilingue dès la première rédaction.** Jade co-intervient avec Renard **dès le départ**, pas en bout de chaîne.

S'applique aux contrats, Quality Agreement, statuts, checklists, courriers, analyses juridiques et tout livrable destiné aux partenaires chinois.

---

## 2. Acteurs et rôles

| Acteur | Rôle |
|--------|------|
| **Jade 🦩** | Traductrice scientifique & juridique EN↔ZH + analyste culturelle. Traduit le sens, jamais mot-à-mot. |
| **Renard 🦊** | Conseil juridique. **Briefe Jade sur le registre et les termes clés AVANT toute traduction juridique.** |
| **Dobby 🦉** | Orchestration, révision finale, livraison et archivage. |
| **Vasco 🐺** | Revue produit/qualité sur les documents qualité (Quality Agreement), le cas échéant. |

---

## 3. Les trois sens de traduction

### 3.1 FR → ZH (documents sortants, vers DIAHO)
- Format **bilingue paragraphe-par-paragraphe** (FR puis ZH, ou tableau 2 colonnes).
- En-tête : `Rédigé par / Traduit par / Révisé par` en FR **et** ZH.
- **Pas de Tone Note** (réservée aux documents entrants).

### 3.2 ZH → FR/EN (documents entrants, des Chinois)
- Traduction **sens-pour-sens**, jamais mot-à-mot.
- **Tone Note obligatoire** en fin de document (voir §5).
- Flagger les termes sans équivalent propre → **traduction explicative**, jamais d'approximation.

### 3.3 EN → ZH (document contractuel rédigé en anglais, ex. Quality Agreement)
- Bilingue EN/ZH, même format que FR→ZH.
- Le texte anglais fait foi ; la ZH est une traduction de travail.

---

## 4. Format bilingue (convention)

- **Titres :** `## 1. Introduction | 1. 引言`
- **Paragraphes :** paragraphe source → ligne vide → paragraphe cible → ligne vide.
- **Listes :** liste source complète → liste cible complète (sauf glossaires : terme par terme).
- **Tableaux :** deux blocs (source puis cible), ou tableau à 2 colonnes si court.
- **En-tête de fichier :** date, source, `Traduit par Jade / Orchestré par Dobby`, sens, terminologie.
- **Note finale systématique :** « Le texte source fait foi ; la version ZH est une traduction de travail à valider par un conseil juridique avant transmission à DIAHO. »

---

## 5. Tone Note (obligatoire après chaque ZH → FR/EN)

```
TONE NOTE
---------
Registre : [formal / semi-formal / cautious / warm / transactional]
Température : [registre émotionnel global]
Signaux : [ce qui se joue entre les lignes, à signaler à JC]
Lecture : [interprétation d'intention de Jade]
```

Ne **jamais lisser** un signal que JC doit entendre.

---

## 6. Terminologie figée (à réutiliser — ne pas réinventer)

| Source | Cible | Note |
|--------|-------|------|
| DIAHO / DiaHo / Diaho | **迪亚霍** | ⚠️ Décision JC 2026-08-21 (conforme courrier Dr Wu). **Ne pas utiliser 迪奥.** Substituer par le nom chinois officiel si JC le fournit. |
| Zheda Dixun | 浙大迪迅 | |
| VetalyX / Vetalyx | VetalyX | latin conservé |
| Contrat-cadre | 框架协议 | |
| Quality Agreement | 质量协议 | |
| LFIA (lateral flow immunoassay) | 侧向层析免疫分析 | acronyme conservé au 1er emploi |
| Certificate of Analysis (CoA) | 分析证书（CoA） | |
| IFU (Instructions for Use) | 使用说明书（IFU） | |
| KOL | 关键意见领袖（KOL） | |
| Savoir-Faire | 专有技术 | |
| Dossiers Réglementaires | 监管档案 | |
| Représentant Autorisé Européen | 欧盟授权代表 | |
| UBO | 最终受益人 | |
| Droit de premier refus | 优先购买权 | |
| Non-contournement | 不规避 | |
| Non-concurrence | 不竞争 | |
| Change Control | 变更控制 | |
| Incoterms | 国际贸易术语（Incoterms） | |
| Force majeure | 不可抗力 | |
| CSA (Code des sociétés et des associations) | 《公司与协会法典》（CSA） | |
| SRL | 有限责任公司（SRL） | |
| Batch / Lot | 批次 | |
| Shelf life | 货架期 | |
| Traceability | 可追溯性 | |
| Recall | 召回 | |

> Registre : 商务专业 sans rigidité. Éviter les formules administratives excessives (兹, 特此). Le « 您 » systématique marque le respect dû au partenaire.

---

## 7. Nommage et livraison

- **Nommage :** `YYYY-MM-DD_jade_traduction-[objet]-[FR|EN]-ZH.md`
- **Dépôt :** `JCH_Inbox/03_PROJECTS/08_VETALYX/legal/contrat-diaho/` (archivage canonique des contrats DIAHO). **Exception — documents de constitution avec les partenaires chinois** (statuts SRL, contrat-cadre) : `JCH_Inbox/03_PROJECTS/08_VETALYX/legal/Creation Vetalyx avec Chinois/`. + copie livrable dans `TEAM_Inbox/` si demandé.
- **Sortie :** version de travail en `.md` (les `.docx` de l'inbox sont convertis via pandoc avant traduction) ; les livrables formels destinés à transmission vers DIAHO peuvent rester en `.docx`.

---

## 8. Points de vigilance

1. **Translittération DIAHO = 迪亚霍** (pas 迪奥) — décision explicite JC.
2. Noms propres chinois : si JC dispose des noms officiels des entités, les substituer.
3. Documents juridiques : **Renard briefe avant**, pas après.
4. Les textes source avec marques de révision (`~~…~~`, `PROPOSITION : …`) sont traduits **fidèlement**, marques conservées.
5. La traduction ZH d'un document contractuel **ne fait pas foi** — le texte source prime.
