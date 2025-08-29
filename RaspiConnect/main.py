from serial_handler import ESP32,send_command, receive_data, close_serial
from databaseConnect import connectDB, getUser
from read_card import RC522CardReader


if __name__ == "__main__":

    # connectDB()
    supabase = connectDB()
    esp32 = ESP32()
    card_reader = RC522CardReader()

    while True:

        cardUID = card_reader.read_with_debounce()
        # print("Card UID:", card_reader.translate_uid(cardUID))
        if cardUID is not None :
            hexUID = card_reader.translate_uid(cardUID)
            if len(getUser(supabase, hexUID).data) != 0:
                print(f"Found User: {hexUID}")
                # command = input("Enter command (or 'exit' to quit): ").strip()
                # if command.lower() == 'exit' or command.lower() == 'quit':
                #     break

                command = "activate"
                send_command(command)
                response = receive_data()

                if command == "getdata":
                    esp32.getSensor()
                    print("WaterLevel: ", esp32.waterLevel)
                    print("Temperature: ", esp32.temperature)
                    print("Weight", esp32.weight)
            else:
                print(f"User {hexUID} not found")
        else:
            print("Invalid user")

    
    close_serial()
    print("Connection closed!")
