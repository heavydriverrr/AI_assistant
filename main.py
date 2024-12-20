from modules.actions import ActionHandler
from modules.intent_detection import IntentDetector
from modules.nims import NIMHandler
from modules.speech import SpeechHandler

# Initialize modules
speech = SpeechHandler()
actions = ActionHandler()
intent_detector = IntentDetector()
nim_handler = NIMHandler()


def main():
    speech.speak("Hello, I am your AI assistant. How can I help you today?")

    while True:
        command = speech.take_command()
        if command:
            intent, detail = intent_detector.detect_intent(command)

            if intent == "weather":
                weather_info = actions.get_weather(detail)
                speech.speak(weather_info)
            elif intent == "open":
                if not actions.open_website(detail):
                    speech.speak("Sorry, I couldn't recognize that website.")
            else:
                speech.speak("Let me think about that...")
                response = nim_handler.get_response(detail)
                speech.speak(response)
        else:
            print("No command recognized. Waiting for the next input.")


if __name__ == "__main__":
    main()
