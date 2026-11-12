# Hub Esneux — Infrastructure partagée Serre + Maison

> **Architecture cible historique du 2026-06-22 — ne décrit pas intégralement le matériel installé.**
> Partagée entre `iot-serre/` et `iot-maison/`. À réviser avec le RPi bureau existant avant tout achat.

## État réel au 2026-11-05

- Le seul **RPi HAOS observé** est `lupo` : **RPi 5, 8 Go de RAM, SD 256 Go**, actuellement au bureau et accessible via Tailscale. Aucun second RPi n'est ajouté au stock ; l'écart avec l'achat historique 4 Go reste à réconcilier.
- Deux **AirGuard TH E-Ink** sont enregistrés : **SNZB-02UL = Lupo** et **SNZB-02DR2 = Serre**. Le signal Lupo a été jugé satisfaisant à 12 m à travers des murs lors du test précédent, mais sa dernière trame réelle date de 13:01 ; une mesure fraîche reste à valider le 06/11.
- **Zigbee2MQTT est opérationnel** : le dongle a été déplacé du port noyau `1-2` vers `3-2`, puis relancé une fois. Après le test initial de 10 min, le contrôle de 23:50 confirme près de 3 h sans nouvelle déconnexion USB ni sous-tension ; Z2M est actif et MQTT connecté. À 23:46, l'AirGuard Serre a publié : **22,5 °C, 55,7 %, batterie 95 %, LQI 255/255**. Aucune mise à jour corrective n'est indiquée. En cas de récidive, tester une courte rallonge USB2 puis l'alimentation officielle directe, une variable à la fois.
- Un seul ZBDongle-E est détecté. Le second a été commandé le 05/11 pour la maison/serre, livraison prévue le 06/11 ; réception, affectation et installation non confirmées.
- Ce RPi est aussi la cible matérielle du van : les rôles fixe et embarqué ne sont pas simultanés sans déplacer le RPi ou utiliser un autre hub fixe. Le M5 dispose déjà de HA/Mosquitto, mais son pont Zigbee est en panne faute de dongle local.
- Le développement fonctionnel serre/maison reste gelé ; ce pilote ne vaut pas reprise du projet complet.

## Cible d'architecture — Option B « SSD + UPS »

```
┌──────────────────────────────────────┐
│  X1201-C1 Boîtier métal              │
│  ┌────────────────────────────────┐  │
│  │  X1001 NVMe HAT + SSD 128 Go   │  │ ← cible, non confirmée
│  │  M.2 2280 NVMe                 │  │
│  ├────────────────────────────────┤  │
│  │  RPi 5 (8 Go) — cible BOM      │  │
│  ├────────────────────────────────┤  │
│  │  X1201 UPS + 2× 18650          │  │ ← cible, non confirmée
│  └────────────────────────────────┘  │
└──────────────────────────────────────┘
```

## BOM cible historique (~298 €, non consolidée)

| Composant | Référence envisagée | Prix est. historique | Statut |
|---|---|---|---|
| RPi 5 | Raspberry Pi 5 8 Go | ~188 € | À réconcilier avec le RPi existant |
| UPS | Geekworm X1201 V1.1 | ~25 € | Cible, non confirmée |
| NVMe HAT | Geekworm X1001 | ~15 € | Cible, non confirmée |
| SSD | M.2 NVMe 128 Go | ~20 € | Cible, non confirmée |
| Boîtier | Geekworm X1201-C1 | ~20 € | Stock global à réconcilier avant achat |
| Alim | USB-C PD 5 V 5 A | ~15 € | À réconcilier avec le matériel existant |
| Accus | 2× 18650 | ~15 € | Stock global disponible, compatibilité à vérifier |

> Cette BOM ne doit pas être commandée telle quelle : inventorier d'abord le RPi bureau et les composants déjà reçus.

## Protections envisagées

| Couche | Cible |
|---|---|
| Stockage | SSD NVMe plutôt que SD pour la cible historique |
| UPS | Shutdown propre via I2C |
| Système de fichiers | OverlayFS en lecture seule sur la partition système |
| Watchdog | Watchdog matériel + systemd |
| Sauvegarde | Configuration HA vers Mac M1 via Tailscale |

Ces protections sont des choix de conception à vérifier, pas des fonctions confirmées sur le pilote actuel.

## Stack logicielle cible

- Home Assistant OS bare metal
- Zigbee2MQTT ou ZHA avec Sonoff ZBDongle-E
- Mosquitto local
- Tailscale
- M1 pour Frigate/Whisper en option ultérieure

## Capteurs partagés envisagés

| Capteur | Usage serre | Usage maison |
|---|---|---|
| Station météo Ecowitt | Pluie, température extérieure, arrosage/ventilation | Dashboard météo |
| Capteur température/humidité extérieur | Référence climatique | Confort et alerte gel |

Les deux AirGuard actuellement appairés constituent un pilote de mesure, pas la couverture complète de cette cible.

## Dashboard envisagé

- Vue « Serre » : humidité du sol, arrosage, température, ventilation.
- Vue « Maison » : température/humidité des pièces, énergie, sécurité.
- Vue « Météo » : station Ecowitt.

---

*Document recadré le 2026-11-05 : état réel en tête, architecture du 22/06 conservée comme cible historique.*
