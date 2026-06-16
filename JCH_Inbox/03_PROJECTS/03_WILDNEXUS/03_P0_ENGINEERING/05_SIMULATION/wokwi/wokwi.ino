/**
 * WildNexus P0 — Smoke Test Firmware for Wokwi Simulation
 * 
 * Board: ESP32-S3-DevKitC-1 (ADR-001)
 * Purpose: Validate the core P0 logic loop in simulation
 * 
 * Hardware (matching diagram.json):
 *   - GPIO2  → LED IR (wokwi-led, red)
 *   - GPIO4  → PIR EKMB motion sensor (wokwi-pir-motion-sensor)
 *   - HSPI   → microSD (wokwi-microsd-card)
 *     - GPIO14 = SCK, GPIO12 = MISO, GPIO13 = MOSI, GPIO15 = CS
 * 
 * Behaviour:
 *   1. Boot → 3 fast LED blinks → init SD → log event
 *   2. Configure PIR wake-up on GPIO4
 *   3. Enter deep sleep (timer + PIR wake)
 *   4. Wake → log event → back to sleep
 */

#include "Arduino.h"
#include "FS.h"
#include "SD.h"
#include "SPI.h"

#define PIN_LED        2
#define PIN_PIR        4
#define PIN_SD_SCK    14
#define PIN_SD_MISO   12
#define PIN_SD_MOSI   13
#define PIN_SD_CS     15

#define DEEP_SLEEP_SEC  10   // Shorter for CI

RTC_DATA_ATTR uint32_t boot_count = 0;

void setup() {
    Serial.begin(115200);
    delay(200);

    boot_count++;
    esp_sleep_wakeup_cause_t wake_reason = esp_sleep_get_wakeup_cause();
    const char* event = (wake_reason == ESP_SLEEP_WAKEUP_EXT0) ? "WAKE_PIR" :
                        (boot_count == 1) ? "BOOT_COLD" : "WAKE_TIMER";

    Serial.printf("BOOT #%u | %s\n", boot_count, event);

    // LED boot blink
    pinMode(PIN_LED, OUTPUT);
    for (int i = 0; i < 3; i++) {
        digitalWrite(PIN_LED, HIGH);
        delay(50);
        digitalWrite(PIN_LED, LOW);
        delay(50);
    }
    Serial.println("LED:OK");

    // Init SD
    SPIClass sd_spi(HSPI);
    sd_spi.begin(PIN_SD_SCK, PIN_SD_MISO, PIN_SD_MOSI, PIN_SD_CS);
    if (SD.begin(PIN_SD_CS, sd_spi, 4000000)) {
        Serial.println("SD:OK");
        File f = SD.open("/wn_test.log", FILE_APPEND);
        if (f) {
            f.printf("boot#%u | %s\n", boot_count, event);
            f.close();
            Serial.println("LOG:OK");
        }
    } else {
        Serial.println("SD:FAIL");
    }

    // Configure wake sources and sleep
    pinMode(PIN_PIR, INPUT);
    esp_sleep_enable_ext0_wakeup((gpio_num_t)PIN_PIR, 1);
    esp_sleep_enable_timer_wakeup((uint64_t)DEEP_SLEEP_SEC * 1000000);

    Serial.printf("SLEEP %ds\n", DEEP_SLEEP_SEC);
    Serial.flush();
    delay(20);
    esp_deep_sleep_start();
}

void loop() {}
