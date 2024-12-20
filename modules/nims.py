import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
NIM_API_KEY = os.getenv("NIM_API_KEY")

class NIMHandler:
    def __init__(self):
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=NIM_API_KEY
        )

    def get_response(self, user_query):
        try:
            completion = self.client.chat.completions.create(
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
