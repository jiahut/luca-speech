import argparse
from datetime import datetime
from dotenv import load_dotenv
from provider_factory import get_tts_provider

def main():
    # Load environment variables from .env file
    load_dotenv()

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Unified Text-to-Speech CLI")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("-o", "--output", help="Output audio file path (e.g., output.mp3)")
    args = parser.parse_args()

    # Determine the output path
    if args.output:
        output_path = args.output
    else:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        output_path = f"tts_output_{timestamp}.mp3"

    try:
        # Get the configured TTS provider
        tts_provider = get_tts_provider()

        # Synthesize the text
        tts_provider.synthesize(args.text, output_path)

    except (ValueError, FileNotFoundError) as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()
