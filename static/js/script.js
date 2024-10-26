// static/js/scripts.js

document.addEventListener('DOMContentLoaded', function() {
    // Hent den nåværende URL-en for å avgjøre hvilken side som er lastet
    const path = window.location.pathname;
    
    if (path === '/raspberry') {
        fetch('/data')
            .then(response => response.json())
            .then(data => {
                initializeMap(data);
                initializeCharts(data);
                populateTable(data);
            })
            .catch(error => console.error('Error fetching data:', error));
    }
    // Hvis du har annen funksjonalitet for andre sider, kan du legge til her
});

// Initialiser Leaflet-kart
function initializeMap(data) {
    var map = L.map('map').setView([0, 0], 2); // Start med verdensvisning

    // Legg til OpenStreetMap-tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap bidragsytere'
    }).addTo(map);

    // Legg til markører for hver Raspberry Pi
    data.forEach(device => {
        var lat = device.location.latitude;
        var lon = device.location.longitude;
        var region = device.location.region;
        var weather = device.weather.weatherCondition;

        L.marker([lat, lon]).addTo(map)
            .bindPopup(`<b>ID:</b> ${device.raspberryPiId}<br><b>Region:</b> ${region}<br><b>Vær:</b> ${weather}`);
    });
}

// Initialiser Chart.js grafer
function initializeCharts(data) {
    // Batteristørrelse
    var batteryCtx = document.getElementById('batteryChart').getContext('2d');
    var batteryLabels = data.map(device => device.raspberryPiId);
    var batterySizes = data.map(device => device.batterySize_kWh);

    new Chart(batteryCtx, {
        type: 'bar',
        data: {
            labels: batteryLabels,
            datasets: [{
                label: 'Batteristørrelse (kWh)',
                data: batterySizes,
                backgroundColor: 'rgba(54, 162, 235, 0.6)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Batteristørrelse per Raspberry Pi'
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: { 
                    title: {
                        display: true,
                        text: 'Raspberry Pi ID'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Batteristørrelse (kWh)'
                    }
                }
            }
        }
    });

    // Solpanel Størrelse
    var solarCtx = document.getElementById('solarChart').getContext('2d');
    var solarSizes = data.map(device => device.solarPanelSize_peak_kW);

    new Chart(solarCtx, {
        type: 'bar',
        data: {
            labels: batteryLabels,
            datasets: [{
                label: 'Solpanel Størrelse (kW)',
                data: solarSizes,
                backgroundColor: 'rgba(255, 206, 86, 0.6)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Solpanel Størrelse per Raspberry Pi'
                },
                legend: {
                    display: false
                }
            },
            scales: {
                x: { 
                    title: {
                        display: true,
                        text: 'Raspberry Pi ID'
                    }
                },
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Solpanel Størrelse (kW)'
                    }
                }
            }
        }
    });
}

// Populer tabellen med data
function populateTable(data) {
    var tableBody = document.querySelector('#dataTable tbody');

    data.forEach(device => {
        var row = document.createElement('tr');

        row.innerHTML = `
            <td>${device.raspberryPiId}</td>
            <td>${device.location.region}</td>
            <td>${device.batterySize_kWh}</td>
            <td>${device.solarPanelSize_peak_kW}</td>
            <td>${device.averageConsumption_kWh}</td>
            <td>${device.weather.weatherCondition}</td>
        `;

        tableBody.appendChild(row);
    });
}