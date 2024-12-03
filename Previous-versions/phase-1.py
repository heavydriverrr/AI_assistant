import webbrowser
import speech_recognition as sr
import win32com.client
import pyttsx3
import requests
from openai import OpenAI
import API_key

# Set up speaker for text-to-speech
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Function to capture voice commands
def takecommand():
    r = sr.Recognizer()  # Initialize the recognizer
    with sr.Microphone() as source:
        r.pause_threshold = 1  # Adjust for pauses
        print("Listening...")
        audio = r.listen(source)  # Capture audio

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")  # Use Google Speech API
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speaker.Speak("Sorry, I could not understand the audio. say something you motherfucker bosddikke")
            query = None  # Return None if the command is not understood
        except sr.RequestError as e:
            print(f"Request error from Google Cloud Speech API; {e}")
            speaker.Speak("Sorry, I am unable to process your request right now.")
            query = None  # Return None in case of API failure

        return query


# Function to open websites based on voice commands
def open_website(query):
    # List of common websites
    sites = [
        ["youtube", "https://www.youtube.com"],
        ["google", "https://www.google.com"],
        ["facebook", "https://www.facebook.com"],
        ["twitter", "https://www.twitter.com"],
        ["instagram", "https://www.instagram.com"],
        ["linkedin", "https://www.linkedin.com"],
        ["reddit", "https://www.reddit.com"],
        ["wikipedia", "https://www.wikipedia.org"],
        ["news", "https://www.bbc.com/news"],
        ["github", "https://www.github.com"],
        ["stackoverflow", "https://www.stackoverflow.com"]
    ]

    # Match command and open corresponding website
    for site in sites:
        if site[0].lower() in query.lower():  # Match command (case insensitive)
            speaker.Speak(f"Opening {site[0]} for you.")
            webbrowser.open(site[1])
            return True  # Return True once a match is found
    return False  # Return False if no match is found


# Function to fetch weather information
def get_weather(query):
    # Extract city name from the command (e.g., "What's the weather in Bhubaneswar?")
    if "weather" or "temperature" in query and "in" in query:
        city_name = query.split("in")[-1].strip()  # Extract the city name after 'in'
        api_key = API_key.api_weather  # Replace with your API key
        base_url = "http://api.openweathermap.org/data/2.5/weather?"
        complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"  # Use 'metric' for Celsius

        response = requests.get(complete_url)
        data = response.json()

        if data["cod"] != "404":
            weather_data = data["main"]
            temp = weather_data["temp"]
            description = data["weather"][0]["description"]
            return f"The current temperature in {city_name} is {temp}°C with {description}."
        else:
            return "City not found, please try again."

    return None  # If no weather-related query found


# Main logic to handle voice commands
if __name__ == '__main__':
    s = "Hello, I am your AI assistant. How can I help you?"
    speaker.Speak(s)  # Introduce the assistant

    while True:
        print("Listening for a command...")
        text = takecommand()  # Capture voice input

        if text:
            # Handle opening websites
            if not open_website(text):
                # Handle weather-related queries
                weather_info = get_weather(text)
                if weather_info:
                    speaker.Speak(weather_info)
                else:
                    speaker.Speak("Sorry, I could not recognize your request.")

        else:
            # If the command is None (unrecognized), handle gracefully
            print("No command recognized, waiting for next input.")
