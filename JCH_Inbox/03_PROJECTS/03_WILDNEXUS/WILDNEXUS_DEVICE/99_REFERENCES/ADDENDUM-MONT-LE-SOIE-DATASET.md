# Addendum CCTP — Phase Dataset Mont-le-Soie

> Dobby 🦉 — 2026-07-20
> Complément au `CCTP-WILDNEXUS-ECURIE-V1.0.md`
> Objet : Hardware enregistreur continu 3 semaines + Outil d'annotation pour experts équestres

---

## 1. Stratégie dataset

Deux phases distinctes, deux hardwares différents :

| Phase | Objectif | Hardware | Durée |
|-------|----------|----------|-------|
| **Collecte** | Enregistrer 3 semaines de sons d'écurie continus | Enregistreur secteur, pas d'edge AI | 3 semaines |
| **Déploiement** | Module autonome edge AI temps réel | WildNexus Acoustic Node (batterie) | Permanent |

**Pourquoi ne pas utiliser le module WildNexus pour la collecte ?** Parce que le module actuel fait des cycles de 3s/15min en deep sleep. Pour constituer un dataset riche, on a besoin de **continu 24/7** sur 3 semaines — ce qui nécessite une alimentation secteur et un stockage massif. L'écurie a des prises électriques.

---

## 2. Hardware enregistreur — Solution retenue

### 2.1 Vieux PC + micro USB (coût : ~€10–30)

JC a des vieux PC disponibles. Un PC sous Linux (ou Windows avec WSL) fait parfaitement l'affaire. Pas besoin de RPi.

| Composant | Spécification | Coût |
|-----------|--------------|------|
| **Compute** | Vieux PC (Linux ou Windows+WSL) — déjà possédé | €0 |
| **Audio** | Micro USB (webcam, casque, ou micro de conférence) — déjà possédé ou €10–30 | ~€15 |
| **Stockage** | Disque dur interne du PC (min. 250 GB libre) | €0 |
| **Alim** | Secteur (prise écurie) | €0 |
| **Script** | `ffmpeg` — enregistrement continu, segmentation en fichiers de 10 min | 0 dev |
| **Boîtier** | Le boîtier du PC lui-même, placé en hauteur hors de portée | €0 |
| **Total** | | **~€15** |

> **Note sur les micros :** Les micros I2S (SPH0645LM4H-B) ne se connectent pas à un PC standard (pas de bus I2S). Pour la phase dataset, un micro USB standard est suffisant : les sons d'écurie (hennissements, chocs, voix) sont dans le spectre audible classique, la différence avec les MEMS I2S sera marginale pour l'annotation. Le futur module WildNexus utilisera bien les MEMS I2S — la phase dataset sert à collecter des labels, pas à calibrer le hardware final.

### 2.2 Script d'enregistrement continu (Linux/Mac/WSL)

```bash
#!/bin/bash
# enregistreur-continu.sh — Mont-le-Soie dataset
# Usage : ./enregistreur-continu.sh /chemin/vers/stockage/
# Prérequis : ffmpeg installé (apt install ffmpeg / brew install ffmpeg)

OUTDIR="${1:-./ecurie-dataset}"
DURATION=600  # 10 minutes par fichier
RATE=16000
CHANNELS=1  # mono suffisant pour l'annotation

mkdir -p "$OUTDIR"

echo "=== Enregistreur continu Écurie ==="
echo "Stockage : $OUTDIR"
echo "Fichiers de ${DURATION}s, ${RATE}Hz, mono"
echo "Ctrl+C pour arrêter"
echo ""

while true; do
    TS=$(date +%Y%m%d_%H%M%S)
    FNAME="${OUTDIR}/ecurie_${TS}.wav"
    echo "[$(date)] ▶️  $FNAME"
    ffmpeg -y -f avfoundation -i ":0" -ar $RATE -ac $CHANNELS -t $DURATION "$FNAME" 2>/dev/null
    # Rotation : supprimer les fichiers de + de 25 jours si espace disque < 10%
    DISK_USAGE=$(df "$OUTDIR" | tail -1 | awk '{print $5}' | sed 's/%//')
    if [ "$DISK_USAGE" -gt 90 ]; then
        find "$OUTDIR" -name "*.wav" -mtime +25 -delete
        echo "[$(date)] 🧹 Nettoyage disque"
    fi
done
```

