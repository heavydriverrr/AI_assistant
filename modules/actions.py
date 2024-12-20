import os
import webbrowser
import requests
from dotenv import load_dotenv

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

class ActionHandler:
    def __init__(self):
        self.sites = {
            "youtube": "https://www.youtube.com",
            "google": "https://www.google.com",
            "facebook": "https://www.facebook.com",
            "twitter": "https://www.twitter.com",
            "instagram": "https://www.instagram.com",
            "linkedin": "https://www.linkedin.com",
            "reddit": "https://www.reddit.com",
            "wikipedia": "https://www.wikipedia.org",
            "news": "https://www.bbc.com/news",
            "github": "https://www.github.com",
            "stackoverflow": "https://www.stackoverflow.com"
        }

    def open_website(self, query):
        for site, url in self.sites.items():
            if site in query.lower():
                webbrowser.open(url)
                return True
        return False

    def get_weather(self, city_name="Bhubaneswar"):
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city_name}&appid={WEATHER_API_KEY}&units=metric"
        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            temp = data["main"]["temp"]
            return f"The temperature in {city_name} is {temp}°C."
        else:
            return "City not found."
