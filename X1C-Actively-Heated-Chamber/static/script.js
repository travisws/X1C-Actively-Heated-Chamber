// Cache references to frequently accessed elements
const setTempDisplay = document.getElementById('set_temp_display');
const relayStatusElement = document.getElementById('relay_status');
const temperatureElement = document.getElementById('temperature');
const humidityElement = document.getElementById('humidity');
const setTempInput = document.getElementById('set_temp');
const setTimerInput = document.getElementById('set_timer');

let sensorDataInterval;
let statusInterval;

function updateSensorData() {
    fetch('/get_sensor_data')
        .then(response => response.json())
        .then(data => {
            temperatureElement.textContent = data.temperature;
            humidityElement.textContent = data.humidity;
        });
}

function stopRelay() {
    fetch('/stop_relay');
}

function updateStatus() {
    fetch('/get_status')
        .then(response => response.json())
        .then(data => {
            setTempDisplay.textContent = data.set_temp;
            relayStatusElement.style.backgroundColor = data.relay_status ? 'red' : 'gray';
        });
}

function setValue(url, valueKey) {
    const value = valueKey === 'set_temp' ? setTempInput.value : setTimerInput.value;
    fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `${valueKey}=${value}`
    });
}

function resetTimer() {
    fetch('/reset_timer');
}

function startIntervals() {
    sensorDataInterval = setInterval(updateSensorData, 3000);
    statusInterval = setInterval(updateStatus, 3000);
}

function stopIntervals() {
    clearInterval(sensorDataInterval);
    clearInterval(statusInterval);
}

function handleVisibilityChange() {
    if (document.hidden) {
        stopIntervals();
    } else {
        startIntervals();
    }
}

document.addEventListener("visibilitychange", handleVisibilityChange);

// Start the intervals when the page loads
startIntervals();