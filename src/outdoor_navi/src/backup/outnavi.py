from outdoor import move_around

class move_base(object):
    def __init__(self):
        self.move_flag = "Start"
        self.nav = move_around()

    def start_move(self):
        while True:
            while self.move_flag == "Start":
                self.nav.go_forward()
        
    def turn_right(self):
        self.nav.turn_right()

    def turn_left(self):
        self.nav.turn_right()

if __name__ == "__main__":
    print "here is main"
    mb = move_base()
    net = upper_socket_server()
    net.start()

