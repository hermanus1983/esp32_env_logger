from machine import Pin
from neopixel import NeoPixel
import time

NEOPIXEL_LED_COUNT = 30

led_strip_pin = Pin(23, Pin.OUT)   # set GPIO0 to output to drive NeoPixels
led_strip = NeoPixel(led_strip_pin, NEOPIXEL_LED_COUNT)   # create NeoPixel driver on GPIO0 for 8 pixels
led_strip.write()              # write data to all pixels
r, g, b = led_strip[4]         # get first pixel colour

def startLEDStrip():
  n = 0
  while n < NEOPIXEL_LED_COUNT:
    if n%2 == 0:
      led_strip[n] = (0, 127, 0)
    else: 
      led_strip[n] = (127, 127, 0)
    led_strip.write()
    n = n + 1

# Clear all pixels 
def clearPixels():
	for i in range(NEOPIXEL_LED_COUNT):
		led_strip[i] = (0, 0, 0)
		led_strip.write()


#Set all pixels to the same color
def setColor(r, g, b):
	for i in range(NEOPIXEL_LED_COUNT):
		led_strip[i] = (r, g, b)
	led_strip.write()


# This function creates a bounce effect and accepts the r, g and b parameters to set 
# the color, and the waiting time. The waiting time determines how fast the bouncing effect is.
# This effect shows an off pixel that runs through all the strip positions.
def bounce(r, g, b, wait):
	for i in range(4 * NEOPIXEL_LED_COUNT):
		for j in range(NEOPIXEL_LED_COUNT):
			led_strip[j] = (r, g, b)
		if ((i // NEOPIXEL_LED_COUNT) % 2) == 0:
			led_strip[i % NEOPIXEL_LED_COUNT] = (0, 0, 0)
		else:
			led_strip[NEOPIXEL_LED_COUNT - 1 - (i%NEOPIXEL_LED_COUNT)] = (0, 0, 0)
		led_strip.write()
		time.sleep_ms(wait)


# This effect works similarly to the bounce effect. There is a pixel on that runs 
# through all the strip positions while the other pixels are off.
def cycle(r, g, b, wait):
	for i in range(4 * NEOPIXEL_LED_COUNT):
		for j in range(NEOPIXEL_LED_COUNT):
			led_strip[j] = (0, 0, 0)
		led_strip[i % NEOPIXEL_LED_COUNT] = (r, g, b)
		led_strip.write()
		time.sleep_ms(wait)
		

# Input a value 0 to 255 to get a color value.
# The colours are a transition r - g - b - back to r.
def wheel(pos):
	if pos < 0 or pos > 255:
		return (0, 0, 0)
	if pos < 85:
		return (255 - pos * 3, pos * 3, 0)
	if pos < 170:
		pos -= 85
		return (0, 255 - pos * 3, pos * 3)
	pos -= 170
	return (pos * 3, 0, 255 - pos * 3)


def rainbow_cycle(wait):
	for j in range(255):
		for i in range(NEOPIXEL_LED_COUNT):
			rc_index = (i * 256 // n) + j
			led_strip[i] = wheel(rc_index & 255)
		led_strip.write()
		time.sleep_ms(wait)
		
