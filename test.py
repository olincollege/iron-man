import sounddevice as sd
from groq import Groq
import env

# Constants
FS = 44100  # Sample rate
CHUNK_DURATION = 1  # Chunk duration in seconds
CHUNK_SIZE = int(FS * CHUNK_DURATION)  # Number of samples per chunk

# Initialize the Groq client
client = Groq(api_key=env.GROQ_API_KEY)


def transcribe_stream(audio_data):
    """
    Transcribe audio data (raw bytes) in real-time using Groq API.
    """
    transcription = client.audio.transcriptions.create(
        file=("stream.wav", audio_data),
        model="whisper-large-v3-turbo",
        response_format="json",
        language="en",
        temperature=0.0,
    )
    return transcription.text.lower()


def audio_callback(indata, frames, time, status):
    """
    Callback function to process audio in real-time.
    """
    if status:
        print(f"Audio status: {status}")
    # Convert audio chunk to bytes
    audio_bytes = indata.tobytes()
    # Transcribe the audio chunk
    command = transcribe_stream(audio_bytes)
    print(f"Command: {command}")

    # Perform actions based on transcription
    if "open" in command and "helmet" in command:
        print("helmet opened")
    elif "close" in command and "helmet" in command:
        print("helmet closed")
    elif "bye" in command:
        print("bye bye!")
        raise sd.CallbackStop()  # Stop the stream


# Open audio stream
print("Starting real-time transcription...")
with sd.InputStream(
    samplerate=FS, channels=1, callback=audio_callback, blocksize=CHUNK_SIZE
):
    try:
        sd.sleep(int(1e6))  # Keep the stream alive indefinitely
    except KeyboardInterrupt:
        print("Stopped by user")
