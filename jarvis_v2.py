"""
conda install -c conda-forge ffmpeg
"""
import os
from io import BytesIO
import logging
from functools import lru_cache
from pydub import AudioSegment
from pydub.playback import play
from groq import Groq
from dotenv import load_dotenv
import speech_recognition as sr
import serial
import subprocess
import datetime

load_dotenv()
# Configure loggingf
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
FS = 44100  # Sample rate
SECONDS = 2  # Duration of recording
OUTPUT_PATH = "audio/output.wav"
arduino = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=0.1)
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
ACTIVATED = False
while True:
    record_audio()
    command = transcribe()
    if not ACTIVATED:
        if "jarvis" in command and "activate" in command:
            ACTIVATED = True
            logging.info("activate jarvis")
            arduino.write(bytes(b'<Activate Jarvis>\n'))
            # Play audio
            play(AudioSegment.from_file("audio/jarvis_activate.mp3"))
            play(AudioSegment.from_file("audio/iron_man_repulsor.mp3"))
    elif ACTIVATED:
        if "open" in command and "helmet" in command:
            # Open helmet with servo
            logging.info("helmet opened")
            # Play audio
            sound = AudioSegment.from_file("audio/open_helmet.mp3")
            play(sound)
            arduino.write(bytes(b"Open helmet\n"))
        elif "close" in command and "helmet" in command:
            # Close helmet with servo
            logging.info("helmet closed")
            # Play audio
            sound = AudioSegment.from_file("audio/close_helmet.mp3")
            play(sound)
            arduino.write(bytes(b"Close helmet\n"))

        elif "jarvis" in command and (("say cheese" in command) or ("take" in command and "picture" in command)):
            now = datetime.datetime.now()
            # Take a picture, name the jpg file after the time when taken
            subprocess.run(["libcamera-still", "-o", f"images/{now:%Y-%m-%d %H:%M}.jpg", "--qt"])
            logging.info("taking photo")
            # Play audio
            play(AudioSegment.from_file("audio/say_cheese.mp3"))
            play(AudioSegment.from_file("audio/camera_stutter.mp3"))

        elif "take" in command and "video" in command and "jarvis" in command:
            now = datetime.datetime.now()
            # Take a 10s video
            subprocess.run(["libcamera-vid", "--codec", "libav", "--libav-audio", "-o", 
                            f"images/videos/{now:%Y-%m-%d%H:%M}.mp4", "--timeout", "10000", "--qt"])
            logging.info("taking video")
            play(AudioSegment.from_file("audio/say_cheese.mp3"))
            play(AudioSegment.from_file("audio/camera_stutter.mp3"))

        elif "deactivate" in command and "jarvis" in command:
            ACTIVATED = False
            sound1 = AudioSegment.from_file("audio/jarvis_deactivating.mp3")
            sound2 = AudioSegment.from_file("audio/power_down.mp3")
            arduino.write(bytes(b'<Deactivate Jarvis>\n'))
            play(sound1)
            play(sound2)
            logging.info("deactivating jarvis")
        elif "bye" in command:
            logging.info("bye bye!")
            break
