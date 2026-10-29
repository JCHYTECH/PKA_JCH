#!/usr/bin/env python3
"""Pont HTTP→MQTT dans Docker — utilise host.docker.internal pour MQTT."""
import json
from http.server import HTTPServer, BaseHTTPRequestHandler
import paho.mqtt.client as mqtt

BROKER_HOST = "host.docker.internal"
BROKER_PORT = 1883
USERNAME = "jchavaux"
PASSWORD = "Dobby2026!"
TOPIC = "esneux/iphone"

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
mqtt_client.username_pw_set(USERNAME, PASSWORD)
mqtt_client.connect(BROKER_HOST, BROKER_PORT, 60)
mqtt_client.loop_start()
print("[bridge] MQTT connecté à host.docker.internal:1883", flush=True)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length).decode()
        print(f"[bridge] RECU {len(body)}o: {body[:200]}", flush=True)
        try:
            data = json.loads(body)
            items = data.get("payload", [data])
            for item in items:
                name = item.get("name", "")
                values = item.get("values", {})
                print(f"[bridge] sensor={name} keys={list(values.keys())}", flush=True)
                if name == "barometer":
                    p = values.get("pressure")
                    a = values.get("relativeAltitude")
                    if p is not None:
                        mqtt_client.publish("esneux/iphone/pressure", p, qos=0)
                        print(f"[bridge] → MQTT pressure={p}", flush=True)
                    if a is not None:
                        mqtt_client.publish("esneux/iphone/altitude", a, qos=0)
                        print(f"[bridge] → MQTT altitude={a}", flush=True)
                    msg = {}
                    if p is not None: msg["pressure"] = p
                    if a is not None: msg["relativeAltitude"] = a
                    if msg:
                        mqtt_client.publish(TOPIC, json.dumps(msg), qos=0)
            self.send_response(200)
        except Exception as e:
            print(f"[bridge] ERROR: {e}", flush=True)
            self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        pass

print("[bridge] HTTP sur port 8888 → http://192.168.129.31:8888/data", flush=True)
HTTPServer(('0.0.0.0', 8888), Handler).serve_forever()
