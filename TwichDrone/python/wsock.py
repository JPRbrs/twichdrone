import model
import thread
import time

from SimpleWebSocketServer import SimpleWebSocketServer, WebSocket


class WebSocketHandler(WebSocket):

    def handleMessage(self):
        try:
            model.MODEL.handle_data(self.data, self)
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


def websocket_server_thread(host='', port=8000):
    server = SimpleWebSocketServer(host, port, WebSocketHandler)
    server.serveforever()


def websocket_server_start(host='', port=8000):
    thread.start_new_thread(websocket_server_thread, (host, port))


if __name__ == "__main__":
    websocket_server_thread()
