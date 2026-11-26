#!/usr/bin/env python3
"""
pka_mqtt_discovery_bridge.py
Model: Claude Sonnet 5 (OpenRouter) — 2026-07-19 — Forge — pont MQTT Discovery générique

Pont générique multi-instances : écoute un topic MQTT source (JSON brut, ex: Sensor Logger)
et republie en MQTT Discovery pour Home Assistant. Aucune logique spécifique à une instance
ou un capteur dans ce script — tout vient du fichier de mapping JSON passé en --config.

Usage:
    python3 scripts/pka_mqtt_discovery_bridge.py --config mapping-lupo-assiette.json
    python3 scripts/pka_mqtt_discovery_bridge.py --config mapping-lupo-assiette.json --once  # publie config puis quitte

Dépendance: paho-mqtt (pip install paho-mqtt)

Format du fichier de mapping (JSON):
{
  "broker": {"host": "...", "port": 1883, "username": "...", "password": "..."},
  "device": {"identifiers": ["lupo"], "name": "Lupo"},
  "source_topic": "lupo/assiette",
  "sensors": [
    {"key": "pitch", "name": "Van Pitch", "unit": "°", "state_topic": "lupo/assiette/pitch"},
    {"key": "roll",  "name": "Van Roll",  "unit": "°", "state_topic": "lupo/assiette/roll"}
  ]
}
"""

import argparse
import json
import sys
import time

try:
    import paho.mqtt.client as mqtt
except ImportError:
    print("ERREUR: paho-mqtt manquant. Installer avec: pip install paho-mqtt", file=sys.stderr)
    sys.exit(1)


def load_mapping(path):
    with open(path, "r") as f:
        return json.load(f)


def publish_discovery_configs(client, mapping):
    """Publie les topics config Discovery pour chaque capteur (retain=true, une fois)."""
    device = mapping["device"]
    node_id = "_".join(device["identifiers"])
    for sensor in mapping["sensors"]:
        object_id = sensor["state_topic"].replace("/", "_")
        config_topic = f"homeassistant/sensor/{node_id}_{object_id}/config"
        payload = {
            "name": sensor["name"],
            "state_topic": sensor["state_topic"],
            "unit_of_measurement": sensor.get("unit", ""),
            "unique_id": f"{node_id}_{object_id}",
            "device": device,
        }
        client.publish(config_topic, json.dumps(payload), retain=True, qos=1)
        print(f"[discovery] {config_topic} -> {sensor['name']}")


def build_client(broker_cfg):
    client = mqtt.Client(protocol=mqtt.MQTTv5)
    if broker_cfg.get("username"):
        client.username_pw_set(broker_cfg["username"], broker_cfg.get("password"))
    client.connect(broker_cfg["host"], broker_cfg.get("port", 1883), keepalive=60)
    return client


def main():
    parser = argparse.ArgumentParser(description="Pont MQTT Discovery générique PKA")
    parser.add_argument("--config", required=True, help="Fichier de mapping JSON")
    parser.add_argument("--once", action="store_true", help="Publie les configs Discovery puis quitte (pas de relais d'état)")
    args = parser.parse_args()

    mapping = load_mapping(args.config)
    client = build_client(mapping["broker"])
    client.loop_start()

    publish_discovery_configs(client, mapping)

    if args.once:
        time.sleep(1)
        client.loop_stop()
        client.disconnect()
        print("Configs Discovery publiées. Fin (--once).")
        return

    source_topic = mapping["source_topic"]
    sensors = mapping["sensors"]
    source_format = mapping.get("source_format", "flat")

    def extract_flat(data, sensor):
        if sensor["key"] in data:
            return data[sensor["key"]]
        return None

    def extract_sensor_logger(data, sensor):
        """Extrait les valeurs depuis le format Sensor Logger (payload[] avec name/values)."""
        import math
        key = sensor["key"]

        # Capteurs d'orientation : radians → degrés
        orientation_keys = {"pitch", "roll", "yaw"}
        if key in orientation_keys:
            for item in data.get("payload", []):
                if item.get("name") == "orientation":
                    values = item.get("values", {})
                    if key in values:
                        return round(values[key] * 180.0 / math.pi, 2)

        # Capteurs GPS : dans payload[name=location]
        gps_keys = {"latitude", "longitude", "altitude", "speed", "course"}
        if key in gps_keys:
            for item in data.get("payload", []):
                if item.get("name") == "location":
                    values = item.get("values", {})
                    if key in values:
                        return round(values[key], 5) if key in ("latitude", "longitude") else round(values[key], 1)

        # Baromètre : dans payload[name=barometer]
        if key == "pressure":
            for item in data.get("payload", []):
                if item.get("name") == "barometer":
                    values = item.get("values", {})
                    if "pressure" in values:
                        return round(values["pressure"], 0)

        # Batterie : dans payload[name=battery]
        if key == "batteryLevel":
            for item in data.get("payload", []):
                if item.get("name") == "battery":
                    values = item.get("values", {})
                    if "batteryLevel" in values:
                        return round(values["batteryLevel"] * 100, 0)

        # Capteurs compas/magnetometer : magneticBearing en radians → degrés
        compass_keys = {"magneticBearing"}
        if key in compass_keys:
            for item in data.get("payload", []):
                if item.get("name") in ("compass", "magnetometer"):
                    values = item.get("values", {})
                    if key in values:
                        val = values[key]
                        # Si < 2π (~6.28), c'est en radians → convertir
                        if val < 7:
                            return round(val * 180.0 / math.pi, 2)
                        return round(val, 2)

        # Fallback : cherche la clé dans n'importe quel payload
        for item in data.get("payload", []):
            values = item.get("values", {})
            if key in values:
                return values[key]

        return None

    extractors = {
        "flat": extract_flat,
        "sensor_logger": extract_sensor_logger,
    }
    extract = extractors.get(source_format, extract_flat)

    # Cache GPS pour device_tracker combiné
    gps_cache = {"latitude": None, "longitude": None}
    position_topic = mapping.get("device_tracker", {}).get("state_topic", "")

    def on_message(c, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return
        updated = False
        for sensor in sensors:
            value = extract(data, sensor)
            if value is not None:
                client.publish(sensor["state_topic"], value, qos=0)
                if sensor["key"] in ("latitude", "longitude"):
                    gps_cache[sensor["key"]] = value
                    updated = True
        if updated and position_topic and gps_cache["latitude"] is not None and gps_cache["longitude"] is not None:
            client.publish(position_topic, json.dumps(gps_cache), qos=0)

    client.on_message = on_message
    client.subscribe(source_topic)
    print(f"[bridge] écoute {source_topic} — relais vers {len(sensors)} capteurs. Ctrl+C pour arrêter.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        client.loop_stop()
        client.disconnect()


if __name__ == "__main__":
    main()
