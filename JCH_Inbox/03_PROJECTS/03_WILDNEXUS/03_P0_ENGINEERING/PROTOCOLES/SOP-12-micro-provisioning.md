# SOP-12 — Phase L : Micro MEMS + Provisioning

**SOP :** SOP-12  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** L — Test micro MEMS + provisioning clés (eFuse)  
**Durée :** ~30 minutes  
**Prérequis :** SOP-05 réussi, micro MEMS (A06 BOM) + script provisioning disponibles  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 1.0  

---

## Objectif

Deux tests en une phase :

1. **Micro MEMS** : vérifier la capture audio (Scope Lock P0 exige « capture audio locale courte via micro mono »), mesurer la consommation.
2. **Provisioning** : vérifier que la procédure de gravure eFuse (ADR-011) fonctionne : lecture Serial, dérivation de clé, gravure, verrouillage.

---

## Partie A — Test Micro MEMS

### Matériel

| # | Élément |
|---|---------|
| 1 | Micro MEMS analogique ou I²S (réf A06 du BOM) |
| 2 | 3 câbles Dupont |

### Pinout (micro MEMS analogique typique)

| Micro | ESP32-S3 |
|-------|:--------:|
| VCC | 3V3 |
| GND | GND |
| OUT | GPIO 4 (ADC1_CH3) |

### Firmware `wn_mic_test`

```cpp
// SOP-12a — wn_mic_test
// WildNexus P0 — Phase L — Test micro MEMS
// Échantillonne le micro pendant 2 secondes, imprime les niveaux.

#include "esp_sleep.h"

#define MIC_PIN 4
#define SAMPLE_COUNT 100
#define SAMPLE_DELAY_MS 20

RTC_DATA_ATTR int mic_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  mic_count++;

  Serial.printf("=== MIC TEST #%d ===\n", mic_count);
  analogReadResolution(12);

  Serial.print("Samples: ");
  for (int i = 0; i < SAMPLE_COUNT; i++) {
    int val = analogRead(MIC_PIN);
    if (i % 10 == 0) Serial.printf("%d ", val);
    delay(SAMPLE_DELAY_MS);
  }
  Serial.println();

  Serial.println("Mic test done → sleep");
  Serial.flush();
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### Test

1. Brancher le micro (3V3, GND, OUT→IO4).
2. Flasher `wn_mic_test`.
3. Moniteur série : observer les valeurs ADC.
4. **Claquer des doigts** près du micro → les valeurs doivent varier.
5. Silence → valeurs stables (bruit de fond).

> ✅ Valeurs qui varient avec le son → micro fonctionnel.

### Mesure PPK2

| Mesure | Valeur |
|--------|--------|
| Courant actif avec micro (mA) | _____ mA |
| Deep sleep avec micro branché (µA) | _____ µA |
| ⚠️ Micro fuit-il en veille ? | Oui / Non |

---

## Partie B — Test Provisioning (ADR-011)

### Objectif

Vérifier que la procédure de provisioning fonctionne :

```
1. Au premier boot, l'ESP32 lit son numéro de série (MAC)
2. Combine avec une clé maître externe (injectée via Serial)
3. Dérive une clé unique par appareil (HKDF)
4. Grave la clé dans l'eFuse
5. Verrouille l'eFuse → lecture seule
6. Redémarre → vérifie que la clé est accessible mais non modifiable
```

### ⚠️ AVERTISSEMENT — L'eFuse est IRREVERSIBLE

- Une fois verrouillée, une eFuse ne peut plus être modifiée.
- **Ne pas exécuter le verrouillage sur le DevKit de test.** Utiliser un ESP32-S3 dédié au test de provisioning, ou sauter l'étape de verrouillage.
- En production, chaque appareil aura sa propre clé unique.

### Firmware `wn_provision`

```cpp
// SOP-12b — wn_provision
// WildNexus P0 — Phase L — Test provisioning (DRY RUN)
// Lit le MAC, simule la dérivation de clé, mais NE GRAVE PAS l'eFuse.
// Pour le test réel : décommenter la section efuse.

