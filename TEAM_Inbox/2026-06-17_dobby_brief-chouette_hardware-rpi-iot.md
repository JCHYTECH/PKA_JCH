# Brief — [[Chouette]] 🦉 : Validation hardware RPi IoT + PI-CI

**Date :** 2026-06-17  
**Émis par :** [[Dobby]]  
**Deadline :** 2026-06-28 (2 semaines)  
**Priorité :** P0 — déploiement hardware RPi Belgique  

## Contexte

Le RPi 5 4GB est reçu (10 juin) avec SSD, alim, boîtier, ZBDongle-E. Le capteur SNZB-02DR2 (Temphumid) est déjà opérationnel sur M5 — à migrer vers le RPi.

PI-CI permet de préparer et tester la config avant flashage. Une fois la config validée par [[Forge]], [[Chouette]] prend le relais hardware.

## Missions

### 1. Assembler et tester le hardware RPi
- Assembler RPi 5 + SSD USB + boîtier + refroidisseur actif
- Brancher le ZBDongle-E, identifier le port série (`ls /dev/serial/by-id/`)
- Flasher l'image SD préparée par [[Forge]] (PI-CI)
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/rpi-belgique/hardware-setup.md` (photos, ports, checklists)

### 2. Migrer le capteur Zigbee SNZB-02DR2
- Actuellement appairé au ZBDongle-E sur M5 → désappairer → ré-appairer sur RPi
- Valider que les données remontent dans HA (température, humidité)
- **Livrable :** Rapport de migration + screenshot dashboard HA

### 3. Valider le script d'installation
- Une fois [[Forge]] a livré `install-rpi.sh`, exécuter sur le RPi physique
- Reporter tout bug ou écart vs PI-CI
- **Livrable :** Feedback pour [[Forge]]

### 4. (Bonus) Spécifier le hardware Van
- Architecture distribuée : 3 HA autonomes (Belgique, Italie, Van)
- Le van a des contraintes spécifiques : offline, alimentation batterie, espace réduit
- **Action :** Lister les capteurs nécessaires (porte frigo, température, alarme), proposer une BOM légère
- **Livrable :** `JCH_Inbox/03_PROJECTS/11_IOT/iot-van/hardware-spec.md`

## Références
- `docs/system/station-domotique-plan-rpi5.md` — plan RPi5
- `docs/manuels/sonoff-zigbee-ha-guide.md` — guide appairage Zigbee
- `MEMORY.md` — architecture distribuée (13 juin), leçon Docker restart (16 juin)
