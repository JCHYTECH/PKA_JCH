# Thread — IOT / Domotique

> Living document maintenu par Dobby 🦉.
> **Dernière mise à jour** : 2026-11-11 — RPi Home (JC home) **résolu** : Core port 80, SSH permanent, Z2M réinstallé et **healthy** (dongle `ttyUSB0`, MQTT connecté). Reste : **re-appairer 3 devices** (réseau reformé) + stabilité 24 h.
> **Statut** : 🔴 P0 van Lupo — échéance **15 décembre 2026**. Serre/maison : pilote actif, développement fonctionnel gelé.

---

## Vue d'ensemble

L'architecture cible reste distribuée : HA Docker sur M5, un hub maison/serre à Esneux, HAOS dans le van Lupo et un site italien planifié, supervisés via Tailscale.

**Un seul RPi HAOS est actuellement observé** : hostname `lupo`, RPi 5 avec 8 Go de RAM, physiquement au bureau Esneux lors de ce diagnostic. Les rôles « bureau » et « van » ne peuvent donc pas être simultanés sans déplacer ce RPi ou affecter un autre hub à la maison/serre. Aucun second RPi n'est ajouté au stock. L'achat historique d'un RPi 5 4 Go reste à réconcilier avec les 8 Go mesurés.

## État actuel

| Axe | Statut | Détail confirmé |
|-----|--------|-----------------|
| Global | 🔴 P0 | Lupo reste la priorité jusqu'au **15/12/2026** ; le pilote Esneux ne rouvre pas le développement serre/maison |
| Karotz (avatar Dobby) | 🟢 | Ressuscité 2026-11-09 : miniil OS + OpenKarotz, WiFi WPA/TKIP sur RUT240 dédié, web `http://192.168.129.250` |
| Cozmo (compagnon IA) | ⚪ | En préparation — fichier de travail `cozmo-reborn/README.md` créé 2026-11-10 ; PoC SDK + vision à définir |
| RPi HAOS `lupo` | 🟡 | RPi 5 **8 Go**, SD 256 Go, HAOS **18.3**, Core **2026.11.0**, Supervisor **2026.09.3**. Actuellement au bureau, sur le Wi-Fi maison ; Ethernet désactivé |
| RPi — mises à jour | 🟡 | Core **2026.11.0** installé et vérifié. HAOS **18.4**, Supervisor **2026.10.5** et autres modules proposés lors du diagnostic du 05/11 ; pas de nouvelle mise à jour forcée dans ce chantier |
| RPi — alimentation | 🟢 | `binary_sensor.raspberry_pi_power_status` = **off** (pas de sous-tension) au 10/11 ; alerte Repairs acquittée après déplacement propre + re-rallumage. RPi joignable (ping ~9,5 ms) |
| Van — NVMe | ⚫ | Fanxiang 256 Go retiré physiquement ; décision SD seule |
| Van — alimentation | 🟡 | Remplacement **X1205 → X1200** envisagé, non commandé. X1200 validé sur datasheet en 5,1 V/5 A avec jauge I²C ; compatibilité du boîtier X1201-C1 et format réel des accus à vérifier. DC-DC USB-C PD 5 A à spécifier |
| Van — réseau | 🔴 | **RUT240 en stock**, mais aucune liaison Ethernet sur le RPi et aucun réseau van configuré. Le RPi utilise `192.168.129.16` sur le Wi-Fi maison |
| Van — boîtier | 🟡 | X1201-C1 monté ; silentblocs et coating restants ; compatibilité avec le X1200 non présumée |
| Van — capteurs | 🟡 | WiCAN Pro documenté comme physiquement installé ; **AirGuard Lupo SNZB-02UL** appairé. Dernière trame réelle retrouvée à 13:01 : 20,9 °C, 51,8 %, batterie 100 %, LQI 56/255 ; mesure fraîche à revalider. Lot P1 de **10 articles, ~121 € estimés**, température frigo incluse |
| Van — CAN/OBD | 🔴 | Aucun appareil WiCAN ni entité CAN dans le registre HA consulté ; aucune remontée réelle validée. Les 17+ entités et la compatibilité Exosfer restent des cibles à tester |
| Esneux — pilote HA | 🟡 | HA accessible via Tailscale ; deux appareils **AirGuard Lupo/Serre** enregistrés. Signal Lupo précédemment satisfaisant à 12 m à travers murs |
| Esneux — Zigbee | 🟢 | ZBDongle-E déplacé du port noyau `1-2` vers `3-2`, puis une relance Z2M contrôlée. Test initial de 10 min puis contrôle à 23:50, près de 3 h après le changement : service actif, USB présent, MQTT connecté, aucune nouvelle coupure ni sous-tension. AirGuard Serre à 23:46 : **22,5 °C, 55,7 %, batterie 95 %, LQI 255/255**. Second dongle toujours commandé, réception non confirmée |
| Serre / maison | ⚪ | Développement fonctionnel et automatisations gelés ; AirGuard Serre = SNZB-02DR2 |
| Supervision AirGuard | 🟢 | `http://lupo:8123/airguard-supervision/0` : mesures, batteries, tension et historiques 24 h vérifiés. Lupo 100 %, Serre 95 % et 2700 mV. Pas d'entité LQI/linkquality/last_seen exposée, donc aucune alerte de péremption arbitraire |
| MCP HA Lupo | 🟡 | Relais local persistant M5 `[::1]:8123` → `192.168.129.16:8123`, aucune exposition Internet. Kimi et DeepSeek testés par appels réels read-only ; Claude configuré mais authentification Anthropic expirée ; Codex OAuth HA réussi mais modèles refusés par le compte. ChatGPT Web et MCP M5 non validés |
| Time Machine | 🟡 | v2.4.1 actif par Ingress, démarrage au boot, aucun port externe. Cron **03:17**, Europe/Brussels, rétention 30 et Smart Backup. Première copie `/media/timemachine/2026/11/2026-11-06-120648` : **10 fichiers, 52 KiB**, diff Lovelace sans changement. Restauration non testée, copie encore sur le même RPi |
| HA M5 | 🔴 | HA et Mosquitto Docker actifs. Zigbee2MQTT redémarre en boucle : le pont série cherche `/dev/tty.usbserial-1110`, absent du Mac |