> **Note Windows :** Sous Windows, remplacer `avfoundation` par `dshow` et `:0` par le nom du périphérique audio (trouvable via `ffmpeg -list_devices true -f dshow -i dummy`).

### 2.3 Estimation stockage

| Paramètre | Valeur |
|-----------|-------|
| Débit (16kHz, 16-bit, mono) | 256 kbps = 32 KB/s |
| Par jour (24h) | ~2.7 GB |
| Pour 3 semaines (21 jours) | **~57 GB** |
| Marge de sécurité 2× | ~120 GB |

Un vieux PC avec 250 GB de disque libre suffit largement.

### 2.4 Placement dans l'écurie

- PC en hauteur (étagère, poutre) hors de portée des chevaux
- Micro USB positionné au centre du plafond ou au-dessus des boxes centraux
- Câble USB prolongateur si nécessaire (5m max)
- Protection anti-poussière basique (sac plastique ajouré autour du PC, pas autour du micro)
- 2–3 PC pour couvrir différentes zones (boxes, couloir, sellerie)

---

## 3. Outil d'annotation pour experts équestres

### 3.1 Principe

On adapte l'outil `insectnet-qc-review.html` (InsectNet) pour l'écurie. L'outil existant permet de :
- Afficher une grille de cartes (spectrogramme + lecteur audio)
- Filtrer par catégorie, statut QC
- Marquer chaque segment : ✅ Keep / ❌ Reject / 🔍 Review
- Ajouter un commentaire texte
- Exporter en CSV

**Ce qu'on adapte pour l'écurie :**

| InsectNet (original) | Écurie (adaptation) |
|---------------------|---------------------|
| Species (nom latin) | Catégorie son (hennissement, choc, voix, feu…) |
| `visual_qc` : keep/review/reject | Même logique, vocabulaire FR |
| Filtres par espèce | Filtres par catégorie ET par reviewer |
| Auto-suggestions QC | Désactivé en v0.1 (pas de modèle pré-entraîné) |
| Export CSV pour entraînement | Export CSV avec colonnes : `fichier, catégorie, reviewer, label, commentaire` |

### 3.2 Workflow annotation

```
1. Chouette/Dobby prégénère les segments (3s) + spectrogrammes
   depuis les enregistrements continus (script Python existant InsectNet)
                ↓
2. Les fichiers sont packagés dans un dossier web statique :
   segments/  spectrograms/  manifest.csv
                ↓
3. L'outil HTML est envoyé aux 4 reviewers (palefrenier, lad, véto, cavaliers)
   → Ils ouvrent la page dans leur navigateur (local ou hébergé)
                ↓
4. Chaque reviewer écoute + regarde le spectrogramme
   → Clique : ✅ Son identifié (précise la catégorie)
              ❌ Bruit / silence / inexploitable
              🔍 Incertain → sera revu par un 2e reviewer
                ↓
5. Export CSV → Dobby consolide les annotations des 4 reviewers
   → Règle de consensus : 3/4 d'accord = label validé
   → Conflit → Dobby ou JC tranche
```

### 3.3 Catégories de sons (simplifiées pour l'annotation)

