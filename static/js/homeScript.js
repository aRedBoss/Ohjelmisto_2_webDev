// Initialize map
const map = L.map('map').setView([60.192059, 24.945831], 6); // Centered on Finland
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

// Get the elements
const storyButton = document.getElementById('storyButton');
const storyPopup = document.getElementById('storyPopup');
const closePopup = document.getElementById('closePopup');

// Show the popup when the button is clicked
storyButton.addEventListener('click', function() {
    storyPopup.style.display = 'flex';  // Show the popup
});

// Close the popup when the close button is clicked
closePopup.addEventListener('click', function() {
    storyPopup.style.display = 'none';  // Hide the popup
});

// Close the popup if the user clicks outside of the popup content
window.addEventListener('click', function(event) {
    if (event.target === storyPopup) {
        storyPopup.style.display = 'none';
    }
});


// Fetch airports and add markers
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

// Fetch and display weather
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
            // Display the Start Game button
            const startGameButton = document.getElementById('startGame');
            startGameButton.style.display = 'block';

            // Add event listener to the "Start Game" button
            startGameButton.addEventListener('click', function() {
                // Navigate to the game page
                window.location.href = '/game';  // This navigates to the /game route
            });
        });
}
