#include "PiezoWeight.h"

PiezoWeight::PiezoWeight(int pin)
{
    pinMode(pin, INPUT);
}

int PiezoWeight::readWeight()
{
    int value = analogRead(pin);
    return value;
}