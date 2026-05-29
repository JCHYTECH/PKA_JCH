# [[Insectes vol]] — Rapport préliminaire de faisabilité

## Projet

Reconnaissance bioacoustique d’insectes en vol  
Approche inspirée de [[BirdNET]] appliquée aux insectes européens.

Version : Préliminaire  
Date : 2026-05-24

---

# 1. Contexte du projet

L’objectif du projet est d’évaluer la faisabilité technique d’un système capable de :

- détecter la présence d’insectes en vol ;
- reconnaître certains groupes d’insectes ;
- éventuellement identifier certaines espèces ;
- fonctionner sur matériel léger type [[Raspberry Pi]] ;
- évoluer vers un système autonome terrain basse consommation.

Le projet s’inscrit dans une logique :
- bioacoustique ;
- edge AI ;
- monitoring biodiversité ;
- capteurs environnementaux ;
- analyse locale ou hybride cloud.

---

# 2. Différence fondamentale avec [[BirdNET]]

[[BirdNET]] reconnaît principalement :
- chants ;
- cris ;
- vocalisations.

Dans le cas des insectes, le signal utile est souvent :
- le battement d’ailes ;
- le spectre harmonique du vol ;
- la signature fréquentielle ;
- la modulation du bourdonnement.

Le problème est plus complexe car :
- le signal est faible ;
- les fréquences se recouvrent ;
- le bruit ambiant est important ;
- les conditions météo influencent fortement le signal.

---

# 3. Architecture conceptuelle envisagée

## Niveau 1 — Détection

Déterminer :
“un insecte volant est présent”.

## Niveau 2 — Classification grossière

Exemples :
- abeille ;
- bourdon ;
- moustique ;
- mouche ;
- papillon ;
- frelon.

## Niveau 3 — Identification espèce

Exemple :
- Bombus terrestris ;
- Apis mellifera.

Cette étape nécessite :
- énormément de données ;
- diversité environnementale ;
- metadata riches.

---

# 4. État de l’art scientifique

Des publications scientifiques montrent qu’il est possible de distinguer :

- abeilles ;
- bourdons ;
- frelons ;
- abeilles solitaires ;

à partir du son de vol.

Les méthodes utilisées combinent :
- fréquence fondamentale ;
- harmoniques ;
- MFCC ;
- spectrogrammes ;
- SVM ;
- CNN.

Certaines études obtiennent des précisions élevées en environnement contrôlé.

Cependant :
- les performances chutent en extérieur ;
- le vent et le bruit sont critiques ;
- la distance micro/insecte influence énormément le résultat.

---

# 5. Faisabilité spécifique : abeille vs bourdon

## Conclusion préliminaire

La distinction :
- abeille domestique ;
- bourdon ;

semble techniquement faisable.

Mais :
- pas avec une précision parfaite ;
- probablement sous forme probabiliste.

## Difficultés

Les fréquences de battement se recouvrent partiellement.

La fréquence seule n’est pas suffisante.

Il faut combiner :
- fondamentale ;
- harmonique ;
- texture spectrale ;
- dynamique du signal ;
- intensité ;
- durée.

---

# 6. Datasets identifiés

## 6.1 WINGBEATS

Source :
https://www.kaggle.com/datasets/potamitis/wingbeats

### Contenu

- 279 000+ fichiers WAV ;
- moustiques ;
- battements d’ailes ;
- données propres.

### Téléchargement automatisé

Oui via API Kaggle.

### Intérêt

Excellent dataset de départ.

### Limites

- principalement moustiques ;
- environnement contrôlé.

---

## 6.2 HumBugDB

Sources :
- https://github.com/HumBug-Mosquito/HumBugDB
- https://zenodo.org/records/4904800

### Contenu

- 20 heures audio ;
- 36 espèces ;
- bruit réel terrain.

### Intérêt

Très important pour :
- robustesse ;
- environnement naturel ;
- IA réaliste.

---

## 6.3 ECOSoundSet

Source :
https://arxiv.org/abs/2504.20776

### Particularité

Dataset européen :
- Belgique ;
- France ;
- Allemagne ;
- Pays-Bas ;
- Suisse ;
- etc.

### Contenu

Principalement :
- orthoptères ;
- cigales ;
- stridulations.

### Intérêt

Très stratégique pour biodiversité européenne.

