# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import serial
# import struct
# import subprocess
# import threading
# import time

# # Serial setup
# SERIAL_PORT = 'COM3'
# BAUDRATE = 9600

# start_point = None
# end_point = None

# def send_command(pos, speed):
#     try:
#         data = struct.pack('<BH', pos, speed)
#         arduino.write(data)
#     except Exception as e:
#         messagebox.showerror("Serial Error", str(e))

# def home():
#     send_command(0, 0)
#     log("Sent homing command.")

# def find_max():
#     send_command(255, 0)
#     log("Sent find max command.")

# def capture():
#     send_command(10, 100)
#     log("Sent move to position 10, speed 100.")
#     time.sleep(2)
#     log("Capturing image...")
#     try:
#         subprocess.run(
#             ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py'],
#             check=True
#         )
#         log("Image captured.")
#     except Exception as e:
#         log(f"Error running image capture: {e}")
#     time.sleep(2)
#     send_command(250, 1000)
#     log("Returned to max position.")

# def log(msg):
#     log_text.config(state=tk.NORMAL)
#     log_text.insert(tk.END, msg + "\n")
#     log_text.see(tk.END)
#     log_text.config(state=tk.DISABLED)

# def listen_serial():
#     while True:
#         try:
#             if arduino.in_waiting:
#                 msg = arduino.readline().decode('utf-8', errors='replace').strip()
#                 if msg:
#                     log(f"Arduino: {msg}")
#             time.sleep(0.1)
#         except Exception as e:
#             log(f"Serial error: {e}")
#             break

# # Custom dialog for start/end input
# class RangeDialog(simpledialog.Dialog):
#     def body(self, master):
#         tk.Label(master, text="Start Point (0-255):").grid(row=0, column=0, padx=5, pady=5)
#         tk.Label(master, text="End Point (0-255):").grid(row=1, column=0, padx=5, pady=5)
#         self.start_entry = tk.Entry(master)
#         self.end_entry = tk.Entry(master)
#         self.start_entry.grid(row=0, column=1, padx=5, pady=5)
#         self.end_entry.grid(row=1, column=1, padx=5, pady=5)
#         return self.start_entry

#     def apply(self):
#         try:
#             self.start = int(self.start_entry.get())
#             self.end = int(self.end_entry.get())
#         except ValueError:
#             self.start = None
#             self.end = None

# def move_range_thread(start, end):
#     # Move to start position
#     send_command(start, 100)
#     log(f"Moved to start position: {start} at speed 100")
#     time.sleep(2)  # Wait for Arduino to reach start

#     # Trigger camera capture
#     log("Capturing image at start position...")
#     try:
#         subprocess.run(
#             ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py'],
#             check=True
#         )
#         log("Image captured at start position.")
#     except Exception as e:
#         log(f"Error running image capture: {e}")

#     # Move to end position
#     send_command(end, 100)
#     log(f"Moved to end position: {end} at speed 100")
#     time.sleep(2)  # Wait for Arduino to reach end

#     # Return to max position (250)
#     send_command(250, 1000)
#     log("Returned to max position (250)")

# def set_range():
#     global start_point, end_point
#     dialog = RangeDialog(root, title="Set Range")
#     if hasattr(dialog, 'start') and hasattr(dialog, 'end') and dialog.start is not None and dialog.end is not None:
#         if 0 <= dialog.start <= 255 and 0 <= dialog.end <= 255:
#             start_point = dialog.start
#             end_point = dialog.end
#             log(f"Start point set to {start_point}, End point set to {end_point}")
#             # Move in a thread to keep GUI responsive
#             threading.Thread(target=move_range_thread, args=(start_point, end_point), daemon=True).start()
#         else:
#             messagebox.showerror("Invalid Input", "Values must be between 0 and 255.")
#     else:
#         log("Set Range cancelled or invalid input.")

# # Open serial port
# try:
#     arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=0.1)
# except Exception as e:
#     messagebox.showerror("Serial Error", f"Could not open serial port: {e}")
#     exit(1)

