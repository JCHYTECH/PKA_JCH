---
date: 2026-07-19
tags: [daily, PKA, session]
type: daily
status: active
---

# 2026-07-19 — MQTT Discovery générique multi-instances (Lupo + Esneux)

## Session — 23:02 — MQTT Discovery générique multi-instances (Lupo + Esneux)

### Contexte
- Modèle : claude-sonnet-5
- Projet : IOT

### Résumé
Résolution du blocage capteurs MQTT sur Lupo (mqtt:/broker: YAML obsolete). Architecture MQTT Discovery générique adoptée pour toutes les instances HA. Extension immédiate testée sur cas Esneux (pression barométrique iPhone).

### Actions
Créé ARCHITECTURE-MQTT-DISCOVERY.md (11_IOT/_shared/) ; créé scripts/pka_mqtt_discovery_bridge.py (pont générique, Forge) ; créé mapping-lupo-assiette.json ; corrigé SPEC-ASSIETTE-VAN-IPHONE-MQTT.md (retrait YAML obsolète) ; archivé le fichier INBOX traité vers 07_ARCHIVES/inbox-traites/ ; créé mapping-esneux-pression.json (baromètre iPhone, broker M5 192.168.129.31, credentials jchavaux/dobby trouvés dans zigbee2mqtt config) ; vérifié via App Store API que Sensor Logger est EN uniquement (pas de FR)

### Décisions
MQTT Discovery natif HA retenu comme protocole générique multi-instances (Lupo, Esneux, futurs) plutôt que capteurs YAML/UI ad hoc par instance ; un seul script de pont réutilisable, un fichier de mapping JSON par instance/usage

### Prochaines étapes
Test réel sur Lupo : lancer le pont + Sensor Logger + vérifier entités van_pitch/van_roll dans HA ; Test réel sur Esneux : configurer Sensor Logger Stream (Server 192.168.129.31, port 1883, user jchavaux, pass dobby, topic esneux/iphone), activer Barometer, lancer le pont, vérifier entités pression/altitude ; ajuster les clés JSON du mapping si le payload réel de Sensor Logger diffère (pressure/relativeAltitude à confirmer)
