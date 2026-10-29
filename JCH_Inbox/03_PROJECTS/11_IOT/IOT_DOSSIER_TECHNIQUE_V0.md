# IOT — Dossier technique V0 (« bible »)
## Référentiel consolidé — point zéro

**Version :** V0.1 · **Date :** 2026-10-29 · **Rédaction :** Dobby 🦉
**Statut :** DRAFT — revue experts internes (Forge / Araignée / Atlas) intégrée ensuite.
**Nature :** infrastructure **personnelle** (pas de commercialisation) — référentiel technique, pas business plan.
**Source de vérité opérationnelle :** `thread-iot.md` (dernière maj 2026-10-22) + `iot-van/` (docs 2026-10) primés sur les BOM plus anciens.
**Périmètre :** 3 sites (Esneux Belgique, Van Lupo, Italie) + hub M5 Docker (base).

> ⚠️ **Règle d'or** : ce document reconcile des sources d'âges différents. En cas de conflit, **le `thread-iot.md` (2026-10-22) fait foi** sur les BOM (2026-07). Les divergences résolues sont listées §11.

---

## 0. Fiche signalétique

| Élément | Valeur |
|---|---|
| **Projet** | IOT / Domotique JCH (ombrelle) |
| **Sous-projets** | `iot-van` (Lupo), `iot-serre` (Esneux), `iot-maison` (Esneux) + `_shared` |
| **Stack** | Home Assistant OS · RPi 5 · Zigbee (Z2M/ZHA) · MQTT (Mosquitto) · Tailscale · Victron · ESPHome · CAN/OBD (WiCAN Pro) |
| **Priorité P0** | **Van Lupo** — deadline **15/12/2026** (arbitrage JC 19/10) |
| **Budget van (BOM)** | ~1 026 € (dont ~446 € payé, ~584 € à commander) |
| **Budget hub Esneux** | ~298 € (RPi 5 8 Go + X1201 + X1001 + SSD 128 Go) |
| **Principe** | Autonome par site, supervision unifiée iPhone via Tailscale, **zéro cloud, zéro abonnement** |

---

## 1. Architecture globale (état 2026-10)

```
[HA Docker — Mac M5]        [RPi 5 HA OS — Esneux]       [RPi 5 HA OS — Van Lupo]      [Italie — RPi 5]
Belgique (base/dev)         Serre + Maison               Véhicule nomade               Résidence secondaire
     │                           │                             │                            (planifié)
     └───────────────────────────┴───────── Tailscale ─────────┴────────────────────────────┘
                                        Supervision unifiée iPhone
```

- **M5 Docker** : HA de base/dev, opérationnel (hostname `homeassistant`).
- **Esneux RPi 5 8 Go** : HA OS bare metal, UPS X1201, NVMe X1001, SSD 128 Go (serre + maison partagent ce hub).
- **Van RPi 5 4 Go** : HA OS, **SD 256 Go** (NVMe retiré), alim en cours (X1205 → X1200), RUT240 4G, WiCAN Pro OBD/CAN.
- **Italie** : RPi 5 prévu, non démarré.

---

## 2. Stack transverse

- **OS** : Home Assistant OS (bare metal RPi) + HA Docker (M5).
- **Zigbee** : Sonoff ZBDongle-E, Zigbee2MQTT (Z2M) **un seul coordinateur par réseau** (recommandation 2026 : choisir une voie, densifier par routeurs alimentés).
- **MQTT** : Mosquitto local.
- **VPN** : Tailscale (accès distant iPhone).
- **Énergie/solaire** : Victron (P3) — cible **intégration Victron GX native via MQTT** (voir §12).
- **Capteurs** : Aqara, Sonoff (SNZB-02D/02DR2/04), Ecowitt (météo), ESPHome (ESP32-C3/S3).
- **Véhicule** : CAN/OBD via **WiCAN Pro** (MeatPi ESP32-S3 + STN) → 17+ entités HA (HS-CAN moteur + MS-CAN carrosserie).

---

## 3. iot-van — Lupo (P0, deadline 15/12/2026)

