async function getWeather() {
    const city = document.getElementById("city").value;
    const error = document.getElementById("error");
    const card = document.getElementById("weather-card");

    error.textContent = "";
    card.classList.add("hidden");

    if (!city) {
        error.textContent = "Please enter a city name";
        return;
    }

    try {
        const res = await fetch(`/weather?city=${city}`);
        const data = await res.json();

        if (data.error) {
            error.textContent = data.error;
            return;
        }

        document.getElementById("cityName").textContent = data.city;
        document.getElementById("temperature").textContent = `${data.temp}°C`;
        document.getElementById("condition").textContent = data.condition;
        document.getElementById("humidity").textContent = `Humidity: ${data.humidity}%`;
        document.getElementById("wind").textContent = `Wind: ${data.wind} m/s`;
        document.getElementById("updated").textContent =
            "Last Updated: " + new Date().toLocaleString();

        card.classList.remove("hidden");

    } catch (err) {
        error.textContent = "Failed to fetch data";
    }
}
