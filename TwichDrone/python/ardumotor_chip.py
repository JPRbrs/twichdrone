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

    def move_motor(self, right_power, right_dir,
                   left_power, left_dir):

        if right_power == 0 and left_power == 0:
            self.arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
            self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)
            return

        self.arduino_api.analogWrite(MOTOR_LEFT_EN, right_power)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, left_power)

        # Move motors here

    def test_motor_with_arduino_api(self, ml=None, mr=None):
        ''' Test motors speed using ArduinoApi
        THIS IS NOT USING ArduMotor class
        '''

        # Enable
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 255)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 255)

        # Move forward
        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, self.arduino_api.HIGH)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, self.arduino_api.HIGH)

        # Change speed
        for x in range(250, 0, -50):
            print("Going: {}".format(x))
            sleep(1)
            self.arduino_api.analogWrite(MOTOR_LEFT_EN, x)
            self.arduino_api.analogWrite(MOTOR_RIGHT_EN, x)

        # Disable
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)

    def test_motor_direction(self, ml=None, mr=None):
        '''Test motors direction using ArduinoApi
        THIS IS NOT USING ArduMotor class
        '''
        
        # Enable
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 255)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 255)

        # Move fw
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, 1)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_RV, 0)

        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, 1)
        self.arduino_api.digitalWrite(MOTOR_LEFT_RV, 0)

        sleep(0.5)

        # Move bw
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, 0)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_RV, 1)

        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, 0)
        self.arduino_api.digitalWrite(MOTOR_LEFT_RV, 1)

        sleep(0.5)

        # Move right
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, 1)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_RV, 0)

        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, 0)
        self.arduino_api.digitalWrite(MOTOR_LEFT_RV, 1)

        sleep(0.5)

        # Move left
        self.arduino_api.digitalWrite(MOTOR_RIGHT_FWD, 0)
        self.arduino_api.digitalWrite(MOTOR_RIGHT_RV, 1)

        self.arduino_api.digitalWrite(MOTOR_LEFT_FWD, 1)
        self.arduino_api.digitalWrite(MOTOR_LEFT_RV, 0)

        sleep(0.5)

        # Disable
        self.arduino_api.analogWrite(MOTOR_LEFT_EN, 0)
        self.arduino_api.analogWrite(MOTOR_RIGHT_EN, 0)


if __name__ == '__main__':
    # TODO: Add parameters to run different tests
    parser = argparse.ArgumentParser()
    parser.add_argument("-s",
                        "--serialport",
                        help="arduino serial port",
                        default='')

    args = parser.parse_args()

    driver = ArduMotor('/dev/' + args.serialport)

    driver.test_motor_direction()
