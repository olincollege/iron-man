import pigpio
import wave
import struct
import numpy as np
import time

# Initialize pigpio library
pi = pigpio.pi("192.168.35.0", 8888)

# Check if pigpio is running
if not pi.connected:
    print("Failed to connect to pigpio daemon")
    exit()

# Set up GPIO for PWM output
GPIO_PIN = 13
pi.set_mode(GPIO_PIN, pigpio.OUTPUT)

# Function to load a WAV file and extract samples
def load_wav(filename):
    with wave.open(filename, 'rb') as wav_file:
        # Get audio properties: channels, sample width, sample rate
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        
        # Ensure we are working with mono audio (single channel)
        if num_channels != 1:
            raise ValueError("Only mono WAV files are supported.")

        # Extract the raw audio data
        num_frames = wav_file.getnframes()
        raw_data = wav_file.readframes(num_frames)

        # Unpack the raw data into a tuple of samples
        fmt = "<" + str(num_frames) + "h"  # 'h' for signed short (2 bytes)
        samples = np.array(struct.unpack(fmt, raw_data))

        return samples, sample_rate

# Function to play the audio file using PWM
def play_audio(filename):
    # Load the audio file and get samples
    samples, sample_rate = load_wav(filename)

    # Set PWM frequency (use audio sample rate as a base frequency for PWM)
    pi.set_PWM_frequency(GPIO_PIN, sample_rate)

    # Play the audio by adjusting PWM duty cycle based on sample data
    for sample in samples:
        # Convert the sample value to a duty cycle between 0-255
        # Normalize the sample from range (-32768 to 32767) to (0 to 255)
        duty_cycle = int(np.clip((sample + 32768) / 256, 0, 255))
        
        # Set the duty cycle for PWM
        pi.set_PWM_dutycycle(GPIO_PIN, duty_cycle)

        # Sleep for the time corresponding to one sample at the given sample rate
        time.sleep(1 / sample_rate)

# Run the audio playback
try:
    play_audio('audio/output.wav')  # Replace with your actual WAV file path
except KeyboardInterrupt:
    print("Playback interrupted")
    # Clean up
    pi.set_PWM_dutycycle(GPIO_PIN, 0)  # Stop PWM
    pi.stop()  # Disconnect from pigpio
 
