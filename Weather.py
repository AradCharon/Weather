import requests
from datetime import datetime
import matplotlib.pyplot as plt

API_KEY = "2da96e8ad076ac98cfdaf97e80642e87"
CITY = input("Enter city name: ")

current_url = "http://api.openweathermap.org/data/2.5/weather"
current_params = {
    "q": CITY,
    "units": "metric",
    "appid": API_KEY
}

try:
    current_response = requests.get(current_url, params=current_params)
    current_data = current_response.json()

    if "main" in current_data:
        print("\n=== Current Weather ===")
        print("City: " + CITY)
        print("Temperature: " + str(current_data['main']['temp']) + "°C")
        print("Feels like: " + str(current_data['main']['feels_like']) + "°C")
        print("Weather: " + current_data['weather'][0]['description'])
        print("Humidity: " + str(current_data['main']['humidity']) + "%")
        print("Wind speed: " + str(current_data['wind']['speed']) + " m/s\n")
    else:
        print("Error: " + current_data.get("message", "Unknown error"))
        exit()

except requests.exceptions.RequestException:
    print("Network error: could not fetch current weather.")
    exit()

forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
forecast_params = {
    "q": CITY,
    "units": "metric",
    "appid": API_KEY
}

try:
    forecast_response = requests.get(forecast_url, params=forecast_params)
    forecast_data = forecast_response.json()

    if "list" in forecast_data:
        print("=== 5-Day Forecast (3-hour intervals) ===")

        times = []
        temps = []
        feels_like = []

        for entry in forecast_data['list']:
            dt = datetime.utcfromtimestamp(entry['dt'])
            times.append(dt)
            temps.append(entry['main']['temp'])
            feels_like.append(entry['main']['feels_like'])

            print("Time: " + dt.strftime('%Y-%m-%d %H:%M'))
            print("Temp: " + str(entry['main']['temp']) + "°C")
            print("Feels like: " + str(entry['main']['feels_like']) + "°C")
            print("Weather: " + entry['weather'][0]['description'])
            print("Humidity: " + str(entry['main']['humidity']) + "%")
            print("Wind speed: " + str(entry['wind']['speed']) + " m/s\n")
    else:
        print("Error: " + forecast_data.get("message", "Unknown error"))
        exit()

except requests.exceptions.RequestException:
    print("Network error: could not fetch forecast.")
    exit()

if times and temps:
    plt.figure(figsize=(12,6))
    plt.plot(times, temps, label="Temp (°C)", marker='o')
    plt.plot(times, feels_like, label="Feels Like (°C)", marker='x')
    plt.title("5-Day Forecast for " + CITY)
    plt.xlabel("Time")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
