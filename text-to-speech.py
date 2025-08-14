import requests

import argparse
from datetime import datetime

# https://elevenlabs.io/app/speech-synthesis/text-to-speech

# API_KEY = "sk_e509d90f2f354fd4f13d882e9cc397fcc41110c7a2beecfe"
API_KEY = ELEVENLABS_API_KEY
# VOICE_ID = "jBpfuIE2acCO8z3wKNLl"  # ElevenLabs voice ID (e.g., Bella)
# VOICE_ID = "yoZ06aMxZJJ28mfd3POQ"  # ElevenLabs voice ID (e.g., Sam)
VOICE_ID = "AZnzlk1XvdvUeBnXmlld"  # Domi

url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": API_KEY
}

def main():
    # parse command-line arguments
    parser = argparse.ArgumentParser(description="Convert text to speech using ElevenLabs API.")
    parser.add_argument('text', help='Text to synthesize')
    parser.add_argument('-o', '--output', help='Output MP3 file path (default: kindergarten_voice_<timestamp>.mp3)')
    args = parser.parse_args()

    # prepare request data
    data = {
        "text": args.text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.4,
            "similarity_boost": 0.8
        }
    }
    response = requests.post(url, json=data, headers=headers)
    # determine output filename
    if args.output:
        out_path = args.output
    else:
        ts = datetime.now().strftime('%Y%m%d%H%M%S')
        out_path = f"kindergarten_voice_{ts}.mp3"
    # write audio file
    with open(out_path, 'wb') as f:
        f.write(response.content)
    print(f"Audio saved to {out_path}")

if __name__ == '__main__':
    main()