## Décisions clés

| Date | Décision | Contexte |
|------|----------|----------|
| 2026-11-10 | Cozmo : cerveau local (Ollama M1 gemma3:27b vision) plutôt que cloud GPT | Cohérent avec le zéro cloud ; M5 = hôte SDK, RUT240 = SSID 2,4 GHz dédié si besoin |
| 2026-11-06 | Exposer uniquement le MCP natif HA en lecture seule | Outils domotiques d'action filtrés ; boucle locale M5 et dernier kilomètre LAN, aucune exposition publique. Incendie, CO et sécurité restent locaux et déterministes |
| 2026-11-06 | Retenir Time Machine pour les instantanés de configuration, sans le confondre avec une sauvegarde complète | Copie et diff Lovelace validés ; aucune restauration sans confirmation spécifique, prochaine exécution automatique à vérifier et copie externe à prévoir |
| 2026-11-05 | Ne plus compter séparément les rôles RPi bureau et RPi van | Un seul hôte HAOS `lupo` observé au bureau ; 8 Go mesurés. Écart avec la ligne d'achat 4 Go conservé comme anomalie, sans créer un second appareil |
| 2026-11-05 | Traiter l'instabilité USB avant une nouvelle relance Z2M | Le premier redémarrage contrôlé avait restauré le réseau ~2 min avant une nouvelle déconnexion USB. Aucune sous-tension RPi signalée et aucune suspension USB |
| 2026-11-05 | Conserver le dongle sur le nouveau port USB `3-2` | Après changement de port et une seule relance : test de 10 min puis près de 3 h sans nouvelle coupure, mesures fraîches Serre jusqu'à 23:46. Pas de flash ni de mise à jour ; tester rallonge puis alimentation seulement en cas de récidive |
| 2026-11-05 | Ne pas déclarer AirGuard Lupo en panne sans nouvelle mesure | Les publications de 20:41 et 20:51 sont des valeurs retenues avec `linkquality:null` ; dernière trame réelle à 13:01. Réveil et contrôle à distance reportés au 06/11 |
| 2026-11-05 | Distinguer pilote Esneux actif et développement serre/maison gelé | Deux AirGuard enregistrés ; service Zigbee rétabli et mesure Serre validée, sans rouvrir le développement fonctionnel |
| 2026-11-05 | Auto-update sélectif : Supervisor + quatre modules ; HAOS/Core manuels | Sauvegarde complète `c38337a2`, prudence après l'ancien bug HAOS/NVMe |
| 2026-11-05 | Second ZBDongle-E maison/serre commandé | Livraison annoncée le 06/11 ; ne pas marquer reçu avant confirmation |
| 2026-07-11 | SD boot retenu pour Lupo | NVMe boot intermittent sur l'ancienne chaîne d'alimentation |
| 2026-07-11 | Hostname `lupo` + `ha supervisor repair` | Résolution du duplicate_os_installation avec le Docker M5 |
| 2026-07-09 | WiCAN Pro retenu | Cible OBD/CAN Ford Transit, HS-CAN + MS-CAN, 17+ entités à valider |
| 2026-06-13 | Architecture distribuée | Instances autonomes, supervision Tailscale |