# # GUI setup
# root = tk.Tk()
# root.title("Arduino Conveyor Control")

# frame = tk.Frame(root)
# frame.pack(padx=10, pady=10)

# btn_home = tk.Button(frame, text="Home", width=15, command=home)
# btn_home.grid(row=0, column=0, padx=5, pady=5)

# btn_max = tk.Button(frame, text="Find Max", width=15, command=find_max)
# btn_max.grid(row=0, column=1, padx=5, pady=5)

# btn_capture = tk.Button(frame, text="Capture", width=15, command=capture)
# btn_capture.grid(row=0, column=2, padx=5, pady=5)

# btn_set_range = tk.Button(frame, text="Set Range", width=15, command=set_range)
# btn_set_range.grid(row=0, column=3, padx=5, pady=5)

# log_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
# log_text.pack(padx=10, pady=10)

# serial_thread = threading.Thread(target=listen_serial, daemon=True)
# serial_thread.start()

# def on_close():
#     try:
#         arduino.close()
#     except:
#         pass
#     root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_close)
# root.mainloop()











# edit 0:













# import tkinter as tk
# from tkinter import messagebox, simpledialog
# import serial
# import struct
# import subprocess
# import threading
# import time

# SERIAL_PORT = 'COM3'
# BAUDRATE = 9600

# start_point = None
# end_point = None

# def send_command(pos, speed):
#     try:
#         data = struct.pack('<BH', pos, speed)
#         arduino.write(data)
#     except Exception as e:
#         messagebox.showerror("Serial Error", str(e))

# def home():
#     send_command(0, 0)
#     log("Sent homing command.")

# def find_max():
#     send_command(255, 0)
#     log("Sent find max command.")

# def ask_num_pictures():
#     num = simpledialog.askinteger(
#         "Number of Pictures",
#         "How many pictures to take?",
#         parent=root,
#         minvalue=1,
#         maxvalue=10000
#     )
#     if num is None:
#         num = 400  # Default if nothing is provided
#     return num

# def capture():
#     num_pictures = ask_num_pictures()
#     send_command(10, 100)
#     log("Sent move to position 10, speed 100.")
#     time.sleep(2)
#     log(f"Capturing {num_pictures} image(s)...")
#     try:
#         subprocess.run(
#             ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\1_aquire_video_photo\aquired_location.py', str(num_pictures)],
#             check=True
#         )
#         log(f"{num_pictures} image(s) captured.")
#     except Exception as e:
#         log(f"Error running image capture: {e}")
#     time.sleep(2)
#     send_command(250, 1000)
#     log("Returned to max position.")

# def log(msg):
#     log_text.config(state=tk.NORMAL)
#     log_text.insert(tk.END, msg + "\n")
#     log_text.see(tk.END)
#     log_text.config(state=tk.DISABLED)

# def listen_serial():
#     while True:
#         try:
#             if arduino.in_waiting:
#                 msg = arduino.readline().decode('utf-8', errors='replace').strip()
#                 if msg:
#                     log(f"Arduino: {msg}")
#             time.sleep(0.1)
#         except Exception as e:
#             log(f"Serial error: {e}")
#             break

# # Custom dialog for start/end input
# class RangeDialog(simpledialog.Dialog):
#     def body(self, master):
#         tk.Label(master, text="Start Point (0-255):").grid(row=0, column=0, padx=5, pady=5)
#         tk.Label(master, text="End Point (0-255):").grid(row=1, column=0, padx=5, pady=5)
#         self.start_entry = tk.Entry(master)
#         self.end_entry = tk.Entry(master)
#         self.start_entry.grid(row=0, column=1, padx=5, pady=5)
#         self.end_entry.grid(row=1, column=1, padx=5, pady=5)
#         return self.start_entry

#     def apply(self):
#         try:
#             self.start = int(self.start_entry.get())
#             self.end = int(self.end_entry.get())
#         except ValueError:
#             self.start = None
#             self.end = None

