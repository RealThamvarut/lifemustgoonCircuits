from serial_handler import ESP32,send_command, receive_data, close_serial
from databaseConnect import connectDB, getUser
from read_card import RC522CardReader
from flaskWebServer import start_camera, stop_camera, create_app
from thingSpeakConnect import send_to_thingspeak
from led import Led
import time
import lgpio
import requests
import threading


def run_flask(app):
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
    
def safe_init_esp32(retries=5):
    # Try to create ESP32 object safely without crashing program
    for i in range(retries):
        try:
            print(f"Initializing ESP32... Attempt {i+1}/{retries}")
            return ESP32()
        except Exception as e:
            print("ESP32 init failed:", e)
            time.sleep(1)
    print("⚠ ESP32 could not be initialized; continuing without it.")
    return None

if __name__ == "__main__":
    
    supabase = connectDB()
    print("esp32 test")
    esp32 = safe_init_esp32()
    print("esp32 passed!")
    card_reader = RC522CardReader()
    led = Led()


    CHIP = 0               # usually 0 on all Raspberry Pis
    BUTTON_PIN = 16       # GPIO number, not pin number

    h = lgpio.gpiochip_open(CHIP)
    lgpio.gpio_claim_input(h, BUTTON_PIN)


    # Note: gpiod doesn't directly handle internal pull-up/pull-downs
    # You may need to enable them in /boot/config.txt using dtoverlay if needed:
    # e.g., "dtoverlay=gpio-pull,16,pull-down"

    print("Monitoring button on GPIO16...")
    
    # Start camera + Flask server in background
    start_camera()
    app = create_app()

    flask_thread = threading.Thread(target=run_flask, args=(app,), daemon=True)
    flask_thread.start()

    print("Flask web server started in background thread.")

    try:
        while True:
            cardUID = card_reader.read_with_debounce()
            # print("Card UID:", card_reader.translate_uid(cardUID))
            if cardUID is not None :
                hexUID = card_reader.translate_uid(cardUID)
                # if len(getUser(supabase, hexUID).data) != 0:
                if True:
                    print(f"Found User: {hexUID}")
                    led.greenOn()
                    # send to MQTT
                    send_to_thingspeak(hexUID)

                    # command = input("Enter command (or 'exit' to quit): ").strip()
                    # if command.lower() == 'exit' or command.lower() == 'quit':
                    #     break

                    # # command = "activate"
                    # # send_command(command)
                    # # response = receive_data()


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
            
            # For non-subscriber play an ad
            val = lgpio.gpio_read(h, BUTTON_PIN)
            # print("Button:", val)   # DEBUG — SEE IF BUTTON WORKS
            if val:
                print("Button was pushed!")
                try:
                    r = requests.post("http://127.0.0.1:5000/trigger_ad")
                    print("Trigger response:", r.text)
                except Exception as e:
                    print("Failed to trigger ad:", e)

                time.sleep(1)  # debounce

            time.sleep(0.05)
            
    finally:
        close_serial()
        led.setLed("red", 0)
        led.setLed("yellow", 0)
        led.setLed("green", 0)
        print("Connection closed!")
