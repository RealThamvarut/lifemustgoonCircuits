from serial_handler import ESP32,send_command, receive_data, close_serial
from databaseConnect import connectDB, getUser
from read_card import RC522CardReader
from led import Led
import time
import lgpio

if __name__ == "__main__":

    supabase = connectDB()
    print("esp32 test")
    esp32 = ESP32()
    print("esp32 passed!")
    card_reader = RC522CardReader()
    led = Led()


    CHIP = 0               # usually 0 on all Raspberry Pis
    PUMP_PIN = 5       # output
    BUTTON_PIN = 16       # GPIO number, not pin number

    h = lgpio.gpiochip_open(CHIP)
    lgpio.gpio_claim_output(h, PUMP_PIN)

    lgpio.gpio_claim_input(h, BUTTON_PIN)


    # Note: gpiod doesn't directly handle internal pull-up/pull-downs
    # You may need to enable them in /boot/config.txt using dtoverlay if needed:
    # e.g., "dtoverlay=gpio-pull,16,pull-down"

    print("Monitoring button on GPIO16...")


    try:
        while True:
            val = lgpio.gpio_read(h, BUTTON_PIN)
            if val:
                print("Button was pushed!")
            time.sleep(0.1)

            cardUID = card_reader.read_with_debounce()
            # print("Card UID:", card_reader.translate_uid(cardUID))
            if cardUID is not None :
                hexUID = card_reader.translate_uid(cardUID)
                if len(getUser(supabase, hexUID).data) != 0:
                    print(f"Found User: {hexUID}")
                    led.greenOn()

                    # command = input("Enter command (or 'exit' to quit): ").strip()
                    # if command.lower() == 'exit' or command.lower() == 'quit':
                    #     break

                    command = "activate"
                    # send_command(command)
                    # response = receive_data()
                    response = True

                    if response: 
                        lgpio.gpio_write(h, PUMP_PIN, 1)
                        time.sleep(5)
                        lgpio.gpio_write(h, PUMP_PIN, 0)



                    # if command == "getdata":
                    #     esp32.getSensor()
                    #     print("WaterLevel: ", esp32.waterLevel)
                    #     print("Temperature: ", esp32.temperature)
                    #     print("Weight", esp32.weight)
                    led.greenOff()
                else:
                    print(f"User {hexUID} not found")
                    led.redOn()
            # else:
            #     print("Invalid user")
    finally:
        close_serial()
        led.setLed("red", 0)
        led.setLed("yellow", 0)
        led.setLed("green", 0)
        print("Connection closed!")
