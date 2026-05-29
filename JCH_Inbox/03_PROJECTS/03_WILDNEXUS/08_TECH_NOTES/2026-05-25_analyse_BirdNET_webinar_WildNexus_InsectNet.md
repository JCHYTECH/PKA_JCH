# Analyse [[BirdNET]] — Webinar Open Ecoacoustics #2

> **Date :** 2026-05-25
> **Source :** Transcript NoteGPT — « [[BirdNET]]: Tips, Tricks, and Insights for Ecoacoustic Analysis »
> **Intervenants :** Phil Eichinski (QUT), Nina Scarpelli (Museums Victoria), Kellen Alexander (QUT / BirdLife Australia)
> **Analyse par :** [[Furet]] 🦡 (recherche) — pour l'équipe WildNexus + InsectNet
> **Tags :** #[[BirdNET]] #ecoacoustics #embeddings #classification #insectnet #bioacoustique #machine-learning #validation

---

## Résumé exécutif

Ce webinar de l'Open Ecoacoustics Community (Australie) livre un retour d'expérience concret sur [[BirdNET]] — le modèle de classification acoustique le plus utilisé en écoacoustique. Trois chercheurs partagent leurs astuces, leurs échecs et leurs workflows. Les points saillants pour nos projets sont : **(1)** la supériorité du clustering d'embeddings sur les scores de confiance bruts, **(2)** l'importance critique de faire matcher les données d'entraînement avec l'environnement de déploiement, et **(3)** le pipeline de validation manuelle pragmatique qui change tout.

---

## 1. Ce qu'il faut retenir pour WildNexus

### 1.1 Architecture [[BirdNET]] — rappel utile

```
Audio → segmentation 3s → embeddings (espace latent) → classification head → espèce + score
```

Les **embeddings** sont la représentation interne du modèle : des vecteurs où des sons similaires sont proches dans l'espace. On peut les extraire sans passer par la classification head, ce qui ouvre des possibilités au-delà de la prédiction d'espèce brute.

### 1.2 Les 6 pièges identifiés — et comment on les évite

| Piège | Description | Contre-mesure WildNexus |
|-------|-------------|--------------------------|
| **Données d'entraînement ≠ environnement** | Les cochons près des pièges font des sons différents des cochons en liberté → le recognizer ne généralise pas | Toujours entraîner sur des données du site cible ou valider rigoureusement |
| **Faux positifs par corrélation parasite** | « Eau qui clapote = pélican » parce que dans les données d'entraînement, les pélicans étaient toujours près de l'eau | Validation manuelle systématique des espèces rares/inattendues |
| **Espèces confusibles non incluses** | Koala confondu avec cochon → ajouter le koala comme classe améliore les deux | Inclure les espèces confusibles connues dans le recognizer, même si on ne les cible pas |
| **Scores de confiance non fiables** | Des vrais positifs à 0.4, des faux positifs à 0.9 — aucun seuil magique | Ne pas se fier au score seul. Utiliser le **clustering d'embeddings (HDBSCAN)** |
| **Surestimation de la richesse spécifique** | Même à haut seuil de confiance, [[BirdNET]] surestime le nombre d'espèces présentes | Validation experte avant toute publication de liste d'espèces |
| **Appels stéréotypés vs non-stéréotypés** | Koala : 39 segments suffisent. Cochon : beaucoup plus. Les sons sans pattern demandent plus de données. | Anticiper plus de données d'entraînement pour les espèces à vocalises variables |

### 1.3 Le workflow de validation qui change tout (Kellen Alexander)

La méthode « annoter seulement les faux positifs » :
1. Charger des milliers de segments dans Raven
2. Utiliser « Choose Measurements → Begin File » pour tagger le nom du fichier
3. Annoter **uniquement les faux positifs** (pas les vrais)
4. Un script extrait les faux positifs → le reste = vrais positifs

**Gain :** ne pas perdre de temps à labeliser 2000 vrais positifs identiques. Applicable directement à notre pipeline WildNexus.

### 1.4 Clustering d'embeddings > scores de confiance

Plusieurs cas concrets où le clustering HDBSCAN sur les embeddings a surpassé le meilleur seuil de confiance :
- **Common Myna** : aucun pattern dans les scores de confiance, mais le clustering a parfaitement séparé vrais positifs et bruit
- **Eastern Bristlebird** : des milliers de détections, majoritairement des faux positifs → cluster 8 contenait tous les vrais appels

