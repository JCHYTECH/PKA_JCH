# IOT — Index projet

> Projet ombrelle domotique JCH. État révisé le 2026-11-06.
> **Source de vérité opérationnelle : `thread-iot.md`** ; les autres documents distinguent état réel, cibles et historique.

## Point d'entrée

- **[thread-iot.md](thread-iot.md)** — état opérationnel, décisions et prochaines actions.
- **[IOT_DOSSIER_TECHNIQUE_V0.md](IOT_DOSSIER_TECHNIQUE_V0.md)** — référentiel technique consolidé et revue des risques ; certaines architectures restent des cibles.
- **[executive-summary.md](JCH_Inbox/03_PROJECTS/11_IOT/executive-summary.md)** — synthèse externe de l'état réel.
- **[OPERATIONS-CAN-OBD.md](iot-van/OPERATIONS-CAN-OBD.md)** — diagnostic réel et validation locale WiCAN/RUT240.

## Nature et périmètre

- **Infrastructure personnelle**, sans objectif de commercialisation.
- **Quatre nœuds cibles** : `M5 Docker`, hub fixe Esneux, `RPi 5 Van Lupo`, `RPi Italie` planifié.
- **Un seul RPi HAOS observé** : `lupo`, RPi 5 8 Go, actuellement au bureau Esneux. Il ne peut pas couvrir simultanément les rôles fixe et embarqué ; aucun second RPi n'est créé dans l'inventaire.
- Autonomie par site, supervision iPhone via **Tailscale**, objectif **zéro cloud / zéro abonnement**.

## Sous-projets

| Projet | Hub / lieu | Statut |
|---|---|---|
| [`iot-van/`](iot-van/) | Cible RPi 5 voiture 12 V — Westfalia Kelsey « Lupo » | 🔴 **P0 — échéance 15/12/2026** ; hub actuellement au bureau |
| [`iot-serre/`](iot-serre/) | Pilote sur le RPi `lupo` à Esneux | ⚪ développement fonctionnel gelé ; pilote Zigbee opérationnel et mesure Serre validée |
| [`iot-maison/`](iot-maison/) | Même pilote provisoire | ⚪ développement fonctionnel gelé |
| [`karotz-reborn/`](karotz-reborn/) | Karotz ressuscité — avatar physique Dobby (M5) | 🟡 en projet — à flasher (miniil Karotz OS) |
| [`cozmo-reborn/`](cozmo-reborn/) | Cozmo → compagnon IA local (M5 + M1 Ollama) | ⚪ en préparation — PoC SDK + vision à définir |
| [`_shared/`](_shared/) | Ressources communes | Documentation, achats et architecture cible |

## Structure réelle

```
11_IOT/
├── INDEX.md
├── IOT_DOSSIER_TECHNIQUE_V0.md
├── thread-iot.md
├── executive-summary.md
├── iot-van/
│   ├── ASSEMBLAGE-RPi5-VANLIFE.md · BOM-VANLIFE.md · scenarios-algorithmes-vanlife.md
│   ├── OPERATIONS-CAN-OBD.md · procédures, diagnostics et postmortem
│   ├── adr/ · specs/ · ds300-tap/ · carplay/ · dashboard/
│   ├── enclosure/ · rpi-config/ · securite/ · 99_REFERENCES/
│   └── passe-utile/
├── iot-serre/ · iot-maison/
├── karotz-reborn/
├── cozmo-reborn/
├── _shared/
├── PROTOCOLES/progress.md
├── guide installation HA/
└── HISTORIQUE/
```

## État par site au 2026-11-05

| Site | État confirmé | Reste à établir |
|---|---|---|
| **RPi `lupo`, actuellement au bureau** | RPi 5 **8 Go**, SD 256 Go, HAOS 18.3, **Healthy/Supported** ; Wi-Fi maison, Ethernet désactivé ; ZBDongle-E sur nouveau port USB, Z2M/MQTT stables près de 3 h et mesures fraîches AirGuard Serre jusqu'à 23:46 | Écart avec l'achat documenté d'un RPi 4 Go ; surveillance USB seulement en cas de récidive ; réception du second dongle non confirmée |
| **Van Lupo** | WiCAN Pro documenté comme physiquement installé ; RUT240 en stock ; AirGuard Lupo appairé | Dernière trame réelle Lupo à 13:01, mesure fraîche à revalider le 06/11 ; aucun appareil/entité WiCAN dans HA ; aucune liaison RUT240 Ethernet ; réseau van, entités CAN, Exosfer, alimentation et tests à valider |
| **M5 Docker** | HA et Mosquitto actifs | Zigbee2MQTT redémarre en boucle : `/dev/tty.usbserial-1110` absent du pont série |
| **Italie** | Site planifié | Périmètre et matériel non définis |

