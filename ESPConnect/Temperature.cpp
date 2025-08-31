#include "Temperature.h"

Temperature::Temperature(uint8_t pin, uint8_t type)
  : pin(pin), type(type), dht(pin, type) {}

void Temperature::begin() {
  dht.begin();
}

float Temperature::getTemperature() {
  return dht.readTemperature();
}