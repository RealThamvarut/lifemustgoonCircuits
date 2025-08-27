import serial
import time

from supabase import create_client, Client

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)

url: str = "https://iafczodqvfosapepeinj.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImlhZmN6b2RxdmZvc2FwZXBlaW5qIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1NjEzMDQ4MywiZXhwIjoyMDcxNzA2NDgzfQ.HfI10kvj1cUUX-Ilp785J5QXyVnSo_A1P5p1UFA8O6I"
supabase: Client = create_client(url, key)

# cardID = "FA42F380"
def send_command(cmd):
    if not cmd:
        return
    try:
        ser.write((cmd + '\n').encode()) # ส่งคำสั่งพร้อมขึ้นบรรทัดใหม่
        print(f"Send command: {cmd}")

    except serial.SerialException as e:
        print(f"Nah uh something failed: {e}")

def receive_data():
    try:
        time.sleep(0.5)
        line = ser.readline().decode('utf-8').strip()  
        while line == "":
            line = ser.readline().decode('utf-8').strip()
        
        # print(f"Receive from ESP32: {line}")
        return line
    except serial.SerialException as e:
        print(f"Nah uh something failed: {e}")
        return None
    
def print_text(text):
    print("Hi, " + text)


if __name__ == "__main__":
    time.sleep(1) # รอการเชื่อมต่อ
    while True:
        command = input("Enter command (or 'exit' to quit): ").strip()
        if command.lower() == 'exit' or command.lower() == 'quit':
            break

        send_command(command)
        if command == "getdata":
            response = receive_data()

            if response:
                print(f"Response: {response}")
            else :
                print("No response received.")

            responseList = response.split(";")
            waterLevel = responseList[0]
            temperature = responseList[1]

            print("WaterLevel: ", waterLevel)
            print("Temperature: ", temperature)

            insertTable = (
                supabase.table("water_tank")
                .insert({"temperature": temperature, "water_level": waterLevel})
                .execute()
            )

            print("Insert successfully")

    ser.close()
    print("Connection closed!")
