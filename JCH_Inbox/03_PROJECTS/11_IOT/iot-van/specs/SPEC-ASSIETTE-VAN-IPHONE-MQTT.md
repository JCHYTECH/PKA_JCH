# SPEC — Assiette Van via iPhone (Sensor Logger + MQTT Discovery)

> Date : 2026-07-18, corrigé 2026-07-19 | Dobby 🦉
> Décision : Sensor Logger (iOS) + MQTT Discovery → Home Assistant. 0 matériel supplémentaire.
> Les 3× MPU6050 GY-521 commandés restent en spare.
> ⚠️ v1 (18/07) utilisait `mqtt: broker:` en YAML — obsolète sur HA récent. Voir
> [[ARCHITECTURE-MQTT-DISCOVERY]] pour la solution générique multi-instances retenue.

---

## Architecture

```
iPhone (Sensor Logger)          RPi 5 Lupo (HA OS)
┌────────────────────┐         ┌─────────────────────────┐
│ Accéléromètre      │         │ Mosquitto Broker        │
│ → pitch (X)        │─MQTT──▶│   (add-on HA)           │
│ → roll (Y)         │  WiFi   │          │              │
│                     │         │  pka_mqtt_discovery_    │
│ Sensor Logger       │         │  bridge.py (pont)       │
│ → Stream MQTT      │         │          │              │
│ → topic:            │         │   Entités auto-créées  │
│   lupo/assiette     │         │   (MQTT Discovery)      │
└────────────────────┘         │   → van_pitch           │
                               │   → van_roll             │
                               │   Dashboard Lovelace     │
                               └─────────────────────────┘
```

---

## Étape 1 — Mosquitto Broker (HA OS)

Sur HA Lupo → Settings → Add-ons → Mosquitto broker → Install

Configuration minimale (add-on, pas configuration.yaml) :
```yaml
logins:
  - username: jchavaux
    password: dobby2026!
require_certificate: false
```

**Connexion HA au broker** : via l'intégration UI — Paramètres → Appareils et services →
Ajouter une intégration → MQTT. Pas de bloc `mqtt: broker:` en YAML (obsolète, cause l'erreur
rencontrée le 18/07).

---

## Étape 2 — Sensor Logger (iPhone)

1. Installer [Sensor Logger](https://apps.apple.com/app/sensor-logger/id1531582925) (gratuit)
2. Onglet **Stream** → **MQTT**
3. Configuration :
   - **Broker URL** : `mqtt://<IP_RPi_Lupo>:1883`
   - **Username** : `jchavaux`
   - **Password** : `dobby2026!`
   - **Topic** : `lupo/assiette`
   - **Mode** : JSON
   - **Batch period** : 1000 ms
   - **Skip writing** : activé
4. Onglet **Sensors** → activer **Accelerometer** et **Gyroscope**
5. Appuyer sur ▶️ Record → les données commencent à streamer

---

## Étape 3 — Pont MQTT Discovery (remplace la config YAML capteurs)

Sensor Logger publie du JSON brut sur `lupo/assiette` — il ne parle pas MQTT Discovery
nativement. Au lieu de créer les capteurs à la main (UI ou YAML, non générique), on utilise le
pont générique :

```bash
python3 scripts/pka_mqtt_discovery_bridge.py \
  --config JCH_Inbox/03_PROJECTS/11_IOT/iot-van/specs/mapping-lupo-assiette.json
```

Le fichier `mapping-lupo-assiette.json` définit le broker, le device (`lupo`), le topic source
et les capteurs à extraire (pitch, roll). Le script publie les topics Discovery une fois puis
relaie les valeurs en continu. Voir [[ARCHITECTURE-MQTT-DISCOVERY]] pour le détail du protocole
et son application aux autres instances (Esneux, futurs sites).

> Note : Sensor Logger envoie potentiellement les données brutes d'accéléromètre (m/s²) plutôt
> que pitch/roll calculés. À vérifier au premier test réel — si besoin, ajouter le calcul dans
> le pont (extension simple : ajouter une fonction de transformation par capteur dans le
> mapping).

---

## Étape 4 — Template binaire « Niveau OK »

```yaml
template:
  - binary_sensor:
      - name: "Van Level OK"
        state: >
          {{ states('sensor.van_pitch') | float(-99) | abs < 3
             and states('sensor.van_roll') | float(-99) | abs < 3 }}
        icon: mdi:level
```

---

## Étape 5 — Carte Lovelace

```yaml
type: custom:mushroom-template-card
primary: Assiette Van
secondary: |
  Tangage : {{ states('sensor.van_pitch') }}°
  Roulis : {{ states('sensor.van_roll') }}°
icon: mdi:level
icon_color: >
  {% if is_state('binary_sensor.van_level_ok', 'on') %}
    green
  {% elif is_state('binary_sensor.van_level_ok', 'off') %}
    red
  {% else %}
    grey
  {% endif %}
badge_icon: mdi:check-circle
badge_color: green
```

---

## Usage terrain

1. Arrivé au bivouac → poser l'iPhone à plat au plancher
2. Ouvrir Sensor Logger → Stream → ▶️
3. Lancer (ou laisser tourner en fond) `pka_mqtt_discovery_bridge.py`
4. Dashboard HA affiche pitch/roll en temps réel
5. Caler le van → vert = OK
6. Arrêter le stream

---

## Fallback manuel

Si pas de réseau/signal : l'app **Mesure** (Compass) intégrée à iOS affiche un niveau à bulle.
Pas de HA, mais fonctionne hors-ligne.

---

## Notes

- L'iPhone doit être sur le même réseau WiFi que le RPi Lupo
- Consommation : Sensor Logger en arrière-plan ≈ 5-8% batterie/heure
- Les 3× MPU6050 GY-521 commandés restent en spare — pourront servir si l'approche iPhone
  s'avère contraignante en usage réel

---

## Voir aussi

- [[ARCHITECTURE-MQTT-DISCOVERY]] — solution générique multi-instances (Lupo, Esneux, futurs)
- [[hub-esneux]] — instance HA Esneux (M5)

---

*Corrigé par Dobby 🦉 — 2026-07-19 — Claude Sonnet 5*
*v1 (18/07) : deepseek-v4 — approche YAML ad hoc, remplacée par le pont générique*
