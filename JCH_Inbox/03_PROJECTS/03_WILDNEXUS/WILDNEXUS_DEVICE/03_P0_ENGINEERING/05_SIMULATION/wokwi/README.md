# WildNexus Wokwi Simulation — [[README]]

**Date :** 2026-06-14  
**Owner :** [[Dobby]] 🦉  
**Statut :** ✅ Fonctionnel — ESP32-S3 + LED + SD + PIR + deep sleep validés

## Fichiers

| Fichier | Rôle |
|---------|------|
| `wokwi.toml` | Config Wokwi (ELF + firmware binary) |
| `diagram.json` | Schéma : ESP32-S3-DevKitC-1 + PIR + LED + microSD |
| `wokwi.ino` | Firmware Arduino smoke test |
| `libraries.txt` | Dépendances (SD) |
| `build/` | Binaires compilés (ne pas commiter) |

## Résultat simulation (2026-06-14)

```
ESP-ROM:esp32s3-20210327
BOOT #1 | BOOT_COLD
LED:OK
SD:OK
LOG:OK
SLEEP 10s
TEST PASSED.
```

## Quick start

### 1. Setup (one-time)
```bash
# Token Wokwi
export WOKWI_CLI_TOKEN="wok_..."   # depuis https://wokwi.com/dashboard/ci

# Compiler
cd 03_P0_ENGINEERING/05_SIMULATION/wokwi
arduino-cli compile --fqbn esp32:esp32:esp32s3 --build-path build .
```

### 2. Run simulation
```bash
wokwi-cli . --timeout 30000 --expect-text "BOOT #1" --expect-text "SD:OK"
```

### 3. CI (GitHub Actions)
```yaml
- name: Wokwi Smoke Test
  uses: wokwi/wokwi-ci-action@v1
  with:
    token: ${{ secrets.WOKWI_CLI_TOKEN }}
    path: 03_P0_ENGINEERING/05_SIMULATION/wokwi
    timeout: 30000
    expect_text: |
      BOOT #1
      LED:OK
      SD:OK
      LOG:OK
```

## Pinout simulé

| Composant | GPIO | Type Wokwi |
|-----------|------|------------|
| LED IR | GPIO2 | `wokwi-led` |
| PIR EKMB | GPIO4 | `wokwi-pir-motion-sensor` |
| SD SCK | GPIO14 | `wokwi-microsd-card` |
| SD MISO | GPIO12 | (DO sur le part) |
| SD MOSI | GPIO13 | (DI sur le part) |
| SD CS | GPIO15 | |

## Limitations

- ❌ Caméra OV5640 — non simulable
- ❌ LoRa SX1262 — non simulable
- 🟡 Deep sleep — simulé mais pas cycle-accurate
- 🟡 50 min/mois gratuites (plan Free)

## Leçons apprises

1. **Serial monitor obligatoire** : `diagram.json` doit connecter `$serialMonitor` pour capturer le output
2. **Compiler en ELF** : le CLI Wokwi n'accepte pas le source `.ino`, il faut compiler avant
3. **`fullBoot: "1"`** : utile pour voir les messages de boot ESP32
4. **ESP32-S3 fonctionne** : le type `board-esp32-s3-devkitc-1` est supporté
