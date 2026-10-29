# SOP-08 — Phase H : Test caméra OV5640

**SOP :** SOP-08  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** H — Test module caméra OV5640 DVP  
**Durée :** ~35 minutes  
**Prérequis :** SOP-05 réussi, module OV5640 Arducam DVP M12 reçu  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## ⚠️ AVERTISSEMENT — LIRE AVANT DE COMMENCER

1. **Ne jamais brancher la caméra sans le pinout exact du module.** Les modules OV5640 ont des brochages différents selon les versions (Arducam, Waveshare, modules nus).
2. **Ne jamais forcer la nappe.** Si elle résiste, vérifier le sens d'insertion.
3. **L'OV5640 chauffe en mode actif.** Ne pas laisser la caméra allumée en continu. Après chaque capture, la mettre en veille.
4. **La nappe DVP est fragile.** Pas de pliure serrée. Rayon de courbure > 5 mm.

---

## Matériel spécifique

| # | Élément |
|---|---------|
| 1 | Module caméra OV5640 DVP (Arducam M12 ou équivalent) |
| 2 | Nappe DVP (généralement fournie avec le module) |
| 3 | Lentille M12 IR-corrigée (Lensation LS-6028 ou similaire) |

---

## Étape 1 — Identifier le pinout

### Pinout Arducam OV5640 DVP (le plus probable pour le BOM)

| Signal OV5640 | ESP32-S3 GPIO | Câble |
|--------------|:------------:|-------|
| VCC (3.3V) | 3V3 | Rouge |
| GND | GND | Noir |
| SIOC (I²C clock) | GPIO 21 | Jaune |
| SIOD (I²C data) | GPIO 20 | Vert |
| XCLK | GPIO 17 | Orange |
| VSYNC | GPIO 1 | Violet |
| HREF | GPIO 2 | Gris |
| PCLK | GPIO 18 | Blanc |
| D0-D7 | GPIO 4-11 | (8 fils) |

> ⚠️ **SI VOTRE MODULE A UN PINOUT DIFFÉRENT :** arrêter, noter les différences, demander l'arbitrage de [[Forge]] AVANT de brancher.

---

## Étape 2 — Firmware `wn_cam_test` (3 minutes)

