# WILDMESH — Réseau LoRa Mesh pour caméras-pièges naturalistes

> *Projet open source de surveillance faunistique distribuée*
> Initié par JC Havaux — avril 2026

---

## 1. Contexte et origine

Ce projet est né de la convergence de deux besoins :
- Gérer un réseau de caméras-pièges en forêt sans déplacement physique systématique
- Offrir à des communautés naturalistes un outil de collecte de données environnementales augmenté

L'idée centrale : utiliser un réseau maillé LoRa pour relier des nœuds autonomes (caméra + capteurs environnementaux) déployés en milieu forestier, capables de remonter des métriques de télémétrie sans infrastructure cellulaire ni Wi-Fi.

---

## 2. Objectifs

### Objectifs primaires
- Transmettre à distance les métriques de chaque caméra : localisation GPS, état de batterie, nombre de photos prises, horodatage de la dernière prise
- Couvrir un maillage de **10 nœuds espacés de ~500 m** en forêt dense
- Fonctionner de façon autonome (solaire + batterie)

### Objectifs secondaires
- Intégrer des capteurs environnementaux par nœud : température, humidité, luminosité
- Rendre le système reproductible et documenté pour des communautés naturalistes (associations, chercheurs, gestionnaires d'espaces naturels)
- Maintenir un coût unitaire accessible

### Hors périmètre (V1)
- Transmission des photos via LoRa (bande passante incompatible — max ~250 bytes/paquet)
- Interface cloud propriétaire

---

## 3. Architecture technique envisagée

### Technologie réseau
**LoRa mesh** — protocole Meshtastic (open source, actif, communauté large)

| Paramètre | Valeur cible |
|---|---|
| Portée inter-nœuds | 500 m (forêt dense) |
| Nombre de nœuds | 10 |
| Topologie | Mesh (chaque nœud = relais potentiel) |
| Fréquence EU | 868 MHz (bande ISM européenne) |
| Payload par trame | < 30 octets (métriques seules) |

### Nœud type (hardware proposé)

| Composant | Référence indicative | Rôle |
|---|---|---|
| MCU + LoRa | ESP32 + module RA-02 / RAK3272 | Cerveau + radio |
| Caméra trigger | Raspberry Pi Zero 2W + caméra HQ | Capture image |
| Capteur env. | BME280 (temp/humidité/pression) | Données microclimat |
| Capteur lumière | BH1750 ou VEML7700 | Luminosité lux |
| GPS | u-blox NEO-6M ou M8N | Localisation nœud |
| Stockage | Carte microSD 64 Go | Photos locales |
| Alimentation | Panneau solaire 5W + batterie LiFePO4 18650 | Autonomie totale |
| Boîtier | IP65 minimum | Résistance terrain |

### Données transmises par nœud (télémétrie)

```
- node_id        : identifiant unique
- gps_lat/lon    : position (fixe ou GPS embarqué)
- battery_pct    : % batterie
- photo_count    : nombre de photos sur la SD
- last_photo_ts  : timestamp dernière photo
- temp_c         : température (°C)
- humidity_pct   : humidité relative (%)
- lux            : luminosité (lux)
- rssi           : qualité signal LoRa
```

### Architecture du réseau

```
[Nœud 1] ──┐
[Nœud 2] ──┤
[Nœud 3] ──┤──> [Nœud Gateway] ──> [Base station] ──> Dashboard local / MQTT
[...]      ──┤
[Nœud 10] ──┘
```

La gateway (nœud central ou de bordure) peut être connectée via :
- 4G LTE (carte SIM) pour envoi distant
- Wi-Fi si proximité d'un bâtiment
- Stockage local sur carte SD + collecte périodique

---

## 4. Analyse du marché — caméras commerciales

### Bilan de l'état de l'art

| Approche | Exemple | Verdict |
|---|---|---|
| LoRa natif propriétaire | Covert LC32 | Écarté : fermé, réseau US (AT&T/Verizon), pas de télémétrie exposée |
| Firmware hackable | Browning Recon Force / HP5 | Intéressant mais modification firmware complexe, pas de port série externe |
| SD card intercept | Expérimental (WILDLABS) | Technique élégante mais pas mature |
| Build custom (recommandé) | Pi Zero 2W + ESP32 + LoRa | Contrôle total, open source, extensible |

**Recommandation V1 :** construction from scratch sur base Raspberry Pi Zero 2W + module LoRa externe. Donne un contrôle total sur les données et l'intégration des capteurs.

---

## 5. Contraintes identifiées

- **Portée réelle en sous-bois** : variable selon végétation — prévoir nœuds relais intercalaires si nécessaire
- **Consommation** : le Pi Zero 2W doit impérativement être en veille profonde entre déclenchements (gestion PIR → wake → capture → sleep)
- **Synchronisation horaire** : RTC (DS3231) ou GPS nécessaire pour horodatage fiable sans réseau
- **Résistance terrain** : boîtier IP65 minimum, condensation, insectes (joint silicone sur connecteurs)
- **Réglementation fréquences** : 868 MHz — duty cycle max 1% en Europe (LoRaWAN), Meshtastic peer-to-peer moins contraint mais à vérifier

---

## 6. Dimension communautaire

### Cible utilisateurs
- Associations naturalistes (LPO, natagora, groupes faune locaux)
- Gestionnaires d'espaces protégés (réserves, parcs naturels)
- Chercheurs en écologie (suivis longue durée)
- Photographes animaliers avec démarche scientifique

### Valeur ajoutée vs solutions existantes
- Aucune dépendance à une infrastructure cellulaire ou Wi-Fi
- Données environnementales couplées aux données de présence faunistique
- Open source et reproductible (documentation complète)
- Coût unitaire cible : < 150 € / nœud

### Intégration données possibles
- Export GBIF (format Darwin Core)
- Compatibilité iNaturalist / Observation.org
- API MQTT pour dashboard type Home Assistant ou Grafana

---

## 7. Étapes projet — Roadmap V1

| Phase | Contenu | Statut |
|---|---|---|
| **P0 — Cadrage** | Brief projet, architecture, BOM | ✅ En cours |
| **P1 — Prototype nœud unique** | 1 nœud fonctionnel : caméra + capteurs + LoRa | À faire |
| **P2 — Mesh 3 nœuds** | Validation portée, relais, télémétrie | À faire |
| **P3 — Déploiement 10 nœuds** | Terrain réel, autonomie, robustesse | À faire |
| **P4 — Dashboard** | Visualisation métriques, alertes batterie | À faire |
| **P5 — Documentation open source** | Guide de montage, code, schémas | À faire |
| **P6 — Diffusion communautaire** | Publication, retours, itérations | À faire |

---

## 8. Questions ouvertes

- Quel protocole mesh privilégier : **Meshtastic** (mature, large communauté) ou **MeshCore** (plus récent, plus flexible) ?
- Gestion des images : collecte manuelle sur SD ou transmission différée via gateway 4G ?
- Nom du projet / branding pour diffusion communautaire
- Licence open source : MIT, GPL, CERN OHL (hardware) ?
- Partenariats potentiels : Natagora, universités belges (ULg, UCLouvain) ?

---

## 9. Références et ressources

- [Meshtastic](https://meshtastic.org) — firmware mesh LoRa open source
- [MeshCore](https://meshcore.co.uk) — alternative mesh LoRa
- [WILDLABS](https://wildlabs.net) — communauté tech conservation
- [Conservation X — Camera Trap 3.0](https://conservationx.com/challenge/cameratrap/camera)
- [Winterberry Wildlife](https://winterberrywildlife.ouroneacrefarm.com) — firmware hacking Browning
- BME280 datasheet — Bosch Sensortec
- RAK3272 datasheet — RAKWireless

---

*Document généré le 22 avril 2026 — version 0.1 — à compléter au fil du projet*
