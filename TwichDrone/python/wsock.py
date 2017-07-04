import thread
from SimpleWebSocketServer import (
    SimpleWebSocketServer,
    WebSocket
)
import model
from utils import date_message


class WSockHandler(WebSocket):
    def log_message(self):
        return "[WEBSOCKET][%s:%d ".format(
            self.address[0],
            self.address[1]
        )

    def handleMessage(self):
        try:
            model.MODEL.HandleData(self.data, self)
        except Exception as e:
            print "Exception: ", e.message

    def handleConnected(self):
        date_message(self.log_message() + 'Connected')

    def handleClose(self):
        date_message(self.log_message() + 'Closed')


def websocketserver_thread(host='', port=8000):
    server = SimpleWebSocketServer(host, port, WSockHandler)
    server.serveforever()


def websocketserver_start(host='', port=8000):
    thread.start_new_thread(websocketserver_thread, (host, port))


if __name__ == "__main__":
    websocketserver_thread()
