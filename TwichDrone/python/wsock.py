import time
import thread
from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket
import model


class WSockHandler(WebSocket):

    def handleMessage(self):
        # can't send messages TO client. I don't know why. Try at home.
        try:
            model.MODEL.HandleData(self.data, self)
            # print("wsock: model printdata")
            # model.MODEL.printdata()
            self.sendMessage("TwichDrone ready to rock!")

        except Exception as e:
            print("Exception: {}".format(e.msg))

    def handleConnected(self):
        s = time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())
        print("[WEBSOCKET][%s][%s:%d] Connected" % (
            s,
            self.address[0],
            self.address[1]))

    def handleClose(self):
        s = time.strftime("%Y/%m/%d %H:%M:%S",
                          time.localtime())
        print("[WEBSOCKET][%s][%s:%d] Closed" % (
            s,
            self.address[0],
            self.address[1]))


def websocketserver_thread(
        host='',
        port=8000):
    server = SimpleWebSocketServer(host, port, WSockHandler)
    server.serveforever()


def websocketserver_start(
        host='',
        port=8000):
    thread.start_new_thread(
        websocketserver_thread,
        (host, port))


if __name__ == "__main__":
    websocketserver_thread()