**Implication pour nous :** intégrer le clustering d'embeddings dans le pipeline WildNexus comme étape de post-traitement standard, plutôt que de se battre avec des seuils.

---

## 2. Ce qu'il faut retenir pour InsectNet

### 2.1 Le pipeline [[BirdNET]] est transposable à l'insecte

Le cœur du message : **le modèle d'embeddings + classification head n'est pas limité aux oiseaux.** Phil Eichinski le dit explicitement : on peut entraîner un recognizer pour n'importe quelle espèce, y compris non-oiseau, si on a des données d'entraînement.

Points directement applicables à InsectNet :

| Enseignement [[BirdNET]] | Application InsectNet |
|----------------------|----------------------|
| Les **appels non-stéréotypés** demandent plus de données d'entraînement | Les stridulations d'insectes sont souvent stéréotypées (orthoptères) → bon candidat. Mais les sons de vol ou de déplacement sont variables → prévoir plus de données |
| **3 secondes** est le format d'entrée standard | Segmenter les enregistrements InsectNet en fenêtres de 3s pour compatibilité |
| **Inclure les espèces confusibles** comme classes | Ajouter les orthoptères/amphibiens confusibles dans le modèle InsectNet |
| Le **clustering d'embeddings** fonctionne pour tout type de son | Utiliser HDBSCAN pour séparer les stridulations d'insectes du bruit de fond sans seuil manuel |

### 2.2 Points d'attention spécifiques InsectNet

- **Bruit de fond insecte constant** : plusieurs intervenants mentionnent que quand un insecte est présent en fond dans les données d'entraînement mais absent sur le site de déploiement, le modèle peut mal généraliser. Pour InsectNet, c'est un risque majeur — le paysage sonore insecte varie énormément par site et saison.
- **Fréquence filtering** : mentionné comme utile pour les espèces nocturnes à basse fréquence → exploitable pour isoler certaines bandes de stridulation.
- **Volume de données** : le transcript ne donne pas de chiffres pour les insectes, mais le principe « appels stéréotypés = moins de données » suggère que les stridulations rythmiques d'orthoptères pourraient nécessiter relativement peu d'exemples.

---

## 3. Recommandations concrètes

### Pour WildNexus (priorité immédiate)

1. **Intégrer le clustering HDBSCAN** dans le pipeline de post-traitement audio — ne pas se contenter des scores [[BirdNET]] bruts
2. **Adopter le workflow Raven** de Kellen Alexander pour la validation à grande échelle (script false-positive dispo sur demande)
3. **Documenter les espèces confusibles** par région dans notre base de connaissances — les inclure systématiquement dans les recognizers
4. **Former les recognizers sur des données locales** — éviter de déployer un modèle entraîné sur données australiennes sans validation sur nos sites
5. **Ne jamais publier de liste d'espèces** sans validation experte — [[BirdNET]] surestime systématiquement

### Pour InsectNet (exploration)

1. **Tester [[BirdNET]] avec des stridulations d'orthoptères** — utiliser le mode custom recognizer pour entraîner sur quelques espèces cibles
2. **Expérimenter le clustering d'embeddings** sur les enregistrements InsectNet existants — voir si ça sépare proprement les signaux du bruit
3. **Segmenter en fenêtres de 3 secondes** pour compatibilité avec le pipeline [[BirdNET]] standard
4. **Cartographier les espèces confusibles** insectes par site — le problème « koala vs cochon » aura son équivalent insecte

---

## 4. Ressources mentionnées

- **[[BirdNET]] GUI** : permet d'extraire les embeddings sans coder
- **HDBSCAN** : algorithme de clustering utilisé pour les embeddings
- **Raven (Cornell)** : interface de validation avec « Choose Measurements → Begin File »
- **Script false-positive Kellen Alexander** : dispo sur demande par [[email]]
- **Ecosounds** : interface de validation alternative
- **Open Ecoacoustics Workshop** : 17 novembre, Perth — prochaine édition
- **International Ecoacoustics Congress** : juillet 2026, Brisbane

---

## Source

Transcript original : `JCH_Inbox/07_ARCHIVES/NoteGPT_TRANSCRIPT_BirdNET  Tips, Tricks, and Insights for Ecoacoustic Analysis - Open Ecoacoustics Webinar Series #2.txt`
