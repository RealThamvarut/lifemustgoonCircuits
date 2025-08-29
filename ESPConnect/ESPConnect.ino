#include "AirSensor.h"
#include "UltraSonic.h"
#include "PiezoWeight.h"
#include <math.h>

// #define RX1 44
// #define TX1 43
#define pumpPin 5

AirSensor air;
UltraSonic sonar(37, 36); // trig=37, echo=36
PiezoWeight wieghtSensor(15);


void setup()
{
  // Log
  Serial.begin(9600);
  // UART
  Serial2.begin(115200, SERIAL_8N1, 44, 43);

  if (!air.begin())
  {
    Serial.println("BME280 not found!");
  }
  else
  {
    Serial.println("BME280 initialized");
  }

  pinMode(pumpPin, OUTPUT); // set water-pump trigger
  pinMode(15, INPUT);
  Serial.println("Serial begin...");
  // Serial2.println("Hello from ESP32");
}

float getWaterLevel(float distance, float radius = 4.5, float tankHeight = 16.5)
{
  return M_PI * pow(radius, 2) * (tankHeight - distance);
}

void loop()
{
  float dist = sonar.readDistance();
  float temp = air.readTemperature();
  float pressure = air.readPressure();
  float humid = air.readHumidity();
  // float weight = wieghtSensor.readWeight();
  float weight = analogRead(15);
  // Log
  // Serial.print("Distance: ");
  // Serial.println(dist);s

  // Serial.print("Temp: ");
  // Serial.println(temp);

  // Serial.print("Pressure: ");
  // Serial.println(pressure);

  // Serial.print("Humid: ");
  // Serial.println(humid);

  // Serial.println("-----------------------------------");
  //  end of log
  String message = "";

  while (Serial2.available() > 0)
  {
    String command = Serial2.readStringUntil('\n');
    command.trim();
    Serial.print("Receive data from RASPI: ");
    Serial.println(command);
    if (command == "activate")
    {
      unsigned long startTime = millis();
      bool isVibration = false;
      while ((millis() - startTime) < 5000) {
        weight = analogRead(15);
        if (weight >= 2000){
          isVibration = true;
          break;
        }
      }

      if (isVibration){
        digitalWrite(pumpPin, HIGH);

        unsigned long startTime = millis();
        while ((millis() - startTime) < 5000) {}

        Serial2.println("PUMP active: " + String(weight));
        digitalWrite(pumpPin, LOW);
      }
      else{
        Serial2.println("PUMP not active: " + String(weight));
      }

      weight = 0;
    }
    else if (command == "deactivate")
    {
      digitalWrite(pumpPin, LOW);
      Serial2.println("PUMP OFF");
    }
    else if (command == "getdata")
    {
      dist = sonar.readDistance();
      // float currentWaterLevel = getWaterLevel(dist);
      temp = air.readTemperature();
      pressure = air.readPressure();
      humid = air.readHumidity();
      weight = analogRead(15);

      message = String(dist) + ";" + String(temp) + ";" + String(weight);
      Serial2.println(message);
    }
    else
    {
      Serial2.println("Unknown command bro: " + command);
    }
  }
}