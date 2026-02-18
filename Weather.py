import requests
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

API_KEY = "2da96e8ad076ac98cfdaf97e80642e87"
current_url = "http://api.openweathermap.org/data/2.5/weather"
forecast_url = "http://api.openweathermap.org/data/2.5/forecast"

def get_current_weather(city):
    params = {"q": city, "units": "metric", "appid": API_KEY}
    try:
        response = requests.get(current_url, params=params)
        data = response.json()
        if "main" in data:
            print(f"\n=== Current Weather in {city.title()} ===")
            print(f"Temperature: {data['main']['temp']}°C")
            print(f"Feels like: {data['main']['feels_like']}°C")
            print(f"Weather: {data['weather'][0]['description']}")
            print(f"Humidity: {data['main']['humidity']}%")
            print(f"Wind speed: {data['wind']['speed']} m/s")
            return data
        else:
            print(f"Error for {city}: {data.get('message', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException:
        print(f"Network error for {city}")
        return None

def get_forecast(city):
    params = {"q": city, "units": "metric", "appid": API_KEY}
    try:
        response = requests.get(forecast_url, params=params)
        data = response.json()
        if "list" not in data:
            print(f"Error for {city}: {data.get('message', 'Unknown error')}")
            return None, None, None, None, None, None
        times, temps, feels_like, humidities, wind_speeds, weather_desc = [], [], [], [], [], []
        for entry in data['list']:
            dt = datetime.utcfromtimestamp(entry['dt'])
            times.append(dt)
            temps.append(entry['main']['temp'])
            feels_like.append(entry['main']['feels_like'])
            humidities.append(entry['main']['humidity'])
            wind_speeds.append(entry['wind']['speed'])
            weather_desc.append(entry['weather'][0]['description'])
        return times, temps, feels_like, humidities, wind_speeds, weather_desc
    except requests.exceptions.RequestException:
        print(f"Network error for {city}")
        return None, None, None, None, None, None

def display_forecast_details(city, times, temps, feels_like, humidities, wind_speeds, weather_desc, max_entries=8):
    print(f"\n=== 5-Day Forecast for {city.title()} (3-hour intervals) ===")
    for i in range(min(max_entries, len(times))):
        print(f"Time: {times[i].strftime('%Y-%m-%d %H:%M')}")
        print(f"Temp: {temps[i]}°C")
        print(f"Feels like: {feels_like[i]}°C")
        print(f"Weather: {weather_desc[i]}")
        print(f"Humidity: {humidities[i]}%")
        print(f"Wind speed: {wind_speeds[i]} m/s\n")

def plot_single_city(times, temps, feels_like, humidities, wind_speeds, city):
    plt.figure()
    plt.plot(times, temps, label="Temperature (°C)", marker='o', color='red', linewidth=2)
    plt.plot(times, feels_like, label="Feels Like (°C)", marker='s', linestyle='--', color='orange', linewidth=2)
    plt.title(f"Temperature Forecast for {city.title()}")
    plt.ylabel("Temperature (°C)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(times, humidities, label="Humidity (%)", marker='^', color='blue', linewidth=2)
    plt.plot(times, wind_speeds, label="Wind Speed (m/s)", marker='d', color='green', linewidth=2)
    plt.title(f"Humidity & Wind Speed Forecast for {city.title()}")
    plt.ylabel("Values")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

def plot_two_cities(times1, temps1, feels_like1, humidities1, wind_speeds1,
                    times2, temps2, feels_like2, humidities2, wind_speeds2,
                    city1, city2):
    plt.figure()
    plt.plot(times1, temps1, label=f"{city1.title()} Temp", marker='o', color='red', linewidth=2)
    plt.plot(times1, feels_like1, label=f"{city1.title()} Feels Like", marker='s', linestyle='--', color='orange', linewidth=2)
    plt.plot(times2, temps2, label=f"{city2.title()} Temp", marker='x', color='blue', linewidth=2)
    plt.plot(times2, feels_like2, label=f"{city2.title()} Feels Like", marker='d', linestyle='--', color='cyan', linewidth=2)
    plt.title(f"Temperature Comparison: {city1.title()} vs {city2.title()}")
    plt.ylabel("Temperature (°C)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

    plt.figure()
    plt.plot(times1, humidities1, label=f"{city1.title()} Humidity", marker='o', color='blue', linewidth=2)
    plt.plot(times2, humidities2, label=f"{city2.title()} Humidity", marker='x', color='green', linewidth=2)
    plt.title(f"Humidity Comparison: {city1.title()} vs {city2.title()}")
    plt.ylabel("Humidity (%)")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

    temp_diff = np.array(temps1) - np.array(temps2)
    feels_diff = np.array(feels_like1) - np.array(feels_like2)

    plt.figure()
    plt.plot(times1, wind_speeds1, label=f"{city1.title()} Wind Speed", marker='o', color='green', linewidth=2)
    plt.plot(times2, wind_speeds2, label=f"{city2.title()} Wind Speed", marker='x', color='purple', linewidth=2)
    plt.plot(times1, temp_diff, label="Temp Difference", marker='s', color='red', linewidth=2)
    plt.plot(times1, feels_diff, label="Feels Like Difference", marker='d', linestyle='--', color='orange', linewidth=2)
    plt.axhline(0, color='black', linewidth=1)
    plt.title(f"Wind & Temperature Differences: {city1.title()} vs {city2.title()}")
    plt.ylabel("Values")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    plt.gca().xaxis.set_major_locator(mdates.HourLocator(interval=12))
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.show()

while True:
    print("\n=== Weather App Menu ===")
    print("1 - Single city forecast")
    print("2 - Compare two cities")
    print("0 - Exit")
    choice = input("Choose option: ").strip()
    
    if choice == "1":
        CITY = input("Enter city name: ").strip().lower()
        get_current_weather(CITY)
        times, temps, feels_like, humidities, wind_speeds, weather_desc = get_forecast(CITY)
        if times:
            display_forecast_details(CITY, times, temps, feels_like, humidities, wind_speeds, weather_desc)
            plot_single_city(times, temps, feels_like, humidities, wind_speeds, CITY)
        input("Press Enter to return to menu...")

    elif choice == "2":
        CITY1 = input("Enter first city name: ").strip().lower()
        CITY2 = input("Enter second city name: ").strip().lower()
        get_current_weather(CITY1)
        get_current_weather(CITY2)
        times1, temps1, feels_like1, humidities1, wind_speeds1, _ = get_forecast(CITY1)
        times2, temps2, feels_like2, humidities2, wind_speeds2, _ = get_forecast(CITY2)
        if times1 and times2:
            display_forecast_details(CITY1, times1, temps1, feels_like1, humidities1, wind_speeds1, _)
            display_forecast_details(CITY2, times2, temps2, feels_like2, humidities2, wind_speeds2, _)
            plot_two_cities(times1, temps1, feels_like1, humidities1, wind_speeds1,
                            times2, temps2, feels_like2, humidities2, wind_speeds2,
                            CITY1, CITY2)
        input("Press Enter to return to menu...")

    elif choice == "0":
        print("Exiting...")
        break
    else:
        print("Invalid choice.")
