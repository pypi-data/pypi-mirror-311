import requests
import json
from story_dialogue_generator.config import config
from story_dialogue_generator.auth import UserSession

class StoryService:
    def __init__(self, user_session=None, title=None, settings=None, characters=None, plots=1, endings=1, json_path=None):
        self.user_session = user_session or UserSession()
        self.response = None

        if json_path:
            with open(json_path, "r") as file:
                data = json.load(file)
                self.title = data.get("title")
                self.settings = data.get("settings", {})
                self.characters = data.get("characters", [])
                self.plots = data.get("plots", 1)
                self.endings = data.get("endings", 1)
        else:
            self.title = title
            self.settings = settings or {}
            self.characters = characters or []
            self.plots = plots
            self.endings = endings

    def generate_story(self):
        url = f"{config.GENERATE_SERVICE_URL}/generate/story"
        data = {
            "title": self.title,
            "settings": {
                "size": self.settings.get("size", "medium"),
                "attributes": [
                    {"key": attr["key"], "value": attr["value"]}
                    for attr in self.settings.get("attributes", [])
                ]
            },
            "characters": [
                {
                    "name": char["name"],
                    "attributes": [
                        {"key": attr["key"], "value": attr["value"]}
                        for attr in char.get("attributes", [])
                    ]
                }
                for char in self.characters
            ],
            "plots": self.plots,
            "endings": self.endings
        }

        response = requests.post(
            url,
            json=data,
            headers={"Authorization": f"Bearer {self.user_session.get_token()}"}
        )

        if response.status_code == 200:
            self.response = response.json()
        else:
            self.response = {
                "error": "Failed to generate story",
                "status_code": response.status_code,
                "details": response.text
            }

        return self.response
