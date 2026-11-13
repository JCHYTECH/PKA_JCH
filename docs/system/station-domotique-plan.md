# Plan — Station Domotique Maison + Van

> Généré le 2026-06-07 — modèle: DeepSeek V4
> Objectif : remplacer le Docker HA sur M5 par une station dédiée, transportable maison/van

---

## 1. Checklist Achat

### Matériel principal

| Qté | Référence | Prix estimé | Usage |
|-----|-----------|-------------|-------|
| Qté | Référence | Prix constaté (06/2026) | Usage |
|-----|-----------|-------------------------|-------|
| 1 | **Beelink Mini S12 Pro** (N100, 16GB, 500GB SSD) | ~369€ | Station domotique HA OS |
| 1 | **Sonoff ZBDongle-P** (CC2652P7) | ~18€ | Coordinateur Zigbee ZHA |

### Alimentation van

| Qté | Référence | Prix constaté (06/2026) | Usage |
|-----|-----------|-------------------------|-------|
| 1 | **Régulateur DC-DC Step-Down 12V/12V** (LM2596 avec affichage, ou Mean Well SD-15A-12) | ~10-15€ | Stabiliser l'alim van (10-14.6V → 12V fixe) |
| 1 | **Câble allume-cigare → jack 5.5/2.5mm 12V** | ~8-12€ | Branchement rapide dans le van |
| 1 | **Porte-fusible 5A + fusible 5A** | ~3€ | Protection circuit van |
| 1 | **Câble secteur C8 vers jack 12V** (maison) | ~8-10€ | Alimentation secteur à la maison |

### Accessoires

| Qté | Référence | Prix constaté (06/2026) | Usage |
|-----|-----------|-------------------------|-------|
| 1 | **Câble USB-A vers USB-C** (1m) | ~5€ | Dongle Zigbee → N100 |

**Total : ~410-435€**

---

## 2. Installation HA OS sur N100

### Étapes

```
Étape 1 — Télécharger HA OS
   → https://github.com/home-assistant/operating-system/releases
   → Version "Generic x86-64" (haos_generic-x86-64-*.img.xz)

Étape 2 — Graver sur clé USB bootable
   Balena Etcher (GUI) ou dd (CLI) :
   xzcat haos_generic-x86-64-*.img.xz | dd of=/dev/sdX bs=4M status=progress

Étape 3 — Booter le N100 sur la clé USB
   → HA OS s'installe automatiquement sur le SSD NVMe

Étape 4 — Premier accès
   → Attendre ~10 min, naviguer vers http://homeassistant.local:8123
   → Suivre le wizard de création de compte

Étape 5 — Ajouter le dongle Zigbee
   → Brancher Sonoff ZBDongle-P en USB
   → Aller dans Paramètres → Intégrations → Ajouter → ZHA
   → Sélectionner /dev/ttyACM0 ou /dev/ttyUSB0
```

### Addons recommandés

Via le store des addons HA OS :
- **Mosquitto MQTT** — broker MQTT pour l'IoT
- **ESPHome** — gestion des ESP32/ESP8266
- **Samba/SCP** — accès fichiers config
- **Studio Code Server** — éditer config depuis le navigateur

---

## 3. Migration depuis Docker M5

### Ce qui change

| Composant | Emplacement MAINTENANT | Destination sur N100 |
|-----------|----------------------|---------------------|
| Configuration HA | `_local/homeassistant/` | Backup → restore |
| Automations/Scènes/Scripts | YAML | Backup → restore |
| Intégrations | config_entries | Re-config (automatique via backup) |
| Dongle Zigbee | Aucun | Sonoff ZBDongle-P via USB |
| Accès distant | Tailscale 100.108.55.44:8123 | À re-vérifier |

### Procédure

```
[M5] $ docker exec homeassistant ha backups create --name "migration-van"
[M5] $ docker cp homeassistant:/backup ./backup-migration.tar

→ Copier le fichier .tar sur le N100

[N100] HA → Paramètres → Système → Backups → Upload backup
[N100] Restaurer → Confirmer
```

Après restauration :
- Vérifier que l'URL Tailscale pointe toujours vers la bonne IP
- Reconfigurer go2rtc (le localhost change)
- La mobile app (iPhone) se reconnecte automatiquement

---

## 4. Alimentation van — Schéma

```
Batterie Lithium 12V  ─── Fusible 5A ─── Régulateur DC-DC ─── N100 (jack)
                                                         └── Step-Down 5V ─── ZBDongle-P USB
```

Points critiques :
- **Tension van** : une batterie LiFePO4 varie de 10V à 14.6V. Le régulateur stabilise à 12V constant.
- **Fusible 5A** côté batterie : protection en cas de court-circuit.
- **Connexion rapide** : le câble allume-cigare permet de tout débrancher en 2 secondes.

---

## 5. Plan de déploiement

### Phase 1 — Achat
- [ ] Commader Minisforum UN100 (ou Beelink S12 Pro)
- [ ] Commader Sonoff ZBDongle-P
- [ ] Commader SSD NVMe 256GB (si nécessaire)
- [ ] Commader câble alim van + régulateur

### Phase 2 — Installation N100
- [ ] Installer HA OS sur N100
- [ ] Brancher dongle Zigbee, configurer ZHA
- [ ] Restaurer backup depuis le M5
- [ ] Vérifier intégrations, automations, mobile app

### Phase 3 — Mise en service
- [ ] Arrêter le container Docker HA sur M5
- [ ] Vérifier accès local + Tailscale
- [ ] Supprimer le container Docker après confirmation

### Phase 4 — Intégration van
- [ ] Installer le régulateur 12V dans le van
- [ ] Fixer le N100 dans un compartiment sec
- [ ] Brancher le dongle Zigbee
- [ ] Connecter WiFi van ou routeur 4G
- [ ] Tester : couper secteur, confirmer le démarrage sur batterie

---

## À savoir

- Le réseau Zigbee reste stable quand la machine change d'emplacement (le dongle suit la machine)
- Pas de carte SD : SSD NVMe + HA OS, arrêt brutal géré proprement
- Migration réversible : le backup HA permet de revenir au Docker M5 en 5 minutes
- Le M5 retrouve de la RAM et des cycles CPU en n'étant plus serveur
