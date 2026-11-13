# Analyse comparative — PKA / WildNexus vs Savonia « Tekoälyä talleille »

> Dobby 🦉 — DeepSeek V4 — 2026-07-20
> Objectif : préparer l'argumentaire bilatéral pour le futur contact avec Savonia.
> Principe : honnêteté intellectuelle. On liste nos forces ET leurs forces. Pas de propagande.

---

## 1. Nos avantages (PKA → Savonia)

### 1.1 Autonomie énergétique (le gap #1)

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Alimentation** | Secteur 230V (RPi 4 ×4 + caméras) | 8×AA batteries → 60 jours autonome |
| **Consommation** | ~5–10W par RPi en continu | ~300µA deep sleep, ~80mA actif 3s |
| **Déploiement** | Nécessite prises électriques dans l'écurie | Poser le boîtier n'importe où, pas de câble |
| **Sécurité** | Câbles 230V dans environnement poussière/paille = risque feu | Basse tension 3.3V, aucun risque |

> **Impact** : nos modules peuvent être placés au-dessus des boxes, dans les combles, dans le grenier à foin — là où aucun câble électrique ne passe. Liberté totale de placement pour optimiser la couverture acoustique.

### 1.2 Edge AI embarquée (pas de dépendance serveur)

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Où tourne l'inférence** | Serveur NVIDIA DGX distant (après transfert SSH) | ESP32-S3 onboard (CNN 330K INT8 + FFT) |
| **Latence détection** | Heures (transfert programmé la nuit) | ~3.5 secondes après l'événement |
| **Dépendance réseau** | WiFi obligatoire pour transfert | Aucune — LoRa ou SD local |
| **Alerte temps réel** | Impossible avec archi actuelle | Oui — push/SMS immédiat via LoRa |

> **Impact** : un cheval qui se coince dans son box à 2h du matin. Avec Savonia, l'alerte arrive le lendemain matin quand les données sont transférées et traitées. Avec WildNexus, l'alerte part en 3 secondes via LoRa vers le téléphone du propriétaire.

### 1.3 Robustesse hardware & terrain

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Boîtier** | Aucun (RPi nu + caméra USB ?) | NEMA 4X IP67 — poussière, ammoniac, humidité |
| **Température** | 0–40°C (RPi standard) | −20 à +60°C (spécifié pour outdoor) |
| **Résistance environnement** | Non conçu pour environnement agricole | Joints silicone, ventilation passive, anti-condensation |
| **Micros** | Probablement micros USB consumer | MEMS I2S Knowles SPH0645LM4H-B, SNR 65dB, bande 20Hz–10kHz |

> **Impact** : une écurie est un environnement hostile — ammoniac urinaire, poussière de foin, humidité, rats qui grignotent les câbles. Nos boîtiers sont conçus pour ça. Leurs RPi nus ne tiendront pas une saison.

### 1.4 Coût & scalabilité

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Coût par nœud** | ~€80–100 (RPi 4) + caméra + micro + câbles + alim | ~€85–110 tout compris (PCB, ESP32-S3, micros, LoRa, batterie, boîtier) |
| **Installation** | Électricien nécessaire (prises 230V) | Aucune — autoportant |
| **Passage à 50 boxes** | 50 prises électriques à installer | 50 boîtiers posés en 1 journée |
| **Maintenance** | Mises à jour manuelles par SSH | OTA via LoRa ou SD swap |

### 1.5 Modularité & double usage

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Architecture** | Monolithique (RPi fait tout) | PCB unifié, deux configs filles |
| **Flexibilité** | Un seul use case (écurie) | Même boîtier = Camera Trap OU Acoustic Node OU les deux en alternance |
| **Production** | Achat de composants disparates par projet | PCB unique → volume → baisse des coûts |

---

## 2. Leurs avantages (Savonia → PKA)

### 2.1 Dataset équin & expertise métier (le gap #1)

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Dataset** | 7 chevaux × nuits d'enregistrement à Rauhalahti, annoté par experts | 0 données équines |
| **Experts métier** | Vétérinaires, soigneurs, propriétaires dans l'Innovation Group | Pas de partenaire équin actif (hors Mont-le-Soie potentiel) |
| **Connaissance du terrain** | Savonia travaille avec des écuries finlandaises depuis 2024 | On démarre de zéro |
| **Annotation** | Protocole rodé : vidéo pour valider les labels audio | Pas encore de protocole |

> **Impact** : on a le hardware mais pas la data. Sans dataset équin, notre CNN est un coquillage vide. Savonia a 1+ an d'avance sur la collecte et l'annotation de sons équins réels.

### 2.2 Infrastructure d'entraînement lourd

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Serveur entraînement** | NVIDIA DGX (cluster GPU entreprise) | Mac M5 / M1 (consumer) |
| **Capacité** | Entraînement PANNs/CNN14 sur AudioSet complet | Fine-tuning léger, pas d'entraînement from scratch |
| **Temps d'itération** | Heures pour un cycle complet | Jours sur hardware consumer |

> **Impact** : notre CNN 330K est un petit modèle pour l'edge. Leur PANNs/CNN14 + autoencoder est bien plus puissant pour la classification fine. Si on veut un modèle qui distingue « hennissement de douleur » de « hennissement de faim », il faut leur puissance de calcul.

