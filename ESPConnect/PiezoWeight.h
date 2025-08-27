#ifndef PIEZOWEIGHT_H
#define PIEZOWEIGHT_H

#include <Arduino.h>

class PiezoWeight
{
public:
    PiezoWeight(int pin);
    int readWeight();

private:
    int pin;
};