import network

my_ssid = 'Maanster'
ssid_password = 'WGhOnnGvVbn,mvKeLeS!'


def create_station():
    wlan = network.WLAN(network.STA_IF)  # create station interface
    wlan.active(True)  # activate the interface
    wlan.scan()  # scan for access points
    wlan.isconnected()  # check if the station is connected to an AP
    wlan.connect('my_ssid', 'ssid_password')  # connect to an AP
    wlan.config('mac')  # get the interface's MAC address
    wlan.ifconfig()  # get the interface's IP/netmask/gw/DNS addresses


def create_ap():
    ap = network.WLAN(network.AP_IF)  # create access-point interface
    ap.config(essid='ESP32-LIGHTCTRL-AP')  # set the ESSID of the access point
    ap.active(True)  # activate the interface


def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("connecting to network...")
        wlan.connect('my_ssid', 'ssid_password')
        while not wlan.isconnected():
            pass
    print("network config: ", wlan.ifconfig())
