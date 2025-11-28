import serial
from flask import Flask, request, jsonify

app = Flask(__name__)

# SERIAL_PORT = '/dev/serial0'
# BAUD_RATE = 115200

try:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=5)
except serial.SerialException as e:
    print(f"OH NO: Could not open serial port: {e}")
    ser = None

def send_uart_command(cmd_string):
    if not ser:
        return "Serial port is not init"
    if not cmd_string:
        return "Nah you don't have command"

    try:
        ser.write((cmd_string + '\n').encode()) 
        return f"Send command: {cmd_string}"

    except serial.SerialException as e:
        return print(f"OH NO: Could not open serial port: {e}")

##### IMPORTANT
# You could just sendcommand wherever you want by using "send_uart_command(<command_string>)"

# I wrote this just to make endpoint that can recieve and send json data using command below
# curl -X POST http://localhost:5000/control -H "Content-Type: application/json" -d '{"command": "<link>"}'
@app.route('/control', method=['POST'])
def control_endpoint():
    data = request.json
    if not data or 'command' not in data:
        return jsonify({"error": "No command provided"}), 400
    command_str = data['command']
    
    result = send_uart_command(command_str)
    # return jsonify({"status": "Sent command to ESP32 successfully"})
    return jsonify({"status": result})
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)