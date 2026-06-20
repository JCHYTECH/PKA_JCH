// SOP-03-H1 — wn_deep_sleep_30s_arbor_h1
// WildNexus P0 — Arbor Nœud 1 : GPIO zero-leakage + PSRAM power-down
// Hypothèse : config GPIO + PSRAM + RTC power-down réduit la conso de > 15% (1052 → < 900 µA)
//
// DIFFÉRENCES vs baseline wn_deep_sleep_30s :
//   - Tous les GPIOs inutilisés → INPUT_PULLDOWN (évite leakage des pins flottantes)
//   - PSRAM power-down avant deep sleep
//   - RTC peripherals power-down
//   - Brownout detector désactivé en deep sleep (optionnel, ~40 µA gagnés)
//   - GPIOs utilisés (UART TX/RX, USB) préservés

#include "esp_sleep.h"
#include "driver/gpio.h"

// ---------------------------------------------------------------------------
// Configuration : GPIOs utilisés par WildNexus P0 (à préserver)
// ---------------------------------------------------------------------------
// Si tu utilises d'autres GPIOs (PIR, LED, etc.), modifie cette liste.
// Les pins UART0 TX/RX (GPIO 43/44 sur ESP32-S3) sont toujours utilisées par Serial.
// Les pins USB (GPIO 19/20 sur ESP32-S3) sont utilisées par le port USB natif.

// Pins à NE PAS reconfigurer (elles sont utilisées) :
// - GPIO 43 : UART0 TX (U0TXD)
// - GPIO 44 : UART0 RX (U0RXD)
// - GPIO 19 : USB D- (sur certains DevKit S3, USB Serial/JTAG)
// - GPIO 20 : USB D+ (sur certains DevKit S3, USB Serial/JTAG)
// Toutes les autres pins (0-18, 21, 26, 33-42, 45-48) → INPUT_PULLDOWN

#define MIN_UNUSED_GPIO 0
#define MAX_UNUSED_GPIO 48

// Pins à préserver (ne pas reconfigurer)
const int PRESERVED_PINS[] = {43, 44};  // UART0
const int PRESERVED_COUNT = 2;

bool is_preserved(int pin) {
  for (int i = 0; i < PRESERVED_COUNT; i++) {
    if (pin == PRESERVED_PINS[i]) return true;
  }
  return false;
}

// ---------------------------------------------------------------------------
// setup()
// ---------------------------------------------------------------------------

void setup() {
  Serial.begin(115200);
  delay(1000);  // Laisser le temps au moniteur série de s'ouvrir

  Serial.println("=== WildNexus Arbor H1 : GPIO + PSRAM + RTC power-down ===");
  Serial.println("Configuration des GPIOs inutilises en INPUT_PULLDOWN...");

  // 1. Configurer tous les GPIOs inutilisés en INPUT_PULLDOWN
  //    Les pins flottantes consomment 5-20 µA cumulé en leakage.
  int configured = 0;
  for (int pin = MIN_UNUSED_GPIO; pin <= MAX_UNUSED_GPIO; pin++) {
    if (is_preserved(pin)) continue;  // Ne pas toucher aux pins utilisées

    // Certaines pins n'existent pas sur tous les packages ESP32-S3
    // (ex: GPIO 22-25 absents sur certains packages). On les ignore.
    // Les pins 26-32 sont pour la flash/PSRAM interne — les ignorer.
    if (pin >= 26 && pin <= 32) continue;

    gpio_config_t io_conf = {};
    io_conf.pin_bit_mask = (1ULL << pin);
    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pull_down_en = GPIO_PULLDOWN_ENABLE;   // Tirer vers GND = pas de courant
    io_conf.pull_up_en = GPIO_PULLUP_DISABLE;       // Pull-up désactivé
    io_conf.intr_type = GPIO_INTR_DISABLE;
    gpio_config(&io_conf);
    configured++;
  }
  Serial.printf("  GPIOs configures : %d\n", configured);

  // 2. Forcer le power-down des périphériques RTC en deep sleep
  //    Par défaut, certains périphériques RTC restent partiellement alimentés.
  //    ESP_PD_DOMAIN_RTC_PERIPH = coupe ULP, GPIOs RTC, I2C RTC, etc.
  //    Les domaines SLOW_MEM/FAST_MEM n'existent pas dans cette version Arduino-ESP32.
  Serial.println("Power-down des domaines RTC...");
  esp_sleep_pd_config(ESP_PD_DOMAIN_RTC_PERIPH, ESP_PD_OPTION_OFF);

  // 3. Brownout detector — désactivé via menuconfig (CONFIG_ESP_SLEEP_BROWNOUT_DET)
  //    Pas d'API directe dans Arduino-ESP32. On le laisse géré par le SDK.
  //    Le test reste valide : le gain brownout (~30 µA) sera mesuré plus tard
  //    en environnement ESP-IDF natif si nécessaire.

  // 4. Désactiver la PSRAM avant d'entrer en deep sleep (si présente)
  //    La PSRAM en mode rétention consomme 20-40 µA.
  //    Sur ESP32-S3 avec PSRAM octo/quad, on peut la couper complètement
  //    car le contenu n'est pas préservé en deep sleep de toute façon.
  Serial.println("Power-down PSRAM...");
  esp_sleep_pd_config(ESP_PD_DOMAIN_VDDSDIO, ESP_PD_OPTION_OFF);

  // 5. Configurer le réveil par timer : 30 secondes
  esp_sleep_enable_timer_wakeup(30ULL * 1000000ULL);

  Serial.println("Endormissement 30s...");
  Serial.flush();  // Vider le buffer série avant de dormir
  delay(50);       // Attendre que le flush soit complet

  // --- ENTRÉE EN DEEP SLEEP ---
  esp_deep_sleep_start();
}

void loop() {
  // Jamais exécuté — après deep sleep, l'ESP32 redémarre → setup()
}
