# Plan — Station Domotique Maison + Van (RPi5)

> Généré le 2026-06-07 — modèle: DeepSeek V4
> Objectif : remplacer le Docker HA sur M5 par une station RPi5, transportable maison/van
> Version alternative au plan N100 : `station-domotique-plan.md`
> Prix vérifiés DuckDuckGo (Amazon FR, idealo, LDLC) — juin 2026

---

## 1. Checklist Achat

### Matériel principal

| Qté | Référence | Prix vérifié (06/2026) | Source |
|-----|-----------|-----------------------|--------|
| Qté | Référence | Prix vérifié (06/2026) | Statut |
|-----|-----------|-----------------------|--------|
| 1 | **Raspberry Pi 5 4GB** (board seule) | 132,09€ (Amazon) | ✅ commandé |
| 1 | **Bloc alim officiel RPi5 USB-C 27W** | 15,32€ (Amazon) | ✅ commandé |
| 1 | **Hsthe Sea refroidisseur actif RPi5** (ventilateur + radiateur) | 9,99€ (Amazon) | ✅ commandé |
| 1 | **SONOFF SNZB-02DR2 AirGuard TH** (température/humidité Zigbee + écran LCD 3.6'') | 15,15€ (Amazon) | ✅ commandé |
| 1 | **SSD USB 256GB** (Netac / ORICO / SSK) | ~40-55€ | à acheter |
| 1 | **Sonoff ZBDongle-P** (CC2652P7) | ~18€ | à acheter |
| 1 | **Carte microSD 32GB** (pour flash initial uniquement) | ~8€ | à acheter |

### UPS HAT van — remplace le régulateur

| Qté | Référence | Prix vérifié (06/2026) | Statut |
|-----|-----------|-----------------------|--------|
| 1 | **Geekworm X1205 UPS HAT** (entrée 9-18V, sortie 5.1V 6A) | 42,39€ (AliExpress) | ✅ commandé |
| 1 | **Geekbord X1201-C1 boîtier métal** RPi5+UPS | 18,59€ (AliExpress) | ✅ commandé |
| 2 | **Batteries 21700** (Samsung 50E, 5000mAh) | ~20-25€ | à acheter |
| 1 | **Porte-fusible 5A + fusible 5A** | ~3€ | à acheter |

**Total : ~233-246€ déjà dépensé — reste ~74-86€** (SSD, dongle, SD, batteries, fusible)

---

## 2. Installation HA OS sur RPi5

### Matériel nécessaire pour le flash

- Un ordinateur (M5) + lecteur SD (ou Raspberry Pi Imager)
- La carte microSD 32GB (flash initial, puis on boote sur SSD)

### Étapes

```
Étape 1 — Télécharger Raspberry Pi Imager
   → https://www.raspberrypi.com/software/
   → Installer sur le M5

Étape 2 — Flasher HA OS sur la microSD
   → Lancer Raspberry Pi Imager
   → Choose OS → Other specific-purpose OS → Home Assistants → Home Assistant OS
   → Choose Storage → Sélectionner la microSD
   → ⚙️ Configurer : hostname, user/pass, WiFi, activer SSH
   → Write

Étape 3 — Booter le RPi5 sur la microSD
   → Brancher microSD, alimentation, Ethernet
   → Attendre ~10 min

Étape 4 — Premier accès
   → http://homeassistant.local:8123
   → Suivre le wizard

Étape 5 — Basculer le boot sur SSD USB
   → HA → Paramètres → Système → Stockage → Déplacer le datadisk
   → Sélectionner le SSD USB → Redémarrer
```

### Addons recommandés

- **Mosquitto MQTT** — broker MQTT pour l'IoT
- **ESPHome** — gestion des ESP32/ESP8266
- **Samba/SCP** — accès fichiers config
- **Studio Code Server** — éditer config depuis le navigateur

---

## 3. Migration depuis Docker M5

### Procédure

```
[M5] $ docker exec homeassistant ha backups create --name "migration-van"
[M5] $ docker cp homeassistant:/backup ./backup-migration.tar

→ Copier le fichier .tar sur le RPi5

[RPi5] HA → Paramètres → Système → Backups → Upload backup
[RPi5] Restaurer → Confirmer
```

