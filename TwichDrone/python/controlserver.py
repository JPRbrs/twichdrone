#!/usr/bin/python

import threading
import wsock
import model
import argparse
import time
# from ardumotor import ArduMotor


def log(msg):
    s = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    msg = "[%s]" + msg
    return msg % s


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose",
                        help="Show detailed model info",
                        action="count",
                        default=0)
    parser.add_argument("-a",
                        "--address",
                        help="Host Address",
                        default='')
    parser.add_argument("-p",
                        "--port",
                        help="Listen Port",
                        default=8000)
    parser.add_argument("-f",
                        "--frequency",
                        help="FPS to run model",
                        default=60)
    parser.add_argument("-g",
                        "--gopropasswd",
                        help="GoPro Password",
                        default='')
    parser.add_argument("-s",
                        "--serialport",
                        help="arduino serial port",
                        default='')
    args = parser.parse_args()

    model.MODEL = model.DroneModel(verbose=args.verbose)
    model.MODEL_LOCK = threading.Lock()

    wsock.websocketserver_start(args.address, int(args.port))

    print("ControlServer started at {}:{} (verbose:{}) Refresh: {} Hz").format(
        args.address, args.port, args.verbose, args.frequency)

    # driver = ArduMotor(port=args.serialport)

    olddata = None
    ml_amp = 0.0
    mr_amp = 0.0

    while True:
        target_freq = 1/float(args.frequency)
        sample_start_time = time.time()

        # begin block

        # ml_amp = (ml_amp + driver.GetCurrent(ArduMotor.MOTOR_LEFT))/2.0
        # mr_amp = (mr_amp + driver.GetCurrent(ArduMotor.MOTOR_RIGHT))/2.0

        stats = {'amp_l': ml_amp, 'amp_r': mr_amp}

        model.MODEL.set_stats(stats)
        model.MODEL.update()
        data = model.MODEL.getdata()

        if olddata and (olddata['data'] != data['data']
                        or olddata['MR'] != data['MR']
                        or olddata['ML'] != data['ML']
                        or olddata['buttons'] != data['buttons']):

            # manage buttons
            rec_old = olddata['buttons'] and olddata['buttons']['rec']
            rec = None
            if data['buttons'] and 'rec' in data['buttons']:
                rec = data['buttons']['rec']

            if data['buttons']:
                if rec_old:
                    if not rec_old and rec:
                        if args.verbose > 1:
                            print(log("START_RECORDING"))
                    if rec_old and not rec:
                        if args.verbose > 1:
                            print(log("STOP_RECORDING"))
                else:
                    if rec:
                        if args.verbose > 1:
                            print(log("START_RECORDING"))
                    else:
                        if args.verbose > 1:
                            print(log("STOP_RECORDING"))

        #     # send data to arduino HERE

        #     # driver.DriveMotor(
        #     #     ArduMotor.MOTOR_LEFT,
        #     #     data['ML'].direction,
        #     #     data['ML'].power)
        #     # driver.DriveMotor(
        #     #     ArduMotor.MOTOR_RIGHT,
        #     #     data['MR'].direction,
        #     #     data['MR'].power)

        #     # until here

            if args.verbose >= 1:
                MRD = 'F'
                MLD = 'F'
                if data['MR'].direction == model.MotorModel.BACKWARD:
                    MRD = 'B'
                if data['ML'].direction == model.MotorModel.BACKWARD:
                    MLD = 'B'

                # print(log("[ctl][out][left] [Pwr: %03d] [Dir: %s[%s] | [right] [Pwr: %03d] [Dir: %s[%s]" % (data['MR'].power, data['MR'].direction, MRD, data['ML'].power, data['ML'].direction, MLD)))  # NOQA

        olddata = data
        # driver.DriveMotor(
        #     ArduMotor.MOTOR_LEFT,
        #     brake=True)
        # driver.DriveMotor(
        #     ArduMotor.MOTOR_RIGHT,
        #     brake=True)

        # time control
        sample_end_time = time.time()
        time_diff = sample_end_time - sample_start_time
        if time_diff < target_freq:
            time.sleep(target_freq - time_diff)
