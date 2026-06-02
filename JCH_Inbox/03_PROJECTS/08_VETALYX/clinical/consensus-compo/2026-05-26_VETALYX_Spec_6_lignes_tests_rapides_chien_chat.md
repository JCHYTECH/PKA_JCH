---
date: 2026-05-26
project: VETALYX
type: product-spec
status: draft-v1
owner: [[Dobby]]
clinical_lead: [[Vasco]]
scientific_review: [[Clio]]
topic: Specification 6 lignes allergenes tests rapides chien chat
---

# VETALYX - Specification tests rapides 6 lignes chien/chat

## 1. Principe de design

Chaque "ligne" doit etre un **groupe allergenique cliniquement actionnable**, pas un allergene isole sauf exception majeure. Avec seulement 6 lignes, il faut couvrir les familles les plus frequentes et les plus utiles pour l'orientation veterinaire.

Point de prudence : les tests IgE alimentaires ne doivent pas etre vendus comme diagnostic d'allergie alimentaire. Ils peuvent seulement aider a orienter un regime d'eviction, qui reste la reference clinique.

## 2. Chien - test rapide IgE respiratoire / aeroallergenes

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | House dust mites | Dermatophagoides farinae + Dermatophagoides pteronyssinus |
| 2 | Storage mites | Tyrophagus putrescentiae + Acarus siro + Lepidoglyphus destructor |
| 3 | Graminees | Phleum pratense/Timothy + Lolium + Dactylis + Festuca + Poa |
| 4 | Mauvaises herbes | Artemisia/mugwort + Ambrosia/ragweed + Plantago + Parietaria/Urticaceae |
| 5 | Arbres Europe | Betula/birch + Alnus/alder + Corylus/hazel + Quercus/oak + Fraxinus/ash ou Platanus/plane |
| 6 | Moisissures | Alternaria + Cladosporium + Aspergillus + Penicillium |

Option Mediterranee : remplacer une partie de la ligne "Arbres Europe" par olive + cypress/Cupressaceae.

## 3. Chien - test rapide IgE dermique / dermatite allergique

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | Puce | Ctenocephalides felis / flea saliva |
| 2 | House dust mites | D. farinae + D. pteronyssinus |
| 3 | Storage mites | Tyrophagus + Acarus + Lepidoglyphus |
| 4 | Levures cutanees | Malassezia pachydermatis |
| 5 | Pollens cutaneo-atopiques | Graminees mix + Artemisia/Plantago/Parietaria selon region |
| 6 | Moisissures environnementales | Alternaria + Cladosporium + Aspergillus + Penicillium |

Ne pas inclure "contact allergy" comme promesse principale : la dermatite de contact vraie est souvent non-IgE et mal servie par un test serum rapide.

## 4. Chien - test rapide IgE alimentaire

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | Boeuf | Beef proteins / bovine serum albumin si disponible |
| 2 | Lait / produits laitiers | Cow milk proteins |
| 3 | Poulet | Chicken proteins |
| 4 | Ble / cereales | Wheat +/- cereal mix si contraintes techniques |
| 5 | Oeuf | Egg white proteins |
| 6 | Soja | Soybean proteins |

Usage recommande : "food sensitization support", pas "food allergy diagnosis".

## 5. Chat - test rapide IgE respiratoire / aeroallergenes

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | House dust mites | D. farinae + D. pteronyssinus |
| 2 | Storage mites | Tyrophagus + Acarus + Lepidoglyphus |
| 3 | Graminees | Timothy/Phleum + Lolium + Dactylis + Poa |
| 4 | Arbres / herbes regionales | Betula/Alnus/Corylus ou olive/cypress en Mediterranee |
| 5 | Moisissures | Alternaria + Cladosporium + Aspergillus + Penicillium |
| 6 | Indoor insect allergens | Cockroach +/- moth/mosquito selon disponibilite fournisseur |

Chez le chat asthmatique, le test ne remplace pas le parcours respiratoire : examen clinique, imagerie, exclusion infectieuse/parasitaires selon contexte.

## 6. Chat - test rapide IgE dermique / dermatite allergique

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | Puce | Ctenocephalides felis / flea saliva |
| 2 | House dust mites | D. farinae + D. pteronyssinus |
| 3 | Storage mites | Tyrophagus + Acarus + Lepidoglyphus |
| 4 | Pollens | Graminees + weed/tree regional mix |
| 5 | Moisissures | Alternaria + Cladosporium + Aspergillus + Penicillium |
| 6 | Insectes piqueurs | Mosquito/insect bite mix si techniquement disponible ; sinon cockroach |

Priorite commerciale : "feline atopic skin syndrome / non-flea non-food hypersensitivity support", avec interpretation prudente.

## 7. Chat - test rapide IgE alimentaire

| Ligne | Groupe conseille | Composition recommandee |
|---:|---|---|
| 1 | Boeuf | Beef proteins |
| 2 | Poisson | Fish mix, idealement poisson blanc + saumon/thon selon exposition alimentaire |
| 3 | Poulet | Chicken proteins |
| 4 | Lait / produits laitiers | Cow milk proteins |
| 5 | Oeuf | Egg proteins |
| 6 | Ble / soja | Wheat + soybean, ou ligne separee selon contrainte technique locale |

Usage recommande : aide a la discussion du regime d'eviction, jamais diagnostic autonome.

## 8. Arbitrage si un seul test rapide par espece

Si VETALYX doit lancer un seul test chien et un seul test chat en P0 :

### Chien P0 unique

1. House dust mites.
2. Storage mites.
3. Flea saliva.
4. Grass pollen mix.
5. Weed/tree regional mix.
6. Mould mix.

### Chat P0 unique

1. Flea saliva.
2. House dust mites.
3. Storage mites.
4. Pollens regional mix.
5. Mould mix.
6. Food top-3 warning line : beef/fish/chicken only if the claim is clearly "sensitization support"; sinon indoor insects.

## 9. Sources

- ICADA canine atopic dermatitis treatment guidelines: https://pmc.ncbi.nlm.nih.gov/articles/PMC4537558/
- Canine atopic dermatitis diagnosis and allergen identification guidelines: https://bmcvetres.biomedcentral.com/articles/10.1186/s12917-015-0515-5
- Efficacy of diagnostic testing for allergen sensitization in canine atopic dermatitis - systematic review: https://pmc.ncbi.nlm.nih.gov/articles/PMC12133834/
- International seroprevalence survey of IgE sensitisation to Dermatophagoides farinae in atopic dogs: https://pmc.ncbi.nlm.nih.gov/articles/PMC9292188/
- Allergens in veterinary medicine: https://pmc.ncbi.nlm.nih.gov/articles/PMC4716287/
- Common food allergen sources in dogs and cats: https://pmc.ncbi.nlm.nih.gov/articles/PMC4710035/
- Can in vivo or in vitro tests diagnose adverse food reactions in dogs and cats?: https://link.springer.com/article/10.1186/s12917-017-1142-0
- Cutaneous manifestations of adverse food reactions in dogs and cats: https://link.springer.com/article/10.1186/s12917-019-1880-2
- MSD Veterinary Manual - Feline atopic dermatitis: https://www.msdvetmanual.com/integumentary-system/atopic-dermatitis/feline-atopic-dermatitis
- Review of feline allergic skin disease: https://pmc.ncbi.nlm.nih.gov/articles/PMC5606602/