# def move_range_thread(start, end, num_pictures):
#     # Move to start position
#     send_command(start, 100)
#     log(f"Moved to start position: {start} at speed 100")
#     time.sleep(2)  # Wait for Arduino to reach start

#     # Trigger camera capture
#     log(f"Capturing {num_pictures} image(s) at start position...")
#     try:
#         subprocess.run(
#             ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\1_aquire_video_photo\aquired_location.py', str(num_pictures)],
#             check=True
#         )
#         log(f"{num_pictures} image(s) captured at start position.")
#     except Exception as e:
#         log(f"Error running image capture: {e}")

#     # Move to end position
#     send_command(end, 100)
#     log(f"Moved to end position: {end} at speed 100")
#     time.sleep(2)  # Wait for Arduino to reach end

#     # Return to max position (250)
#     send_command(250, 1000)
#     log("Returned to max position (250)")

# def set_range():
#     global start_point, end_point
#     dialog = RangeDialog(root, title="Set Range")
#     if hasattr(dialog, 'start') and hasattr(dialog, 'end') and dialog.start is not None and dialog.end is not None:
#         if 0 <= dialog.start <= 255 and 0 <= dialog.end <= 255:
#             start_point = dialog.start
#             end_point = dialog.end
#             log(f"Start point set to {start_point}, End point set to {end_point}")
#             num_pictures = ask_num_pictures()
#             # Move in a thread to keep GUI responsive
#             threading.Thread(target=move_range_thread, args=(start_point, end_point, num_pictures), daemon=True).start()
#         else:
#             messagebox.showerror("Invalid Input", "Values must be between 0 and 255.")
#     else:
#         log("Set Range cancelled or invalid input.")

# # Open serial port
# try:
#     arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=0.1)
# except Exception as e:
#     messagebox.showerror("Serial Error", f"Could not open serial port: {e}")
#     exit(1)

# # GUI setup
# root = tk.Tk()
# root.title("Arduino Conveyor Control")

# frame = tk.Frame(root)
# frame.pack(padx=10, pady=10)

# btn_home = tk.Button(frame, text="Home", width=15, command=home)
# btn_home.grid(row=0, column=0, padx=5, pady=5)

# btn_max = tk.Button(frame, text="Find Max", width=15, command=find_max)
# btn_max.grid(row=0, column=1, padx=5, pady=5)

# btn_capture = tk.Button(frame, text="Capture", width=15, command=capture)
# btn_capture.grid(row=0, column=2, padx=5, pady=5)

# btn_set_range = tk.Button(frame, text="Set Range", width=15, command=set_range)
# btn_set_range.grid(row=0, column=3, padx=5, pady=5)

# log_text = tk.Text(root, height=10, width=60, state=tk.DISABLED)
# log_text.pack(padx=10, pady=10)

# serial_thread = threading.Thread(target=listen_serial, daemon=True)
# serial_thread.start()

# def on_close():
#     try:
#         arduino.close()
#     except:
#         pass
#     root.destroy()

# root.protocol("WM_DELETE_WINDOW", on_close)
# root.mainloop()















# edit 2:













# import sys
# import serial
# import struct
# import subprocess
# import threading
# import time
# from PyQt5 import QtGui

# from PyQt5.QtWidgets import (
#     QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
#     QMessageBox, QInputDialog, QDialog, QFormLayout, QLineEdit, QLabel
# )
# from PyQt5.QtCore import Qt, pyqtSignal, QObject

# SERIAL_PORT = 'COM3'
# BAUDRATE = 9600

# start_point = None
# end_point = None

# # Signal class for thread-safe logging
# class Communicate(QObject):
#     log_signal = pyqtSignal(str)

# # Serial send
# def send_command(pos, speed):
#     try:
#         data = struct.pack('<BH', pos, speed)
#         arduino.write(data)
#     except Exception as e:
#         QMessageBox.critical(None, "Serial Error", str(e))

