# Procédure d'appairage — Capteurs Zigbee (Van Lupo)

> **Date :** 2026-10-05 | **Orchestré par :** Dobby 🦉
> **Objectif :** appairer et nommer les capteurs Zigbee de la cellule van, de façon standardisée et reproductible, pour tenir la deadline du **1er novembre 2026**.
> **Règle multi-terminal :** chaque commande/action est préfixée par sa machine cible — [M5] (Mac), [RPi] (Lupo), [M1] (serveur LLM). L'appairage se pilote depuis un navigateur (Mac/iPad), l'iPhone sert à la vérification live.
> **Contexte :** RPi 5 Lupo, HAOS 18.3, Zigbee opérationnel (Sonoff ZBDongle-E, Ember, canal 15), Zigbee2MQTT → Mosquitto `:1883`. Réseau « up, 0 appareil joint » au 01/10.

---

## Prérequis

- [ ] [RPi] RPi 5 sous tension, Home Assistant accessible (IP locale ou Tailscale).
- [ ] [M5] Zigbee2MQTT opérationnel (add-on HA actif, dongle reconnu).
- [ ] Capteur + sa batterie insérée (voir tableau §4).
- [ ] À portée radio du coordinateur (le dongle est sur le RPi ; appairer **près du RPi** pour la première jonction).

---

## Procédure générique (tous capteurs)

### Étape 0 — Préparer le capteur
- Insérer la batterie (retirer la languette plastique le cas échéant).
- Vérifier qu'il est **hors du mode « Proximity »** (réservé à l'app eWeLink) — on vise le **mode Zigbee**.

### Étape 1 — Ouvrir le réseau (Permit join)
1. [M5/iPad] Navigateur → Home Assistant : `http://lupo.local:8123` ou `http://<IP-Tailscale>:8123`.
2. Settings → Add-ons → **Zigbee2MQTT** → « **Open Web UI** » (ou `http://<IP>:8099`).
3. Clic **« Permit join (All) »** → réseau ouvert ~4 min (254 s).

### Étape 2 — Mettre le capteur en mode appairage
- **Appui long ~5 s** sur le bouton d'appairage (arrière ou face, selon modèle) jusqu'au clignotement de l'indicateur (LED ou icône signal Zigbee à l'écran).

### Étape 3 — Renommer (friendly_name)
- Le capteur apparaît en quelques secondes sous un nom technique (`0x…` = son adresse IEEE).
- **Méthode automatisée (Dobby)** : service HA `mqtt.publish` (credentials internes de HA, pas besoin du mot de passe MQTT) :
  - topic `zigbee2mqtt/bridge/request/device/rename`
  - payload `{"from": "<ieee>", "to": "<friendly_name>"}`
- **Méthode manuelle (UI)** : [M5/iPad] Z2M → Open Web UI → clic sur l'appareil → onglet **About** → changer `friendly_name`.
- Convention de nommage : §3. ⚠️ HA ne renomme pas les `entity_id` automatiquement — renommer ensuite dans HA (Appareils → Entités → ⋮ → Renommer).

### Étape 4 — Vérifier les entités
- Home Assistant **auto-découvre** via MQTT → entités `sensor.<friendly>_temperature`, `_humidity`, `_battery`, `binary_sensor.<friendly>_contact`, etc.
- [iPhone] App Home Assistant → vérifier que les valeurs remontent en live.

### Étape 5 — Placement + test de signal
- Placer le capteur à son emplacement final (frigo, porte, cellule…).
- [iPhone] Vérifier la valeur qui évolue et le **linkquality** (signal) dans Z2M : viser ≥ 40.

---

## Convention de nommage (friendly_name)

| Usage | friendly_name | Entités exposées |
|---|---|---|
| Frigo (T°/H°) | `frigo` | `sensor.frigo_temperature`, `sensor.frigo_humidity`, `sensor.frigo_battery` |
| Cellule (T°/H°) | `cellule` | `sensor.cellule_temperature`, `sensor.cellule_humidity` |
| Portes cabine | `door_front_left`, `door_front_right` | `binary_sensor.door_front_left_contact` |
| Porte coulissante | `door_sliding_left`, `door_sliding_right` | `binary_sensor.door_sliding_*_contact` |
| Hayon | `door_tailgate` | `binary_sensor.door_tailgate_contact` |
| Toit relevable | `door_popup_roof` | `binary_sensor.door_popup_roof_contact` |
| Frigo (contact porte) | `door_fridge` | `binary_sensor.door_fridge_contact` |

> Règle : `snake_case`, en anglais, descriptif. Ne pas utiliser de majuscules ni d'espaces (contrainte MQTT/HA).

---

## Capteurs van — geste d'appairage

| Capteur | Modèle | Geste pairing | Batterie |
|---|---|---|---|
| T°/H° frigo | Sonoff **SNZB-02DR2** (AirGuard TH) | appui long 5 s → icône signal Zigbee clignote | **2× AAA (LR03)** |
| T°/H° (sans écran) | Sonoff **SNZB-02D** | appui long 5 s → icône clignote | CR2450 |
| T°/H° cellule (rapide) | Sonoff **SNZB-02P** | appui long 5 s | CR2477 |
| Contact porte (Aqara) | Aqara **MCCGQ11LM** | appui long 5 s → LED bleue clignote | CR1632 |
| Contact porte/toit (Sonoff) | Sonoff **SNZB-04P** | appui long 5 s | CR2477 |

> Pour tout modèle : si la LED n'existe pas, se fier à l'apparition dans la liste Z2M dans les ~30 s.
> ⚠️ Types de batterie : **SNZB-02DR2** (2× AAA) et **SNZB-02D** (CR2450) sont vérifiés (docs officielles). Les autres (CR1632/CR2477) sont indicatifs — confirmer sur la notice du capteur avant achat de piles.

---

## Dépannage

| Symptôme | Action |
|---|---|
| Ne se joint pas | Retirer une pile 10 s → réinsérer → refaire « Permit join » + appui long |
| Rapporte mal / valeurs figées | Force-remove dans Z2M → redémarrer Z2M → re-pair |
| Apparaît « unsupported » | Mettre à jour Zigbee2MQTT (modèle récent) ou ajouter un convertisseur externe |
| Signal faible (linkquality < 40) | Rapprocher du dongle, ou ajouter un routeur Zigbee (prise Sonoff S31) |

---

## Outil recommandé par étape

| Étape | Outil |
|---|---|
| Permit join + renommage + OTA | **Mac** (ou iPad) — UI Z2M confortable |
| Appui physique sur le capteur | À la main (peu importe l'outil) |
| Vérification live + placement | **iPhone** — app Home Assistant |
| Notifications / supervision route | iPhone (Tailscale) |

---

## Points de vigilance

1. **Ne JAMAIS laisser l'auto-update HAOS** (bug 18.x) — voir `PROCEDURE-REACTIVATION-IOT-VAN-2026-10-01.md`.
2. Appairer **près du RPi** (banc) avant d'installer dans le van.
3. La **SNZB-02DR2** supporte l'OTA ; firmware **1.0.5+** requis pour la fonction « affichage distant » (script officiel `SNZB-02DR2_Remote_Temp_Humidity_Features_Z2M.zip`).
4. Double-clic bouton sur Sonoff = bascule °C/°F de l'affichage (ne change pas l'unité mesurée).
5. Après appairage, mettre à jour `LISTE-CAPTEURS-ZIGBEE-2026-10-01.md` (statut « appairé ») et `thread-iot.md`.

---

*Fichier maintenu par Dobby 🦉 — à mettre à jour après chaque session d'appairage.*
