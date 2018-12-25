# This is a test to check nanpy works on arduino

from nanpy import ArduinoApi
from nanpy import SerialManager
from time import sleep

MOTOR_LEFT_EN = 5
MOTOR_LEFT_FWD = 3
MOTOR_LEFT_RV = 4

MOTOR_RIGHT_EN = 10
MOTOR_RIGHT_FWD = 8
MOTOR_RIGHT_RV = 9


class ArduMotor(object):

    def __init__(self, port=None):
        self.connection = SerialManager(device='/dev/ttyACM3')
        self.arduino_api = ArduinoApi(connection=self.connection)

        self.arduino_api.pinMode(MOTOR_RIGHT_EN, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_RIGHT_FWD, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_RIGHT_RV, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_EN, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_FWD, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_RV, self.arduino_api.OUTPUT)

    def move_motor(self, ml=None, mr=None):
        if ml and mr:
            # Activate motors

            if ml.power > 0 and mr.power > 0:
                if ml.direction == 1 and mr.direction == 1:
                    self.arduino_api.analogWrite(MOTOR_LEFT_EN, 255)
                    self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 255)

                    self.arduino_api.digitalWrite(MOTOR_LEFT_FWD,
                                                  self.arduino_api.HIGH)
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD,
                                                  self.arduino_api.HIGH)
                    self.arduino_api.digitalWrite(MOTOR_LEFT_RV,
                                                  self.arduino_api.LOW)
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_RV,
                                                  self.arduino_api.LOW)

                if ml.direction == 0 and mr.direction == 0:
                    self.arduino_api.analogWrite(MOTOR_LEFT_EN, 200)
                    self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 200)

                    self.arduino_api.digitalWrite(MOTOR_LEFT_FWD,
                                                  self.arduino_api.LOW)
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD,
                                                  self.arduino_api.LOW)
                    self.arduino_api.digitalWrite(MOTOR_LEFT_RV,
                                                  self.arduino_api.HIGH)
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_RV,
                                                  self.arduino_api.HIGH)

                if ml.direction == 0 and mr.direction == 1:
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD,
                                                  self.arduino_api.HIGH)
                    self.arduino_api.digitalWrite(MOTOR_RIGHT_RV,
                                                  self.arduino_api.LOW)

                if ml.direction == 1 and mr.direction == 0:
                    self.arduino_api.digitalWrite(MOTOR_LEFT_FWD,
                                                  self.arduino_api.HIGH)
                    self.arduino_api.digitalWrite(MOTOR_LEFT_RV,
                                                  self.arduino_api.LOW)

        else:
            # Deactivate
            self.arduino_api.digitalWrite(MOTOR_LEFT_EN, self.arduino_api.LOW)
            self.arduino_api.digitalWrite(MOTOR_RIGHT_EN, self.arduino_api.LOW)

    def test_motor(self, ml=None, mr=None):
        connection = SerialManager(device='/dev/ttyACM3')

        arduino_api = ArduinoApi(connection=connection)
        arduino_api.pinMode(MOTOR_LEFT_EN, arduino_api.OUTPUT)
        arduino_api.pinMode(MOTOR_LEFT_FWD, arduino_api.OUTPUT)
        arduino_api.pinMode(MOTOR_LEFT_RV, arduino_api.OUTPUT)
        arduino_api.pinMode(MOTOR_RIGHT_EN, arduino_api.OUTPUT)
        arduino_api.pinMode(MOTOR_RIGHT_FWD, arduino_api.OUTPUT)
        arduino_api.pinMode(MOTOR_RIGHT_RV, arduino_api.OUTPUT)

        # ENABLE
        arduino_api.analogWrite(MOTOR_LEFT_EN, 255)
        arduino_api.analogWrite(MOTOR_RIGHT_EN, 255)

        # MOVE FORWARD
        arduino_api.digitalWrite(MOTOR_LEFT_FWD, arduino_api.HIGH)
        arduino_api.digitalWrite(MOTOR_RIGHT_FWD, arduino_api.HIGH)

        for x in range(250, 0, -50):
            print("Going: {}".format(x))
            sleep(1)
            arduino_api.analogWrite(MOTOR_LEFT_EN, x)
            arduino_api.analogWrite(MOTOR_RIGHT_EN, x)

        # DISABLE
        arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
        arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)


if __name__ == '__main__':
    driver = ArduMotor(port='/dev/ttyACM3')
    driver.test_motor()
