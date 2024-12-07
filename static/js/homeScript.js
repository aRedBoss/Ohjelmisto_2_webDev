const map = L.map('map').setView([60.192059, 24.945831], 6);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

const storyButton = document.getElementById('storyButton');
const storyPopup = document.getElementById('storyPopup');
const closePopup = document.getElementById('closePopup');

storyButton.addEventListener('click', function() {
    storyPopup.style.display = 'flex';
});

closePopup.addEventListener('click', function() {
    storyPopup.style.display = 'none';
});

window.addEventListener('click', function(event) {
    if (event.target === storyPopup) {
        storyPopup.style.display = 'none';
    }
});

fetch('/get_airports?country_code=FI')
    .then(response => response.json())
    .then(data => {
        data.forEach(airport => {
            const marker = L.marker(airport.coords).addTo(map);
            marker.bindPopup(`
                <div class="popup-container">
                    <h3 class="airport-name">${airport.name}</h3>
                    <button class="choose-btn" onclick="showWeather(${airport.coords[0]}, ${airport.coords[1]})">Choose</button>
                </div>
            `);
        });
    });
function showWeather(lat, lon) {
    fetch(`/get_weather?lat=${lat}&lon=${lon}`)
        .then(response => response.json())
        .then(data => {
            const weatherDiv = document.getElementById('weather');
            weatherDiv.innerHTML = `
                <h2>Weather at Selected Location</h2>
                <p><b>Temperature:</b> ${data.main.temp}°C</p>
                <p><b>Condition:</b> ${data.weather[0].description}</p>
            `;
            const startGameButton = document.getElementById('startGame');
            startGameButton.style.display = 'block';

            startGameButton.addEventListener('click', function() {
                window.location.href = '/game';
            });
        });
}
