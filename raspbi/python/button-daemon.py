# EasyCabTracker Button listener
#

#Imports
import RPi.GPIO as GPIO
import time
import os
from subprocess import call
import ledhandler
from daemon import runner
from lockfile import LockTimeout

#constants
CLICK_TIMEOUT = 2

class ButtonListener():

    def __init__(self):
        """ Initializes daemon """
        self.stdin_path = '/dev/null'
        self.stdout_path = '/var/log/buttond/buttond.log'
        self.stderr_path = '/var/log/buttond/buttond-error.log'
        self.pidfile_path =  '/var/run/buttond/buttond.pid'
        self.block_file_path = '/'
        self.block_file_name = 'block'
        self.pidfile_timeout = 5
        self.oldtime = time.time()
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(ledhandler.BUTTON_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.remove_event_detect(ledhandler.BUTTON_GPIO)
        GPIO.add_event_detect(ledhandler.BUTTON_GPIO, GPIO.RISING, bouncetime=900, callback=self.cb_button)
        while True:
            pass

    def cb_button(self, channel):
        if GPIO.event_detected(ledhandler.BUTTON_GPIO):
            if (time.time()-self.oldtime) > CLICK_TIMEOUT:          
                print 'pressed'           
                block_file_uri = self.block_file_path + self.block_file_name
                self.oldtime = time.time()
                if not os.path.exists(block_file_uri):
                    new_name = os.path.join(self.block_file_path, self.block_file_name)         
                    new_file = open(new_name, "w")
                    new_file.write('')
                    new_file.close()
                else:
                    call(['service', 'easycabd', 'restart'])

buttonListener = ButtonListener()
daemon_runner = runner.DaemonRunner(buttonListener)

try:
    daemon_runner.do_action()

except LockTimeout:
    print 'Error: could not aquire lock, will restart daemon'
