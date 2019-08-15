from SocketServer import BaseRequestHandler, ThreadingUDPServer
import time
import threading
from outnavi import move_base 
from go_to_specific_point_on_map import *
mv = move_base()
class Handler(BaseRequestHandler):
    def handle(self):
        print('Got connection from', self.client_address)
        # Get message and client socket
        msg, sock = self.request
        print(msg)  # write control function down here!
        if msg == "turn":
            mv.turn_right()
        elif msg == "stop":
            # nav.stop()
            mv.move_flag = "Stop"
        elif msg == "start":
            # nav.go_forward()
            mv.move_flag = "Start"
        else:
             dest = msg.split(':')[-1]
             print dest
             go_somewhere(dest) 


class upper_socket_server(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.server = ThreadingUDPServer(('192.168.20.136', 20000), Handler)

    def run(self):
        self.server.serve_forever()


if __name__ == '__main__':
    up_ser = upper_socket_server()
    up_ser.setDaemon(True)
    up_ser.start()
    if sys.argv[-1] == 'outdoor':
        mv.start_move()
    else:
        while(True):
            pass
