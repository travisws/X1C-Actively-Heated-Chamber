from flask import Flask, render_template, jsonify, request
import threading
import time
import RPi.GPIO as GPIO
from smbus2 import SMBus, i2c_msg

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)

# Global variable to store set temperature
set_temp = 25.0
timer_end_time = None

# Simulated AHT20 sensor reading
def read_sensor():
    return {"temperature": 25.0, "humidity": 50.0}

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
    set_temp = float(request.form.get("set_temp", 25.0))
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
