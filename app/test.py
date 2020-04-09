import subprocess
from . import pir
from . import led
from . import video
import time
import logging
import logging.handlers

def main_menu():
    x = input("video=v\npir=p\npirVerbose=pv\nled=l\n")

    if x == "v":
        video.main()
        main_menu()

    elif x == "p":
        '''
        Runs PIR until triggered(1) and then
        runs pin reverts to not triggered(0)
        '''
        pir_sensor = pir.sensor(11)
        while True:
            result = pir_sensor.read()
            if result == 1:
                print('PIR TRIGGERED')
                while True:
                    result = pir_sensor.read()
                    if result == 0:
                        print('PIR NOT TRIGGERED')
                        break

        main_menu()

    elif x == "pv":
        '''
        Prints result of a pir read
        '''
        pir_sensor = pir.sensor(11)
        while True:
            print(pir_sensor.read())

        main_menu()

    elif x == 'l':
        irled = led.sensor(17)
        print('LED ON')
        irled.on()
        time.sleep(5)
        print('LED OFF')
        irled.off()


if __name__ == "__main__":
    formatter = logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s:%(message)s')
    handler = logging.handlers.RotatingFileHandler(
        filename="test.log", maxBytes=1024 * 1024 * 5, backupCount=5
    )
    handler.setFormatter(formatter)
    logging.basicConfig(handlers=[handler], level=logging.DEBUG)
    
    main_menu()