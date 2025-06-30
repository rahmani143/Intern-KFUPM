# import serial
# import serial.tools.list_ports
# import struct
# import time
# import threading

# def find_arduino_port():
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         if "Arduino" in port.description or "CH340" in port.description or "USB Serial" in port.description:
#             return port.device
#     return None

# def read_serial_continuously(ser):
#     while True:
#         if ser.in_waiting:
#             try:
#                 line = ser.readline().decode('utf-8', errors='ignore').strip()
#                 if line:
#                     print("Arduino:", line)
#             except:
#                 pass
#         time.sleep(0.1)

# def send_command(ser, pos, speed):
#     data = struct.pack('<BH', pos, speed)
#     ser.write(data)
#     print(f"Sent position={pos}, speed={speed}")

# def main():
#     port = find_arduino_port()
#     if not port:
#         print("Arduino not found. Please connect your Arduino.")
#         return

#     ser = serial.Serial(port, 9600, timeout=1)
#     time.sleep(2)  # allow Arduino to reset

#     # Start background thread to continuously read Arduino messages
#     threading.Thread(target=read_serial_continuously, args=(ser,), daemon=True).start()

#     print("Ready to send commands.")
#     print("Position range: 10-250")
#     print("Speed range: 50-1000")

#     try:
#         while True:
#             user_input = input("Enter pos speed (e.g. 128 300): ").strip()
#             if not user_input:
#                 continue
#             if user_input.lower() in ('exit', 'quit'):
#                 break

#             try:
#                 pos_str, speed_str = user_input.split()
#                 pos = int(pos_str)
#                 speed = int(speed_str)

#                 if not (10 <= pos <= 250):
#                     print("Error: Position must be between 10 and 250")
#                     continue
#                 if not (50 <= speed <= 1000):
#                     print("Error: Speed must be between 50 and 1000")
#                     continue

#                 send_command(ser, pos, speed)

#             except ValueError:
#                 print("Invalid input. Please enter two integers separated by space.")

#     except KeyboardInterrupt:
#         print("\nExiting...")

#     ser.close()

# if __name__ == "__main__":
#     main()









# edit 1:








# import sys
# import struct
# import serial
# import serial.tools.list_ports
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox
# )
# from PyQt6.QtCore import QThread, pyqtSignal

# def find_arduino_port():
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         desc = port.description.lower()
#         if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
#             return port.device
#     return None

# class SerialReaderThread(QThread):
#     data_received = pyqtSignal(str)

#     def __init__(self, serial_port):
#         super().__init__()
#         self.ser = serial_port
#         self.running = True

#     def run(self):
#         while self.running:
#             if self.ser.in_waiting:
#                 try:
#                     line = self.ser.readline().decode('utf-8', errors='ignore').strip()
#                     if line:
#                         self.data_received.emit(line)
#                 except Exception as e:
#                     pass

#     def stop(self):
#         self.running = False
#         self.wait()

# class StepperControlApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Stepper Control")

#         self.serial = None
#         self.reader_thread = None

#         self.layout = QVBoxLayout()

#         self.status_label = QLabel("Arduino Port: Not connected")
#         self.layout.addWidget(self.status_label)

#         self.pos_label = QLabel("Position (10-250):")
#         self.layout.addWidget(self.pos_label)
#         self.pos_input = QLineEdit()
#         self.layout.addWidget(self.pos_input)

#         self.speed_label = QLabel("Speed (50-1000):")
#         self.layout.addWidget(self.speed_label)
#         self.speed_input = QLineEdit()
#         self.layout.addWidget(self.speed_input)

#         self.send_button = QPushButton("Send Command")
#         self.send_button.clicked.connect(self.send_command)
#         self.layout.addWidget(self.send_button)

#         self.output_text = QTextEdit()
#         self.output_text.setReadOnly(True)
#         self.layout.addWidget(self.output_text)

#         self.setLayout(self.layout)

#         self.connect_serial()

#     def connect_serial(self):
#         port = find_arduino_port()
#         if not port:
#             self.status_label.setText("Arduino Port: Not found! Connect Arduino.")
#             return
#         try:
#             self.serial = serial.Serial(port, 9600, timeout=0.1)
#             self.status_label.setText(f"Arduino Port: {port}")
#             # Start thread to read serial data
#             self.reader_thread = SerialReaderThread(self.serial)
#             self.reader_thread.data_received.connect(self.handle_serial_data)
#             self.reader_thread.start()
#         except Exception as e:
#             self.status_label.setText(f"Failed to open port: {e}")

#     def handle_serial_data(self, data):
#         self.output_text.append(f"Arduino: {data}")

#     def send_command(self):
#         if not self.serial or not self.serial.is_open:
#             QMessageBox.warning(self, "Error", "Serial port not connected.")
#             return

#         try:
#             pos = int(self.pos_input.text())
#             speed = int(self.speed_input.text())
#         except ValueError:
#             QMessageBox.warning(self, "Input Error", "Position and speed must be integers.")
#             return

#         if not (10 <= pos <= 250):
#             QMessageBox.warning(self, "Input Error", "Position must be between 10 and 250.")
#             return

#         if not (50 <= speed <= 1000):
#             QMessageBox.warning(self, "Input Error", "Speed must be between 50 and 1000.")
#             return

#         # Pack data: position (1 byte), speed (2 bytes little endian)
#         data = struct.pack('<BH', pos, speed)
#         self.serial.write(data)
#         self.output_text.append(f"Sent: pos={pos}, speed={speed}")

