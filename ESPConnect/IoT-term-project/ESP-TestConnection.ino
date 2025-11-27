#include <Arduino.h>

void setup()
{
    // Log
    Serial1.begin(9600);
    Serial1.println("Serial begin...");
    
    // UART
    Serial2.begin(115200, SERIAL_8N1, 44, 43);
    // Serial2.println("Hello from ESP32");
}

void loop()
{
    // listen every loop
    // if(Serial2.available()){
    //     String input = Serial2.readStringUntil('\n');
    //      input.trim();
    //     // Print Log to Serial1
    //     Serial1.print("Receive data from RASPI: ");
    //     Serial1.println(input);
    // }

    // always listening
    while (Serial2.available() > 0)
    {
        String input = Serial2.readStringUntil('\n');
        input.trim();
        // Print Log to Serial1
        Serial1.print("Received data from RP5: ");
        Serial1.println(input);

        // Extract link from
    }
}