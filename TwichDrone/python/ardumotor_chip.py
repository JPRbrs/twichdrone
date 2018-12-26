import argparse

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

    def __init__(self, device=None):
        self.connection = SerialManager(device=device)
        self.arduino_api = ArduinoApi(connection=self.connection)

        self.arduino_api.pinMode(MOTOR_RIGHT_EN, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_RIGHT_FWD, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_RIGHT_RV, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_EN, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_FWD, self.arduino_api.OUTPUT)
        self.arduino_api.pinMode(MOTOR_LEFT_RV, self.arduino_api.OUTPUT)

    def move_motor(self,
                   right_power=None,
                   right_dir=None,
                   left_power=None,
                   left_dir=None):
        if not right_power and right_dir and left_power and left_dir:
            self.arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
            self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)
            return

        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 250)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 250)

        if right_dir == 1:
            print("right fw")
            #self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, self.arduino_api.HIGH)
        else:
            print("rightback")
            #self.arduino_api.digitalWrite(MOTOR_RIGHT_RV, self.arduino_api.LOW)

        if left_dir == 1:
            print("left fw")
            #self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, self.arduino_api.HIGH)
        else:
            print("left bw")
            #self.arduino_api.digitalWrite(MOTOR_LEFT_RV, self.arduino_api.LOW)

    def move_motor_old(self, ml=None, mr=None):
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

    def test_motor_with_arduino_api(self, ml=None, mr=None):
        ''' Test the motors are able to move using ArduinoApi 
        THIS IS NOT TESTING ArduMotor class
        '''

        print('Please note that this is not testing ArduMotor class')

        # ENABLE
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 255)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 255)

        # MOVE FORWARD
        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, self.arduino_api.HIGH)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, self.arduino_api.HIGH)

        for x in range(250, 0, -50):
            print("Going: {}".format(x))
            sleep(1)
            self.arduino_api.analogWrite(MOTOR_LEFT_EN, x)
            self.arduino_api.analogWrite(MOTOR_RIGHT_EN, x)

        # DISABLE
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--serialport",
                        help="arduino serial port",
                        default='')
    args = parser.parse_args()

    driver = ArduMotor('/dev/' + args.serialport)
    driver.test_motor_with_arduino_api()