#     def closeEvent(self, event):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         if self.serial and self.serial.is_open:
#             self.serial.close()
#         event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StepperControlApp()
#     window.show()
#     sys.exit(app.exec())










# edit 2:






# closest ever to wht i want until now 

# import sys
# import struct
# import serial
# import serial.tools.list_ports
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
#     QPushButton, QTextEdit, QMessageBox, QStackedLayout, QHBoxLayout
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# import time

# def find_arduino_port():
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         desc = port.description.lower()
#         if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
#             return port.device
#     return None

# class SerialReaderThread(QThread):
#     data_received = pyqtSignal(str)

#     def __init__(self, serial_port):
#         super().__init__()
#         self.ser = serial_port
#         self.running = True

#     def run(self):
#         while self.running:
#             if self.ser.in_waiting:
#                 try:
#                     line = self.ser.readline().decode('utf-8', errors='ignore').strip()
#                     if line:
#                         self.data_received.emit(line)
#                 except Exception:
#                     pass

#     def stop(self):
#         self.running = False
#         self.wait()

# class StepperControlApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Stepper Control")
#         self.resize(350, 320)

#         self.serial = None
#         self.reader_thread = None
#         self.system_ready = False

#         self.stack = QStackedLayout()
#         self.setLayout(self.stack)

#         self.init_main_menu()
#         self.init_manual_page()
#         self.init_automatic_page()

#         self.connect_serial()

#         self.stack.setCurrentWidget(self.page_main)

#     # --- UI Initialization ---

#     def init_main_menu(self):
#         self.page_main = QWidget()
#         layout = QVBoxLayout()
#         self.page_main.setLayout(layout)

#         # Homing status label on top
#         self.homing_label_main = QLabel("Homing system: Please wait...")
#         self.homing_label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_main)

#         label = QLabel("Choose mode:")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         self.btn_manual_mode = QPushButton("Manual")
#         self.btn_manual_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_manual))
#         layout.addWidget(self.btn_manual_mode)

#         self.btn_auto_mode = QPushButton("Automatic")
#         self.btn_auto_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_auto))
#         layout.addWidget(self.btn_auto_mode)

#         self.stack.addWidget(self.page_main)

#     def init_manual_page(self):
#         self.page_manual = QWidget()
#         layout = QVBoxLayout()
#         self.page_manual.setLayout(layout)

#         self.homing_label_manual = QLabel("Homing system: Please wait...")
#         self.homing_label_manual.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_manual)

#         self.status_label_manual = QLabel("Arduino Port: Not connected")
#         layout.addWidget(self.status_label_manual)

#         pos_layout = QHBoxLayout()
#         pos_label = QLabel("Position (10-250):")
#         self.pos_input = QLineEdit()
#         pos_layout.addWidget(pos_label)
#         pos_layout.addWidget(self.pos_input)
#         layout.addLayout(pos_layout)

#         speed_layout = QHBoxLayout()
#         speed_label = QLabel("Speed (50-1000) [default=100]:")
#         self.speed_input = QLineEdit()
#         speed_layout.addWidget(speed_label)
#         speed_layout.addWidget(self.speed_input)
#         layout.addLayout(speed_layout)

#         self.send_btn_manual = QPushButton("Send Command")
#         self.send_btn_manual.clicked.connect(self.manual_send_command)
#         layout.addWidget(self.send_btn_manual)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.output_text_manual = QTextEdit()
#         self.output_text_manual.setReadOnly(True)
#         layout.addWidget(self.output_text_manual)

#         self.stack.addWidget(self.page_manual)

#     def init_automatic_page(self):
#         self.page_auto = QWidget()
#         layout = QVBoxLayout()
#         self.page_auto.setLayout(layout)

#         self.homing_label_auto = QLabel("Homing system: Please wait...")
#         self.homing_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_auto)

#         self.capture_btn = QPushButton("Capture Data (Pos=170, Speed=100)")
#         self.capture_btn.clicked.connect(self.automatic_capture_data)
#         layout.addWidget(self.capture_btn)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.status_label_auto = QLabel("")
#         self.status_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.status_label_auto)

#         self.stack.addWidget(self.page_auto)

#     # --- Serial connection ---
#     def connect_serial(self):
#         port = find_arduino_port()
#         if not port:
#             self.update_status_all("Arduino Port: Not found! Connect Arduino.")
#             return
#         try:
#             self.serial = serial.Serial(port, 9600, timeout=0.1)
#             time.sleep(2)  # Arduino reset delay
#             self.update_status_all(f"Arduino Port: {port}")
#             self.start_serial_thread()
#         except Exception as e:
#             self.update_status_all(f"Failed to open port: {e}")

#     def update_status_all(self, msg):
#         self.status_label_manual.setText(msg)
#         self.status_label_auto.setText(msg)
#         self.homing_label_main.setText("Homing system: Please wait..." if not self.system_ready else "")
#         self.homing_label_manual.setText("Homing system: Please wait..." if not self.system_ready else "")
#         self.homing_label_auto.setText("Homing system: Please wait..." if not self.system_ready else "")

