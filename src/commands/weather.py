import requests

City = "Oshawa"
Lat = 43.90
Long = -73.85

class Weather:
    def __init__(self, client) -> None:
        self.client = client

        @client.command(regex=r"weather")
        def test_weather(query) -> None:
            response = requests.get(f"https://api.open-meteo.com/v1/forecast?latitude={Lat}&longitude={Long}&current_weather=true")
            print(response.text)
            print("Running weather app!!!")

    
def setup(client) -> None:
    client.add_class(Weather(client))