# Lupo Van — Station Météo Intérieure : Boîtier Cheminée

**Designer** : Scarabée 🪲, Équipe PKA  
**Date** : 2025-07-11  
**Licence** : MIT  

---

## Design Intent

Le boîtier **Cheminée** est conçu pour héberger la station météo intérieure du van Lupo. Il répond à quatre contraintes clés :

1. **Exposition IAQ** — Les capteurs de qualité d'air (BME688) doivent être en contact avec l'air ambiant. Les ouvertures en partie basse assurent l'admission d'air frais.
2. **Séparation thermique** — L'ESP32-C3 dissipe ~0.5-1 W en fonctionnement. Sans séparation, il fausserait les mesures de température/humidité des capteurs. Une paroi pleine de 2 mm isole la chambre haute (chaude) de la chambre basse (froide).
3. **Ventilation passive** — Le flux d'air naturel bas→haut (effet cheminée) est amorcé par les fentes d'admission au plancher et d'évacuation au plafond. L'air frais entre par le bas, traverse la chambre des capteurs, puis est aspiré vers la chambre ESP32 où il évacue la chaleur.
4. **Fixation murale & accessibilité** — 2× M3 fraisés en face arrière, USB-C accessible sur le côté droit, LED visible en façade.

---

## Dimensions extérieures

| Paramètre       | Valeur (mm) |
|-----------------|-------------|
| Largeur (X)     | 43.0        |
| Profondeur (Y)  | 29.0        |
| Hauteur (Z)     | 28.5        |
| Épaisseur paroi | 2.0         |
| Séparateur      | 2.0         |

Le boîtier tient dans un cube de **43×29×28.5 mm** — compact, discret, adapté à l'habitacle d'un van.

---

## Composants logés

| Composant             | Dimensions PCB (mm) | Position               |
|-----------------------|---------------------|------------------------|
| ESP32-C3 Super Mini   | 22.5 × 18 × 5.5     | Chambre haute          |
| BME688 breakout       | 15 × 12 × 3         | Chambre basse (gauche) |
| SHT31 breakout        | 15 × 12 × 3         | Chambre basse (droite) |
| Jumpers I2C ×4        | —                   | Traversée séparateur   |

Tolérance uniforme : **+0.5 mm** sur chaque cote.

---

## Architecture mécanique

```
    ┌──────────────────┐  ← plafond (2 mm)
    │  ░░░░  ░░░░  ░░░░│  ← fentes évacuation air chaud
    │                  │
    │   ┌──────────┐   │
    │   │ ESP32-C3 │   │  ← chambre haute (13.0 mm)
    │   │  [USB-C]→│   │  ← découpe USB-C côté droit
    │   └──────────┘   │
    │──────────────────│  ← séparateur thermique (2 mm)
    │ BME688   SHT31   │  ← chambre basse (9.5 mm) — hauteur interne
    │                  │
    │  ░░░░  ░░░░  ░░░░│  ← fentes admission air frais
    └──────────────────┘  ← plancher (2 mm)

    Face avant : couvercle clipsable + 2 vis M2
    Face arrière : 2× M3 fraisés (fixation murale)
    Côté droit : découpe USB-C
    Façade : guide lumière LED ∅1.8 mm
```

---

## Instructions d'impression 3D

### Matériel

| Paramètre          | Valeur                  |
|--------------------|-------------------------|
| Imprimante         | Prusa Mini+             |
| Buse               | 0.4 mm standard         |
| Matériau           | **PETG**                |
| Plateau            | 180 × 180 mm            |
| Hauteur de couche  | 0.20 mm (QUALITY)       |
| Périmètres         | 2–3                     |
| Remplissage        | 15–20 % gyroïde         |
| Support            | **Aucun** (design auto-porteur) |
| Adhérence plateau  | Brim recommandé (PETG)  |
| Température buse   | 240 °C (PETG)           |
| Température plateau| 85 °C (PETG)            |

### Orientation d'impression

- **Face arrière sur le plateau** (trous M3 visibles vers le haut)
- La face avant (couvercle) sera vers le haut — les ponts des fentes de ventilation sont courts (< 12 mm) et s'impriment sans support.
- Imprimer le couvercle **à plat**, face extérieure contre le plateau pour un état de surface propre.

### Post-traitement

- Aucun support à retirer.
- Les trous M2 du couvercle sont prévus pour des vis auto-taraudeuses (⌀2 mm). Si nécessaire, passer un taraud M2 ou utiliser des vis à bois courtes (4–6 mm).
- Les trous M3 arrière acceptent des vis M3 standard ; la fraisure est dimensionnée pour tête fraisée ISO 7046.

---

## Génération du STL

OpenSCAD n'étant pas installé dans l'environnement actuel, exécuter :

```bash
cd /Users/jchavauxm5/PKA_JCH/JCH_Inbox/03_PROJECTS/11_IOT/iot-van/enclosure/

# Corps principal + berceaux (sans couvercle)
openscad -o lupo-meteo-enclosure-body.stl lupo-meteo-enclosure.scad

# Couvercle seul (décommenter lid() à la fin du .scad, commenter le reste)
openscad -o lupo-meteo-enclosure-lid.stl \
  -D 'RENDER_LID=true' lupo-meteo-enclosure.scad
```

Astuce : ajouter `$fn=64` en ligne de commande pour des perçages plus propres :

```bash
openscad -o lupo-meteo-enclosure-body.stl --enable=manifold -D '$fn=64' lupo-meteo-enclosure.scad
```

---

## Points d'attention

- **Séparateur thermique** : le petit canal de passage des 4 fils I2C (SDA, SCL, 3.3V, GND) mesure 4×6 mm. Le remplir de mastic silicone après câblage pour restaurer l'isolation thermique.
- **LED** : le trou ∅1.8 mm est aligné avec la LED GPIO8 de l'ESP32-C3 Super Mini. Vérifier la position exacte sur votre PCB (elle peut varier selon le batch) — ajuster `LED_HOLE_D` et la translation X dans le code si nécessaire.
- **USB-C** : la découpe de 8.5×3.2 mm est dimensionnée pour le connecteur seul. Si votre câble a un overmold large, élargir `ESP32_USBC_W` à 10 mm.
- **PETG** : choisi pour sa température de transition vitreuse (~80 °C) supérieure au PLA (~60 °C) — important dans un van exposé au soleil. Le PETG est aussi moins conducteur thermiquement que le PLA chargé métal, ce qui aide la séparation thermique.

---

## Licence

MIT — © 2025 PKA / Scarabée 🪲