#         # Disable/Enable controls based on system_ready
#         controls_enabled = self.system_ready
#         self.btn_manual_mode.setEnabled(controls_enabled)
#         self.btn_auto_mode.setEnabled(controls_enabled)
#         self.pos_input.setEnabled(controls_enabled)
#         self.speed_input.setEnabled(controls_enabled)
#         self.send_btn_manual.setEnabled(controls_enabled)
#         self.capture_btn.setEnabled(controls_enabled)

#     def start_serial_thread(self):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         self.reader_thread = SerialReaderThread(self.serial)
#         self.reader_thread.data_received.connect(self.handle_serial_data)
#         self.reader_thread.start()

#     # --- Handle serial data received ---
#     def handle_serial_data(self, data):
#         # Check if homing completed message received
#         if "System ready" in data:
#             self.system_ready = True
#             self.update_status_all(self.status_label_manual.text())  # refresh UI to enable controls and hide homing msg

#         # Append to output areas
#         self.output_text_manual.append(f"Arduino: {data}")
#         current_auto_text = self.status_label_auto.text()
#         new_text = (current_auto_text + "\nArduino: " + data).strip()
#         self.status_label_auto.setText(new_text)

#     # --- Command sending functions ---
#     def send_command(self, pos, speed):
#         if not self.serial or not self.serial.is_open:
#             self.show_warning("Serial port not connected.")
#             return False

#         data = struct.pack('<BH', pos, speed)
#         self.serial.write(data)
#         return True

#     def manual_send_command(self):
#         pos_text = self.pos_input.text().strip()
#         speed_text = self.speed_input.text().strip()

#         if not pos_text:
#             self.show_warning("Position is required.")
#             return
#         try:
#             pos = int(pos_text)
#         except ValueError:
#             self.show_warning("Position must be an integer.")
#             return

#         if not (10 <= pos <= 250):
#             self.show_warning("Position must be between 10 and 250.")
#             return

#         if speed_text == "":
#             speed = 100
#         else:
#             try:
#                 speed = int(speed_text)
#             except ValueError:
#                 self.show_warning("Speed must be an integer.")
#                 return
#             if not (50 <= speed <= 1000):
#                 self.show_warning("Speed must be between 50 and 1000.")
#                 return

#         sent = self.send_command(pos, speed)
#         if sent:
#             self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")

#     def automatic_capture_data(self):
#         pos = 170
#         speed = 100
#         sent = self.send_command(pos, speed)
#         if sent:
#             self.status_label_auto.setText(f"Sent: Position={pos}, Speed={speed}")
#         else:
#             self.status_label_auto.setText("Failed to send command: Serial not connected.")

#     def show_warning(self, message):
#         QMessageBox.warning(self, "Input Error", message)

#     # --- Cleanup ---
#     def closeEvent(self, event):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         if self.serial and self.serial.is_open:
#             self.serial.close()
#         event.accept()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StepperControlApp()
#     window.show()
#     sys.exit(app.exec())









# edit 3:








# import sys
# import struct
# import serial
# import serial.tools.list_ports
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
#     QPushButton, QTextEdit, QMessageBox, QStackedLayout, QHBoxLayout
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# import time


# def find_arduino_port():
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         desc = port.description.lower()
#         if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
#             return port.device
#     return None


# class SerialReaderThread(QThread):
#     data_received = pyqtSignal(str)

#     def __init__(self, serial_port):
#         super().__init__()
#         self.ser = serial_port
#         self.running = True

#     def run(self):
#         while self.running:
#             if self.ser.in_waiting:
#                 try:
#                     line = self.ser.readline().decode('utf-8', errors='ignore').strip()
#                     if line:
#                         self.data_received.emit(line)
#                 except Exception:
#                     pass

#     def stop(self):
#         self.running = False
#         self.wait()


# class StepperControlApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Stepper Control")
#         self.resize(350, 320)

#         self.serial = None
#         self.reader_thread = None
#         self.system_ready = False

#         self.stack = QStackedLayout()
#         self.setLayout(self.stack)

#         self.init_main_menu()
#         self.init_manual_page()
#         self.init_automatic_page()

#         self.connect_serial()
#         self.stack.setCurrentWidget(self.page_main)

#     # --- UI Initialization ---

#     def init_main_menu(self):
#         self.page_main = QWidget()
#         layout = QVBoxLayout()
#         self.page_main.setLayout(layout)

#         self.homing_label_main = QLabel("🔄 Homing system: Please wait...")
#         self.homing_label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_main)

#         label = QLabel("Choose mode:")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         self.btn_manual_mode = QPushButton("Manual")
#         self.btn_manual_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_manual))
#         layout.addWidget(self.btn_manual_mode)

#         self.btn_auto_mode = QPushButton("Automatic")
#         self.btn_auto_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_auto))
#         layout.addWidget(self.btn_auto_mode)

#         self.stack.addWidget(self.page_main)

#     def init_manual_page(self):
#         self.page_manual = QWidget()
#         layout = QVBoxLayout()
#         self.page_manual.setLayout(layout)

#         self.homing_label_manual = QLabel("🔄 Homing system: Please wait...")
#         self.homing_label_manual.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_manual)

#         self.status_label_manual = QLabel("Arduino Port: Not connected")
#         layout.addWidget(self.status_label_manual)

#         pos_layout = QHBoxLayout()
#         pos_label = QLabel("Position (10-250):")
#         self.pos_input = QLineEdit()
#         pos_layout.addWidget(pos_label)
#         pos_layout.addWidget(self.pos_input)
#         layout.addLayout(pos_layout)

