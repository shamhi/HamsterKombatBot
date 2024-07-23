import json


class JsonDB:
    def __init__(self, name: str):
        self.name = name if name.endswith(".json") else f"{name}.json"

    def get_data(self):
        try:
            with open(self.name, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_data(self, data: dict):
        with open(self.name, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
