#ifndef TEMPERATURE_H
#define TEMPERATURE_H

#include <Arduino.h>
#include <DHT.h>

class Temperature {
  private:
    uint8_t pin;
    uint8_t type;
    DHT dht;

  public:
    Temperature(uint8_t pin, uint8_t type = DHT22);

    void begin();
    float getTemperature();
};

#endif