import copy
import datetime
import json
import math
import time

from nonlinearinterp import NonLinearInterpolator


class MotorModel:

        FORWARD = 1
        BACKWARD = 0
        MAXPOWER = 255
        MAXSPEED = 0.6  # in m/s. Power<->Speed is LINEAR relation
        MAXANGSPEED = ((MAXPOWER*2) * MAXSPEED) / MAXPOWER

        def __init__(self, mlabel):
            self.mlabel = mlabel
            self.direction = MotorModel.FORWARD
            self.power = 0.0

        def __eq__(self, other):

            if self.mlabel == other.mlabel and \
               self.power == other.power and \
               self.direction == other.direction:
                    return True
            return False

        def __ne__(self, other):
            return not self.__eq__(other)

        def __str__(self):
            s = "[ %s, %d, %d]" % (self.label, self.power, self.direction)
            return s

        def update(self, power, direction):
                self.power = power
                self.direction = direction


class InputData:

    def __init__(self,
                 distance=0.0,
                 angle=0.0,  # radians
                 maxdistance=75,
                 x=None,
                 y=None):

        self.distance_linear = distance
        self.distance = distance
        self.angle = angle
        self.maxdistance = maxdistance
        self.x = x
        self.y = y

    def __eq__(self, other):
        if self.distance_linear == other.distance_linear and \
           self.distance == other.distance and \
           self.angle == other.angle and \
           self.maxdistance == other.maxdistance and \
           self.x == other.x and self.y == other.y:
                return True
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        s = "[%3.2f, %3.2f, %3.2f, %3.2f, %s %s]" % (self.distance_linear, self.distance, self.angle, self.maxdistance, self.x, self.y)  ## NOQA
        return s


