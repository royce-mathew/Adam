class Weather:
    def __init__(self, client) -> None:
        self.client = client;
        self.regex = r""
    
    def main(self):
        print("Running weather app!!!")

    


def setup(client):
    client.add_command(Weather(client))