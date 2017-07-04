from goprohero import GoProHero
import logging


class GoProHelper:
    def __init__(self, passwd):
        self.camera = GoProHero(password=passwd,
                                log_level=logging.CRITICAL)

    def Status(self):
        s = self.camera.status()
        if s['raw'] == {}:
            s = {
                'power': 'off',
                'batt1': 0
            }
        return s

    def RecordStart(self):
        self.camera.command('record', 'on')

    def RecordStop(self):
        self.camera.command('record', 'off')
