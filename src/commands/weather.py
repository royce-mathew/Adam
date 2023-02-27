class Weather:
    def __init__(self, client) -> None:
        self.client = client;
        

    


def setup(client):
    client.add_command(Weather(client))