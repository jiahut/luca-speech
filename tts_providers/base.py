import abc

class TTSProvider(abc.ABC):
    """Abstract base class for TTS providers."""

    @abc.abstractmethod
    def synthesize(self, text: str, output_path: str):
        """
        Synthesizes text to speech and saves it to a file.

        Args:
            text (str): The text to synthesize.
            output_path (str): The path to save the output audio file.
        """
        pass
