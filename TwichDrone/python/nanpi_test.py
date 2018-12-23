# This is a test to check nanpy works on arduino

import time

from nanpy import ArduinoApi
from nanpy import SerialManager

connection = SerialManager(device='/dev/ttyACM0')

a = ArduinoApi(connection=connection)
a.pinMode(10, a.OUTPUT)
a.pinMode(3, a.OUTPUT)
a.pinMode(4, a.OUTPUT)
a.pinMode(5, a.OUTPUT)
a.pinMode(8, a.OUTPUT)
a.pinMode(9, a.OUTPUT)

a.digitalWrite(5, a.HIGH)
a.digitalWrite(10, a.HIGH)

a.digitalWrite(3, a.LOW)
a.digitalWrite(8, a.LOW)
a.digitalWrite(4, a.HIGH)
a.digitalWrite(9, a.HIGH)

time.sleep(1)

a.digitalWrite(5, a.LOW)
a.digitalWrite(10, a.LOW)
