#ifndef ULTRASONIC_H
#define ULTRASONIC_H

#include <Arduino.h>

class UltraSonic {
  public:
    UltraSonic(int trigPin, int echoPin);
    int readDistance();
  private:
    int trigPin;
    int echoPin;
};

#endif
