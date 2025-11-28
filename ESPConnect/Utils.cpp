#include "Utils.h"
#include <Arduino.h>

void connectWiFi(const char* ssid, const char* password) {
  WiFi.mode(WIFI_STA); //Optional
  WiFi.begin(ssid, password);
  Serial2.println("\nConnecting");

  while(WiFi.status() != WL_CONNECTED){
      Serial.print(".");
      delay(100);
  }

  Serial2.println("\nConnected to the WiFi network");
  Serial2.print("Local ESP32 IP: ");
  Serial2.println(WiFi.localIP());

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
