from gpiozero import PWMOutputDevice
import time

# Set up GPIO 13 (physical pin 33) for PWM output
pwm = PWMOutputDevice(13)

# Function to simulate audio signal
def play_pwm_audio(frequency, duration):
    pwm.frequency = frequency  # Set PWM frequency to match audio tone
    pwm.value = 0.5            # 50% duty cycle (adjust for volume control)
    time.sleep(duration)
    pwm.value = 0              # Turn off PWM after duration

# Example usage: Generate a 1kHz tone for 2 seconds
try:
    while True:
    	play_pwm_audio(1000, 2)  # Play a 1kHz tone for 2 seconds
    	time.sleep(1)
    	play_pwm_audio(500, 2)   # Play a 500Hz tone for 2 seconds
    	time.sleep(1)
except KeyboardInterrupt:
    print("Terminating the PWM audio")
    pwm.close()  # Clean up and stop PWM
