import yaml
from tts_providers.elevenlabs import ElevenLabsProvider
from tts_providers.speechify import SpeechifyProvider

def get_tts_provider():
    """
    Reads config.yaml to determine the active TTS provider,
    initializes it with its configuration, and returns the instance.
    """
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    active_provider_name = config.get("active_provider")
    if not active_provider_name:
        raise ValueError("'active_provider' not set in config.yaml")

    provider_config = config.get("providers", {}).get(active_provider_name)
    if not provider_config:
        raise ValueError(f"No configuration found for provider '{active_provider_name}' in config.yaml")

    if active_provider_name == "elevenlabs":
        return ElevenLabsProvider(provider_config)
    elif active_provider_name == "speechify":
        return SpeechifyProvider(provider_config)
    else:
        raise ValueError(f"Unknown provider: {active_provider_name}")
