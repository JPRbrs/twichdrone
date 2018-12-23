# This is a test to check nanpy works on arduino

from nanpy import ArduinoApi
from nanpy import SerialManager


class ArduMotor(object):

    def __init__(self, port=None):
        self.connection = SerialManager(device='/dev/ttyACM0')
        self.a = ArduinoApi(connection=self.connection)

        self.a.pinMode(10, self.a.OUTPUT)
        self.a.pinMode(3, self.a.OUTPUT)
        self.a.pinMode(4, self.a.OUTPUT)
        self.a.pinMode(5, self.a.OUTPUT)
        self.a.pinMode(8, self.a.OUTPUT)
        self.a.pinMode(9, self.a.OUTPUT)

    def move_motor(self, ml, mr):
        # Activate motors
        self.a.digitalWrite(5, self.a.HIGH)
        self.a.digitalWrite(10, self.a.HIGH)
        print('activated')

        print('ML: {}, MR: {}')
        # Move motors
        if ml == 1:
            self.a.digitalWrite(3, self.a.LOW)
            self.a.digitalWrite(4, self.a.HIGH)
        else:
            self.a.digitalWrite(3, self.a.HIGH)
            self.a.digitalWrite(4, self.a.LOW)

        if mr == 1:
            self.a.digitalWrite(8, self.a.LOW)
            self.a.digitalWrite(9, self.a.HIGH)
        else:
            self.a.digitalWrite(8, self.a.HIGH)
            self.a.digitalWrite(9, self.a.LOW)

        # self.a.digitalWrite(3, self.a.LOW)
        # self.a.digitalWrite(4, self.a.LOW)
        # self.a.digitalWrite(8, self.a.LOW)
        # self.a.digitalWrite(9, self.a.LOW)

        print('deactivating')
        self.a.digitalWrite(5, self.a.HIGH)
        self.a.digitalWrite(10, self.a.HIGH)
