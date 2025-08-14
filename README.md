# Unified Text-to-Speech (TTS) CLI

This is a command-line tool for synthesizing text into speech using different TTS providers. It is designed to be easily extensible with new providers.

## Features

- Unified CLI for multiple TTS providers.
- Configuration via `config.yaml`.
- Secure handling of API keys using a `.env` file.
- Currently supports:
  - ElevenLabs
  - Speechify

## Setup

1.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

2.  **Create a `.env` file:**

    Copy the example file:
    ```bash
    cp .env.example .env
    ```
    Then, open `.env` and add your API keys:
    ```
    ELEVENLABS_API_KEY=your_elevenlabs_api_key
    SPEECHIFY_API_KEY=your_speechify_api_key
    ```

3.  **Configure the TTS provider:**

    Open `config.yaml` to choose the active TTS provider and customize its settings.

    To use ElevenLabs:
    ```yaml
    active_provider: elevenlabs
    ```

    To use Speechify:
    ```yaml
    active_provider: speechify
    ```

    You can also change provider-specific settings like the voice, model, etc., in this file.

## Usage

Run the script from your terminal, providing the text you want to convert.

**Basic usage:**
```bash
python tts_cli.py "Hello, world!"
```
This will save the audio to a timestamped file like `tts_output_20231027_103000.mp3`.

**Specify an output file:**
```bash
python tts_cli.py "This is a test." -o my_audio.mp3
```

The tool will use the provider specified in `config.yaml`.