Après restauration :
- Vérifier que l'URL Tailscale pointe toujours sur la bonne IP
- Reconfigurer go2rtc (le localhost change)
- La mobile app (iPhone) se reconnecte automatiquement

---

## 4. Alimentation van — Schéma (UPS HAT)

```
Batterie Lithium 12V ─── Fusible 5A ─── Geekworm X1205 UPS HAT (entrée 9-18V DC5521)
                                             │
                                             ├── Batteries 21700 (backup, 2×5000mAh)
                                             │
                                             └── RPi5 (pogo pins, 5.1V 6A)
                                                    └── Port USB ─── ZBDongle-P
```

Ce schéma remplace le régulateur Step-Down 12V→5V par un UPS HAT complet. Avantages :
- **Entrée 9-18V directe** sur le 12V van — pas de convertisseur supplémentaire
- **Backup batterie** 21700 intégré : le Pi5 reste allumé 4-6h après une coupure
- **Auto power-on** : quand le courant revient, le Pi5 redémarre tout seul
- **Safe shutdown** : le HAT détecte la perte de courant, lance un shutdown propre via GPIO, puis se coupe
- **RTC intégrée** : plus besoin de pile CR1220 externe

---

## 5. Plan de déploiement

### Phase 1 — Achat
- [x] RPi5 4GB board (132,09€ Amazon) ✅
- [x] Geekworm X1205 UPS HAT (42,39€ AliExpress) ✅
- [x] Geekbord X1201-C1 boîtier métal (18,59€ AliExpress) ✅
- [x] Bloc alim officiel RPi5 27W (15,32€ Amazon) ✅
- [x] Hsthe Sea refroidisseur actif RPi5 (9,99€ Amazon) ✅
- [x] SONOFF SNZB-02DR2 AirGuard TH (15,15€ Amazon) ✅
- [ ] SSD USB 256GB (~40-55€)
- [ ] Sonoff ZBDongle-P (~18€)
- [ ] Carte microSD 32GB (~8€)
- [ ] 2× batteries 21700 Samsung 50E (~20-25€)
- [ ] Porte-fusible 5A (~3€)

### Phase 2 — Installation RPi5
- [ ] Installer l'Active Cooler sur le SoC du RPi5
- [ ] Flasher HA OS sur microSD
- [ ] Booter, configurer HA OS
- [ ] Brancher dongle Zigbee, configurer ZHA
- [ ] Basculer datadisk sur SSD USB
- [ ] Installer addons (Mosquitto, ESPHome)
- [ ] Installer le logiciel UPS (script Python fourni par Geekworm)

### Phase 3 — Migration
- [ ] Créer backup HA sur Docker M5
- [ ] Restaurer backup sur RPi5
- [ ] Arrêter le container Docker HA sur M5
- [ ] Vérifier accès local + Tailscale
- [ ] Supprimer le container Docker après confirmation

### Phase 4 — Intégration van
- [ ] Fixer le X1205 sur le RPi5 (pogo pins, entretoises)
- [ ] Brancher le dongle Zigbee
- [ ] Connecter le jack DC5521 du X1205 au 12V van (via fusible 5A)
- [ ] Insérer les batteries 21700
- [ ] Connecter WiFi van ou routeur 4G
- [ ] Tester : couper secteur, vérifier le shutdown propre + redémarrage auto

---

## À savoir

- **4GB suffisent pour HA** : ZHA, ESPHome, Mosquitto, Node-RED tournent confortablement (~1.5-2.5GB utilisés)
- **SSD USB plutôt que SD** : le datadisk sur SSD évite la corruption. La microSD ne sert qu'au flash initial
- **UPS intégré** : le X1205 gère l'alimentation 12V→5V + backup + shutdown — zéro câble supplémentaire
- **Autonomie** : 2× 21700 5000mAh = ~10 000mAh → tient 4-6h en charge HA
- **Conso** : RPi5 ~2.5W au repos, ~7W en charge — négligeable sur batterie van 200Ah
- **Migration réversible** : le backup HA permet de revenir au Docker M5 en 5 minutes
- **Plan N100** : voir `station-domotique-plan.md` pour la version Beelink S12 Pro (~387€)
