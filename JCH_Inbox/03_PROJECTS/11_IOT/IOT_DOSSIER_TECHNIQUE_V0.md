# IOT — Dossier technique V0 (« bible »)
## Référentiel consolidé — point zéro

**Version :** V0.3 · **Consolidation initiale :** 2026-10-29 · **Recadrage :** 2026-11-05 · **Rédaction :** Dobby 🦉

**Statut :** référentiel technique ; les architectures cibles ne sont pas des états installés.

**Nature :** infrastructure **personnelle** (pas de commercialisation).

**Source de vérité opérationnelle :** `thread-iot.md` + faits matériels confirmés ; ils priment sur les BOM et documents anciens.

**Périmètre cible :** Esneux (maison/serre), van Lupo, Italie et hub M5 Docker.

> ⚠️ **Règle d'or** : en cas de conflit, les observations datées du `thread-iot.md` font foi. Les divergences historiques sont listées §11 ; les montants non vérifiés ne sont pas des restes à payer.

---

## 0. Fiche signalétique

| Élément | Valeur |
|---|---|
| **Projet** | IOT / Domotique JCH (ombrelle) |
| **Sous-projets** | `iot-van` (Lupo), `iot-serre` (Esneux), `iot-maison` (Esneux) + `_shared` |
| **Stack** | Home Assistant OS · RPi 5 · Zigbee2MQTT · MQTT/Mosquitto · Tailscale · Victron · ESPHome · CAN/OBD WiCAN Pro |
| **Priorité P0** | **Van Lupo** — échéance **15/12/2026** (arbitrage JC 19/10) |
| **Budget van** | ~1 026 € dans une BOM historique, **non consolidé** |
| **Budget hub Esneux** | ~298 € historique pour une cible RPi 5 8 Go + NVMe, **non consolidé** |
| **Principe** | Autonomie par site, supervision unifiée iPhone via Tailscale, objectif **zéro cloud, zéro abonnement** |

---

## 1. Architecture globale — cible et réalité

```text
[Mac M5 Docker]          [RPi HAOS `lupo`, actuellement bureau Esneux]       [Italie]
HA + Mosquitto actifs    Cible van + pilote provisoire maison/serre           Site planifié
Zigbee M5 en panne       RPi 5 8 Go, HAOS sain, Zigbee arrêté                 Non démarré
          │                              │
          └────────────── Tailscale ─────┴────────── Supervision iPhone

[Hub fixe Esneux et hub van séparés] = cible d'affectation, pas deux RPi observés.
```

- **Un seul RPi HAOS est observé** : hostname `lupo`, **Raspberry Pi 5 Model B Rev 1.0, 8 Go**, SD/mmcblk0 de 238,4 Gio (carte commercialisée 256 Go). Il se trouve au bureau lors du diagnostic et ne peut donc pas couvrir simultanément un hub fixe et le van.
- **M5 Docker** : Home Assistant et Mosquitto actifs. Zigbee2MQTT redémarre en boucle car son pont série cherche un dongle USB local absent ; le M5 n'est pas un hub Zigbee opérationnel.
- **RPi `lupo`** : HAOS 18.3, Core 2026.9.4, Supervisor 2026.09.3 ; Supervisor `healthy` et `supported`. Wi-Fi maison `192.168.129.16/23`, Ethernet désactivé/sans liaison. Un seul ZBDongle-E est détecté ; Zigbee2MQTT est arrêté après une déconnexion/reconnexion USB.
- **Affectation à arbitrer à réception du second dongle** : le M5 peut devenir le hub fixe maison/serre afin de libérer le RPi pour le van. Ce choix n'est ni appliqué ni définitivement acté.
- **Écart d'inventaire :** achat historique documenté d'un RPi 5 **4 Go**, mesure réelle **8 Go**. Vérifier facture/boîte ; ne pas créer un second RPi fictif.
- **Italie** : site planifié, non démarré.

---

## 2. Stack transverse

