import os
import google.generativeai as genai
from .base_provider import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    def __init__(self, model: str = "gemini-pro"):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Please set the GOOGLE_API_KEY environment variable.")
        # Configure the Gemini API with the provided key
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model)

    def generate_text(self, prompt: str) -> str:
        response = self.model.generate_content(prompt)
        return response.text
