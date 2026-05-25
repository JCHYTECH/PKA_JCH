# Design — Agent Procurement Semi-Autonome PKA

**Date :** 2026-05-25  
**Auteur :** Dobby 🦉 (claude-sonnet-4-6)  
**Statut :** Approuvé par JCH  
**Projet :** Générique PKA — applicable à WildNexus, DIM3, Vetalyx et tout projet avec BOM

---

## 1. Objectif

Créer un agent procurement semi-autonome capable de lire une BOM (Bill of Materials), consulter les APIs Mouser et DigiKey, enrichir la BOM avec prix/stock/alternatives, détecter l'obsolescence, et préparer un rapport de validation — sans jamais passer commande sans accord explicite de JCH.

---

## 2. Architecture générale

```
JCH → Dobby → /procurement [projet] [bom_file]
                    ↓
                  Forge (subagent Claude — orchestrateur)
                    ↓
        ┌─────────────┬─────────────┬─────────────┐
   bom_parser    api_client    bom_writer   report_writer
   (.xlsx/.csv)  (Mouser/DK)  (BOM enrichi) (TEAM_Inbox)
```

### Composants

| Script | Chemin | Rôle |
|---|---|---|
| `bom_parser.py` | `scripts/procurement/` | Lit Excel ou CSV/MD → JSON normalisé |
| `api_client.py` | `scripts/procurement/` | Appels Mouser/DigiKey ou simulation |
| `bom_writer.py` | `scripts/procurement/` | Réécrit le BOM source avec colonnes enrichies |
| `report_writer.py` | `scripts/procurement/` | Génère le rapport Markdown daté dans `TEAM_Inbox/` |

**Forge** reçoit le JSON normalisé, raisonne sur les alternatives et l'obsolescence, orchestre les scripts d'écriture.  
**Dobby** invoque Forge, présente le rapport à JCH, attend la validation avant toute action suivante.

---

## 3. Formats BOM acceptés

### 3.1 Excel (`.xlsx`)
- Détection automatique si extension `.xlsx`
- Feuille active par défaut (ou feuille nommée `BOM` si présente)
- Ligne 1 ou 2 considérée comme header (skip lignes de titre fusionnées)

### 3.2 CSV
- Séparateur `,` ou `;` (auto-détecté)
- Encodage UTF-8

### 3.3 Markdown (`.md`)
- Table Markdown standard parsée ligne par ligne
- Colonnes reconnues par nom (insensible à la casse)

### 3.4 Colonnes minimales requises (tous formats)

| Colonne | Obligatoire | Description |
|---|---|---|
| `ref` | ✅ | Référence schéma (ex. U1, C3) |
| `description` | ✅ | Nom composant |
| `qty` | ✅ | Quantité |
| `mpn` | Recommandé | Manufacturer Part Number |
| `preferred_supplier` | Optionnel | Mouser / DigiKey / Farnell… |
| `category` | Optionnel | MCU, Capteur, Passif… |
| `notes` | Optionnel | Contraintes ou variantes |

---

## 4. Modèle de données interne (JSON normalisé)

```json
{
  "project": "WILDNEXUS",
  "bom_source": "WILDNEXUS_BOM_P0_v0.2.xlsx",
  "generated_at": "2026-05-25T14:00:00",
  "components": [
    {
      "ref": "U1",
      "description": "ESP32-S3-WROOM-1U-N8R8",
      "qty": 5,
      "category": "MCU",
      "preferred_supplier": "Mouser",
      "mpn": "ESP32-S3-WROOM-1U-N8R8",
      "notes": "",
      "price_unit": 5.36,
      "currency": "EUR",
      "stock_qty": 1200,
      "lead_time_days": 2,
      "obsolete": false,
      "alternatives": [],
      "supplier_url": "https://www.mouser.be/...",
      "simulation": false
    }
  ]
}
```

---

## 5. Intégration API

### 5.1 Fournisseurs supportés

| Fournisseur | API | Quota gratuit |
|---|---|---|
| Mouser | Search API v2 | 1 000 req/jour |
| DigiKey | Product Search API v4 | Sandbox disponible |

### 5.2 Configuration (`.env` local, jamais commité)

```env
MOUSER_API_KEY=xxx
DIGIKEY_CLIENT_ID=xxx
DIGIKEY_CLIENT_SECRET=xxx
```

`api_client.py` détecte la présence des clés au démarrage et bascule automatiquement entre mode réel et mode simulation.

### 5.3 Provisioning API