## Achats et budgets

- La [liste P1 du 01/10](iot-van/LISTE-CAPTEURS-ZIGBEE-2026-10-01.md) contient **10 articles pour environ 121 € estimés**, température frigo et éclairage compris. Les anciens 118–133 € et « température couverte » ne décrivent plus ce panier.
- Le [registre procurement](_shared/procurement-register.md) distingue commandes reçues et besoins non chiffrés. Mopeka P3 (~45 € historiques) est hors P1.
- X1200 : spécifications constructeur vérifiées (5,1 V/5 A, deux 18650, jauge I²C), mais prix courant et compatibilité avec le boîtier X1201-C1 non validés.
- DC-DC USB-C PD 5 A, silentblocs et coating n'ont pas de prix consolidé : **aucun total final de reste à payer**.
- Les totaux historiques (~1 026 € van, ~298 € hub Esneux) sont **non consolidés**.

## Points techniques bloquants

Le **Zigbee RPi n'est plus bloquant** : après déplacement du dongle de `1-2` vers `3-2` et une relance contrôlée, le test initial de 10 min a été prolongé par un contrôle à 23:50, près de 3 h après le changement, sans nouvelle coupure USB ni sous-tension. AirGuard Serre a publié à 23:46 : 22,5 °C, 55,7 %, batterie 95 %, LQI 255/255. Conserver ce port ; aucune mise à jour corrective n'est indiquée. AirGuard Lupo reste à réveiller pour obtenir une mesure fraîche.

1. **Zigbee M5** : pont série configuré sur un périphérique absent ; ne pas assimiler les conteneurs M5 à HAOS sur `lupo`.
2. **WiCAN/RUT240** : aucune intégration HA détectée et aucune liaison Ethernet ; intervention locale dans le van nécessaire.
3. `iot-van/ds300-tap/esphome-ds300.yaml` : **GPIO8 utilisé deux fois**, à corriger avant flash.
4. **Alimentation** : DC-DC USB-C PD 5 A à spécifier ; identifier le X1205 et ses accus avant de commander un X1200.
5. Canal Zigbee 15 recouvrant Wi-Fi 6 : choisir un canal hors Wi-Fi 1/6/11 après vérification locale.
6. **Sous-tension RPi détectée le 06/11** : alerte matérielle `Under-voltage detected`. Vérifier physiquement l'alimentation et le câble ; ne pas conclure à une panne Zigbee ni effacer l'alerte sans traitement.

## Supervision et MCP — contrôles du 2026-11-06

- **MCP natif HA, lecture seule** : relais persistant M5 `[::1]:8123` vers Lupo `192.168.129.16:8123`, sans exposition Internet. Kimi et DeepSeek ont réellement interrogé les capteurs. Claude est configuré mais nécessite une nouvelle authentification ; Codex a obtenu OAuth HA mais son compte refuse les modèles demandés. ChatGPT Web et le MCP du Core M5 ne sont pas validés. Aucune action domotique n'est exposée.
- **AirGuard** : `http://lupo:8123/airguard-supervision/0` affiche mesures, batteries, tension et historiques 24 h. Batteries : Lupo 100 %, Serre 95 %, tension Serre 2700 mV. Aucune entité LQI/linkquality/last_seen n'est disponible ; aucune alerte de péremption arbitraire n'est créée. Incendie, CO et sécurité restent locaux et déterministes.
- **Time Machine v2.4.1** : module actif uniquement par Ingress, planification `17 3 * * *`, Europe/Brussels, rétention 30 et Smart Backup. Premier instantané `/media/timemachine/2026/11/2026-11-06-120648` : **10 fichiers, 52 KiB**. Lecture et diff Lovelace validés ; planification automatique future, restauration et copie hors du RPi non validées. Ce n'est pas une sauvegarde HA complète.
- **Défaut amont limité** : la validation d'un chemin inexistant provoque une erreur d'affichage `TypeError` (`#backupPathError` absent). Après création du dossier, la validation, la copie et le diff fonctionnent ; aucun code du module n'est modifié. L'audit statique `.supply-chain-risk-auditor/results.md` n'est ni un scan CVE actif ni une certification.

## Spécialistes

- **Araignée** — Zigbee/Z2M, ESPHome, capteurs
- **Forge** — hardware, alimentation, ADR, CAN/OBD
- **Atlas** — documentation, synthèse, cohérence
- **Vega** — architecture

---

*Index maintenu par Dobby 🦉 — cohérence documentaire révisée le 2026-11-06.*
