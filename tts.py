"""Text to speech streaming"""

from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from io import BytesIO


def speak_chunk_byte(chunk):
    tts = gTTS(text=chunk, lang="en", tld="co.uk", slow=False)
    with BytesIO() as fp:
        tts.write_to_fp(fp)
        fp.seek(0)
        audio = AudioSegment.from_file(fp, format="mp3")
        play(audio)


def chunked_speak_bytefile(text, chunk_size=50):
    words = text.split()
    chunks = [
        " ".join(words[i : i + chunk_size]) for i in range(0, len(words), chunk_size)
    ]
    for chunk in chunks:
        speak_chunk_byte(chunk)


if __name__ == "__main__":
    text = """I see skies of blue and clouds of white
             The bright blessed days, the dark sacred nights
             And I think to myself
             What a wonderful world"""  # Please provide a large text
    chunked_speak_bytefile(text, chunk_size=50)
