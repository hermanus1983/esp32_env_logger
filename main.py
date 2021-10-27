import myNetwork_settings
import sys
import utime as time
from BMP180 import BMP180
from machine import I2C, Pin                        # create an I2C bus object accordingly to the port you are using
from micropython import const
import gc
import ssd1306_i2c
import uasyncio as asyncio

LIVE_LED_BLINK_INTERVAL = const(500)

# Pin definitions
repl_button = Pin(12, Pin.IN, Pin.PULL_DOWN)
usr_button1 = Pin(14, Pin.IN, Pin.PULL_DOWN)
usr_button2 = Pin(27, Pin.IN, Pin.PULL_DOWN)

bus = I2C(scl=Pin(22), sda=Pin(21), freq=100000)  # on esp8266

# OLED Display
display = ssd1306_i2c.Display(bus)
display.fb.fill(0)
display.fb.text("Hello", 52, 31, 1)
display.update()

#myNetwork_settings.do_connect()

global temp_str
global pressure_str
global altitude_str


def toggle_led(pin, pin_state):
    if pin_state:
        pin.on()
    else:
        pin.off()


async def memory_information():
    live_led = Pin(13, Pin.OUT)     # Configure GPIO13
    led_state = 0
    """display vital information about the module."""
    INTERVAL = const(5)
    min_free = gc.mem_free()
    next_show = time.time() + INTERVAL
    while True:
        min_free = min(min_free, gc.mem_free())  # collect the all time low.
        if time.time() >= next_show:
            next_show = time.time() + INTERVAL
            print("\n\nRuntime:", time.time())
            print("Free: {:7} bytes, used: {:7d} bytes".format(gc.mem_free(), gc.mem_alloc()))
            print("Minimum free: {:7d} bytes".format(min_free))
            gc.collect()

        # If button 0 is pressed, drop to REPL
        if repl_button.value() == 1:
            print("Dropping to REPL")
            sys.exit()

        led_state ^= 1
        toggle_led(live_led, led_state)
        await asyncio.sleep_ms(LIVE_LED_BLINK_INTERVAL)


def gather_data(device):
    return device.temperature, device.pressure, device.altitude


async def service_bmp180(i2c_bus):
    global temp_str, pressure_str, altitude_str
    bmp180 = BMP180(i2c_bus, baseline=101325.0)
    bmp180.oversample_sett = 2
    while True:
        temp, p, altitude = bmp180.temperature, bmp180.pressure, bmp180.altitude
        temp_str = "T: {} ".format(temp)
        pressure_str = "P: {} mbar ".format(p)
        altitude_str = "A: {} m ".format(altitude)

        # print(temp_str + " " + pressure_str + " " + altitude_str)
        await asyncio.sleep_ms(20)


async def update_oled():

    while True:
        if usr_button1.value() == 1:
            display.fb.fill(0)
            display.fb.text(temp_str, 0, 0, 1)
            display.fb.text(pressure_str, 0, 8, 1)
            display.fb.text(altitude_str, 0, 16, 1)
            display.update()
        else:
            display.fb.fill(0)
            display.fb.text("B1: ...", 2, 15, 1)
            display.fb.text("B2: Env Stats", 2, 23, 1)
            display.update()

        await asyncio.sleep_ms(100)

loop = asyncio.new_event_loop()
loop.create_task(memory_information())
loop.create_task(service_bmp180(bus))
loop.create_task(update_oled())

while True:
    # Wait for button 0 to be pressed to exit
    try:
        loop.run_forever()

    except KeyboardInterrupt:
        print("Going to REPL from console")
        break
