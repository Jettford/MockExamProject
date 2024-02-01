import copy

from datetime import datetime

from typing import List

from .net import Net

class GeoToolkit:
    def __init__(self, api_key: str = "d548c5ed24604be6a9dd0d989631f783"):
        self.api_key: str = api_key
        self.geo_locate_url: str = "https://api.geoapify.com/v1/geocode/search?format=json&apiKey=" + api_key
        self.weather_url: str = "https://api.open-meteo.com/v1/forecast?hourly=temperature_2m"

    def fetch_lat_lon(self, location: str) -> (float, float):
        # Gather the latitude and longitude of the location

        geo_locate_json = Net.request_json_resource(self.geo_locate_url + "&text=" + location)

        lat: float = geo_locate_json["results"][0]["lat"]
        lon: float = geo_locate_json["results"][0]["lon"]

        return lat, lon

    def fetch_weather(self, lat: float, lon: float) -> dict:
        # Gather the weather data of the location

        return Net.request_json_resource(self.weather_url + f"&latitude={lat}&longitude={lon}")
    
class Weather:
    def __init__(self, lat: float, lon: float):
        self.location: str = ""
        self.geo_toolkit: GeoToolkit = GeoToolkit()

        self.state: dict = self.get_weather(lat, lon)
        self.state_lat_lon: (float, float) = (lat, lon)

        self.rebuild_state()

    def get_weather(self, location: str) -> dict:
        # Gather the weather data of the location by using the geo toolkit, based upon the location string
        
        self.state_lat_lon = self.geo_toolkit.fetch_lat_lon(location)
        return self.geo_toolkit.fetch_weather(*self.state_lat_lon)
    
    def get_weather(self, lat: float, lon: float) -> dict:
        # Gather the weather data of the location by using the geo toolkit, based upon latitude and longitude

        self.state_lat_lon = (lat, lon)
        return self.geo_toolkit.fetch_weather(*self.state_lat_lon)
    
    def rebuild_state(self) -> None:
        # The state gathered from the API is not in a format that is easy to use
        # This function rebuilds the state into a more usable format, there is no schema but you can extrapolate it from the code

        state_cache = copy.deepcopy(self.state)

        self.state = {
            "metadata": {
                "units": {}
            },
            "data": []
        }

        for key in state_cache:
            if not type(state_cache[key]) in [list, dict]:
                self.state["metadata"][key] = state_cache[key]
        
        for key in state_cache["hourly_units"]:
            self.state["metadata"]["units"][key] = state_cache["hourly_units"][key]

        keys: List[str] = []

        for key in state_cache["hourly"]:
            keys += [key]

        for i in range(len(state_cache["hourly"][keys[0]])):
            self.state["data"] += [{}]

            for key in keys:
                self.state["data"][i][key] = state_cache["hourly"][key][i]

        # this just blobs the data into 24 hour chunks, this is because the API returns every single hour in one chunk
        self.state["data"] = [self.state["data"][i:i + 24] for i in range(0, len(self.state["data"]), 24)]
    
    def get_current_temp(self) -> float:
        # Get the current temperature of the location from the current hour

        for item in self.state["data"][0]:
            if datetime.fromisoformat(item['time']).hour == datetime.now().hour:
                return item["temperature_2m"]
        
        return 0