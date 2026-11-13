# Plan — Hub HA « JC home » (maison/serre) sur RPi 5 (Esneux)

> Projet 11 (IOT) · Dobby 🦉 · 2026-11-07
> Décision : dédier le **RPi 5 (4 Go, jamais utilisé)** au pilotage maison/serre, à Esneux (domicile, serre dans le jardin).

## Architecture cible

```
Van (Lupo)        → RPi 5 8 Go   (HAOS)    · ZBDongle-E canal 11   → van uniquement
JC home (maison/serre) → RPi 5 4 Go (HAOS) · 2ᵉ ZBDongle-E canal 15 → vanne + AirGuard serre + LuxSerre  ← NOUVEAU
M5 (Mac)          → dev/desktop  (HA Docker à terme retiré)
```

## Matériel requis (tout en stock)

| Élément | Statut |
|---------|--------|
| RPi 5 (4 Go) jamais utilisé | ✅ stock |
| 2ᵉ Sonoff ZBDongle-E (maison/serre) | ✅ reçu (06/11), à affecter |
| microSD **64 Go High Endurance A2** | ✅ utilisée (64 Go FAT32) |
| Alim officielle RPi5 27W (5V/5A) | ✅ stock (obligatoire pour RPi 5) |

## Procédure (7 étapes)

1. **Flasher HAOS** sur microSD → image officielle **`rpi5-64`** (Raspberry Pi Imager → « Other specific-purpose OS » → Home Assistant → HAOS RPi 5).
2. **Booter le RPi 5** → brancher au réseau Esneux (Ethernet), accéder à `http://homeassistant.local:8123` → créer le compte, nom du hub : **`JC home`**.
3. **Tailscale** → add-on Tailscale (clé d'auth PKA) pour supervision à distance.
4. **Add-ons** → installer **Mosquitto** (broker MQTT) + **Zigbee2MQTT**.
5. **Zigbee** → brancher le 2ᵉ ZBDongle-E sur le RPi 5, config Z2M : `serial: /dev/ttyACM0` (ou ttyUSB0), `adapter: ember`, **canal 15**.
6. **Ré-appairer les 3 appareils** (voir checklist ci-dessous).
7. **Migrer + basculer** → dashboards/automatisations depuis M5, puis éteindre HA sur M5 (ou garder en dev).

## Checklist ré-appairage (étape 6)

- [ ] **Vanne** (Sonoff ZBSWV `0x44e2…`) → retirer de M5, appairer sur RPi 5, renommer `vanne_serre`
- [ ] **AirGuard serre** (SNZB-02DR2 `0xa4c1…`) → idem, renommer `serre_temp_hum`
- [ ] **LuxSerre** (mouvement `0x54ef…`) → idem, garder `LuxSerre`

*Procédure : sur M5, supprimer l'appareil (Z2M « force remove ») → sur RPi 5, activer `permit_join` → réappairer physiquement chaque capteur (bouton ~5 s).*

## Points d'attention

- **Couverture Zigbee** : placer le RPi 5 **près d'une fenêtre côté jardin** (la serre est à l'extérieur). Les 3 capteurs sont sur batterie (end devices, pas routeurs) → la portée du coordinateur compte.
- **Canal** : garder **15** (pas de conflit avec le van sur 11).
- **Backup** : après configuration, faire un backup HAOS complet (pour pouvoir réinstaller en 5 min).
- **Règle de routage** : une fois le RPi 5 en service, mettre à jour `hardware-state.md` (RPi 5 affecté maison/serre) et `etat-projets.md`.

## Rollback

- Rien n'est cassé sur M5 tant qu'on n'éteint pas son HA. Le basculement est réversible : M5 HA reste en secours jusqu'à validation du RPi 5.