# def ask_num_pictures():
#     num, ok = QInputDialog.getInt(None, "Number of Pictures", "How many pictures to take?", 400, 1, 10000)
#     return num if ok else 400

# class RangeDialog(QDialog):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.start = None
#         self.end = None
#         self.setWindowTitle("Set Range")
#         layout = QFormLayout(self)

#         self.start_input = QLineEdit()
#         self.end_input = QLineEdit()
#         layout.addRow("Start Point (0-255):", self.start_input)
#         layout.addRow("End Point (0-255):", self.end_input)

#         self.start_input.setValidator(QtGui.QIntValidator(0, 255))
#         self.end_input.setValidator(QtGui.QIntValidator(0, 255))

#         btn = QPushButton("OK")
#         btn.clicked.connect(self.validate_input)
#         layout.addWidget(btn)

#     def validate_input(self):
#         try:
#             self.start = int(self.start_input.text())
#             self.end = int(self.end_input.text())
#             if 0 <= self.start <= 255 and 0 <= self.end <= 255:
#                 self.accept()
#             else:
#                 raise ValueError
#         except:
#             QMessageBox.warning(self, "Invalid Input", "Please enter values between 0 and 255.")

# class MainWindow(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.comm = Communicate()
#         self.comm.log_signal.connect(self.log)

#         self.setWindowTitle("Arduino Conveyor Control")
#         self.init_ui()
#         self.start_serial_thread()

#     def init_ui(self):
#         layout = QVBoxLayout()

#         btn_layout = QHBoxLayout()
#         self.btn_home = QPushButton("Home")
#         self.btn_home.clicked.connect(self.home)
#         btn_layout.addWidget(self.btn_home)

#         self.btn_max = QPushButton("Find Max")
#         self.btn_max.clicked.connect(self.find_max)
#         btn_layout.addWidget(self.btn_max)

#         self.btn_capture = QPushButton("Capture")
#         self.btn_capture.clicked.connect(self.capture)
#         btn_layout.addWidget(self.btn_capture)

#         self.btn_set_range = QPushButton("Set Range")
#         self.btn_set_range.clicked.connect(self.set_range)
#         btn_layout.addWidget(self.btn_set_range)

#         layout.addLayout(btn_layout)

#         self.log_text = QTextEdit()
#         self.log_text.setReadOnly(True)
#         layout.addWidget(self.log_text)

#         self.setLayout(layout)

#     def log(self, msg):
#         self.log_text.append(msg)

#     def home(self):
#         send_command(0, 0)
#         self.comm.log_signal.emit("Sent homing command.")

#     def find_max(self):
#         send_command(255, 0)
#         self.comm.log_signal.emit("Sent find max command.")

#     def capture(self):
#         num_pictures = ask_num_pictures()
#         send_command(10, 100)
#         self.comm.log_signal.emit("Sent move to position 10, speed 100.")
#         time.sleep(2)
#         self.comm.log_signal.emit(f"Capturing {num_pictures} image(s)...")
#         try:
#             subprocess.run(
#                 ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py', str(num_pictures)],
#                 check=True
#             )
#             self.comm.log_signal.emit(f"{num_pictures} image(s) captured.")
#         except Exception as e:
#             self.comm.log_signal.emit(f"Error running image capture: {e}")
#         time.sleep(2)
#         send_command(250, 1000)
#         self.comm.log_signal.emit("Returned to max position.")

#     def move_range_thread(self, start, end, num_pictures):
#         send_command(start, 100)
#         self.comm.log_signal.emit(f"Moved to start position: {start}")
#         time.sleep(2)

#         self.comm.log_signal.emit(f"Capturing {num_pictures} image(s) at start position...")
#         try:
#             subprocess.run(
#                 ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py', str(num_pictures)],
#                 check=True
#             )
#             self.comm.log_signal.emit(f"{num_pictures} image(s) captured at start position.")
#         except Exception as e:
#             self.comm.log_signal.emit(f"Error running image capture: {e}")

