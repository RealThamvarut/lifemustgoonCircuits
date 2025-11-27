#ifndef UTILS_H
#define UTILS_H

#include <WiFi.h>

void connectWiFi(const char* ssid, const char* password);
bool waitForTrigger(int pin, int timeout, int threshold);

#endif