### 3.1 État hardware (source : thread 2026-10-22)
- **RPi 5 4 Go** — boot résolu (01/10), **SD 256 Go Endurance**, **HAOS 18.3** (fix #5005), Supervisor+Core à jour, auto-update OFF, Healthy.
- **NVMe** : métal retiré physiquement → **décision SD seule** (l'échec venait des pogo pins X1205 <5 A).
- **Alimentation** : **remplacer X1205 → Geekworm X1200** (5.1 V/5 A, 2×18650, ~50-70 €). En attendant : alim USB-C directe (`throttled=0x0`). *Cause : undervoltage boot + throttling sous charge.*
- **Boîtier** : X1201-C1 monté ; reste silentblocs + coating.
- **Réseau** : **RUT240 Teltonika (4G) en stock** → passerelle internet (SIM 4G → Ethernet → RPi). Remplace ZTE MF833U1.
- **Capteurs** : WiCAN Pro **installé** ; SNZB-02DR2 **appairé** (cellule, 07/10) via Z2M ; **7 capteurs ~88 €** à commander.

### 3.2 CAN/OBD (WiCAN Pro)
17+ entités HA sans capteur physique : vitesse, RPM, carburant, conso, T° moteur, pression turbo, T° ext, DTC, état portes ×6, pression pneus ×6, batterie SOC/courant/tension. Mode stationnement : deep sleep <1 mA, wake 5 min. Spec : `iot-van/specs/SPEC-CAN-BUS.md`.

### 3.3 DS300 Tap (interface CBE DS300)
ESP32-C3 + ADS1115 → lecture tensions batteries, niveaux cuves, états relais **sans modifier le câblage**. Spec + `esphome-ds300.yaml`. ~15 €.

### 3.4 Autres modules
- **Assiette van** : inclinomètre délégué à l'iPhone (MPU6050 supprimé 23/07) — specs `assiette-van-*`.
- **CarPlay** : `carplay/CARPLAY*.md`.
- **Dashboard** : `dashboard/ui-lovelace.yaml`.
- **Enclosure** : boîtier météo `enclosure/lupo-meteo-enclosure.scad`.

### 3.5 P0 restant (TTD)
- [ ] Commander **7** capteurs Zigbee (~88 € ; thread 2026-10-22 — la LISTE du 01/10 en listait 10/121 €, écart à clarifier) + silentblocs + coating + UPS **X1200** (~50-70 €) + **DC-DC USB-C PD 5 A** (exigé par ADR-001, **absent du BOM**).
- [ ] Intégrer **WiCAN Pro + RUT240 (4G)** dans HA van.
- [ ] Installer l'ensemble dans Lupo.

---

## 4. iot-serre — Esneux (gelé post-van)

- **Statut** : ⚪ gelé jusqu'à fin van (post-septembre).
- **BOM serre ~247 €**, 5 phases. Capteurs : T°/HR (Aqara/Sonoff), électrovanne arrosage, détecteur niveau liquide (ADS1115 + ESP32-C3).
- **Hub Esneux** (partagé serre + maison) : RPi 5 8 Go + UPS X1201 (bottom, pogo) + NVMe HAT X1001 (top) + SSD 128 Go + boîtier X1201-C1, ~298 €. Protections : SSD (pas SD), UPS shutdown I2C, OverlayFS read-only, watchdog, backup auto → M1 via Tailscale.

## 5. iot-maison — Esneux (ébauche)
Ébauche long terme, même hub que serre. Capteurs pièces, énergie, sécurité. Peu documenté à ce jour.

## 6. _shared — ressources partagées
`hub-esneux.md`, `convergence-van-serre-capteurs.md` (achat groupé), `procurement-register.md`, `panier-amazon-van-serre.html`, `ARCHITECTURE-MQTT-DISCOVERY.md`, `detecteur-niveau-liquide/`. ⚠️ un fichier hors-sujet traîne (`2026-06-20_Lukeditria_instagram.md`) → à sortir.

---

## 7. BOM & coûts consolidés

| Bloc | Montant |
|---|---|
| Van — hub RPi 5 (reçu) | ~435 € |
| Van — reste (capteurs, X1200, silentblocs, coating...) | ~584 € |
| **Total van** | **~1 026 €** |
| Hub Esneux (RPi 5 8 Go + Geekworm) | ~298 € |

> ⚠️ **Budget à réconcilier (vérifié par Atlas)** — trois chiffres coexistent : dossier « ~584 € à commander » ; `BOM-VANLIFE.md:213` « reste P1 ~370 € » (+ P3 ~210 €) ; `thread-iot.md` ~150 € court terme (88 € capteurs + X1200). Le **reste réel court terme ≈ 150 €**. Le BOM (2026-07) est aussi périmé sur l'alim (X1205→X1200), le stockage (NVMe→SD) et le WiCAN (déjà installé). À resynchroniser (§13).

---

## 8. ADR (décisions actives) — `iot-van/adr/`
ADR-001 alimentation F3/convertisseur · ADR-002 Zigbee vs Z-Wave vs BLE · ADR-003 SSD NVMe boot · ADR-004 présence extérieure PIR · ADR-005 plateforme RPi5 vs x86 · ADR-006 OBD/CAN WiCAN Pro.
> Note : ADR-003 (NVMe boot) est **contredit par le réel** (NVMe retiré, SD seule) → à amender.

---

## 9. Risques & points de vigilance

| Risque | Détail | Mitigation |
|---|---|---|
| **Alim van (undervoltage)** | X1205 pogo <5 A → throttling/boot | X1200 5.1 V/5 A ; en attendant alim USB-C directe |
| **HAOS 18 régression RPi5** | Matter/OpenThread Border Router instables en 18.x | Ils sont en 18.3 : éviter Matter/Thread pour l'instant ; surveiller les patchs |
| **NVMe abandonné** | SD moins résistante aux coupures | SD Endurance + UPS propre + backups Tailscale |
| **Deadline 15/12** | dépend d'achats (88 € capteurs + X1200) | Commande groupée ASAP |
| **Docs drift** | BOM/INDEX/ADR obsolètes vs thread | Resynchroniser (cette bible + §13) |
| **Italie non planifiée** | site mentionné mais sans doc | Décider P? et documenter |
| **Coût budgété ~1 026 €** | dépassement possible | Suivre procurement-register |

> ⚠️ **Revue experts (§16)** — 3 points bloquants **vérifiés** : (1) `esphome-ds300.yaml` → **GPIO8 utilisé 2×** (I²C SDA + relais) ; (2) **DC-DC USB-C PD 5 A absent du BOM** ; (3) **X1200 non vérifié** (datasheet/jauge I²C). À traiter avant flash du van.

---

## 10. Roadmap par site

| Site | Phase | Prochaine étape |
|---|---|---|
| **Van Lupo** | 🔴 P0 | Acheter capteurs+X1200, intégrer WiCAN/RUT240, installer dans le van (≤ 15/12) |
| **Serre Esneux** | ⚪ gelé | Reprise post-van (BOM 247 € prêt) |
| **Maison Esneux** | ⚪ ébauche | Après serre, mêmes hub/capteurs |
| **Italie** | ⚪ planifié | Décider périmètre + BOM RPi 5 |
| **M5 Docker** | 🟢 base | Sert de dev/backup HA |

---

## 11. Divergences résolues (adéquation aux changements)

| Sujet | Doc ancien | Réalité (thread 2026-10) | Décision |
|---|---|---|---|
| Stockage van | BOM : SSD NVMe 256 Go | NVMe retiré, SD 256 Go | **SD seule** |
| Alim van | BOM : X1205 reçu | Under-voltage | **X1200** (achat différé) |
| Sites | exec : 3 sites (Esneux/Italie/Van) ; INDEX : 3 sous-projets (van/serre/maison) | M5 base + Esneux + Van + Italie | **4 nœuds** (M5, Esneux, Van, Italie) |
| HAOS | thread 07-09 : 17.3 | 18.3 | **18.3** |

---

## 12. Veille techno 2026 & améliorations recommandées

- **Victron → HA** : utiliser l'**intégration native « Victron GX » via MQTT** (auto-discovery, Venus OS ≥3.5, sans YAML) plutôt qu'un parsing VE.Direct maison. Nécessite un device GX (Cerbo GX) ou un Cerbo/compatible. → simplifie P3, fiabilise SOC LiFePO4.
- **Stratégie radio** : **un seul réseau Zigbee** (Z2M) + densifier avec des **routeurs alimentés** ; Matter/Thread **en option tardive** (HA Connect ZBT-2) — mais vu la régression HAOS 18 Matter/OTBR sur RPi5, **ne pas activer Thread/Matter maintenant**.
- **ESPHome (2025.11)** : bonnes pratiques → `substitutions`, `cpu_frequency: 160MHz` pour réduire la conso, capa 100-1000 µF sur 3.3 V (pics), boutons `safe_mode`+`restart`. À appliquer aux ESP32-C3/S3 (DS300 Tap, niveau liquide).
- **Budget énergie RPi 5** : ~3.5-5 W en charge (vs HA Green 2-3 W). À intégrer dans le bilan batterie van (UPS 2×18650).
- **Home Assistant Green** : alternative « tout-en-un » 1er prix (99 €, 2-3 W) pour sites secondaires (maison/Italie) si la puissance RPi 5 n'est pas nécessaire.

---

## 13. Actions de resynchronisation (issues de cet audit)
1. **BOM-VANLIFE.md** : corriger alim (X1205→X1200) + stockage (SD, NVMe retiré) + capteurs restants.
2. **ADR-003** : amender (NVMe boot abandonné → SD).
3. **INDEX.md** : réécrire sur la structure réelle (`passe-utile/`, docs 2026-10, 4 nœuds).
4. **executive-summary** : aligner (4 nœuds, état van réel, pas « tout reçu »).
5. **Ranger** : 4 notes datées racine + `passe-utile/taches-annulees/` + fichier Instagram → `HISTORIQUE/`.

---

## 14. Gouvernance & sources de vérité
- **Opérationnel** : `thread-iot.md`.
- **BOM maître** : `iot-van/BOM-VANLIFE.md` (à resynchroniser).
- **Décisions** : `iot-van/adr/`.
- **Procurement** : `_shared/procurement-register.md`.
- **Spécialistes** : Araignée (Zigbee/ESPHome/capteurs), Forge (hardware/ADR), Atlas (doc/synthèse), Vega (architecture).

---

## 15. Annexe — sources veille (2026-10-29)
Home Assistant (RPi5 recommandé, coordinateur unique, Matter/Thread optionnel ; régression HAOS 18 OTBR/Matter sur RPi5) · Victron GX integration HA (MQTT natif) · ESPHome 2025.11 changelog + FAQ (cpu_frequency, caps) · comparatifs RPi5 vs HA Green (conso 3.5-5 W vs 2-3 W) · Vanomation (HA en van).

---

## 16. Revue des experts internes (V0.1)

> 3 revues internes — Forge (hardware/énergie), Araignée (radio/ESPHome), Atlas (doc/cohérence). Constats **vérifiés sur les fichiers réels**.

### 16.1 Forge — hardware/énergie — verdict : **à corriger**
- Forts : diagnostic undervoltage correct ; chaîne alim cadrée (ADR-001 : fusible 5 A, DC-DC USB-C PD 5 A, masse -B2) ; WiCAN Pro bien cadré.
- À corriger : **DC-DC USB-C PD 5 A absent du BOM** (seul HW-133 3 A non-PD listé) → X1200 « 5,1 V/5 A » inatteignable ; **X1200 non vérifié** (datasheet, pogo vs connecteur, jauge I²C 0x32/0x36 pour shutdown) ; budget à réconcilier.
- Recos : (1) ajouter DC-DC PD 5 A ; (2) valider X1200 sur datasheet avant achat ; (3) vérifier jauge I²C ; (4) resynchroniser BOM ; (5) tester la chaîne 12V→5V en charge.

### 16.2 Araignée — radio/capteurs/ESPHome — verdict : **à corriger (1 blocker)**
- Forts : Z2M + ZBDongle-E (adapter ember) cohérent ; DS300 Tap bonne archi ADC (ADS1115 16-bit, optocoupleurs) ; §12 sain.
- **BLOCKER vérifié** : `iot-van/ds300-tap/esphome-ds300.yaml` → **GPIO8 utilisé 2×** (`sda: GPIO8` l.53 + `Main Relay` l.236). Config à corriger (autre GPIO pour le relais) **avant tout flash**.
- À corriger : canal Zigbee **15 recouvre Wi-Fi 6** (ADR-002 « 15-20 » erroné : 15→Wi-Fi 6, 20→Wi-Fi 11 ; RUT240 ajoute un AP 2,4 GHz) ; **routeur de secours** = Sonoff S31 **Wi-Fi** (variante ZB = US 120 V) → seul vrai routeur du panier = GLEDOPTO ; **Aqara MCCGQ11LM non Zigbee 3.0** (ré-appairages).
- Recos : (1) corriger GPIO8 ; (2) canal Zigbee hors Wi-Fi 1/6/11 (ex. 25) ; (3) ajouter de vrais routeurs alimentés ; (4) standardiser capteurs ZB 3.0 ; (5) ESPHome `cpu_frequency` + capa anti-pics.

### 16.3 Atlas — doc/cohérence — verdict : **à corriger (budget/capteurs)**
- Forts : dispositif anti-drift ; traçabilité des renvois vérifiée (tous les chemins cités existent) ; TTD aligné thread.
- À corriger : budget incohérent à 3 niveaux (584 € / 370 € / ~150 €) — corrigé en §7 ; compte capteurs contradictoire (7 vs 8 ; LISTE 01/10 = 10/121 €) — corrigé en §3.5.
- Recos : (1) réconcilier le « reste » (~150 € court terme) ; (2) unifier le compte capteurs ; (3) réécrire INDEX ; (4) aligner exec-summary ; (5) ranger les obsolètes en HISTORIQUE.

### 16.4 Action prioritaire (avant flash van)
**Corriger `esphome-ds300.yaml` (GPIO8 ×2)** + **ajouter le DC-DC USB-C PD 5 A** + **valider X1200** = les 3 points qui bloquent réellement le P0.

---

*Fin du dossier V0.1 — revue experts internes intégrée (Forge/Araignée/Atlas).*
