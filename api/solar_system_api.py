import os
import requests

class SolarSystemAPI:

    BASE_URL = "https://api.le-systeme-solaire.net/rest/bodies"

    def __init__ (self, key):
        self.key = key
        self.headers = {"Authorization": f"Bearer {key}"}

    def get_bodies(self):
        response = requests.get(url=f"{self.BASE_URL}", headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_body(self, name):
        response = requests.get(url=f"{self.BASE_URL}/{name}", headers=self.headers)
        response.raise_for_status()

        return response.json()
