import serial
import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)

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
        commad = input("Enter command (or 'exit' to quit): ").strip()
        if commad.lower() == 'exit' or commad.lower() == 'quit':
            break
        
        send_command(commad)
        # if commad == "getdata":
        response = receive_data()
        if response:
            print(f"Response: {response}")
        else :
            print("No response received.")
        
        

    ser.close()
    print("Connection closed!")