from machine import Pin
import myNetwork_settings
import sys
import time
from network import Bluetooth
import binascii
import dataStore  # Import DataStore

LIVE_LED_BLINK_INTERVAL = 500

class bluetooth:
    data = dataStore.DataStore()
    bluetooth = Bluetooth()
    bluetooth.init()

    def __init__(self, data, ):
        # Init Bluetooth and enable Scanning
        self.data = data
        if not self.bluetooth.isscanning():
            self.bluetooth.start_scan(-1)

    def scan(self):
        adv = self.bluetooth.get_adv()
        try:
            # look if the received mac is in the data store
            for x in range(0, (self.data.getAnzahlTokens())):
                if str(binascii.hexlify(adv.mac)) == str(self.data.getnextMac()):
                    # lay down the RSSI value to the DataStore
                    print('*********************************************')
                    print("Geraete Mac Adresse = {}".format(binascii.hexlify(adv.mac)))
                    print("Geraete Sendestaerke = {}".format(adv.rssi))
                    data_stream = str(adv.data)
                    self.data.setRssi(binascii.hexlify(adv.mac), adv.rssi)
                    self.data.setDaten(binascii.hexlify(adv.mac), data_stream.replace("\\", ";"))
                    break
        except:
            pass


def runApp():
    # Pin definitions
    repl_button = Pin(12, Pin.IN, Pin.PULL_UP)
    connect_network_led = Pin(22, Pin.OUT)
    connect_network_led.off()
    live_led = Pin(13, Pin.OUT)  # Configure GPIO13
    live_led.on() # High level turns LED on

    live_led_timer = time.ticks_ms()  # get millisecond counter
    connect_network_led.on()
    #myNetwork_settings.do_connect()
    connect_network_led.off()

    BLE = bluetooth()

    while True:
        # Wait for button 0 to be pressed to exit
        try:
            if time.ticks_diff(time.ticks_ms(), live_led_timer) >= LIVE_LED_BLINK_INTERVAL:
                live_led.value(not live_led.value())
                live_led_timer = time.ticks_ms()  # get millisecond counter
                BLE.scan()

            # If button 0 is pressed, drop to REPL
            if repl_button.value() == 0:
                print("Dropping to REPL")
                sys.exit()

            # Do nothing
            # time.sleep(0.1)
        except KeyboardInterrupt:
            print("Going to REPL from console")
            break


if __name__ == "__main__":
    runApp()
