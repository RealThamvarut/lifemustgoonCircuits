import serial
# import time

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)

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
    
def print_text(text):
    return ("Hi, " + text)

def close_serial():
    ser.close()
    return None
