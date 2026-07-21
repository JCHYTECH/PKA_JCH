# ARCHITECTURE — MQTT Discovery générique multi-instances HA

> Créé : 2026-07-19 | Dobby 🦉 + Forge 🔨
> Portée : toute instance Home Assistant du réseau PKA (Lupo/RPi, Esneux/M5, et futures instances)
> Origine : blocage capteurs MQTT Lupo — `00_INBOX/2026-07-18_dobby_resume-session-soir.md`

---

## Problème résolu

HA (≥2024.x) ne supporte plus la configuration `mqtt:` + `broker:` en YAML. La connexion au
broker se fait exclusivement via l'intégration UI (Paramètres → Appareils et services → MQTT).
Créer des capteurs un par un via l'UI **fonctionne mais n'est pas générique** — chaque nouvelle
instance HA (Lupo, Esneux, futur van #2, futur nœud IoT) impose de refaire la manip à la main
pour chaque capteur.

## Principe — MQTT Discovery

MQTT Discovery est un protocole natif de HA, actif par défaut dès que l'intégration MQTT UI est
configurée. Il ne dépend d'aucun YAML custom et fonctionne **identiquement sur toutes les
instances** :

1. Un message MQTT **retenu** (`retain=true`) est publié sur un topic normalisé :
   `homeassistant/<component>/<node_id>/<object_id>/config`
2. Le payload JSON décrit le capteur (nom, unité, topic d'état, template, device).
3. HA (qui écoute `homeassistant/#` par défaut) crée l'entité automatiquement — sans YAML,
   sans redémarrage, sans intervention UI manuelle.
4. L'état circule ensuite sur le `state_topic` déclaré dans le payload.

**Aucune différence de configuration entre Lupo et Esneux** — seul le champ `device.identifiers`
change (`"lupo"` vs `"esneux"`), ce qui permet en plus de regrouper proprement les entités par
site dans HA.

### Exemple — capteur générique

```json
Topic (retain=true):
homeassistant/sensor/lupo_van_pitch/config

Payload:
{
  "name": "Van Pitch",
  "state_topic": "lupo/assiette/pitch",
  "unit_of_measurement": "°",
  "unique_id": "lupo_van_pitch",
  "device": {
    "identifiers": ["lupo"],
    "name": "Lupo",
    "manufacturer": "PKA_JCH"
  }
}
```

Puis publier l'état en texte brut sur `lupo/assiette/pitch` (ex : `2.4`).

## Cas d'usage identifié : Sensor Logger (iPhone)

Sensor Logger publie du JSON brut agrégé (`{"pitch":..,"roll":..}`) sur un topic unique — il ne
parle pas Discovery nativement (contrairement à ESPHome, qui le fait de base). C'est le seul cas
qui justifie un composant logiciel : **un pont générique** qui écoute un topic source brut et
republie en Discovery.

## Outil — `scripts/pka_mqtt_discovery_bridge.py`

Pont générique réutilisable par toute instance et tout capteur non-Discovery-natif.

- Lit un fichier de mapping JSON (`--config <fichier>`), propre à chaque instance/capteur.
- Se connecte au broker MQTT local à l'instance (paramétrable, pas hardcodé).
- Publie une fois les topics `config` Discovery pour chaque capteur défini.
- Écoute le topic source, extrait chaque clé JSON définie, republie sur le `state_topic`
  correspondant.
- Aucune logique spécifique à Lupo, Esneux, ou Sensor Logger dans le code — tout est dans le
  fichier de mapping.

### Exemple de mapping (`mapping-lupo-assiette.json`)

```json
{
  "broker": {"host": "192.168.129.16", "port": 1883, "username": "jchavaux", "password": "dobby2026!"},
  "device": {"identifiers": ["lupo"], "name": "Lupo"},
  "source_topic": "lupo/assiette",
  "sensors": [
    {"key": "pitch", "name": "Van Pitch", "unit": "°", "state_topic": "lupo/assiette/pitch"},
    {"key": "roll",  "name": "Van Roll",  "unit": "°", "state_topic": "lupo/assiette/roll"}
  ]
}
```

Pour ajouter une nouvelle instance ou un nouveau capteur non-Discovery : créer un nouveau fichier
de mapping, aucune modification du script.

## Règle transversale

Toute nouvelle instance HA (van #2, serre, futur site) qui reçoit un capteur ne parlant pas
Discovery nativement (apps mobiles type Sensor Logger, scripts maison, capteurs legacy) doit
passer par ce pont plutôt que par une configuration YAML `mqtt: sensor:` ad hoc par instance.

## Voir aussi

- [[SPEC-ASSIETTE-VAN-IPHONE-MQTT]] — cas d'usage van Lupo (assiette)
- [[hub-esneux]] — instance HA Esneux (M5)
- [[SPEC-CAPTEUR-ENV]] — capteurs ESPHome (Discovery natif, pas besoin du pont)
