# ambient-light
Created an immersive ambient background lighting system that dynamically extends screen colors to the surrounding environment. The system samples display pixels in real-time and maps them to an addressable RGB LED strip behind the monitor.

# Hardware Used

- ESP32-C3 SuperMini
- WS2812B RGB LED Strip
- USB Cable
- PC/Laptop running Python
  
# Hardware Setup
- upload .ino file in the esp32
- connect led data pin to pin number 2
- also connect 5v and gnd
- plug in usb check for port number
- edit port number in py script and hit RUN
  
# Features

- Real-time screen edge color detection
- Fast serial communication
- Custom LED layout support
- Lightweight Python implementation
- Easy to modify and expand

# LED Layout

Current configuration:

| Position | Number of LEDs |
| Bottom | 16 |
| Right | 11 |
| Top | 16 |
| Left | 11 |

Total LEDs: **54**

# Python Dependencies

Install required libraries:
```bash
pip install pyserial numpy pillow
```
# Wiring

| WS2812B | ESP32-C3 SuperMini |
|---|---|
| DIN | GPIO Pin used in firmware |
| 5V | 5V |
| GND | GND |

> Recommended: Use an external 5V power supply for larger LED counts.

# ESP32 Firmware
The ESP32 reads RGB data from serial communication and updates the LED strip.
Recommended libraries:
- FastLED
- Adafruit NeoPixel

### Windows
```python
SERIAL_PORT = 'COM3'
```
### Linux
```python
SERIAL_PORT = '/dev/ttyUSB0'
```
### macOS
```python
SERIAL_PORT = '/dev/cu.usbserial'
```
# Running the Project

Run the Python script:
```bash
python ambient_light.py
```
Press:
```bash
Ctrl + C
```
to stop the program safely.

# How It Works

1. Captures the screen using `PIL.ImageGrab`
2. Divides screen edges into LED regions
3. Calculates average RGB values
4. Sends RGB data over serial
5. ESP32 updates the WS2812B strip in real time

# RGB Color Order

Current transmission order:
```python
bytes([g, r, b])
```
If colors appear incorrect, try:
```python
bytes([r, g, b])
```
or
```python
bytes([b, g, r])
```
depending on your LED strip configuration.

# Performance Notes

- `ImageGrab` is the main performance bottleneck
- Reducing capture resolution can improve FPS
- Removing delays improves responsiveness

Optional optimization:
```python
screen = screen.resize((300, 200))
```

# Future Improvements

- Audio reactive mode
- Wireless streaming over WiFi
- Multi-monitor support
- Dynamic brightness control
- GPU accelerated screen capture
- Smoothing and transition effects

# Demo Applications

- Gaming setups
- Ambient movie lighting
- Music visualization
- Smart desk lighting
- RGB room setups
