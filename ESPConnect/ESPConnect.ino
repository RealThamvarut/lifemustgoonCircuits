#include "UltraSonic.h"
#include "PiezoWeight.h"
#include "Temperature.h"
#include "Utils.h"
#include <math.h>
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

#define SSID "thamva_router"
#define PASSWORD ""

#define RX1 44
#define TX1 43

// Define Pump pin
// #define pumpPin 5


// Define I2C pins
#define SDA_PIN  8
#define SCL_PIN  9

// Define Weight pin
#define W_PIN 15

// Define Temp pin
#define T_PIN 16

UltraSonic sonar(37, 36); // trig=37, echo=36
PiezoWeight wieghtSensor(W_PIN);
Temperature temp(T_PIN, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup()
{
  Serial.begin(9600);

  connectWiFi(SSID, PASSWORD);

  // UART
  Serial2.begin(115200, SERIAL_8N1, RX1, TX1);
  
  Wire.begin(SDA_PIN, SCL_PIN); 
  
  lcd.init();                     
  lcd.backlight();
  lcd.clear();

  // pinMode(pumpPin, OUTPUT); // set water-pump trigger
  pinMode(W_PIN, INPUT);
  temp.begin();
  Serial.println("Serial begin...");
  // Serial2.println("Hello from ESP32");
}

void loop()
{
  float dist = sonar.readDistance();
  float weight = analogRead(W_PIN);
  float celcius = temp.getTemperature();

  dist = (16 - dist) / 0.16;
  if(dist < 0) dist = 0;
  dist = round(dist);

  // lcd.clear();
  // lcd.setCursor(0,0); 
  // lcd.print("Water Lv:" + String(dist) + "%   ");
  // lcd.setCursor(0,1); 
  // lcd.print("Temp:" + String(celcius) + " C   ");

  // Log
  // Serial.print("Distance: ");
  // Serial.println(dist);
  //
  // Serial.print("Temp: ");
  // Serial.println(celcius);
  //
  // Serial.print("Pressure: ");
  // Serial.println(weight);
  //
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
      // lcd.clear();
      // lcd.setCursor(0,0); 
      // lcd.print("Place your cup!");
      
      bool isVibration = waitForTrigger(W_PIN, 5000, 2000);
      // lcd.clear();
      if (isVibration){

        // lcd.setCursor(0,0); 
        // lcd.print("Pumping");
        // digitalWrite(pumpPin, HIGH);

        unsigned long startTime = millis();
        while ((millis() - startTime) < 5000) {}

        Serial2.println("PUMP active: " + String(weight));
        // digitalWrite(pumpPin, LOW);
        // lcd.clear();
      }
      else{
        Serial2.println("PUMP not active: " + String(weight));
      }

      weight = 0;
    }
    else if (command == "deactivate")
    {
      // digitalWrite(pumpPin, LOW);
      Serial2.println("PUMP OFF");
    }
    else if (command == "getdata")
    {
      dist = sonar.readDistance();
      weight = analogRead(W_PIN);
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
