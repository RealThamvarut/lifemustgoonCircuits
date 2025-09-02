#include "UltraSonic.h"
#include "PiezoWeight.h"
#include "Temperature.h"
#include <math.h>
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

// #define RX1 44
// #define TX1 43
#define pumpPin 5

// Define I2C pins
#define SDA_PIN  8 
#define SCL_PIN  9 

UltraSonic sonar(37, 36); // trig=37, echo=36
PiezoWeight wieghtSensor(15);
Temperature temp(16, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
  // Log
  Serial.begin(9600);
  // UART
  Serial2.begin(115200, SERIAL_8N1, 44, 43);
  
  Wire.begin(SDA_PIN, SCL_PIN); 
  lcd.init();                     
  lcd.backlight();
  lcd.clear();
  

  pinMode(pumpPin, OUTPUT); // set water-pump trigger
  pinMode(15, INPUT);
  temp.begin();
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
  // float weight = wieghtSensor.readWeight();
  float weight = analogRead(15);
  float celcius = temp.getTemperature();
  dist = (16 - dist) / 0.16;
  if(dist < 0) dist = 0;
  dist = round(dist);
  // lcd.clear();
  lcd.setCursor(0,0); 
  lcd.print("Water Lv:" + String(dist) + "% ");
  lcd.setCursor(0,1); 
  lcd.print("Temp:" + String(celcius) + " C ");

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
      lcd.clear();
      dist = sonar.readDistance();
      // float currentWaterLevel = getWaterLevel(dist);
      weight = analogRead(15);
      celcius = temp.getTemperature();

      message = String(dist) + ";" + String(celcius) + ";" + String(weight);
      Serial2.println(message);
    }
    else if (command == "");
    else
    {
      Serial2.println("Unknown command bro: " + command);
    }
  }
}