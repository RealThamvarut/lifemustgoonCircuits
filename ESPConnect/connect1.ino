#include "AirSensor.h"
#include "UltraSonic.h"
#include "PiezoWeight.h"

// #define RX1 44
// #define TX1 43
#define pumpPin 5

AirSensor air;
UltraSonic sonar(37, 36); // trig=37, echo=36
// PiezoWeight wieghtSensor(pin)

void setup()
{
  // Log
  Serial.begin(115200);
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
  Serial.println("Serial begin...");
  // Serial2.println("Hello from ESP32");
}

void loop()
{
  float dist = sonar.readDistance();
  float temp = air.readTemperature();
  float pressure = air.readPressure();
  float humid = air.readHumidity();
  // Log
  // Serial.print("Distance: ");
  // Serial.println(dist);

  // Serial.print("Temp: ");
  // Serial.println(temp);

  // Serial.print("Pressure: ");
  // Serial.println(pressure);

  // Serial.print("Humid: ");
  // Serial.println(humid);

  // Serial.println("-----------------------------------");
  //  end of log
  String message = "";
  // message = "Dist: " + String(dist) + ";" + "Temp: " +String(temp);
  // Serial2.println(message);

  while (Serial2.available() > 0)
  {
    String command = Serial2.readStringUntil('\n');
    command.trim();
    Serial.print("Receive data from RASPI: ");
    Serial.println(command);
    if (command == "activate")
    {
      digitalWrite(pumpPin, HIGH);
      Serial2.println("PUMP ON");
    }
    else if (command == "deactivate")
    {
      digitalWrite(pumpPin, LOW);
      Serial2.println("PUMP OFF");
    }
    else if (command == "getdata")
    {
      dist = sonar.readDistance();
      temp = air.readTemperature();
      pressure = air.readPressure();
      humid = air.readHumidity();
      message = String(dist) + ";" + String(temp);
      Serial2.println(message);
    }
    else
    {
      Serial2.println("Unknown command bro: " + command);
    }
  }
}