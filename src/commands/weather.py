import requests
from colorama import Fore


WMO_CODES = {
    "0": "Clear Sky",
    "1": "Mainly Clear",
    "2": "Partly Cloudy",
    "3": "Cloud Overcast",
    "45": "Foggy",
    "48": "Depositing Rime Fog",
    "51": "Light Drizzle",
    "53": "Moderate Drizzle",
    "55": "Intense Drizzle",
    "61": "Slight Rain",
    "63": "Moderate Rain",
    "65": "Heavy Rain",
    "66": "Light Freezing Rain",
    "67": "Heavy Freezing Rain",
    "71": "Slight Snowfall",
    "73": "Moderate Snowfall",
    "75": "Heavy Snowfall",
    "77": "Snow grains",
    "80": "Slight Rain Showers",
    "81": "Moderate Rain Showers",
    "82": "Violent Rain Showers",
    "85": "Slight Snow Showers",
    "86": "Heavy Snow Showers",
    "95": "Slight Thunderstorm",
    "96": "Thunderstorm with Slight Hail",
    "99": "Thunderstorm with Heavt Hail",
}

class Weather:
    def __init__(self, client) -> None:
        self.client = client
        # Latitude and Longitude for Weather Data
        Latitude: float = 0.0
        Longitude: float = 0.0

        # Get Geolocation Data
        print(f"{Fore.LIGHTYELLOW_EX}Getting Geolocation Data{Fore.RESET}")
        response: requests.Response = requests.get("https://www.ipinfo.io/loc")
        Latitude, Longitude = (float(x) for x in response.text.split(",")) # Don't try and catch; If this fails just don't load module


        @client.command(regex=r"temperature")
        def get_temp(query) -> None:
            """
                Get the temperature for today
            """
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&current_weather=true")
            temp = response.json()["current_weather"]["temperature"]
            client.speak(f"The current temperature is {temp} °C")
            
        @client.command(regex=r"weather")
        def get_weather(query) -> None:
            """
                Get the most severe weather condition on the given day
            """
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&current_weather=true")
            weather_code = response.json()["current_weather"]["weathercode"]
            client.speak(f"The current weather status is: {WMO_CODES[weather_code]}")


        @client.command(regex=r"rain")
        def get_rain(query) -> None:
            """
                Get the number of hours with rain for the day
            """
            print(f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&precipitation_hours=true")
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={Latitude}&longitude={Longitude}&daily=precipitation_hours&timezone=auto")
            precip_hours = response.json()["daily"]["precipitation_hours"]["0"]
            client.speak(f"The number of hours with rain for today is approximately {precip_hours} hours")

    
def setup(client) -> None:
    client.add_class(Weather(client))