# Résumé session — 2026-07-18 (soir)

> Dobby 🦉 — deepseek-v4 — 2026-07-18

---

## Ce qui a été fait

### 1. INBOX → Projets (Vetalyx + TRAVELS)

7 fichiers Vetalyx/DIAHO déplacés et renommés :
- `contacts/` : Q&A Dr. Wu, Profil Pr. Zheng Yilei, Message Peiwen (principes Wu : 110K€, 40/60, financement si manque)
- `strategy/` : Proposition AB next steps (création Vetalyx, budget validation 20K€, IgE totales chien/chat)
- `legal/contrat-diaho/` : Accord seing privé Renard 2026-07-08
- `legal/` : Bail type Novalis IDELUX (centre entreprises Arlon)
- `products/01 Zheda Dixun.../` : Product list Zheda Dxun (xlsx)

2 fichiers TRAVELS :
- `van technique/` : TowBox V5 Swing Union, Flat Jack Camper 2.0 instructions

### 2. Capteurs Lupo — Références AliExpress

Fichier créé : `11_IOT/iot-van/passe-utile/boms/references-aliexpress-capteurs-lupo.md`
- 11 capteurs avec URLs AliExpress Belgique (nl.aliexpress.com, EUR)
- MPU6050 GY-521 : 3× (au lieu de 1×, spare inclus)
- Total estimé : ~218€ AliExpress + ~30€ Amazon (PIR Optex)

### 3. Assiette van — Approche iPhone + MQTT

Décision : utiliser Sensor Logger (iOS) + MQTT → Mosquitto → Home Assistant. 0 matériel.

Fichier créé : `11_IOT/iot-van/specs/SPEC-ASSIETTE-VAN-IPHONE-MQTT.md`

Avancement :
- ✅ Sensor Logger installé sur iPhone
- ✅ Configuration MQTT : broker `192.168.129.16:1883`, topic `lupo/assiette`, TCP, sans TLS
- ✅ Mosquitto add-on actif sur Lupo (port 1883 exposé)
- ✅ Credentials MQTT enregistrés dans `JCH_PRIVATE/credentials-central.md` (jchavaux/dobby2026!)
- ⚠️ Capteurs HA NON configurés — voir blocage ci-dessous

---

## Difficultés rencontrées

### Problème principal : ajout capteurs MQTT dans HA

**Situation :** Mosquitto tourne (`docker ps` confirme, port 1883 accessible depuis le M5), mais les capteurs `sensor.van_pitch` et `sensor.van_roll` n'apparaissent pas dans HA.

**Tentatives :**
1. Ajout via `mqtt:` dans `configuration.yaml` avec `broker: core-mosquitto` → erreur : `broker` option invalide pour `mqtt:` (HA 2026.7)
2. Ajout sans `broker:` (juste `sensor:`) → config valide (`ha core check` OK), redémarrages multiples, mais capteurs non créés
3. Suppression du bloc `mqtt:` → retour à `default_config` seul → ok

**Cause probable :** `default_config` dans HA 2026.7 gère l'intégration MQTT de manière opaque. Le bloc `mqtt:` YAML ne semble pas se combiner avec. Les capteurs doivent probablement être ajoutés via l'UI : **Paramètres → Appareils et services → MQTT → Configurer → Ajouter une entité manuelle → Capteur**.

**Action pour JC :**
1. Ouvrir HA → Paramètres → Appareils et services → MQTT
2. Trouver l'option pour ajouter un capteur manuel
3. Créer 2 capteurs :

| Champ | Van Pitch | Van Roll |
|-------|-----------|----------|
| Topic | `lupo/assiette` | `lupo/assiette` |
| Unité | `°` | `°` |
| Template | `{{ value_json.pitch \| default(0) \| round(1) }}` | `{{ value_json.roll \| default(0) \| round(1) }}` |

### Problème secondaire : Sensor Logger MQTT streaming

L'onglet "Stream" n'était pas visible — probablement une feature Pro (payante). JC a trouvé le chemin de configuration directement.

### Problème tertiaire : redémarrage HA

- `ha core restart` via SSH timeout systématiquement
- Workaround : `docker restart homeassistant` (plus rapide)
- Attention : `docker restart` peut ne pas recharger le YAML proprement

---

## État actuel du fichier `configuration.yaml` (Lupo)

```yaml
default_config:
frontend:
  themes: !include_dir_merge_named themes
automation: !include automations.yaml
script: !include scripts.yaml
scene: !include scenes.yaml
```

Propre, pas de bloc `mqtt:`.

---

## Fichiers créés/modifiés cette session

| Fichier | Action |
|---------|--------|
| `11_IOT/iot-van/passe-utile/boms/references-aliexpress-capteurs-lupo.md` | Créé |
| `11_IOT/iot-van/specs/SPEC-ASSIETTE-VAN-IPHONE-MQTT.md` | Créé + mis à jour |
| `JCH_PRIVATE/credentials-central.md` | Ajout section Mosquitto Lupo |
| `08_VETALYX/` (7 fichiers) | Déplacés depuis INBOX |
| `07_TRAVELS/van technique/` (2 fichiers) | Déplacés depuis INBOX |

---

## Test à faire

1. Lancer Sensor Logger → Start Recording
2. Dans HA → Outils de développement → MQTT → Écouter `lupo/assiette`
3. Si les données arrivent → créer les capteurs via l'UI MQTT
4. Si pas de données → vérifier que Sensor Logger est bien sur le même WiFi que Lupo
