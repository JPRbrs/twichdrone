#!/usr/bin/python

import threading
import wsock
import model
import argparse
import time
from ardumotor_chip import ArduMotor


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

    driver = ArduMotor(device=args.serialport)

    olddata = None
    ml_amp = 0.0
    mr_amp = 0.0

    target_freq = 1/float(args.frequency)

    while True:
        sample_start_time = time.time()

        stats = {'amp_l': ml_amp, 'amp_r': mr_amp}
        model.MODEL.set_stats(stats)
        model.MODEL.update()
        data = model.MODEL.get_data()

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

            # send data to arduino HERE

            print('[ML][dir]: {}, [ML][pow]: {}, [MR][dir]: {}, [MR][pow]: {}'.format(  # NOQA
                data['ML'].direction,
                data['ML'].power,
                data['MR'].direction,
                data['MR'].power))

            driver.move_motor(
                data['MR'].power,
                data['MR'].direction,
                data['ML'].power,
                data['ML'].direction
            )
            # until here

        olddata = data
        driver.move_motor()

        # time control
        sample_end_time = time.time()
        time_diff = sample_end_time - sample_start_time
        if time_diff < target_freq:
            time.sleep(target_freq - time_diff)
