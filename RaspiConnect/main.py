from serial_handler import ESP32, send_command, receive_data, close_serial
from databaseConnect import connectDB, getUser
from read_card import RC522CardReader
from flaskWebServer import start_camera, stop_camera, get_video_duration_opencv, create_app
from thingSpeakConnect import send_to_thingspeak
from led import Led
import time
import lgpio
import requests
import threading

def run_flask(app):
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

def safe_init_esp32(retries=5, delay=1):
    for i in range(retries):
        try:
            print(f"Initializing ESP32... Attempt {i+1}/{retries}")
            esp = ESP32()
            print("ESP32 initialized successfully.")
            return esp
        except Exception as e:
            print(f"ESP32 init failed on attempt {i+1}: {e}")
            if i < retries - 1:
                print(f"Retrying in {delay} second(s)...")
                time.sleep(delay)
    print("⚠ ESP32 could not be initialized; continuing without it.")
    return None

def activate_pump(delay=5):
    print("Activating pump.")
    lgpio.gpio_write(h, PUMP_PIN, 1)
    time.sleep(delay)
    lgpio.gpio_write(h, PUMP_PIN, 0)

if __name__ == "__main__":
    supabase = connectDB()
    esp32 = safe_init_esp32()
    card_reader = RC522CardReader()
    led = Led()

    CHIP = 0
    PUMP_PIN = 5
    BUTTON_PIN = 16

    h = None
    try:
        h = lgpio.gpiochip_open(CHIP)
        lgpio.gpio_claim_output(h, PUMP_PIN)
        lgpio.gpio_claim_input(h, BUTTON_PIN)
        print("GPIO initialized for pump and button.")
    except Exception as e:
        print(f"FATAL: Failed to initialize GPIO: {e}. Exiting.")
        led.cleanup()
        exit()

    # Start Background Camera and Web Server
    start_camera()
    app = create_app()
    flask_thread = threading.Thread(target=run_flask, args=(app,), daemon=True)
    flask_thread.start()
    print("Flask web server started in background thread on http://0.0.0.0:5000")
    print("Monitoring button on GPIO16 and waiting for card scans...")

    try:
        while True:
            print("1", end="")
            cardUID = card_reader.read_with_debounce()
            if cardUID is not None:
                # print(f"2")
                hexUID = card_reader.translate_uid(cardUID)
                user_data = getUser(supabase, hexUID)
                # print(f"3")
                if len(user_data.data) != 0:
                    print(f"Found User (Subscriber): {hexUID}")
                    led.greenOn()
                    
                    send_to_thingspeak(hexUID)

                    command = "activate:3000"
                    response = None
                    if esp32:
                        try:
                            send_command(command)
                            response = receive_data()
                            print("Log from ESP32:", response)
                        except Exception as e:
                            print(f"Error communicating with ESP32: {e}")
                    
                    if response == "1" or not esp32:
                        activate_pump(5)
                    time.sleep(1)
                    led.greenOff()
                else:
                    print(f"User {hexUID} not found (Non-subscriber)")
                    try:
                        send_command("invaliduser")
                    except Exception as e:
                        print(f"Error communicating with ESP32: {e}")
                    led.redOn(delay=2)
            if lgpio.gpio_read(h, BUTTON_PIN):
                print("Button was pushed! Triggering ad.")
                try:
                    r = requests.post("http://127.0.0.1:5000/trigger_ad")
                    print("Ad trigger response:", r.text)
                    time.sleep(float(get_video_duration_opencv()))
                except requests.exceptions.RequestException as e:
                    print(f"Failed to trigger ad: Could not connect to web server. {e}")
                time.sleep(0.5)  # Debounce for button

            time.sleep(0.1)

    finally:
        print("\nCleaning up and shutting down...")
        if esp32:
            close_serial()
        stop_camera()
        led.cleanup()
        if h:
            lgpio.gpio_write(h, PUMP_PIN, 0)
            lgpio.gpiochip_close(h)
            print("Main GPIO resources released.")
        print("Cleanup complete. Goodbye!")
