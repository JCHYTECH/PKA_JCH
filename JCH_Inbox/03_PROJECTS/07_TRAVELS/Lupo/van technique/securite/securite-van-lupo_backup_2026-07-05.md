# Sécurité Van Lupo — Westfalia Kelsey 2026
> Analyse et recommandations — Dobby 🦉 — 2026-07-05
> Source : PDF « 20 idées géniales pour sécuriser votre van » (Vanlife Store) + recherches web

---

## Contexte JC

- **Véhicule :** « Lupo » — Westfalia Kelsey 2026 (Ford Transit Custom 2.0 EcoBlue, 170ch, 4×4, blanc)
- **Usage :** nature/campagne majoritairement, bivouacs isolés, photos animalières
- **Déjà en place :** RPi 5 + Home Assistant + Zigbee (Sonoff ZBDongle-E) + Tailscale
- **En cours :** Projet Lupo — caméras ESP32-CAM de surveillance extérieure

---

## Architecture de sécurité recommandée

```
                    ┌──────────────────────────────┐
                    │      HOME ASSISTANT (RPi 5)   │
                    │   Automations + Notifications │
                    └──────────┬───────────────────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ▼                      ▼                      ▼
┌───────────────┐    ┌───────────────┐    ┌───────────────┐
│ CAPTEURS       │    │ VERROUILLAGE   │    │ ALARME         │
│ Zigbee         │    │ Mécanique      │    │ Connectée       │
├───────────────┤    ├───────────────┤    ├───────────────┤
│ Portes (4×)    │    │ IMC Créations  │    │ Fencive        │
│ Vibrations (2×) │    │ HEO Safe       │    │ Sirène Zigbee  │
│ Mouvement (2×) │    │ Thule Van Lock │    │ Notif iPhone   │
└───────────────┘    └───────────────┘    └───────────────┘
        │                      │                      │
        └──────────────────────┼──────────────────────┘
                               │
                               ▼
                    ┌──────────────────┐
                    │  CAMÉRAS LUPO    │
                    │  ESP32-CAM ×2    │
                    │  (en projet)     │
                    └──────────────────┘
```

---

## 1. Capteurs Zigbee + HA 🥇 — Priorité absolue

**Déjà compatible avec ton setup.** Le RPi 5 + Sonoff ZBDongle-E dans le van = tout est prêt.

| Capteur | Qté | Prix unité | Total | Usage |
|---------|-----|-----------|-------|-------|
| Aqara Door/Window Sensor | 4 | ~10€ | 40€ | 2× portes cabine + 1× porte cellule + 1× coffre |
| Aqara Vibration Sensor | 2 | ~15€ | 30€ | Collé sur chaque serrure — détecte tentative effraction |
| Aqara Motion Sensor P1 | 2 | ~15€ | 30€ | Intérieur cellule + extérieur (sous auvent) |
| Sirène Zigbee (Tuya) | 1 | ~20€ | 20€ | Dissuasion sonore 90dB |
| **TOTAL** | | | **~120€** | |

### Automations HA recommandées

```yaml
# Alarme — mode absence
alias: "Sécurité Van — Alarme Armée"
trigger:
  - platform: state
    entity_id: binary_sensor.porte_cabine_gauche
    to: "on"
  - platform: state
    entity_id: binary_sensor.vibration_serrure_cellule
    to: "on"
condition:
  - condition: state
    entity_id: input_boolean.alarme_van
    state: "on"
action:
  - service: notify.mobile_app_iphone
    data:
      title: "🚨 ALERTE VAN"
      message: "Intrusion détectée — {{ trigger.to_state.attributes.friendly_name }}"
  - service: switch.turn_on
    entity_id: switch.sirene_zigbee
  - service: light.turn_on
    entity_id: light.toutes_cellule
```

---

## 2. Verrouillage mécanique additionnel 🥈

**Aucune serrure connectée n'existe pour le format FAP européen.** RVLock, ZKCE, Kedite = format US uniquement.

| Solution | Prix | Notes |
|----------|------|-------|
| **IMC Créations** — verrou cellule | ~120€ | 🇫🇷 Français, brevet international, commandable intérieur ET extérieur, 500 000 combinaisons |
| **HEO Safe** | ~100€ | Même principe, montage sur paroi |
| **Thule Van Lock** | ~80€ | Barillet pour porte coulissante + arrière, glisse entre porte et cadre |
| **Stoplock Pro** (canne volant) | ~55€ | Dissuasif visible, jaune fluo |

### Recommandation : IMC Créations

