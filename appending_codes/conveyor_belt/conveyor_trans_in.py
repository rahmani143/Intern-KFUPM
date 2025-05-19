# import serial
# import struct
# from serial.tools.list_ports import comports
# import time

# for portitems in comports():
#     print(portitems)

# arduinoserial = serial.Serial(port="COM7",baudrate=9600,timeout=.5)

# print(arduinoserial.is_open)

# arduinoserial.close()
# # print(arduinoserial.is_open)

# # arduinoserial.open()

# # numbertosend = 432

# # stringconverted = str(numbertosend)

# # arduinoserial.write(bytes(stringconverted,'utf-8'))

# # time.sleep(.01)

# # readLine = arduinoserial.readline()

# # stringline = readLine.decode("utf-8")

# # receivedinteger = int(stringline)

# # print(receivedinteger)

# # arduinoserial.close()

# # ser = serial.Serial('COM6', 9600)  # Replace with your port

# # def send_position(value: float):
# #     if 0.0 <= value <= 1.0:
# #         # Pack float into 4 bytes (big-endian format)
# #         data = struct.pack('>f', value)
# #         ser.write(data)
# #     else:
# #         print("Value must be between 0.0 and 1.0")

# # # Example usage:
# # send_position(0.5)  # Send normalized position 0.5
# # ser.close()






# import os; os.system('cls')

# import serial
# arduino = serial.Serial(port='COM7', baudrate=9600, timeout=0.1)

# msgWR = input('Enter a value from 0 to 255: ')
# arduino.write(bytes(msgWR, 'utf-8'))  # write bytes to Arduino

# msgRD = arduino.readline()  # read bytes from Arduino
# msgRD = msgRD.decode('utf-8')  # convert bytes to string
# print(f'Read message from Arduino: {msgRD}\n')




# import os; os.system('cls')
# import serial

# arduino = serial.Serial(port='COM6', baudrate=9600, timeout=None)

# msgWR = input('Enter a value from 0 to 255: ')
# arduino.write(bytes([int(msgWR)]))  # Send as a single byte

# print("Listening for messages from Arduino (press Ctrl+C to stop):")

# try:
#     while True:
#         msgRD = arduino.readline()  # Wait for a line ending with '\n'
#         if msgRD:
#             print(f'Read message from Arduino: {msgRD.decode("utf-8").strip()}')
# except KeyboardInterrupt:
#     print("\nStopped listening. Exiting...")
#     arduino.close()






# import os
# import serial
# import threading

# os.system('cls')  # Clear console (Windows)

# arduino = serial.Serial(port='COM6', baudrate=9600, timeout=0.1)

# def send_commands():
#     while True:
#         try:
#             user_input = input("Enter a value from 0 to 255: ")
#             value = int(user_input)
#             if 0 <= value <= 255:
#                 arduino.write(bytes([value]))
#             else:
#                 print("Error: Value must be between 0 and 255")
#         except ValueError:
#             print("Error: Please enter an integer between 0 and 255")

# # Start input thread
# input_thread = threading.Thread(target=send_commands, daemon=True)
# input_thread.start()

# print("Listening for Arduino messages (Ctrl+C to exit):")

# try:
#     while True:
#         if arduino.in_waiting:
#             msg = arduino.readline().decode('utf-8', errors='replace').strip()
#             print(f"Arduino: {msg}")
# except KeyboardInterrupt:
#     print("\nClosing connection...")
#     arduino.close()







# import os
# import serial
# import struct

# os.system('cls')
# arduino = serial.Serial(port='COM6', baudrate=9600, timeout=0.1)

# print("Listening for Arduino messages (Ctrl+C to exit):")

# try:
#     while True:
#         if arduino.in_waiting:
#             msg = arduino.readline().decode('utf-8', errors='replace').strip()
#             print(f"Arduino: {msg}")
#             if "Enter position (0-255) and speed (50-1000):" in msg:
#                 while True:
#                     try:
#                         pos = int(input("Enter position (0-255): "))
#                         speed = int(input("Enter speed (50-1000((0 to 100%)): "))
#                         if 0 <= pos <= 255 and 50 <= speed <= 1000:
#                             # Pack as 3 bytes: 1 (position) + 2 (speed)
#                             data = struct.pack('<BH', pos, speed)
#                             arduino.write(data)
#                             break
#                         else:
#                             print("Error: Invalid range")
#                     except ValueError:
#                         print("Error: Use integers only")
# except KeyboardInterrupt:
#     arduino.close()





import os
import serial
import struct

os.system('cls')
arduino = serial.Serial(port='COM6', baudrate=9600, timeout=0.1)

print("Listening for Arduino messages (Ctrl+C to exit):")

try:
    while True:
        if arduino.in_waiting:
            msg = arduino.readline().decode('utf-8', errors='replace').strip()
            print(f"Arduino: {msg}")
            
            if "Enter position (0-255) and speed (50-1000):" in msg:
                while True:
                    try:
                        use_speed = input("Do you want to set speed? (y/n): ").strip().lower()
                        pos = int(input("Enter position (0-255): "))
                        if not (0 <= pos <= 255):
                            print("Position must be 0-255!")
                            continue
                        if use_speed == 'y':
                            speed = int(input("Enter speed (50-1000): "))
                            if not (50 <= speed <= 1000):
                                print("Speed must be 50-1000!")
                                continue
                        else:
                            speed = 0  # 0 means don't change speed on Arduino side
                        data = struct.pack('<BH', pos, speed)
                        arduino.write(data)
                        break
                    except ValueError:
                        print("Invalid input! Use integers.")
except KeyboardInterrupt:
    arduino.close()
