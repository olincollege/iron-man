# voice_assistant/transcription.py

import json
import logging

from colorama import Fore

# from openai import OpenAI
from groq import Groq
from deepgram import DeepgramClient, PrerecordedOptions


def transcribe_audio(model, api_key, audio_file_path, local_model_path=None):
    """
    Transcribe an audio file using the specified model.

    Args:
        model (str): The model to use for transcription ('openai', 'groq', 'deepgram', 'fastwhisper', 'local').
        api_key (str): The API key for the transcription service.
        audio_file_path (str): The path to the audio file to transcribe.
        local_model_path (str): The path to the local model (if applicable).

    Returns:
        str: The transcribed text.
    """
    try:
        if model == "openai":
            # return _transcribe_with_openai(api_key, audio_file_path)
            pass
        elif model == "groq":
            return _transcribe_with_groq(api_key, audio_file_path)
        elif model == "deepgram":
            return _transcribe_with_deepgram(api_key, audio_file_path)
        elif model == "fastwhisperapi":
            return _transcribe_with_fastwhisperapi(audio_file_path)
        elif model == "local":
            # Placeholder for local STT model transcription
            return "Transcribed text from local model"
        else:
            raise ValueError("Unsupported transcription model")
    except Exception as e:
        logging.error(f"{Fore.RED}Failed to transcribe audio: {e}{Fore.RESET}")
        raise Exception("Error in transcribing audio")


def _transcribe_with_groq(api_key, audio_file_path):
    client = Groq(api_key=api_key)
    with open(audio_file_path, "rb") as audio_file:
        transcription = client.audio.transcriptions.create(
            model="whisper-large-v3", file=audio_file, language="en"
        )
    return transcription.text


def _transcribe_with_deepgram(api_key, audio_file_path):
    deepgram = DeepgramClient(api_key)
    try:
        with open(audio_file_path, "rb") as file:
            buffer_data = file.read()

        payload = {"buffer": buffer_data}
        options = PrerecordedOptions(model="nova-2", smart_format=True)
        response = deepgram.listen.prerecorded.v("1").transcribe_file(payload, options)
        data = json.loads(response.to_json())

        transcript = data["results"]["channels"][0]["alternatives"][0]["transcript"]
        return transcript
    except Exception as e:
        logging.error(f"{Fore.RED}Deepgram transcription error: {e}{Fore.RESET}")
        raise
