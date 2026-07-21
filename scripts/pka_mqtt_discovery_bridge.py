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
    client = mqtt.Client()
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

    def on_message(c, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
        except (json.JSONDecodeError, UnicodeDecodeError):
            return
        for sensor in sensors:
            if sensor["key"] in data:
                value = data[sensor["key"]]
                client.publish(sensor["state_topic"], value, qos=0)

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
