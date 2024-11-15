import sounddevice as sd
from scipy.io.wavfile import write
from pydub import AudioSegment
from pydub.playback import play
from groq import Groq
import env

FS = 44100  # Sample rate
SECONDS = 2  # Duration of recording
OUTPUT_PATH = "audio/output.wav"

# Initialize the Groq client
client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key=env.GROQ_API_KEY
)


def record_audio():
    myrecording = sd.rec(
        int(SECONDS * FS), samplerate=FS, channels=1
    )  # check channels with python3 -m sounddevice
    sd.wait()  # Wait until recording is finished
    write(OUTPUT_PATH, FS, myrecording)  # Save as WAV file
    return


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
        print(command)
        return command


while True:
    print("started recording...")
    record_audio()
    print("stop recording...")
    command = transcribe()
    if "open" in command and "helmet" in command:
        # Open helmet with servo
        print("helmet opened")
        # Play audio
        sound = AudioSegment.from_file("audio/open_helmet.mp3")
        play(sound)

    elif "close" in command and "helmet" in command:
        # Close helmet with servo
        print("helmet closed")
        # Play audio
        sound = AudioSegment.from_file("audio/close_helmet.mp3")
        play(sound)
    elif "bye" in command:
        print("bye bye!")
        break
