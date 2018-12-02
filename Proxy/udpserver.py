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

    def unpack_message(self, data):
        unpacker = struct.Struct('I 1s I')
        unpacked_data = unpacker.unpack(data)
        first_number, oper, second_number = unpacked_data
        result = self.calculate(oper, first_number, second_number)
        return result

    def handleConnections(self):
        while self.inputs:
            try:
                data = self.server.recvfrom(4096)
                result = self.unpack_message(data)
                self.server.sendall("Hello, I'm udp server.")

            except KeyboardInterrupt:
                print "Close the system"
                for c in self.inputs:
                    c.close()
                self.inputs = []


udpServer = UDPServer()
udpServer.handleConnections()
