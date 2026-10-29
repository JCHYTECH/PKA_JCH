---
name: wildnexus-bom
description: Générer ou mettre à jour le BOM WildNexus P0 en Excel multi-onglets depuis les ADRs et données hardware. Déclencher sur "génère le BOM", "mets à jour le budget", "shortlist achat", "BOM WildNexus".
---

# Skill — wildnexus-bom

## Déclencheurs
- "génère le BOM", "mets à jour le BOM"
- "shortlist achat", "liste de composants"
- "mets à jour le budget WildNexus"
- "BOM Excel", "fichier achat"

## Contexte système
- BOM source (Markdown) : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM/`
- Script générateur : `generate_bom_excel.py` dans le même dossier
- ADR Index : `JCH_Inbox/03_PROJECTS/03_WILDNEXUS/02_DECISIONS/WILDNEXUS_ADR_INDEX.md`
- Budget P0 : `03_P0_ENGINEERING/08_BUDGET_MODELES/WILDNEXUS_P0_BUDGET_RANGE.md`
- Enveloppe : **1 000 € max** — dépassement bloquant sauf décision JCH
- Règle > 50 € : signaler à JCH avant commande

## Procédure

### 1. Vérifier l'état des ADRs
- Lire `WILDNEXUS_ADR_INDEX.md`
- Tous les ADRs doivent être **Accepté** avant génération BOM finale
- Tout ADR encore "Proposé" → signaler à JCH et indiquer l'impact sur les lignes concernées

### 2. Versionner le fichier existant
- Appliquer `pka-file-versioning` : copier `WILDNEXUS_BOM_P0_vX.Y.xlsx` → `WILDNEXUS_BOM_P0_vX.Y-1.xlsx` avant écrasement

### 3. Mettre à jour le script ou les données
- Si nouvelles données (prix, composants, décisions) → modifier `generate_bom_excel.py`
- Incrémenter la version dans le nom du fichier de sortie (vX.Y)
- Mettre à jour la date en haut de chaque feuille

### 4. Régénérer le fichier Excel
```bash
cd /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/03_WILDNEXUS/03_P0_ENGINEERING/07_PROCUREMENT_BOM
python3 generate_bom_excel.py
```

### 5. Structure Excel obligatoire (4 onglets minimum)
| Onglet | Contenu |
|--------|---------|
| Option A — Banc rapide | Composants commandables immédiatement |
| Option B — Terrain compact | Composants après résultats M-02 |
| Budget consolidé | Synthèse A+B, frais port, marge, réserve vs enveloppe |
| ADR & Paniers | Statut ADRs + stratégie paniers fournisseurs |

### 6. Conventions de style Excel
- Header ligne 1 : fusion, titre + date, bleu foncé `#1F4E79`
- Header ligne 2 : colonnes, fond bleu `#1F4E79`, texte blanc, gras
- Lignes alternées : fond `#D6E4F0`
- Cellules ⚠️ : fond `#FFF2CC`
- Cellules ✅ : fond `#E2EFDA`
- Freeze : ligne 2 + colonnes A-B
- Wrap text : toutes les cellules

### 7. Colonnes obligatoires BOM
`#` | `Composant` | `Référence précise (MPN)` | `Fournisseur` | `Qté` | `Prix unit. TTC` | `Total` | `Délai` | `Risque supply` | `Statut` | `Note` | `Action requise`

**Règles absolues :**
- MPN (référence fabricant) obligatoire — jamais de description générique
- Ne jamais acheter microSD consumer — industrial grade uniquement
- Lentille : ne pas descendre sous 30 €/pièce
- PPK2 : non négociable, priorité absolue dans Option A
- Toujours vérifier EU868 pour modules [[LoRa]]

### 8. Rapport à JCH
Après génération :
- Confirmer le chemin du fichier
- Afficher le total consolidé vs enveloppe
- Signaler tout composant > 50 € ou tout total projeté > 900 €
- Signaler les ADRs non encore acceptés qui bloquent des lignes BOM
