#include <Adafruit_Sensor.h>
#include <Adafruit_BME280.h>
#include <Arduino.h>

// defines pins numbers
const int UltraSonicTrigPin = 37;
const int UltraSonicEchoPin = 36;

long duration;
int distance;

// Air Measure
Adafruit_BME280 bme; // I2C

void initAirSensor(Adafruit_BME280 &bme)

{
  bool status;
  status = bme.begin(0x76);
  if (!status)
  {
    Serial.println("Could not find a valid BME280 sensor, check wiring!");
    // while (1);
  }
}

void setup() {
  Serial1.begin(115200, SERIAL_8N1, 44, 43);  // Set baud rate, must be the same as in Raspberry Pi
  Serial.begin(115200);                       // Starts the serial communication

  pinMode(UltraSonicTrigPin, OUTPUT);  // Sets the trigPin as an Output
  pinMode(UltraSonicEchoPin, INPUT);   // Sets the echoPin as an Input


  Serial1.println("ESP32 Ready...");
  initAirSensor(bme);

  pinMode(5, OUTPUT);
}

void loop() {
  Serial.println("xD1");
  String message = "";
  digitalWrite(UltraSonicTrigPin, LOW);
  delayMicroseconds(1000000);
  


  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(UltraSonicTrigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(UltraSonicTrigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(UltraSonicEchoPin, HIGH);

  // Calculating the distance
  distance = duration * 0.034 / 2;
  Serial.println("xD2");
  // message += (distance);

  if (Serial1.available()) {
    Serial1.println("xD3");
    Serial1.println(String(distance));
    String command = Serial1.readStringUntil('\n'); // read until \n
    command.trim(); // remove space

    if (command == "status") {
    } else if (command == "blink") {
      for(int i=0; i<3; i++) {
        digitalWrite(5, HIGH); // If we connect LED on pin 2 of ESP32
        delay(200);
        digitalWrite(5, LOW);
        delay(200);
      }
    } else {
      Serial1.println("Unknown command: " + command);
    }
  } else {
    Serial1.println("Serial 1 not available");
  }
}