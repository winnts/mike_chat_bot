import json


class Config:
    def __init__(self):
        self.config = self.get_config()

    def get_config(self):
        file = open("config.json", "r")
        return json.load(file)