#         speed_layout = QHBoxLayout()
#         speed_label = QLabel("Speed (50-1000) [default=100]:")
#         self.speed_input = QLineEdit()
#         speed_layout.addWidget(speed_label)
#         speed_layout.addWidget(self.speed_input)
#         layout.addLayout(speed_layout)

#         self.send_btn_manual = QPushButton("Send Command")
#         self.send_btn_manual.clicked.connect(self.manual_send_command)
#         layout.addWidget(self.send_btn_manual)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.output_text_manual = QTextEdit()
#         self.output_text_manual.setReadOnly(True)
#         layout.addWidget(self.output_text_manual)

#         self.stack.addWidget(self.page_manual)

#     def init_automatic_page(self):
#         self.page_auto = QWidget()
#         layout = QVBoxLayout()
#         self.page_auto.setLayout(layout)

#         self.homing_label_auto = QLabel("🔄 Homing system: Please wait...")
#         self.homing_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_auto)

#         self.capture_btn = QPushButton("Capture Data")
#         self.capture_btn.clicked.connect(self.automatic_capture_data)
#         layout.addWidget(self.capture_btn)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.status_label_auto = QLabel("")
#         self.status_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.status_label_auto)

#         self.stack.addWidget(self.page_auto)

#     # --- Serial connection ---
#     def connect_serial(self):
#         port = find_arduino_port()
#         if not port:
#             self.update_status_all("Arduino Port: Not found! Connect Arduino.")
#             return
#         try:
#             self.serial = serial.Serial(port, 9600, timeout=0.1)
#             time.sleep(2)
#             self.update_status_all(f"Arduino Port: {port}")
#             self.start_serial_thread()
#         except Exception as e:
#             self.update_status_all(f"Failed to open port: {e}")

#     def start_serial_thread(self):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         self.reader_thread = SerialReaderThread(self.serial)
#         self.reader_thread.data_received.connect(self.handle_serial_data)
#         self.reader_thread.start()

#     def update_status_all(self, msg):
#         self.status_label_manual.setText(msg)
#         self.status_label_auto.setText(msg)
#         self.update_ui_state()

#     def update_ui_state(self):
#         if self.system_ready:
#             ready_msg = "✅ Homing successful. You can now operate the machine."
#         else:
#             ready_msg = "🔄 Homing system: Please wait..."

#         self.homing_label_main.setText(ready_msg)
#         self.homing_label_manual.setText(ready_msg)
#         self.homing_label_auto.setText(ready_msg)

#         controls_enabled = self.system_ready
#         self.btn_manual_mode.setEnabled(controls_enabled)
#         self.btn_auto_mode.setEnabled(controls_enabled)
#         self.pos_input.setEnabled(controls_enabled)
#         self.speed_input.setEnabled(controls_enabled)
#         self.send_btn_manual.setEnabled(controls_enabled)
#         self.capture_btn.setEnabled(controls_enabled)

#     # --- Handle serial data received ---
#     def handle_serial_data(self, data):
#         # print("DEBUG: Received from Arduino:", data)  # See exactly what's received

#         if "system ready" in data.lower():  # More flexible matching
#             self.system_ready = True
#             self.update_ui_state()

#         self.output_text_manual.append(f"Arduino: {data}")
#         current_auto_text = self.status_label_auto.text()
#         new_text = (current_auto_text + "\nArduino: " + data).strip()
#         self.status_label_auto.setText(new_text)


#     # --- Command sending functions ---
#     def send_command(self, pos, speed):
#         if not self.serial or not self.serial.is_open:
#             self.show_warning("Serial port not connected.")
#             return False

#         data = struct.pack('<BH', pos, speed)
#         self.serial.write(data)
#         return True

#     def manual_send_command(self):
#         pos_text = self.pos_input.text().strip()
#         speed_text = self.speed_input.text().strip()

#         if not pos_text:
#             self.show_warning("Position is required.")
#             return
#         try:
#             pos = int(pos_text)
#         except ValueError:
#             self.show_warning("Position must be an integer.")
#             return

#         if not (10 <= pos <= 250):
#             self.show_warning("Position must be between 10 and 250.")
#             return

#         if speed_text == "":
#             speed = 100
#         else:
#             try:
#                 speed = int(speed_text)
#             except ValueError:
#                 self.show_warning("Speed must be an integer.")
#                 return
#             if not (50 <= speed <= 1000):
#                 self.show_warning("Speed must be between 50 and 1000.")
#                 return

#         sent = self.send_command(pos, speed)
#         if sent:
#             self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")

#     def automatic_capture_data(self):
#         pos = 170
#         speed = 100
#         sent = self.send_command(pos, speed)
#         if sent:
#             self.status_label_auto.setText(f"Sent: Capture command (pos={pos}, speed={speed})")
#         else:
#             self.status_label_auto.setText("Failed to send command: Serial not connected.")

#     def show_warning(self, message):
#         QMessageBox.warning(self, "Input Error", message)

#     def closeEvent(self, event):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         if self.serial and self.serial.is_open:
#             self.serial.close()
#         event.accept()


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StepperControlApp()
#     window.show()
#     sys.exit(app.exec())









# edit 4:









# import sys
# import struct
# import serial
# import serial.tools.list_ports
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
#     QPushButton, QTextEdit, QMessageBox, QStackedLayout, QHBoxLayout
# )
# from PyQt6.QtCore import Qt, QThread, pyqtSignal
# import subprocess
# import time

