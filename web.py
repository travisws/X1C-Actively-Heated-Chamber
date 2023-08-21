from flask import Flask, render_template, jsonify, request
import threading
import time
import RPi.GPIO as GPIO
from smbus2 import SMBus, i2c_msg

app = Flask(__name__)

# Setting up the GPIO pins for the Raspberry Pi
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.output(4, GPIO.LOW)

# Initial values for temperature, humidity, and set temperature
current_temp = 0
current_humidity = 0
set_temp = 25  # default temperature in Celsius
end_time = None  # for timer functionality

class AHT20:
    # Constants related to the AHT20 temperature and humidity sensor
    _AHT20_ADDRESS = 0x38
    _AHT20_CALIBRATE = [0xE1, 0x08, 0x00]
    _AHT20_START = [0xAC, 0x33, 0x00]

    def __init__(self):
        # Initializing the I2C bus
        self.bus = SMBus(1)
        self.calibrate()

    def calibrate(self):
        # Sending calibration command to the AHT20 sensor
        self.bus.write_i2c_block_data(self._AHT20_ADDRESS, 0, self._AHT20_CALIBRATE)
        time.sleep(0.5)

    def read(self):
        # Reading temperature and humidity values from the AHT20 sensor
        self.bus.write_i2c_block_data(self._AHT20_ADDRESS, 0, self._AHT20_START)
        time.sleep(0.1)
        data = self.bus.read_i2c_block_data(self._AHT20_ADDRESS, 0, 6)
        humidity = ((data[1] << 12) | (data[2] << 4) | (data[3] >> 4)) * 100 / (1 << 20)
        temperature = (((data[3] & 0x0F) << 16) | (data[4] << 8) | data[5]) * 200 / (1 << 20) - 50
        return temperature, humidity

def read_aht20_data():
    # Continuous reading of temperature and humidity data
    global current_temp, current_humidity
    sensor = AHT20()
    while True:
        current_temp, current_humidity = sensor.read()
        # Control the GPIO output based on temperature
        if current_temp > set_temp:
            GPIO.output(4, GPIO.LOW)
        else:
            GPIO.output(4, GPIO.HIGH)
        time.sleep(5)

def timer_monitor():
    # Monitor if the timer has reached its end time
    global end_time
    while True:
        if end_time and datetime.now() > end_time:
            GPIO.output(4, GPIO.LOW)
        time.sleep(10)

@app.route('/')
def index():
    # Render the main webpage
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    return jsonify({'temp': current_temp, 'humidity': current_humidity})

# API endpoint to update the target temperature
@app.route('/update_temp', methods=['POST'])
def update_temp():
    global set_temp
    try:
        set_temp = float(request.form.get('temperature'))
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

# API endpoint to set a timer for the heater
@app.route('/set_timer', methods=['POST'])
def set_timer():
    global end_time
    timer_value = request.form.get('timer')
    try:
        hours, minutes = map(int, timer_value.split(":"))
        end_time = datetime.now() + timedelta(hours=hours, minutes=minutes)
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

# API endpoint to immediately stop the heating
@app.route('/stop_heating', methods=['POST'])
def stop_heating():
    GPIO.output(4, GPIO.LOW)
    return jsonify({'success': True})

# Start reading data and monitoring timer in separate threads
if __name__ == '__main__':
    threading.Thread(target=read_aht20_data).start()
    threading.Thread(target=timer_monitor).start()
    app.run(host='0.0.0.0')
