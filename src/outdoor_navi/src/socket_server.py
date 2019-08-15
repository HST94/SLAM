from SocketServer import BaseRequestHandler, ThreadingUDPServer
import time
import threading


class Handler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, sock = self.request
        print(msg)  # write control function down here!


class upper_socket_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = ThreadingUDPServer(('', 20000), Handler)

    def run(self):
        self.server.serve_forever()

    def go(self):
        self.setDaemon(True)
        self.start()


if __name__ == '__main__':
    up_ser = upper_socket_server()
    up_ser.go()
    while True:
        print("hello")
        time.sleep(1)
