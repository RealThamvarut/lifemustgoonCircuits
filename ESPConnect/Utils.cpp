#include "Utils.h"
#include <Arduino.h>

void connectWiFi(const char* ssid, const char* password) {
    Serial.print("Connecting to WiFi: ");
    WiFi.begin(ssid, password);
    Serial.println("WiFi connected");
}

bool waitForTrigger(int pin, int timeout, int threshold) {
    unsigned long startTime = millis();
    while ((millis() - startTime) < timeout) {
        if (analogRead(pin) >= threshold) {
            return true;
        }
    }
    return false;
}