| Code | Catégorie | Icône | Description pour non-experts |
|------|-----------|-------|------------------------------|
| `HEN` | Hennissement | 🐴 | Cri du cheval, fort, long |
| `MAR` | Marche/sabot | 🦶 | Bruit de pas, fer sur sol dur |
| `MAN` | Mange/boit | 🌾 | Mastication, eau, foin |
| `CHO` | Choc violent | 💥 | Coup contre mur/porte, chute |
| `GRA` | Gratte/tape | 🚪 | Gratte sol, tape mur ou porte |
| `VOI` | Voix humaine | 🗣️ | Parle, appelle, crie |
| `POR` | Porte/loquet | 🔑 | Bruit métallique porte, verrou |
| `OIS` | Oiseau | 🐦 | Pépiements, battements d'ailes |
| `RON` | Rongeur | 🐀 | Grattements, couinements |
| `VEN` | Ventilation/machine | 🌀 | Bruit continu mécanique |
| `FEU` | Crépitement/feu | 🔥 | Crépitement anormal, alarme |
| `AMB` | Ambiant extérieur | 🌧️ | Pluie, vent, orage, tracteur |
| `AUT` | Autre / inconnu | ❓ | Son non identifiable |
| `SIL` | Silence | 🔇 | Aucun son significatif |

### 3.4 Interface utilisateur (adaptée)

```
┌─────────────────────────────────────────────────────────┐
│  🐴 ANNOTATION SONS ÉCURIE — Mont-le-Soie               │
│                                                          │
│  Reviewer : [Palefrenier ▼]  Catégorie : [Toutes ▼]     │
│  Statut   : [Tous ▼]         ⬇ Export CSV               │
│                                                          │
│  ┌──────────────────────┐ ┌──────────────────────┐      │
│  │     Spectrogramme    │ │     Spectrogramme    │      │
│  │     (image PNG)      │ │     (image PNG)      │      │
│  ├──────────────────────┤ ├──────────────────────┤      │
│  │ ▶️ Lecture audio     │ │ ▶️ Lecture audio     │      │
│  ├──────────────────────┤ ├──────────────────────┤      │
│  │ Fichier: 2026...wav  │ │ Fichier: 2026...wav  │      │
│  │ Durée: 3.0s          │ │ Durée: 3.0s          │      │
│  │                                                       │
│  │ Catégorie: [HEN ▼]    │ │ Catégorie: [SIL ▼]    │      │
│  │ [✅ Valider] [❌ Rejeter] [🔍 Incertain]              │      │
│  │ Commentaire: _________ │ │ Commentaire: _________ │      │
│  └──────────────────────┘ └──────────────────────┘      │
│                                                          │
│  12/450 segments annotés — 2.7%                          │
└─────────────────────────────────────────────────────────┘
```

### 3.5 Déploiement

| Méthode | Avantage | Inconvénient |
|---------|----------|-------------|
| **Fichier HTML local** (double-clic) | Zéro infra, 100% offline | Fichiers audio doivent être en relatif |
| **Hébergé sur aroundus.tech/sons-ecurie/** | Accessible partout, multi-reviewer simultané | Upload des fichiers massif |
| **Serveur local sur le Mac de JC** | Rapide, contrôle total | Reviewers doivent être sur le même réseau |

> **Recommandé :** fichier HTML local pour la v0.1. JC prépare une clé USB avec le dossier complet (HTML + spectrogrammes + audio), la donne aux reviewers. Ils travaillent hors ligne. Ils rendent le CSV. Simple, robuste.

---

## 4. Prochaines actions immédiates

| Priorité | Action | Responsable |
|----------|--------|-------------|
| 🔴 P0 | Récupérer/acheter RPi + disque dur pour enregistreur | JC |
| 🔴 P0 | Configurer micros I2S sur RPi + script enregistrement continu | Forge |
| 🔴 P0 | Produire la version adaptée de `insectnet-qc-review.html` pour l'écurie | Dobby + Chouette |
| 🔴 P0 | Planifier installation enregistreurs au Mont-le-Soie | JC |
| 🟡 P1 | Script de prégénération segments 3s + spectrogrammes depuis les WAV continus | Clio |
| 🟡 P1 | Former les reviewers au protocole d'annotation | JC |

---

*Addendum au CCTP — sera fusionné dans la V1.1.*
