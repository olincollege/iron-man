# voice_assistant/text_to_speech.py
import logging
from deepgram import DeepgramClient, SpeakOptions


def text_to_speech(
    model: str,
    api_key: str,
    text: str,
    output_file_path: str,
    local_model_path: str = None,
):
    """
    Convert text to speech using the specified model.

    Args:
    model (str): The model to use for TTS ('openai', 'deepgram', 'elevenlabs', 'local').
    api_key (str): The API key for the TTS service.
    text (str): The text to convert to speech.
    output_file_path (str): The path to save the generated speech audio file.
    local_model_path (str): The path to the local model (if applicable).
    """

    try:
        client = DeepgramClient(api_key=api_key)
        options = SpeakOptions(
            model="aura-arcas-en",  # "aura-luna-en", # https://developers.deepgram.com/docs/tts-models
            encoding="linear16",
            container="wav",
        )
        SPEAK_OPTIONS = {"text": text}
        response = client.speak.v("1").save(output_file_path, SPEAK_OPTIONS, options)

    except Exception as e:
        logging.error(f"Failed to convert text to speech: {e}")
