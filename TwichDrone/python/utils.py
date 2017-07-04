from datetime import time


def date_message(message):
    timestamp = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
    print "{} {}".format(timestamp, message)
