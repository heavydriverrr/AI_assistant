import speech_recognition as sr
import win32com.client

class SpeechHandler:
    def __init__(self):
        self.speaker = win32com.client.Dispatch("SAPI.SpVoice")

    def speak(self, message):
        print(f"AI Assistant: {message}")
        self.speaker.Speak(message)

    def take_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.pause_threshold = 1
            self.speak("Listening...")
            audio = recognizer.listen(source)

            try:
                self.speak("Recognizing...")
                query = recognizer.recognize_google(audio, language="en-in")
                print(f"User said: {query}")
                return query
            except sr.UnknownValueError:
                self.speak("Sorry, I could not understand the audio.")
                return None
            except sr.RequestError as e:
                self.speak("There was an issue with the speech recognition service.")
                return None
