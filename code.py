import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import Adafruit_MCP3008

# GPIO Pin Setup
GPIO.setmode(GPIO.BCM)
WATER_PUMP_PIN = 18
LIGHT_PIN = 23
AERATION_PIN = 24
GPIO.setup(WATER_PUMP_PIN, GPIO.OUT)
GPIO.setup(LIGHT_PIN, GPIO.OUT)
GPIO.setup(AERATION_PIN, GPIO.OUT)

# MCP3008 Setup (For Analog Sensors)
CLK = 11  # Clock pin
MISO = 9  # Data output pin
MOSI = 10 # Data input pin
CS = 8    # Chip select
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Sensor Setup
DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4
WATER_LEVEL_PIN = 17
GPIO.setup(WATER_LEVEL_PIN, GPIO.IN)

# Functions to read sensors
def get_temperature_humidity():
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    return temperature, humidity

def get_water_level():
    return GPIO.input(WATER_LEVEL_PIN)

def get_ph_level():
    ph_level = 6.8  # Placeholder, replace with actual sensor read
    return ph_level

def get_dissolved_oxygen():
    do_level = 7.5  # Placeholder, replace with actual sensor read
    return do_level

def get_ec_level():
    ec_channel = 0  # Assuming EC sensor is connected to channel 0 of MCP3008
    ec_value = mcp.read_adc(ec_channel)
    return ec_value

def get_npk_values():
    npk_channel = 1  # Assuming NPK sensor is connected to channel 1 of MCP3008
    npk_value = mcp.read_adc(npk_channel)
    return npk_value

def get_pressure_value():
    pressure_channel = 2  # Assuming pressure sensor is connected to channel 2 of MCP3008
    pressure_value = mcp.read_adc(pressure_channel)
    return pressure_value

def get_light_level():
    light_channel = 3  # Assuming light sensor is connected to channel 3 of MCP3008
    light_value = mcp.read_adc(light_channel)
    return light_value

def get_soil_moisture():
    soil_moisture_channel = 4  # Assuming soil moisture sensor is connected to channel 4 of MCP3008
    soil_moisture_value = mcp.read_adc(soil_moisture_channel)
    return soil_moisture_value

# Control Functions
def water_pump_control(state):
    if state:
        GPIO.output(WATER_PUMP_PIN, GPIO.HIGH)
        print("Water pump ON")
    else:
        GPIO.output(WATER_PUMP_PIN, GPIO.LOW)
        print("Water pump OFF")

def light_control(state):
    if state:
        GPIO.output(LIGHT_PIN, GPIO.HIGH)
        print("Light ON")
    else:
        GPIO.output(LIGHT_PIN, GPIO.LOW)
        print("Light OFF")

def aeration_control(state):
    if state:
        GPIO.output(AERATION_PIN, GPIO.HIGH)
        print("Aeration ON")
    else:
        GPIO.output(AERATION_PIN, GPIO.LOW)
        print("Aeration OFF")

# Main loop
try:
    while True:
        # Read sensor data
        temperature, humidity = get_temperature_humidity()
        water_level = get_water_level()
        ph_level = get_ph_level()
        do_level = get_dissolved_oxygen()
        ec_value = get_ec_level()
        npk_value = get_npk_values()
        pressure_value = get_pressure_value()
        light_value = get_light_level()
        soil_moisture = get_soil_moisture()

        # Log sensor data
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Water Level: {'Low' if water_level == 0 else 'OK'}")
        print(f"pH: {ph_level}, DO: {do_level}, EC: {ec_value}, NPK: {npk_value}")
        print(f"Pressure: {pressure_value}, Light: {light_value}, Soil Moisture: {soil_moisture}")

        # Control logic based on thresholds

        # Water Pump Control
        if water_level == 0:  # If water level is too low, turn off the pump
            water_pump_control(False)
        else:
            if humidity < 50 or soil_moisture < 500:  # Adjust soil moisture threshold as per sensor calibration
                water_pump_control(True)
            else:
                water_pump_control(False)

        # Light Control (based on light level or humidity)
        if light_value < 300:  # Assuming 300 is the threshold for light intensity
            light_control(True)
        else:
            light_control(False)

        # Aeration Control (based on dissolved oxygen levels)
        if do_level < 6:
            aeration_control(True)
        else:
            aeration_control(False)

        # Sleep for 60 seconds before the next reading
        time.sleep(60)

except KeyboardInterrupt:
    print("Program terminated")
    GPIO.cleanup()