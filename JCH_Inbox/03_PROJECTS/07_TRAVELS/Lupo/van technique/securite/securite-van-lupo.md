# Sécurité Van Lupo — Westfalia Kelsey 2026
> Analyse critique & recommandations simplifiées — Dobby 🦉 — 2026-07-06
> **Principe :** rasoir d'Occam — chaque couche doit avoir un effet unique, pas de doublon.
> Version précédente archivée : `securite-van-lupo_backup_2026-07-05.md`

---

## Contexte

- **Véhicule :** « Lupo » — Westfalia Kelsey 2026 (Ford Transit Custom 2.0 EcoBlue, 170ch, 4×4, blanc)
- **Usage :** nature/campagne, bivouacs isolés, photos animalières
- **Déjà en place :** RPi 5 + Home Assistant + Zigbee (Sonoff ZBDongle-E) + Tailscale
- **En projet :** Caméras ESP32-CAM ×2 (surveillance extérieure)
- **Base Ford :** immobiliser PATS de série
- **Portes :** 2 portes cabine + 2 portes latérales coulissantes + 1 coffre arrière

---

## Ce qui a été éliminé (et pourquoi)

| Solution éliminée | Prix économisé | Raison |
|-------------------|---------------|--------|
| **Fencive** | 250€ | 100% redondant avec Zigbee+HA. Mêmes capteurs (portes, mouvement), même sirène, mêmes notifs. Fencive = pack clé-en-main pour non-techniciens. Test Automotive Insiders (03/2026) : « si tu bidouilles Zigbee, solution maison moins chère » |
| **Stoplock Pro** | 55€ | Effet dissuasif déjà couvert par IMC Créations (visible extérieur). Vol du véhicule protégé par OBD blocker + immobiliser PATS Ford. Canne volant = doublon |
| **Aqara Motion extérieur** | 15€ | Pas d'indice IP — non conçu pour l'extérieur. La lumière PIR 12V fait le même job en étant étanche |
| **Aqara Vibration ×1** | 15€ | 2 capteurs → 1 (porte cellule principale uniquement). Early warning utile, mais pas besoin sur les 4 portes |
| **Coffre-fort à câble** | 30€ | Rangement, pas sécurité périmétrique. Si besoin → boîte à gants fermant à clé (déjà présente sur Transit Custom) |

---

## Recommandation — 5 couches non redondantes

```
COUCHE 1 — Capteurs (Zigbee → HA)
   ├─ Aqara Door Sensor ×5 (50€)
   ├─ Aqara Vibration ×1 (15€)
   ├─ Aqara Motion P1 ×1 intérieur (15€)
   └─ Sirène Zigbee 90dB (20€)
          │
COUCHE 2 — Verrouillage mécanique
   └─ IMC Créations verrou cellule (120€)
          │
COUCHE 3 — Tracking
   └─ Invoxia GPS tracker (99€)
          │
COUCHE 4 — Durcissement
   ├─ Film sécurité 3M ×2 vitres (80€)
   └─ Bloqueur OBD bbfly-K01 (25€)
          │
COUCHE 5 — Dissuasion passive
   ├─ Lumière PIR 12V extérieure (15€)
   └─ Autocollant vidéosurveillance (5€)
```

### Détail par couche

#### Couche 1 — Capteurs Zigbee → Home Assistant (100€)
Déjà compatible avec ton setup. Tout remonte dans HA, qui est le cerveau.

| Capteur | Qté | Prix unité | Usage |
|---------|-----|-----------|-------|
| Aqara Door/Window Sensor | 5 | ~10€ | 2× portes cabine + 2× portes coulissantes + 1× coffre |
| Aqara Vibration Sensor | 1 | ~15€ | Porte coulissante côté route (la plus exposée en bivouac) — détecte tentative avant ouverture |
| Aqara Motion Sensor P1 | 1 | ~15€ | Intérieur cellule — détection présence intrusive |
| Sirène Zigbee Tuya 90dB | 1 | ~20€ | Dissuasion sonore immédiate |

**Automation HA recommandée :**
```yaml
# Note : avec 2 portes coulissantes, toutes les entités porte_* et vibration_* sont en trigger
alias: "Sécurité Van — Alarme Armée"
trigger:
  - platform: state
    entity_id: binary_sensor.porte_cabine_gauche
    to: "on"
  - platform: state
    entity_id: binary_sensor.vibration_serrure_cellule
    to: "on"
  - platform: state
    entity_id: binary_sensor.porte_coulissante_droite
    to: "on"
  # ... toutes les portes listées
  - platform: state
    entity_id: binary_sensor.motion_interieur
    to: "on"
condition:
  - condition: state
    entity_id: input_boolean.alarme_van
    state: "on"
action:
  - service: notify.mobile_app_iphone
    data:
      title: "🚨 ALERTE VAN"
      message: "Intrusion — {{ trigger.to_state.attributes.friendly_name }}"
  - service: switch.turn_on
    entity_id: switch.sirene_zigbee
  - service: light.turn_on
    entity_id: light.toutes_cellule
```

