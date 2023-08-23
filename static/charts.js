    fetch(`http://localhost:8000/device/{{ device_id }}/sensor`, {
    method: 'GET',
    headers: {
        'Authorization': `Bearer {{ access_token }}`,
        'Content-Type': 'application/json'
    }
})
.then(response => response.json())
.then(sensorData => {
    // Tutaj możesz przetworzyć dane zwrócone z serwera
    console.log(sensorData);
})
.catch(error => {
    console.error('Błąd podczas żądania:', error);
});
        var chart = null;
        var number_charts = {};
        var maxColumns = 8;
        var sensors_counter = 1;
        var device_dict = {};
        var isFirstMessage = true;
        var sensorsData = null;
        var message = {
            token: "{{ access_token }}"
        };

        console.log(JSON.stringify(message));

        var socket = new WebSocket('ws://localhost:8000/device/{{ device_id }}/sensor/data');
        socket.onopen = function () {
            socket.send(JSON.stringify(message));
        };

        socket.onmessage = function (e) {
            var wsData = JSON.parse(e.data);

            // Licznik ilości sensorów

            //Iteracja urządzenia
            // Iteracja po device_id
            if (isFirstMessage) { // Sprawdzanie, czy to jest pierwsza wiadomość
                isFirstMessage = false; // Ustawienie flagi na false po otrzymaniu pierwszej wiadomości

                // Licznik ilości sensorów
                for (var mac_address in wsData) {
                    if (!device_dict.hasOwnProperty(mac_address)) {
                        device_dict[mac_address] = {};
                    }
                    for (var sensor_id in wsData[mac_address]) {
                        if (!device_dict[mac_address].hasOwnProperty(sensor_id)) {
                            device_dict[mac_address][sensor_id] = {};
                            device_dict[mac_address][sensor_id]['timestamp'] = [];
                            device_dict[mac_address][sensor_id]['value'] = [];
                            sensors_counter++;
                        }
                        device_dict[mac_address][sensor_id]['timestamp'].push(wsData[mac_address][sensor_id]['timestamp']);
                        device_dict[mac_address][sensor_id]['value'].push(wsData[mac_address][sensor_id]['value']);
                        if (device_dict[mac_address][sensor_id]['timestamp'].length > maxColumns) {
                            device_dict[mac_address][sensor_id]['timestamp'].shift();
                        }
                        if (device_dict[mac_address][sensor_id]['value'].length > maxColumns) {
                            device_dict[mac_address][sensor_id]['value'].shift();
                        }
                    }
                }
                console.log("Suma ilości zmiennych sensor_id: " + (sensors_counter - 1));
                console.log(device_dict);

                for (var x in device_dict) {
                    for (var y in device_dict[x]) {
                        const ctx2 = document.getElementById("myCharts")
                        var ctx = document.createElement('canvas');
                        ctx.id = y
                        ctx2.appendChild(ctx)
                        ctx_now = document.getElementById(y);
                        number_charts[y] = new Chart(ctx_now, {
                                type: 'line',
                                data: {
                                    labels: [2],
                                    datasets: [{
                                        label: 'Terrarium Temperature: ',
                                        data: [1],
                                        borderWidth: 1
                                    }]
                                },
                                options: {
                                    responsive: true,
                                    fill: true,
                                    maintainAspectRatio: true,
                                    scales: {
                                        y: {
                                            beginAtZero: false,
                                            min: 1,
                                            max: 80
                                        }
                                    },
                                    animation: {
                                        duration: 0
                                    }
                                }
                            }
                        )
                    }
                    function formatDate(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = (date.getMonth() + 1).toString().padStart(2, '0');
    const day = date.getDate().toString().padStart(2, '0');
    const hours = date.getHours().toString().padStart(2, '0');
    const minutes = date.getMinutes().toString().padStart(2, '0');
    return `${year}-${month}-${day}, ${hours}:${minutes}`;
}
// Aktualizacja danych wykresu
for (var j in device_dict) {
    for (var z in device_dict[j]) {
        // Przetwarzanie etykiet czasu bez dodatkowej zmiennej
        number_charts[z].data.labels = device_dict[j][z]['timestamp'].map(timestamp => {
            const date = new Date(timestamp);
            const formattedDate = date.toLocaleDateString();
            const formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return `${formattedDate}, ${formattedTime}`;
        });

        number_charts[z].data.datasets[0].data = device_dict[j][z]['value'].map(value => parseFloat(value).toFixed(2));
        number_charts[z].data.datasets[0].label = parseFloat(device_dict[j][z]['value'][0]).toFixed(2);

        // Dodanie etykiety reprezentującej sensor
        const sensorLabel = `Sensor PIN: ${z}` ; // Zaktualizuj to, aby pasowało do twojego źródła danych
        number_charts[z].options.plugins = {
            legend: {
                display: true,
                labels: {
                    generateLabels: function (chart) {
                        const labels = Chart.defaults.plugins.legend.labels.generateLabels(chart);
                        labels[0].text = sensorLabel; // Aktualizacja etykiety
                        return labels;
                    }
                }
            }
        };

        number_charts[z].options.animation.duration = 0;
        number_charts[z].update();
    }
}
                }
            } else {
                // Obsługa pozostałych wiadomości
                // Aktualizacja danych wykresu bez ponownego pobierania sumy sensorów
                for (var j in device_dict) {
    for (var y in device_dict[j]) {
        const updatedTimestamp = wsData[j][y]['timestamp'];
        const updatedValue = wsData[j][y]['value'];

        device_dict[j][y]['timestamp'].push(updatedTimestamp);
        device_dict[j][y]['value'].push(updatedValue);

        if (device_dict[j][y]['timestamp'].length > maxColumns) {
            device_dict[j][y]['timestamp'].shift();
        }
        if (device_dict[j][y]['value'].length > maxColumns) {
            device_dict[j][y]['value'].shift();
        }

        // Aktualizacja wykresu
        number_charts[y].data.labels = device_dict[j][y]['timestamp'].map(timestamp => {
            const date = new Date(timestamp);
            const formattedDate = date.toLocaleDateString();
            const formattedTime = date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return `${formattedDate}, ${formattedTime}`;
        });

        number_charts[y].data.datasets[0].data = device_dict[j][y]['value'].map(value => parseFloat(value).toFixed(2));
        number_charts[y].data.datasets[0].label = parseFloat(updatedValue).toFixed(2);
        number_charts[y].options.animation.duration = 0;
        number_charts[y].update();
    }
}
            }
        };
