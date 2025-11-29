import serial
# import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)

class ESP32:
    def __init__(self):
        self.waterLevel = None
        self.temperature = None
        self.weight = None

    def getSensor(self):
        send_command("getdata")
        response = receive_data()

        if not response:
            print("No response received")

        responseList = response.split(";")
        if len(responseList) != 3:
            print("Invalid response")
        self.waterLevel = round(max(((16 - float(responseList[0])) / 0.16 ), 0), 2)
        self.temperature = responseList[1]
        self.weight = responseList[2]

def send_command(cmd):
    if not cmd:
        return None
    try:
        ser.write((cmd + '\n').encode()) # ส่งคำสั่งพร้อมขึ้นบรรทัดใหม่
        return f"Send command: {cmd}"

    except serial.SerialException as e:
        return f"Nah uh something failed: {e}"

def receive_data():
    try:
        # time.sleep(0.5)
        line = ser.readline().decode('utf-8').strip()  
        while line == "":
            line = ser.readline().decode('utf-8').strip()
        
        # print(f"Receive from ESP32: {line}")
        return line
    except serial.SerialException as e:
        return f"Nah uh something failed: {e}"
    
def close_serial():
    ser.close()
    return None
