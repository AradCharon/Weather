import requests
from datetime import datetime

API_KEY = "2da96e8ad076ac98cfdaf97e80642e87"
CITY = "Tehran"

current_url = "http://api.openweathermap.org/data/2.5/weather"
current_params = {
    "q": CITY,
    "units": "metric",
    "appid": API_KEY
}

current_response = requests.get(current_url, params=current_params)
current_data = current_response.json()

if "main" in current_data:
    print("=== Current Weather ===")
    print("Temperature: " + str(current_data['main']['temp']) + "°C")
    print("Feels like: " + str(current_data['main']['feels_like']) + "°C")
    print("Weather: " + current_data['weather'][0]['description'])
    print("Humidity: " + str(current_data['main']['humidity']) + "%")
    print("Wind speed: " + str(current_data['wind']['speed']) + " m/s\n")
else:
    print("Error fetching current weather: " + current_data.get("message", "Unknown error"))

forecast_url = "http://api.openweathermap.org/data/2.5/forecast"
forecast_params = {
    "q": CITY,
    "units": "metric",
    "appid": API_KEY
}

forecast_response = requests.get(forecast_url, params=forecast_params)
forecast_data = forecast_response.json()

if "list" in forecast_data:
    print("=== 5-Day Forecast (3-hour intervals) ===")
    for entry in forecast_data['list']:
        dt = datetime.utcfromtimestamp(entry['dt']).strftime('%Y-%m-%d %H:%M')
        print("Time: " + dt)
        print("Temp: " + str(entry['main']['temp']) + "°C")
        print("Feels like: " + str(entry['main']['feels_like']) + "°C")
        print("Weather: " + entry['weather'][0]['description'])
        print("Humidity: " + str(entry['main']['humidity']) + "%")
        print("Wind speed: " + str(entry['wind']['speed']) + " m/s\n")
else:
    print("Error fetching forecast: " + forecast_data.get("message", "Unknown error"))
