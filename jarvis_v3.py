"""jarvis voice assistant"""

import logging
import subprocess
import datetime
from pydub import AudioSegment
from pydub.playback import play
from dotenv import load_dotenv
import serial
import llm
import stt
import tts

load_dotenv()
# Configure loggingf
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
FS = 44100  # Sample rate
SECONDS = 2  # Duration of recording
OUTPUT_PATH = "audio/output.wav"
arduino = serial.Serial(port="/dev/ttyUSB0", baudrate=9600, timeout=0.1)


ACTIVATED = False
while True:
    stt.record_audio()
    command = stt.transcribe()
    if not ACTIVATED:
        if "jarvis" in command and "activate" in command:
            ACTIVATED = True
            logging.info("activate jarvis")
            arduino.write(bytes(b"<Activate Jarvis>\n"))
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

        elif "jarvis" in command and (
            ("say cheese" in command) or ("take" in command and "picture" in command)
        ):  # take picture
            now = datetime.datetime.now()
            # Take a picture, name the jpg file after the time when taken
            subprocess.run(
                [
                    "libcamera-still",
                    "-o",
                    f"images/{now:%Y-%m-%d %H:%M}.jpg",
                    "--qt",
                ]
            )
            logging.info("taking photo")
            # Play audio
            play(AudioSegment.from_file("audio/say_cheese.mp3"))
            play(AudioSegment.from_file("audio/camera_stutter.mp3"))
            # llm processng
            llm_response = llm.image_response()
            tts.chunked_speak_bytefile(llm_response, chunk_size=50)

        elif "take" in command and "video" in command and "jarvis" in command:
            now = datetime.datetime.now()
            # Take a 10s video
            subprocess.run(
                [
                    "libcamera-vid",
                    "--codec",
                    "libav",
                    "--libav-audio",
                    "-o",
                    f"images/videos/{now:%Y-%m-%d%H:%M}.mp4",
                    "--timeout",
                    "10000",
                    "--qt",
                ]
            )
            logging.info("taking video")
            play(AudioSegment.from_file("audio/say_cheese.mp3"))
            play(AudioSegment.from_file("audio/camera_stutter.mp3"))

        elif "deactivate" in command and "jarvis" in command:
            ACTIVATED = False
            sound1 = AudioSegment.from_file("audio/jarvis_deactivating.mp3")
            sound2 = AudioSegment.from_file("audio/power_down.mp3")
            arduino.write(bytes(b"<Deactivate Jarvis>\n"))
            play(sound1)
            play(sound2)
            logging.info("deactivating jarvis")
        elif "bye" in command:
            logging.info("bye bye!")
            break
        else:
            llm_response = llm.general_response(command)
            tts.chunked_speak_bytefile(llm_response, chunk_size=50)
