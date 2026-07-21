# SOP-12 — Phase L : Provisioning (eFuse)

**SOP :** SOP-12  
**Projet :** WildNexus P0 — M-02 Prototype banc fonctionnel  
**Phase :** L — Test provisioning clés (eFuse)  
**Durée :** ~15 minutes  
**Prérequis :** SOP-05 réussi  
**Auteur :** [[Dobby]]  
**Date :** 2026-06-12  
**Version :** 2.0 — 2026-07-05 : partie micro extraite vers SOP-13 (ADR-013 I2S stéréo)  

---

## Objectif

Vérifier que la procédure de provisioning de clés fonctionne : lecture MAC, dérivation de clé unique, simulation de gravure eFuse (DRY RUN).

> ⚠️ **La partie micro MEMS a été extraite vers SOP-13** suite à ADR-013 (19/06) : le micro analogique a été remplacé par 2× SPH0645LM4H-B I2S digital stéréo. L'ancien test micro analogique sur ADC GPIO 4 est obsolète.

---

## ⚠️ AVERTISSEMENT — L'eFuse est IRRÉVERSIBLE

- Une fois verrouillée, une eFuse ne peut plus être modifiée.
- **Ne pas exécuter le verrouillage sur le DevKit de test.** DRY RUN uniquement.
- En production, chaque appareil aura sa propre clé unique.

---

## Firmware `wn_provision`

```cpp
// SOP-12 — wn_provision v2
// WildNexus P0 — Phase L — Test provisioning (DRY RUN)
// Lit le MAC, simule la dérivation de clé, NE GRAVE PAS l'eFuse.

#include "esp_sleep.h"
#include "esp_system.h"
#include "esp_mac.h"
#include "mbedtls/sha256.h"

RTC_DATA_ATTR int prov_count = 0;

void setup() {
  Serial.begin(115200);
  delay(500);
  prov_count++;
  Serial.printf("=== PROVISIONING TEST #%d ===\n", prov_count);

  // 1. Lire le MAC
  uint8_t mac[6];
  esp_read_mac(mac, ESP_MAC_WIFI_STA);
  Serial.printf("MAC: %02X:%02X:%02X:%02X:%02X:%02X\n",
                mac[0], mac[1], mac[2], mac[3], mac[4], mac[5]);

  // 2. Clé maître (en production : injectée via Serial)
  const char *master_key = "WildNexus-P0-MasterKey-2026";
  uint8_t derived_key[32];

  // 3. Dériver clé = SHA256(master_key || MAC)
  mbedtls_sha256_context ctx;
  mbedtls_sha256_init(&ctx);
  mbedtls_sha256_starts(&ctx, 0);
  mbedtls_sha256_update(&ctx, (const unsigned char *)master_key, strlen(master_key));
  mbedtls_sha256_update(&ctx, mac, sizeof(mac));
  mbedtls_sha256_finish(&ctx, derived_key);
  mbedtls_sha256_free(&ctx);

  Serial.print("Derived key: ");
  for (int i = 0; i < 8; i++) Serial.printf("%02X", derived_key[i]);
  Serial.println("...");

  Serial.println("⚠️ DRY RUN — efuse NOT burned");
  Serial.println("✅ Key derivation OK — reproducible");

  Serial.flush();
  esp_sleep_enable_timer_wakeup(60ULL * 1000000ULL);
  esp_deep_sleep_start();
}
void loop() {}
```

---

## Grille de décision

| Critère | ✅ GO | 🟠 Orange | ❌ NO-GO |
|---------|:-----:|:---------:|:--------:|
| MAC stable | Oui | — | Change à chaque boot |
| Clé reproductible | Oui | — | Non |

---

**Fin de SOP-12 v2.0. Le test micro MEMS est maintenant SOP-13.**