#         send_command(end, 100)
#         self.comm.log_signal.emit(f"Moved to end position: {end}")
#         time.sleep(2)

#         send_command(250, 1000)
#         self.comm.log_signal.emit("Returned to max position (250)")

#     def set_range(self):
#         global start_point, end_point
#         dialog = RangeDialog(self)
#         if dialog.exec_():
#             start_point = dialog.start
#             end_point = dialog.end
#             self.comm.log_signal.emit(f"Start: {start_point}, End: {end_point}")
#             num_pictures = ask_num_pictures()
#             threading.Thread(target=self.move_range_thread, args=(start_point, end_point, num_pictures), daemon=True).start()

#     def start_serial_thread(self):
#         def listen():
#             while True:
#                 try:
#                     if arduino.in_waiting:
#                         msg = arduino.readline().decode('utf-8', errors='replace').strip()
#                         if msg:
#                             self.comm.log_signal.emit(f"Arduino: {msg}")
#                     time.sleep(0.1)
#                 except Exception as e:
#                     self.comm.log_signal.emit(f"Serial error: {e}")
#                     break
#         threading.Thread(target=listen, daemon=True).start()

#     def closeEvent(self, event):
#         try:
#             arduino.close()
#         except:
#             pass
#         event.accept()

# # Initialize serial
# try:
#     arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=0.1)
# except Exception as e:
#     app = QApplication(sys.argv)
#     QMessageBox.critical(None, "Serial Error", f"Could not open serial port: {e}")
#     sys.exit(1)

# # Run App
# app = QApplication(sys.argv)
# window = MainWindow()
# window.show()
# sys.exit(app.exec_())


# edit 3:


import sys
import serial
import serial.tools.list_ports
import struct
import subprocess
import threading
import time
from PyQt5 import QtGui

