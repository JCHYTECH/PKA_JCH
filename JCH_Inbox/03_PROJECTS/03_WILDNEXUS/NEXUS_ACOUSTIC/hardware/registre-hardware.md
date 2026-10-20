# NEXUS_ACOUSTIC — Registre hardware (acquisitions)

**Date :** 2026-06-22
**Objet :** Nouveaux composants réceptionnés

---

## Entrée 001 — 2026-06-22

### Geekworm X1201 V1.1 — UPS 18650 pour Raspberry Pi 5

| Champ | Valeur |
|---|---|
| **Référence** | Geekworm X1201 V1.1 |
| **Fonction** | Carte UPS 18650 avec mise sous tension automatique |
| **Compatibilité** | Raspberry Pi 5 |
| **Boîtier** | Geekworm X1201-C1 (métallique, refroidisseur actif intégré) |
| **Réception** | 2026-06-22 |
| **Projets** | NEXUS_ACOUSTIC (station terrain BirdNET-Go) + IOT Vanlife (RPi autonome) |
| **Statut** | À monter |

**Usage NEXUS_ACOUSTIC :**
- Station BirdNET-Go portable sur batterie 18650
- Aligne avec le jalon F-MVP-01 : « station RPi exécute BirdNET-Go 24h/24 »
- Permet tests terrain sans dépendance secteur
- Autonomie estimée : 2× 18650 (3000 mAh) → ~6-8h en continu (RPi 5 + SSD + BirdNET)

**Usage IOT Vanlife :**
- Backup UPS en complément de l'alimentation DC-DC 12V→5V principale
- Maintient le RPi en vie pendant les transitions batterie (démarrage moteur, toggle chargeur)
- Permet un shutdown propre en cas de coupure
- Voir ADR-005 (2026-06-21)

---

### Aqara T1 — Capteur de luminosité Zigbee 3.0

| Champ | Valeur |
|---|---|
| **Référence** | Aqara T1 Zigbee 3.0 |
| **Fonction** | Capteur de luminosité + détecteur de lumière |
| **Protocole** | Zigbee 3.0 |
| **Compatibilité** | Home Assistant, Aqara Home, Apple HomeKit |
| **Fixation** | Magnétique |
| **Réception** | 2026-06-22 |
| **Projets** | IOT Home (domotique maison) |
| **Statut** | À installer |

**Usage :**
- Automatisation éclairage via Home Assistant
- Corrélation luminosité avec données environnementales WildNexus
- Intégration dans le dashboard maison off-grid

---

## Liens

- NEXUS_ACOUSTIC → `Projet_bioacoustique.md` (jalon F-MVP-01)
- IOT Vanlife → `adr/ADR-005-plateforme-hardware-rpi5-vs-x86.md`
- IOT Home → `iot-home/`

---

*Généré par Dobby 🦉 — 2026-06-22*
