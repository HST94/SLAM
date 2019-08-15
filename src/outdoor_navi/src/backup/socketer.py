# coding:utf-8
from socket import socket, AF_INET, SOCK_DGRAM


class socket_sender(object):
    def __init__(self, addr, port):
        self.sock = socket(AF_INET, SOCK_DGRAM)
        self.addr = addr
        self.port = port

    def send_data(self, data):
        self.sock.sendto(data, (self.addr, self.port))
