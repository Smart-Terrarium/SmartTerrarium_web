var chart = null;
var maxColumns = 8;

var socket = new WebSocket('ws://localhost:8000/device/sensor/data');

socket.onmessage = function (e) {
    var wsData = JSON.parse(e.data);

    var device_dict = {};
    for (var device_id in wsData) { // iteracja po kluczach w obiekcie data
        // Utworzenie nowego obiektu dla urządzenia, jeśli nie istnieje
        if (!device_dict.hasOwnProperty(device_id)) {
            device_dict[device_id] = {};
        }
        for (var sensor_id in wsData[device_id]) { // iteracja po kluczach w obiekcie dla danego urządzenia
            // Dodanie nowego czujnika dla urządzenia, jeśli nie istnieje
            if (!device_dict[device_id].hasOwnProperty(sensor_id)) {
                device_dict[device_id][sensor_id] = [];
            }
            device_dict[device_id][sensor_id].push([wsData[device_id][sensor_id]['timestamp'], wsData[device_id][sensor_id]['value']]);
            // Jeśli liczba wartości przekracza 5, usunięcie najstarszej wartości z tablicy
            if (device_dict[device_id][sensor_id].length > maxColumns) {
                device_dict[device_id][sensor_id].shift();
            }
        }
    }

    var firstSensorData = device_dict[Object.keys(device_dict)[0]][Object.keys(device_dict[Object.keys(device_dict)[0]])[0]];
    // Pobierz wartości timestamp i wartość dla pierwszego sensora pierwszego urządzenia
    var labels = chart ? chart.data.labels : [];
    var data = chart ? chart.data.datasets[0].data : [];

    if (labels.length < maxColumns) {
        labels.push(firstSensorData[firstSensorData.length - 1][0]);
        data.push(firstSensorData[firstSensorData.length - 1][1]);
    } else {
        labels.shift();
        data.shift();
        labels.push(firstSensorData[firstSensorData.length - 1][0]);
        data.push(firstSensorData[firstSensorData.length - 1][1]);
    }

    // Aktualizacja wartości temperatury w HTML
    var temperatureValue = firstSensorData[firstSensorData.length - 1][1];
    var formattedTemperature = temperatureValue.toFixed(1) + "°C"; // Zaokrąglamy do jednego miejsca po przecinku i dodajemy znak stopnia Celsjusza
    document.getElementById('temperatureValue').textContent = formattedTemperature;


    var secondSensorData = device_dict[Object.keys(device_dict)[0]][Object.keys(device_dict[Object.keys(device_dict)[0]])[1]];
    // Pobierz wartości timestamp i wartość dla drugiego sensora pierwszego urządzenia
    var secondLabels = chart ? secondChart.data.labels : [];
    var secondData = chart ? secondChart.data.datasets[0].data : [];

    if (secondLabels.length < maxColumns) {
        secondLabels.push(secondSensorData[secondSensorData.length - 1][0]);
        secondData.push(secondSensorData[secondSensorData.length - 1][1]);
    } else {
        secondLabels.shift();
        secondData.shift();
        secondLabels.push(secondSensorData[secondSensorData.length - 1][0]);
        secondData.push(secondSensorData[secondSensorData.length - 1][1]);
    }

    // Aktualizacja wartości temperatury w HTML
    var secondTemperatureValue = secondSensorData[secondSensorData.length - 1][1];
    var secondFormattedTemperature = secondTemperatureValue.toFixed(1) + "°C"; // Zaokrąglamy do jednego miejsca po przecinku i dodajemy znak stopnia Celsjusza
    document.getElementById('secondTemperatureValue').textContent = secondFormattedTemperature;

    if (!chart) {
        const ctx = document.getElementById('myChart');
        chart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Terrarium Temperature: ' + formattedTemperature,
                    data: data,
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                fill: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 15,
                        max: 40
                    }
                },
                animation: {
                    duration: 0 // Ustawienie czasu trwania animacji na 0
                }
            }
        });

        const secondCtx = document.getElementById('secondChart');
        secondChart = new Chart(secondCtx, {
            type: 'line',
            data: {
                labels: secondLabels,
                datasets: [{
                    label: 'Second Sensor Temperature: ' + secondFormattedTemperature,
                    data: secondData,
                    borderWidth: 1,
                    backgroundColor: 'rgba(255, 165, 0, 0.5)'
                }]
            },
            options: {
                responsive: true,
                fill: true,
                maintainAspectRatio: false,
                scales: {
                    y: {
                        beginAtZero: false,
                        min: 15,
                        max: 40
                    }
                },
                animation: {
                    duration: 0 // Ustawienie czasu trwania animacji na 0
                }
            }
        });
    } else {
        chart.data.labels = labels;
        chart.data.datasets[0].data = data;
        chart.data.datasets[0].label = 'Terrarium Temperature: ' + formattedTemperature;
        chart.options.animation.duration = 0; // Ustawienie czasu trwania animacji na 0
        chart.update();

        secondChart.data.labels = secondLabels;
        secondChart.data.datasets[0].data = secondData;
        secondChart.data.datasets[0].label = 'Second Sensor Temperature: ' + secondFormattedTemperature;
        secondChart.options.animation.duration = 0; // Ustawienie czasu trwania animacji na 0
        secondChart.update();
    }


};