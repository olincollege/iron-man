import gpiod
import time


LED_PIN  = 17
chip = gpiod.Chip('gpiochip4')
led_line = chip.get_line(LED_PIN)

led_line.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)

counter = 0
num_blinks = 10
try:
	while counter <= num_blinks:
		led_line.set_value(1)
		time.sleep(1)
		led_line.set_value(0)
		time.sleep(1)
		counter += 1
		print("blinked!")

finally:
	led_line.release()
