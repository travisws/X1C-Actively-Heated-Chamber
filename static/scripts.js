$(document).ready(function () {
    // Update readings every 5 seconds
    setInterval(updateReadings, 5000);

    // Set Temperature Button
    $("#setTempBtn").click(function () {
        $.post("/update_temp", { temperature: $("#setTemp").val() }, function (data) {
            if (data.success) {
                alert("Temperature set successfully!");
            } else {
                alert("Error setting temperature. Try again.");
            }
        });
    });

    // Set Timer Button
    $("#setTimerBtn").click(function () {
        $.post("/set_timer", { timer: $("#setTimer").val() }, function (data) {
            if (data.success) {
                alert("Timer set successfully!");
            } else {
                alert("Error setting timer. Ensure format is HH:MM.");
            }
        });
    });

    // Stop Heating Button
    $("#stopBtn").click(function () {
        $.post("/stop_heating", function (data) {
            if (data.success) {
                alert("Heating stopped successfully!");
            } else {
                alert("Error stopping heating. Try again.");
            }
        });
    });
});

function updateReadings() {
    $.get("/get_data", function (data) {
        $("#currentTemp").text(data.temp.toFixed(1));
        $("#currentHumidity").text(data.humidity.toFixed(1));
    });
}

// Check and apply the user's preference from local storage
window.onload = function () {
    if (localStorage.getItem('mode') === 'light') {
        document.body.classList.add('light-mode');
    }
}

function toggleMode() {
    if (document.body.classList.contains('light-mode')) {
        document.body.classList.remove('light-mode');
        localStorage.setItem('mode', 'dark');
    } else {
        document.body.classList.add('light-mode');
        localStorage.setItem('mode', 'light');
    }
}

// Toggle between light and dark modes
$("#toggleModeBtn").click(function () {
    $("body").toggleClass("light-mode");
    // Change button text based on mode
    if ($("body").hasClass("light-mode")) {
        $("#toggleModeBtn").text("Toggle Dark Mode");
    } else {
        $("#toggleModeBtn").text("Toggle Light Mode");
    }
});