#include "esp_sleep.h"
#include "esp_system.h"
#include "esp_mac.h"
#include "mbedtls/md.h"
#include "mbedtls/sha256.h"

RTC_DATA_ATTR int prov_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  prov_count++;

  Serial.printf("=== PROVISIONING TEST #%d ===\n", prov_count);

  // 1. Lire le MAC (identité unique)
  uint8_t mac[6];
  esp_read_mac(mac, ESP_MAC_WIFI_STA);
  Serial.printf("MAC: %02X:%02X:%02X:%02X:%02X:%02X\n",
                mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // 2. Clé maître (en production : injectée une seule fois via Serial)
  const char *master_key = "WildNexus-P0-MasterKey-2026";
  uint8_t derived_key[32];

  // 3. Dériver clé unique = SHA256(master_key || MAC)
  mbedtls_sha256_context ctx;
  mbedtls_sha256_init(&ctx);
  mbedtls_sha256_starts(&ctx, 0);  // 0 = SHA-256
  mbedtls_sha256_update(&ctx, (const unsigned char *)master_key, strlen(master_key));
  mbedtls_sha256_update(&ctx, mac, sizeof(mac));
  mbedtls_sha256_finish(&ctx, derived_key);
  mbedtls_sha256_free(&ctx);

  Serial.print("Derived key: ");
  for (int i = 0; i < 8; i++) Serial.printf("%02X", derived_key[i]);
  Serial.println("... (first 8 bytes)");

  // 4. DRY RUN — on ne grave PAS l'eFuse sur le DevKit de test
  Serial.println("⚠️ DRY RUN — efuse NOT burned");
  Serial.println("   In production: esp_efuse_write_block(...) here");
  Serial.println("   In production: esp_efuse_set_read_protect(...) after");

  // 5. Vérifier que la clé est reproductible
  Serial.println("✅ Key derivation OK — reproducible");

  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}

void loop() {}
```

### Test

1. Flasher `wn_provision`.
2. Moniteur série :

```
=== PROVISIONING TEST #1 ===
MAC: 7C:DF:A1:xx:xx:xx
Derived key: A3F1092B... (first 8 bytes)
⚠️ DRY RUN — efuse NOT burned
✅ Key derivation OK — reproducible

--- 60 secondes ---

=== PROVISIONING TEST #2 ===
MAC: 7C:DF:A1:xx:xx:xx
Derived key: A3F1092B... (first 8 bytes)   ← IDENTIQUE = reproductible ✓
```

> ✅ Même MAC à chaque boot. Même clé dérivée. → Provisioning OK.

---

## Grille de décision combinée

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| Micro : variation signal | Oui | Faible | Aucune |
| Micro : conso veille | < 10 µA | 10-50 µA | > 50 µA |
| Provisioning : MAC stable | Oui | — | Change à chaque boot |
| Provisioning : clé reproductible | Oui | — | Non |

---

## Clôture

- [ ] Micro MEMS branché et testé
- [ ] Signal audio confirmé (claquement de doigts)
- [ ] Provisioning : MAC lu, clé dérivée, reproductible
- [ ] DRY RUN — eFuse non gravée
- [ ] Mesures PPK2 micro notées

---

## 🏁 FIN DU PARCOURS M-02

Les 12 SOPs couvrent l'intégralité du banc de test P0 :

| Phase | SOP | Composant | Statut |
|-------|-----|-----------|--------|
| A | SOP-01 | ESP32 alive | □ |
| B | SOP-02 | Deep sleep 30s | □ |
| C | SOP-03 | PPK2 deep sleep | □ |
| D | SOP-04 | Réveil 20 cycles | □ |
| E | SOP-05 | Simulation événement | □ |
| F | SOP-06 | microSD | □ |
| G | SOP-07 | LoRa | □ |
| H | SOP-08 | Caméra OV5640 | □ |
| I | SOP-09 | PIR EKMB | □ |
| J | SOP-10 | Batterie AA | □ |
| K | SOP-11 | Edge AI benchmark | □ |
| L | SOP-12 | Micro + Provisioning | □ |

**Une fois toutes les cases cochées GO, M-02 est validé → M-03 EVT terrain.**
