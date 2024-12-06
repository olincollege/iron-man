from groq import Groq
import os
import speech_recognition as sr
from functools import lru_cache
import logging
from io import BytesIO
from pydub import AudioSegment


OUTPUT_PATH = "audio/output.wav"

# Initialize the Groq client
client = Groq(
    api_key=os.environ.get("GROQ_API_KEY"),
)


@lru_cache(maxsize=None)
def get_recognizer():
    """
    Return a cached speech recognizer instance
    """
    return sr.Recognizer()


def record_audio(
    timeout=10,
    phrase_time_limit=None,
    retries=3,
    energy_threshold=2000,
    pause_threshold=1,
    phrase_threshold=0.1,
    dynamic_energy_threshold=True,
    calibration_duration=1,
):
    """
    Record audio from the microphone and save it as an MP3 file.
    Args:
    timeout (int): Maximum time to wait for a phrase to start (in seconds).
    phrase_time_limit (int): Maximum time for the phrase to be recorded (in seconds).
    retries (int): Number of retries if recording fails.
    energy_threshold (int): Energy threshold for considering whether a given chunk of audio is speech or not.
    pause_threshold (float): How much silence the recognizer interprets as the end of a phrase (in seconds).
    phrase_threshold (float): Minimum length of a phrase to consider for recording (in seconds).
    dynamic_energy_threshold (bool): Whether to enable dynamic energy threshold adjustment.
    calibration_duration (float): Duration of the ambient noise calibration (in seconds).
    """
    recognizer = get_recognizer()
    recognizer.energy_threshold = energy_threshold
    recognizer.pause_threshold = pause_threshold
    recognizer.phrase_threshold = phrase_threshold
    recognizer.dynamic_energy_threshold = dynamic_energy_threshold
    for attempt in range(retries):
        try:
            with sr.Microphone() as source:
                logging.info("Calibrating for ambient noise...")
                recognizer.adjust_for_ambient_noise(
                    source, duration=calibration_duration
                )
                logging.info("Recording started")
                # Listen for the first phrase and extract it into audio data
                audio_data = recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
                logging.info("Recording complete")
                # Convert the recorded audio data to an MP3 file
                wav_data = audio_data.get_wav_data()
                audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
                mp3_data = audio_segment.export(
                    OUTPUT_PATH,
                    format="mp3",
                    bitrate="128k",
                    parameters=["-ar", "22050", "-ac", "1"],
                )
                return
        except sr.WaitTimeoutError:
            logging.warning(
                f"Listening timed out, retrying... ({attempt + 1}/{retries})"
            )
        except Exception as e:
            logging.error(f"Failed to record audio: {e}")
            if attempt == retries - 1:
                raise
    logging.error("Recording failed after all retries")


def transcribe():
    # Open the audio file
    with open(OUTPUT_PATH, "rb") as file:
        # Create a transcription of the audio file
        transcription = client.audio.transcriptions.create(
            file=(OUTPUT_PATH, file.read()),  # Required audio file
            model="whisper-large-v3-turbo",  # Required model to use for transcription
            prompt="Specify context or spelling",  # Optional
            response_format="json",  # Optional
            language="en",  # Optional
            temperature=0.0,  # Optional
        )
        # Print the transcription text
        command = transcription.text.lower()
        logging.info(command)
        return command