- Se monte **à côté** de la serrure FAP existante (aucune modification)
- Verrouillable de l'intérieur (quand tu dors) ET de l'extérieur (quand tu t'éloignes)
- Barillet 7 broches, anti-perçage, anti-crochetage
- Visible de l'extérieur → effet dissuasif immédiat
- [Fiche produit](https://www.camping-car-plus.com/securite-caravane/protection-antivol/serrures-imc-crations/verrou-imc-porte-cellule-8164.html)

---

## 3. Alarme connectée autonome 🥉

| Solution | Prix | Fonctionnalités |
|----------|------|----------------|
| **Fencive** 🇫🇷 | ~250€ | Capteurs portes + mouvement, app smartphone, alerte intrusion, GPS optionnel |
| SQUIDDY Confort | ~180€ | Pack alarme modulaire, détecteurs ouverture + sirène |

→ **Fencive recommandé** : startup française, conçu spécifiquement pour vans et camping-cars. L'app smartphone fait le taf si HA est offline.

---

## 4. GPS Tracker caché

| Modèle | Prix | Abonnement | Points forts |
|--------|------|-----------|-------------|
| **Tracki** | ~25€ | ~10€/mois | Aimanté, 4G, geofencing, alerte mouvement, app |
| **Invoxia** | ~99€ | 0€ | Réseau LoRa Sigfox, pile 3 ans, discret, pas d'abonnement |
| Apple AirTag | ~35€ | 0€ | Si iPhone, réseau Find My, pas de GPS mais maillage |

→ **Invoxia recommandé** : pas d'abonnement, pile 3 ans, discret. Se cache dans le compartiment fusibles.

---

## 5. Sécurité périmétrique & dissuasion

| Solution | Prix | Usage |
|----------|------|-------|
| **Film sécurité 3M** vitres | ~40€/vitre | Rend le verre 5× plus résistant, ne cède pas |
| **bbfly-K01** bloqueur OBD | ~25€ | Empêche le clonage de clé via port OBD |
| Lumière PIR extérieure 12V | ~15€ | Éclairage automatique si mouvement autour du van |
| Coffre-fort à câble | ~30€ | Pour passeport, argent, clés de secours |
| Autocollant « Vidéosurveillance » | ~5€ | Dissuasion psychologique |

---

## 6. Ce qui NE marche PAS (pertes de temps évitées)

| Solution | Raison |
|----------|--------|
| RVLock / ZKCE / Kedite serrures connectées | Format US Bauer/Global Link — incompatible FAP européen |
| SwitchBot Lock | Conçu pour cylindre européen maison — pas pour porte de véhicule |
| Nuki Smart Lock | Idem, porte de maison uniquement |
| Serrures à empreinte camping-car | Toutes au format US, aucune en FAP |

---

## Budget total — Pack sécurité van

| Catégorie | Solution | Prix |
|-----------|----------|------|
| Capteurs | Zigbee (portes + vibration + mouvement + sirène) | 120€ |
| Verrouillage | IMC Créations verrou cellule | 120€ |
| Alarme | Fencive | 250€ |
| GPS | Invoxia | 99€ |
| Vitres | Film sécurité 3M (2 vitres) | 80€ |
| OBD | bbfly-K01 bloqueur | 25€ |
| Dissuasion | Canne Stoplock Pro + autocollant | 60€ |
| **TOTAL** | | **~754€** |

### Par priorité

| Phase | Contenu | Prix | Délai |
|-------|---------|------|-------|
| 🔴 P0 | Capteurs Zigbee + sirène | 120€ | Maintenant (plug & play) |
| 🟡 P1 | IMC Créations + Stoplock | 175€ | Avant prochain voyage |
| 🟢 P2 | Fencive + Invoxia + film 3M | 429€ | Quand budget dispo |
| ⚪ P3 | Bloqueur OBD + coffre | 55€ | Accessoire |

---

## Notes

- **Pourquoi pas de serrure connectée :** le marché européen du camping-car utilise exclusivement le format FAP (italien). Aucun fabricant ne propose de serrure Bluetooth/empreinte pour ce format. Les serrures connectées type RVLock sont au format US Bauer/Global Link, incompatible.
- **HA reste le hub central :** tous les capteurs Zigbee remontent dans HA, qui est ton cerveau de sécurité. Même sans la serrure elle-même connectée, tu sais en temps réel ce qui se passe.
- **L'effet dissuasif > la technologie :** un verrou IMC visible + une canne Stoplock + un autocollant vidéosurveillance font passer un voleur au van d'à côté.

---

*Document créé par Dobby 🦉 — DeepSeek TUI — 2026-07-05*
*À mettre à jour après achat/installation des premiers composants.*
