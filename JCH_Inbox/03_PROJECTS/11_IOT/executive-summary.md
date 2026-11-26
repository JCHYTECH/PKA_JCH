# IOT / Domotique — Executive Summary

> **Version 2.4 — 2026-11-06.** Document externe pour partenaires techniques et installateurs.
> État opérationnel : `thread-iot.md`. Référentiel technique : `IOT_DOSSIER_TECHNIQUE_V0.md`.
> **Infrastructure personnelle — pas de commercialisation.**

## En une phrase

Architecture domotique cible distribuée et autonome entre la base belge, le van Lupo et un site italien planifié, supervisée depuis un iPhone via Tailscale, avec pour objectif zéro cloud et zéro abonnement.

## Les nœuds

| Nœud | Rôle | État réel |
|---|---|---|
| **M5 Docker** | Base / développement Home Assistant | HA et Mosquitto actifs ; Zigbee2MQTT en échec, dongle local absent |
| **RPi `lupo`, actuellement à Esneux** | Pilote provisoire serre + maison, cible van | RPi 5 8 Go, HA sain ; Zigbee2MQTT opérationnel après changement de port USB et mesures Serre validées |
| **Van Lupo** | Véhicule nomade Westfalia Kelsey | 🔴 **P0 — échéance 15/12/2026** ; WiCAN/RUT240 non intégrés |
| **RPi Italie** | Résidence secondaire | ⚪ planifié |

Un seul RPi HAOS est observé. Les rôles fixe et embarqué sont donc des affectations successives tant qu'un autre hub n'est pas retenu pour Esneux. L'écart entre les 8 Go mesurés et l'achat historique d'un RPi 5 4 Go reste documenté, sans double comptage.

## Van Lupo — priorité P0

- **Hub disponible** : RPi 5 8 Go, SD 256 Go, HAOS 18.3, **Healthy/Supported**, actuellement au bureau et connecté au Wi-Fi maison. NVMe retiré ; Ethernet désactivé.
- **Alimentation** : X1200 envisagé, non commandé. Le constructeur confirme 5,1 V/5 A et la jauge I²C ; le boîtier X1201-C1 existant et les accus de la chaîne actuelle doivent être identifiés avant achat. Le DC-DC USB-C PD 5 A reste à spécifier.
- **Véhicule et réseau** : WiCAN Pro documenté comme physiquement installé, RUT240 en stock. Aucun appareil/entité WiCAN n'est enregistré dans HA et aucune liaison Ethernet RUT240 n'est active. Les **17+ entités CAN** sont une cible, pas une fonction livrée.
- **Capteurs** : un ZBDongle-E et deux AirGuard enregistrés. AirGuard Lupo = SNZB-02UL ; AirGuard Serre = SNZB-02DR2. Après déplacement du dongle sur un autre port USB et une relance contrôlée, Z2M/MQTT sont restés stables pendant le test de 10 min puis jusqu'au contrôle de 23:50, près de 3 h après le changement. AirGuard Serre a publié à 23:46 : 22,5 °C, 55,7 %, batterie 95 %, LQI 255/255. La dernière trame réelle retrouvée pour Lupo date de 13:01 : 20,9 °C, 51,8 %, batterie 100 %, LQI 56/255 ; une mesure fraîche reste à obtenir. La liste P1 comporte 10 articles pour environ 121 € historiques, température frigo et éclairage compris.
- **DS300 Tap** : cible de lecture du tableau CBE ; conflit GPIO8 à corriger avant flash.

## Pilote Esneux

- Home Assistant et le service Zigbee sont opérationnels sur le RPi après changement de port USB ; aucune nouvelle coupure ni sous-tension n'a été constatée pendant le test initial ni au contrôle final de 23:50.
- Le signal de l'AirGuard Lupo a précédemment été validé à 12 m à travers des murs ; ce test historique ne vaut pas mesure fraîche actuelle. Sa dernière trame réelle date de 13:01 et les publications ultérieures sont des valeurs retenues. L'AirGuard Serre a publié à 23:46 avec un LQI de 255/255.
- Un second ZBDongle-E a été commandé le 05/11 pour la maison/serre, avec livraison prévue le 06/11 ; réception et affectation au M5 ou à un autre hub non confirmées.
- Le développement des automatisations serre et maison reste gelé.

## Accès IA, supervision et sauvegarde — 06/11

- Le MCP natif Home Assistant de Lupo est accessible en **lecture seule** via un relais local M5 persistant, sans port Internet ouvert. Kimi et DeepSeek ont passé un appel réel sur les capteurs ; Claude nécessite une reconnexion, Codex reste bloqué par les modèles autorisés sur son compte. ChatGPT Web et le MCP du Core M5 ne sont pas validés.
- Le tableau `http://lupo:8123/airguard-supervision/0` a été vérifié avec mesures, batteries et historiques 24 h. Aucune alerte de sécurité ne dépend du LLM ; les alertes incendie, CO et sécurité restent locales et déterministes.
- Time Machine v2.4.1 est actif par Ingress et planifié à 03:17 (Europe/Brussels). La première copie contient 10 fichiers (52 KiB) et permet le diff Lovelace. La planification future et la restauration ne sont pas encore validées ; la copie reste sur le même RPi et ne remplace pas une sauvegarde complète/externalisée.
- **Alerte matérielle `Under-voltage detected`** : l'alimentation et le câble du RPi exigent une vérification physique. Les anciens tests sans sous-tension restent des observations datées, pas l'état actuel.

## Coûts — prudence

Les montants historiques (~1 026 € van, ~298 € hub Esneux) et les anciens restes à payer ne sont **pas consolidés**. La base P1 est arithmétiquement cohérente à ~121 €, mais ses prix datent du 01/10. X1200, DC-DC, silentblocs et coating ne permettent pas encore de calculer un total final fiable.

## Points de vigilance

1. Conserver le dongle du RPi sur le nouveau port USB et tester rallonge puis alimentation uniquement si la coupure récidive ; traiter séparément le pont série M5.
2. Corriger le conflit GPIO8 dans `ds300-tap` avant tout flash.
3. Vérifier la chaîne d'alimentation et la compatibilité X1200/boîtier/accus avant commande.
4. Établir localement RUT240 → réseau van → WiCAN → MQTT → HA avant toute automatisation CAN.
5. Valider Exosfer, la consommation réelle en veille et les PIDs du véhicule, sans présumer l'absence de risque batterie ou garantie.

## Stack

Home Assistant OS · Home Assistant Docker · MCP natif HA en lecture seule · Home Assistant Time Machine par Ingress · Raspberry Pi · Zigbee2MQTT · MQTT/Mosquitto · Tailscale · ESPHome · CAN/OBD WiCAN Pro · Victron en phase ultérieure.

---

*Synthèse alignée sur les faits confirmés ; les objectifs techniques ne sont pas présentés comme des fonctions déjà livrées.*