- **OS** : Home Assistant OS sur RPi + Home Assistant Docker sur M5.
- **Zigbee** : Sonoff ZBDongle-E, Zigbee2MQTT ; **un coordinateur par réseau**, densification par routeurs alimentés.
- **État Zigbee au 05/11** : service RPi en erreur après événement USB ; service M5 en boucle avec `HOST_FATAL_ERROR`, faute de dongle local. Aucun des deux n'est déclaré fonctionnel.
- **MQTT** : Mosquitto local sur les deux hôtes.
- **VPN** : Tailscale pour accès distant iPhone et administration.
- **Énergie/solaire** : Victron en P3 ; cible d'intégration Victron GX via MQTT à valider selon le matériel réel.
- **Capteurs** : Sonoff, Aqara, Ecowitt et ESPHome selon les sous-projets.
- **Véhicule** : WiCAN Pro → RUT240 → MQTT → HA ; 17+ entités sont une **cible**, aucune entité CAN n'est enregistrée au 05/11.

---

## 3. iot-van — Lupo (P0, échéance 15/12/2026)

### 3.1 État matériel et logiciel

- **RPi `lupo`** : RPi 5 **8 Go mesurés**, SD 256 Go, HAOS **18.3**, Core **2026.9.4**, Supervisor **2026.09.3**, actuellement au bureau. Healthy + Supported ; aucune alerte Resolution.
- **Mises à jour** : auto-update sélectif configuré pour Supervisor et quatre modules ; HAOS/Core manuels. HAOS **18.4**, Core **2026.11.0**, Supervisor **2026.10.5** et des modules sont proposés, mais aucune mise à jour n'est forcée dans cette passe.
- **NVMe** : Fanxiang 256 Go retiré physiquement ; décision **SD seule**. L'ancienne explication imputant l'échec à une limite intrinsèque du X1205 sous 5 A n'est pas retenue : la cause exacte de la sous-tension historique reste à revérifier.
- **Alimentation** : remplacement **X1205 → X1200 envisagé, non commandé**. Le [wiki constructeur X1200](https://wiki.geekworm.com/X1200) confirme une sortie **5,1 V ±5 %, max 5 A**, deux accus **18650**, une jauge I²C et l'alimentation par contacts pogo.
- **Compatibilités ouvertes** : le wiki associe le X1200 au boîtier **X1200-C1**, tandis que le stock contient un **X1201-C1**. Le X1205 est décrit avec des accus **21700**, alors que le stock documente des 18650 : identifier physiquement carte et accus avant montage ou achat. Le prix courant du X1200 n'a pas été obtenu ; ~50–70 € reste une estimation historique.
- **Boîtier** : X1201-C1 documenté comme monté ; silentblocs et coating restants. Le DC-DC USB-C PD 5 A exigé par ADR-001 reste à spécifier.
- **Réseau** : **RUT240 en stock**, mais aucune liaison Ethernet ou configuration du réseau van. Le ZTE MF833U1 reste en stock mais n'est pas la cible réseau retenue.
- **Capteurs** : WiCAN Pro documenté comme physiquement installé ; **AirGuard Lupo SNZB-02UL appairé**. AirGuard Serre est un **SNZB-02DR2** distinct. La liste P1 contient **10 articles, capteurs + éclairage, ~121 € estimés au 01/10**, température frigo incluse, prix à revalider.

### 3.2 CAN/OBD — diagnostic et cible

Le WiCAN Pro est documenté comme physiquement installé, mais **aucun appareil WiCAN ni entité CAN** n'existe dans le registre HA consulté. L'intégration RUT240/MQTT, la compatibilité Exosfer, les PIDs réels et la consommation ne sont pas validés.

La cible historique est 17+ entités : vitesse, RPM, carburant, consommation, température moteur/extérieure, pression turbo, DTC, portes, pneus et batterie. Veille `<1 mA`, réveil toutes les 5 minutes et cutoff sont des paramètres à mesurer, non des acquis.

- Procédure : [`iot-van/OPERATIONS-CAN-OBD.md`](iot-van/OPERATIONS-CAN-OBD.md)
- Spécification : [`iot-van/specs/SPEC-CAN-BUS.md`](iot-van/specs/SPEC-CAN-BUS.md)
- Prochaine étape : intervention locale dans le van pour alimenter/connecter le RUT240 puis valider WiCAN → MQTT → HA. **Aucun achat ou flash initial.**

### 3.3 DS300 Tap (interface CBE DS300)

ESP32-C3 + ADS1115 → lecture tensions batteries, niveaux cuves et états relais **sans modifier le câblage**. Spec + `esphome-ds300.yaml`, ~15 € historique. **GPIO8 utilisé deux fois** : correction obligatoire avant flash.

### 3.4 Autres modules

- **Assiette van** : inclinomètre délégué à l'iPhone (MPU6050 supprimé 23/07) — specs `assiette-van-*`.
- **CarPlay** : `iot-van/carplay/`.
- **Dashboard** : `iot-van/dashboard/ui-lovelace.yaml`, à réconcilier avec les entités réelles avant usage.
- **Enclosure** : boîtier météo `iot-van/enclosure/lupo-meteo-enclosure.scad`.

### 3.5 P0 restant

- [ ] Réveiller AirGuard Lupo le 06/11 et contrôler une mesure fraîche ainsi que son LQI ; sa dernière trame réelle date du 05/11 à 13:01. Le dongle et AirGuard Serre ont été validés après changement de port USB.
- [ ] À réception du second dongle, confirmer l'affectation maison/serre ; option recommandée : M5 fixe, RPi libéré pour le van. Corriger le pont série M5 ou arrêter son service Zigbee2MQTT inutilisé.
- [ ] Revalider les [10 articles P1](iot-van/LISTE-CAPTEURS-ZIGBEE-2026-10-01.md), ~121 € historiques ; obtenir les prix réels X1200, DC-DC, silentblocs et coating avant tout total.
- [ ] Identifier physiquement le X1205 et ses accus ; vérifier boîtier X1201-C1/X1200 et spécifier le DC-DC USB-C PD 5 A.
- [ ] Connecter localement **RUT240 + WiCAN Pro**, valider MQTT, entités réelles, Exosfer et consommation.
- [ ] Corriger le conflit GPIO8 du DS300 Tap avant flash, puis installer et tester l'ensemble dans Lupo.

---

## 4. iot-serre — Esneux (pilote HA, développement gelé)

- **État réel** : le RPi `lupo` au bureau sert provisoirement le pilote HA. Deux appareils AirGuard sont enregistrés : **SNZB-02DR2 = Serre**, **SNZB-02UL = Lupo**. Le signal Lupo a été jugé satisfaisant à 12 m à travers murs lors du test précédent.
- **État Zigbee validé** : après déplacement du dongle du port noyau `1-2` vers `3-2` et une relance contrôlée, Z2M/MQTT sont restés actifs sans nouvelle coupure USB ni sous-tension jusqu'au contrôle de 23:50, près de 3 h après le changement. AirGuard Serre a publié à 23:46 : 22,5 °C, 55,7 %, batterie 95 %, LQI 255/255. AirGuard Lupo reste sans trame réelle depuis 13:01 ; les valeurs retenues ne prouvent pas une mesure fraîche.
- **Second coordinateur** : ZBDongle-E commandé le 05/11, livraison annoncée le 06/11 ; réception et installation non confirmées.
- **Inventaire** : RPi 5 **8 Go mesurés**, pas un modèle restant à inventorier. Écart avec l'ancien achat 4 Go conservé comme anomalie ; aucun second RPi ajouté.
- **Statut fonctionnel** : ⚪ développement serre gelé malgré le pilote HA. La BOM historique ~247 € reste une cible non consolidée.
- **Cible historique du hub** : RPi 5 8 Go + X1201 + X1001 + SSD 128 Go + boîtier, ~298 €. Cette architecture n'est pas confirmée sur le pilote actuel ; voir `_shared/hub-esneux.md`.

## 5. iot-maison — Esneux (pilote partagé, développement gelé)

Même RPi provisoire que la serre. Les capteurs de pièces, l'énergie, la sécurité et les automatisations restent une ébauche gelée ; les deux AirGuard enregistrés ne valent pas déploiement maison complet.

## 6. _shared — ressources partagées

`hub-esneux.md`, `convergence-van-serre-capteurs.md`, `procurement-register.md`, `panier-amazon-van-serre.html`, `ARCHITECTURE-MQTT-DISCOVERY.md`, `detecteur-niveau-liquide/`. Le fichier hors sujet `2026-06-20_Lukeditria_instagram.md` est dans `HISTORIQUE/`.

---

## 7. BOM et coûts — historique, pas devis courant

| Bloc | Montant |
|---|---|
| Van — total BOM historique | ~1 026 €, non consolidé |
| Van — anciens restes à commander | ~584 € / ~370 € / ~150 € selon périmètres : **aucun total courant retenu** |
| Van — liste P1 du 01/10 | **10 articles, ~121 € estimés**, température frigo et éclairage inclus |
| Mopeka Pro Check | P3, ~45 € historiques, hors P1 |
| X1200 | ~50–70 € historiques ; prix courant non obtenu |
| Hub Esneux — cible historique | ~298 €, non consolidée, à réconcilier avec le RPi existant |

> **Aucun « reste réel » n'est affirmé.** Les prix sont anciens ou manquants, le stock doit être exclu, et X1200/DC-DC/silentblocs/coating ne sont pas tous chiffrés. Voir `_shared/procurement-register.md`. Aucun achat n'a été effectué dans cette passe.

---

## 8. ADR — décisions à maintenir ou amender

ADR-001 alimentation F3/convertisseur · ADR-002 Zigbee vs Z-Wave vs BLE · ADR-003 SSD NVMe boot · ADR-004 présence extérieure PIR · ADR-005 plateforme RPi5 vs x86 · ADR-006 OBD/CAN WiCAN Pro, dans `iot-van/adr/`.

> ADR-003 (NVMe boot) est **contredit par le réel** : NVMe retiré, SD seule. À amender sans réécrire rétroactivement le diagnostic historique.

---

## 9. Risques et points de vigilance

| Risque | Constat | Action |
|---|---|---|
| **Zigbee RPi interrompu** | Événement USB puis arrêt Z2M ; cause physique inconnue | Vérifier contact/alimentation puis redémarrage contrôlé avec accord |
| **Zigbee M5 en boucle** | `/dev/tty.usbserial-1110` absent ; aucun dongle local | Choisir l'affectation du second dongle puis corriger ou arrêter le service |
| **WiCAN/RUT240 non intégrés** | Aucun appareil CAN ; Ethernet sans liaison | Intervention locale et validation couche par couche |
| **Alimentation van** | Sous-tension historique, cause exacte à revérifier | Identifier UPS/accus ; tester 12 V → DC-DC PD → X1200 en charge |
| **Compatibilités X1200** | Boîtier X1201-C1, accus documentés différemment du X1205 | Vérifier constructeur et montage avant achat |
| **NVMe abandonné** | SD plus exposée aux coupures | SD Endurance + UPS validé + sauvegardes |
| **DS300 Tap** | GPIO8 utilisé deux fois | Corriger avant tout flash |
| **Échéance 15/12** | Dépend d'achats et de validations physiques | Traiter d'abord Zigbee, alimentation et chaîne CAN |
| **Documentation** | Anciennes BOM/ADR divergent du réel | Maintenir `thread-iot.md` puis resynchroniser BOM/ADR |
| **Italie non planifiée** | Site sans périmètre défini | Arbitrer priorité avant BOM |

---

## 10. Roadmap par site

| Site | Phase | Prochaine étape |
|---|---|---|
| **Van Lupo** | 🔴 P0 | Réparer Zigbee, identifier l'alimentation, connecter localement RUT240/WiCAN, corriger DS300 |
| **Serre Esneux** | ⚪ gelé, pilote HA | Maintenir le pilote ; ne pas rouvrir les automatisations sans arbitrage |
| **Maison Esneux** | ⚪ gelé, pilote partagé | Confirmer le hub fixe à réception du second dongle |
| **Italie** | ⚪ planifié | Décider périmètre et matériel |
| **M5 Docker** | 🟡 partiel | HA/Mosquitto actifs ; traiter la boucle Zigbee2MQTT |

---

## 11. Divergences résolues

| Sujet | Ancien document | Réalité au 2026-11-05 | Décision |
|---|---|---|---|
| Nombre de RPi | Bureau + van présentés comme deux hôtes | Un seul `lupo`, actuellement bureau | **Un hôte ; deux rôles non simultanés** |
| RAM | Achat RPi 5 4 Go ; modèle/RAM à inventorier | **8 Go mesurés** | **Écart facture/boîte à vérifier** |
| Stockage van | SSD NVMe 256 Go | NVMe retiré, SD 256 Go | **SD seule** |
| Alimentation | X1205 présenté comme limité sous 5 A | Wiki à revérifier, cause historique non établie ; X1200 confirmé 5 A max | **Diagnostic avant remplacement** |
| Boîtier/accus | X1201-C1 + 18650 supposés compatibles | X1200 associé à X1200-C1 ; X1205 décrit en 21700 | **Identification physique obligatoire** |
| Zigbee | M5/RPi décrits comme opérationnels | RPi arrêté après événement USB ; M5 sans dongle | **Deux pannes distinctes à traiter** |
| WiCAN / CAN | 17+ entités présentées comme remontées | Aucun appareil/entité CAN enregistré | **Cible à tester localement** |
| Capteurs P1 | 7/8 capteurs, 118–133 €, température « couverte » | 10 articles incluant SNZB-02P frigo + éclairage, ~121 € au 01/10 | **Prix historiques à revalider** |
| Hub Esneux | RPi 5 8 Go + NVMe présenté comme installé | RPi 8 Go sur SD, cible NVMe non confirmée | **Ne pas commander la cible historique** |
| Serre/maison | Actifs ou entièrement absents selon documents | Deux AirGuard enregistrés, service Zigbee interrompu | **Pilote HA, développement gelé** |

---

## 12. Veille techno et recommandations conditionnelles

- **Victron → HA** : privilégier une intégration Victron GX/MQTT si un device GX compatible est retenu ; ne pas la présenter comme installée.
- **Radio** : un coordinateur par réseau et de vrais routeurs Zigbee alimentés ; ne pas activer Matter/Thread dans cette passe.
- **ESPHome** : appliquer les bonnes pratiques de consommation et de stabilité après correction des GPIO ; aucun flash avant recette.
- **Énergie RPi 5** : intégrer la consommation réelle dans le bilan van, plutôt qu'une estimation générique.
- **Hub fixe** : à réception du second dongle, étudier d'abord le M5 déjà équipé de HA/Mosquitto avant d'acheter un autre RPi. Home Assistant Green reste une alternative, pas une décision.

---

## 13. Resynchronisation au 2026-11-05

1. **Fait** : INDEX, executive summary, thread, hub Esneux, procurement et hardware-state distinguent état réel, cibles et historique.
2. **Fait** : `OPERATIONS-CAN-OBD.md` et `SPEC-CAN-BUS.md` partent maintenant du réseau/MQTT, sans commander ou flasher systématiquement.
3. **Reste documentaire** : resynchroniser `BOM-VANLIFE.md` et amender ADR-003 pour la SD ; vérifier les anciens dashboards/scénarios avant usage.
4. **Reste matériel** : réparer Zigbee RPi/M5, confirmer le second dongle, identifier UPS/accus/boîtier et tester WiCAN/RUT240 localement.
5. **Reste achats** : revalider prix et compatibilités ; aucun total final ni achat automatique.

---

## 14. Gouvernance et sources de vérité

- **Opérationnel** : `thread-iot.md`.
- **Inventaire matériel PKA** : `../../04_PILOTAGE_STRATEGIQUE/hardware-state.md`.
- **BOM historique à resynchroniser** : `iot-van/BOM-VANLIFE.md`.
- **Décisions** : `iot-van/adr/`.
- **Procurement** : `_shared/procurement-register.md`.
- **Domaines de revue** : Zigbee/ESPHome, hardware/alimentation, documentation et architecture. Une mention de spécialiste dans l'historique ne vaut pas revue actuelle.

---

## 15. Sources principales

- Relevés HAOS, registre HA, journaux Zigbee2MQTT et configuration Docker du 2026-11-05, consignés dans `thread-iot.md`.
- [Wiki constructeur Geekworm X1200](https://wiki.geekworm.com/X1200) — 5,1 V ±5 %, max 5 A, deux 18650, jauge I²C et contacts pogo.
- [WiCAN Pro / firmware](https://github.com/meatpi-electronics/wican-fw) et procédure CAN révisée.
- Les anciennes notes de veille Home Assistant, Victron et ESPHome restent des références de conception, pas des preuves d'installation.

---

## 16. Revue historique V0.1 et statut actuel

> Cette section conserve les constats de la revue V0.1 ; elle ne représente pas une nouvelle délégation au 05/11. Les faits matériels et le statut ci-dessous priment.

### 16.1 Hardware et alimentation

- **Toujours ouvert** : DC-DC USB-C PD 5 A absent du BOM ; l'ancien HW-133 3 A non-PD ne répond pas à cette exigence.
- **Partiellement résolu** : les spécifications du X1200 sont maintenant confirmées sur le wiki constructeur, y compris la jauge I²C et les contacts pogo.
- **Toujours ouvert** : compatibilité du boîtier X1201-C1, identification X1205/accus, prix courant et test de la chaîne 12 V → 5 V en charge.
- **À reformuler** : l'ancien diagnostic « X1205 <5 A » n'est plus affirmé ; la cause de la sous-tension historique doit être revérifiée.

### 16.2 Radio, capteurs et ESPHome

- **Blocker toujours vérifié dans le fichier** : `iot-van/ds300-tap/esphome-ds300.yaml` utilise **GPIO8 deux fois** (I²C SDA + relais) ; corriger avant flash.
- Canal Zigbee 15 recouvrant Wi-Fi 6 : choisir un canal hors Wi-Fi 1/6/11 après relevé local ; le RUT240 ajoutera un AP 2,4 GHz.
- Le Sonoff S31 cité comme secours est Wi-Fi dans sa variante documentée ; ne pas le compter comme routeur Zigbee. Vérifier les routeurs réellement choisis.
- Aqara MCCGQ11LM n'est pas Zigbee 3.0 : tenir compte du risque de ré-appairage et standardiser les nouveaux capteurs autant que possible.

### 16.3 Documentation et budget

- Les anciens budgets 584 € / 370 € / ~150 € et comptes 7/8/10 articles ne sont plus mélangés.
- La liste P1 de **10 articles (~121 € au 01/10)** sert de base à revalider ; elle inclut bien le frigo et l'éclairage.
- Le registre d'achat consolide les besoins et prix manquants ; les BOM historiques restent à resynchroniser.

### 16.4 Ordre de traitement recommandé

1. **Maintenant** : réparer le Zigbee RPi après vérification physique du dongle.
2. **À réception** : affecter le second dongle au hub fixe, en privilégiant le M5 si les tests sont concluants.
3. **Avant achat/montage** : identifier X1205/accus/boîtier et spécifier X1200 + DC-DC PD 5 A.
4. **Dans le van** : établir RUT240 → WiCAN → MQTT → HA puis mesurer PIDs, Exosfer et veille.
5. **Avant flash DS300** : corriger GPIO8 et valider l'alimentation.

---

*Fin du dossier V0.3 — état réel recadré au 2026-11-05 ; aucune intégration distante ou validation physique n'est implicite.*
