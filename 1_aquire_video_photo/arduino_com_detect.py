import serial.tools.list_ports

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        if "Arduino" in port.description:
            return port.device
    return None

port = find_arduino_port()
if port:
    print(f"Arduino found on port: {port}")
else:
    print("Arduino not found. Please connect your Arduino.")
