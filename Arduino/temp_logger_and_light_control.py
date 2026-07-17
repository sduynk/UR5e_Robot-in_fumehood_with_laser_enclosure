import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk
import serial
import threading
import time
import csv
import re


PORT = '/dev/ttyACM0'    # Change this to your Arduino port
BAUD = 115200

class TempLoggerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("NeoPixel Control + Temp Logger")

        # Serial connection
        self.ser = None
        self.running = True

        # Variables
        self.color_rgb = (255, 100, 0)
        self.brightness = 128
        self.temp_str = tk.StringVar(value="Temperature: -- °C")

        # Setup UI
        self.setup_ui()

        # Start serial thread
        self.thread = threading.Thread(target=self.serial_read_loop, daemon=True)
        self.thread.start()

        # Open serial port
        try:
            self.ser = serial.Serial(PORT, BAUD, timeout=1)
            time.sleep(2)  # Arduino reset time
            print("Connected to Arduino")
        except serial.SerialException as e:
            print("Error opening serial port:", e)

        # Open log file
        self.csvfile = open("/home/ur5e/Documents/temp2.csv", "a", newline="")
        self.csvwriter = csv.writer(self.csvfile)
        self.csvwriter.writerow(["Timestamp", "Temperature (°C)"])

    def setup_ui(self):
        # Color picker button
        self.btn_pick_color = ttk.Button(self.root, text="Pick Color", command=self.pick_color)
        self.btn_pick_color.grid(row=0, column=0, padx=10, pady=10)

        # Brightness slider
        self.scale_brightness = ttk.Scale(self.root, from_=0, to=255, orient='horizontal', command=self.brightness_changed)
        self.scale_brightness.set(self.brightness)
        self.scale_brightness.grid(row=0, column=1, padx=10, pady=10)

        # Current color display
        self.color_display = tk.Canvas(self.root, width=50, height=50, bg=self.rgb_to_hex(self.color_rgb))
        self.color_display.grid(row=0, column=2, padx=10, pady=10)

        # Temperature display label
        self.label_temp = ttk.Label(self.root, textvariable=self.temp_str, font=("Arial", 16))
        self.label_temp.grid(row=1, column=0, columnspan=3, pady=10)

        # Exit button
        self.btn_exit = ttk.Button(self.root, text="Exit", command=self.close)
        self.btn_exit.grid(row=2, column=1, pady=10)

    def rgb_to_hex(self, rgb):
        return '#%02x%02x%02x' % rgb

    def pick_color(self):
        color_code = colorchooser.askcolor(color=self.rgb_to_hex(self.color_rgb))
        if color_code[0]:
            self.color_rgb = tuple(map(int, color_code[0]))
            self.color_display.configure(bg=self.rgb_to_hex(self.color_rgb))
            self.send_color()

    def brightness_changed(self, val):
        self.brightness = int(float(val))
        self.send_color()

    def send_color(self):
        if self.ser and self.ser.is_open:
            r, g, b = self.color_rgb
            # Send color and brightness as R,G,B,BRT\n
            cmd = f"{r},{g},{b},{self.brightness}\n"
            self.ser.write(cmd.encode())
            print("Sent:", cmd.strip())
            
        else:
            print("Serial port not connected")

    def serial_read_loop(self):
        temp_pattern = re.compile(r"Temperature:\s*([-+]?\d*\.\d+|\d+)\s*°C")
        while self.running:
            if self.ser and self.ser.in_waiting:
                try:
                    line = self.ser.readline().decode('utf-8').strip()
                    # print("Received:", line)  # Debug
                    m = temp_pattern.search(line)
                    if m:
                        temp_c = float(m.group(1))
                        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
                        self.temp_str.set(f"Temperature: {temp_c:.2f} °C")
                        # Log to CSV
                        self.csvwriter.writerow([timestamp, f"{temp_c:.2f}"])
                        self.csvfile.flush()
                except Exception as e:
                    print("Error reading serial:", e)
            time.sleep(0.1)

    def close(self):
        self.running = False
        if self.ser and self.ser.is_open:
            self.ser.close()
        if self.csvfile:
            self.csvfile.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TempLoggerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.close)
    root.mainloop()