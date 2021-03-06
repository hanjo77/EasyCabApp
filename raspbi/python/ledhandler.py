# EasyCabTracker LED and Button handling
#

#Imports
import RPi.GPIO as GPIO
import time
import threading

#Constants
PHONE_GPIO = 24 #17
NETWORK_GPIO = 23 #27
GPS_GPIO = 22
TAXI_GPIO = 27 #23
DRIVER_GPIO = 17 #24
BUTTON_GPIO = 25
BLINK_INTERVAL = 0.5
RESET_INTERVAL = 0.5
PHONE_KEY = 'phone'
NETWORK_KEY = 'network'
GPS_KEY = 'gps'
TAXI_KEY = 'car'
DRIVER_KEY = 'driver'


class Led():
    """Helper class that represents an LED"""
    def __init__(self, gpio_number):
        self.gpio = gpio_number
        self.blink = False


class LedHandler():
    """Handles the button and the leds"""
    gpio_list = [PHONE_GPIO, NETWORK_GPIO, GPS_GPIO, TAXI_GPIO, DRIVER_GPIO]


    def __init__(self):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        self.setup_led()
        self.button_pressed = False
        self.since_button_pressed = -1
        self.is_tracking = True
        self.led_list = {PHONE_KEY: Led(PHONE_GPIO),
                NETWORK_KEY: Led(NETWORK_GPIO),
                GPS_KEY: Led(GPS_GPIO),
                TAXI_KEY: Led(TAXI_GPIO),
                DRIVER_KEY: Led(DRIVER_GPIO)}

#functions for LED
    def setup_led(self):
        GPIO.setup(self.gpio_list, GPIO.OUT)

    def set_led_blink(self, key, value):
        self.led_list[key].blink = value
        if not value:
            self.set_led_on(self.led_list[key].gpio)

    def get_led_blink(self, pin):
        return self.led_list[pin].blink

    def set_led_on(self, pin):
        GPIO.output(self.led_list[pin].gpio, GPIO.HIGH)

    def set_led_off(self, pin):
        GPIO.output(self.led_list[pin].gpio, GPIO.LOW)

    def set_all_led_off(self):
        GPIO.output(self.gpio_list, GPIO.LOW)

    def on_restart_handler(self):
        GPIO.output(self.gpio_list, GPIO.LOW)
        GPIO.cleanup()

    def is_button_pressed(self):
        """Checks if button is clicked and if it was a doubleclick"""
        if self.button_pressed:
            self.button_pressed = False
            #Double click
            if(time.time() - self.since_button_pressed
                    < RESET_INTERVAL):
                self.since_button_pressed = -1
                for led in self.led_list.itervalues():
                    led.blink = not led.blink
#                print 'reset'
            else:
                self.since_button_pressed = time.time()
#                print 'to long since double-click'
        else:
            self.button_pressed = True
            self.since_button_pressed = time.time()
#            print 'putton pressed'

    def change_tracking(self):
        """Changes tracking"""
        self.button_pressed = False
        self.is_tracking = not self.is_tracking
        self.since_button_pressed = -1
        GPIO.output(self.gpio_list, self.is_tracking)
