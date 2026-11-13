# Mode d'emploi — Intégration Sonoff Zigbee → Home Assistant

> Édition : 2026-06-13 — [[Dobby]] 🦉  
> Contexte : installation d'un Sonoff AirGuard TH (SNZB-02DR2) + extension à tous les capteurs Zigbee  
> HA : 2026.5.4 — Docker sur Mac M5 — `http://localhost:8123`

---

## Pourquoi cette procédure ?

Tu as un capteur Sonoff AirGuard TH (température + humidité, écran LCD). C'est un capteur **Zigbee**, pas WiFi. Il ne peut pas parler directement à Home Assistant — il lui faut un **coordinateur Zigbee** (un dongle USB qui fait le pont radio).

Une fois le coordinateur installé, **tous** les futurs capteurs Zigbee (Sonoff, Aqara, Philips Hue, IKEA, etc.) s'y connecteront sans matériel supplémentaire.

---

## Matériel

| Élément | Modèle | Prix approx. | Où acheter |
|---------|--------|:---:|------------|
| Dongle Zigbee USB | **Sonoff ZBDongle-E** (recommandé) | ~25€ | Amazon, AliExpress, Mouser |
| Alternative | Sonoff ZBDongle-P | ~30€ | Idem |
| Capteur (déjà possédé) | Sonoff AirGuard TH SNZB-02DR2 | ✓ | — |

Le **ZBDongle-E** utilise une puce Silicon Labs EFR32MG21 (plus récente, firmware EZSP). Le **ZBDongle-P** utilise une Texas Instruments CC2652P (compatible Z-Stack). Les deux fonctionnent, le -E est plus récent.

---

## Étape 1 — Brancher le dongle

1. Brancher le dongle sur un port USB du Mac M5
2. Ouvrir un terminal et vérifier qu'il est détecté :

```bash
ls /dev/ttyUSB* /dev/ttyACM*
```

Tu devrais voir `/dev/ttyUSB0` (ZBDongle-P) ou `/dev/ttyACM0` (ZBDongle-E).

Si rien n'apparaît :
- Vérifier que le dongle est bien enfoncé
- Essayer un autre port USB
- Pas de driver nécessaire sur macOS

---

## Étape 2 — Lancer le script d'installation

```bash
bash /Users/jchavauxm5/PKA_JCH/_local/install-zigbee-ha.sh
```

Ce script fait automatiquement :
1. Détecte le dongle branché
2. Stoppe le container Home Assistant
3. Recrée le container avec le dongle passé en `--device`
4. Affiche les instructions pour la suite

**Ce que fait la commande docker en détail :**
```
docker stop homeassistant
docker rm homeassistant
docker run -d \
  --name homeassistant \
  --restart unless-stopped \
  --device=/dev/ttyUSB0:/dev/ttyUSB0 \
  -v /Users/jchavauxm5/PKA_JCH/_local/homeassistant:/config \
  -p 8123:8123 \
  ghcr.io/home-assistant/home-assistant:stable
```

> ⚠️ Le container est recréé, mais **toutes les données HA sont préservées** (elles sont dans le volume `_local/homeassistant`).

---

## Étape 3 — Activer ZHA dans Home Assistant

ZHA (Zigbee Home Automation) est l'intégration Zigbee **intégrée** à Home Assistant — aucun addon à installer, pas de HACS nécessaire.

1. Ouvrir `http://localhost:8123`
2. Aller dans **Paramètres** (⚙️ en bas à gauche)
3. **Appareils & services** → **Ajouter une intégration** (bouton bleu en bas)
4. Chercher **Zigbee Home Automation** → cliquer dessus
5. Dans la fenêtre de configuration :
   - **Port série** : sélectionner le device détecté (`/dev/ttyUSB0` ou `/dev/ttyACM0`)
   - **Radio type** : laisser **auto-détection** (ou sélectionner EZSP pour ZBDongle-E)
   - **Network settings** : laisser par défaut (canal 15, auto)
6. Cliquer **Submit**

