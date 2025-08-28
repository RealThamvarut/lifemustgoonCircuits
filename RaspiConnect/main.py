from serial_handler import send_command, receive_data, close_serial

if __name__ == "__main__":
    
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit' or command.lower() == 'quit':
            break

        send_command(command)
        response = receive_data()
        if command == "getdata":

            if response:
                print(f"Response: {response}")
            else :
                print("No response received.")

            responseList = response.split(";")
            waterLevel = responseList[0]
            temperature = responseList[1]

            print("WaterLevel: ", waterLevel)
            print("Temperature: ", temperature)

    close_serial()
    print("Connection closed!")