## TTD — Pending

- [ ] **P2 · continu · (Dobby)** Surveiller que `binary_sensor.raspberry_pi_power_status` reste `off` ; ré-intervenir sur l'alimentation/câble si récidive.
- [ ] **P0 · — · (JC)** RPi Home : diagnostic physique (alimentation/LED, microSD flash `rpi5-64`, Ethernet) puis probable re-flash HAOS — non joignable au 10/11.
- [ ] **P1 · après 03:17 · (Dobby)** Vérifier l'exécution automatique Time Machine et la rétention ; tester une restauration uniquement avec confirmation explicite de JC et prévoir une copie hors du RPi.
- [ ] **P2 · — · (JC + Dobby)** Reconnecter Claude ; résoudre séparément les modèles Codex refusés par le compte. Ne pas exposer HA publiquement pour ChatGPT Web.
- [ ] **P1 · si doute sur un capteur · (JC + Dobby)** Contrôler une mesure fraîche ; aucune entité LQI/linkquality/last_seen n'est exposée, donc ne pas conclure à une panne sur les seules valeurs retenues.
- [ ] **P1 · si nouvelle coupure USB · (JC + Dobby)** Tester une courte rallonge USB2 saine, puis l'alimentation officielle directe du RPi, une variable à la fois. Ne pas mettre à jour le firmware pour masquer une coupure USB.
- [ ] **P0 · M5 · (JC + Dobby)** Décider si le second dongle doit équiper le M5 ; ensuite corriger le pont série ou arrêter le service Zigbee2MQTT inutilisé. Ne pas laisser la boucle de redémarrage sans traitement.
- [ ] **P0 · avant achat · (Dobby + Forge)** Identifier physiquement le X1205 et ses accus, vérifier boîtier X1201-C1/X1200 et sélectionner le DC-DC USB-C PD 5 A ; obtenir les prix réels.
- [ ] **P0 · 15/12 · (JC + Dobby)** Revalider les 10 articles P1 (~121 € historiques), les silentblocs et le coating ; aucun total final tant que les prix manquent.
- [ ] **P0 · accès local van · (Dobby + Forge)** Brancher/configurer le RUT240, établir le réseau van puis valider WiCAN → MQTT → HA, les entités réelles et Exosfer. Aucun flash requis pour ce premier diagnostic.
- [ ] **P0 · avant flash · (Dobby + Forge)** Corriger le GPIO8 du DS300 Tap et valider la chaîne d'alimentation.
- [ ] **P0 · 15/12 · (Dobby + JC)** Installer et tester l'ensemble dans Lupo.
- [ ] **À réception · (JC + Dobby)** Confirmer le second ZBDongle-E puis documenter son installation ; ne pas rouvrir pour autant le gel serre/maison.
- [ ] **P2 · quand JC voudra · (JC + Dobby)** Installer le Cozmo d'Anki en compagnon IA : réutiliser les leçons du Karotz (compatibilité WiFi, flash, interface web) → `cozmo-reborn/README.md` (fichier de travail) + `karotz-reborn/resurrection-karotz-2026-11-09.md`.

## TTD — Done

