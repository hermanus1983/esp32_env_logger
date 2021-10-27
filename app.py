from machine import Pin
import myNetwork_settings
import led_strip
import time
import sys

LIVE_LED_BLINK_INTERVAL = 500
led_state = 0


def runApp():
    live_led = Pin(13, Pin.OUT)  # Configure GPIO13
    live_led.on()

    live_led_timer = time.ticks_ms()  # get millisecond counter
    myNetwork_settings.do_connect()
    led_strip.startLEDStrip()

    while True:
        try:
            if (time.ticks_diff(time.ticks_ms(), live_led_timer) > LIVE_LED_BLINK_INTERVAL):
                live_led.value(not live_led.value())
                live_led_timer = time.ticks_ms()  # get millisecond counter
        except KeyboardInterrupt:
            print("End of application")
            sys.exit()
