from machine import Pin, PWM, UART
import time

led = Pin(5, Pin.OUT)
uart = UART(2, 115200, tx=2, rx=15)
pwm1 = PWM(Pin(25, Pin.OUT))
pwm2 = PWM(Pin(27, Pin.OUT))
pwm3 = PWM(Pin(12, Pin.OUT))

pwm1.freq(50)
pwm2.freq(50)
pwm3.freq(50)

import network as MOD_NETWORK
import secrets

# Connect to Wifi
GLOB_WLAN=MOD_NETWORK.WLAN(MOD_NETWORK.STA_IF)
GLOB_WLAN.active(True)
GLOB_WLAN.connect(secrets.ssid, secrets.password)

while not GLOB_WLAN.isconnected():
  pass

# Connect to Firebase
import ufirebase as firebase
firebase.setURL("https://fir-test-d61b0-default-rtdb.asia-southeast1.firebasedatabase.app/")
led.on() # to indicate that connection to firebase is successful
