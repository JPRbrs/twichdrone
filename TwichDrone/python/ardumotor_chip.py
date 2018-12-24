# This is a test to check nanpy works on arduino

from nanpy import ArduinoApi
from nanpy import SerialManager

MOTOR_LEFT_EN = 5
MOTOR_LEFT_RV = 4
MOTOR_LEFT_FWD = 3
MOTOR_RIGHT_EN = 10
MOTOR_RIGHT_RV = 9
MOTOR_RIGHT_FWD = 8


class ArduMotor(object):

    def __init__(self, port=None):
        self.connection = SerialManager(device='/dev/ttyACM0')
        self.a = ArduinoApi(connection=self.connection)

        self.a.pinMode(MOTOR_RIGHT_EN, self.a.OUTPUT)
        self.a.pinMode(MOTOR_RIGHT_FWD, self.a.OUTPUT)
        self.a.pinMode(MOTOR_RIGHT_RV, self.a.OUTPUT)
        self.a.pinMode(MOTOR_LEFT_EN, self.a.OUTPUT)
        self.a.pinMode(MOTOR_LEFT_FWD, self.a.OUTPUT)
        self.a.pinMode(MOTOR_LEFT_RV, self.a.OUTPUT)

    def move_motor(self, ml=None, mr=None):
        if ml and mr:
            # Activate motors
            self.a.digitalWrite(MOTOR_LEFT_EN, self.a.HIGH)
            self.a.digitalWrite(MOTOR_RIGHT_EN, self.a.HIGH)

            if ml.power > 0 and mr.power > 0:
                if ml.direction == 1 and mr.direction == 1:
                    self.a.digitalWrite(MOTOR_LEFT_FWD, self.a.HIGH)
                    self.a.digitalWrite(MOTOR_RIGHT_FWD, self.a.HIGH)
                    self.a.digitalWrite(MOTOR_LEFT_RV, self.a.LOW)
                    self.a.digitalWrite(MOTOR_RIGHT_RV, self.a.LOW)

                if ml.direction == 0 and mr.direction == 0:
                    self.a.digitalWrite(MOTOR_LEFT_FWD, self.a.LOW)
                    self.a.digitalWrite(MOTOR_RIGHT_FWD, self.a.LOW)
                    self.a.digitalWrite(MOTOR_LEFT_RV, self.a.HIGH)
                    self.a.digitalWrite(MOTOR_RIGHT_RV, self.a.HIGH)

                if ml.direction == 0 and mr.direction == 1:
                    self.a.digitalWrite(MOTOR_RIGHT_FWD, self.a.HIGH)
                    self.a.digitalWrite(MOTOR_RIGHT_RV, self.a.LOW)

                if ml.direction == 1 and mr.direction == 0:
                    self.a.digitalWrite(MOTOR_LEFT_FWD, self.a.HIGH)
                    self.a.digitalWrite(MOTOR_LEFT_RV, self.a.LOW)

        else:
            # Deactivate
            self.a.digitalWrite(MOTOR_LEFT_EN, self.a.LOW)
            self.a.digitalWrite(MOTOR_RIGHT_EN, self.a.LOW)