# def find_arduino_port():
#     ports = list(serial.tools.list_ports.comports())
#     for port in ports:
#         desc = port.description.lower()
#         if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
#             return port.device
#     return None

# class SerialReaderThread(QThread):
#     data_received = pyqtSignal(str)

#     def __init__(self, serial_port):
#         super().__init__()
#         self.ser = serial_port
#         self.running = True

#     def run(self):
#         while self.running:
#             if self.ser.in_waiting:
#                 try:
#                     line = self.ser.readline().decode('utf-8', errors='ignore').strip()
#                     if line:
#                         self.data_received.emit(line)
#                 except Exception:
#                     pass

#     def stop(self):
#         self.running = False
#         self.wait()

# class StepperControlApp(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Stepper Control")
#         self.resize(400, 400)

#         self.serial = None
#         self.reader_thread = None
#         self.system_ready = False

#         self.stack = QStackedLayout()
#         self.setLayout(self.stack)

#         self.init_main_menu()
#         self.init_manual_page()
#         self.init_automatic_page()

#         self.connect_serial()

#         self.stack.setCurrentWidget(self.page_main)

#     # --- UI Initialization ---

#     def init_main_menu(self):
#         self.page_main = QWidget()
#         layout = QVBoxLayout()
#         self.page_main.setLayout(layout)

#         self.homing_label_main = QLabel("Homing system: Please wait...")
#         self.homing_label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_main)

#         label = QLabel("Choose mode:")
#         label.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(label)

#         self.btn_manual_mode = QPushButton("Manual")
#         self.btn_manual_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_manual))
#         layout.addWidget(self.btn_manual_mode)

#         self.btn_auto_mode = QPushButton("Automatic")
#         self.btn_auto_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_auto))
#         layout.addWidget(self.btn_auto_mode)

#         self.stack.addWidget(self.page_main)

#     def init_manual_page(self):
#         self.page_manual = QWidget()
#         layout = QVBoxLayout()
#         self.page_manual.setLayout(layout)

#         self.homing_label_manual = QLabel("Homing system: Please wait...")
#         self.homing_label_manual.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_manual)

#         self.status_label_manual = QLabel("Arduino Port: Not connected")
#         layout.addWidget(self.status_label_manual)

#         pos_layout = QHBoxLayout()
#         pos_label = QLabel("Position (10-250):")
#         self.pos_input = QLineEdit()
#         pos_layout.addWidget(pos_label)
#         pos_layout.addWidget(self.pos_input)
#         layout.addLayout(pos_layout)

#         speed_layout = QHBoxLayout()
#         speed_label = QLabel("Speed (50-1000) [default=100]:")
#         self.speed_input = QLineEdit()
#         speed_layout.addWidget(speed_label)
#         speed_layout.addWidget(self.speed_input)
#         layout.addLayout(speed_layout)

#         count_layout = QHBoxLayout()
#         count_label = QLabel("Number of images to capture:")
#         self.count_input = QLineEdit()
#         count_layout.addWidget(count_label)
#         count_layout.addWidget(self.count_input)
#         layout.addLayout(count_layout)

#         self.send_btn_manual = QPushButton("Send Command")
#         self.send_btn_manual.clicked.connect(self.manual_send_command)
#         layout.addWidget(self.send_btn_manual)

#         self.capture_btn_manual = QPushButton("Capture Data")
#         self.capture_btn_manual.clicked.connect(self.manual_capture_images)
#         layout.addWidget(self.capture_btn_manual)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.output_text_manual = QTextEdit()
#         self.output_text_manual.setReadOnly(True)
#         layout.addWidget(self.output_text_manual)

#         self.stack.addWidget(self.page_manual)

#     def init_automatic_page(self):
#         self.page_auto = QWidget()
#         layout = QVBoxLayout()
#         self.page_auto.setLayout(layout)

#         self.homing_label_auto = QLabel("Homing system: Please wait...")
#         self.homing_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.homing_label_auto)

#         self.capture_btn = QPushButton("Capture Data (Pos=170, Speed=100)")
#         self.capture_btn.clicked.connect(self.automatic_capture_data)
#         layout.addWidget(self.capture_btn)

#         back_btn = QPushButton("Back")
#         back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
#         layout.addWidget(back_btn)

#         self.status_label_auto = QLabel("")
#         self.status_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         layout.addWidget(self.status_label_auto)

#         self.stack.addWidget(self.page_auto)

#     # --- Serial connection ---
#     def connect_serial(self):
#         port = find_arduino_port()
#         if not port:
#             self.update_status_all("Arduino Port: Not found! Connect Arduino.")
#             return
#         try:
#             self.serial = serial.Serial(port, 9600, timeout=0.1)
#             time.sleep(2)  # Arduino reset delay
#             self.update_status_all(f"Arduino Port: {port}")
#             self.start_serial_thread()
#         except Exception as e:
#             self.update_status_all(f"Failed to open port: {e}")