#### Couche 2 — Verrouillage mécanique (120-240€)

**IMC Créations verrou porte** — seul dispositif mécanique retenu.
- 🇫🇷 Français, brevet international
- Se monte à côté de la serrure FAP existante (aucune modification)
- Verrouillable de l'intérieur (nuit) ET de l'extérieur (absence)
- Barillet 7 broches, anti-perçage, anti-crochetage, 500 000 combinaisons
- Visible de l'extérieur → effet dissuasif immédiat pour qui passe devant cette porte

**Avec 2 portes coulissantes :**
- La porte côté route est la plus vulnérable (côté rue/parking) → **1 IMC prioritaire** (120€)
- La porte côté trottoir est moins exposée (souvent contre un talus/mur en bivouac)
- Si les deux côtés sont régulièrement exposés → **2 IMC recommandés** (240€)
- Budget ci-dessous calculé avec 1 IMC (option de base)
- [Fiche produit](https://www.camping-car-plus.com/securite-caravane/protection-antivol/serrures-imc-crations/verrou-imc-porte-cellule-8164.html)

#### Couche 3 — Tracking (99€)

**Invoxia GPS Tracker** — pas d'abonnement, pile 3 ans, discret.
- Réseau LoRa Sigfox (couverture Europe)
- Geofencing + alerte mouvement
- Se cache dans compartiment fusibles
- Alternative gratuite : Apple AirTag (35€) en complément — réseau Find My pour dernier emplacement connu

#### Couche 4 — Durcissement (105€)

| Solution | Prix | Effet |
|----------|------|-------|
| **Film sécurité 3M** ×2 vitres cellule | 80€ | Verre 5× plus résistant, ne cède pas sous impact |
| **bbfly-K01 bloqueur OBD** | 25€ | Empêche clonage de clé via port diagnostic |

#### Couche 5 — Dissuasion passive (20€)

| Solution | Prix | Effet |
|----------|------|-------|
| **Lumière PIR 12V extérieure** | 15€ | Éclairage automatique si mouvement → fait fuir + éclaire |
| **Autocollant « Vidéosurveillance »** | 5€ | Signal psychologique : « ce van est protégé, va au suivant » |

---

## Budget total

| Couche | Contenu | Prix |
|--------|---------|------|
| 1 — Capteurs | Door ×5 + Vibration ×1 + Motion ×1 + Sirène | 100€ |
| 2 — Mécanique | IMC Créations verrou cellule | 120€ |
| 3 — Tracking | Invoxia GPS tracker | 99€ |
| 4 — Durcissement | Film 3M + bloqueur OBD | 105€ |
| 5 — Dissuasion | Lumière PIR + autocollant | 20€ |
| **TOTAL** | | **444€** |
| *Option 2 IMC* | Second verrou coulissant | *+120€ → 564€* |

> Économie vs document original : **310€ (41%)** — 754€ → 444€

---

## Phasage

| Phase | Contenu | Prix | Déclencheur |
|-------|---------|------|-------------|
| 🔴 P0 | Capteurs Zigbee + sirène (couche 1) | 100€ | Immédiat — plug & play sur HA existant |
| 🟡 P1 | IMC Créations + bloqueur OBD + autocollant (couches 2, 4b, 5b) | 150€ | Avant prochain voyage |
| 🟢 P2 | Invoxia + film 3M (couches 3, 4a) | 179€ | Quand budget dispo |
| ⚪ Confort | Lumière PIR (couche 5a) | 15€ | Accessoire |

---

## Processus comportementaux (coût 0€)

Aucun gadget ne remplace ces habitudes — la communauté vanlife est unanime (The Van Conversion Guide, Vantour, Hello Aelita) :

- **Parking stratégique** — éviter zones isolées sans visibilité, privilégier Park4Night avec avis récents
- **Rien de visible** — zéro objet de valeur visible, stores baissés systématiquement
- **Clés jamais sur le contact** — même pour 2 minutes
- **Verrouillage intérieur la nuit** — IMC Créations le permet
- **Checklist départ** — portes, fenêtres, toit, alarme armée avant de s'éloigner

---

## Ce qui NE marche PAS (pertes de temps évitées)

| Solution | Raison |
|----------|--------|
| RVLock / ZKCE / Kedite | Format US Bauer/Global Link — incompatible FAP européen |
| SwitchBot Lock / Nuki | Conçu pour porte de maison, pas véhicule |
| Serrures empreintes camping-car | Toutes au format US |
| SimpliSafe | US uniquement, dépendant Wi-Fi |
| Fencive / Vanguard | Redondant avec Zigbee+HA (voir analyse) |

---

*Document créé par Dobby 🦉 — DeepSeek TUI — 2026-07-06*
*Version précédente archivée : `securite-van-lupo_backup_2026-07-05.md`*