class DroneModel:

    FORWARD_ANGLE_RANGE = (90-60, 90 + 60)  # goes forward
    BACKWARD_ANGLE_RANGE = (270-60, 270 + 60)  # goes backward (reverse)
    NEAR_ZERO = 0.0001
    MAX_DISTANCE = 75
    # if you set the same than 90-40 ... there is no gap
    MAX_STEERINGANGLE = math.radians(45)
    DISTANCECURVE = [
            [(0, 15), (0, 7)],
            [(15, 30), (7, 18)],
            [(30, 45), (18, 31)],
            [(45, 65), (31, 49)],
            [(65, 76), (49, 76)]]
    POWERCURVE = [[(0, 40), (0, 15)],
                  [(40, 80), (15, 40)],
                  [(80, 120), (40, 70)],
                  [(120, 200), (70, 140)],
                  [(200, 240), (140, 190)],
                  [(240, 256), (190, 210)]]

    def __init__(self, verbose=0):

        self.MR = MotorModel("R")
        self.ML = MotorModel("L")
        self.data = InputData()
        self.allowed_messages = {'joystick', 'button', 'status'}

        self.buttons = {}
        self.interpolator = NonLinearInterpolator()

        self.verbose = verbose
        self.start_time = time.time()
        self.stats = None

    def handle_data(self, data, wsock=None):
        "receive a JSON string, and process it. Do some sanity checks."
        # {u'y': u'up', u'distance': 30.675723300355934, u'kind': u'joystick', u'angle': 1.902855794337782, u'x': u'left'}  # NOQA
        # {u'y': 0, u'distance': 0, u'kind': u'joystick', u'angle': 0, u'x': 0}
        # {u'kind': u'button', u'id': u'rec', u'pressed': u'true'}
        # {u'kind': u'status' }

        if data is None or data == "":
                return

        try:
            data = json.loads(data)
        except Exception as e:
            s = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
            print("[MODEL][handle_data] Exception".format(e))
            return

        if 'kind' in data \
           and data["kind"].lower() in self.allowed_messages:

            if data["kind"].lower() == "joystick" \
               and "distance" in data.keys() and "angle" in data.keys():
                # joystick input
                # print("joystick: ", data)
                self.update_joystick_data(data)

            if data["kind"].lower() == "button" \
               and "id" in data.keys() and "pressed" in data.keys():
                # button pressed (work as boolean switch)
                # print("button: ", data)
                self.update_button_data(data)

            if data["kind"] == "status":
                print("status :", data)
                self.handle_message_status(data, wsock)

    def update_joystick_data(self, data):
        dint = self.interpolator.NLinterp(
                data["distance"],
                DroneModel.DISTANCECURVE)

        with MODEL_LOCK:
            self.data.distance_linear = data["distance"]
            self.data.distance = dint
            self.data.angle = data["angle"]  # in radians

            if self.verbose > 1:
                s = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                print "[MODEL][%s][ IN][joy] [distance: L:%09.5f|NL:%09.5f] [angle: %09.5fd]" % (s,self.data.distance_linear,self.data.distance,math.degrees(self.data.angle))  # NOQA

            # optional
            if "x" in data.keys() and "y" in data.keys():
                self.data.x = data["x"]
                self.data.y = data["y"]

    def update_button_data(self, data):
        with MODEL_LOCK:
            if data["id"] not in self.buttons.keys():
                self.buttons[data["id"]] = False

            # toggle
            if data["pressed"].lower() == "true":
                self.buttons[data["id"]] = not self.buttons[data["id"]]

            if self.verbose > 1:
                s = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
                # print "[MODEL][%s][ IN][button] [Name: %s] [Pressed: %s]" % (s,data["id"],self.buttons[data["id"]])  # NOQA

    def handle_message_status(self, data, wsock):
        time_delta = time.time() - self.start_time
        m, s = divmod(time_delta, 60)
        h, m = divmod(m, 60)
        time_delta_s = "Running time: %02d:%02d:%02d" % (h, m, s)

        gopro = 'Gopro: Not Found/OFF'
        if self.stats['gopro']['power'].lower() == 'on':

            recording = 'off'
            if 'record' in self.stats['gopro'].keys():
                recording = self.stats['gopro']['record']

            gopro = "Powered [battery: %s%%] Recording: %s" % (
                    self.stats['gopro']['batt1'],
                    recording)

        if self.stats['amp_l'] is None or self.stats['amp_r'] is None:
            motor_a = "Left Current: N/A | Right Current: N/A [Arduino Off?]"
        else:
            motor_a = "Left Curr_avg: %3.2fA | Right Curr_avg: %3.2fA" % (
                    self.stats['amp_l'],
                    self.stats['amp_r'])

        msg = "%s</br>%s</br>%s</br>" % (time_delta_s, gopro, motor_a)

        wsock.sendMessage(unicode(msg, 'utf-8'))

    def in_forward_angle(self, angle):
        # in radians
        ang_d = math.degrees(angle)
        if ang_d >= self.FORWARD_ANGLE_RANGE[0] and \
           ang_d <= self.FORWARD_ANGLE_RANGE[1]:
            return True
        return False

    def in_backward_angle(self, angle):
        # in radians
        ang_d = math.degrees(angle)
        if ang_d >= self.BACKWARD_ANGLE_RANGE[0] and \
           ang_d <= self.BACKWARD_ANGLE_RANGE[1]:
            return True
        return False

    def set_stats(self, stats):
        self.stats = stats

    def update(self):
        "calculate everything needed to work propertly"
        data = self.get_data()['data']
        Fx = data.distance * math.cos(data.angle)
        Fy = data.distance * math.sin(data.angle)

        # include partial angle component
        #
        # If Fx -> O, D -> full aligned.
        # Else, asign the partial component to the force, to
        # create somekind of moment.
        # # calculate first the % of the force, then modify it
        #
        percent_x = 0.0
        cx = 0.0
        if data.distance != 0.0:
            cx = math.fabs(Fx)*100.0/data.distance

        # generic power (non balanced)
        MPower = self.interpolator.interpolate(
                data.distance,
                0,
                data.maxdistance,
                0,
                MotorModel.MAXPOWER)

        # get directions
        forward = True
        right = True
        FullForward = False
        FullBackward = False

        if Fy < 0:
                forward = False
        if Fx < 0:
                right = False

        if self.in_forward_angle(data.angle):
            FullForward = True
            cr = cx
            cl = -cx
            if right:
                cr = -cx
                cl = cx

            MRPower = MPower + (MPower * cr / 100.0)
            MLPower = MPower + (MPower * cl / 100.0)

        elif self.in_backward_angle(data.angle):
            FullBackward = True
            cr = cx
            cl = -cx
            if right:
                cr = -cx
                cl = +cx

            MRPower = MPower + (MPower * cr / 100.0)
            MLPower = MPower + (MPower * cl / 100.0)
        else:

            MRPower = MLPower = MPower

        if MRPower > MotorModel.MAXPOWER:
                MRPower = MotorModel.MAXPOWER
        if MLPower > MotorModel.MAXPOWER:
                MLPower = MotorModel.MAXPOWER

        MRPower = self.interpolator.NLinterp(
                MRPower,
                DroneModel.POWERCURVE)
        MLPower = self.interpolator.NLinterp(
                MLPower,
                DroneModel.POWERCURVE)

        MRPower = int(MRPower)
        MLPower = int(MLPower)

        with MODEL_LOCK:

            if FullForward:
                self.MR.update(MRPower, MotorModel.FORWARD)
                self.ML.update(MLPower, MotorModel.FORWARD)
                return

            if FullBackward:
                self.MR.update(MRPower, MotorModel.BACKWARD)
                self.ML.update(MLPower, MotorModel.BACKWARD)
                return

            if forward and not right or\
               not forward and not right:
                self.MR.update(MRPower, MotorModel.FORWARD)
                self.ML.update(MLPower, MotorModel.BACKWARD)

            if forward and right or\
               not forward and right:
                    self.MR.update(MRPower,
                                   MotorModel.BACKWARD)
                    self.ML.update(MLPower,
                                   MotorModel.FORWARD)

    def get_data(self):
        with MODEL_LOCK:
            return {'data': copy.copy(self.data),
                    'MR': copy.copy(self.MR),
                    'ML': copy.copy(self.ML),
                    'buttons': copy.copy(self.buttons)}

    def print_data(self):
        print self.data

    def get_buttons_str(self):
        s = ''
        with MODEL_LOCK:
            for i in self.buttons.keys():
                s += '[%s->%s]' % (i, self.buttons[i])

        return s