- [x] 2026-11-06 · MCP natif HA Lupo activé en lecture seule ; relais `launchd` vérifié actif sur `[::1]:8123` ; appels capteurs réels réussis dans Kimi et DeepSeek. Aucun outil d'action domotique ni exposition Internet.
- [x] 2026-11-06 · Tableau AirGuard validé : mesures, batteries, tension et historiques 24 h. Aucun seuil de fraîcheur ou LQI inventé ; sécurité non déléguée au LLM.
- [x] 2026-11-06 · Time Machine v2.4.1 configuré : planification enregistrée et journal relu, premier instantané de 10 fichiers/52 KiB, lecture et diff Lovelace AirGuard/map/dashboards vérifiés. Aucune restauration effectuée.
- [x] 2026-11-05 · Inventaire réel du RPi `lupo` : RPi 5 8 Go, SD 256 Go, HAOS sain, un dongle USB, Wi-Fi maison et Ethernet désactivé.
- [x] 2026-11-05 · Diagnostic des deux Zigbee2MQTT : arrêt après événement USB sur RPi ; pont série sans dongle sur M5.
- [x] 2026-11-05 · Retest RPi avec redémarrage Z2M autorisé : dongle et réseau reconnus, MQTT online, deux AirGuard joints ; nouvelle coupure USB après ~2 min, aucune mesure fraîche validée. `throttled=0x0` et port USB forcé actif.
- [x] 2026-11-05 · Dongle déplacé de `1-2` vers `3-2`, puis une relance Z2M : 10 min de stabilité USB/Zigbee/MQTT et aucune nouvelle coupure. AirGuard Serre réveillé à 21:04 : mesures fraîches 20,4 °C, 62,2–63,2 %, batterie 95 %, LQI 236–255/255.
- [x] 2026-11-05 · Contrôle final à 23:50 : Z2M actif, dongle présent, MQTT connecté, aucune sous-tension ni déconnexion USB depuis le changement de port. AirGuard Serre à 23:46 : 22,5 °C, 55,7 %, batterie 95 %, LQI 255/255. Dernière trame réelle Lupo retrouvée à 13:01 ; publications ultérieures retenues, sans preuve de mesure fraîche.
- [x] 2026-11-05 · Diagnostic WiCAN/RUT240 : aucun appareil/entité WiCAN enregistré, aucune liaison RUT240 Ethernet ; tests véhicule restant nécessairement locaux.
- [x] 2026-11-05 · Vérification constructeur X1200 : 5,1 V/5 A, deux 18650, jauge I²C ; prix et compatibilité du boîtier non validés.
- [x] 2026-11-05 · Pilote HA Esneux : deux AirGuard appairés, zones Serre/Lupo et test de signal documentés.
- [x] 2026-11-05 · Auto-update sélectif activé après sauvegarde ; aucune mise à jour HAOS/Core forcée.
- [x] 2026-10-22 · Échéance van unifiée au 15/12.
- [x] 2026-10-01 · Boot RPi résolu, NVMe retiré, HAOS 18.3.
- [x] 2026-11-09 · Karotz ressuscité : flash miniil Karotz OS + OpenKarotz, WiFi WPA/TKIP sur RUT240 dédié, interface web sur `http://192.168.129.250`.
- [x] 2026-11-10 · Fichier de travail Cozmo créé (`cozmo-reborn/README.md`) + leçons Karotz backportées dans `resurrection-karotz-2026-11-09.md`.
- [x] 2026-11-10 · Sous-tension Lupo contrôlée : capteur `off`, alerte Repairs acquittée après déplacement propre + re-rallumage ; RPi joignable (ping 9,5 ms).
- [x] 2026-11-10 · Surveillance box Proximus automatisée : `bin/pka-watch-box` + `scripts/box_monitor.py` + LaunchAgent (08:00/11:00, mail si anomalie). Relevé 15 min : 0 coupure, WAN 28 ms.
- [x] 2026-11-10 · RPi Home diagnostiqué : non joignable (mDNS, scan IP/MAC, Tailscale, ports 8123/22 fermés) — HAOS non booté.

## Historique sessions

