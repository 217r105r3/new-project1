import requests

def get_weather(city):
    try:
        # Free weather API (no key needed)
        url = f"https://wttr.in/{city}?format=j1"
        response = requests.get(url)
        response.raise_for_status()  # Error if bad response

        data = response.json()

        # Current condition
        current = data["current_condition"][0]
        temp_c = current["temp_C"]
        feels_like_c = current["FeelsLikeC"]
        weather_desc = current["weatherDesc"][0]["value"]
        humidity = current["humidity"]
        wind_kmph = current["windspeedKmph"]

        print("\n---------- Weather Report ----------")
        print(f"City: {city}")
        print(f"Temperature: {temp_c}°C (Feels like {feels_like_c}°C)")
        print(f"Condition : {weather_desc}")
        print(f"Humidity  : {humidity}%")
        print(f"Wind speed: {wind_kmph} km/h")
        print("------------------------------------\n")

    except requests.exceptions.RequestException as e:
        print("\n⚠ Error fetching weather data. Please check your internet or city name.")
        print("Details:", e)

def main():
    print("🌦 Simple Weather App (Python + API)")
    print("Type 'q' to quit.\n")

    while True:
        city = input("Enter city name: ").strip()
        if city.lower() == "q":
            print("Exiting Weather App. Bye! 👋")
            break
        elif city == "":
            print("Please enter a valid city name.\n")
            continue

        get_weather(city)

if __name__ == "__main__":
    main()