```cpp
// SOP-08 — wn_cam_test
// WildNexus P0 — Phase H — Test caméra OV5640
// Capture une image JPEG, mesure le boot et la capture, puis deep sleep.

#include "esp_camera.h"
#include "esp_sleep.h"

// Pinout Arducam OV5640 DVP → ESP32-S3
#define CAM_PIN_PWDN  -1  // Pas utilisé
#define CAM_PIN_RESET -1  // Pas utilisé
#define CAM_PIN_XCLK  17
#define CAM_PIN_SIOD  20
#define CAM_PIN_SIOC  21
#define CAM_PIN_D7    11
#define CAM_PIN_D6    10
#define CAM_PIN_D5     9
#define CAM_PIN_D4     8
#define CAM_PIN_D3     7
#define CAM_PIN_D2     6
#define CAM_PIN_D1     5
#define CAM_PIN_D0     4
#define CAM_PIN_VSYNC  1
#define CAM_PIN_HREF   2
#define CAM_PIN_PCLK  18

static camera_config_t cam_cfg = {
  .pin_pwdn  = CAM_PIN_PWDN,
  .pin_reset = CAM_PIN_RESET,
  .pin_xclk  = CAM_PIN_XCLK,
  .pin_sccb_sda = CAM_PIN_SIOD,
  .pin_sccb_scl = CAM_PIN_SIOC,
  .pin_d7 = CAM_PIN_D7, .pin_d6 = CAM_PIN_D6,
  .pin_d5 = CAM_PIN_D5, .pin_d4 = CAM_PIN_D4,
  .pin_d3 = CAM_PIN_D3, .pin_d2 = CAM_PIN_D2,
  .pin_d1 = CAM_PIN_D1, .pin_d0 = CAM_PIN_D0,
  .pin_vsync = CAM_PIN_VSYNC,
  .pin_href  = CAM_PIN_HREF,
  .pin_pclk  = CAM_PIN_PCLK,
  .xclk_freq_hz = 20000000,
  .ledc_timer   = LEDC_TIMER_0,
  .ledc_channel = LEDC_CHANNEL_0,
  .pixel_format = PIXFORMAT_JPEG,
  .frame_size   = FRAMESIZE_VGA,  // 640x480
  .jpeg_quality = 10,
  .fb_count     = 1,
  .grab_mode    = CAMERA_GRAB_WHEN_EMPTY
};

RTC_DATA_ATTR int cap_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  cap_count++;

  Serial.printf("=== CAM TEST #%d ===\n", cap_count);

  esp_err_t err = esp_camera_init(&cam_cfg);
  if (err != ESP_OK) {
    Serial.printf("❌ CAM INIT FAILED: 0x%x\n", err);
    esp_deep_sleep(30ULL * 1000000ULL);
    return;
  }
  Serial.println("✅ Cam init OK");

  // Capturer une image
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("❌ Capture FAILED");
  } else {
    Serial.printf("✅ Capture OK — %zu bytes\n", fb->len);
    esp_camera_fb_return(fb);
  }

  esp_camera_deinit();
  Serial.println("Cam → off");

  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

---

## Étape 3 — Branchement (10 minutes)

1. ESP32 **débranché** de l'USB et du PPK2.
2. Insérer la nappe dans le connecteur caméra.
3. Insérer l'autre extrémité dans le connecteur du module OV5640.
4. **Ne pas forcer.** Le connecteur a un petit clip qu'il faut soulever pour insérer, puis rabattre.
5. Brancher les 14+ fils Dupont selon le pinout ci-dessus.
6. **Double check :** XCLK → GPIO17, SIOD → GPIO20, SIOC → GPIO21.

---

## Étape 4 — Test sans PPK2 (5 minutes)

1. Brancher l'ESP32 en USB.
2. Flasher `wn_cam_test`.
3. Moniteur série 115200 baud.

```
=== CAM TEST #1 ===
✅ Cam init OK
✅ Capture OK — 15360 bytes
Cam → off
```

> ✅ Init + capture OK → caméra fonctionnelle.

> ❌ `CAM INIT FAILED` :
> - Vérifier le câblage, en particulier XCLK, SIOD, SIOC
> - Vérifier que la nappe est bien enclenchée
> - Certains modules OV5640 nécessitent PWDN ou RESET — adapter le pinout

> ❌ `Capture FAILED` mais init OK :
> - Vérifier la connexion D0-D7, VSYNC, HREF, PCLK
> - La lentille est-elle vissée ? (certains modules refusent de capturer sans lentille)

---

## Étape 5 — Mesure PPK2 (10 minutes)

1. Débrancher USB ESP32.
2. PPK2 OFF → VOUT→5V, GND→GND.
3. Source Meter 5.0V, acquisition, sortie ON.

**Courbe attendue :**

```
Courant
  │
  │  ┌─────────────────────────┐
  │  │  boot caméra + capture  │
  │  │  ~120-200 mA (!)        │
  │──┘                         └──────────────────────┐
  │                                                   │
  │  ▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔▔  ← sleep        │
  └───────────────────────────────────────────────────────→
```

| Mesure | Valeur |
|--------|--------|
| Courant boot caméra (mA) | _____ mA |
| Courant pic capture (mA) | _____ mA |
| Durée boot + capture (s) | _____ s |
| Charge cycle caméra (mAh) | _____ mAh |
| Deep sleep caméra OFF (µA) | _____ µA |
| ⚠️ La caméra chauffe-t-elle ? | Oui / Non |

> ⚠️ L'OV5640 consomme **beaucoup** en actif (120-200 mA). C'est pour ça que le BOM prévoit un MOSFET de power gating — on coupe complètement l'alimentation de la caméra entre deux captures. Le `esp_camera_deinit()` doit ramener la consommation à zéro. Si ce n'est pas le cas → documenter.

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Init caméra | OK | Timeout | Échec |
| Capture JPEG | > 5 kB | 1-5 kB | 0 byte |
| Deep sleep cam OFF | < 150 µA | 150-300 µA | > 300 µA |
| Surchauffe | Aucune | Tiède après 3 captures | Chaud après 1 capture |

---

## Clôture

- [ ] Pinout vérifié avant branchement
- [ ] Nappe insérée sans forcer, clip verrouillé
- [ ] `wn_cam_test` compilé et flashé
- [ ] Init + capture OK
- [ ] Mesure PPK2 : boot + capture + sommeil
- [ ] Caméra correctement éteinte après deinit (deep sleep < 150 µA)

---

**Fin de SOP-08. Prochaine étape : SOP-09 Phase I — Test PIR EKMB.**