ZHA crée le réseau Zigbee. Une carte visuelle apparaît — elle est vide pour l'instant.

![Schéma logique]
```
  Capteurs Zigbee (Sonoff, Aqara...)
         │
    ~~~ Zigbee 2.4 GHz ~~~
         │
  Dongle USB (coordinateur)
         │
    ── USB ──
         │
  Mac M5 → Docker → Home Assistant
         │
    http://localhost:8123 (interface)
```

---

## Étape 4 — Appairer le AirGuard TH

1. Dans HA, aller sur l'intégration **ZHA**
2. Cliquer **Ajouter un appareil** (en bas)
3. HA passe en mode recherche (compte à rebours de 60 secondes)
4. **Sur le capteur Sonoff** : faire un **appui long de 5 secondes** sur le bouton
   - La LED se met à clignoter → le capteur est en mode appairage
5. HA détecte le capteur automatiquement en quelques secondes
6. Il apparaît avec :
   - **Entité température** (`sensor.xxx_temperature`)
   - **Entité humidité** (`sensor.xxx_humidity`)
   - **Entité batterie** (`sensor.xxx_battery`)
   - **Écran LCD** reconnu comme entité de configuration

---

## Étape 5 — Vérifier et utiliser

### Sur le dashboard HA
- Les entités température/humidité apparaissent automatiquement
- Tu peux les ajouter à un tableau de bord (carte `Entités` ou `Jauge`)

### Via l'app iPhone
- L'app Home Assistant (déjà installée sur ton iPhone JCH 17) affiche les données
- Notifications possibles : alerte si température > seuil, batterie faible, etc.

### Automatisations possibles (exemples)
```yaml
# Alerte température élevée
alias: "Alerte chaleur bureau"
trigger:
  - platform: numeric_state
    entity_id: sensor.airguard_th_temperature
    above: 28
action:
  - service: notify.mobile_app_jch_17
    data:
      message: "Température bureau : {{ states('sensor.airguard_th_temperature') }}°C"
```

---

## Ajouter d'autres capteurs Zigbee plus tard

Une fois le réseau Zigbee créé, ajouter un nouveau capteur prend 30 secondes :

1. ZHA → **Ajouter un appareil**
2. Mettre le capteur en mode appairage (appui long)
3. C'est tout

**Appareils compatibles testés avec ZHA :**
- Sonoff SNZB-02P/02D (température/humidité)
- Sonoff SNZB-03P (mouvement PIR)
- Sonoff SNZB-04P (ouverture porte/fenêtre)
- Aqara temperature/humidity/contact/vibration
- Philips Hue bulbs
- IKEA Trådfri bulbs/remotes

---

## Dépannage

| Symptôme | Cause probable | Solution |
|----------|---------------|----------|
| Dongle non détecté | Port USB défectueux ou câble | Changer de port, vérifier `ls /dev/tty*` |
| ZHA n'apparaît pas dans les intégrations | HA n'a pas redémarré après script | Redémarrer HA : Paramètres → Système → Redémarrer |
| Appairage échoue (timeout) | Capteur hors de portée | Rapprocher le capteur du dongle (< 2m) pour le premier appairage |
| Capteur déjà appairé ailleurs | Mémoire d'appairage antérieure | Reset usine : appui long 10s sur le bouton |
| Données ne se mettent pas à jour | Intervalle de rapport long | Dans ZHA → entité → Configurer → ajuster l'intervalle |

---

## À propos de HACS

**HACS n'est pas nécessaire pour ce capteur Zigbee.** ZHA est intégré à HA.

Tu installeras HACS plus tard si tu as besoin de :
- Intégrations communautaires non officielles
- Custom cards (cartes dashboard avancées)
- Thèmes visuels

**Installation HACS (pour référence future) :**
```bash
docker exec -it homeassistant bash
wget -O - https://get.hacs.xyz | bash -
```
Puis redémarrer HA → Paramètres → Intégrations → Ajouter → HACS.

---

*Document créé par [[Dobby]] le 2026-06-13. Projet : Home Assistant / STATION-DOMO.*
