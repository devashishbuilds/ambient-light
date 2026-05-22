#include <FastLED.h>

#define LED_PIN 2         // GPIO 8 on ESP32-C3 (confirm your wiring)
#define NUM_LEDS 54        // Number of LEDs
#define BRIGHTNESS 255    // LED brightness

CRGB leds[NUM_LEDS];

void setup() {
  // Important for ESP32: delay before starting Serial
  delay(500);            
  Serial.begin(115200);  // ESP32 typically uses 115200 or higher
  FastLED.addLeds<WS2811, LED_PIN, RGB>(leds, NUM_LEDS);
  FastLED.setBrightness(BRIGHTNESS);
}
void loop() {
  const int bytesNeeded = NUM_LEDS * 3;
  if (Serial.available() >= bytesNeeded) {
    for (int i = 0; i < NUM_LEDS; i++) {
      byte r = Serial.read();
      byte g = Serial.read();
      byte b = Serial.read();
      leds[i] = CRGB(r, g, b);
    }
    FastLED.show();
  }
}
