from gpiozero import LED
from logging import getLogger

logger = getLogger()

class sensor:
    def __init__(self, pin):
        self.led = LED(pin)
        return

    def on(self, value=1):
        logger.debug("LED on")
        self.led.on()  # Full brightness unless told otherwise
        return

    def off(self):
        logger.debug("LED off")
        self.led.off()  # Off
        return
