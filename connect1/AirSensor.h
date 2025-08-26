#ifndef AIRSENSOR_H
#define AIRSENSOR_H

#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>

class AirSensor {
  public:
    AirSensor();
    bool begin(uint8_t addr = 0x76);
    float readTemperature();
    float readPressure();
    float readHumidity();
  private:
    Adafruit_BME280 bme;
};

#endif