#     def update_status_all(self, msg):
#         self.status_label_manual.setText(msg)
#         self.status_label_auto.setText(msg)
#         if not self.system_ready:
#             self.homing_label_main.setText("Homing system: Please wait...")
#             self.homing_label_manual.setText("Homing system: Please wait...")
#             self.homing_label_auto.setText("Homing system: Please wait...")
#         else:
#             # Show success message centered
#             success_msg = "Homing successful. You can now operate the machine."
#             self.homing_label_main.setText(success_msg)
#             self.homing_label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.homing_label_manual.setText(success_msg)
#             self.homing_label_manual.setAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.homing_label_auto.setText(success_msg)
#             self.homing_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         controls_enabled = self.system_ready
#         self.btn_manual_mode.setEnabled(controls_enabled)
#         self.btn_auto_mode.setEnabled(controls_enabled)
#         self.pos_input.setEnabled(controls_enabled)
#         self.speed_input.setEnabled(controls_enabled)
#         self.send_btn_manual.setEnabled(controls_enabled)
#         self.capture_btn.setEnabled(controls_enabled)
#         self.capture_btn_manual.setEnabled(controls_enabled)
#         self.count_input.setEnabled(controls_enabled)

#     def start_serial_thread(self):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         self.reader_thread = SerialReaderThread(self.serial)
#         self.reader_thread.data_received.connect(self.handle_serial_data)
#         self.reader_thread.start()

#     # --- Handle serial data received ---
#     def handle_serial_data(self, data):
#         if "System ready" in data:
#             self.system_ready = True
#             self.update_status_all(self.status_label_manual.text())

#         self.output_text_manual.append(f"Arduino: {data}")
#         current_auto_text = self.status_label_auto.text()
#         new_text = (current_auto_text + "\nArduino: " + data).strip()
#         self.status_label_auto.setText(new_text)

#     # --- Command sending functions ---
#     def send_command(self, pos, speed):
#         if not self.serial or not self.serial.is_open:
#             self.show_warning("Serial port not connected.")
#             return False

#         data = struct.pack('<BH', pos, speed)
#         self.serial.write(data)
#         return True

#     def manual_send_command(self):
#         pos_text = self.pos_input.text().strip()
#         speed_text = self.speed_input.text().strip()

#         if not pos_text:
#             self.show_warning("Position is required.")
#             return
#         try:
#             pos = int(pos_text)
#         except ValueError:
#             self.show_warning("Position must be an integer.")
#             return

#         if not (10 <= pos <= 250):
#             self.show_warning("Position must be between 10 and 250.")
#             return

#         if speed_text == "":
#             speed = 100
#         else:
#             try:
#                 speed = int(speed_text)
#             except ValueError:
#                 self.show_warning("Speed must be an integer.")
#                 return
#             if not (50 <= speed <= 1000):
#                 self.show_warning("Speed must be between 50 and 1000.")
#                 return

#         sent = self.send_command(pos, speed)
#         if sent:
#             self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")

#     def manual_capture_images(self):
#         pos_text = self.pos_input.text().strip()

#         if not pos_text:
#             self.show_warning("Position is required to capture data.")
#             return
#         try:
#             pos = int(pos_text)
#         except ValueError:
#             self.show_warning("Position must be an integer.")
#             return

#         if not (10 <= pos <= 250):
#             self.show_warning("Position must be between 10 and 250.")
#             return

#         speed_text = self.speed_input.text().strip()
#         if speed_text == "":
#             speed = 100
#         else:
#             try:
#                 speed = int(speed_text)
#             except ValueError:
#                 self.show_warning("Speed must be an integer.")
#                 return
#             if not (50 <= speed <= 1000):
#                 self.show_warning("Speed must be between 50 and 1000.")
#                 return

#         count_text = self.count_input.text().strip()
#         if count_text == "":
#             count = 400  # default number of images
#         else:
#             try:
#                 count = int(count_text)
#             except ValueError:
#                 self.show_warning("Number of images must be an integer.")
#                 return
#             if count <= 0:
#                 self.show_warning("Number of images must be positive.")
#                 return

#         sent = self.send_command(pos, speed)
#         if not sent:
#             self.output_text_manual.append("Failed to send stepper command.")
#             return

#         self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")
#         self.output_text_manual.append(f"Capturing {count} images...")

#         try:
#             subprocess.run(
#                 ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\1_aquire_video_photo\aquired_location.py', str(count)],
#                 check=True
#             )
#             self.output_text_manual.append("Image capture completed.")
#         except Exception as e:
#             self.output_text_manual.append(f"Error running image capture: {e}")

#     def automatic_capture_data(self):
#         pos = 170
#         speed = 100
#         sent = self.send_command(pos, speed)
#         if sent:
#             self.status_label_auto.setText(f"Sent: Position={pos}, Speed={speed}")
#             self.status_label_auto.repaint()  # Update label immediately
#             self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")
#             # Call capture script with default 400 images
#             try:
#                 subprocess.run(
#                     ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\1_aquire_video_photo\aquired_location.py', '400'],
#                     check=True
#                 )
#                 self.output_text_manual.append("Automatic image capture completed.")
#             except Exception as e:
#                 self.output_text_manual.append(f"Error running automatic image capture: {e}")
#         else:
#             self.status_label_auto.setText("Failed to send command: Serial not connected.")

#     def show_warning(self, message):
#         QMessageBox.warning(self, "Input Error", message)

#     # --- Cleanup ---
#     def closeEvent(self, event):
#         if self.reader_thread:
#             self.reader_thread.stop()
#         if self.serial and self.serial.is_open:
#             self.serial.close()
#         event.accept()

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     window = StepperControlApp()
#     window.show()
#     sys.exit(app.exec())










# edit 5:










import sys
import struct
import serial
import serial.tools.list_ports
import subprocess
import time

from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QMessageBox, QStackedLayout, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal


def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        desc = port.description.lower()
        if "arduino" in desc or "ch340" in desc or "usb serial" in desc:
            return port.device
    return None


class SerialReaderThread(QThread):
    data_received = pyqtSignal(str)

    def __init__(self, serial_port):
        super().__init__()
        self.ser = serial_port
        self.running = True

    def run(self):
        while self.running:
            if self.ser.in_waiting:
                try:
                    line = self.ser.readline().decode('utf-8', errors='ignore').strip()
                    if line:
                        self.data_received.emit(line)
                except Exception:
                    pass

    def stop(self):
        self.running = False
        self.wait()


class CaptureThread(QThread):
    finished = pyqtSignal()

    def __init__(self, num_images=200, parent=None):
        super().__init__(parent)
        self.num_images = num_images

    def run(self):
        try:
            # Run your image acquisition script with number of images as argument
            subprocess.run(
                ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\1_aquire_video_photo\aquired_location.py', str(self.num_images)],
                check=True
            )
        except Exception as e:
            # You can log errors here if needed
            pass
        self.finished.emit()


class StepperControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stepper Control")
        self.resize(400, 380)

        self.serial = None
        self.reader_thread = None
        self.system_ready = False

        self.stack = QStackedLayout()
        self.setLayout(self.stack)

        self.init_main_menu()
        self.init_manual_page()
        self.init_automatic_page()

        self.connect_serial()

        self.stack.setCurrentWidget(self.page_main)

    # --- UI Initialization ---

    def init_main_menu(self):
        self.page_main = QWidget()
        layout = QVBoxLayout()
        self.page_main.setLayout(layout)

        # Homing status label on top
        self.homing_label_main = QLabel("Homing system: Please wait...")
        self.homing_label_main.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.homing_label_main)

        label = QLabel("Choose mode:")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        self.btn_manual_mode = QPushButton("Manual")
        self.btn_manual_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_manual))
        layout.addWidget(self.btn_manual_mode)

        self.btn_auto_mode = QPushButton("Automatic")
        self.btn_auto_mode.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_auto))
        layout.addWidget(self.btn_auto_mode)

        self.stack.addWidget(self.page_main)

    def init_manual_page(self):
        self.page_manual = QWidget()
        layout = QVBoxLayout()
        self.page_manual.setLayout(layout)

        self.homing_label_manual = QLabel("Homing system: Please wait...")
        self.homing_label_manual.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.homing_label_manual)

        self.status_label_manual = QLabel("Arduino Port: Not connected")
        layout.addWidget(self.status_label_manual)

        pos_layout = QHBoxLayout()
        pos_label = QLabel("Position (10-250):")
        self.pos_input = QLineEdit()
        pos_layout.addWidget(pos_label)
        pos_layout.addWidget(self.pos_input)
        layout.addLayout(pos_layout)

        speed_layout = QHBoxLayout()
        speed_label = QLabel("Speed (50-1000) [default=100]:")
        self.speed_input = QLineEdit()
        speed_layout.addWidget(speed_label)
        speed_layout.addWidget(self.speed_input)
        layout.addLayout(speed_layout)

        count_layout = QHBoxLayout()
        count_label = QLabel("Number of Images to Capture [default=200]:")
        self.count_input = QLineEdit()
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_input)
        layout.addLayout(count_layout)

        self.send_btn_manual = QPushButton("Send Command")
        self.send_btn_manual.clicked.connect(self.manual_send_command)
        layout.addWidget(self.send_btn_manual)

        self.capture_btn_manual = QPushButton("Capture Data")
        self.capture_btn_manual.clicked.connect(self.manual_capture_data)
        layout.addWidget(self.capture_btn_manual)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(lambda: self.stack.setCurrentWidget(self.page_main))
        layout.addWidget(back_btn)

        self.output_text_manual = QTextEdit()
        self.output_text_manual.setReadOnly(True)
        layout.addWidget(self.output_text_manual)

        self.stack.addWidget(self.page_manual)

    def init_automatic_page(self):
        self.page_auto = QWidget()
        layout = QVBoxLayout()
        self.page_auto.setLayout(layout)

        self.homing_label_auto = QLabel("Homing system: Please wait...")
        self.homing_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.homing_label_auto)

        self.move_to_170_btn = QPushButton("Move to 170")
        self.move_to_170_btn.clicked.connect(self.move_to_170)
        layout.addWidget(self.move_to_170_btn)

        self.object_placed_btn = QPushButton("Object Placed")
        self.object_placed_btn.clicked.connect(self.object_placed)
        self.object_placed_btn.setVisible(False)
        layout.addWidget(self.object_placed_btn)

        back_btn = QPushButton("Back")
        back_btn.clicked.connect(self.back_to_main_from_auto)
        layout.addWidget(back_btn)

        self.status_label_auto = QLabel("")
        self.status_label_auto.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label_auto)

        self.stack.addWidget(self.page_auto)

    # --- Serial connection ---
    def connect_serial(self):
        port = find_arduino_port()
        if not port:
            self.update_status_all("Arduino Port: Not found! Connect Arduino.")
            return
        try:
            self.serial = serial.Serial(port, 9600, timeout=0.1)
            time.sleep(2)  # Arduino reset delay
            self.update_status_all(f"Arduino Port: {port}")
            self.start_serial_thread()
        except Exception as e:
            self.update_status_all(f"Failed to open port: {e}")

    def update_status_all(self, msg):
        self.status_label_manual.setText(msg)
        self.status_label_auto.setText(msg)
        if self.system_ready:
            homing_msg = "Homing successful. You can now operate the machine."
        else:
            homing_msg = "Homing system: Please wait..."
        self.homing_label_main.setText(homing_msg)
        self.homing_label_manual.setText(homing_msg)
        self.homing_label_auto.setText(homing_msg)

        # Disable/Enable controls based on system_ready
        controls_enabled = self.system_ready
        self.btn_manual_mode.setEnabled(controls_enabled)
        self.btn_auto_mode.setEnabled(controls_enabled)

        # Manual page controls
        self.pos_input.setEnabled(controls_enabled)
        self.speed_input.setEnabled(controls_enabled)
        self.count_input.setEnabled(controls_enabled)
        self.send_btn_manual.setEnabled(controls_enabled)
        self.capture_btn_manual.setEnabled(controls_enabled)

        # Automatic page controls
        self.move_to_170_btn.setEnabled(controls_enabled)
        self.object_placed_btn.setEnabled(controls_enabled)

    def start_serial_thread(self):
        if self.reader_thread:
            self.reader_thread.stop()
        self.reader_thread = SerialReaderThread(self.serial)
        self.reader_thread.data_received.connect(self.handle_serial_data)
        self.reader_thread.start()

    # --- Handle serial data received ---
    def handle_serial_data(self, data):
        if "System ready" in data:
            self.system_ready = True
            self.update_status_all(self.status_label_manual.text())

        self.output_text_manual.append(f"Arduino: {data}")
        current_auto_text = self.status_label_auto.text()
        new_text = (current_auto_text + "\nArduino: " + data).strip()
        self.status_label_auto.setText(new_text)

    # --- Command sending functions ---
    def send_command(self, pos, speed):
        if not self.serial or not self.serial.is_open:
            self.show_warning("Serial port not connected.")
            return False

        data = struct.pack('<BH', pos, speed)
        self.serial.write(data)
        return True

    def manual_send_command(self):
        pos_text = self.pos_input.text().strip()
        speed_text = self.speed_input.text().strip()

        if not pos_text:
            self.show_warning("Position is required.")
            return
        try:
            pos = int(pos_text)
        except ValueError:
            self.show_warning("Position must be an integer.")
            return

        if not (10 <= pos <= 250):
            self.show_warning("Position must be between 10 and 250.")
            return

        if speed_text == "":
            speed = 100
        else:
            try:
                speed = int(speed_text)
            except ValueError:
                self.show_warning("Speed must be an integer.")
                return
            if not (50 <= speed <= 1000):
                self.show_warning("Speed must be between 50 and 1000.")
                return

        sent = self.send_command(pos, speed)
        if sent:
            self.output_text_manual.append(f"Sent: pos={pos}, speed={speed}")

    def manual_capture_data(self):
        count_text = self.count_input.text().strip()

        if count_text == "":
            num_images = 200
        else:
            try:
                num_images = int(count_text)
            except ValueError:
                self.show_warning("Number of images must be an integer.")
                return

        # Start capture in a thread so UI stays responsive
        self.capture_thread = CaptureThread(num_images)
        self.capture_thread.finished.connect(self.capture_finished_manual)
        self.capture_thread.start()
        self.output_text_manual.append(f"Started capturing {num_images} images...")

    def capture_finished_manual(self):
        self.output_text_manual.append("Image capture completed.")

    # --- Automatic page functions ---
    def back_to_main_from_auto(self):
        self.reset_automatic_page()
        self.stack.setCurrentWidget(self.page_main)

    def reset_automatic_page(self):
        self.status_label_auto.setText("")
        self.move_to_170_btn.setVisible(True)
        self.move_to_170_btn.setEnabled(True)
        self.object_placed_btn.setVisible(False)
        self.object_placed_btn.setEnabled(True)

    def move_to_170(self):
        pos = 170
        speed = 100
        sent = self.send_command(pos, speed)
        if sent:
            self.status_label_auto.setText(f"Moving to position {pos} at speed {speed}...")
            self.move_to_170_btn.setEnabled(False)
            # Ideally wait for confirmation from Arduino here before showing next button
            time.sleep(1)
            self.status_label_auto.setText("Place the object and press 'Object Placed' when ready.")
            self.object_placed_btn.setVisible(True)
        else:
            self.status_label_auto.setText("Failed to send move command.")

    def object_placed(self):
        # Disable button to prevent multiple presses
        self.object_placed_btn.setEnabled(False)

        pos = 105
        speed = 50
        sent = self.send_command(pos, speed)
        if sent:
            self.status_label_auto.setText(f"Moving to position {pos} at speed {speed} and starting capture...")
            self.capture_thread = CaptureThread(200)
            self.capture_thread.finished.connect(self.capture_finished_auto)
            self.capture_thread.start()
        else:
            self.status_label_auto.setText("Failed to send move command.")
            self.object_placed_btn.setEnabled(True)

    def capture_finished_auto(self):
        self.status_label_auto.setText("Image capture completed.")

    def show_warning(self, message):
        QMessageBox.warning(self, "Input Error", message)

    # --- Cleanup ---
    def closeEvent(self, event):
        if self.reader_thread:
            self.reader_thread.stop()
        if self.serial and self.serial.is_open:
            self.serial.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = StepperControlApp()
    window.show()
    sys.exit(app.exec())
