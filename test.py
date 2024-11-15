from pydub import AudioSegment
from pydub.playback import play

sound = AudioSegment.from_file("audio/open_helmet.mp3")
play(sound)
