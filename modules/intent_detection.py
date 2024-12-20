import spacy

class IntentDetector:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")

    def detect_intent(self, query):
        doc = self.nlp(query.lower())
        if "weather" in query.lower():
            for ent in doc.ents:
                if ent.label_ == "GPE":  # Geopolitical Entity
                    return "weather", ent.text
            return "weather", "Bhubaneswar"  # Default city
        elif "open" in query.lower():
            return "open", query
        else:
            return "general", query