### 2.3 Financement & institutionnel

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Financement** | EU CAP Network (CAP Strategic Plans), fonds publics finlandais | Autofinancé |
| **Budget** | Plusieurs centaines de k€ (projet 3 ans, 5+ employés) | < 10 k€ |
| **Statut** | Université publique + partenaires institutionnels | Indépendant, pas de structure légale |
| **Visibilité** | Publications EU CAP, Savonia Article Pro, conférences | Aucune visibilité publique |

> **Impact** : ils ont les moyens de financer un dataset, des salaires, un serveur DGX. Nous, on a l'agilité et la vitesse d'exécution, mais pas leur surface financière.

### 2.4 Application mobile utilisateur final

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **App mobile** | Deux apps en développement (soundscape + stéthoscope) | Aucune — on n'a qu'un dashboard HTML |
| **UX design** | Interface conçue pour propriétaires de chevaux | Pas de design utilisateur final |
| **Distribution** | App Store / Google Play prévu | Rien |

> **Impact** : on sait poser des boîtiers et classer des sons. Mais le propriétaire d'écurie ne veut pas lire un serial console ESP32. Il veut une notification qui dit « 🐴 Cheval box 3 : comportement anormal ». Savonia a cette couche.

### 2.5 Stéthoscope intestinal (deuxième produit)

| | Savonia | PKA / WildNexus |
|---|---------|-----------------|
| **Stéthoscope AI** | Pilote en cours — Thinklabs, Stemoscope évalués | Rien |
| **Marché** | Prévention coliques → réduction coûts vétérinaires | Pas adressé |

> **Impact** : leur deuxième produit (stéthoscope intestinal) ouvre un marché adjacent qu'on n'a même pas exploré. C'est un levier de financement supplémentaire.

---

## 3. Synthèse — Qui apporte quoi

```
┌─────────────────────────────────────────────────────────────┐
│               COMPLÉMENTARITÉ PARFAITE                        │
│                                                               │
│  SAVONIA apporte :               PKA apporte :                │
│  ┌──────────────────────┐       ┌──────────────────────┐      │
│  │ Dataset équin annoté  │       │ Hardware autonome    │      │
│  │ Modèle PANNs/DGX     │       │ Edge AI temps réel   │      │
│  │ App mobile end-user  │       │ Enclosure IP67       │      │
│  │ Partenaires véto     │       │ LoRa mesh sans WiFi  │      │
│  │ Infrastructure GPU   │       │ 60j batterie         │      │
│  │ Financement EU       │       │ Coût marginal <€100  │      │
│  │ Stéthoscope intestinal│      │ Déploiement sans élec │      │
│  └──────────────────────┘       └──────────────────────┘      │
│                                                               │
│  ENSEMBLE →                                                     │
│  Module autonome qui tourne à Rauhalahti 24/7,                 │
│  classifie en edge avec le modèle entraîné sur DGX,            │
│  alerte en temps réel via LoRa,                                │
│  remonte les données au DGX pour ré-entraînement.              │
└─────────────────────────────────────────────────────────────┘
```

---

## 4. L'angle de collaboration le plus crédible

**Ne pas leur dire « remplacez vos RPi par notre module ».** Ça les braquerait — ils ont déjà investi dans leur infrastructure.

**Dire plutôt :** « On peut étendre votre couverture à des zones où le RPi ne peut pas aller. »

| Use case | Solution actuelle Savonia | Valeur ajoutée PKA |
|----------|--------------------------|-------------------|
| Boxes avec prises | RPi 4 + caméra + micro — OK | Pas nécessaire, on n'apporte rien |
| Boxes sans prises (vieux bâtiments) | Impossible | Module WildNexus sur batterie |
| Paddocks extérieurs / prés | Impossible | Module IP67 outdoor |
| Grenier à foin / sellerie | Câbles trop loin | Module autonome |
| Surveillance incendie (combles) | Trop dangereux (230V + poussière) | Module basse tension safe |
| Écuries mobiles / temporaires | Pas adapté | Installation 30 secondes |
| Déploiement multi-sites (client final) | Trop cher et complexe | Plug-and-forget |

> 🎯 **Pitch final :** « Vous couvrez les boxes connectés avec vos RPi. Nous couvrons tout le reste avec nos modules autonomes. Même pipeline AI, même dashboard, deux hardwares complémentaires. »

---

## 5. Points de vigilance (ne pas survendre)

| Ce qu'on dit | La réalité à nuancer |
|-------------|---------------------|
| « CNN 330K INT8 onboard » | Estimé à 200-500ms — à valider sur hardware réel. Et 330K params c'est petit : suffisant pour 5-10 classes, pas pour 50. |
| « 60 jours sur 8×AA » | Validé pour le cycle caméra (1 photo/15min). Reste à valider pour le cycle audio (3s capture + 500ms CNN toutes les 15 min). |
| « LoRa mesh » | Portée théorique 2-15km. À l'intérieur d'un bâtiment agricole (murs épais, poutres métalliques), portée réelle probablement <100m. |
| « IP67 » | Le boîtier est IP67. Les micros MEMS exposés à l'ammoniac urinaire permanent : vieillissement accéléré à valider. |
| « Pas de câble » | Vrai pour l'alim. Mais sans WiFi, comment l'app mobile reçoit les alertes ? Il faut un gateway LoRa → IP. |

---

*Document interne — destiné à préparer l'argumentaire, pas à être partagé avec Savonia.*
