import os
import base64
import requests
from pathlib import Path
from .base import TTSProvider

class SpeechifyProvider(TTSProvider):
    """TTS provider for Speechify."""

    def __init__(self, config: dict):
        self.api_key = os.getenv("SPEECHIFY_API_KEY")
        if not self.api_key:
            raise ValueError("SPEECHIFY_API_KEY environment variable not set.")

        self.config = config
        self.base_url = "https://api.sws.speechify.com/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def synthesize(self, text: str, output_path: str):
        """
        Synthesizes text to speech using the Speechify API.
        """
        payload = {
            "input": text,
            "voice_id": self.config.get("voice", "cliff"),
            "language": self.config.get("language", "en-US"),
            "model": self.config.get("model", "simba-english")
        }

        try:
            response = requests.post(
                f"{self.base_url}/audio/speech",
                headers=self.headers,
                json=payload
            )
            response.raise_for_status()
            result = response.json()

            audio_data = result.get('audio_data') or result.get('audioData') or result.get('data')
            if not audio_data:
                print("No audio data found in the response.")
                return None

            audio_bytes = base64.b64decode(audio_data)

            Path(output_path).parent.mkdir(parents=True, exist_ok=True)

            with open(output_path, 'wb') as f:
                f.write(audio_bytes)

            print(f"Audio saved to {output_path}")
            return output_path

        except requests.exceptions.RequestException as e:
            print(f"Error calling Speechify API: {e}")
            if hasattr(e.response, 'text'):
                print(f"Error details: {e.response.text}")
            return None
        except Exception as e:
            print(f"Failed to save audio file: {e}")
            return None
