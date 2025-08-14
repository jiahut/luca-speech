import argparse
import os
import yaml
from datetime import datetime
from dotenv import load_dotenv
from provider_factory import get_tts_provider

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Load configuration from config.yaml
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)
    output_dir = config.get("output_directory", ".")

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Unified Text-to-Speech CLI")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("-o", "--output", help="Output audio file name (e.g., output.mp3)")
    args = parser.parse_args()

    # Determine the output path
    if args.output:
        output_filename = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_filename = f"tts_output_{timestamp}.mp3"

    # Create the full output path
    output_path = os.path.join(output_dir, output_filename)

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # Get the configured TTS provider
        tts_provider = get_tts_provider()

        # Synthesize the text
        tts_provider.synthesize(args.text, output_path)
        print(f"Audio saved to {output_path}")

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
    except Exception as e:
        # The provider will print the detailed error
        print(f"Failed to generate audio.")

if __name__ == "__main__":
    main()
