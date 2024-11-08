import sounddevice as sd
from scipy.io.wavfile import write
from playsound import playsound
from groq import Groq
import env

FS = 44100  # Sample rate
SECONDS = 3  # Duration of recording
OUTPUT_PATH = "audio/output.wav"
myrecording = sd.rec(
    int(SECONDS * FS), samplerate=FS, channels=1
)  # check channels with python3 -m sounddevice
sd.wait()  # Wait until recording is finished
write(OUTPUT_PATH, FS, myrecording)  # Save as WAV file

# Initialize the Groq client
client = Groq(
    # api_key=os.environ.get("GROQ_API_KEY"),
    api_key=env.GROQ_API_KEY
)

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


if "open" in command and "helmet" in command:
    # Open helmet with servo
    print("helmet opened")
    # Play audio
    playsound("audio/open_helmet.mp3")

elif "close" in command and "helmet" in command:
    # Close helmet with servo
    print("helmet closed")
    # Play audio
    playsound("audio/close_helmet.mp3")
