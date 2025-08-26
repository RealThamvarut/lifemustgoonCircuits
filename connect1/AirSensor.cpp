#include "AirSensor.h"

AirSensor::AirSensor() {}

bool AirSensor::begin(uint8_t addr) {
  return bme.begin(addr);
}

float AirSensor::readTemperature() {
  return bme.readTemperature();
}

float AirSensor::readPressure() {
  return bme.readPressure() / 100.0F;
} 

float AirSensor::readHumidity() {
  return bme.readHumidity();
}
