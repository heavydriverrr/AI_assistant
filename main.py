import webbrowser
import speech_recognition as sr
import win32com.client
import requests
from openai import OpenAI
import spacy

# Load spaCy model for intent detection
nlp = spacy.load("en_core_web_sm")

# Set up text-to-speech
speaker = win32com.client.Dispatch("SAPI.SpVoice")

# Function to capture voice commands
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
        except sr.UnknownValueError:
            print("Sorry, I could not understand the audio.")
            speaker.Speak("Sorry, I could not understand the audio.")
            query = None
        except sr.RequestError as e:
            print(f"Request error from Google Speech API: {e}")
            speaker.Speak("Sorry, I am unable to process your request right now.")
            query = None

        return query

# Function to open websites
def open_website(query):
    sites = {
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

    for site, url in sites.items():
        if site in query.lower():
            speaker.Speak(f"Opening {site} for you.")
            webbrowser.open(url)
            return True
    return False

# Function to get weather
def get_weather(city_name="Bhubaneswar"):
    api_key = 'ba80f49117e9a517983bf121633c5982'
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}q={city_name}&appid={api_key}&units=metric"
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != "404":
        weather_data = data["main"]
        temp = weather_data["temp"]
        return f"The temperature in {city_name} is {temp}°C."
    else:
        return "City not found."

# Function to integrate NVIDIA NIM 70B
def get_nim_response(user_query):
    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key="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"
    )

    try:
        completion = client.chat.completions.create(
            model="nvidia/llama-3.1-nemotron-70b-instruct",
            messages=[{"role": "user", "content": user_query}],
            temperature=0.5,
            top_p=1,
            max_tokens=1024,
            stream=True
        )

        response = ""
        for chunk in completion:
            if chunk.choices[0].delta.content:
                response += chunk.choices[0].delta.content

        return response.strip()

    except Exception as e:
        return f"Error fetching response: {e}"

# Function to analyze query using spaCy
def analyze_query(query):
    doc = nlp(query.lower())
    if "weather" in query.lower():
        for ent in doc.ents:
            if ent.label_ == "GPE":  # GPE: Geopolitical Entity, such as a city
                return "weather", ent.text
        return "weather", "Bhubaneswar"  # Default city
    elif "open" in query.lower():
        return "open", query
    else:
        return "general", query

# Enhanced command routing
def handle_command(command):
    intent, detail = analyze_query(command)

    if intent == "weather":
        weather_info = get_weather(detail)
        speaker.Speak(weather_info)
    elif intent == "open":
        if not open_website(detail):
            speaker.Speak("Sorry, I couldn't recognize that website.")
    else:
        speaker.Speak("Let me think about that...")
        response = get_nim_response(detail)
        speaker.Speak(response)

# Main logic
if __name__ == '__main__':
    speaker.Speak("Hello, I am your AI assistant. How can I help you today?")

    while True:
        print("Listening for a command...")
        text = takecommand()

        if text:
            handle_command(text)
        else:
            print("No command recognized, waiting for next input.")