from PyQt5.QtWidgets import (
    QApplication, QWidget, QPushButton, QTextEdit, QVBoxLayout, QHBoxLayout,
    QMessageBox, QInputDialog, QDialog, QFormLayout, QLineEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QObject

BAUDRATE = 9600

start_point = None
end_point = None

# Signal class for thread-safe logging
class Communicate(QObject):
    log_signal = pyqtSignal(str)

# Serial send
def send_command(pos, speed):
    try:
        data = struct.pack('<BH', pos, speed)
        arduino.write(data)
    except Exception as e:
        QMessageBox.critical(None, "Serial Error", str(e))

def ask_num_pictures():
    num, ok = QInputDialog.getInt(None, "Number of Pictures", "How many pictures to take?", 400, 1, 10000)
    return num if ok else 400

class RangeDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.start = None
        self.end = None
        self.setWindowTitle("Set Range")
        layout = QFormLayout(self)

        self.start_input = QLineEdit()
        self.end_input = QLineEdit()
        layout.addRow("Start Point (0-255):", self.start_input)
        layout.addRow("End Point (0-255):", self.end_input)

        self.start_input.setValidator(QtGui.QIntValidator(0, 255))
        self.end_input.setValidator(QtGui.QIntValidator(0, 255))

        btn = QPushButton("OK")
        btn.clicked.connect(self.validate_input)
        layout.addWidget(btn)

    def validate_input(self):
        try:
            self.start = int(self.start_input.text())
            self.end = int(self.end_input.text())
            if 0 <= self.start <= 255 and 0 <= self.end <= 255:
                self.accept()
            else:
                raise ValueError
        except:
            QMessageBox.warning(self, "Invalid Input", "Please enter values between 0 and 255.")

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.comm = Communicate()
        self.comm.log_signal.connect(self.log)

        self.setWindowTitle("Arduino Conveyor Control")
        self.init_ui()
        self.start_serial_thread()

    def init_ui(self):
        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()
        self.btn_home = QPushButton("Home")
        self.btn_home.clicked.connect(self.home)
        btn_layout.addWidget(self.btn_home)

        self.btn_max = QPushButton("Find Max")
        self.btn_max.clicked.connect(self.find_max)
        btn_layout.addWidget(self.btn_max)

        self.btn_capture = QPushButton("Capture")
        self.btn_capture.clicked.connect(self.capture)
        btn_layout.addWidget(self.btn_capture)

        self.btn_set_range = QPushButton("Set Range")
        self.btn_set_range.clicked.connect(self.set_range)
        btn_layout.addWidget(self.btn_set_range)

        layout.addLayout(btn_layout)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        layout.addWidget(self.log_text)

        self.setLayout(layout)

    def log(self, msg):
        self.log_text.append(msg)

    def home(self):
        send_command(0, 0)
        self.comm.log_signal.emit("Sent homing command.")

    def find_max(self):
        send_command(255, 0)
        self.comm.log_signal.emit("Sent find max command.")

    def capture(self):
        num_pictures = ask_num_pictures()
        send_command(10, 100)
        self.comm.log_signal.emit("Sent move to position 10, speed 100.")
        time.sleep(2)
        self.comm.log_signal.emit(f"Capturing {num_pictures} image(s)...")
        try:
            subprocess.run(
                ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py', str(num_pictures)],
                check=True
            )
            self.comm.log_signal.emit(f"{num_pictures} image(s) captured.")
        except Exception as e:
            self.comm.log_signal.emit(f"Error running image capture: {e}")
        time.sleep(2)
        send_command(250, 1000)
        self.comm.log_signal.emit("Returned to max position.")

    def move_range_thread(self, start, end, num_pictures):
        send_command(start, 100)
        self.comm.log_signal.emit(f"Moved to start position: {start}")
        time.sleep(2)

        self.comm.log_signal.emit(f"Capturing {num_pictures} image(s) at start position...")
        try:
            subprocess.run(
                ['python', r'C:\Users\bss10\OneDrive\Desktop\camera_env\flir_test\aquired_location.py', str(num_pictures)],
                check=True
            )
            self.comm.log_signal.emit(f"{num_pictures} image(s) captured at start position.")
        except Exception as e:
            self.comm.log_signal.emit(f"Error running image capture: {e}")

        send_command(end, 100)
        self.comm.log_signal.emit(f"Moved to end position: {end}")
        time.sleep(2)

        send_command(250, 1000)
        self.comm.log_signal.emit("Returned to max position (250)")

    def set_range(self):
        global start_point, end_point
        dialog = RangeDialog(self)
        if dialog.exec_():
            start_point = dialog.start
            end_point = dialog.end
            self.comm.log_signal.emit(f"Start: {start_point}, End: {end_point}")
            num_pictures = ask_num_pictures()
            threading.Thread(target=self.move_range_thread, args=(start_point, end_point, num_pictures), daemon=True).start()

    def start_serial_thread(self):
        def listen():
            while True:
                try:
                    if arduino.in_waiting:
                        msg = arduino.readline().decode('utf-8', errors='replace').strip()
                        if msg:
                            self.comm.log_signal.emit(f"Arduino: {msg}")
                    time.sleep(0.1)
                except Exception as e:
                    self.comm.log_signal.emit(f"Serial error: {e}")
                    break
        threading.Thread(target=listen, daemon=True).start()

    def closeEvent(self, event):
        try:
            arduino.close()
        except:
            pass
        event.accept()

def find_arduino_port():
    ports = list(serial.tools.list_ports.comports())
    for port in ports:
        # This checks if the word "Arduino" is in the description of the device
        if "Arduino" in port.description:
            return port.device
    return None

# Auto-detect Arduino COM port
SERIAL_PORT = find_arduino_port()

if SERIAL_PORT is None:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Serial Error", "Could not find Arduino COM port. Please connect your Arduino and restart.")
    sys.exit(1)

try:
    arduino = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, timeout=0.1)
except Exception as e:
    app = QApplication(sys.argv)
    QMessageBox.critical(None, "Serial Error", f"Could not open serial port {SERIAL_PORT}: {e}")
    sys.exit(1)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
