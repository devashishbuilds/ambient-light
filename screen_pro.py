import serial
import time
import numpy as np
from PIL import ImageGrab

# ---- Configuration ----
SERIAL_PORT = 'COM3'  
BAUD_RATE = 115200
NUM_LEDS = 54

# LED section sizes
bottom_leds = 16
right_leds = 11
top_leds = 16
left_leds = 11

print(f"Connecting to {SERIAL_PORT}...")

try:
    # Added write_timeout to prevent hanging if ESP32 disconnects
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1, write_timeout=1)
    time.sleep(3) # Wait 3 seconds for ESP32 to reboot after connection
    print("Connected! Press Ctrl+C to stop.")

except serial.SerialException as e:
    print(f"Error: Could not open port {SERIAL_PORT}. Is Arduino IDE open?")
    exit()

def get_edge_colors():
    screen = ImageGrab.grab()
    # Resize to small image for faster processing (optional but recommended)
    # screen = screen.resize((300, 200)) 
    screen_np = np.array(screen)
    h, w, _ = screen_np.shape

    led_data = []

    # --- Capture Logic (Same as yours) ---
    # Bottom
    for i in range(bottom_leds):
        x_start = int(i * w / bottom_leds)
        x_end = int((i + 1) * w / bottom_leds)
        region = screen_np[h - 20:h, x_start:x_end]
        avg = np.mean(region, axis=(0, 1))
        led_data.append(tuple(avg.astype(int))) # Ensure int

    # Right
    for i in range(right_leds):
        y_start = int(i * h / right_leds)
        y_end = int((i + 1) * h / right_leds)
        region = screen_np[y_start:y_end, w - 20:w]
        avg = np.mean(region, axis=(0, 1))
        led_data.append(tuple(avg.astype(int)))

    # Top
    top_colors = []
    for i in range(top_leds):
        x_start = int(i * w / top_leds)
        x_end = int((i + 1) * w / top_leds)
        region = screen_np[0:20, x_start:x_end]
        avg = np.mean(region, axis=(0, 1))
        top_colors.append(tuple(avg.astype(int)))
    top_colors.reverse()
    led_data.extend(top_colors)

    # Left
    for i in range(left_leds):
        y_start = int(i * h / left_leds)
        y_end = int((i + 1) * h / left_leds)
        region = screen_np[y_start:y_end, 0:20]
        avg = np.mean(region, axis=(0, 1))
        led_data.append(tuple(avg.astype(int)))

    return led_data

try:
    while True:
        start_time = time.time()
        colors = get_edge_colors()
        
        serial_data = bytearray()
        for r, g, b in colors:
            # TRY THIS: Standard RGB order first. 
            # If colors are wrong, change to [g, r, b]
            serial_data += bytes([0, 255, 0]) 

        ser.write(serial_data)
        
        # Optional: Print FPS to ensure it's not freezing
        # print(f"FPS: {1.0 / (time.time() - start_time):.2f}") 
        
        # Removed sleep(0.02) to maximize speed, ImageGrab is already slow enough
        
except KeyboardInterrupt:
    print("\nStopping...")
    ser.close()
    print("Serial closed.")
except serial.SerialTimeoutException:
    print("Error: Serial write timed out. Is the ESP32 disconnected?")
    ser.close()