| Date | Résumé | Livrable |
|------|--------|----------|
| 2026-11-10 | Cozmo compagnon IA : analyse + fichier de travail `cozmo-reborn/README.md` + backport Karotz | `cozmo-reborn/README.md`, `karotz-reborn/resurrection-karotz-2026-11-09.md` (backport), `INDEX.md`, `thread-iot.md`, `wiki/Daily/2026/11/2026-11-10-cozmo-compagnon-ia-corrections-wildnexus-caméra-et-graphe.md` |
| 2026-11-10 | Box Proximus automatisée + sous-tension Lupo résolue + RPi Home non joignable | `bin/pka-watch-box`, `scripts/box_monitor.py`, `bin/install-box-watch-launchd.sh`, `_local/launchd-plists/com.dobby.pka-watch-box.plist`, `karotz-reborn/rapport-box-proximus-15min-2151-2026-11-10.md`, `iot-van/99_REFERENCES/claude-ha-mcp_2026-11-10/`, `thread-iot.md` |
| 2026-11-09 | Résurrection du Karotz (miniil OS + OpenKarotz) : WiFi WPA/TKIP, correctif serveur web (inetd), installation OpenKarotz | `karotz-reborn/resurrection-karotz-2026-11-09.md`, `karotz-reborn/README.md`, `thread-iot.md`, `wiki/Daily/2026/11/2026-11-09-résurrection-du-karotz-miniil-os-openkarotz.md` |
| 2026-11-06 | MCP HA natif read-only, dashboard AirGuard et première copie Time Machine ; Kimi/DeepSeek testés, limites Claude/Codex/ChatGPT consignées ; sous-tension RPi à traiter | `scripts/ha_mcp_loopback_proxy.py`, `scripts/mcp_ha_lupo_readonly.sh`, `scripts/launchd/com.jchytech.pka-ha-mcp-lupo-loopback.plist`, `thread-iot.md`, `INDEX.md`, `executive-summary.md`, `wiki/Daily/2026/11/2026-11-06-mcp-home-assistant-et-lightroom-testes.md` |
| 2026-11-05 | Changement de port USB du dongle : près de 3 h sans nouvelle coupure, mesures Serre validées à 23:46 ; Lupo toujours sans trame réelle depuis 13:01, réveil reporté au 06/11 | `thread-iot.md`, `INDEX.md`, `executive-summary.md`, `_shared/hub-esneux.md`, `hardware-state.md`, `wiki/Daily/2026/11/2026-11-05-stabilisation-zigbee-rpi-et-revue-multiprojet.md` |
| 2026-11-05 | Retest Zigbee RPi avec redémarrage contrôlé : reprise temporaire puis nouvelle déconnexion USB ; aucune mesure fraîche avant la coupure | `thread-iot.md`, `INDEX.md`, `hardware-state.md` |
| 2026-11-05 | Inventaire réel, consolidation P1, diagnostic Zigbee/M5 et WiCAN/RUT240 ; aucune reconfiguration distante | `thread-iot.md`, `hardware-state.md`, `iot-van/OPERATIONS-CAN-OBD.md`, `_shared/procurement-register.md` |
| 2026-11-05 | Bilan HA van/Esneux, appairage AirGuard, commande du second dongle, clarification des cibles et achats | `thread-iot.md`, `INDEX.md`, `hardware-state.md` |
| 2026-11-05 | Auto-update sélectif après sauvegarde ; Healthy + Supported, LAN/Tailscale/MQTT validés | `thread-iot.md` |
| 2026-10-01 | RPi réparé, HAOS 18.3, Zigbee2MQTT opérationnel ; liste capteurs créée ; WiCAN physiquement installé | `iot-van/LISTE-CAPTEURS-ZIGBEE-2026-10-01.md` |
| 2026-07-11 | RPi Lupo stabilisé sur SD, hostname `lupo`, double instance HA résolu | `MEMORY.md` |
| 2026-07-09 | Diagnostic boot NVMe et WiCAN Pro retenu | documentation van |
| 2026-07-08 | Assemblage initial RPi van ; échec du boot NVMe | — |
| 2026-06-30 | Réception du matériel RPi initial et commande du van | — |

## Topics

- [Zigbee](topic-zigbee.md) — 🟡 coordinateurs Lupo (canal 11) + M5 (canal 15) opérationnels ; AirGuard ré-appairés ; valve + LuxSerre à ré-appairer.

## Liens

- Index : `INDEX.md`
- Liste P1 : `iot-van/LISTE-CAPTEURS-ZIGBEE-2026-10-01.md`
- Hardware PKA : `../../04_PILOTAGE_STRATEGIQUE/hardware-state.md`
- Boot NVMe : `iot-van/SOLUTION-BOOT-NVME-2026-07-09.md`
- Assemblage : `iot-van/ASSEMBLAGE-RPi5-VANLIFE.md`
- Diagnostic CAN : `iot-van/OPERATIONS-CAN-OBD.md`
- Spécification CAN : `iot-van/specs/SPEC-CAN-BUS.md`
- Procurement : `_shared/procurement-register.md`
- Appairage Zigbee : `iot-van/PROCEDURE-APPAIRAGE-ZIGBEE-2026-10-05.md`
- Hub Esneux, architecture cible : `_shared/hub-esneux.md`

---

*Fichier maintenu par Dobby 🦉 ; les états confirmés priment sur les anciennes BOM et architectures cibles.*