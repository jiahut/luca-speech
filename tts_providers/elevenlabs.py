import os
import requests
from .base import TTSProvider

class ElevenLabsProvider(TTSProvider):
    """TTS provider for ElevenLabs."""

    def __init__(self, config: dict):
        self.api_key = os.getenv("ELEVENLABS_API_KEY")
        if not self.api_key:
            raise ValueError("ELEVENLABS_API_KEY environment variable not set.")

        self.voice_id = config.get("voice_id", "AZnzlk1XvdvUeBnXmlld")
        self.model = config.get("model", "eleven_multilingual_v2")
        self.voice_settings = config.get("voice_settings", {
            "stability": 0.4,
            "similarity_boost": 0.8
        })
        self.url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.voice_id}"
        self.headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.api_key
        }

    def synthesize(self, text: str, output_path: str):
        """
        Synthesizes text to speech using the ElevenLabs API.
        """
        data = {
            "text": text,
            "model_id": self.model,
            "voice_settings": self.voice_settings
        }

        try:
            response = requests.post(self.url, json=data, headers=self.headers)
            response.raise_for_status()

            with open(output_path, 'wb') as f:
                f.write(response.content)
            return output_path
        except requests.exceptions.RequestException as e:
            print(f"Error calling ElevenLabs API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Error details: {e.response.text}")
            # Raise the exception to be caught by the CLI
            raise e