1. **Mouser** : inscription sur [developer.mouser.com](https://developer.mouser.com) → créer une application → copier la clé dans `.env`
2. **DigiKey** : inscription sur [developer.digikey.com](https://developer.digikey.com) → créer une app → OAuth2 client credentials → copier `client_id` et `client_secret`

### 5.4 Mode simulation (aucune clé)

- `api_client.py` retourne des données mockées réalistes
- Chaque ligne enrichie porte le flag `"simulation": true`
- Le rapport affiche `⚠️ [SIMULATION]` en en-tête
- La BOM enrichie inclut une colonne `Simulation` = `OUI`

---

## 6. Logique Forge (raisonnement LLM)

Forge reçoit le JSON normalisé complet et exécute dans l'ordre :

1. **Détection obsolescence** — composant marqué EOL ou stock = 0 depuis > 3 mois → flag `🔴 OBSOLETE`
2. **Génération alternatives** — pour tout composant obsolète ou rupture stock : 2 alternatives minimum, même footprint si possible
3. **Scoring fournisseur** — applique les critères de la politique procurement PKA (fiabilité, centralisation, délai, coût)
4. **Préparation panier** — regroupe par fournisseur, calcule coût total livré (avec frais de port)
5. **Vérification budget** — si règle projet définie (ex. WildNexus : 1 000 € max), signalement si dépassement
6. **Rédaction rapport** — synthèse en langage naturel, prête pour validation JCH

---

## 7. Sorties

### 7.1 BOM enrichi

Fichier source mis à jour avec colonnes supplémentaires :

| Colonne ajoutée | Contenu |
|---|---|
| `Prix unit. (EUR)` | Prix unitaire fournisseur |
| `Stock` | Quantité disponible |
| `Délai (j)` | Lead time en jours ouvrés |
| `Obsolète` | OUI / NON / ⚠️ À VÉRIFIER |
| `Alternative` | MPN alternatif recommandé |
| `URL fournisseur` | Lien direct produit |
| `Simulation` | OUI si mode dégradé |

**Règle de versionnage** : avant écrasement, copier `BOM_vX.Y.xlsx` → `BOM_vX.Y-1.xlsx` (via `pka-file-versioning`).

### 7.2 Rapport Markdown

Chemin : `TEAM_Inbox/YYYY-MM-DD_Forge_procurement_[projet].md`

Structure obligatoire :
```
# Rapport Procurement — [PROJET] — YYYY-MM-DD
## Résumé
## Composants analysés
## Alertes (obsolescence, rupture stock, budget)
## Paniers recommandés (par fournisseur)
## Alternatives proposées
## Décisions en attente JCH
## Prochaines étapes (après validation)
```

---

## 8. Flux de validation JCH

```
Forge génère rapport + BOM enrichi
        ↓
Dobby présente résumé à JCH
        ↓
JCH : ✅ Valider | ✏️ Modifier | ❌ Bloquer
        ↓ (si ✅)
Dobby génère cart summary (liens directs fournisseurs)
— aucune commande automatique, jamais
```

La validation JCH est un **point de non-retour explicite**. L'agent ne génère pas de panier sans réponse affirmative.

---

## 9. Gestion d'erreurs

| Cas | Comportement |
|---|---|
| Composant non trouvé par MPN | Forge cherche par description, sinon flag `⚠️ MANUEL` |
| Stock = 0 | 2 alternatives minimum obligatoires |
| Obsolescence détectée | Flag `🔴 OBSOLETE` + alternative obligatoire |
| Budget dépassé | Signalement Dobby avant validation, ligne rouge dans rapport |
| API timeout | Retry ×2, puis mode simulation partielle pour ce composant |
| Format BOM non reconnu | Erreur explicite avec liste des colonnes manquantes |

---

## 10. Déclenchement

```
/procurement [projet] [chemin_bom]
```

Exemples :
```
/procurement WILDNEXUS JCH_Inbox/03_PROJECTS/03_WILDNEXUS/.../WILDNEXUS_BOM_P0_v0.2.xlsx
/procurement DIM3 JCH_Inbox/09_DIM3/bom_dim3_v1.csv
```

Si aucun argument : Dobby demande le projet et le fichier BOM à JCH.

---

## 11. Hors périmètre (v1)

- Commande automatique (jamais, par design)
- Intégration Farnell / RS / TME (v2)
- Comparaison multi-fournisseurs automatique (v2 — Forge compare manuellement en v1)
- Interface web ou dashboard (hors PKA CLI)
- Gestion des délais douaniers / taxes import (hors UE)
