import socket
import sys
import struct


class UDPServer:
    def __init__(self, addr='localhost', port=10000):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server_address = (addr, port)
        # Bind the socket to the port
        self.server.bind(self.server_address)
        # Sockets from which we expect to read
        self.inputs = [self.server]

    def calculate(self, oper, first, second):
        return {
            '+': first + second,
            '-': first - second,
            '*': first * second,
            '/': first / second
        }[oper]

    def handleConnections(self):
        while self.inputs:
            try:
                data, address = self.server.recvfrom(4096)
                unpacker = struct.Struct('I 1s I')
                unpacked_data = unpacker.unpack(data)
                first, oper, second = unpacked_data
                result = self.calculate(oper, first, second)
                self.server.sendto(str(result), address)

            except KeyboardInterrupt:
                print "Close the system"
                for c in self.inputs:
                    c.close()
                self.inputs = []


udpServer = UDPServer()
udpServer.handleConnections()
