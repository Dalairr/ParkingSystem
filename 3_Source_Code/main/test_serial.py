import serial
import os
from time import sleep
from dotenv import load_dotenv

# ✅ Load the actual configuration.env file
load_dotenv("configuration.env")

ser = serial.Serial(os.getenv("SERIAL_PORT"), 9600, timeout=1)
print("📡 Reading from serial port...")

while True:
    if ser.in_waiting > 0:
        raw = ser.readline().decode("utf-8", errors="ignore").strip()
        print(f"🧾 Raw: {raw}")
    sleep(0.1)
