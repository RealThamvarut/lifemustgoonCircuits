from serial_handler import ESP32,send_command, receive_data, close_serial
from databaseConnect import connectDB, getUser


if __name__ == "__main__":

    # connectDB()
    supabase = connectDB()
    esp32 = ESP32()
    
    while True:
        # UIDCard = getUID() # TODO

        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit' or command.lower() == 'quit':
            break

        send_command(command)
        response = receive_data()

        if command == "getdata":
            esp32.getSensor()
            print("WaterLevel: ", esp32.waterLevel)
            print("Temperature: ", esp32.temperature)
            print("Weight", esp32.weight)

    close_serial()
    print("Connection closed!")
