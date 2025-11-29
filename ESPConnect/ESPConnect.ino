#include "UltraSonic.h"
#include "PiezoWeight.h"
#include "Temperature.h"
#include "Utils.h"
#include "MQTT.h"
#include <math.h>
#include <Arduino.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <WiFi.h>

#define SSID "Thamva-router"
#define PASSWORD "<thamva12345>"

// MQTT Broker details
#define MQTT_SERVER "mqtt3.thingspeak.com"
#define MQTT_PORT 1883
#define MQTT_USER "LwEPGy4rLh4tMhMDLQwgBwc"
#define MQTT_PASSWORD "/dhZK/IMhUvop5mPCqhQqm4h"
#define MQTT_CLIENT_ID "LwEPGy4rLh4tMhMDLQwgBwc"
#define MQTT_TOPIC_WATER_LEVEL "channels/3184682/publish"
#define MQTT_TOPIC_TEMPERATURE "channels/3185470/publish"

#define RX1 44
#define TX1 43

// Define I2C pins
#define SDA_PIN  8
#define SCL_PIN  9

// Define Weight pin
#define W_PIN 18

// Define Temp pin
#define T_PIN 16

UltraSonic sonar(37, 36); // trig=37, echo=36
PiezoWeight wieghtSensor(W_PIN);
Temperature temp(T_PIN, DHT22);
LiquidCrystal_I2C lcd(0x27, 16, 2);
MQTT mqtt(MQTT_SERVER, MQTT_PORT, MQTT_USER, MQTT_PASSWORD, MQTT_CLIENT_ID);

void setup()
{
  Serial.begin(9600);

  connectWiFi(SSID, PASSWORD);
  mqtt.setup();

  // UART
  Serial2.begin(115200, SERIAL_8N1, RX1, TX1);
  
  Wire.begin(SDA_PIN, SCL_PIN); 
  
  lcd.init();                     
  lcd.backlight();
  lcd.clear();

  pinMode(W_PIN, INPUT);
  temp.begin();
}

void loop()
{
  mqtt.loop();
  float dist = sonar.readDistance();
  float weight = analogRead(W_PIN);
  float celcius = temp.getTemperature();

  dist = (16 - dist) / 0.16;
  if(dist < 0) dist = 0;
  dist = round(dist);

  // Log
  
  // lcd.clear();
  // lcd.setCursor(0,0); 
  // lcd.print("Press the button");
  // lcd.setCursor(0,1);
  // lcd.print("or tab the card");
  lcd.setCursor(0,0);
  lcd.print("Wight");
  lcd.setCursor(0,1);
  lcd.print(weight);
  // Serial2.println(weight);

  // Serial2.print("Distance: ");
  // Serial2.println(dist);
  //
  // Serial2.print("Temp: ");
  // Serial2.println(celcius);
  //
  // Serial2.print("Pressure: ");
  // Serial2.println(weight);
  //
  // Serial2.println("-----------------------------------");
  
  //
  //  end of log
  
  mqtt.publish(MQTT_TOPIC_WATER_LEVEL, dist);
  mqtt.publish(MQTT_TOPIC_TEMPERATURE, celcius);

  String message = "";

  if (Serial2.available() > 0)
  {
    String command = Serial2.readStringUntil('\n');
    command.trim();

    String prefix = "activate:";
    if (command.startsWith(prefix)) 
    {
      String valueString = command.substring(prefix.length());
        
      int value = valueString.toInt();

      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Place your cup!");
      
      bool isVibration = waitForTrigger(W_PIN, 5000, value);
      lcd.clear();
      if (isVibration){

        lcd.setCursor(0,0); 
        lcd.print("Pumping");

        unsigned long startTime = millis();
        while ((millis() - startTime) < 5000) {}

        Serial2.println(true);
        // Serial2.println("PUMP active: " + String(weight));
        lcd.clear();
      }
      else{
        Serial2.println(false);
        // Serial2.println("PUMP not active: " + String(weight));
      }

      weight = 0;
    }
    else if (command == "invaliduser"){
      lcd.clear();
      lcd.setCursor(0,0); 
      lcd.print("Invalid User");
      delay(2000);
    }
    // else if (command == "getdata")
    // {
    //   dist = sonar.readDistance();
    //   weight = analogRead(W_PIN);
    //   celcius = temp.getTemperature();
    //
    //   message = String(dist) + ";" + String(celcius) + ";" + String(weight);
    //   Serial2.println(message);
    // }
    else if (command == "");
    else
    {
      Serial2.println("Unknown command bro: " + command);
    }
  }
}
