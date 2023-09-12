from flask import Flask, render_template, jsonify, request
import threading
import time
import RPi.GPIO as GPIO
from smbus2 import SMBus, i2c_msg

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

# Global variable to store set temperature
set_temp = 5.0
timer_end_time = None

# Initialize I2C bus
bus = SMBus(1)

# AHT20 sensor I2C address
AHT20_ADDR = 0x38

# Initialize AHT20 sensor
def initialize_sensor():
    bus.write_i2c_block_data(AHT20_ADDR, 0xE1, [0x08, 0x00])

# Read temperature and humidity from AHT20
def read_sensor():
    initialize_sensor()
    bus.write_i2c_block_data(AHT20_ADDR, 0xAC, [0x33, 0x00])
    time.sleep(0.25)
    data = bus.read_i2c_block_data(AHT20_ADDR, 0x00, 6)
    
    humidity = ((data[1] << 12) + (data[2] << 4) + (data[3] >> 4)) * 100 / 0x100000
    temperature = (((data[3] & 0x0F) << 16) + (data[4] << 8) + data[5]) * 200 / 0x100000 - 50
    
    humidity = round(humidity, 2)
    temperature = round(temperature, 2)

    return {"temperature": temperature, "humidity": humidity}

# Control relay
def control_relay():
    global set_temp, timer_end_time
    while True:
        sensor_data = read_sensor()
        if sensor_data["temperature"] >= set_temp:
            GPIO.output(4, GPIO.LOW)
        else:
            GPIO.output(4, GPIO.HIGH)

        if timer_end_time and time.time() >= timer_end_time:
            GPIO.output(4, GPIO.LOW)
            set_temp = 5.0
            timer_end_time = None

        time.sleep(5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_sensor_data')
def get_sensor_data():
    return jsonify(read_sensor())

@app.route('/stop_relay')
def stop_relay():
    global set_temp
    GPIO.output(4, GPIO.LOW)
    set_temp = 5.0
    return jsonify({"status": "stopped"})

@app.route('/set_temp', methods=['POST'])
def set_temperature():
    global set_temp
    set_temp = float(request.form.get("set_temp", 5.0))
    return jsonify({"status": "temperature set"})

@app.route('/set_timer', methods=['POST'])
def set_timer():
    global timer_end_time
    hh_mm = request.form.get('time')
    hh, mm = map(int, hh_mm.split(":"))
    timer_end_time = time.time() + hh * 3600 + mm * 60
    return jsonify({"status": "timer set"})

@app.route('/reset_timer')
def reset_timer():
    global timer_end_time
    timer_end_time = None
    return jsonify({"status": "timer reset"})

if __name__ == '__main__':
    t = threading.Thread(target=control_relay)
    t.start()
    app.run(host='0.0.0.0', port=5000)