---

## 6.4 InsectSound1000

Source :
https://www.nature.com/articles/s41597-024-03301-4

### Contenu

- 169 000+ samples ;
- qualité élevée.

### Intérêt

Très utile pour :
- deep learning ;
- modèles robustes.

---

# 7. Vérification licences et automatisation

| Dataset | Licence | Download auto | API |
|---|---|---|---|
| WINGBEATS | Kaggle | Oui | API Kaggle |
| HumBugDB | Ouverte recherche | Oui | GitHub/Zenodo |
| ECOSoundSet | Scientifique ouverte | Oui | Scripts possibles |
| InsectSound1000 | Recherche ouverte | Oui | Download direct |

Conclusion :
le téléchargement automatisé est globalement possible.

---

# 8. Choix hardware

## 8.1 [[Raspberry Pi]]

Plateforme recommandée pour démarrer.

Avantages :
- puissance suffisante ;
- TensorFlow Lite ;
- stockage local ;
- spectrogrammes ;
- IA embarquée.

Version recommandée :
- [[Raspberry Pi 5]].

---

## 8.2 [[ESP32]]

Possible uniquement :
- en préfiltrage ;
- détection simple ;
- ultra basse consommation.

Limites :
- RAM ;
- traitement temps réel complexe ;
- IA avancée difficile.

---

# 9. Microphones

## Conclusion importante

Pas nécessairement besoin d’un micro “scientifique”.

Mais :
- le choix du micro reste critique.

---

## 9.1 Prototype initial

Possible avec :
- micro USB ;
- micro MEMS ;
- micro électret de bonne qualité.

---

## 9.2 Point critique réel

Le problème principal est :
- la distance ;
- le vent ;
- le bruit environnemental.

---

## 9.3 Recommandation terrain

Prévoir :
- bonnette anti-vent ;
- placement proche des fleurs ;
- distance cible :
  - 20 à 50 cm.

---

# 10. Pipeline IA recommandé

## Étape 1

Télécharger datasets.

## Étape 2

Créer :
- spectrogrammes Mel ;
- extraction MFCC.

## Étape 3

Tester :
- SVM ;
- Random Forest.

## Étape 4

Tester CNN léger.

## Étape 5

Déploiement [[Raspberry Pi]].

---

# 11. Metadata à intégrer absolument

Le comportement acoustique des insectes dépend fortement de :

- température ;
- humidité ;
- heure ;
- météo ;
- habitat ;
- saison ;
- phase lunaire.

Ces données doivent être stockées avec chaque enregistrement.

---

# 12. Proposition d’expérience minimale

## Objectif

Tester :
abeille vs bourdon.

---

## Matériel

- [[Raspberry Pi]] ;
- micro USB/MEMS ;
- bonnette anti-vent.

---

## Méthode

Collecter :
- 100 à 200 sons abeilles ;
- 100 à 200 sons bourdons.

Conditions :
- même micro ;
- même distance ;
- environnement similaire.

---

## Traitement

Découpage :
- segments 0,5 à 1 seconde.

Extraction :
- fréquence dominante ;
- fondamentale ;
- harmoniques ;
- MFCC ;
- spectrogrammes.

---

## Critère décisionnel

Si précision :
- >85 % :
  poursuite fortement recommandée.

Si :
- 70–85 % :
  faisabilité probable avec amélioration dataset.

Si :
- <70 % :
  mieux viser :
  “groupe pollinisateur”
  plutôt que
  “espèce”.

---

# 13. Vision stratégique du projet

Le véritable actif stratégique pourrait devenir :

un dataset propriétaire européen de sons d’insectes en environnement réel.

Particulièrement :
- Belgique ;
- France ;
- Italie ;
- habitats variés.

---

# 14. Conclusion générale

Le projet semble techniquement faisable pour :

- détection ;
- classification grossière ;
- reconnaissance probabiliste.

La reconnaissance parfaite espèce par espèce paraît beaucoup plus complexe.

La voie recommandée :

1. Prototype [[Raspberry Pi]] ;
2. Collecte données terrain ;
3. Pipeline IA simple ;
4. Validation scientifique ;
5. Extension progressive.

Le principal verrou ne semble pas être :
- la puissance informatique ;

mais plutôt :
- la qualité du dataset réel terrain.
