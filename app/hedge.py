
from . import pir
import subprocess
from datetime import datetime
from . import led
import logging
import logging.handlers
from json_minify import json_minify
import json
from pathlib import Path

pir_sensor = pir.sensor(11)
irled = led.sensor(17)  # Instantiate led class and assign the pin the BCM3
irled.off()  # Turn led off
logger = logging.getLogger()

config = json.loads(json_minify(open(Path.home() / 'config.json', 'r').read()))['hedge']

def main():
    while True:
        hour = int(datetime.strftime(datetime.now(), '%H'))
        if hour >= config['after']  or hour <= config['before']:
            if pir_sensor.read(config['pir_runs']) == 1:
                logger.info("PIR triggered")
                irled.on()
                subprocess.run(["python", Path.home() / 'app' / 'video.py'])
                irled.off()

if __name__ == "__main__":
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    handler = logging.handlers.RotatingFileHandler(
        filename="remoteCam.log", maxBytes=1024 * 1024 * 5, backupCount=5
    )
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)

    main()
